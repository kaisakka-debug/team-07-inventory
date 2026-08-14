"""
ฟีเจอร์แจ้งเตือนสต็อกต่ำ และรายงานมูลค่าสต็อก
อ้างอิงจาก spec.md (FR-01 ถึง FR-06, NFR-01 ถึง NFR-03)

ออกแบบตาม Design Notes: แยก business logic (InventoryService)
ออกจาก notification logic (Notifier) ผ่าน interface กลาง
เพื่อให้เพิ่มช่องทางแจ้งเตือนใหม่ได้โดยไม่แก้โค้ดเดิม (NFR-02)
"""

from abc import ABC, abstractmethod
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Dict, List, Optional


DEFAULT_THRESHOLD = 10  # FR-05: ถ้าไม่ระบุ threshold ให้ใช้ค่า default นี้


# ---------------------------------------------------------------------------
# Domain model
# ---------------------------------------------------------------------------

@dataclass
class Product:
    sku: str
    name: str
    quantity: float
    unit_price: float
    category: Optional[str] = None
    threshold: Optional[float] = None  # FR-05: threshold ต่อสินค้า, None = ใช้ default
    channels: List[str] = field(default_factory=list)  # FR-06: เช่น ["email", "sms"]

    @property
    def effective_threshold(self) -> float:
        return self.threshold if self.threshold is not None else DEFAULT_THRESHOLD

    @property
    def category_display(self) -> str:
        # AC US-03: สินค้าไม่มีหมวดหมู่ -> จัดเข้ากลุ่ม "ไม่ระบุหมวดหมู่"
        return self.category if self.category else "ไม่ระบุหมวดหมู่"

    @property
    def value(self) -> float:
        return self.quantity * self.unit_price


class InsufficientStockError(Exception):
    """FR-02: ปฏิเสธรายการจ่ายเมื่อสต็อกไม่พอ"""


# ---------------------------------------------------------------------------
# Notification layer (แยกจาก business logic ตาม NFR-02 / Design Notes)
# ---------------------------------------------------------------------------

class Notifier(ABC):
    """Interface กลางสำหรับช่องทางแจ้งเตือนทุกชนิด"""

    channel_name: str

    @abstractmethod
    def send(self, message: str) -> bool:
        """คืนค่า True ถ้าส่งสำเร็จ, False ถ้าล้มเหลว (ตาม NFR-03)"""
        raise NotImplementedError


class EmailNotifier(Notifier):
    channel_name = "email"

    def send(self, message: str) -> bool:
        # In scope: print แทนการส่งจริง
        print(f"[Email] {message}")
        return True


class SmsNotifier(Notifier):
    channel_name = "sms"

    def send(self, message: str) -> bool:
        print(f"[SMS] {message}")
        return True


class NotificationDispatcher:
    """
    ส่งข้อความไปยังทุกช่องทางที่เปิดใช้งาน (FR-06)
    ถ้าช่องทางใดล้มเหลว ช่องทางอื่นต้องยังทำงานต่อ (NFR-03)
    """

    def __init__(self, notifiers: Dict[str, Notifier]):
        self._notifiers = notifiers  # key = channel_name

    def dispatch(self, channels: List[str], message: str) -> Dict[str, bool]:
        results: Dict[str, bool] = {}
        for channel in channels:
            notifier = self._notifiers.get(channel)
            if notifier is None:
                results[channel] = False
                continue
            try:
                results[channel] = notifier.send(message)
            except Exception:
                # NFR-03: ช่องทางหนึ่งล้มเหลวไม่ทำให้ช่องทางอื่นหยุด
                results[channel] = False
        return results


# ---------------------------------------------------------------------------
# Business logic (ไม่ผูกติดกับ notification โดยตรง - NFR-02)
# ---------------------------------------------------------------------------

class InventoryService:
    def __init__(self, dispatcher: Optional[NotificationDispatcher] = None):
        self._products: Dict[str, Product] = {}
        self._dispatcher = dispatcher

    def add_product(self, product: Product) -> None:
        self._products[product.sku] = product

    def get_product(self, sku: str) -> Product:
        return self._products[sku]

    # FR-01: อัปเดตสต็อกทันทีหลังบันทึกรับเข้า
    def receive_stock(self, sku: str, amount: float) -> Product:
        if amount <= 0:
            raise ValueError("จำนวนรับเข้าต้องมากกว่า 0")
        product = self._products[sku]
        product.quantity += amount
        # AC US-02: การรับเข้าไม่ทำให้สต็อกต่ำกว่า threshold ได้
        # จึงไม่ตรวจ/ไม่ส่งแจ้งเตือนใด ๆ ในรอบนี้ (out of scope: แจ้งเตือน "กลับสู่ปกติ")
        return product

    # FR-01, FR-02, FR-03: บันทึกจ่ายออก + ตรวจสต็อก + แจ้งเตือนถ้าจำเป็น
    def dispatch_stock(self, sku: str, amount: float) -> Product:
        if amount <= 0:
            raise ValueError("จำนวนจ่ายออกต้องมากกว่า 0")

        product = self._products[sku]

        # FR-02: ปฏิเสธถ้าจำนวนที่จ่ายมากกว่าสต็อกคงเหลือ (ไม่อัปเดต, ไม่แจ้งเตือน)
        if amount > product.quantity:
            raise InsufficientStockError(
                f"สต็อกไม่เพียงพอ: มี {product.quantity} แต่ขอจ่าย {amount}"
            )

        product.quantity -= amount

        # FR-03: ใช้ operator "<" เท่านั้น (เท่ากับ threshold ถือว่ายังไม่ต่ำ)
        if product.quantity < product.effective_threshold:
            self._notify_low_stock(product)

        return product

    def _notify_low_stock(self, product: Product) -> None:
        if self._dispatcher is None or not product.channels:
            return
        message = (
            f"สินค้า {product.name} เหลือ {product.quantity} "
            f"(ต่ำกว่า threshold {product.effective_threshold})"
        )
        self._dispatcher.dispatch(product.channels, message)

    # FR-04: รายงานมูลค่าสต็อกแยกตามหมวดหมู่ รวมถึง "ไม่ระบุหมวดหมู่"
    def stock_value_report(self) -> Dict[str, float]:
        report: Dict[str, float] = defaultdict(float)
        for product in self._products.values():
            report[product.category_display] += product.value
        report["รวมทั้งหมด"] = sum(
            v for k, v in report.items() if k != "รวมทั้งหมด"
        )
        return dict(report)


# ---------------------------------------------------------------------------
# ตัวอย่างการใช้งาน / สาธิตตาม Acceptance Criteria ใน spec
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    dispatcher = NotificationDispatcher(
        {"email": EmailNotifier(), "sms": SmsNotifier()}
    )
    service = InventoryService(dispatcher)

    wire = Product(
        sku="WIRE-2.5",
        name="สายไฟ 2.5 sq.mm",
        quantity=20,
        unit_price=15.0,
        category="สายไฟ",
        threshold=15,
        channels=["email", "sms"],
    )
    service.add_product(wire)

    print("--- Scenario: จ่ายจนต่ำกว่า threshold ---")
    service.dispatch_stock("WIRE-2.5", 8)  # เหลือ 12 -> แจ้งเตือน
    print(f"สต็อกคงเหลือ: {wire.quantity}\n")

    print("--- Scenario: boundary case เท่ากับ threshold พอดี (ไม่แจ้งเตือน) ---")
    wire2 = Product("WIRE-2.5B", "สายไฟ 2.5 sq.mm", 20, 15.0, "สายไฟ", 15, ["email"])
    service.add_product(wire2)
    service.dispatch_stock("WIRE-2.5B", 5)  # เหลือ 15 == threshold -> ไม่แจ้งเตือน
    print(f"สต็อกคงเหลือ: {wire2.quantity}\n")

    print("--- Scenario: จ่ายเกินสต็อก (ปฏิเสธ) ---")
    bolt = Product("BOLT-M6", "น็อตหกเหลี่ยม M6", 10, 2.5, "น็อตและสกรู")
    service.add_product(bolt)
    try:
        service.dispatch_stock("BOLT-M6", 20)
    except InsufficientStockError as e:
        print(f"ปฏิเสธรายการ: {e}\n")

    print("--- รายงานมูลค่าสต็อก ---")
    misc = Product("MISC-01", "อุปกรณ์เบ็ดเตล็ด", 30, 10.0, category=None)
    service.add_product(misc)
    for category, value in service.stock_value_report().items():
        print(f"{category}: {value:,.2f} บาท")
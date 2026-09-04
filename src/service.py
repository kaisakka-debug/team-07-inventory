"""
service.py
Business logic ของระบบ inventory (InventoryService)

ไฟล์นี้มีเฉพาะ business logic เท่านั้น: การรับ/จ่ายสินค้า, การคำนวณสต็อก,
การตรวจ threshold, และการคำนวณรายงานมูลค่าสต็อก

InventoryService ไม่รู้จัก EmailNotifier/SMSNotifier โดยตรง (ตามข้อห้ามของโปรเจกต์)
รู้จักเพียง Notifier protocol และ NotifierFactory เท่านั้น (DIP) เพื่อให้ business logic
ไม่ผูกติดกับการแจ้งเตือน (NFR-02) และไม่ปนกับ I/O ในเมธอดเดียวกัน
"""

from __future__ import annotations

from src.models import Product, StockTransaction, TransactionType
from src.notifiers import NotifierFactory


class ProductNotFoundError(Exception):
    """เกิดขึ้นเมื่ออ้างอิงถึงสินค้าที่ไม่มีอยู่ในระบบ"""


class InsufficientStockError(Exception):
    """เกิดขึ้นเมื่อพยายามจ่ายสินค้าออกมากกว่าจำนวนคงเหลือในสต็อก"""


class InventoryService:
    """บริการหลักของระบบ inventory: จัดการสินค้า, รับ/จ่ายสต็อก, และรายงานมูลค่าสต็อก"""

    def __init__(self, notifier_factory: NotifierFactory) -> None:
        """
        สร้าง InventoryService โดยรับ NotifierFactory ผ่าน constructor (Dependency Injection)

        ข้อมูลสต็อกทั้งหมดเก็บอยู่ใน memory เท่านั้น (ตาม In Scope ของ spec)
        """
        self._notifier_factory = notifier_factory
        self._products: dict[str, Product] = {}
        self._transactions: list[StockTransaction] = []

    def add_product(self, product: Product) -> None:
        """เพิ่มสินค้าใหม่เข้าระบบ (หรือแทนที่สินค้าเดิมถ้าชื่อซ้ำ)"""
        self._products[product.name] = product

    def get_product(self, product_name: str) -> Product:
        """
        ดึงข้อมูลสินค้าตามชื่อ

        Raises:
            ProductNotFoundError: ถ้าไม่พบสินค้าที่ชื่อนี้ในระบบ
        """
        product = self._products.get(product_name)
        if product is None:
            raise ProductNotFoundError(f"ไม่พบสินค้า '{product_name}' ในระบบ")
        return product

    def list_products(self) -> list[Product]:
        """คืนรายการสินค้าทั้งหมดในระบบ"""
        return list(self._products.values())

    def receive_stock(self, product_name: str, quantity: int) -> Product:
        """
        บันทึกรับสินค้าเข้าสต็อกและอัปเดตจำนวนคงเหลือทันที (FR-01, US-01)

        การรับเข้าไม่มีทางทำให้สต็อกต่ำกว่า threshold ได้ จึงไม่ตรวจ/ส่งแจ้งเตือนในเมธอดนี้
        (ตาม Out of Scope: ไม่แจ้งเตือน "สต็อกกลับสู่ปกติ")

        Raises:
            ProductNotFoundError: ถ้าไม่พบสินค้า
            ValueError: ถ้าจำนวนที่รับเข้าไม่ใช่ค่าบวก
        """
        if quantity <= 0:
            raise ValueError("จำนวนที่รับเข้าต้องมากกว่า 0")

        product = self.get_product(product_name)
        product.quantity += quantity

        self._transactions.append(
            StockTransaction(
                product_name=product_name,
                transaction_type=TransactionType.IN,
                quantity=quantity,
                resulting_quantity=product.quantity,
            )
        )
        return product

    def issue_stock(self, product_name: str, quantity: int) -> Product:
        """
        บันทึกจ่ายสินค้าออกจากสต็อกและอัปเดตจำนวนคงเหลือทันที (FR-01, US-01)

        ถ้าจำนวนที่จ่ายมากกว่าสต็อกคงเหลือ จะปฏิเสธรายการทั้งหมด: ไม่อัปเดตสต็อก
        ไม่บันทึกรายการ และไม่ส่งการแจ้งเตือนใด ๆ (FR-02)

        ถ้าจ่ายสำเร็จและสต็อกคงเหลือ "น้อยกว่า" threshold ของสินค้านั้น (ใช้ operator '<'
        เท่านั้น ไม่ใช่ '<=') จะส่งการแจ้งเตือนไปยังทุกช่องทางที่เปิดใช้งานสำหรับสินค้านั้น
        ทุกครั้งที่เกิดเหตุการณ์นี้ แม้สต็อกจะต่ำกว่า threshold อยู่แล้วก็ตาม (FR-03)

        Raises:
            ProductNotFoundError: ถ้าไม่พบสินค้า
            ValueError: ถ้าจำนวนที่จ่ายไม่ใช่ค่าบวก
            InsufficientStockError: ถ้าสต็อกคงเหลือไม่พอสำหรับจำนวนที่ขอจ่ายออก
        """
        if quantity <= 0:
            raise ValueError("จำนวนที่จ่ายออกต้องมากกว่า 0")

        product = self.get_product(product_name)

        if quantity > product.quantity:
            raise InsufficientStockError("สต็อกไม่เพียงพอ")

        product.quantity -= quantity

        self._transactions.append(
            StockTransaction(
                product_name=product_name,
                transaction_type=TransactionType.OUT,
                quantity=quantity,
                resulting_quantity=product.quantity,
            )
        )

        if product.is_below_threshold():
            self._notify_low_stock(product)

        return product

    def _notify_low_stock(self, product: Product) -> None:
        """
        ส่งการแจ้งเตือนสต็อกต่ำไปยังทุกช่องทางที่เปิดใช้งานสำหรับสินค้านี้ (FR-06)

        ถ้าช่องทางใดล้มเหลว (สร้าง notifier ไม่ได้ หรือ send() คืนค่า False/raise exception)
        จะข้ามช่องทางนั้นไปแล้วพยายามส่งช่องทางที่เหลือต่อ ไม่กระทบการบันทึกสต็อกที่ทำสำเร็จ
        ไปแล้ว และไม่ทำให้ระบบล้มทั้งหมด (NFR-03)
        """
        message = (
            f"สินค้า {product.name} เหลือ {product.quantity} "
            f"(ต่ำกว่า threshold {product.threshold})"
        )

        for channel_name in product.notification_channels:
            config = product.channel_config.get(channel_name, {})
            try:
                notifier = self._notifier_factory.create(channel_name, **config)
                notifier.send(message)
            except Exception:
                # ช่องทางเดียวล้มเหลวต้องไม่ทำให้ช่องทางอื่นหรือรายการสต็อกล้มไปด้วย
                continue

    def get_stock_value_report(self) -> dict[str, object]:
        """
        คำนวณรายงานมูลค่าสต็อกทั้งหมดแยกตามหมวดหมู่ (FR-04)

        สินค้าที่ไม่ได้ระบุหมวดหมู่จะถูกจัดกลุ่มไว้ในหมวด "ไม่ระบุหมวดหมู่"
        และมูลค่าของสินค้ากลุ่มนี้ก็ยังถูกรวมเข้ากับยอดรวมทั้งหมดด้วย

        Returns:
            dict ที่มี key "by_category" (dict มูลค่ารวมแยกตามหมวดหมู่)
            และ key "total" (มูลค่ารวมทั้งหมดของทุกหมวด) ถ้าไม่มีสินค้าในระบบเลย
            จะคืนค่ามูลค่ารวมเป็น 0 โดยไม่เกิด error
        """
        by_category: dict[str, float] = {}
        total = 0.0

        for product in self._products.values():
            category_name = product.category_name
            by_category[category_name] = by_category.get(category_name, 0.0) + product.total_value
            total += product.total_value

        return {"by_category": by_category, "total": total}

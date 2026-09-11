"""
tests/test_inventory.py
ทดสอบครอบคลุมทุก Acceptance Criteria (Given-When-Then) ใน spec
"""

from __future__ import annotations

import pytest

from src.models import Product
from src.notifiers import NotifierFactory
from src.service import InsufficientStockError, InventoryService, ProductNotFoundError


@pytest.fixture
def factory() -> NotifierFactory:
    return NotifierFactory()


@pytest.fixture
def service(factory: NotifierFactory) -> InventoryService:
    return InventoryService(notifier_factory=factory)


# ---------------------------------------------------------------------------
# AC ของ US-01
# ---------------------------------------------------------------------------

def test_receive_stock_updates_quantity(service: InventoryService):
    """Given สต็อก 100 ตัว, When รับเข้า 50 ตัว, Then สต็อกคงเหลือ 150 ตัว"""
    service.add_product(Product(name="น็อตหกเหลี่ยม M6", unit_price=1.0, quantity=100))

    product = service.receive_stock("น็อตหกเหลี่ยม M6", 50)

    assert product.quantity == 150


def test_issue_stock_insufficient_is_rejected(service: InventoryService):
    """Given สต็อก 10 ตัว, When พยายามจ่าย 20 ตัว, Then ปฏิเสธ สต็อกไม่เปลี่ยน ไม่ส่งแจ้งเตือน"""
    service.add_product(Product(name="น็อตหกเหลี่ยม M6", unit_price=1.0, quantity=10))

    with pytest.raises(InsufficientStockError, match="สต็อกไม่เพียงพอ"):
        service.issue_stock("น็อตหกเหลี่ยม M6", 20)

    product = service.get_product("น็อตหกเหลี่ยม M6")
    assert product.quantity == 10
    assert len(service._transactions) == 0


# ---------------------------------------------------------------------------
# AC ของ US-02
# ---------------------------------------------------------------------------

def test_issue_stock_below_threshold_sends_notification(service: InventoryService, capsys):
    """Given สต็อก 20 threshold 15, When จ่ายออก 8, Then เหลือ 12 และส่งแจ้งเตือนทุกช่องทาง"""
    service.add_product(
        Product(
            name="สายไฟ 2.5 sq.mm",
            unit_price=10.0,
            quantity=20,
            threshold=15,
            notification_channels=["email", "sms"],
            channel_config={
                "email": {"email_address": "manager@example.com"},
                "sms": {"phone_number": "0812345678"},
            },
        )
    )

    product = service.issue_stock("สายไฟ 2.5 sq.mm", 8)

    assert product.quantity == 12
    captured = capsys.readouterr()
    assert "[Email" in captured.out
    assert "[SMS" in captured.out
    assert "สายไฟ 2.5 sq.mm" in captured.out
    assert "12" in captured.out
    assert "15" in captured.out


def test_issue_stock_above_threshold_no_notification(service: InventoryService, capsys):
    """Given สต็อก 50 threshold 15, When จ่ายออก 10, Then เหลือ 40 ไม่ส่งแจ้งเตือน"""
    service.add_product(
        Product(
            name="สายไฟ 2.5 sq.mm",
            unit_price=10.0,
            quantity=50,
            threshold=15,
            notification_channels=["email"],
            channel_config={"email": {"email_address": "manager@example.com"}},
        )
    )

    product = service.issue_stock("สายไฟ 2.5 sq.mm", 10)

    assert product.quantity == 40
    captured = capsys.readouterr()
    assert captured.out == ""


def test_issue_stock_equal_to_threshold_no_notification(service: InventoryService, capsys):
    """boundary case: สต็อกหลังจ่ายเท่ากับ threshold พอดี (15) -> ไม่ถือว่าต่ำกว่า ไม่แจ้งเตือน"""
    service.add_product(
        Product(
            name="สายไฟ 2.5 sq.mm",
            unit_price=10.0,
            quantity=20,
            threshold=15,
            notification_channels=["email"],
            channel_config={"email": {"email_address": "manager@example.com"}},
        )
    )

    product = service.issue_stock("สายไฟ 2.5 sq.mm", 5)

    assert product.quantity == 15
    captured = capsys.readouterr()
    assert captured.out == ""


def test_issue_stock_repeated_below_threshold_notifies_every_time(service: InventoryService, capsys):
    """สต็อกต่ำกว่า threshold อยู่แล้ว (12 < 15) แล้วจ่ายซ้ำ -> ต้องแจ้งเตือนซ้ำอีกครั้ง ไม่ใช่แจ้งครั้งเดียวแล้วเงียบ"""
    service.add_product(
        Product(
            name="สายไฟ 2.5 sq.mm",
            unit_price=10.0,
            quantity=12,
            threshold=15,
            notification_channels=["email"],
            channel_config={"email": {"email_address": "manager@example.com"}},
        )
    )

    product = service.issue_stock("สายไฟ 2.5 sq.mm", 2)

    assert product.quantity == 10
    captured = capsys.readouterr()
    assert "[Email" in captured.out
    assert "10" in captured.out


def test_receive_stock_back_above_threshold_no_notification(service: InventoryService, capsys):
    """การรับเข้าไม่ตรวจ/ส่งแจ้งเตือน 'สต็อกกลับสู่ปกติ' แม้จะพ้น threshold แล้วก็ตาม"""
    service.add_product(
        Product(
            name="สายไฟ 2.5 sq.mm",
            unit_price=10.0,
            quantity=10,
            threshold=15,
            notification_channels=["email"],
            channel_config={"email": {"email_address": "manager@example.com"}},
        )
    )

    product = service.receive_stock("สายไฟ 2.5 sq.mm", 20)

    assert product.quantity == 30
    captured = capsys.readouterr()
    assert captured.out == ""


# ---------------------------------------------------------------------------
# AC ของ US-03
# ---------------------------------------------------------------------------

def test_stock_value_report_by_category(service: InventoryService):
    """รายงานมูลค่าสต็อกแยกตามหมวดหมู่ และยอดรวมทั้งหมด"""
    service.add_product(Product(name="สายไฟ A", unit_price=100.0, quantity=50, category="สายไฟ"))  # 5000
    service.add_product(Product(name="น็อต A", unit_price=6.0, quantity=200, category="น็อตและสกรู"))  # 1200

    report = service.get_stock_value_report()

    assert report["by_category"]["สายไฟ"] == 5000.0
    assert report["by_category"]["น็อตและสกรู"] == 1200.0
    assert report["total"] == 6200.0


def test_stock_value_report_empty_inventory(service: InventoryService):
    """ไม่มีสินค้าในระบบเลย -> มูลค่ารวมเป็น 0 โดยไม่เกิด error"""
    report = service.get_stock_value_report()

    assert report["by_category"] == {}
    assert report["total"] == 0.0


def test_stock_value_report_uncategorized_product(service: InventoryService):
    """สินค้าที่ไม่ได้ระบุหมวดหมู่ -> จัดไว้ในหมวด 'ไม่ระบุหมวดหมู่' และรวมเข้ายอดรวมด้วย"""
    service.add_product(Product(name="อุปกรณ์เบ็ดเตล็ด", unit_price=300.0, quantity=1, category=None))

    report = service.get_stock_value_report()

    assert report["by_category"]["ไม่ระบุหมวดหมู่"] == 300.0
    assert report["total"] == 300.0


# ---------------------------------------------------------------------------
# FR-05: threshold default
# ---------------------------------------------------------------------------

def test_default_threshold_is_ten_when_not_specified(service: InventoryService, capsys):
    """ไม่ระบุ threshold -> ใช้ค่า default = 10"""
    service.add_product(
        Product(
            name="สกรูเกลียวปล่อย",
            unit_price=2.0,
            quantity=15,
            notification_channels=["email"],
            channel_config={"email": {"email_address": "manager@example.com"}},
        )
    )

    product = service.issue_stock("สกรูเกลียวปล่อย", 6)

    assert product.quantity == 9
    assert product.threshold == 10
    captured = capsys.readouterr()
    assert "[Email" in captured.out


# ---------------------------------------------------------------------------
# NFR-03: ช่องทางหนึ่งล้มเหลว ไม่ล้มทั้งระบบ
# ---------------------------------------------------------------------------

def test_one_channel_failure_does_not_block_others_or_transaction(service: InventoryService, capsys):
    """จำลอง SMS ส่งไม่สำเร็จ (ไม่ระบุเบอร์โทร -> สร้าง notifier ไม่ได้) แต่ email ต้องยังส่งได้
    และรายการสต็อกต้องบันทึกสำเร็จตามปกติ"""
    service.add_product(
        Product(
            name="สายไฟ 2.5 sq.mm",
            unit_price=10.0,
            quantity=20,
            threshold=15,
            notification_channels=["email", "sms"],
            channel_config={
                "email": {"email_address": "manager@example.com"},
                # ไม่มี phone_number -> SMSNotifier สร้างไม่สำเร็จ (จำลองความล้มเหลว)
                "sms": {},
            },
        )
    )

    product = service.issue_stock("สายไฟ 2.5 sq.mm", 8)

    assert product.quantity == 12  # รายการสต็อกยังบันทึกสำเร็จ
    captured = capsys.readouterr()
    assert "[Email" in captured.out  # ช่องทางที่เหลือยังส่งได้ตามปกติ
    assert "[SMS" not in captured.out


def test_product_not_found_raises_error(service: InventoryService):
    """เรียกสินค้าที่ไม่มีในระบบ -> ProductNotFoundError"""
    with pytest.raises(ProductNotFoundError):
        service.issue_stock("ไม่มีอยู่จริง", 1)


# ---------------------------------------------------------------------------
# NFR-02 / OCP: เพิ่มช่องทางใหม่ได้โดยไม่แก้ InventoryService
# ---------------------------------------------------------------------------

def test_new_notifier_channel_can_be_registered_without_touching_service(service: InventoryService, factory: NotifierFactory, capsys):
    """จำลองการเพิ่มช่องทางใหม่ (Line) โดย register เข้ากับ factory เท่านั้น ไม่แก้ InventoryService"""

    class LineNotifier:
        def __init__(self, line_id: str) -> None:
            self.line_id = line_id

        def send(self, message: str) -> bool:
            print(f"[Line -> {self.line_id}] {message}")
            return True

    factory.register("line", LineNotifier)

    service.add_product(
        Product(
            name="สายไฟ 2.5 sq.mm",
            unit_price=10.0,
            quantity=20,
            threshold=15,
            notification_channels=["line"],
            channel_config={"line": {"line_id": "U1234"}},
        )
    )

    service.issue_stock("สายไฟ 2.5 sq.mm", 8)

    captured = capsys.readouterr()
    assert "[Line" in captured.out

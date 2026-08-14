"""
models.py
โมเดลข้อมูลของระบบ inventory: Product, Category, StockTransaction
ไฟล์นี้มีเฉพาะโครงสร้างข้อมูล (data model) เท่านั้น ไม่มี business logic
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

# ค่า default threshold เมื่อสินค้าไม่ได้ระบุค่าตั้งเอง (FR-05)
DEFAULT_THRESHOLD: int = 10

# ชื่อหมวดหมู่ที่ใช้แทนสินค้าที่ไม่ได้กำหนดหมวดหมู่ (AC ของ US-03)
UNCATEGORIZED_NAME: str = "ไม่ระบุหมวดหมู่"


class TransactionType(str, Enum):
    """ประเภทของรายการเคลื่อนไหวสต็อก"""

    IN = "IN"
    OUT = "OUT"


@dataclass
class Category:
    """หมวดหมู่ของสินค้า"""

    name: str

    def __post_init__(self) -> None:
        """ตรวจสอบว่าชื่อหมวดหมู่ไม่ว่างเปล่า"""
        if not self.name or not self.name.strip():
            raise ValueError("ชื่อหมวดหมู่ต้องไม่ว่างเปล่า")


@dataclass
class Product:
    """
    สินค้าหนึ่งรายการในสต็อก

    Attributes:
        name: ชื่อสินค้า (ใช้เป็นตัวระบุตัวตนของสินค้าในระบบนี้)
        unit_price: ราคาต่อหน่วย
        quantity: จำนวนคงเหลือปัจจุบัน
        category: ชื่อหมวดหมู่ (None หมายถึงยังไม่ได้ระบุหมวดหมู่)
        threshold: ค่าขั้นต่ำที่ใช้เทียบเพื่อแจ้งเตือนสต็อกต่ำ (ค่า default = 10 ตาม FR-05)
        notification_channels: รายชื่อช่องทางแจ้งเตือนที่เปิดใช้งานสำหรับสินค้านี้ เช่น ["email", "sms"]
        channel_config: ค่า config ของแต่ละช่องทาง เช่น
            {"email": {"email_address": "manager@example.com"},
             "sms": {"phone_number": "0812345678"}}
    """

    name: str
    unit_price: float
    quantity: int = 0
    category: str | None = None
    threshold: int = DEFAULT_THRESHOLD
    notification_channels: list[str] = field(default_factory=list)
    channel_config: dict[str, dict] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """ตรวจสอบความถูกต้องของข้อมูลเบื้องต้น"""
        if not self.name or not self.name.strip():
            raise ValueError("ชื่อสินค้าต้องไม่ว่างเปล่า")
        if self.unit_price < 0:
            raise ValueError("ราคาต่อหน่วยต้องไม่ติดลบ")
        if self.quantity < 0:
            raise ValueError("จำนวนสต็อกเริ่มต้นต้องไม่ติดลบ")

    @property
    def category_name(self) -> str:
        """คืนชื่อหมวดหมู่ที่ใช้แสดงผล (ถ้าไม่ได้ระบุ ให้คืนค่า 'ไม่ระบุหมวดหมู่')"""
        return self.category if self.category else UNCATEGORIZED_NAME

    @property
    def total_value(self) -> float:
        """คำนวณมูลค่ารวมของสินค้านี้ (จำนวน x ราคาต่อหน่วย)"""
        return self.quantity * self.unit_price

    def is_below_threshold(self) -> bool:
        """ตรวจสอบว่าจำนวนคงเหลือปัจจุบัน 'น้อยกว่า' threshold หรือไม่ (ใช้ operator '<' เท่านั้น ตาม FR-03)"""
        return self.quantity < self.threshold


@dataclass
class StockTransaction:
    """บันทึกรายการเคลื่อนไหวสต็อกหนึ่งรายการ (รับเข้า/จ่ายออก)"""

    product_name: str
    transaction_type: TransactionType
    quantity: int
    resulting_quantity: int
    timestamp: datetime = field(default_factory=datetime.now)

    def __post_init__(self) -> None:
        """ตรวจสอบว่าจำนวนที่ทำรายการเป็นค่าบวก"""
        if self.quantity <= 0:
            raise ValueError("จำนวนที่ทำรายการต้องมากกว่า 0")

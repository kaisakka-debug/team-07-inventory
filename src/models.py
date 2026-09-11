"""
models.py
โมเดลข้อมูลของระบบ inventory: Product, Category, StockTransaction
ไฟล์นี้มีเฉพาะโครงสร้างข้อมูล (data model) เท่านั้น ไม่มี business logic
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

DEFAULT_THRESHOLD: int = 10
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
        if not self.name or not self.name.strip():
            raise ValueError("ชื่อหมวดหมู่ต้องไม่ว่างเปล่า")


@dataclass
class Product:
    """สินค้าหนึ่งรายการในสต็อก"""

    name: str
    unit_price: float
    quantity: int = 0
    category: str | None = None
    threshold: int = DEFAULT_THRESHOLD

    def __post_init__(self) -> None:
        if not self.name or not self.name.strip():
            raise ValueError("ชื่อสินค้าต้องไม่ว่างเปล่า")
        if self.unit_price < 0:
            raise ValueError("ราคาต่อหน่วยต้องไม่ติดลบ")
        if self.quantity < 0:
            raise ValueError("จำนวนสต็อกเริ่มต้นต้องไม่ติดลบ")

    @property
    def category_name(self) -> str:
        return self.category if self.category else UNCATEGORIZED_NAME

    @property
    def total_value(self) -> float:
        return self.quantity * self.unit_price

    def is_below_threshold(self) -> bool:
        return self.quantity < self.threshold


@dataclass
class StockTransaction:
    """บันทึกรายการเคลื่อนไหวสต็อกหนึ่งรายการ"""

    product_name: str
    transaction_type: TransactionType
    quantity: int
    resulting_quantity: int
    timestamp: datetime = field(default_factory=datetime.now)

    def __post_init__(self) -> None:
        if self.quantity <= 0:
            raise ValueError("จำนวนที่ทำรายการต้องมากกว่า 0")
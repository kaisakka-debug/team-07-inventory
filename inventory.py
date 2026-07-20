"""
inventory.py
US-01: เขียนฟังก์ชันดึงข้อมูลสินค้าทั้งหมด (get_all_products) -> issue #19
"""

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Product:
    id: str
    name: str
    quantity: int


class Inventory:
    """เก็บรายการสินค้าในระบบแบบ in-memory"""

    def __init__(self, products: Optional[List[Product]] = None):
        self._products: List[Product] = products if products is not None else []

    def add(self, product: Product) -> None:
        """เพิ่มสินค้าเข้าระบบ (ใช้สำหรับเตรียมข้อมูลทดสอบ / เชื่อมกับ US-02 ในอนาคต)"""
        self._products.append(product)

    def get_all_products(self) -> List[Product]:
        """
        คืนรายการสินค้าทั้งหมดในระบบ

        AC-1: ถ้ามีสินค้าอย่างน้อย 1 รายการ -> คืนรายการสินค้าทั้งหมด
              (ชื่อ, รหัส, จำนวนคงเหลือ ครบทุกรายการ)
        AC-2: ถ้ายังไม่มีสินค้าในระบบ -> คืน list ว่าง
              (การแสดงข้อความ "ยังไม่มีสินค้าในระบบ" ทำที่ชั้น UI ใน ui.py)
        """
        return list(self._products)

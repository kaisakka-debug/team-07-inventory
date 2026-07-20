"""
ui.py
US-01: สร้าง UI หน้าตารางแสดงรายการสินค้าพร้อมจำนวนคงเหลือ -> issue #11
"""

from typing import List
from inventory import Product

EMPTY_MESSAGE = "ยังไม่มีสินค้าในระบบ"


def format_products_table(products: List[Product]) -> str:
    """
    แปลงรายการสินค้าเป็นตารางข้อความสำหรับแสดงผล

    AC-1: มีสินค้า -> แสดงชื่อ รหัส และจำนวนคงเหลือครบทุกรายการ
    AC-2: ไม่มีสินค้า -> แสดงข้อความ "ยังไม่มีสินค้าในระบบ" แทนรายการว่าง
    """
    if not products:
        return EMPTY_MESSAGE

    header = f"{'รหัส':<10}{'ชื่อสินค้า':<20}{'จำนวนคงเหลือ':<15}"
    separator = "-" * len(header)
    rows = [
        f"{p.id:<10}{p.name:<20}{p.quantity:<15}"
        for p in products
    ]
    return "\n".join([header, separator, *rows])

"""
ui.py
US-01: สร้าง UI หน้าตารางแสดงรายการสินค้าพร้อมจำนวนคงเหลือ -> issue #11
"""

from typing import List
from inventory import Product

EMPTY_MESSAGE = "ยังไม่มีสินค้าในระบบ"


COLUMNS = [
    ("รหัส", "id", 10),
    ("ชื่อสินค้า", "name", 20),
    ("จำนวนคงเหลือ", "quantity", 14),
]


def _row(values: List[str]) -> str:
    cells = [f" {val:<{width - 1}}" for val, (_, _, width) in zip(values, COLUMNS)]
    return "│" + "│".join(cells) + "│"


def format_products_table(products: List[Product]) -> str:
    """
    แปลงรายการสินค้าเป็นตารางที่มีเส้นขอบสำหรับแสดงผลใน terminal

    AC-1: มีสินค้า -> แสดงชื่อ รหัส และจำนวนคงเหลือครบทุกรายการ
    AC-2: ไม่มีสินค้า -> แสดงข้อความ "ยังไม่มีสินค้าในระบบ" แทนรายการว่าง
    """
    if not products:
        return EMPTY_MESSAGE

    top = "┌" + "┬".join("─" * width for _, _, width in COLUMNS) + "┐"
    header = _row([label for label, _, _ in COLUMNS])
    header_sep = "├" + "┼".join("─" * width for _, _, width in COLUMNS) + "┤"
    rows = [
        _row([str(getattr(p, field)) for _, field, _ in COLUMNS])
        for p in products
    ]
    bottom = "└" + "┴".join("─" * width for _, _, width in COLUMNS) + "┘"

    return "\n".join([top, header, header_sep, *rows, bottom])

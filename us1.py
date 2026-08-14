from tabulate import tabulate
from data_manager import load_products

EMPTY_MESSAGE = "ยังไม่มีสินค้าในระบบ"

# ปรับ COLUMNS ให้ตรงกับโครงสร้างข้อมูลของ us1.py
COLUMNS = [
    ("รหัส", "code", 10),
    ("ชื่อสินค้า", "name", 20),
    ("จำนวนคงเหลือ", "qty", 14),
    ("หน่วย", "unit", 10),
]


def _row(values):
    """สร้างแถวข้อมูลพร้อมจัดรูปแบบตามความกว้างคอลัมน์"""
    cells = [f" {val:<{width - 1}}" for val, (_, _, width) in zip(values, COLUMNS)]
    return "│" + "│".join(cells) + "│"


def format_products_table(products):
    headers = ["รหัส", "ชื่อสินค้า", "จำนวนคงเหลือ", "หน่วย"]
    rows = [
        [
            p.get("code", ""),
            p.get("name", ""),
            p.get("qty", ""),
            p.get("unit", ""),
        ]
        for p in products
    ]
    return tabulate(rows, headers=headers, tablefmt="grid", stralign="left", numalign="right")


def view_all_products():
    """แสดงรายการสินค้าทั้งหมดในรูปแบบตาราง พร้อมจำนวนคงเหลือ"""
    products = load_products()

    print(format_products_table(products))

    if products:
        print(f"\nรวมทั้งหมด {len(products)} รายการ\n")
    else:
        print()
        

if __name__ == "__main__":
    view_all_products()

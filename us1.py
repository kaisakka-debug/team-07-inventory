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
    """แปลงรายการสินค้าเป็นตารางแบบมีกรอบ (UI จาก ui.py)"""
    if not products:
        return EMPTY_MESSAGE

    # สร้างส่วนหัวตาราง
    top = "┌" + "┬".join("─" * width for _, _, width in COLUMNS) + "┐"
    header = _row([label for label, _, _ in COLUMNS])
    header_sep = "├" + "┼".join("─" * width for _, _, width in COLUMNS) + "┤"

    # สร้าง rows
    rows = []
    for p in products:
        warning = "⚠" if p["qty"] <= 5 else ""
        row_values = [
            p["code"],
            p["name"],
            f"{p['qty']} {warning}",
            p["unit"],
        ]
        rows.append(_row(row_values))

    bottom = "└" + "┴".join("─" * width for _, _, width in COLUMNS) + "┘"

    return "\n".join([top, header, header_sep, *rows, bottom])


def view_all_products():
    """แสดงรายการสินค้าทั้งหมดในรูปแบบตาราง พร้อมจำนวนคงเหลือ"""
    products = load_products()

    print("\n" + format_products_table(products))

    if products:
        print(f"\nรวมทั้งหมด {len(products)} รายการ\n")
    else:
        print()
        

if __name__ == "__main__":
    view_all_products()

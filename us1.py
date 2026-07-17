"""
us1.py
------
User Story 1:
"ต้องการดูรายการสินค้าทั้งหมดพร้อมจำนวนคงเหลือ เพื่อตรวจสต็อกได้รวดเร็ว"
"""

from data_manager import load_products


def view_all_products():
    """แสดงรายการสินค้าทั้งหมดในรูปแบบตาราง พร้อมจำนวนคงเหลือ"""
    products = load_products()

    if not products:
        print("\n[!] ยังไม่มีสินค้าในระบบ\n")
        return

    print("\n" + "=" * 60)
    print(f"{'รหัส':<11}{'ชื่อสินค้า':<25}{'จำนวนคงเหลือ':<15}{'หน่วย':<10}")
    print("=" * 60)

    for p in products:
        # เตือนถ้าสินค้าใกล้หมด (จำนวน <= 5) เพื่อให้ตรวจสต็อกได้ง่ายขึ้น
        warning = " ⚠ ใกล้หมด" if p["qty"] <= 5 else ""
        print(f"{p['code']:<10}{p['name']:<21}{p['qty']:<14}{p['unit']:<10}{warning}")

    print("=" * 60)
    print(f"รวมทั้งหมด {len(products)} รายการ\n")


if __name__ == "__main__":
    # เผื่อรันไฟล์นี้เดี่ยว ๆ เพื่อทดสอบ
    view_all_products()

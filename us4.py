"""
us4.py
------
User Story 4:
"ต้องการค้นหาสินค้าด้วยชื่อหรือรหัส เพื่อดูรายละเอียดได้เร็ว"
"""

from data_manager import load_products


def search_product():
    """ค้นหาสินค้าจากรหัสหรือชื่อ (รองรับการค้นหาแบบบางส่วนของชื่อ)"""
    products = load_products()

    if not products:
        print("\n[!] ยังไม่มีสินค้าในระบบ\n")
        return

    print("\n--- ค้นหาสินค้า ---")
    keyword = input("กรอกรหัสหรือชื่อสินค้าที่ต้องการค้นหา: ").strip().lower()

    if not keyword:
        print("[!] กรุณากรอกคำค้นหา\n")
        return

    results = [
        p for p in products
        if keyword in p["code"].lower() or keyword in p["name"].lower()
    ]

    if not results:
        print(f"[!] ไม่พบสินค้าที่ตรงกับ '{keyword}'\n")
        return

    print(f"\nพบสินค้า {len(results)} รายการ:")
    print("=" * 60)
    print(f"{'รหัส':<10}{'ชื่อสินค้า':<25}{'จำนวนคงเหลือ':<15}{'หน่วย':<10}")
    print("=" * 60)
    for p in results:
        print(f"{p['code']:<10}{p['name']:<25}{p['qty']:<15}{p['unit']:<10}")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    search_product()

"""
us3.py
------
User Story 3:
"ต้องการแก้ไขจำนวนสินค้าเมื่อรับหรือจ่ายของ เพื่อให้ยอดคงเหลือถูกต้อง"
"""

from data_manager import load_products, save_products, find_product_by_code


def update_quantity():
    """ปรับจำนวนสินค้า โดยเลือกได้ว่าจะ 'รับเข้า' หรือ 'จ่ายออก'"""
    products = load_products()

    if not products:
        print("\n[!] ยังไม่มีสินค้าในระบบ กรุณาเพิ่มสินค้าก่อน\n")
        return

    print("\n--- แก้ไขจำนวนสินค้า (รับ/จ่าย) ---")
    code = input("รหัสสินค้าที่ต้องการแก้ไข: ").strip()

    product = find_product_by_code(products, code)
    if not product:
        print(f"[!] ไม่พบสินค้ารหัส '{code}'\n")
        return

    print(f"สินค้า: {product['name']}  |  จำนวนคงเหลือปัจจุบัน: {product['qty']} {product['unit']}")

    print("เลือกประเภทการทำรายการ:")
    print("  1. รับเข้า (เพิ่มจำนวน)")
    print("  2. จ่ายออก (ลดจำนวน)")
    action = input("เลือก (1/2): ").strip()

    if action not in ("1", "2"):
        print("[!] กรุณาเลือก 1 หรือ 2 เท่านั้น\n")
        return

    amount_input = input("จำนวนที่ต้องการรับ/จ่าย: ").strip()
    try:
        amount = int(amount_input)
        if amount <= 0:
            raise ValueError
    except ValueError:
        print("[!] จำนวนต้องเป็นตัวเลขจำนวนเต็มบวก\n")
        return

    if action == "1":
        product["qty"] += amount
        print(f"[✓] รับเข้า {amount} {product['unit']} เรียบร้อยแล้ว")
    else:
        if amount > product["qty"]:
            print(f"[!] จำนวนคงเหลือไม่พอ (มีอยู่ {product['qty']} {product['unit']}) ยกเลิกรายการ\n")
            return
        product["qty"] -= amount
        print(f"[✓] จ่ายออก {amount} {product['unit']} เรียบร้อยแล้ว")

    save_products(products)
    print(f"    จำนวนคงเหลือใหม่: {product['qty']} {product['unit']}\n")


if __name__ == "__main__":
    update_quantity()

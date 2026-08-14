"""
us3.py (Merged Version)
------
User Story 3:
"ต้องการแก้ไขจำนวนสินค้าเมื่อรับหรือจ่ายของ เพื่อให้ยอดคงเหลือถูกต้อง"
"""

from data_manager import load_products, save_products, find_product_by_code


def update_quantity(code, action, amount_input):
    """
    Logic สำหรับอัปเดตจำนวนสินค้า
    รับค่าจาก UI: (code, action, amount_input)
    """

    products = load_products()

    if not products:
        print("\n[!] ยังไม่มีสินค้าในระบบ กรุณาเพิ่มสินค้าก่อน\n")
        return

    # หา product จากรหัส
    product = find_product_by_code(products, code)
    if not product:
        print(f"[!] ไม่พบสินค้ารหัส '{code}'\n")
        return

    print(f"\nสินค้า: {product['name']}  |  จำนวนคงเหลือปัจจุบัน: {product['qty']} {product['unit']}")

    # ตรวจ action
    if action not in ("1", "2"):
        print("[!] ประเภทรายการไม่ถูกต้อง (ต้องเป็น 1 หรือ 2)\n")
        return

    # ตรวจจำนวน
    try:
        amount = int(amount_input)
        if amount <= 0:
            raise ValueError
    except ValueError:
        print("[!] จำนวนต้องเป็นตัวเลขจำนวนเต็มบวก\n")
        return

    # ดำเนินการ
    if action == "1":
        product["qty"] += amount
        print(f"[✓] รับเข้า {amount} {product['unit']} เรียบร้อยแล้ว")

    else:  # action == "2"
        if amount > product["qty"]:
            print(f"[!] จำนวนคงเหลือไม่พอ (มีอยู่ {product['qty']} {product['unit']}) ยกเลิกรายการ\n")
            return
        product["qty"] -= amount
        print(f"[✓] จ่ายออก {amount} {product['unit']} เรียบร้อยแล้ว")

    # บันทึกลง database
    save_products(products)
    print(f"    จำนวนคงเหลือใหม่: {product['qty']} {product['unit']}\n")


# ทดสอบร่วมกับ UI
if __name__ == "__main__":
    from ui_update_quantity import prompt_update_quantity   # ← UI ของคุณ

    print("=== เริ่มการทดสอบ UI + Logic (Issue #16 + #17) ===")

    code, action, amount_input = prompt_update_quantity()

    if code is not None:
        update_quantity(code, action, amount_input)

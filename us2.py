"""
us2.py
------
User Story 2:
"ต้องการเพิ่มสินค้าใหม่เข้าระบบ เพื่อให้ข้อมูลสต็อกครบถ้วนเสมอ"
"""

from data_manager import load_products, save_products, is_code_exists


def add_product():
    """รับข้อมูลจากผู้ใช้เพื่อเพิ่มสินค้าใหม่เข้าระบบ"""
    products = load_products()

    print("\n--- เพิ่มสินค้าใหม่ ---")
    code = input("รหัสสินค้า: ").strip()

    if not code:
        print("[!] กรุณากรอกรหัสสินค้า\n")
        return

    if is_code_exists(products, code):
        print(f"[!] รหัสสินค้า '{code}' มีอยู่แล้วในระบบ กรุณาใช้รหัสอื่น\n")
        return

    name = input("ชื่อสินค้า: ").strip()
    if not name:
        print("[!] กรุณากรอกชื่อสินค้า\n")
        return

    qty_input = input("จำนวนเริ่มต้น: ").strip()
    try:
        qty = int(qty_input)
        if qty < 0:
            raise ValueError
    except ValueError:
        print("[!] จำนวนต้องเป็นตัวเลขจำนวนเต็มไม่ติดลบ\n")
        return

    unit = input("หน่วยนับ (เช่น ชิ้น, กล่อง): ").strip() or "ชิ้น"

    new_product = {
        "code": code,
        "name": name,
        "qty": qty,
        "unit": unit,
    }

    products.append(new_product)
    save_products(products)
    
    print("------------------------------------------------")
    print(f"[✓] เพิ่มสินค้า '{name}' (รหัส {code}) เรียบร้อยแล้ว")
    print("------------------------------------------------")


if __name__ == "__main__":
    add_product()

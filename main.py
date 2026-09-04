"""
main.py
-------
โปรแกรมหลักของระบบจัดการสินค้าแบบ command line
เชื่อมโยงการทำงานจากแต่ละ user story (us1.py - us5.py)
"""

# import แบบปลอดภัย เพื่อให้รู้ทันทีว่าไฟล์/ฟังก์ชันไหนมีปัญหา
try:
    from us1 import view_all_products
    from us2 import add_product
    from us3 import update_quantity
    from us4 import search_product
    from us5 import export_csv
except ImportError as e:
    print(f"\n[IMPORT ERROR] ไม่สามารถ import module/function ได้: {e}")
    print("กรุณาตรวจสอบว่าไฟล์ us1.py - us5.py อยู่ในโฟลเดอร์เดียวกับ main.py")
    raise


def show_menu():
    print("\n" + "#" * 45)
    print("#      ระบบจัดการสินค้า (Inventory System)     #")
    print("#" * 45)
    print("1. ดูรายการสินค้าทั้งหมด")
    print("2. เพิ่มสินค้าใหม่")
    print("3. แก้ไขจำนวนสินค้า (รับ/จ่าย)")
    print("4. ค้นหาสินค้า")
    print("5. ส่งออกรายงานสต็อกเป็น CSV")
    print("0. ออกจากโปรแกรม")
    print("-" * 45)


def main():
    actions = {
        "1": ("ดูรายการสินค้าทั้งหมด", view_all_products),
        "2": ("เพิ่มสินค้าใหม่", add_product),
        "3": ("แก้ไขจำนวนสินค้า", update_quantity),
        "4": ("ค้นหาสินค้า", search_product),
        "5": ("ส่งออก CSV", export_csv),
    }

    while True:
        show_menu()
        choice = input("เลือกเมนู: ").strip()

        if choice == "0":
            print("\nขอบคุณที่ใช้บริการ ลาก่อน 👋\n")
            break

        selected = actions.get(choice)
        if not selected:
            print("\n[!] กรุณาเลือกเมนูที่ถูกต้อง (0-5)\n")
            continue

        menu_name, action = selected
        try:
            print(f"\n>> กำลังทำงาน: {menu_name}")

            if choice == "3":
                code = input("รหัสสินค้า: ").strip()
                print("1) รับเข้า")
                print("2) จ่ายออก")
                action_type = input("เลือกประเภท (1/2): ").strip()
                amount_input = input("จำนวน: ").strip()
                action(code, action_type, amount_input)
            else:
                action()

        except Exception as e:
            print(f"\n[ERROR] เกิดข้อผิดพลาดระหว่างทำเมนู '{menu_name}': {e}\n")


if __name__ == "__main__":
    main()

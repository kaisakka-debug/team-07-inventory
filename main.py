"""
main.py
-------
โปรแกรมหลักของระบบจัดการสินค้าแบบ command line
เชื่อมโยงการทำงานจากแต่ละ user story (us1.py - us5.py)
"""

from us1 import view_all_products
from us2 import add_product
from us3 import update_quantity
from us4 import search_product
from us5 import export_csv


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
        "1": view_all_products,
        "2": add_product,
        "3": update_quantity,
        "4": search_product,
        "5": export_csv,
    }

    while True:
        show_menu()
        choice = input("เลือกเมนู: ").strip()

        if choice == "0":
            print("\nขอบคุณที่ใช้บริการ ลาก่อน 👋\n")
            break

        action = actions.get(choice)
        if action:
            action()
        else:
            print("\n[!] กรุณาเลือกเมนูที่ถูกต้อง (0-5)\n")


if __name__ == "__main__":
    main()

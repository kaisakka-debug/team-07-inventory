"""
main.py
CLI สาธิตคำสั่ง 'list' ตามที่ระบุใน AC ของ US-01
"""

from inventory import Inventory, Product
from ui import format_products_table


def main() -> None:
    inventory = Inventory()

    # ตัวอย่าง mock data สำหรับทดลองรัน (ลบ/แก้ไขได้ตามต้องการ)
    # inventory.add(Product(id="P001", name="ปากกา", quantity=50))
    # inventory.add(Product(id="P002", name="ดินสอ", quantity=30))

    print("พิมพ์ 'list' เพื่อดูรายการสินค้าทั้งหมด หรือ 'exit' เพื่อออก")
    while True:
        command = input("> ").strip().lower()
        if command == "list":
            print(format_products_table(inventory.get_all_products()))
        elif command == "exit":
            break
        else:
            print("คำสั่งไม่ถูกต้อง ลองพิมพ์ 'list' หรือ 'exit'")


if __name__ == "__main__":
    main()

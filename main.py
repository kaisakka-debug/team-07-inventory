"""ตัวอย่างการใช้งานระบบคลังสินค้า
ทีม team-07-inventory

รันไฟล์นี้เพื่อดูว่าระบบ Inventory ทำงานได้จริง
    python main.py
"""

from data_manager import Inventory


def main() -> None:
    stock = Inventory()

    # เพิ่มสินค้าเข้าคลัง
    stock.add_item("เสื้อยืดสีขาว", quantity=20, price=150.0)
    stock.add_item("เสื้อยืดสีดำ", quantity=5, price=150.0)
    stock.add_item("กางเกงยีนส์", quantity=0, price=590.0)

    print("=== รายการสินค้าทั้งหมด ===")
    for product in stock.all_items():
        print(f"- {product.name}: เหลือ {product.quantity} ชิ้น (ราคา {product.price} บาท)")

    # ขายสินค้า
    print("\n=== ขายเสื้อยืดสีขาว 3 ชิ้น ===")
    stock.sell("เสื้อยืดสีขาว", 3)
    print(f"คงเหลือ: {stock.get_quantity('เสื้อยืดสีขาว')} ชิ้น")

    # หมายเหตุ: ฟีเจอร์ดูสินค้าใกล้หมด (low_stock_items) ยังไม่ได้เขียน
    # จะเพิ่มด้วยวิธี TDD ตาม Lab 5 ขั้นที่ 2-3
    # ตัวอย่างที่จะใช้ในอนาคต:
    #   for product in stock.low_stock_items(threshold=5):
    #       print(f"ใกล้หมด: {product.name}")


if __name__ == "__main__":
    main()

import pytest

from inventory import Inventory


def test_low_stock_items():
    # 1. Arrange (เตรียมข้อมูล)
    stock = Inventory()
    stock.add_item("เสื้อยืดสีขาว", quantity=20)
    stock.add_item("เสื้อยืดสีดำ", quantity=4)  # ใกล้หมด
    stock.add_item("กางเกงยีนส์", quantity=5)   # ขอบพอดี

    # 2. Act (เรียกใช้งานฟีเจอร์ใหม่ที่ยังไม่เคยมีมาก่อน)
    # สมมติว่าให้ threshold=5 (น้อยกว่าหรือเท่ากับ 5 ถือว่าใกล้หมด)
    low_items = stock.low_stock_items(threshold=5)

    # 3. Assert (ตรวจสอบผลลัพธ์)
    # ดึงชื่อสินค้าออกมาตรวจสอบ ควรจะเจอเสื้อดำกับกางเกงยีนส์
    names = [item.name for item in low_items]
    assert "เสื้อยืดสีดำ" in names
    assert "กางเกงยีนส์" in names
    assert "เสื้อยืดสีขาว" not in names
    assert len(low_items) == 2

# เทสต์ข้อที่ 2: ขายเกินสต็อก (ควรต้องแจ้งเตือน Error ชนิด ValueError)
def test_sell_more_than_stock():
    stock = Inventory()
    stock.add_item("หมวก", quantity=5)
    
    # สั่งให้ pytest เช็คว่าบรรทัดด้านล่างนี้ ต้องเกิด ValueError แน่นอน
    with pytest.raises(ValueError):
        stock.sell("หมวก", quantity=10)

# เทสต์ข้อที่ 4: ขายของที่ไม่มีในคลัง
def test_sell_non_existent_item():
    stock = Inventory()
    
    # สั่งให้ pytest เช็คว่าบรรทัดด้านล่างนี้ ต้องเกิด KeyError แน่นอน
    with pytest.raises(KeyError):
        stock.sell("รองเท้า", quantity=1)
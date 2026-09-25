"""ระบบจัดการสินค้าคงคลัง (Inventory) เบื้องต้น
ทีม team-07-inventory

หมายเหตุ: ไฟล์นี้เป็นโค้ดตั้งต้นแบบง่าย ๆ (เหมือนที่ทีมเขียนไว้ตั้งแต่ต้นเทอม)
ยังไม่มีเมธอด low_stock_items เพราะจะเพิ่มด้วยวิธี TDD ตาม Lab 5 ขั้นที่ 2-3
"""


class Product:
    """สินค้าหนึ่งรายการในคลัง"""

    def __init__(self, name: str, quantity: int, price: float = 0.0):
        self.name = name
        self.quantity = quantity
        self.price = price

    def __repr__(self):
        return f"Product(name={self.name!r}, quantity={self.quantity}, price={self.price})"


class Inventory:
    """คลังสินค้า เก็บสินค้าหลายชิ้น จัดการเพิ่ม/ขาย/ค้นหาสินค้า"""

    def __init__(self):
        self._items: dict[str, Product] = {}

    def add_item(self, name: str, quantity: int, price: float = 0.0) -> None:
        """เพิ่มสินค้าใหม่ หรือเพิ่มจำนวนถ้ามีอยู่แล้ว"""
        if name in self._items:
            self._items[name].quantity += quantity
        else:
            self._items[name] = Product(name, quantity, price)

    def sell(self, name: str, quantity: int) -> None:
        """ขายสินค้า ลดจำนวนคงเหลือ"""
        if name not in self._items:
            raise KeyError(f"ไม่พบสินค้า: {name}")
        
        # เพิ่มการดักจับ: ถ้าสั่งขายเกินจำนวนที่มี ให้แจ้งเตือน ValueError
        if quantity > self._items[name].quantity:
            raise ValueError("จำนวนสินค้าไม่พอขาย")
            
        self._items[name].quantity -= quantity

    def get_quantity(self, name: str) -> int:
        """คืนจำนวนคงเหลือของสินค้าชิ้นหนึ่ง"""
        if name not in self._items:
            raise KeyError(f"ไม่พบสินค้า: {name}")
        return self._items[name].quantity

    def all_items(self) -> list[Product]:
        """คืนรายการสินค้าทั้งหมดในคลัง"""
        return list(self._items.values())

    def low_stock_items(self, threshold: int = 5) -> list[Product]:
        """คืนรายการสินค้าที่มีจำนวนคงเหลือน้อยกว่าหรือเท่ากับ threshold"""
        return [item for item in self._items.values() if item.quantity <= threshold]
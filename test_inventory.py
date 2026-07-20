"""
test_inventory.py
US-01: เขียน Unit Test สำหรับฟังก์ชัน get_all_products -> issue #12
"""

from inventory import Inventory, Product
from ui import format_products_table, EMPTY_MESSAGE


# --- AC-1: มีสินค้าอย่างน้อย 1 รายการ -> คืนครบทุกรายการ ---

def test_get_all_products_returns_all_items():
    inv = Inventory()
    inv.add(Product(id="P001", name="ปากกา", quantity=50))
    inv.add(Product(id="P002", name="ดินสอ", quantity=30))

    result = inv.get_all_products()

    assert len(result) == 2
    assert result[0] == Product(id="P001", name="ปากกา", quantity=50)
    assert result[1] == Product(id="P002", name="ดินสอ", quantity=30)


def test_get_all_products_does_not_mutate_internal_list():
    inv = Inventory()
    inv.add(Product(id="P001", name="ปากกา", quantity=50))

    result = inv.get_all_products()
    result.append(Product(id="P999", name="ของปลอม", quantity=1))

    # แก้ไข list ที่คืนมาแล้วไม่ควรกระทบข้อมูลจริงใน Inventory
    assert len(inv.get_all_products()) == 1


# --- AC-2: ยังไม่มีสินค้าในระบบ -> คืน list ว่าง / UI แสดงข้อความแทน ---

def test_get_all_products_empty_inventory():
    inv = Inventory()

    result = inv.get_all_products()

    assert result == []


def test_table_shows_all_fields_when_items_exist():
    products = [Product(id="P001", name="ปากกา", quantity=50)]

    output = format_products_table(products)

    assert "P001" in output
    assert "ปากกา" in output
    assert "50" in output


def test_table_shows_empty_message_when_no_items():
    output = format_products_table([])

    assert output == EMPTY_MESSAGE

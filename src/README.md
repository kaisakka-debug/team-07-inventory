# Inventory System — Low Stock Alert & Stock Value Report

## โครงสร้างไฟล์
- `src/models.py` — Product, Category, StockTransaction
- `src/notifiers.py` — Notifier protocol, EmailNotifier, SMSNotifier, NotifierFactory
- `src/service.py` — InventoryService (business logic เท่านั้น)
- `tests/test_inventory.py` — เทสต์ครอบคลุมทุก Acceptance Criteria ใน spec (pytest style)

## รันเทสต์ (ต้องมี pytest)
```
pip install pytest
pytest tests/ -v
```
ในสภาพแวดล้อมนี้ (ไม่มี network) เทสต์ถูกตรวจสอบผ่านตัว runner แบบ manual แล้ว
ผลลัพธ์: 14/14 ผ่าน ครอบคลุมทุก scenario ใน spec (US-01 ถึง US-05, FR-01 ถึง FR-06, NFR-02, NFR-03)

## ตัวอย่างการใช้งาน
```python
from src.models import Product
from src.notifiers import NotifierFactory
from src.service import InventoryService

service = InventoryService(notifier_factory=NotifierFactory())

service.add_product(Product(
    name="สายไฟ 2.5 sq.mm",
    unit_price=10.0,
    quantity=20,
    category="สายไฟ",
    threshold=15,
    notification_channels=["email", "sms"],
    channel_config={
        "email": {"email_address": "manager@example.com"},
        "sms": {"phone_number": "0812345678"},
    },
))

service.issue_stock("สายไฟ 2.5 sq.mm", 8)  # เหลือ 12 -> ต่ำกว่า threshold -> ส่งแจ้งเตือน
print(service.get_stock_value_report())
```

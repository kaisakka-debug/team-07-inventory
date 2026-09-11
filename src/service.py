"""
service.py
Business logic ของระบบ inventory (InventoryService)
ใช้ Observer Pattern สำหรับจัดการและกระจายการแจ้งเตือนสต็อกต่ำโดยไม่ขึ้นกับ concrete notifier
"""

from __future__ import annotations

from src.models import Product, StockTransaction, TransactionType
from src.notifiers import Notifier


class ProductNotFoundError(Exception):
    """เกิดขึ้นเมื่ออ้างอิงถึงสินค้าที่ไม่มีอยู่ในระบบ"""


class InsufficientStockError(Exception):
    """เกิดขึ้นเมื่อพยายามจ่ายสินค้าออกมากกว่าจำนวนคงเหลือในสต็อก"""


class InventoryService:
    """บริการหลักของระบบ inventory: จัดการสินค้า, รับ/จ่ายสต็อก, และรายงานมูลค่าสต็อก"""

    def __init__(self) -> None:
        self._products: dict[str, Product] = {}
        self._transactions: list[StockTransaction] = []
        self._observers: list[Notifier] = []

    def add_observer(self, notifier: Notifier) -> None:
        """เพิ่ม observer สำหรับรับการแจ้งเตือน (Observer Pattern)"""
        if notifier not in self._observers:
            self._observers.append(notifier)

    def remove_observer(self, notifier: Notifier) -> None:
        """ลบ observer ออกจากระบบ"""
        if notifier in self._observers:
            self._observers.remove(notifier)

    def _notify_observers(self, message: str) -> None:
        """ส่งข้อความแจ้งเตือนไปยัง Observers ทุกตัวในระบบ (NFR-03)"""
        for observer in self._observers:
            try:
                observer.send(message)
            except Exception:
                continue

    def add_product(self, product: Product) -> None:
        self._products[product.name] = product

    def get_product(self, product_name: str) -> Product:
        product = self._products.get(product_name)
        if product is None:
            raise ProductNotFoundError(f"ไม่พบสินค้า '{product_name}' ในระบบ")
        return product

    def list_products(self) -> list[Product]:
        return list(self._products.values())

    def receive_stock(self, product_name: str, quantity: int) -> Product:
        if quantity <= 0:
            raise ValueError("จำนวนที่รับเข้าต้องมากกว่า 0")

        product = self.get_product(product_name)
        product.quantity += quantity

        self._transactions.append(
            StockTransaction(
                product_name=product_name,
                transaction_type=TransactionType.IN,
                quantity=quantity,
                resulting_quantity=product.quantity,
            )
        )
        return product

    def issue_stock(self, product_name: str, quantity: int) -> Product:
        if quantity <= 0:
            raise ValueError("จำนวนที่จ่ายออกต้องมากกว่า 0")

        product = self.get_product(product_name)

        if quantity > product.quantity:
            raise InsufficientStockError("สต็อกไม่เพียงพอ")

        product.quantity -= quantity

        self._transactions.append(
            StockTransaction(
                product_name=product_name,
                transaction_type=TransactionType.OUT,
                quantity=quantity,
                resulting_quantity=product.quantity,
            )
        )

        if product.is_below_threshold():
            message = (
                f"สินค้า {product.name} เหลือ {product.quantity} "
                f"(ต่ำกว่า threshold {product.threshold})"
            )
            self._notify_observers(message)

        return product

    def get_stock_value_report(self) -> dict[str, object]:
        by_category: dict[str, float] = {}
        total = 0.0

        for product in self._products.values():
            category_name = product.category_name
            by_category[category_name] = by_category.get(category_name, 0.0) + product.total_value
            total += product.total_value

        return {"by_category": by_category, "total": total}
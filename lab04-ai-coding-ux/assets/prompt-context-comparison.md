# Prompt vs Context Comparison - Lab 04

## รอบที่ 1: Prompt สั้น (ไม่มี context)
Prompt: "เขียน function ลด stock แล้วเก็บผลไว้"

ผลลัพธ์ที่ได้: AI เขียนฟังก์ชัน `reduce_stock_in_pv()` แบบ standalone (ไม่ผูกกับ class ใด ๆ) ที่อ่าน/เขียนไฟล์ `.pv` (JSON) ทุกครั้งที่เรียก มี logic ตรวจ FileNotFoundError, JSONDecodeError, หาสินค้าไม่เจอ, สต็อกไม่พอ แล้ว return เป็น `dict` แบบ `{"success": bool, "error": str, ...}` พร้อมสร้าง log การตัดสต็อกเก็บลงไฟล์เดียวกัน (ดูไฟล์โค้ดเต็มที่แนบไว้ก่อนหน้า)
import json
from datetime import datetime
from typing import Dict, Any

def reduce_stock_in_pv(file_path: str, product_id: str, quantity_to_deduct: int, reference_id: str) -> Dict[str, Any]:
    """
    ฟังก์ชันสำหรับลดสต็อกและบันทึกประวัติลงไฟล์ .pv (โครงสร้างข้อมูลแบบ JSON)
    
    :param file_path: Path ของไฟล์ .pv (เช่น 'inventory.pv')
    :param product_id: ID ของสินค้าที่ต้องการลดสต็อก
    :param quantity_to_deduct: จำนวนสินค้าที่ต้องการตัดออก
    :param reference_id: หมายเลขอ้างอิง เช่น Order ID
    :return: dict แสดงสถานะและผลการทำงาน
    """
    try:
        # 1. อ่านข้อมูลจากไฟล์ .pv
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                pv_data = json.load(file)
        except FileNotFoundError:
            return {"success": False, "error": f"ไม่พบไฟล์: {file_path}"}
        except json.JSONDecodeError:
            return {"success": False, "error": "รูปแบบไฟล์ .pv ไม่ถูกต้อง (ไม่ใช่ JSON)"}

        # ตรวจสอบและสร้าง Key สำหรับเก็บข้อมูลหากยังไม่มี
        if "products" not in pv_data:
            pv_data["products"] = []
        if "stock_logs" not in pv_data:
            pv_data["stock_logs"] = []

        # 2. ค้นหาสินค้าตาม product_id
        product = next((p for p in pv_data["products"] if p.get("id") == product_id), None)

        if not product:
            return {"success": False, "error": f"ไม่พบสินค้ารหัส: {product_id}"}

        # 3. ตรวจสอบว่ามีสต็อกเพียงพอหรือไม่
        current_stock = product.get("stock", 0)
        if current_stock < quantity_to_deduct:
            return {
                "success": False, 
                "error": f"สต็อกไม่พอ (คงเหลือ: {current_stock}, ต้องการตัด: {quantity_to_deduct})"
            }

        # 4. คำนวณสต็อกใหม่
        new_stock = current_stock - quantity_to_deduct
        product["stock"] = new_stock

        # 5. สร้าง Log บันทึกประวัติ
        log_entry = {
            "id": f"LOG-{int(datetime.now().timestamp())}",
            "product_id": product_id,
            "action": "DEDUCT",
            "quantity": quantity_to_deduct,
            "remaining_stock": new_stock,
            "reference_id": reference_id,
            "timestamp": datetime.now().isoformat()
        }
        pv_data["stock_logs"].append(log_entry)

        # 6. บันทึกข้อมูลที่อัปเดตแล้วกลับลงไฟล์ .pv
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(pv_data, file, ensure_ascii=False, indent=2)

        return {
            "success": True,
            "product_id": product_id,
            "deducted": quantity_to_deduct,
            "remaining_stock": new_stock,
            "log": log_entry
        }

    except Exception as e:
        return {"success": False, "error": str(e)}


# ==========================================
# ตัวอย่างการใช้งาน (Example Usage)
# ==========================================
if __name__ == "__main__":
    file_name = "inventory.pv"

    # เรียกใช้งานฟังก์ชัน
    result = reduce_stock_in_pv(
        file_path=file_name,
        product_id="PROD-001",
        quantity_to_deduct=2,
        reference_id="ORD-2026-099"
    )

    if result["success"]:
        print("ตัดสต็อกสำเร็จ!")
        print(f"คงเหลือ: {result['remaining_stock']}")
        print("Log บันทึกเรียบร้อย:", result["log"])
    else:
        print("เกิดข้อผิดพลาด:", result["error"])

## รอบที่ 2: Prompt + Context (โค้ดเดิม + เกณฑ์ + ข้อจำกัด)
Prompt: แนบโค้ดเต็มของ `inventory_service.py` (มี `InventoryService`, `InsufficientStockError`, `add_stock`, `get_stock`) พร้อมเกณฑ์ (ต้อง raise `InsufficientStockError` ที่มีอยู่แล้ว, ต้องอัปเดต `self.stock` จริง, ต้องมี type hint/docstring สไตล์เดิม, ต้องจัดการ product_id ที่ไม่เคยมี) และข้อจำกัด (ห้ามใช้ library ภายนอก)
"""
inventory_service.py
โมดูลจัดการสต็อกสินค้าเบื้องต้นสำหรับระบบ inventory
เขียนแบบง่าย ไม่ใช้ library ภายนอก เพื่อใช้เป็นฐานฝึก prompt/context engineering ใน Lab 04
"""

from typing import Dict


class InsufficientStockError(Exception):
    """เกิดขึ้นเมื่อพยายามตัดสต็อกเกินจำนวนที่มีอยู่จริง"""
    pass


class InventoryService:
    """
    จัดการสต็อกสินค้าในหน่วยความจำ (in-memory) ด้วย dict
    key คือ product_id (str), value คือจำนวนคงเหลือ (int)
    """

    def __init__(self) -> None:
        self.stock: Dict[str, int] = {}

    def add_stock(self, product_id: str, quantity: int) -> int:
        """
        เพิ่มจำนวนสต็อกของสินค้า product_id ทีละ quantity ชิ้น
        ถ้ายังไม่เคยมีสินค้านี้ในระบบ จะสร้างรายการใหม่ให้อัตโนมัติ
        คืนค่าจำนวนคงเหลือหลังเพิ่ม

        :raises ValueError: ถ้า quantity เป็นค่าติดลบ
        """
        if quantity < 0:
            raise ValueError("quantity ต้องเป็นค่าบวกหรือศูนย์เท่านั้น")

        current = self.stock.get(product_id, 0)
        self.stock[product_id] = current + quantity
        return self.stock[product_id]

    def get_stock(self, product_id: str) -> int:
        """
        คืนจำนวนสต็อกคงเหลือของ product_id
        ถ้าไม่เคยมีสินค้านี้ในระบบ คืนค่า 0
        """
        return self.stock.get(product_id, 0)

    def reduce_stock(self, product_id: str, quantity: int) -> int:
        """
        ลดจำนวนสต็อกของสินค้า product_id ลงตาม quantity ชิ้น
        อัปเดตค่าสต็อกคงเหลือจริง และคืนค่าจำนวนคงเหลือหลังลด

        :raises ValueError: ถ้า quantity เป็นค่าติดลบ
        :raises InsufficientStockError: ถ้าไม่มีสินค้านี้ในระบบ หรือสต็อกคงเหลือไม่พอตัด
        """
        if quantity < 0:
            raise ValueError("quantity ต้องเป็นค่าบวกหรือศูนย์เท่านั้น")

        current = self.stock.get(product_id, 0)
        
        if current < quantity:
            raise InsufficientStockError(
                f"สต็อกไม่พอ: สินค้า '{product_id}' มีอยู่ {current} ชิ้น แต่ต้องการตัด {quantity} ชิ้น"
            )

        self.stock[product_id] = current - quantity
        return self.stock[product_id]

ผลลัพธ์ที่ได้: AI เพิ่มเมธอด `reduce_stock()` เข้าไปใน class `InventoryService` โดยตรง ใช้ `self.stock` dict เดิม, raise `ValueError` เมื่อ quantity ติดลบ (ตรงกับ pattern ใน `add_stock`), raise `InsufficientStockError` ที่มีอยู่แล้วในไฟล์เมื่อสต็อกไม่พอ (รวมถึงกรณี product_id ไม่เคยมีมาก่อน เพราะ `.get(product_id, 0)` จะได้ 0 แล้วเข้าเงื่อนไขสต็อกไม่พอทันที), docstring ใช้ฟอร์แมต `:raises:` แบบเดียวกับเมธอดอื่นในไฟล์เป๊ะ

## สรุปความต่าง

- **ยึด interface เดิมหรือไม่:** รอบ 1 ไม่ยึดเลย สร้างระบบเก็บข้อมูลใหม่ทั้งหมด (ไฟล์ `.pv` + โครงสร้าง JSON เอง) แยกขาดจาก `InventoryService` ถ้าเอาโค้ดนี้ไปใช้จริงจะกลายเป็นสองระบบสต็อกที่ไม่คุยกัน รอบ 2 เพิ่มเป็นเมธอดในคลาสเดิม ใช้ `self.stock` ตัวเดียวกับที่ `add_stock`/`get_stock` ใช้อยู่แล้ว เรียกใช้ต่อได้ทันที
- **จัดการ error แบบเดียวกับโค้ดเดิมหรือไม่:** รอบ 1 ใช้วิธี return `dict` พร้อม key `success`/`error` ซึ่งเป็นคนละแนวทางกับโค้ดเดิมที่ `add_stock` เลือก raise `ValueError` ตรง ๆ ถ้าเอาทั้งสองมาใช้ในระบบเดียวกัน ผู้เรียกใช้ต้องเขียนโค้ดจัดการ error สองแบบปนกัน รอบ 2 raise exception ตรงตามที่นิยามไว้แล้วในไฟล์ (`InsufficientStockError`) และ `ValueError` แบบเดียวกับ `add_stock` เป๊ะ
- **type hint และ docstring ตรงสไตล์เดิมหรือไม่:** รอบ 1 มี type hint แต่เป็นสไตล์ Sphinx เต็มรูปแบบ (`:param:`, `:return:`) และ return type เป็น `Dict[str, Any]` ซึ่งไม่ตรงกับสไตล์สั้น ๆ ของโค้ดเดิมที่ใช้แค่ประโยคอธิบาย + `:raises:` รอบ 2 เลียนแบบสไตล์เดิมได้ตรงเป๊ะ อ่านแล้วเหมือนเป็นคนเขียนเดียวกัน
- **จัดการ edge case ครบกว่ากันไหม:** รอบ 1 ครบเยอะกว่าในเชิงปริมาณ (ไฟล์หาย, JSON เพี้ยน, สินค้าไม่เจอ, สต็อกไม่พอ) แต่เป็น edge case ของสถาปัตยกรรมที่มันคิดขึ้นเอง ไม่ใช่ของระบบจริง รอบ 2 ครอบคลุม edge case ที่เกี่ยวข้องจริงคือ quantity ติดลบ, สินค้าไม่เคยมีในระบบ (จัดการผ่าน `.get` แล้ว raise error ให้อัตโนมัติ), สต็อกไม่พอ ตรงกับสิ่งที่ระบบนี้ต้องการจริง ๆ
- **สรุปว่าอะไรคือตัวที่ทำให้ต่าง:** คำว่า "เก็บผลไว้" ในรอบ 1 กำกวมมาก AI เลยตีความเป็น "ต้อง persist ลงไฟล์" แล้วสร้างระบบเก็บข้อมูลใหม่ทั้งหมดเพราะไม่เห็นว่ามีระบบเดิมอยู่แล้ว การแนบ **โค้ดเดิมทั้งไฟล์** ทำให้ AI เห็นว่ามี `self.stock` อยู่แล้วและควรอัปเดตตรงนั้น ส่วน **เกณฑ์ที่ระบุ exception ให้ raise ตรงๆ** ตัดความกำกวมเรื่อง error handling ไปเลย และ **ข้อจำกัดห้ามใช้ library ภายนอก** ก็ตัดโอกาสที่ AI จะหยิบเครื่องมือแปลกใหม่มาใช้เกินความจำเป็น สรุปคือ **context ที่แนบไป (โค้ดเดิม + เกณฑ์ + ข้อจำกัด) มีผลมากกว่าการเขียน prompt ให้ยาวขึ้นเฉย ๆ** เพราะมันไปตัดพื้นที่ตีความผิดของ AI ออกทั้งหมด
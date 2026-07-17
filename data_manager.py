"""
data_manager.py
----------------
โมดูลกลางสำหรับจัดการข้อมูลสินค้า (โหลด/บันทึก/โครงสร้างข้อมูล)
ไฟล์ us1.py - us5.py และ main.py จะ import โมดูลนี้ไปใช้ร่วมกัน
เพื่อให้ทุก function อ่าน-เขียนข้อมูลจากแหล่งเดียวกัน (inventory.json)
"""

import json
import os

# ไฟล์เก็บข้อมูลสินค้า (เก็บไว้ที่เดียวกับตัวสคริปต์)
DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "inventory.json")


def load_products():
    """
    โหลดข้อมูลสินค้าทั้งหมดจากไฟล์ JSON
    คืนค่าเป็น list ของ dict เช่น
    [{"code": "P001", "name": "ปากกา", "qty": 10, "unit": "ด้าม"}, ...]
    ถ้ายังไม่มีไฟล์ ให้คืนค่า list ว่าง
    """
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, IOError):
        return []


def save_products(products):
    """
    บันทึกข้อมูลสินค้าทั้งหมดลงไฟล์ JSON
    products: list ของ dict สินค้า
    """
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(products, f, ensure_ascii=False, indent=2)


def find_product_by_code(products, code):
    """ค้นหาสินค้าจาก code แบบตรงตัว (ใช้ภายในหลาย ๆ ที่)"""
    for p in products:
        if p["code"].lower() == code.lower():
            return p
    return None


def is_code_exists(products, code):
    """ตรวจสอบว่ารหัสสินค้านี้มีอยู่แล้วหรือไม่"""
    return find_product_by_code(products, code) is not None

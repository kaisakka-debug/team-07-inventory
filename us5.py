"""
us5.py
------
User Story 5:
"ต้องการส่งออกรายงานสต็อกเป็นไฟล์ CSV เพื่อนำไปทำบัญชีต่อ"
"""

import csv
import os
from datetime import datetime

from data_manager import load_products

# โฟลเดอร์ที่จะเก็บไฟล์รายงาน CSV
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reports")


def export_csv():
    """ส่งออกข้อมูลสินค้าทั้งหมดเป็นไฟล์ CSV พร้อม timestamp ในชื่อไฟล์"""
    products = load_products()

    if not products:
        print("\n[!] ยังไม่มีสินค้าในระบบ ไม่สามารถส่งออกรายงานได้\n")
        return

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"stock_report_{timestamp}.csv"
    filepath = os.path.join(OUTPUT_DIR, filename)

    with open(filepath, "w", newline="", encoding="utf-8-sig") as f:
        # ใช้ utf-8-sig เพื่อให้เปิดด้วย Excel แล้วภาษาไทยไม่เพี้ยน
        writer = csv.writer(f)
        writer.writerow(["รหัสสินค้า", "ชื่อสินค้า", "จำนวนคงเหลือ", "หน่วยนับ"])
        for p in products:
            writer.writerow([p["code"], p["name"], p["qty"], p["unit"]])

    print(f"\n[✓] ส่งออกรายงานสำเร็จ: {filepath}\n")


if __name__ == "__main__":
    export_csv()

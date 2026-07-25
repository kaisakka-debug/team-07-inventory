def prompt_update_quantity():
    """
    UI สำหรับรับค่าการแก้ไขจำนวนสินค้า (Issue #16)
    คืนค่าเป็น (code, action, amount_input) เพื่อส่งต่อให้ Logic (Issue #17)
    """
    print("\n" + "="*40)
    print("   📝 อัปเดตยอดคงเหลือสินค้า")
    print("="*40)
    
    code = input("รหัสสินค้าที่ต้องการแก้ไข (กด Enter เพื่อยกเลิก): ").strip()
    if not code:
        print("❌ ยกเลิกการทำรายการ")
        return None, None, None

    print("\nประเภทการทำรายการ:")
    print("  1. รับเข้า (เพิ่มจำนวน)")
    print("  2. จ่ายออก (ลดจำนวน)")
    action = input("เลือก (1/2): ").strip()

    if action not in ("1", "2"):
        print("❌ กรุณาเลือก 1 หรือ 2 เท่านั้น")
        return None, None, None

    amount_input = input("ระบุจำนวน (ตัวเลข): ").strip()
    
    # ส่งค่าที่ผู้ใช้กรอกกลับไปให้ฟังก์ชันฝั่ง Logic ทำงานต่อ
    return code, action, amount_input
# (โค้ดฟังก์ชัน prompt_update_quantity() ของคุณอยู่ด้านบน...)

# --- เริ่มสคริปต์ทดสอบ ---
if __name__ == "__main__":
    print("=== เริ่มการทดสอบ UI รับค่า (Issue #16) ===")
    
    # 1. เรียกใช้งานฟังก์ชันที่คุณเขียน
    test_code, test_action, test_amount = prompt_update_quantity()
    
    # 2. ปริ้นท์ค่าที่ฟังก์ชันส่งกลับมา เพื่อดูว่าระบบรับค่าไปถูกต้องไหม
    print("\n=== ผลลัพธ์ที่ระบบรับได้ ===")
    print(f"รหัสสินค้า: {test_code}")
    print(f"ประเภทรายการ (1=รับเข้า, 2=จ่ายออก): {test_action}")
    print(f"จำนวน: {test_amount}")
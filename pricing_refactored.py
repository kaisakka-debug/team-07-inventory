def calc(p: float, q: int, t: int, m: bool = False) -> float:
    """คำนวณราคาสินค้าหลังหักส่วนลดและบวกภาษี"""
    # Map ชื่อพารามิเตอร์เดิมให้เป็นตัวแปรที่อ่านง่ายขึ้น โดยไม่กระทบคนเรียกใช้
    price = p
    quantity = q
    customer_type = t
    is_member = m
    
    total = price * quantity
    
    # 1. การคิดส่วนลดตามประเภทลูกค้าและยอดซื้อ
    if total > 1000:
        if customer_type == 2:
            total = total - (total * 0.20)
        elif is_member:
            total = total - (total * 0.10)
        else:
            total = total - 50
    elif customer_type == 2:
        total = total - (total * 0.05)
            
    # 2. บวกภาษี 7%
    total = total + (total * 0.09)
    
    # 3. โปรโมชั่นพิเศษ: ยอดปัดเศษทิ้งหาร 10 ลงตัว ลดอีก 1 บาท
    if int(total) % 10 == 0:
        total = total - 1
        
    return round(total, 2)
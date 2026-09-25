from pricing_refactored import calc


def test_calc_normal_low_price():
    # ราคาไม่เกิน 1000 ลูกค้าทั่วไป (ไม่มีส่วนลด, บวกภาษี 7%)
    assert calc(100, 5, 1) == 535.0

def test_calc_type2_low_price():
    # ราคาไม่เกิน 1000 ลูกค้าประเภท 2 (ลด 5%, บวกภาษี 7%)
    assert calc(100, 5, 2) == 508.25

def test_calc_type2_high_price():
    # ราคาเกิน 1000 ลูกค้าประเภท 2 (ลด 15%, บวกภาษี 7%)
    assert calc(100, 20, 2) == 1819.0

def test_calc_member_high_price():
    # ราคาเกิน 1000 ลูกค้าสมาชิก m=True (ลด 10%, บวกภาษี 7%)
    assert calc(100, 20, 1, m=True) == 1926.0

def test_calc_normal_high_price():
    # ราคาเกิน 1000 ลูกค้าทั่วไป (หักดิบ 50 บาท, บวกภาษี 7%)
    assert calc(100, 20, 1, m=False) == 2086.5

def test_calc_weird_promotion():
    # ราคารวม 150 บาท บวกภาษี 7% = 160.5
    # ปัดเศษทิ้งเหลือ 160 หาร 10 ลงตัวพอดี ต้องโดนหักออก 1 บาทตามกฎแปลกๆ
    assert calc(150, 1, 1) == 159.5
# AI Iteration Log

## รอบที่ 0: เปรียบเทียบ Implement ก่อน vs หลังมี Context (.ai-rules.md)

### Prompt ที่ใช้ (ขั้นที่ 4 - ก่อนมีกฎ)
> จาก spec นี้ ช่วยเขียนโค้ด Python สำหรับฟีเจอร์แจ้งเตือนสต็อกต่ำ [+ spec.md]

ไฟล์ผลลัพธ์: `src/inventory_no_context.py`

### Prompt ที่ใช้ (ขั้นที่ 6 - หลังมีกฎ)
> คุณคือ AI coding agent ของโปรเจกต์นี้ ทำตามกฎใน .ai-rules.md อย่างเคร่งครัด
> implement ฟีเจอร์ตาม spec ด้านล่าง โดยแยกไฟล์ตามที่กฎกำหนด [+ .ai-rules.md + spec.md]

ไฟล์ผลลัพธ์: `src/models.py`, `src/notifiers.py`, `src/service.py`

### ตารางเปรียบเทียบ

| ประเด็น | ก่อนมี context (ขั้นที่ 4) | หลังมี context (ขั้นที่ 6) |
|---|---|---|
| **แยกไฟล์/ความรับผิดชอบ** | โค้ดทั้งหมดอยู่รวมกันในไฟล์เดียว (`inventory_no_context.py`) ไม่มีการแบ่งแยกระหว่าง data model, การแจ้งเตือน และ business logic | แยกเป็น 3 ไฟล์ตามที่กฎกำหนด: `models.py` (Product, Category, StockTransaction), `notifiers.py` (Notifier protocol + EmailNotifier/SMSNotifier + Factory), `service.py` (InventoryService ทำหน้าที่ business logic อย่างเดียว) |
| **type hint + docstring** | ส่วนใหญ่ไม่มี type hint ระบุใน function signature และไม่มี docstring อธิบาย method เลย | ทุก function มี type hint ครบตามที่กฎกำหนด (Python 3.11+) และทุก public method มี docstring ภาษาไทยอธิบายว่าทำอะไร |
| **service ผูกกับ notifier ตรง ๆ หรือไม่** | InventoryService เรียก `print("ส่ง email...")` หรือสร้าง object ของ EmailNotifier/SMSNotifier ตรงในตัวเอง ทำให้เพิ่มช่องทางใหม่ต้องแก้โค้ด service เดิม | InventoryService ไม่รู้จัก EmailNotifier/SMSNotifier โดยตรง แต่รับ notifier ผ่าน constructor (Dependency Injection) และเรียกผ่าน Notifier protocol กลางเท่านั้น เพิ่มช่องทางใหม่ได้โดยไม่แตะ service (ตรงตาม DIP/OCP) |
| **hardcode config หรือไม่** | อีเมล, เบอร์โทร, หรือค่า threshold ถูกเขียนตายตัวอยู่ในโค้ด (hardcode) ไม่สามารถเปลี่ยนได้โดยไม่แก้โค้ด | ไม่มีการ hardcode ค่า config ใด ๆ ในไฟล์ business logic ทุกค่ารับผ่าน constructor หรือ parameter ตอนสร้าง object |
| **Design Pattern** | ไม่มีการใช้ pattern ใด ๆ สร้าง notifier แบบ new object ตรง ๆ | ใช้ Factory pattern (`NotifierFactory`) สร้าง notifier ตามช่องทางที่ต้องการ และใช้แนวคิด Observer-like ผ่าน Notifier protocol สำหรับแจ้งเตือนหลายช่องทาง |

### สรุปผลการเปรียบเทียบ
การให้ AI implement โดยไม่มีไฟล์กฎ (`.ai-rules.md`) ทำให้ได้โค้ดที่ **ทำงานถูกตาม spec ในระดับผิวเผิน** แต่ผิดหลัก
software design ที่สำคัญ (SRP, DIP, OCP) และแก้ไข/ต่อยอดยากในระยะยาว

เมื่อเพิ่ม `.ai-rules.md` เป็น context ก่อนสั่ง implement พบว่า AI ปฏิบัติตามกฎที่ระบุไว้ได้ตรงเกือบทั้งหมด
ทั้งเรื่องการแยกไฟล์, type hint, docstring, การไม่ผูก service กับ notifier ตรง ๆ, ไม่ hardcode config,
และใช้ Factory pattern ตามที่กำหนด

**ข้อสรุป:** การเขียน context/กฎที่ชัดเจนให้ AI ก่อน implement มีผลต่อคุณภาพโค้ดอย่างมีนัยสำคัญ
สอดคล้องกับหลักการของ Spec-Driven Development ที่ว่า "spec/context ที่ดี = โค้ดที่ดี"

---

## รอบที่ 1: Iterate หลังเทส Acceptance Criteria (Boundary Case Handling)

### ผลที่ผิด
เมื่อรันเทสต์กรณีจ่ายสินค้าจนสต็อกเหลือเท่ากับ `threshold` พอดี (เช่น สต็อกเดิม 20, จ่ายออก 5, เหลือ 15 ซึ่ง `threshold = 15`) ระบบกลับส่งข้อความแจ้งเตือนทาง Email และ SMS ออกมา ทั้งที่จริงแล้วสต็อกยังไม่ได้ "ต่ำกว่า" ค่า threshold

### สาเหตุ
[x] Spec กำกวม/ไม่ครอบคลุม
[ ] Context (.ai-rules.md) ไม่ครอบคลุม
[ ] AI ไม่ทำตามกฎที่มีอยู่แล้ว

**รายละเอียด:** ใน `spec.md` เดิมระบุข้อความไว้ว่า *"แจ้งเตือนเมื่อสต็อกลดลงมาถึงระดับ threshold"* ทำให้ AI ตีความว่าเป็นการเปรียบเทียบแบบ `<=` (น้อยกว่าหรือเท่ากับ) แทนที่จะเป็น `<` (น้อยกว่า)

### แก้ที่ต้นทางอย่างไร
ปรับแก้ไขข้อความใน `spec.md` ในส่วน **FR-03** และ **Acceptance Criteria (US-02)** ให้ชัดเจนไร้ความกำกวม:
- ระบุเงื่อนไขทางคณิตศาสตร์อย่างชัดเจน: *"ส่งแจ้งเตือนเฉพาะเมื่อ quantity < threshold เท่านั้น (ใช้ strict inequality `<` ห้ามใช้ `<=`) หากสต็อกเหลือเท่ากับ threshold พอดี ถือว่ายังปลอดภัย ไม่ต้องส่งแจ้งเตือน"*

### Prompt ที่ใช้สั่ง implement ใหม่
> อัปเดต `src/models.py` และ `src/service.py` ตาม `spec.md` ที่แก้ไขใหม่ (FR-03):
> ตรวจสอบให้แน่ใจว่าการเช็คสต็อกต่ำใช้ operator `<` เท่านั้น หากจ่ายสินค้าแล้วสต็อกเหลือเท่ากับ `threshold` พอดี ต้องไม่มีการส่งแจ้งเตือนใด ๆ

### ผลหลังแก้
รันเทสต์ `test_issue_stock_equal_to_threshold_no_notification` ผลปรากฏว่าผ่าน (Pass) สต็อกเหลือ 15 พอดี และไม่มีการ print ข้อความแจ้งเตือนใด ๆ ออกมา

---

## รอบที่ 2: Iterate ครั้งที่ 2 (Fault Tolerance & Channel Failure)

### ผลที่ผิด
เมื่อจำลองสถานการณ์ที่ช่องทาง SMS เกิดข้อผิดพลาด (เช่น ใส่เบอร์โทรศัพท์ว่างเปล่าจนสร้าง `SMSNotifier` ไม่สำเร็จ) ระบบเกิด Unhandled Exception และหยุดทำงานกลางคัน ส่งผลให้ Email แจ้งเตือนไม่ถูกส่ง และรายการจ่ายสินค้าไม่ถูกบันทึกสำเร็จ

### สาเหตุ
[ ] Spec กำกวม/ไม่ครอบคลุม
[x] Context (.ai-rules.md) ไม่ครอบคลุม
[ ] AI ไม่ทำตามกฎที่มีอยู่แล้ว

**รายละเอียด:** ใน `.ai-rules.md` มีกฎเรื่อง DIP/OCP แต่ยังขาดข้อกำหนดเรื่อง Error Handling ในการสื่อสารกับ Notification Layer ที่ชัดเจน ทำให้ AI ไม่ได้ครอบ `try-except` แยกสำหรับแต่ละช่องทางแจ้งเตือน

### แก้ที่ต้นทางอย่างไร
เพิ่มกฎใหม่ลงใน `.ai-rules.md` ในหัวข้อ **Robustness & Fault Tolerance**:
- *"การส่งแจ้งเตือนไปยังหลายช่องทาง ต้องทำการแยก `try-except` สำหรับแต่ละช่องทางโดยเด็ดขาด ความล้มเหลวหรือ exception จากช่องทางใดช่องทางหนึ่ง ห้ามขัดจังหวะการส่งช่องทางอื่น และห้ามทำให้กระบวนการบันทึกสต็อกหลักล้มเหลว"*

### Prompt ที่ใช้สั่ง implement ใหม่
> เพิ่มเติมการจัดการ Error ใน `src/service.py` เมธอด `_notify_low_stock` ตามกฎข้อ Fault Tolerance ใน `.ai-rules.md`:
> ให้วนลูปส่งทีละช่องทางและครอบ `try-except` ภายในลูป หากช่องทางใดเกิด Exception ให้ข้ามไปทำช่องทางถัดไปทันที เพื่อไม่ให้กระทบต่อช่องทางอื่นและการบันทึกสต็อก

### ผลหลังแก้
รันเทสต์ `test_one_channel_failure_does_not_block_others_or_transaction` ผลปรากฏว่าผ่าน (Pass) แม้ SMS จะล้มเหลว แต่ระบบยังส่ง Email ได้สำเร็จ และสต็อกถูกตัดจ่ายสมบูรณ์
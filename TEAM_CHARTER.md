# TEAM_CHARTER.md

## สมาชิกและบทบาท

| ชื่อ | GitHub Username | บทบาท |
|---|---|---|
| Kaisak kabklon  | kaisak gp            | Product Owner |
| Theerut mueangsai  | theerutmu-sudo             | Scrum Master / Developer |
| Piyanuch tangkittipon  | pyxdv             | Scrum Master / Developer |
| Akkadech jaengpromma  | akkadechja             | Developer |
| Kansinee daengtae  | Kansinee-da             | Developer |
| Kittiwin kaeophia  | kittiwinkaeophia            | Developer |


## Branching Strategy

ทีมใช้ GitHub Flow:
- main branch ต้อง deploy ได้เสมอ ห้าม commit โดยตรง
- ทุก feature ใหม่ต้องสร้าง branch ชื่อ feat/<issue-number>-<short-name>
- ทุก PR ต้องมีคนอื่นในทีมอย่างน้อย 1 คน review และ approve ก่อน merge

## Sprint Goal (Sprint 1)
Sprint Goal:
"Sprint นี้ทีมจะส่งมอบระบบจัดการสต็อกสินค้า (US-01, US-02, US-03) ที่พนักงานสามารถดูรายการสินค้า เพิ่มสินค้าใหม่ และอัปเดตยอดคงเหลือได้จริง และผ่าน acceptance criteria ครบถ้วน"
## AI Usage Policy

- ใช้ AI ช่วยเขียน draft code และ draft commit message ได้
- ทุก commit message ที่ AI generate ต้องอ่านและแก้ให้ตรงกับ diff จริงก่อน commit
- ห้าม copy code จาก AI โดยไม่อ่านและทำความเข้าใจก่อน
- ใช้เฉพาะ AI ที่ไม่มีค่าใช้จ่าย ไม่บังคับซื้อ subscription

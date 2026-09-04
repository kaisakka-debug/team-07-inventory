sequenceDiagram
    actor พนักงาน
    participant IS as InventoryService
    participant P as Product
    participant LE as LowStockError (ข้อยกเว้น)
    participant N as Notifier (โปรโตคอล)

    พนักงาน->>IS: issue(สินค้า, จำนวน)
    activate IS
        IS->>P: subtractStock(จำนวน)
        activate P
            P-->>IS: สต็อกที่อัปเดต
        deactivate P
        IS->>P: isStockBelowThreshold()
        activate P
            P-->>IS: true
        deactivate P
        Note right of IS: สต็อกต่ำกว่าขีดจำกัด<br/>เริ่มการแจ้งเตือน
        IS->>IS: generateNotificationMessage(สินค้า)
        Note right of IS: ข้อความ: "สินค้า X<br/>มีสต็อกต่ำ..."
        IS-->>IS: ข้อความแจ้งเตือน
        alt สต็อกเพียงพอ
            IS->>N: send(ข้อความแจ้งเตือน)
            activate N
                Note right of N: ผู้แจ้งเตือนอาจเป็น<br/>อีเมล, SMS, ฯลฯ
                N-->>IS: void
            deactivate N
            IS-->>พนักงาน: void (สำเร็จ)
        else สต็อกไม่เพียงพอ
            Note right of IS: ขว้างข้อยกเว้น<br/>ไม่มีการแจ้งเตือน
            IS-->>พนักงาน: throws LowStockError
        end
    deactivate IS
sequenceDiagram
    autonumber
    actor พนักงาน
    participant IS as InventoryService
    participant P as Product
    participant Obs as Notifier (Observer)

    พนักงาน->>IS: issue_stock("สายไฟ 2.5 sq.mm", 8)
    activate IS
        IS->>IS: get_product("สายไฟ 2.5 sq.mm")
        alt ไม่พบสินค้า
            IS-->>พนักงาน: raise ProductNotFoundError
        end

        alt สต็อกไม่พอ (quantity > P.quantity)
            IS-->>พนักงาน: raise InsufficientStockError
        else สต็อกเพียงพอ
            IS->>P: ลดจำนวนสต็อก (product.quantity -= 8)
            IS->>IS: บันทึก StockTransaction(OUT)
            
            IS->>P: is_below_threshold()
            activate P
                P-->>IS: True
            deactivate P

            opt สต็อกต่ำกว่า threshold (True)
                IS->>IS: _notify_observers(message)
                activate IS
                    loop สำหรับทุก observer ใน _observers
                        IS->>Obs: send(message)
                        activate Obs
                            Note over Obs: แสดงผลการแจ้งเตือน (print)
                            Obs-->>IS: True / False
                        deactivate Obs
                    end
                deactivate IS
            end

            IS-->>พนักงาน: Return Product (อัปเดตสต็อกสำเร็จ)
        end
    deactivate IS
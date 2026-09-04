"""
notifiers.py
ช่องทางแจ้งเตือนทั้งหมดของระบบ inventory

ออกแบบตามหลัก DIP/OCP: InventoryService รู้จักเฉพาะ Notifier protocol และ NotifierFactory
เท่านั้น ไม่รู้จัก EmailNotifier/SMSNotifier โดยตรง เพื่อให้เพิ่มช่องทางใหม่ในอนาคต
(เช่น Line, Push Notification) ได้โดยไม่ต้องแก้ business logic เดิม
"""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class Notifier(Protocol):
    """Interface กลางที่ทุกช่องทางแจ้งเตือนต้อง implement"""

    def send(self, message: str) -> bool:
        """
        ส่งข้อความแจ้งเตือนออกไปยังช่องทางนั้น ๆ

        Returns:
            True ถ้าส่งสำเร็จ, False ถ้าส่งไม่สำเร็จ (ไม่ raise exception
            เพื่อให้ผู้เรียกจัดการความล้มเหลวของแต่ละช่องทางแยกกันได้ตาม NFR-03)
        """
        ...


class EmailNotifier:
    """ช่องทางแจ้งเตือนผ่านอีเมล (จำลองการส่งด้วยการ print แทนการส่งจริงตามข้อกำหนดโปรเจกต์)"""

    def __init__(self, email_address: str) -> None:
        """สร้าง EmailNotifier โดยรับที่อยู่อีเมลปลายทางผ่าน constructor"""
        if not email_address or not email_address.strip():
            raise ValueError("ต้องระบุที่อยู่อีเมลสำหรับ EmailNotifier")
        self.email_address = email_address

    def send(self, message: str) -> bool:
        """จำลองการส่งอีเมล โดย print ข้อความออกทาง console แทนการส่งจริง"""
        try:
            print(f"[Email -> {self.email_address}] {message}")
            return True
        except Exception:
            return False


class SMSNotifier:
    """ช่องทางแจ้งเตือนผ่าน SMS (จำลองการส่งด้วยการ print แทนการส่งจริงตามข้อกำหนดโปรเจกต์)"""

    def __init__(self, phone_number: str) -> None:
        """สร้าง SMSNotifier โดยรับเบอร์โทรศัพท์ปลายทางผ่าน constructor"""
        if not phone_number or not phone_number.strip():
            raise ValueError("ต้องระบุเบอร์โทรศัพท์สำหรับ SMSNotifier")
        self.phone_number = phone_number

    def send(self, message: str) -> bool:
        """จำลองการส่ง SMS โดย print ข้อความออกทาง console แทนการส่งจริง"""
        try:
            print(f"[SMS -> {self.phone_number}] {message}")
            return True
        except Exception:
            return False


class NotifierFactory:
    """
    Factory สำหรับสร้าง instance ของ Notifier ตามชื่อช่องทาง

    ใช้ pattern นี้เพื่อให้ InventoryService ไม่ต้อง import/รู้จัก EmailNotifier
    หรือ SMSNotifier โดยตรง (DIP) และเพิ่มช่องทางใหม่ได้โดยเพียงแค่ register
    class ใหม่เข้ากับ factory โดยไม่ต้องแก้โค้ด business logic เดิม (OCP)
    """

    def __init__(self) -> None:
        """สร้าง factory พร้อม registry เริ่มต้นที่มีช่องทาง email และ sms"""
        self._registry: dict[str, type] = {}
        self.register("email", EmailNotifier)
        self.register("sms", SMSNotifier)

    def register(self, channel_name: str, notifier_cls: type) -> None:
        """ลงทะเบียนช่องทางแจ้งเตือนใหม่เข้ากับ factory"""
        self._registry[channel_name] = notifier_cls

    def create(self, channel_name: str, **config: Any) -> Notifier:
        """
        สร้าง instance ของ notifier ตามชื่อช่องทางที่ระบุ พร้อม config ที่เกี่ยวข้อง

        Raises:
            ValueError: ถ้าไม่รู้จักชื่อช่องทางที่ระบุ
        """
        if channel_name not in self._registry:
            raise ValueError(f"ไม่รู้จักช่องทางแจ้งเตือน: {channel_name}")
        notifier_cls = self._registry[channel_name]
        return notifier_cls(**config)

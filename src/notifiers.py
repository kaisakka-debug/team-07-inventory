"""
notifiers.py
ช่องทางแจ้งเตือนและ NotifierFactory สำหรับสร้าง Notifier (Factory Pattern)
"""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class Notifier(Protocol):
    """Interface กลางที่ทุกช่องทางแจ้งเตือนต้อง implement (DIP)"""

    def send(self, message: str) -> bool:
        ...


class EmailNotifier:
    """ช่องทางแจ้งเตือนผ่านอีเมล"""

    def __init__(self, email_address: str) -> None:
        if not email_address or not email_address.strip():
            raise ValueError("ต้องระบุที่อยู่อีเมลสำหรับ EmailNotifier")
        self.email_address = email_address

    def send(self, message: str) -> bool:
        try:
            print(f"[Email -> {self.email_address}] {message}")
            return True
        except Exception:
            return False


class SMSNotifier:
    """ช่องทางแจ้งเตือนผ่าน SMS"""

    def __init__(self, phone_number: str) -> None:
        if not phone_number or not phone_number.strip():
            raise ValueError("ต้องระบุเบอร์โทรศัพท์สำหรับ SMSNotifier")
        self.phone_number = phone_number

    def send(self, message: str) -> bool:
        try:
            print(f"[SMS -> {self.phone_number}] {message}")
            return True
        except Exception:
            return False


class NotifierFactory:
    """Factory สำหรับสร้าง instance ของ Notifier ตามช่องทางที่ระบุ"""

    _registry: dict[str, type] = {
        "email": EmailNotifier,
        "sms": SMSNotifier,
    }

    @classmethod
    def register(cls, channel_name: str, notifier_cls: type) -> None:
        """ลงทะเบียนช่องทางแจ้งเตือนใหม่เข้ากับ factory"""
        cls._registry[channel_name.lower()] = notifier_cls

    @classmethod
    def create(cls, channel: str, config: dict[str, Any] | None = None) -> Notifier:
        """
        สร้าง Notifier ตามช่องทางและ config ที่ระบุ

        Raises:
            ValueError: ถ้าไม่รู้จักชื่อช่องทางที่ระบุ
        """
        channel_lower = channel.lower()
        if channel_lower not in cls._registry:
            raise ValueError(f"ไม่รู้จักช่องทางแจ้งเตือน: {channel}")

        cfg = config or {}
        notifier_cls = cls._registry[channel_lower]
        return notifier_cls(**cfg)
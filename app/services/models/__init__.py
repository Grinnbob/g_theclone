from umongo import MotorAsyncIOInstance
from .base_class import Base

instance = MotorAsyncIOInstance()

__all__ = [
    "instance",
    "Base"
]
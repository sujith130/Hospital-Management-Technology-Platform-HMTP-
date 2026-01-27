from sqlalchemy import Column, String, Integer, Date, Text
from app.core.base import Base, HospitalIdMixin

class Patient(Base, HospitalIdMixin):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True, nullable=False)
    last_name = Column(String, index=True, nullable=False)
    gender = Column(String)
    date_of_birth = Column(Date)
    phone_number = Column(String, index=True)
    address = Column(Text)
    emergency_contact_name = Column(String)
    emergency_contact_phone = Column(String)

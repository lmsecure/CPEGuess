from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base, engine


class Vendor(Base):
    __tablename__ = "vendor"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, index=True)
    _cpe = relationship("CPE", back_populates="vendor")


class Product(Base):
    __tablename__ = "product"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, index=True)
    _cpe = relationship("CPE", back_populates="product")


class CPE(Base):
    __tablename__ = "cpe"
    id = Column(Integer, primary_key=True)
    part = Column(String(1))
    vendor_id = Column(ForeignKey("vendor.id"))
    product_id = Column(ForeignKey("product.id"))
    version = Column(String, index=True)
    update = Column(String)
    edition = Column(String)
    language = Column(String)
    sw_edition = Column(String)
    target_sw = Column(String)
    target_hw = Column(String)
    other = Column(String)
    vendor = relationship("Vendor", back_populates="_cpe")
    product = relationship("Product", back_populates="_cpe")

    def to_dict(self) -> dict:
        instance = dict()
        instance.update(self.__dict__)
        instance.pop("_sa_instance_state")
        instance.pop("product_id")
        instance.pop("vendor_id")
        instance.pop("id")
        instance["vendor"] = self.vendor.name
        instance["product"] = self.product.name
        return instance

    def to_string(self) -> str:
        return f"cpe:2.3:{self.part}:{self.vendor.name}:{self.product.name}:{self.version}:{self.update}:{self.edition}:{self.language}:{self.sw_edition}:{self.target_sw}:{self.target_hw}:{self.other}"

Base.metadata.create_all(bind=engine)
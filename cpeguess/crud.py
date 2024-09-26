from sqlalchemy.orm import Session
from sqlalchemy import or_, and_,func, Column
from cpeguess import models

COLUMNS = [
    Column(name='vendor'),
    Column(name='product'),
    Column(name='version'),
]

def get_cpe(exact:bool,db: Session, all:bool = False, **kwargs):
    if not exact:
        filters = [column.like(f'%{kwargs.get(column.name)}%') for column in COLUMNS if kwargs.get(column.name, None)]
        data = db.query(func.row_number().over().label('id'),
            models.Vendor.name.label("vendor"),
            models.Product.name.label("product"),
            models.CPE.version.label("version"),
            models.CPE, models.Vendor, models.Product)\
            .join(models.Vendor, models.CPE.vendor_id == models.Vendor.id)\
            .join(models.Product, models.CPE.product_id == models.Product.id)\
            .filter(*filters)
    else:
        filters = [column == kwargs.get(column.name) for column in COLUMNS if kwargs.get(column.name, None)]
        data= db.query(func.row_number().over().label('id'),
                models.Vendor.name.label("vendor"),
                models.Product.name.label("product"),
                models.CPE.version.label("version"),
                models.CPE, models.Vendor, models.Product)\
                .join(models.Vendor, models.CPE.vendor_id == models.Vendor.id)\
                .join(models.Product, models.CPE.product_id == models.Product.id)\
                .filter(*filters)
    return data.all() if all else data.limit(100).all()
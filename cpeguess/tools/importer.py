from cpeguess.schemas.cpe import CPE23
from cpeguess import models
from cpeguess.tools.handler import CPEHandler
from tqdm import tqdm
from cpeguess.tools.parser import XMLParser
from sqlalchemy.orm import sessionmaker


class Importer:
    def __init__(self, path: str, db: sessionmaker):
        self.path = path
        self.data = ()
        self.parser = XMLParser.for_handler(path=path, handler=CPEHandler())
        self.db: sessionmaker = db
        self.counter = 0

    def parse_and_fill(self):
        self.data = list(self.parse())
        self.fill_database()

    def parse(self):
        return self.parser.parse()

    def increment_and_commit(self):
        self.counter += 1
        if self.counter % 5000 == 0:
            self.db.commit()

    def fill_database(self):
        vendors = dict()
        vendor_id_incr = 1
        products = dict()
        product_id_incr = 1
        for i in tqdm(range(len(self.data))):
            try:
                ser_record = CPE23.from_cpe_guesser(self.data[i])
            except Exception as e:
                continue

            dct_record = ser_record.model_dump()
            del dct_record["vendor"]
            del dct_record["product"]
            new_record = models.CPE(**dct_record)

            if vendor_id := vendors.get(ser_record.vendor.name):
                new_record.vendor_id = vendor_id
            else:
                vendors[ser_record.vendor.name] = vendor_id_incr
                new_vendor = models.Vendor(name=ser_record.vendor.name)
                new_record.vendor_id = vendor_id_incr
                vendor_id_incr += 1
                self.db.add(new_vendor)
                self.increment_and_commit()

            if product_id := products.get(ser_record.product.name):
                new_record.product_id = product_id
            else:
                products[ser_record.product.name] = product_id_incr
                new_product = models.Product(name=ser_record.product.name)
                new_record.product_id = product_id_incr
                product_id_incr += 1
                self.db.add(new_product)
                self.increment_and_commit()

            self.db.add(new_record)
            self.increment_and_commit()
        self.db.commit()

from pydantic import BaseModel


class Vendor(BaseModel):
    name: str


class Product(BaseModel):
    name: str


class CPE23(BaseModel):
    part: str
    vendor: Vendor
    product: Product
    version: str
    update: str
    edition: str
    language: str
    sw_edition: str
    target_sw: str
    target_hw:str
    other: str

    @classmethod
    def from_cpe_guesser(cls, data: str):
        values = data.replace("\:","~")
        part, vendor, \
            product, version, \
            update, edition, \
            language, sw_edition, \
            target_sw, target_hw, other = values.split("cpe:2.3:")[1].split(":")

        return cls(part=part,
                   vendor=Vendor(name=vendor.replace("~",":")),
                   product=Product(name=product.replace("~",":")),
                   version=version,
                   update=update,
                   edition=edition,
                   language=language,
                   sw_edition=sw_edition,
                   target_sw=target_sw,
                   target_hw=target_hw,
                   other=other)

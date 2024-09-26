from cpeguess.database import get_db
from cpeguess import crud

class CPEGuess:
    @classmethod
    def search(cls, product:str, vendor:str, version:str, exact:bool = False, format="string"):
        cpes = crud.get_cpe(product=product,vendor=vendor, version=version,exact = exact, db=next(get_db()))
        if format == "dict":
            return [cpe.CPE.to_dict() for cpe in cpes]
        if format == "string":
            return [cpe.CPE.to_string() for cpe in cpes]
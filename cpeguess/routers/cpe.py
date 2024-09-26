from fastapi import APIRouter
from cpeguess.schemas.cpe import CPE23
from sqlalchemy.orm import Session
from fastapi import Depends
from cpeguess.database import get_db
from cpeguess import crud
from fastapi.params import Query
import enum

router = APIRouter(prefix="/api/v1/cpe", tags=["CPERouter"])


class Formatter(str, enum.Enum):
    string = "string"
    dct = "dict"


@router.get("/", response_model=list[dict] | list[str])
def get_cpes(product: str, version: str, vendor: str = "", exact: bool = False,
             format: Formatter = Query(default="dict"), db: Session = Depends(get_db)):
    cpes = crud.get_cpe(product=product, vendor=vendor,
                        version=version, exact=exact, db=db)
    if format == "dict":
        return [cpe.CPE.to_dict() for cpe in cpes]
    if format == "string":
        return [cpe.CPE.to_string() for cpe in cpes]
    raise

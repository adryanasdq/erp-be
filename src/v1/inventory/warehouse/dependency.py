from datetime import datetime
from fastapi import Depends
from sqlmodel import Session as SessionType

from src.core.settings.database import get_session
from src.core.models.inventory.warehouse import Warehouse as DbWarehouse
from src.core.schemas.inventory.warehouse import Warehouse

from .exception import WarehouseIdExists, WarehouseNotFound


def check_if_warehouse_exists(warehouse_id: str, session: SessionType):
    db_warehouse = session.get(DbWarehouse, warehouse_id)
    if db_warehouse:
        raise WarehouseIdExists()
    return


def get_warehouse_by_id(
    id: str, session: SessionType = Depends(get_session)
):
    db_warehouse = session.get(DbWarehouse, id)
    if not db_warehouse:
        raise WarehouseNotFound()
    return db_warehouse


def validate_warehouse(warehouse: Warehouse, session: SessionType, id: str = None):
    if not id:
        db_warehouse = DbWarehouse(
            **warehouse.model_dump(exclude_unset=True, exclude={"id"})
        )
    else:
        db_warehouse = get_warehouse_by_id(id, session)
        for key, attr in warehouse.model_dump(exclude_unset=True).items():
            setattr(db_warehouse, key, attr)

    db_warehouse.modified_date = datetime.now()
    return db_warehouse
from datetime import datetime
from fastapi import Depends
from sqlalchemy.orm import Session as SessionType

from src.core.settings.database import get_session
from src.core.models.hr.position import Position as DbPosition
from src.core.schemas.hr.position import Position
from src.utils import generate_custom_id
from src.v1.hr.department.dependency import get_department_by_id

from .exception import PositionIdExists, PositionNotFound


def check_if_position_exists(pos_id: str, session: SessionType):
    db_pos = session.get(DbPosition, pos_id)
    if db_pos:
        raise PositionIdExists()
    return


def get_position_by_id(
    pos_id: str, session: SessionType = Depends(get_session)
):
    db_pos = session.get(DbPosition, pos_id)
    if not db_pos:
        raise PositionNotFound()
    return db_pos


def validate_position(pos: Position, session: SessionType, id: str = None):
    get_department_by_id(pos.department_id, session)

    if id is None:
        pos.id = generate_custom_id("pos", session)
        check_if_position_exists(pos.id, session)
        db_pos = DbPosition(
            id=pos.id, **pos.model_dump(exclude_unset=True, exclude={"id"})
        )
    else:
        db_pos = get_position_by_id(id, session)
        for key, attr in pos.model_dump(exclude_unset=True).items():
            setattr(db_pos, key, attr)

    db_pos.modified_date = datetime.now()
    return db_pos
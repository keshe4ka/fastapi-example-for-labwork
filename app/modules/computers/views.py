from fastapi import APIRouter, Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from starlette import status

from app.core.db import get_session
from app.models import Computer
from app.modules.computers.schema import ComputerCreate, ComputerRead

router = APIRouter(prefix='/computer')


@router.post('/create', response_model=ComputerRead,
             status_code=status.HTTP_200_OK)
def create_computer(
        data: ComputerCreate,
        db: Session = Depends(get_session)
):
    computer = Computer(**data.dict())

    try:
        db.add(computer)
        db.commit()
        db.refresh(computer)
    except IntegrityError:
        db.rollback()
        return ComputerRead(
            error='User is not exist',
            **computer.to_dict()
        )

    return ComputerRead(
        user=computer.user.to_dict(),
        **computer.to_dict()
    )

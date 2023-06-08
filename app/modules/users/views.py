from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from starlette import status

from app.core.db import get_session
from app.models import User
from app.modules.users.schema import UserRead, UserUpdate

router = APIRouter(prefix='/user')


@router.post('/create', status_code=status.HTTP_200_OK)
def create_user(
        name: str,
        email: str,
        db: Session = Depends(get_session)
):
    user = User(name=name, email=email)

    try:
        db.add(user)
        db.commit()
    except IntegrityError:
        db.rollback()
        return status.HTTP_500_INTERNAL_SERVER_ERROR

    return user.to_dict()


@router.get('/{id}', status_code=status.HTTP_200_OK)
def get_user(
        id: int,
        db: Session = Depends(get_session)
):
    user = db.get(User, id)

    # способ с явным созданием запроса:
    # query = select(User).where(User.id == id) <- здесь мы ничего не получаем, это просто запрос!
    # user = db.scalars(query).first() <- а вот здесь уже выполнили наш запрос в базе

    if not user:
        return status.HTTP_404_NOT_FOUND
    return user.to_dict()


@router.get('/all', status_code=status.HTTP_200_OK)
def get_users(
        # в случае, если параметр name не был задан - мы присваиваем ему значение None
        name: str = None,
        db: Session = Depends(get_session)
):
    query = select(User)

    if name:
        query = query.where(User.name == name)

    users = db.scalars(query).all()

    return [user.to_dict() for user in users]


# Обратите внимание, что здесь мы используем pydantic модели во входных данных,
# а также указываем параметр response_model.
# Посмотрите, как это выглядит в /docs
@router.put('/update', response_model=UserRead, status_code=status.HTTP_200_OK)
def update_user(
        id: int,
        data: UserUpdate,
        db: Session = Depends(get_session)
):
    user = db.get(User, id)

    values = data.dict()  # здесь мы преобразуем pydantic модель в словарь
    user.update(**values)

    # будет исключение, если мы укажем уже существующую в системе почту
    try:
        db.add(user)
        db.commit()
    except IntegrityError:
        db.rollback()

    return user.to_dict()

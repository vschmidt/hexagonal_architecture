from sqlalchemy import insert, select

from src.entities.users.models import UserModel
from src.entities.users.schemas import UserInDBSchema
from src.infrastructure.postgres.database import PostgresDatabase


class UserRepository:
    @classmethod
    def create_new_user(cls, user: UserInDBSchema):
        with PostgresDatabase() as engine:
            engine.session.execute(insert(UserModel).values(**user.dict()))
            engine.session.commit()

    @classmethod
    def get_user_by_cpf(cls, cpf: str) -> UserInDBSchema:
        user = None

        with PostgresDatabase() as engine:
            result = engine.session.execute(
                select(UserModel).where(UserModel.cpf == cpf)
            ).first()

            if result:
                user = UserInDBSchema(**result[0].to_dict())

        return user

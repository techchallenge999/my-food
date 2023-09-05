from uuid import UUID
from src.infrastructure.postgresql.models.user import UserModel


def init_db() -> None:
    user = UserModel.list()
    if len(user) == 0:
        user = UserModel(
            cpf="03476846024",
            email="email@email.com",
            name="Fulano",
            password="SenhaFulano",
            is_admin=True,
            uuid=UUID("58ebc052-d023-4e31-8379-3fc0ff822368"),
        )
        user.create()

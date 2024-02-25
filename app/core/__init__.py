from .config import AuthJWT, DatabaseFactory
from .settings import settings

auth_jwt = AuthJWT()

db_factory = DatabaseFactory(settings.db_url)

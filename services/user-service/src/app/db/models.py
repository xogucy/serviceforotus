"""Import ORM models here so Alembic can discover metadata."""

from app.modules.users.models import User

__all__ = ["User"]

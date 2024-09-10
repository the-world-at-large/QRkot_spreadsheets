from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models import CharityProject
from constants import PAGE_NOT_FOUND_CODE


async def get_project_or_404(
    charity_project_id: int,
    session: AsyncSession,
) -> CharityProject:
    charity_project = await charity_project_crud.get_project_by_id(
        charity_project_id, session,
    )
    if not charity_project:
        raise HTTPException(
            status_code=PAGE_NOT_FOUND_CODE,
            detail='Проект не найден.',
        )
    return charity_project

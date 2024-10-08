from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject
from app.schemas.charity_project import (CharityProjectCreate,
                                         CharityProjectUpdate)


class CRUDCharityProject(CRUDBase):

    async def create_project(
        self,
        obj_in: CharityProjectCreate,
        session: AsyncSession,
    ) -> CharityProject:
        obj_in_data = obj_in.dict()
        return await self.create(obj_in_data, session)

    async def update_project(
        self,
        db_obj: CharityProject,
        obj_in: CharityProjectUpdate,
        session: AsyncSession,
    ) -> CharityProject:
        db_obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)
        for field in db_obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def remove_project(
        self,
        db_obj: CharityProject,
        session: AsyncSession,
    ) -> CharityProject:
        await session.delete(db_obj)
        await session.commit()
        return db_obj

    async def get_id_by_name(
        self,
        project_name: str,
        session: AsyncSession,
    ) -> Optional[int]:
        db_project_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == project_name,
            )
        )
        return db_project_id.scalars().first()

    async def get_project_by_id(
        self,
        project_id: int,
        session: AsyncSession,
    ) -> Optional[CharityProject]:
        db_project = await session.execute(
            select(CharityProject).where(
                CharityProject.id == project_id,
            )
        )
        return db_project.scalars().first()

    async def get_projects_by_completion_rate(
        self,
        session: AsyncSession,
    ) -> Optional[list[dict[str, str]]]:
        projects = await session.execute(
            select(CharityProject).where(CharityProject.fully_invested)
        )
        projects = projects.scalars().all()
        finished_projects = []
        for proj in projects:
            finished_projects.append(
                {
                    'name': proj.name,
                    'description': proj.description,
                    'project_timeline': proj.close_date - proj.create_date,
                }
            )
        return sorted(finished_projects, key=lambda x: (x['project_timeline']))


charity_project_crud = CRUDCharityProject(CharityProject)

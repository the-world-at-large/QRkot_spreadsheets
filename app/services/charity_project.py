from datetime import datetime

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.utils import get_project_or_404
from app.crud.charity_project import charity_project_crud
from app.models import CharityProject, Donation
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectUpdate,
)
from constants import (
    BAD_REQUEST_CODE,
    UNPROCESSABLE_ENTITY,
)


class CharityProjectService:
    def __init__(
        self, session: AsyncSession,
    ):
        self.session = session

    async def check_project_name(
        self,
        project_name: str,
    ) -> None:
        project_id = await charity_project_crud.get_id_by_name(
            project_name, self.session,
        )
        if project_id:
            raise HTTPException(
                status_code=BAD_REQUEST_CODE,
                detail='Проект с таким именем уже существует.',
            )

    def check_project_activeness(
        self,
        charity_project: CharityProject,
    ) -> None:
        if charity_project.fully_invested:
            raise HTTPException(
                status_code=BAD_REQUEST_CODE,
                detail='Нельзя редактировать закрытый проект.',
            )

    def check_project_investment(
        self,
        charity_project: CharityProject,
    ) -> None:
        if charity_project.invested_amount:
            raise HTTPException(
                status_code=BAD_REQUEST_CODE,
                detail='Нельзя удалить проект с уже внесёнными средствами.',
            )

    def check_amount_update(
        self,
        obj_in_full_amount: int,
        actual_amount: int,
    ) -> None:
        if obj_in_full_amount < actual_amount:
            raise HTTPException(
                status_code=UNPROCESSABLE_ENTITY,
                detail='Нельзя установить сумму, меньшую вложенной.',
            )

    async def create_project(
        self,
        project: CharityProjectCreate,
    ) -> CharityProject:
        await self.check_project_name(
            project.name,
        )
        new_project = await charity_project_crud.create_project(
            project, self.session,
        )
        new_project = await self.donation_process(
            new_project, Donation
        )
        await self.session.commit()
        await self.session.refresh(new_project)
        return new_project

    async def update_project(
        self,
        project: CharityProject,
        obj_in: CharityProjectUpdate,
    ) -> CharityProject:
        project = await get_project_or_404(
            project.id, self.session,
        )
        self.check_project_activeness(project)
        if obj_in.name:
            await self.check_project_name(
                obj_in.name,
            )
        if not obj_in.full_amount:
            project = await charity_project_crud.update_project(
                project, obj_in, self.session,
            )
            await self.session.commit()
            await self.session.refresh(project)
            return project
        self.check_amount_update(
            obj_in.full_amount, project.invested_amount,
        )
        charity_project = await charity_project_crud.update_project(
            project, obj_in, self.session,
        )
        charity_project = await self.donation_process(
            project, Donation,
        )
        await self.session.commit()
        await self.session.refresh(charity_project)
        return charity_project

    async def remove_project(
        self,
        project: CharityProject,
    ) -> CharityProject:
        project = await get_project_or_404(
            project.id, self.session,
        )
        self.check_project_investment(project)
        project = await charity_project_crud.remove_project(
            project, self.session,
        )
        await self.session.commit()
        return project

    async def get_all_projects(
        self,
    ) -> list[CharityProject]:
        projects = await charity_project_crud.get_multi(self.session)
        return projects

    async def donation_process(
        self,
        obj_in: CharityProject,
        model_db: Donation,
    ) -> CharityProject:
        source_db_all = (await self.session.execute(
            select(model_db).where(
                model_db.fully_invested == False  # noqa
            ).order_by(model_db.create_date)
        )).scalars().all()

        for source_db in source_db_all:
            obj_in, source_db = await self.money_distribution(
                obj_in, source_db,
            )
            self.session.add(obj_in)
            self.session.add(source_db)

        await self.session.commit()
        await self.session.refresh(obj_in)
        return obj_in

    def close_entity(
        self,
        obj_db: CharityProject,
    ) -> CharityProject:
        obj_db.invested_amount = obj_db.full_amount
        obj_db.fully_invested = True
        obj_db.close_date = datetime.now()
        return obj_db

    async def money_distribution(
        self,
        obj_in: CharityProject,
        obj_db: Donation,
    ) -> tuple[CharityProject, Donation]:
        rem_obj_in = obj_in.full_amount - obj_in.invested_amount
        rem_obj_db = obj_db.full_amount - obj_db.invested_amount

        if rem_obj_in > rem_obj_db:
            obj_in.invested_amount += rem_obj_db
            obj_db = self.close_entity(obj_db)
        elif rem_obj_in == rem_obj_db:
            obj_in = self.close_entity(obj_in)
            obj_db = self.close_entity(obj_db)
        else:
            obj_db.invested_amount += rem_obj_in
            obj_in = self.close_entity(obj_in)

        return obj_in, obj_db

from fastapi import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from src.core.models.hr.department import Department as DbDepartment
from src.core.schemas.hr.department import Department


class DepartmentService:
    def __init__(self, session: AsyncSession):
        self.session = session


    async def get_all_departments(self):
        stmnt = select(DbDepartment)

        result = await self.session.exec(stmnt)
        return result.all()
    
    
    async def get_department_by_id(self, department_id: str):
        stmnt = select(DbDepartment).where(DbDepartment.id == department_id)

        result = await self.session.exec(stmnt)
        return result.first()
    

    async def create_department(self, department: DbDepartment):
        try:
            self.session.add(department)
            await self.session.commit()
            await self.session.refresh(department)
            return Department.model_validate(department)
        except Exception as e:
            self.session.rollback()
            raise HTTPException(status_code=400, detail=str(e))
    

    async def update_department(self, department: DbDepartment):
        try:
            await self.session.commit()
            await self.session.refresh(department)
            return Department.model_validate(department)
        except Exception as e:
            self.session.rollback()
            raise HTTPException(status_code=400, detail=str(e))
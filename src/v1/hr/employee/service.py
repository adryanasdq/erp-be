from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from src.core.models.hr.employee import Employee


class EmployeeService:
    def __init__(self, session: AsyncSession):
        self.session = session


    async def get_all_employees(self):
        stmnt = select(Employee)

        result = await self.session.exec(stmnt)
        return result.all()
    
    
    async def get_employee_by_id(self, employee_id: str):
        stmnt = select(Employee).where(Employee.id == employee_id)

        result = await self.session.exec(stmnt)
        return result.first()
    

    async def create_employee(self, employee: Employee):
        self.session.add(employee)
        await self.session.commit()
        await self.session.refresh(employee)
        return employee
from asyncio import sleep

from efidgy import impl
from efidgy import models
from efidgy.models import ProjectState
from efidgy.models import JobState
from efidgy.models import ProjectTypeCode
from efidgy.models import SharedMode
from efidgy.models import UnitSystem

from . import idd_or


__all__ = [
    idd_or,
    # 'Computation',
    # 'Issue',
    # 'IssueStats',
    # 'IssueType',
    # 'Issues',
    # 'JobMessage',
    JobState,
    'Member',
    'Project',
    ProjectState,
    # 'ProjectSummary',
    'ProjectType',
    ProjectTypeCode,
    # 'Role',
    SharedMode,
    'Solution',
    # 'SolutionSummary',
    UnitSystem,
]


class Member(models.IMember):
    pass


class Currency(models.ICurrency):
    class service(impl.service.AsyncViewMixin, impl.service.EfidgyService):
        path = '/refs/currencies'


class ProjectType(models.IProjectType):
    class service(impl.service.AsyncViewMixin, impl.service.EfidgyService):
        path = '/refs/project_types'


class Project(models.IProject):
    currency = impl.fields.ObjectField(model=Currency)
    project_type = impl.fields.ObjectField(model=ProjectType)
    member = impl.fields.ObjectField(model=Member)

    class service(impl.service.AsyncChangeMixin, impl.service.CustomerService):
        path = '/projects'

    async def start_computation(self):
        c = impl.client.AsyncClient(self.service._get_env())
        await c.post(self._get_computation_path(), None)

    async def stop_computation(self):
        c = impl.client.AsyncClient(self.service._get_env())
        await c.delete(self._get_computation_path())

    async def wait_computation(self):
        while True:
            c = impl.client.AsyncClient(self.service._get_env())
            response = await c.get(self._get_computation_path())
            self._log_messages(response['messages'])
            if response['state'] not in [JobState.PENDING, JobState.WORKING]:
                break
            await sleep(10)

    async def computate(self):
        await self.start_computation()
        await self.wait_computation()


class Solution(models.ISolution):
    class service(impl.service.AsyncViewMixin, impl.service.ProjectService):
        path = '/solutions'

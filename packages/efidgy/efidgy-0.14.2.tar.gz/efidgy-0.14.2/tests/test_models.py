import unittest

import datetime

import asyncio

import efidgy
from efidgy import models
from efidgy import tools
from efidgy import exceptions
from efidgy.asyncapi import models as amodels
from efidgy.asyncapi import tools as atools

import logging


def async_test(coro):
    def wrapper(*args, **kwargs):
        loop = asyncio.new_event_loop()
        try:
            return loop.run_until_complete(coro(*args, **kwargs))
        finally:
            loop.close()
    return wrapper


class TestImpl(unittest.TestCase):
    PROJECT_NAME = 'Test Project'

    def setUp(self):
        efidgy.env = efidgy.env.override(
            unit_system=efidgy.models.UnitSystem.IMPERIAL,
        )
        projects = models.Project.service.filter(name=self.PROJECT_NAME)
        for project in projects:
            project.delete()

    def test_client_errors(self):
        with self.assertRaises(AssertionError):
            models.ProjectType.service.get(pk='XXX')
        with self.assertRaises(AssertionError):
            models.Project.service.get(foo='XXX')

    def test_authentication(self):
        env = efidgy.env.override(token='XXX')
        with self.assertRaises(exceptions.AuthenticationFailed):
            models.Project.service.use(env).get(pk='XXX')

    def test_not_found(self):
        with self.assertRaises(exceptions.NotFound):
            models.Project.service.get(pk='XXX')

    def test_validation(self):
        with self.assertRaises(exceptions.ValidationError):
            models.Project.service.create(
                name=self.PROJECT_NAME,
                currency='USD',
                project_type='XXX',
                shared_mode=models.SharedMode.PRIVATE,
            )

    def test_use(self):
        models.ProjectType.service.all()
        models.ProjectType.service.use(efidgy.env.override(code='XXX')).all()

    def test_filter(self):
        project = models.Project.service.create(
            name=self.PROJECT_NAME,
            currency='USD',
            project_type=models.ProjectTypeCode.IDD_OR,
            shared_mode=models.SharedMode.PRIVATE,
        )
        all_projects = models.Project.service.filter(name=self.PROJECT_NAME)
        first_project = models.Project.service.first(name=self.PROJECT_NAME)

        self.assertEqual(len(all_projects), 1)
        self.assertEqual(first_project, project)

        store = models.idd_or.Store.service.create(
            project=project,
            address='Address',
            name='Delivery Inc.',
            lat=0,
            lon=0,
        )

        stores = models.idd_or.Store.service.all(project=project)
        self.assertEqual(len(stores), 1)

        stores = models.idd_or.Store.service.filter(
            project=project,
            name='Delivery Inc.',
        )
        self.assertEqual(len(stores), 1)

        first_store = models.idd_or.Store.service.first(
            project=project,
            name='Delivery Inc.',
        )
        self.assertEqual(first_store, store)

    @async_test
    async def test_avalidation(self):
        with self.assertRaises(exceptions.ValidationError):
            await amodels.Project.service.create(
                name=self.PROJECT_NAME,
                currency='USD',
                project_type='XXX',
                shared_mode=amodels.SharedMode.PRIVATE,
            )

    def test_sync(self):
        project = models.Project.service.create(
            name=self.PROJECT_NAME,
            currency='USD',
            project_type=models.ProjectTypeCode.IDD_OR,
            shared_mode=models.SharedMode.PRIVATE,
        )
        project.delete()

    @async_test
    async def test_async(self):
        project = await amodels.Project.service.create(
            name=self.PROJECT_NAME,
            currency='USD',
            project_type=amodels.ProjectTypeCode.IDD_OR,
            shared_mode=amodels.SharedMode.PRIVATE,
        )
        await project.delete()


class TestModels(unittest.TestCase):
    PROJECT_NAME = 'Test Project'

    def setUp(self):
        # logging.basicConfig(
        #     format='%(asctime)s %(name)s %(message)s',
        #     level=logging.DEBUG,
        # )

        for project in models.Project.service.all():
            if project.name == self.PROJECT_NAME:
                project.delete()

        self.stores = [
            {
                'address': '6133 Broadway Terr., Oakland, CA 94618, USA',
                'name': 'Delivery Inc.',
                'open_time': datetime.time(8, 0),
                'close_time': datetime.time(18, 0),
            },
        ]

        self.vehicles = [
            {
                'store': 'Delivery Inc.',
                'name': 'Gary Bailey',
                'fuel_consumption': 11.76,
                'fuel_price': 3.25,
                'salary_per_duration': 21,
                'duration_limit': datetime.timedelta(hours=9),
            },
        ]

        self.orders = [
            {
                'store': 'Delivery Inc.',
                'name': '#00001',
                'address': '1 Downey Pl, Oakland, CA 94610, USA',
                'ready_time': datetime.time(8, 0),
                'delivery_time_from': datetime.time(12, 0),
                'delivery_time_to': datetime.time(16, 0),
                'load_duration': datetime.timedelta(minutes=1),
                'unload_duration': datetime.timedelta(minutes=5),
                'items': 1,
                'volume': 3.53,
                'weight': 22.05,
            },
        ]

    def _repr_point(self, point):
        return point.name

    def _print_vehicle(self, vehicle):
        print(vehicle.name)
        if vehicle.route is None:
            return
        prev_schedule = None
        for schedule in vehicle.route.schedule:
            print('{at}\t{arr}\t{dep}'.format(
                at=self._repr_point(schedule.start_point),
                arr=prev_schedule.arrival_time if prev_schedule else '',
                dep=schedule.departure_time,
            ))
            prev_schedule = schedule
        if prev_schedule:
            print('{at}\t{arr}\t{dep}'.format(
                at=self._repr_point(prev_schedule.end_point),
                arr=prev_schedule.arrival_time,
                dep='',
            ))

    def _print_order(self, order):
        print(order.name)
        if order.route is None:
            return
        prev_schedule = None
        for schedule in order.route.schedule:
            print('{at}\t{arr}\t{dep}'.format(
                at=self._repr_point(schedule.start_point),
                arr=prev_schedule.arrival_time if prev_schedule else None,
                dep=schedule.departure_time,
            ))
            prev_schedule = schedule
        if prev_schedule:
            print('{at}\t{arr}\t{dep}'.format(
                at=self._repr_point(prev_schedule.end_point),
                arr=prev_schedule.arrival_time,
                dep=None,
            ))

    def test_solve(self):
        project = models.Project.service.create(
            name=self.PROJECT_NAME,
            currency='USD',
            project_type=models.ProjectTypeCode.IDD_OR,
            shared_mode=models.SharedMode.PRIVATE,
        )

        stores = {}
        for data in self.stores:
            lat, lon = tools.geocode(data['address'])
            store = models.idd_or.Store.service.create(
                project=project,
                lat=lat,
                lon=lon,
                **data,
            )
            stores[store.name] = store

        vehicles = {}
        for data in self.vehicles:
            data['store'] = stores[data['store']]
            vehicle = models.idd_or.Vehicle.service.create(
                project=project,
                **data,
            )
            vehicles[vehicle.name] = vehicle

        orders = {}
        for data in self.orders:
            lat, lon = tools.geocode(data['address'])
            data['store'] = stores[data['store']]
            order = models.idd_or.Order.service.create(
                project=project,
                lat=lat,
                lon=lon,
                **data,
            )
            orders[order.name] = order

        project.computate()

        solutions = models.Solution.service.all(
            project=project,
        )
        self.assertTrue(len(solutions) > 0)
        solution = solutions[0]
        print('{cost:.2f}{currency}'.format(
            cost=solution.cost,
            currency=project.currency.symbol
        ))

        vehicles = models.idd_or.Vehicle.service.all(
            project=project,
            solution=solution,
        )
        for vehicle in vehicles:
            self._print_vehicle(vehicle)

        orders = models.idd_or.Order.service.all(
            project=project,
            solution=solution,
        )
        for order in orders:
            self._print_order(order)

    @async_test
    async def test_asolve(self):
        project = await amodels.Project.service.create(
            name=self.PROJECT_NAME,
            currency='USD',
            project_type=amodels.ProjectTypeCode.IDD_OR,
            shared_mode=amodels.SharedMode.PRIVATE,
        )

        stores = {}
        for data in self.stores:
            lat, lon = await atools.geocode(data['address'])
            store = await amodels.idd_or.Store.service.create(
                project=project,
                lat=lat,
                lon=lon,
                **data,
            )
            stores[store.name] = store

        vehicles = {}
        for data in self.vehicles:
            data['store'] = stores[data['store']]
            vehicle = await amodels.idd_or.Vehicle.service.create(
                project=project,
                **data,
            )
            vehicles[vehicle.name] = vehicle

        orders = {}
        for data in self.orders:
            lat, lon = await atools.geocode(data['address'])
            data['store'] = stores[data['store']]
            order = await amodels.idd_or.Order.service.create(
                project=project,
                lat=lat,
                lon=lon,
                **data,
            )
            orders[order.name] = order

        await project.computate()

        solutions = await amodels.Solution.service.all(
            project=project,
        )
        self.assertTrue(len(solutions) > 0)
        solution = solutions[0]
        print('{cost:.2f}{currency}'.format(
            cost=solution.cost,
            currency=project.currency.symbol
        ))

        vehicles = await amodels.idd_or.Vehicle.service.all(
            project=project,
            solution=solution,
        )
        for vehicle in vehicles:
            self._print_vehicle(vehicle)

        orders = await amodels.idd_or.Order.service.all(
            project=project,
            solution=solution,
        )
        for order in orders:
            self._print_order(order)

from efidgy import impl


__all__ = [
    'Order',
    'OrderRoute',
    'OrderSchedule',
    'Path',
    'Point',
    'PointType',
    'Store',
    'Vehicle',
    'VehicleRoute',
    'VehicleSchedule',
]


class PointType:
    STORE = 'store'
    ORDER = 'order'


class IPoint(impl.model.Model):
    pk = impl.fields.PrimaryKey()
    address = impl.fields.CharField()
    enabled = impl.fields.BooleanField()
    lat = impl.fields.FloatField()
    lon = impl.fields.FloatField()
    point_type = impl.fields.CharField()


class IPath(impl.model.Model):
    pk = impl.fields.PrimaryKey()
    distance = impl.fields.FloatField()
    directions = impl.fields.CharField()


class ISchedule(impl.model.Model):
    pk = impl.fields.PrimaryKey()
    start_point = impl.fields.PolymorphObjectField(
        lookup_field='point_type',
        models={
            PointType.STORE: 'efidgy.models.idd_or.IStore',
            PointType.ORDER: 'efidgy.models.idd_or.IOrder',
        },
    )
    end_point = impl.fields.PolymorphObjectField(
        lookup_field='point_type',
        models={
            PointType.STORE: 'efidgy.models.idd_or.IStore',
            PointType.ORDER: 'efidgy.models.idd_or.IOrder',
        },
    )
    departure_time = impl.fields.TimeField()
    arrival_time = impl.fields.TimeField()
    path = impl.fields.ObjectField(model=IPath)


class IStore(IPoint):
    name = impl.fields.CharField()
    description = impl.fields.CharField()
    open_time = impl.fields.TimeField()
    close_time = impl.fields.TimeField()
    issues = impl.fields.DictField()


class IVehicle(impl.model.Model):
    pk = impl.fields.PrimaryKey()
    name = impl.fields.CharField()
    description = impl.fields.CharField()
    enabled = impl.fields.BooleanField()
    store = impl.fields.ObjectField(model=IStore)
    features = impl.fields.ListField(item=impl.fields.CharField())
    fuel_consumption = impl.fields.FloatField()
    fuel_price = impl.fields.FloatField()
    salary_per_distance = impl.fields.FloatField()
    salary_per_duration = impl.fields.FloatField()
    items_limit = impl.fields.IntegerField()
    volume_limit = impl.fields.FloatField()
    weight_limit = impl.fields.FloatField()
    start_time = impl.fields.TimeField()
    end_time = impl.fields.TimeField()
    duration_limit = impl.fields.DurationField()
    route = impl.fields.ObjectField(model='efidgy.models.idd_or.IVehicleRoute')
    issues = impl.fields.DictField()


class IVehicleRoute(impl.model.Model):
    schedule = impl.fields.ListField(
        item='efidgy.models.idd_or.IVehicleSchedule',
    )
    distance = impl.fields.FloatField()
    distance_salary = impl.fields.FloatField()
    start_time = impl.fields.TimeField()
    duration = impl.fields.DurationField()
    duration_salary = impl.fields.FloatField()
    fuel = impl.fields.FloatField()
    fuel_cost = impl.fields.FloatField()
    issues = impl.fields.DictField()


class IVehicleSchedule(ISchedule):
    orders = impl.fields.ListField(item='efidgy.models.idd_or.IOrder')
    issues = impl.fields.DictField()


class IOrder(IPoint):
    name = impl.fields.CharField()
    description = impl.fields.CharField()
    features = impl.fields.ListField(item=impl.fields.CharField())
    items = impl.fields.IntegerField()
    volume = impl.fields.FloatField()
    weight = impl.fields.FloatField()
    ready_time = impl.fields.TimeField()
    store = impl.fields.ObjectField(model=IStore)
    delivery_time_from = impl.fields.TimeField()
    delivery_time_to = impl.fields.TimeField()
    load_duration = impl.fields.DurationField()
    unload_duration = impl.fields.DurationField()
    route = impl.fields.ObjectField(model='efidgy.models.idd_or.IOrderRoute')
    issues = impl.fields.DictField()


class IOrderRoute(impl.model.Model):
    vehicle = impl.fields.ObjectField(model='efidgy.models.idd_or.IVehicle')
    schedule = impl.fields.ListField(
        item='efidgy.models.idd_or.IOrderSchedule',
    )
    issues = impl.fields.DictField()


class IOrderSchedule(ISchedule):
    issues = impl.fields.DictField()


class Point(IPoint):
    pass


class Path(IPath):
    pass


class Store(IStore):
    class service(impl.service.SyncChangeMixin, impl.service.ProjectService):
        path = '/stores'


class Vehicle(IVehicle):
    store = impl.fields.ObjectField(model=Store)
    route = impl.fields.ObjectField(model='efidgy.models.idd_or.VehicleRoute')

    class service(impl.service.SyncChangeMixin, impl.service.SolutionService):
        path = '/vehicles'


class VehicleRoute(IVehicleRoute):
    schedule = impl.fields.ListField(
        item='efidgy.models.idd_or.VehicleSchedule',
    )


class VehicleSchedule(IVehicleSchedule):
    start_point = impl.fields.PolymorphObjectField(
        lookup_field='point_type',
        models={
            PointType.STORE: 'efidgy.models.idd_or.Store',
            PointType.ORDER: 'efidgy.models.idd_or.Order',
        },
    )
    end_point = impl.fields.PolymorphObjectField(
        lookup_field='point_type',
        models={
            PointType.STORE: 'efidgy.models.idd_or.Store',
            PointType.ORDER: 'efidgy.models.idd_or.Order',
        },
    )
    path = impl.fields.ObjectField(model=Path)
    orders = impl.fields.ListField(item='efidgy.models.idd_or.Order')


class Order(IOrder):
    store = impl.fields.ObjectField(model=Store)
    route = impl.fields.ObjectField(model='efidgy.models.idd_or.OrderRoute')

    class service(impl.service.SyncChangeMixin, impl.service.SolutionService):
        path = '/orders'


class OrderRoute(IOrderRoute):
    vehicle = impl.fields.ObjectField(model='efidgy.models.idd_or.Vehicle')
    schedule = impl.fields.ListField(item='efidgy.models.idd_or.OrderSchedule')


class OrderSchedule(IOrderSchedule):
    start_point = impl.fields.PolymorphObjectField(
        lookup_field='point_type',
        models={
            PointType.STORE: Store,
            PointType.ORDER: Order,
        },
    )
    end_point = impl.fields.PolymorphObjectField(
        lookup_field='point_type',
        models={
            PointType.STORE: Store,
            PointType.ORDER: Order,
        },
    )
    path = impl.fields.ObjectField(model=Path)

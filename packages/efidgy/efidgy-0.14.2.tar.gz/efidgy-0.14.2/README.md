# efidgy

Python bindings to efidgy services.


## Overview


### Environment

Environment in terms of efidgy package is a set of settings to work with efidgy backend.
Theese settings includes **customer code** and **access token** that will be used to communicate with backend.


### Unit System.

If you will not set the unit system directly, efidgy will use current user settings: [console.efidgy.com/profile](https://console.efidgy.com/profile)

Anyway, it is a good practice to define the unit system in your code:

``` python
efidgy.env = efidgy.env.override(
    unit_system=efidgy.models.UnitSystem.IMPERIAL,
)
```


### Credentials

efidgy.env is initialized with settings fetched from the shell environment. The following environment variables are used:

 * EFIDGY_ACCESS_TOKEN -- You can get one at [console.efidgy.com/profile/company](https://console.efidgy.com/profile/company)
 * EFIDGY_CUSTOMER_CODE -- See [console.efidgy.com/profile/tokens](https://console.efidgy.com/profile/tokens)

You can always override code and/or token with the code like this:

``` python
efidgy.env = efidgy.env.override(
    code='hardcoded customer code',
)
```


## API documentation

Find out more at: [efidgy.com/docs](https://efidgy.com/docs)

## Sample usage

``` sh
export EFIDGY_CUSTOMER_CODE=code  # https://console.efidgy.com/profile/company
export EFIDGY_ACCESS_TOKEN=token  # https://console.efidgy.com/profile/tokens
```

``` python
import datetime
import efidgy


project = efidgy.models.Project.service.create(
    name='Demo',
    currency='USD',
    project_type=efidgy.models.ProjectTypeCode.IDD_OR,
    shared_mode=efidgy.models.SharedMode.PRIVATE,
)

store_address = '6133 Broadway Terr., Oakland, CA 94618, USA'
lat, lon = efidgy.tools.geocode(store_address)
store = efidgy.models.idd_or.Store.service.create(
    project=project,
    address=store_address,
    lat=lat,
    lon=lon,
    name='Delivery Inc.',
    open_time=datetime.time(8, 0),
    close_time=datetime.time(18, 0),
)

vehicle = efidgy.models.idd_or.Vehicle.service.create(
    project=project,
    store=store,
    name='Gary Bailey',
    fuel_consumption=11.76,
    fuel_price=3.25,
    salary_per_duration=21,
    duration_limit=datetime.timedelta(hours=9),
)

order_address = '1 Downey Pl, Oakland, CA 94610, USA'
lat, lon = efidgy.tools.geocode(order_address)
order = efidgy.models.idd_or.Order.service.create(
    project=project,
    store=store,
    name='#00001',
    address=order_address,
    lat=lat,
    lon=lon,
    ready_time=datetime.time(8, 0),
    delivery_time_from=datetime.time(12, 0),
    delivery_time_to=datetime.time(16, 0),
    load_duration=datetime.timedelta(minutes=1),
    unload_duration=datetime.timedelta(minutes=5),
    items=1,
    volume=3.53,
    weight=22.05,
)

project.computate()

solutions = efidgy.models.Solution.service.all(
    project=project,
)

if solutions:
    solution = solutions[0]
    print('{cost:.2f}{currency}'.format(
        cost=solution.cost,
        currency=project.currency.symbol
    ))

    vehicle = efidgy.models.idd_or.Vehicle.service.get(
        pk=vehicle.pk,
        project=project,
        solution=solution,
    )

    print(vehicle.name)
    if vehicle.route is not None:
        prev_schedule = None
        for schedule in vehicle.route.schedule:
            print('{at}\t{arr}\t{dep}'.format(
                at=schedule.start_point.name,
                arr=prev_schedule.arrival_time if prev_schedule else vehicle.route.start_time,
                dep=schedule.departure_time,
            ))
            prev_schedule = schedule
        if prev_schedule:
            print('{at}\t{arr}\t{dep}'.format(
                at=prev_schedule.end_point.name,
                arr=prev_schedule.arrival_time,
                dep='',
            ))
```

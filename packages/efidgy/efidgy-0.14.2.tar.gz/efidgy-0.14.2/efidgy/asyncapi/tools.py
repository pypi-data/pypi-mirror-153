import efidgy
from efidgy import impl

import urllib.parse


__all__ = [
    'geocode',
]


async def geocode(address, env=None):
    if env is None:
        env = efidgy.env
    env = env.override(code='efidgy')
    c = impl.client.AsyncClient(env)
    data = await c.get(
        '/tools/geocode/?address={}'.format(urllib.parse.quote(address)),
    )

    lat = data.get('lat')
    lon = data.get('lon')
    if lat is None or lon is None:
        raise efidgy.exceptions.GeocodeError(address)

    return lat, lon

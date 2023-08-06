import os
from hestia_earth.earth_engine import init_gee
from hestia_earth.earth_engine.coordinates import run
from hestia_earth.earth_engine.gee_utils import load_region, load_geometry, area_km2


ENABLED = os.environ.get('VALIDATE_SPATIAL', 'true') == 'true'
gee_init = False


def _init_gee():
    global gee_init
    if gee_init:
        return
    init_gee()
    gee_init = True


def is_enabled(): return ENABLED


def id_to_level(id: str): return id.count('.')


def fetch_data(**kwargs):
    _init_gee()
    return run(kwargs).get('features', [])[0].get('properties')


def get_region_id(gid: str, **kwargs):
    _init_gee()
    try:
        level = id_to_level(gid)
        field = f"GID_{level}"
        id = fetch_data(collection=f"users/hestiaplatform/gadm36_{level}",
                        ee_type='vector',
                        fields=field,
                        **kwargs
                        ).get(field)
        return None if id is None else f"GADM-{id}"
    except Exception:
        return None


def get_region_size(gid: str):
    _init_gee()
    return area_km2(load_region(gid).geometry()).getInfo()


def get_boundary_size(boundary: dict):
    _init_gee()
    return area_km2(load_geometry(boundary)).getInfo()

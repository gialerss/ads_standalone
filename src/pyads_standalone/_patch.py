from __future__ import annotations

from types import ModuleType


def _unwrap(func):
    return getattr(func, "__wrapped__", func)


def _make_set_local_address(ads_module: ModuleType):
    parse_ams_netid = ads_module._parse_ams_netid
    ams_netid_type = ads_module.SAmsNetId
    ads_set_local_address = ads_module.adsSetLocalAddress

    def set_local_address(ams_netid):
        if isinstance(ams_netid, str):
            ams_netid_struct = parse_ams_netid(ams_netid)
        else:
            ams_netid_struct = ams_netid

        if not isinstance(ams_netid_struct, ams_netid_type):
            raise TypeError(f"Expected str or {ams_netid_type.__name__}, got {type(ams_netid).__name__}.")

        return ads_set_local_address(ams_netid_struct)

    set_local_address.__name__ = "set_local_address"
    set_local_address.__doc__ = ads_module.set_local_address.__doc__
    return set_local_address


def patch_loaded_pyads_modules(
    *,
    pyads_module: ModuleType,
    ads_module: ModuleType,
    connection_module: ModuleType,
    pyads_ex_module: ModuleType,
) -> bool:
    if getattr(pyads_module, "__pyads_standalone_patched__", False):
        return False

    raw_add_route = _unwrap(pyads_ex_module.adsAddRoute)
    raw_add_route_to_plc = _unwrap(pyads_ex_module.adsAddRouteToPLC)
    raw_del_route = _unwrap(pyads_ex_module.adsDelRoute)

    pyads_ex_module.adsAddRoute = raw_add_route
    pyads_ex_module.adsAddRouteToPLC = raw_add_route_to_plc
    pyads_ex_module.adsDelRoute = raw_del_route

    ads_module.adsAddRoute = raw_add_route
    ads_module.adsAddRouteToPLC = raw_add_route_to_plc
    ads_module.adsDelRoute = raw_del_route
    ads_module.linux = True
    ads_module.set_local_address = _make_set_local_address(ads_module)

    connection_module.adsAddRoute = raw_add_route
    connection_module.adsDelRoute = raw_del_route
    connection_module.linux = True

    pyads_module.add_route = ads_module.add_route
    pyads_module.add_route_to_plc = ads_module.add_route_to_plc
    pyads_module.delete_route = ads_module.delete_route
    pyads_module.set_local_address = ads_module.set_local_address

    setattr(pyads_module, "__pyads_standalone_patched__", True)
    setattr(ads_module, "__pyads_standalone_patched__", True)
    setattr(connection_module, "__pyads_standalone_patched__", True)
    setattr(pyads_ex_module, "__pyads_standalone_patched__", True)
    return True


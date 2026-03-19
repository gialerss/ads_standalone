from __future__ import annotations

from types import ModuleType

from pyads_standalone._patch import patch_loaded_pyads_modules


class DummySAmsNetId:
    pass


def _build_modules():
    pyads_module = ModuleType("pyads")
    ads_module = ModuleType("pyads.ads")
    connection_module = ModuleType("pyads.connection")
    pyads_ex_module = ModuleType("pyads.pyads_ex")

    def wrapped_add_route(*args, **kwargs):
        raise RuntimeError("wrapped")

    def raw_add_route(*args, **kwargs):
        return ("add", args, kwargs)

    wrapped_add_route.__wrapped__ = raw_add_route

    def wrapped_add_route_to_plc(*args, **kwargs):
        raise RuntimeError("wrapped")

    def raw_add_route_to_plc(*args, **kwargs):
        return ("add_route_to_plc", args, kwargs)

    wrapped_add_route_to_plc.__wrapped__ = raw_add_route_to_plc

    def wrapped_del_route(*args, **kwargs):
        raise RuntimeError("wrapped")

    def raw_del_route(*args, **kwargs):
        return ("delete", args, kwargs)

    wrapped_del_route.__wrapped__ = raw_del_route

    def parse_ams_netid(value):
        assert value == "1.2.3.4.5.6"
        return parsed_value

    def ads_set_local_address(value):
        return ("set_local_address", value)

    def add_route(adr, ip_address):
        return ads_module.adsAddRoute(adr, ip_address)

    def add_route_to_plc(*args, **kwargs):
        return ads_module.adsAddRouteToPLC(*args, **kwargs)

    def delete_route(adr):
        return ads_module.adsDelRoute(adr)

    def set_local_address(value):
        raise RuntimeError("windows guard")

    parsed_value = DummySAmsNetId()

    pyads_ex_module.adsAddRoute = wrapped_add_route
    pyads_ex_module.adsAddRouteToPLC = wrapped_add_route_to_plc
    pyads_ex_module.adsDelRoute = wrapped_del_route

    ads_module.adsAddRoute = wrapped_add_route
    ads_module.adsAddRouteToPLC = wrapped_add_route_to_plc
    ads_module.adsDelRoute = wrapped_del_route
    ads_module.adsSetLocalAddress = ads_set_local_address
    ads_module.SAmsNetId = DummySAmsNetId
    ads_module._parse_ams_netid = parse_ams_netid
    ads_module.set_local_address = set_local_address
    ads_module.add_route = add_route
    ads_module.add_route_to_plc = add_route_to_plc
    ads_module.delete_route = delete_route
    ads_module.linux = False

    connection_module.adsAddRoute = wrapped_add_route
    connection_module.adsDelRoute = wrapped_del_route
    connection_module.linux = False

    pyads_module.add_route = add_route
    pyads_module.add_route_to_plc = add_route_to_plc
    pyads_module.delete_route = delete_route
    pyads_module.set_local_address = set_local_address

    return pyads_module, ads_module, connection_module, pyads_ex_module, parsed_value


def test_patch_loaded_pyads_modules_replaces_windows_guards() -> None:
    pyads_module, ads_module, connection_module, pyads_ex_module, parsed_value = _build_modules()

    changed = patch_loaded_pyads_modules(
        pyads_module=pyads_module,
        ads_module=ads_module,
        connection_module=connection_module,
        pyads_ex_module=pyads_ex_module,
    )

    assert changed is True
    assert ads_module.linux is True
    assert connection_module.linux is True
    assert pyads_ex_module.adsAddRoute("netid", "192.168.0.10")[0] == "add"
    assert ads_module.add_route("netid", "192.168.0.10")[0] == "add"
    assert pyads_module.add_route_to_plc("a", "b", "c", "d", "e")[0] == "add_route_to_plc"
    assert pyads_module.set_local_address("1.2.3.4.5.6") == ("set_local_address", parsed_value)


def test_patch_loaded_pyads_modules_is_idempotent() -> None:
    pyads_module, ads_module, connection_module, pyads_ex_module, _ = _build_modules()

    assert patch_loaded_pyads_modules(
        pyads_module=pyads_module,
        ads_module=ads_module,
        connection_module=connection_module,
        pyads_ex_module=pyads_ex_module,
    ) is True

    assert patch_loaded_pyads_modules(
        pyads_module=pyads_module,
        ads_module=ads_module,
        connection_module=connection_module,
        pyads_ex_module=pyads_ex_module,
    ) is False


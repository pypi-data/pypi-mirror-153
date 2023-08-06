#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import time
from collections import OrderedDict

import pytest
from ophyd.device import Device

from hxrsnd import pneumatic
from hxrsnd.pneumatic import PressureSwitch, ProportionalValve, SndPneumatics

from .conftest import fake_device, get_classes_in_module

logger = logging.getLogger(__name__)


@pytest.mark.parametrize("dev", get_classes_in_module(pneumatic, Device))
def test_devices_instantiate_and_run_ophyd_functions(dev):
    device = fake_device(dev)
    assert(isinstance(device.read(), OrderedDict))
    assert(isinstance(device.read_configuration(), OrderedDict))


def test_ProportionalValve_opens_and_closes_correctly():
    valve = fake_device(ProportionalValve)
    valve.open()
    time.sleep(.1)
    assert valve.position == "OPEN"
    assert valve.opened is True
    assert valve.closed is False
    valve.close()
    time.sleep(.1)
    assert valve.position == "CLOSED"
    assert valve.opened is False
    assert valve.closed is True


def test_PressureSwitch_reads_correctly():
    press = fake_device(PressureSwitch)
    press.pressure.sim_put(0)
    assert press.position == "GOOD"
    assert press.good is True
    assert press.bad is False
    press.pressure.sim_put(1)
    assert press.position == "BAD"
    assert press.good is False
    assert press.bad is True


def test_SndPneumatics_open_and_close_methods():
    vac = fake_device(SndPneumatics)
    for valve in vac._valves:
        valve.close()
    time.sleep(.1)
    vac.open()
    time.sleep(.1)
    for valve in vac._valves:
        assert valve.opened
    vac.close()
    time.sleep(.1)
    for valve in vac._valves:
        assert valve.closed

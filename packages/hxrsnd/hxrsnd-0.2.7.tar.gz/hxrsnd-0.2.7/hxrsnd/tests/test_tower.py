#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import time
from collections import OrderedDict

import pytest
from ophyd.device import Device

from hxrsnd import tower
from hxrsnd.exceptions import MotorDisabled, MotorFaulted
from hxrsnd.sndsystem import ChannelCutTower, DelayTower

from .conftest import fake_device, get_classes_in_module

logger = logging.getLogger(__name__)


@pytest.mark.parametrize("dev", get_classes_in_module(tower, Device))
def test_devices_instantiate_and_run_ophyd_functions(dev):
    device = fake_device(dev, "TEST:SND:T1")
    assert(isinstance(device.read(), OrderedDict))
    assert(isinstance(device.read_configuration(), OrderedDict))


def test_DelayTower_does_not_move_if_motors_not_ready():
    tower = fake_device(DelayTower, "TEST:SND:T1")
    tower.disable()
    time.sleep(.5)
    tower.tth.user_setpoint.sim_set_limits((-100, 100))
    tower.th1.user_setpoint.sim_set_limits((-100, 100))
    tower.th2.user_setpoint.sim_set_limits((-100, 100))

    tower.tth.user_setpoint.check_value = lambda x: None
    tower.th1.user_setpoint.check_value = lambda x: None
    tower.th2.user_setpoint.check_value = lambda x: None

    with pytest.raises(MotorDisabled):
        tower.energy = 10
    tower.enable()
    tower.tth.axis_fault.sim_put(True)
    with pytest.raises(MotorFaulted):
        tower.energy = 10


def test_ChannelCutTower_does_not_move_if_motors_not_ready():
    tower = fake_device(ChannelCutTower, "TEST:SND:T1")
    tower.disable()
    time.sleep(.5)
    tower.th.user_setpoint.sim_set_limits((-100, 100))
    tower.th.user_setpoint.check_value = lambda x: None

    with pytest.raises(MotorDisabled):
        tower.energy = 10
    tower.enable()
    tower.th.axis_fault.sim_put(True)
    with pytest.raises(MotorFaulted):
        tower.energy = 10

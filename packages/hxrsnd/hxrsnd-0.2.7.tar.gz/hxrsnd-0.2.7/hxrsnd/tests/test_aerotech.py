#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
from collections import OrderedDict

import pytest
from ophyd.device import Device

from hxrsnd import aerotech
from hxrsnd.aerotech import AeroBase, MotorDisabled

from .conftest import fake_device, get_classes_in_module

logger = logging.getLogger(__name__)


@pytest.mark.parametrize("dev", get_classes_in_module(aerotech, Device))
def test_aerotech_devices_instantiate_and_run_ophyd_functions(dev):
    motor = fake_device(dev, "TEST:SND:T1")
    assert(isinstance(motor.read(), OrderedDict))
    assert(isinstance(motor.read_configuration(), OrderedDict))


def test_AeroBase_raises_MotorDisabled_if_moved_while_disabled():
    motor = fake_device(AeroBase, "TEST:SND:T1")
    motor.axis_fault.sim_put(0)
    assert not motor.faulted
    motor.disable()
    assert not motor.enabled
    with pytest.raises(MotorDisabled):
        motor.move(10)

# @pytest.mark.parametrize("position", [1])
# def test_AeroBase_callable_moves_the_motor(position):
#     motor = fake_device(AeroBase)
#     motor.axis_fault.sim_put(0)
#     assert not motor.faulted
#     motor.enable()
#     assert motor.enabled
#     motor.limits = (0, 1)
#     assert motor.user_setpoint.get() != position
#     time.sleep(0.5)
#     motor(position, wait=False)
#     time.sleep(0.1)
#     assert motor.user_setpoint.get() == position

# Commented out for now because it causes travis to seg fault sometimes
# def test_AeroBase_raises_MotorFaulted_if_moved_while_faulted():
#     motor = AeroBase("TEST")
#     motor.enable()
#     time.sleep(.1)
#     motor.axis_fault.sim_put(1)
#     with pytest.raises(MotorFaulted):
#         motor.move(10)

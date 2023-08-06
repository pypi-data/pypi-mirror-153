#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
from collections import OrderedDict

import pytest
from ophyd.device import Device

from hxrsnd import snddevice

from .conftest import fake_device, get_classes_in_module

logger = logging.getLogger(__name__)


@pytest.mark.parametrize("dev", get_classes_in_module(snddevice, Device))
def test_sndevice_devices_instantiate_and_run_ophyd_functions(dev):
    device = fake_device(dev)
    assert(isinstance(device.read(), OrderedDict))
    assert(isinstance(device.read_configuration(), OrderedDict))

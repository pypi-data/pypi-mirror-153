#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
from collections import OrderedDict

import pytest
from ophyd.device import Device

from hxrsnd import sequencer

from .conftest import fake_device, get_classes_in_module

logger = logging.getLogger(__name__)


@pytest.mark.parametrize("dev", get_classes_in_module(sequencer, Device))
def test_sequencer_devices_instantiate_and_run_ophyd_functions(dev):
    device = fake_device(dev)
    assert(isinstance(device.read(), OrderedDict))
    assert(isinstance(device.read_configuration(), OrderedDict))

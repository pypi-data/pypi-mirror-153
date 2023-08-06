#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

logger = logging.getLogger(__name__)

# Too hard to port to ophyd=1.2.0
# @pytest.mark.parametrize("dev", get_classes_in_module(sndsystem, Device))
# def test_devices_instantiate_and_run_ophyd_functions(dev):
#     device = fake_device(dev)
#     assert(isinstance(device.read(), OrderedDict))
#     assert(isinstance(device.read_configuration(), OrderedDict))

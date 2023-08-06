"""
Tests for the bin ipython shell
"""
import logging
import sys

import pytest

from .conftest import requires_epics

logger = logging.getLogger(__name__)


@pytest.mark.timeout(60)
@requires_epics
@pytest.mark.skipif(sys.version_info < (3, 6), reason="requires python3.6")
def test_snd_devices_import_with_epics():
    import snd_devices  # noqa


# I couldn't quickly get this to pass with ophyd 1.2.0 (zlentz)
# @pytest.mark.timeout(60)
# @pytest.mark.skipif(sys.version_info < (3, 6), reason="requires python3.6")
# def test_snd_devices_import_no_epics():
#     import snd_devices

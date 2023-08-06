# -*- coding: utf-8 -*-
#
# Copyright 2022 Shanghai AI Lab. Licensed under MIT License.
#

"""OpenDataHub python SDK."""

from opendatahub.__version__ import __version__
from opendatahub.client.odl import ODL

__all__ = ["__version__", "ODL"]

from opendatahub.dataset.dataset import Dataset

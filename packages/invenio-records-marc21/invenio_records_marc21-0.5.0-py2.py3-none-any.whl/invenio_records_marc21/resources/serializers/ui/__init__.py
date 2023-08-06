# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Record response serializers."""

from .schema import Marc21UISchema
from .serializers import Marc21UIJSONSerializer, Marc21UIXMLSerializer

__all__ = (
    "Marc21UISchema",
    "Marc21UIJSONSerializer",
    "Marc21UIXMLSerializer",
)

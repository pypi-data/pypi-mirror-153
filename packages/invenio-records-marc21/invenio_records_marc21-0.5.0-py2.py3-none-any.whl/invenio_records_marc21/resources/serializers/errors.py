# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Errors for serializers."""


class SerializerError(Exception):
    """Base class for serializer errors."""


class Marc21XMLConvertError(SerializerError):
    """Error thrown when a marc21 xml could not be converted."""

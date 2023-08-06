# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.


"""DataCite Serializers for Invenio Marc21 Records."""

from flask_resources.serializers import MarshmallowJSONSerializer

from .schema import Marc21DataCite43Schema


class Marc21DataCite43JSONSerializer(MarshmallowJSONSerializer):
    """Marshmallow based DataCite serializer for records."""

    def __init__(self, **options):
        """Constructor."""
        super().__init__(schema_cls=Marc21DataCite43Schema, **options)

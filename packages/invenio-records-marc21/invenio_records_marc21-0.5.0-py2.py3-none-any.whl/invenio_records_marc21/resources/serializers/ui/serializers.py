# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Marc21 UI record response serializers."""


from copy import deepcopy

from ..serializer import Marc21BASESerializer
from .schema import Marc21UISchema


class Marc21UIBASESerializer(Marc21BASESerializer):
    """UI Base serializer implementation."""

    def __init__(self, object_key="ui", **options):
        """Marc21 UI Base Constructor.

        :param object_key: str key dump ui specific information
        """
        super().__init__(schema_cls=Marc21UISchema, **options)
        self._object_key = object_key

    def dump_one(self, obj):
        """Dump the object into a JSON string."""
        obj[self._object_key] = self._schema_cls().dump(deepcopy(obj))
        return obj


class Marc21UIJSONSerializer(Marc21UIBASESerializer):
    """UI JSON serializer implementation."""


class Marc21UIXMLSerializer(Marc21UIBASESerializer):
    """UI Marc21 xml serializer implementation."""

    def __init__(self, object_key="ui", **options):
        """Marc21 UI XML Constructor.

        :param object_key: str key dump ui specific information
        """
        super().__init__(object_key=object_key, **options)

    def dump_one(self, obj):
        """Dump the object into a JSON string."""
        obj[self._object_key] = self._schema_cls().dump(deepcopy(obj))

        # For edit a marc21 record in the deposit react app we need
        # the metadata field also as a marcxml string
        obj["metadata"] = deepcopy(obj[self._object_key]["metadata"])
        return obj

# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Marc21 record metadata field."""


import json
import typing
from os.path import dirname, join

from jsonschema import ValidationError, validate
from marshmallow.exceptions import ValidationError as MarshmallowValidationError
from marshmallow.fields import Field


def get_schema():
    """Marc21 load json schema."""
    with open(
        join(
            dirname(__file__),
            "../../records/jsonschemas/marc21/marc21-structure-v1.0.0.json",
        ),
        "rb",
    ) as fp:
        input = fp.read()
        return json.loads(input.decode("utf-8"))


class MetadataField(Field):
    """Schema for the record metadata."""

    # FIXME: get_schema

    schema = get_schema()

    def _deserialize(
        self,
        value: typing.Any,
        attr: typing.Optional[str],
        data: typing.Optional[typing.Mapping[str, typing.Any]],
        **kwargs,
    ):
        """Deserialize value. Concrete :class:`Field` classes should implement this method.

        :param value: The value to be deserialized.
        :param attr: The attribute/key in `data` to be deserialized.
        :param data: The raw input data passed to the `Schema.load`.
        :param kwargs: Field-specific keyword arguments.
        :raise ValidationError: In case of formatting or validation failure.
        :return: The deserialized value.

        .. versionchanged:: 2.0.0
            Added ``attr`` and ``data`` parameters.

        .. versionchanged:: 3.0.0
            Added ``**kwargs`` to signature.
        """
        return value

    def _validate(self, value):
        """Perform validation on ``value``.

        Raise a :exc:`ValidationError` if validation
        does not succeed.
        """
        try:
            validate(instance=value, schema=self.schema)
        except ValidationError as e:
            message = f"Field: {e.json_path} Message: {e.message}"
            raise MarshmallowValidationError(message)
        self._validate_all(value)

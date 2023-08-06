# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Marc21 records deposit backend."""

from os.path import dirname, join

from flask import current_app
from marshmallow import Schema, fields
from marshmallow.schema import SchemaMeta
from marshmallow_utils.fields import NestedAttribute

from invenio_records_marc21.services.schemas import Marc21RecordSchema

from ...proxies import current_records_marc21


def dump_empty(schema_or_field):
    """Return a full marc21 record dict with empty values."""
    if isinstance(schema_or_field, (Schema,)):
        schema = schema_or_field
        return {k: dump_empty(v) for (k, v) in schema.fields.items()}
    if isinstance(schema_or_field, SchemaMeta):
        schema = schema_or_field()
        return {k: dump_empty(v) for (k, v) in schema.fields.items()}
    if isinstance(schema_or_field, fields.List):
        field = schema_or_field
        return [dump_empty(field.inner)]
    if isinstance(schema_or_field, NestedAttribute):
        field = schema_or_field
        return dump_empty(field.nested)

    return None


def empty_record():
    """Create an empty record."""
    record = dump_empty(Marc21RecordSchema)

    record["metadata"] = "<record> <leader>00000nam a2200000zca4500</leader></record>"
    record["is_published"] = False
    record["files"] = {"enabled": True}
    return record


def deposit_templates():
    """Retrieve from DB the tamplates for marc21 deposit form."""
    templates = current_records_marc21.templates_service.get_templates()

    if templates:
        return [template.to_dict() for template in templates]
    return []


def deposit_config(**kwargs):
    """Create an deposit configuration."""
    jsonschema = current_app.extensions["invenio-jsonschemas"]
    schema = {}
    if jsonschema:
        schema = jsonschema.get_schema(path="marc21/marc21-structure-v1.0.0.json")
    config = {**kwargs}
    config.setdefault("error", "")
    config.setdefault("schema", schema)
    config.setdefault("createUrl", "/api/marc21")
    return config

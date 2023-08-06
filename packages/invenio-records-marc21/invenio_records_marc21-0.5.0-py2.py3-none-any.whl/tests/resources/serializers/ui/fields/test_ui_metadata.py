# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.


"""Test for record ui MetadataSchema."""

from copy import deepcopy

from marshmallow import Schema

from invenio_records_marc21.resources.serializers.fields import MetadataField


class Marc21TestSchema(Schema):
    """Marc21 Test Schema."""

    metadata = MetadataField(attribute="metadata")


def _test_metadata(test, expected, exept=["__order__"]):
    # assert test.keys() == expected.keys()
    for key in test.keys():
        if key not in exept:
            assert test[key] == expected[key]


def _test_without_order(data, key="__order__"):
    """Test no Key with the name in dict."""
    if isinstance(data, dict):
        for k, v in data.items():
            assert not key == k
            _test_without_order(v, key)
    elif isinstance(data, (list, tuple)):
        for item in data:
            _test_without_order(item, key)


def test_ui_metadata_convert_xml(marc21_metadata):
    metadata = Marc21TestSchema()
    test = deepcopy(marc21_metadata)

    data = metadata.dump({"metadata": test})
    assert isinstance(data["metadata"], dict)

    expect_keys = [
        "main_entry_personal_name",
        "title_statement",
        "physical_description",
        "dissertation_note",
        "general_note",
        "language_code",
        "production_publication_distribution_manufacture_and_copyright_notice",
    ]
    for key in expect_keys:
        assert key in data["metadata"]


def test_ui_metadata_default_schema(marc21_metadata):
    metadataschema = Marc21TestSchema()
    data = metadataschema.dump({"metadata": marc21_metadata})

    expect_keys = [
        "main_entry_personal_name",
        "title_statement",
        "physical_description",
        "dissertation_note",
        "general_note",
        "language_code",
        "production_publication_distribution_manufacture_and_copyright_notice",
    ]
    for key in expect_keys:
        assert key in data["metadata"]
        assert data["metadata"][key] is not None


def test_ui_metadata_json_schema(marc21_metadata, expect_metadata_ui):
    metadata = Marc21TestSchema()
    test = deepcopy(marc21_metadata)
    data = metadata.dump({"metadata": test})

    _test_metadata(
        data["metadata"],
        expect_metadata_ui,
    )

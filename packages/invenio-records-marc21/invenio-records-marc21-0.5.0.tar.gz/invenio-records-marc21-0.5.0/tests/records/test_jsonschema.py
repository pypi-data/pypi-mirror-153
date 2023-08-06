# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.


"""JSONSchema tests."""

import json
from os.path import dirname, join

import pytest
from jsonschema.exceptions import ValidationError

from invenio_records_marc21.records import Marc21Record as Record


#
# Assertion helpers
#
def validates(data):
    """Assertion function used to validate according to the schema."""
    data["$schema"] = "local://marc21/marc21-v1.0.0.json"
    Record(data).validate()
    return True


def validates_meta(data):
    """Validate metadata fields."""
    return validates({"metadata": data})


def fails(data):
    """Assert that validation fails."""
    pytest.raises(ValidationError, validates, data)
    return True


def fails_meta(data):
    """Assert that validation fails for metadata."""
    pytest.raises(ValidationError, validates_meta, data)
    return True


#
# Fixtures
#
@pytest.fixture()
def marc21():
    """marc21 record."""
    return {
        "xml": "<record><controlfield tag='001'>990079940640203331</controlfield> \
       <controlfield tag='003'>AT-OBV</controlfield> \
       <controlfield tag='005'>20170703041800.0</controlfield>\
       <controlfield tag='007'>cr</controlfield>\
       <controlfield tag='008'>100504|1932</controlfield>\
       <controlfield tag='009'>AC08088803</controlfield>\
       <datafield tag='035' ind1=' ' ind2=' '>\
       <subfield code='a'>AC08088803</subfield>\
       </datafield></record>"
    }


def _load_json(filename):
    with open(join(dirname(__file__), filename), "rb") as fp:
        return json.load(fp)


#
# Test a full record
#
def test_full_record(appctx):
    """Test validation of a full record example."""
    assert validates(_load_json("test-record.json"))


#
# Tests internal/external identifiers
#
def test_id(appctx):
    """Test id."""
    assert validates({"id": "12345-abcd"})
    assert fails({"id": 1})


@pytest.mark.parametrize("prop", ["pid"])
def test_pid(appctx, prop):
    """Test pid."""
    pid = {
        "pk": 1,
        "status": "R",
    }
    assert validates({prop: pid})

    # Valid status
    for s in ["N", "K", "R", "M", "D"]:
        pid["status"] = s
        assert validates({prop: pid})

    # Invalid status
    pid["status"] = "INVALID"
    assert fails({prop: pid})

    # Extra propert
    pid["invalid"] = "1"
    assert fails({prop: pid})


def test_pids(appctx):
    """Test external pids."""
    assert validates(
        {
            "pids": {
                "doi": {
                    "identifier": "10.12345",
                    "provider": "datacite",
                    "client": "test",
                }
            }
        }
    )
    assert validates(
        {
            "pids": {
                "doi": {
                    "identifier": "10.12345",
                    "provider": "datacite",
                    "client": "test",
                },
                "oai": {"identifier": "oai:10.12345", "provider": "local"},
            }
        }
    )
    # Extra property
    assert fails(
        {
            "pids": {
                "oai": {
                    "identifier": "oai:10.12345",
                    "provider": "local",
                    "invalid": "test",
                }
            }
        }
    )
    # Not a string
    assert fails({"pids": {"oai": {"identifier": 1, "provider": "local"}}})


#
# Tests metadata
#
def test_metadata(appctx):
    """Test empty metadata."""
    assert validates({"metadata": {"fields": [], "leader": ""}})


def test_metadata_record(appctx):
    """Test title property."""
    assert validates_meta({"xml": "<record></record>"})


def test_marc21(appctx, marc21):
    """Test additional titles property."""
    assert validates_meta(marc21)

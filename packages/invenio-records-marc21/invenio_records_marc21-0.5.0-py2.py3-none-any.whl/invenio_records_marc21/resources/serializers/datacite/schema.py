# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 CERN.
# Copyright (C) 2021 Northwestern University.
#
# Invenio-RDM-Records is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.


"""DataCite based Schema for Invenio RDM Records."""

from flask import current_app
from flask_babelex import lazy_gettext as _
from marshmallow import Schema, fields, missing


def get_scheme_datacite(scheme, config_name, default=None):
    """Returns the datacite equivalent of a scheme."""
    config_item = current_app.config[config_name]
    return config_item.get(scheme, {}).get("datacite", default)


class CreatorSchema43(Schema):
    """Creator schema for v4."""

    name = fields.Method("get_name")

    def get_name(self, obj):
        """Get titles list."""
        names = obj.get("100", [{"subfields": {}}])[0]
        return names.get("subfields", {}).get("a", [""])[0]


class Marc21DataCite43Schema(Schema):
    """DataCite JSON 4.3 Marshmallow Schema."""

    # PIDS-FIXME: What about versioning links and related ids
    identifiers = fields.Method("get_identifiers")
    types = fields.Method("get_type")
    titles = fields.Method("get_titles")
    creators = fields.Nested(CreatorSchema43, attribute="metadata.fields")
    publisher = fields.Str(attribute="metadata.publisher")
    publicationYear = fields.Method("get_publication_year")
    schemaVersion = fields.Constant("http://datacite.org/schema/kernel-4")

    def get_type(self, obj):
        """Get resource type."""
        # FIXME: The metadatafield 970 from dojson module needed
        return {
            "resourceTypeGeneral": "Other",
            "resourceType": "Text",
        }

    def get_titles(self, obj):
        """Get titles list."""
        fields = obj["metadata"]["fields"]
        titles = fields.get("245", [{"subfields": {}}])[0]
        return {"title": titles.get("subfields", {}).get("a", [""])[0]}

    def get_publication_year(self, obj):
        """Get publication year from edtf date."""
        fields = obj["metadata"]["fields"]
        publication_dates = fields.get("362", [{"subfields": {}}])[0]
        publication_date = publication_dates.get("subfields", {}).get("a", [""])[0]
        return publication_date

    def get_language(self, obj):
        """Get language."""
        fields = obj["metadata"]["fields"]
        languages = fields.get("languages", [])
        if languages:
            # DataCite support only one language, so we take the first.
            return languages[0]["id"]

        return missing

    def get_identifiers(self, obj):
        """Get (main and alternate) identifiers list."""
        serialized_identifiers = []

        # pids go first so the DOI from the record is included
        pids = obj["pids"]
        for scheme, id_ in pids.items():
            id_scheme = get_scheme_datacite(
                scheme,
                "INVENIO_MARC21_IDENTIFIERS_SCHEMES",
                default=scheme,
            )

            if id_scheme:
                serialized_identifiers.append(
                    {
                        "identifier": id_["identifier"],
                        "identifierType": id_scheme,
                    }
                )

        return serialized_identifiers or missing

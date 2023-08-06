# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2020-2021 CERN.
# Copyright (C) 2020 Northwestern University.
# Copyright (C) 2021 TU Wien.
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Marc21 Record Resource."""


from flask_resources import route
from invenio_drafts_resources.resources import RecordResource

from . import config


#
# Records
#
class Marc21RecordResource(RecordResource):
    """Bibliographic record resource."""

    config_name = "MARC21_RECORDS_RECORD_CONFIG"
    default_config = config.Marc21RecordResourceConfig

    def p(self, route):
        """Prefix a route with the URL prefix."""
        return f"{self.config.url_prefix}{route}"

    def create_url_rules(self):
        """Create the URL rules for the record resource."""
        routes = self.config.routes

        def p(route):
            """Prefix a route with the URL prefix."""
            return f"{self.config.url_prefix}{route}"

        rules = [
            route("GET", p(routes["list"]), self.search),
            route("POST", p(routes["list"]), self.create),
            route("GET", p(routes["item"]), self.read),
            route("PUT", p(routes["item"]), self.update),
            route("DELETE", p(routes["item"]), self.delete),
            route("GET", p(routes["item-versions"]), self.search_versions),
            route("POST", p(routes["item-versions"]), self.new_version),
            route("GET", p(routes["item-latest"]), self.read_latest),
            route("GET", p(routes["item-draft"]), self.read_draft),
            route("POST", p(routes["item-draft"]), self.edit),
            route("PUT", p(routes["item-draft"]), self.update_draft),
            route("DELETE", p(routes["item-draft"]), self.delete_draft),
            route("POST", p(routes["item-publish"]), self.publish),
        ]

        if self.service.draft_files:
            rules.append(
                route(
                    "POST",
                    p(routes["item-files-import"]),
                    self.import_files,
                    apply_decorators=False,
                )
            )

        return rules


class Marc21ParentRecordLinksResource(RecordResource):
    """Secret links resource."""

    def create_url_rules(self):
        """Create the URL rules for the record resource."""

        def p(route):
            """Prefix a route with the URL prefix."""
            return f"{self.config.url_prefix}{route}"

        routes = self.config.routes
        return [
            route("GET", p(routes["list"]), self.search),
            route("POST", p(routes["list"]), self.create),
            route("GET", p(routes["item"]), self.read),
            route("PUT", p(routes["item"]), self.update),
            route("DELETE", p(routes["item"]), self.delete),
        ]

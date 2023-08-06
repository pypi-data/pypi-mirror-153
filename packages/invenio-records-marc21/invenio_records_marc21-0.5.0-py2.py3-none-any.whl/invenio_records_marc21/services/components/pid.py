# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Marc21 external pid component."""

from invenio_drafts_resources.services.records.components import (
    PIDComponent as BasePIDComponent,
)


class PIDComponent(BasePIDComponent):
    """Service component for pids integration."""

    def create(self, identity, data=None, record=None, **kwargs):
        """Create PID when record is created.."""
        self.service.record_cls.pid.create(record)

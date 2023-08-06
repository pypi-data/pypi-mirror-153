# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""JS/CSS Webpack bundles for theme."""

from invenio_assets.webpack import WebpackThemeBundle

theme = WebpackThemeBundle(
    __name__,
    "assets",
    default="semantic-ui",
    themes={
        "semantic-ui": dict(
            entry={
                "invenio-records-marc21-theme": "./less/invenio_records_marc21/theme.less",
                "invenio-records-marc21-deposit": "./js/invenio_records_marc21/deposit/index.js",
                "invenio-records-marc21-search": "./js/invenio_records_marc21/search/index.js",
                "invenio-records-marc21-landing-page": "./js/invenio_records_marc21/landing_page/index.js",
            },
            dependencies={
                "@babel/runtime": "^7.9.0",
                "clean-webpack-plugin": "4.0.0",
                "react-dropzone": "^11.0.3",
                "react-dnd-html5-backend": "^11.1.3",
                "prismjs": "1.25.0",
                "react-redux": "^7.1.0",
                "formik": "^2.1.4",
                "path": "^0.12.7",
                "axios": "^0.21.1",  # load from website data
                "luxon": "^1.23.0",
                "prop-types": "^15.7.2",
                "react-dnd": "^11.1.3",
                "marcjs": "^2.0.1",
                "react-invenio-deposit": "^0.16.1",
                "react-invenio-forms": "^0.8.7",
                "i18next": "^20.3.1",
                "react-i18next": "^11.11.3",
                "i18next-browser-languagedetector": "^6.1.1",
            },
            aliases={
                "@less/invenio_records_marc21": "./less/invenio_records_marc21",
            },
        ),
    },
)

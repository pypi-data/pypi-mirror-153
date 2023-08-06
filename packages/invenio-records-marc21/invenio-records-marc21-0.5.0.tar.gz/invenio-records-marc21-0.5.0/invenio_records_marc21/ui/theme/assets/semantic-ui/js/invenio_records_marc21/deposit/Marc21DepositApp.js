// This file is part of Invenio.
//
// Copyright (C) 2021 Graz University of Technology.
//
// Invenio-Records-Marc21 is free software; you can redistribute it and/or
// modify it under the terms of the MIT License; see LICENSE file for more
// details.

import React, { Component } from "react";
import { Provider } from "react-redux";

import { configureStore } from "./store";
import { Marc21RecordSchema } from "./Marc21RecordSchema";
import { Marc21Controller } from "./Marc21Controller";
import { Marc21ApiHandler } from "./Marc21ApiHandler";
import { Marc21FormHandler } from "./Marc21FormHandler";
import { Marc21RecordSerializer } from "./Marc21RecordSerializer";

export class Marc21DepositApp extends Component {
  constructor(props) {
    super(props);
    const fileUploader = props.fileUploader;

    const schema = props.schema
      ? props.schema
      : new Marc21RecordSchema(props.config.link, props.config.schema);

    const apihandler = new Marc21ApiHandler(props.config.createUrl);

    const recordSerializer = props.recordSerializer
      ? props.recordSerializer
      : new Marc21RecordSerializer();

    const controller = props.controller
      ? props.controller
      : new Marc21Controller(apihandler, schema);

    this.record_init = recordSerializer.deserialize(props.record);

    const appConfig = {
      config: props.config,
      record: this.record_init,
      files: props.files,
      schema: schema,
      controller: controller,
      apihandler: apihandler,
      fileUploader: fileUploader,
      permissions: props.permissions,
      recordSerializer: recordSerializer,
    };

    const submitFormData = props.submitFormData
      ? props.submitFormData
      : submitFormData;

    this.store = configureStore(appConfig);
  }

  render() {
    return (
      <Provider store={this.store}>
        <Marc21FormHandler props={this.props}>
          {this.props.children}
        </Marc21FormHandler>
      </Provider>
    );
  }
}

Marc21DepositApp.propTypes = {};

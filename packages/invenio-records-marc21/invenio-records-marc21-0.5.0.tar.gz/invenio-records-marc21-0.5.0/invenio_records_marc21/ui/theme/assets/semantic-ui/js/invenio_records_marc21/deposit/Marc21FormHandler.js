// This file is part of Invenio.
//
// Copyright (C) 2021 Graz University of Technology.
//
// Invenio-Records-Marc21 is free software; you can redistribute it and/or
// modify it under the terms of the MIT License; see LICENSE file for more
// details.

import React, { Component } from "react";
import { connect } from "react-redux";
import { BaseForm } from "react-invenio-forms";
import { submitFormData } from "./state/actions";

class Marc21FormHandlerComponent extends Component {
  componentDidMount() {
    window.addEventListener("beforeunload", (e) => {
      if (this.props.fileUploadOngoing) {
        e.returnValue = "";
        return "";
      }
    });
    window.addEventListener("unload", async (e) => {
      // TODO: cancel all uploads
      // Investigate if it's possible to wait for the deletion request to complete
      // before unloading the page
    });
  }

  render() {
    return (
      <BaseForm
        onSubmit={this.props.submitFormData}
        formik={{
          enableReinitialize: true,
          initialValues: this.props.record,
          ...(this.props.errors && { initialErrors: this.props.errors }),
        }}
      >
        {this.props.children}
      </BaseForm>
    );
  }
}

const mapStateToProps = (state) => {
  return {
    record: state.deposit.record,
    formState: state.deposit.formState,
  };
};

const mapDispatchToProps = (dispatch) => ({
  submitFormData: (values, formik) => dispatch(submitFormData(values, formik)),
});

export const Marc21FormHandler = connect(
  mapStateToProps,
  mapDispatchToProps
)(Marc21FormHandlerComponent);

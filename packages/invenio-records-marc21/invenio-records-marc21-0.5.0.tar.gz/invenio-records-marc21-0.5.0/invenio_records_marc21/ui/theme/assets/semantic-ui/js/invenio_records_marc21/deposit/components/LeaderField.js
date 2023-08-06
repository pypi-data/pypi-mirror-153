// This file is part of Invenio.
//
// Copyright (C) 2021 Graz University of Technology.
//
// Invenio-Records-Marc21 is free software; you can redistribute it and/or
// modify it under the terms of the MIT License; see LICENSE file for more
// details.

import React, { Component } from "react";
import PropTypes from "prop-types";

import { TextField } from "react-invenio-forms";

export class LeaderField extends Component {
  render() {
    const { fieldPath } = this.props;
    return (
      <>
        <TextField value={"LDR"} width={2} />
        <TextField
          fieldPath={`${fieldPath}`}
          width={14}
          required
          maxLength={24}
        />
      </>
    );
  }
}

LeaderField.propTypes = {
  fieldPath: PropTypes.string.isRequired,
  helpText: PropTypes.oneOfType([PropTypes.string, PropTypes.object]),
};

LeaderField.defaultProps = {
  helpText: "",
};

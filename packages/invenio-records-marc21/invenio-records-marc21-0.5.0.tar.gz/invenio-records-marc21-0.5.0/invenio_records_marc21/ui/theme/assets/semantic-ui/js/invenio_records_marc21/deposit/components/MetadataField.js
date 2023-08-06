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

export class MetadataField extends Component {
  render() {
    const { fieldPath } = this.props;
    return (
      <>
        <TextField fieldPath={`${fieldPath}.id`} width={3} required />
        <TextField fieldPath={`${fieldPath}.ind1`} width={2} />
        <TextField fieldPath={`${fieldPath}.ind2`} width={2} />
        <TextField fieldPath={`${fieldPath}.subfield`} width={15} required />
      </>
    );
  }
}

MetadataField.propTypes = {
  fieldPath: PropTypes.string.isRequired,
  width: PropTypes.number,
  helpText: PropTypes.oneOfType([PropTypes.string, PropTypes.object]),
};

MetadataField.defaultProps = {
  helpText: "",
};

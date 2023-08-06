// This file is part of Invenio.
//
// Copyright (C) 2021 Graz University of Technology.
//
// Invenio-Records-Marc21 is free software; you can redistribute it and/or
// modify it under the terms of the MIT License; see LICENSE file for more
// details.

import React, { Component } from "react";
import PropTypes from "prop-types";
import { ArrayField } from "react-invenio-forms";
import { Button, Form, Icon } from "semantic-ui-react";
import _get from "lodash/get";
import { GroupField } from "react-invenio-forms";
import { MetadataField, LeaderField } from ".";
export class MetadataFields extends Component {
  render() {
    const { fieldPath } = this.props;
    return (
      <>
        <GroupField fieldPath={`${fieldPath}.leader`}>
          <LeaderField fieldPath={`${fieldPath}.leader`} />
        </GroupField>
        <ArrayField
          addButtonLabel={"Add"}
          fieldPath={`${fieldPath}.fields`}
          defaultNewValue={{ id: "", ind1: "", ind2: "", subfield: "" }}
        >
          {({ array, arrayHelpers, indexPath, key }) => (
            <GroupField fieldPath={fieldPath}>
              <MetadataField fieldPath={key} />
              <Form.Field width={1}>
                <Button icon onClick={() => arrayHelpers.remove(indexPath)}>
                  <Icon name="close" />
                </Button>
              </Form.Field>
            </GroupField>
          )}
        </ArrayField>
      </>
    );
  }
}

MetadataFields.propTypes = {
  fieldPath: PropTypes.string,
};

MetadataFields.defaultProps = {
  fieldPath: "metadata",
};

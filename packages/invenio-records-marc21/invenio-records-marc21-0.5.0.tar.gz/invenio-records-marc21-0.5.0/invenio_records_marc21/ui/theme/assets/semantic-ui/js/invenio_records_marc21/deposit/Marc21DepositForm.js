// This file is part of Invenio.
//
// Copyright (C) 2021 Graz University of Technology.
//
// Invenio-Records-Marc21 is free software; you can redistribute it and/or
// modify it under the terms of the MIT License; see LICENSE file for more
// details.

import _get from "lodash/get";
import React, { Component, createRef } from "react";
import { SaveButton, PublishButton } from "./components";
import { Marc21DepositApp } from "./Marc21DepositApp";
import { AccordionField, MetadataFields } from "./components";
import { Card, Container, Grid, Ref, Sticky } from "semantic-ui-react";
import { TemplateField } from "./components/TemplateField";
import { AccessRightField } from "react-invenio-deposit";
export class Marc21DepositForm extends Component {
  constructor(props) {
    super(props);
    this.props = props;
    this.config = props.config || {};
    this.templates = props.templates || [];
    this.files = props.files;
    this.noFiles = true;
  }

  sidebarRef = createRef();

  accordionStyle = {
    header: { className: "segment inverted brand" },
  };

  render() {
    return (
      <Marc21DepositApp
        config={this.config}
        record={this.props.record}
        files={this.props.files}
        permissions={this.props.permissions}
        templates={this.templates}
      >
        <Container style={{ marginTop: "10px" }}>
          {/* <DepositFormTitle /> */}
          <Grid>
            <Grid.Row>
              <Grid.Column width={11}>
                <AccordionField
                  fieldPath=""
                  active={true}
                  label={"Metadata"}
                  ui={this.accordionStyle}
                >
                  <MetadataFields className={"metadata"} fieldPath="metadata" />
                </AccordionField>
              </Grid.Column>
              {/* Sidebar start */}
              <Ref innerRef={this.sidebarRef}>
                <Grid.Column width={5} className="deposit-sidebar">
                  <Card className="actions">
                    <Card.Content>
                      <div className="sidebar-buttons">
                        <SaveButton fluid className="save-button" />
                      </div>
                      <PublishButton fluid />
                    </Card.Content>
                  </Card>
                  <Sticky context={this.sidebarRef} offset={10}>
                    {this.templates.length > 0 && (
                      <TemplateField
                        label={"Templates"}
                        labelIcon={"bookmark"}
                        templates={this.templates}
                      />
                    )}
                  </Sticky>
                  <AccessRightField label={"Visibility"} labelIcon={"shield"} />
                </Grid.Column>
              </Ref>
            </Grid.Row>
          </Grid>
        </Container>
      </Marc21DepositApp>
    );
  }
}

// This file is part of Invenio.
//
// Copyright (C) 2021 Graz University of Technology.
//
// Invenio-Records-Marc21 is free software; you can redistribute it and/or
// modify it under the terms of the MIT License; see LICENSE file for more
// details.

import {
  ACTION_CREATE_SUCCEEDED,
  ACTION_SAVE_SUCCEEDED,
  ACTION_SAVE_FAILED,
  ACTION_PUBLISH_FAILED,
  ACTION_PUBLISH_SUCCEEDED,
} from "./state/types";
import _isEmpty from "lodash/isEmpty";
import _set from "lodash/set";
import _has from "lodash/has";

export class Marc21Controller {
  constructor(apihandler, schema) {
    this.apihandler = apihandler;
    this.schema = schema;
  }

  /**
   * Creates the current draft (backend) and changes URL to match its edit URL.
   *
   * @param {object} draft - current draft
   * @param {object} store - redux store
   */
  async createDraft(draft, { store }) {
    const recordSerializer = store.config.recordSerializer;
    const payload = recordSerializer.serialize(draft);
    const response = await this.apihandler.create(payload);

    if (_has(response, ["data", "ui", "metadata"])) {
      _set(response.data, "metadata", response.data.ui.metadata);
    }
    store.dispatch({
      type: ACTION_CREATE_SUCCEEDED,
      payload: { data: recordSerializer.deserialize(response.data) },
    });

    const draftURL = response.data.links.self_html;
    window.history.replaceState(undefined, "", draftURL);
    return response;
  }

  draftAlreadyCreated(record) {
    return record.id ? true : false;
  }

  /**
   * Saves the current draft (backend) and changes URL to match its edit URL.
   *
   * @param {object} draft - current draft
   * @param {object} formik - the Formik object
   * @param {object} store - redux store
   */
  async saveDraft(draft, { formik, store }) {
    const recordSerializer = store.config.recordSerializer;
    // Set defaultPreview for files
    draft = _set(
      draft,
      "defaultFilePreview",
      store.getState().deposit.defaultFilePreview
    );

    let response = {};
    //let payload = recordSerializer.serialize(draft);
    if (!this.draftAlreadyCreated(draft)) {
      response = await this.createDraft(draft, { store });
    } else {
      let payload = recordSerializer.serialize(draft);
      response = await this.apihandler.save(payload);
    }

    if (_has(response, ["data", "ui", "metadata"])) {
      _set(response.data, "metadata", response.data.ui.metadata);
    }

    let data = recordSerializer.deserialize(response.data || {});
    let errors = recordSerializer.deserializeErrors(response.errors || []);

    // response 100% successful
    if (200 <= response.code && response.code < 300 && _isEmpty(errors)) {
      store.dispatch({
        type: ACTION_SAVE_SUCCEEDED,
        payload: { data },
      });
    }
    // response exceptionally bad
    else {
      store.dispatch({
        type: ACTION_SAVE_FAILED,
        payload: { errors },
      });
      formik.setErrors(errors);
    }

    formik.setSubmitting(false);
  }

  /**
   * Publishes the current draft (backend) and redirects to its view URL.
   *
   * @param {object} draft - current draft
   * @param {object} formik - the Formik object
   * @param {object} store - redux store
   */
  async publishDraft(draft, { formik, store }) {
    const recordSerializer = store.config.recordSerializer;
    let response = {};

    if (!this.draftAlreadyCreated(draft)) {
      response = await this.createDraft(draft, { store });
    } else {
      let payload = recordSerializer.serialize(draft);
      response = await this.apihandler.save(payload);
    }

    let payload = recordSerializer.serialize(draft);
    response = await this.apihandler.publish(payload);

    let data = recordSerializer.deserialize(response.data || {});
    let errors = recordSerializer.deserializeErrors(response.errors || []);

    // response 100% successful
    if (200 <= response.code && response.code < 300 && _isEmpty(errors)) {
      store.dispatch({
        type: ACTION_PUBLISH_SUCCEEDED,
        payload: { data },
      });
      const recordURL = response.data.links.self_html;
      window.location.replace(recordURL);
    }
    // "succeed or not, there is no partial"
    else {
      store.dispatch({
        type: ACTION_PUBLISH_FAILED,
        payload: { data, errors },
      });
      formik.setErrors(errors);
    }

    formik.setSubmitting(false);
  }
}

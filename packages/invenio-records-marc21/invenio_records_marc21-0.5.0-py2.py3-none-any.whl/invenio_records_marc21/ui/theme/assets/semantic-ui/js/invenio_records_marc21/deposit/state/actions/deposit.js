// This file is part of Invenio.
//
// Copyright (C) 2021 Graz University of Technology.
//
// Invenio-Records-Marc21 is free software; you can redistribute it and/or
// modify it under the terms of the MIT License; see LICENSE file for more
// details.

import {
  FORM_SAVING,
  FORM_PUBLISHING,
  FORM_ACTION_EVENT_EMITTED,
} from "../types";

export const save = (record, formik) => {
  return async (dispatch, getState, config) => {
    const controller = config.controller;
    controller.saveDraft(record, {
      formik,
      store: { dispatch, getState, config },
    });
  };
};

export const publish = (record, formik) => {
  return (dispatch, getState, config) => {
    const controller = config.controller;
    return controller.publishDraft(record, {
      formik,
      store: { dispatch, getState, config },
    });
  };
};

export const submitAction = (action, event, formik) => {
  return async (dispatch, getState, config) => {
    dispatch({
      type: FORM_ACTION_EVENT_EMITTED,
      payload: action,
    });
    formik.handleSubmit(event); // eventually calls submitFormData below
  };
};

export const submitFormData = (record, formik) => {
  return (dispatch, getState, config) => {
    const formState = getState().deposit.formState;
    switch (formState) {
      case FORM_SAVING:
        return dispatch(save(record, formik));
      case FORM_PUBLISHING:
        return dispatch(publish(record, formik));
      default:
        console.log(`onSubmit triggered with unknown action ${formState}`);
    }
  };
};

// This file is part of Invenio.
//
// Copyright (C) 2021 Graz University of Technology.
//
// Invenio-Records-Marc21 is free software; you can redistribute it and/or
// modify it under the terms of the MIT License; see LICENSE file for more
// details.

import {
  FORM_ACTION_EVENT_EMITTED,
  ACTION_CREATE_SUCCEEDED,
  FORM_SAVE_SUCCEEDED,
  FORM_SAVE_FAILED,
  FORM_PUBLISH_FAILED,
  FORM_PUBLISH_SUCCEEDED,
  ACTION_SAVE_SUCCEEDED,
  ACTION_SAVE_FAILED,
  ACTION_PUBLISH_FAILED,
  ACTION_PUBLISH_SUCCEEDED,
} from "../types";

export default (state = {}, action) => {
  switch (action.type) {
    case FORM_ACTION_EVENT_EMITTED:
      return {
        ...state,
        formState: action.payload,
      };
    case ACTION_CREATE_SUCCEEDED:
      return {
        ...state,
        record: { ...state.record, ...action.payload.data },
        formState: null,
      };
    case ACTION_SAVE_SUCCEEDED:
      return {
        ...state,
        record: { ...state.record, ...action.payload.data },
        errors: {},
        formState: FORM_SAVE_SUCCEEDED,
      };
    case ACTION_SAVE_FAILED:
      return {
        ...state,
        errors: { ...action.payload.errors },
        formState: FORM_SAVE_FAILED,
      };
    case ACTION_PUBLISH_SUCCEEDED:
      return {
        ...state,
        record: { ...state.record, ...action.payload.data },
        formState: FORM_PUBLISH_SUCCEEDED,
      };
    case ACTION_PUBLISH_FAILED:
      return {
        ...state,
        errors: { ...action.payload.errors },
        formState: FORM_PUBLISH_FAILED,
      };
    default:
      return state;
  }
};

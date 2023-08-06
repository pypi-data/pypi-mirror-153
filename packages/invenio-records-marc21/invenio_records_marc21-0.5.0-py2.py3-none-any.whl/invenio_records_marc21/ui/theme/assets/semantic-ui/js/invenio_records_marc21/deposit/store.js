// This file is part of Invenio.
//
// Copyright (C) 2021 Graz University of Technology.
//
// Invenio-Records-Marc21 is free software; you can redistribute it and/or
// modify it under the terms of the MIT License; see LICENSE file for more
// details.

import _cloneDeep from "lodash/cloneDeep";
import _get from "lodash/get";
import { createStore, compose, applyMiddleware } from "redux";
import thunk from "redux-thunk";
import rootReducer from "./state/reducers";

export const INITIAL_STORE_STATE = {
  formState: null,
};

export function configureStore(appConfig) {
  const { record, files, config, permissions, ...extra } = appConfig;
  const initialDepositState = {
    record,
    config,
    permissions,
    formState: null,
  };
  const preloadedState = {
    deposit: initialDepositState,
  };

  const composeEnhancers =
    window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ || compose;
  return createStore(
    rootReducer,
    preloadedState,
    composeEnhancers(applyMiddleware(thunk.withExtraArgument(extra)))
  );
}

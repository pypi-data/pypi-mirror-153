// This file is part of Invenio.
//
// Copyright (C) 2021 Graz University of Technology.
//
// Invenio-Records-Marc21 is free software; you can redistribute it and/or
// modify it under the terms of the MIT License; see LICENSE file for more
// details.
import axios from "axios";

const CancelToken = axios.CancelToken;
const apiConfig = {
  withCredentials: true,
  xsrfCookieName: "csrftoken",
  xsrfHeaderName: "X-CSRFToken",
};
const axiosWithconfig = axios.create(apiConfig);

/**
 * API client response.
 *
 * It's a wrapper/sieve around Axios to contain Axios coupling here. It maps
 * good and bad responses to a unified interface.
 *
 */
export class Marc21ApiResponse {
  constructor(data, errors, code) {
    this.data = data;
    this.errors = errors;
    this.code = code;
  }
}

/**
 * API Client for deposits.
 *
 * It mostly uses the API links passed to it from responses.
 *
 */
export class Marc21ApiHandler {
  constructor(createUrl) {
    this.createUrl = createUrl;
  }

  async createResponse(axios_call) {
    try {
      let response = await axios_call();
      return new Marc21ApiResponse(
        response.data,
        response.data.errors,
        response.status
      );
    } catch (error) {
      const err = error.response.data;
      return new Marc21ApiResponse(
        error.response.data,
        error.response.data.errors,
        error.response.status
      );
    }
  }

  /**
   * Calls the API to create a new draft.
   *
   * @param {object} draft - Serialized draft
   */
  async create(draft) {
    return this.createResponse(() =>
      axiosWithconfig.post(this.createUrl, draft, {
        headers: {
          "Content-Type": "application/json",
          Accept: "application/vnd.inveniomarc21.v1+marcxml",
        },
      })
    );
  }

  /**
   * Calls the API to save a pre-existing draft.
   *
   * @param {object} draft - Serialized draft
   */
  async save(draft) {
    return this.createResponse(() =>
      axiosWithconfig.put(draft.links.self, draft, {
        headers: {
          "Content-Type": "application/json",
          Accept: "application/vnd.inveniomarc21.v1+marcxml",
        },
      })
    );
  }

  /**
   * Publishes the draft by calling its publish link.
   *
   * @param {object} draft - the payload from create()
   */
  async publish(draft) {
    return this.createResponse(() =>
      axiosWithconfig.post(draft.links.publish, draft, {
        headers: {
          "Content-Type": "application/json",
          Accept: "application/vnd.inveniomarc21.v1+marcxml",
        },
      })
    );
  }

  /**
   * Deletes the draft by calling DELETE on its self link.
   *
   * @param {object} draft - the payload from create()/save()
   */
  async delete(draft) {
    return this.createResponse(() =>
      axiosWithconfig.delete(
        draft.links.self,
        {},
        {
          headers: { "Content-Type": "application/json" },
        }
      )
    );
  }
}

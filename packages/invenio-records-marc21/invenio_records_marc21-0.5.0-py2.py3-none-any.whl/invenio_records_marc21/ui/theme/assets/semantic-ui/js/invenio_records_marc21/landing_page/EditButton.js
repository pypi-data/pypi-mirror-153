// This file is part of Invenio.
//
// Copyright (C) 2021 Northwestern University.
// Copyright (C) 2021 Graz University of Technology.
//
// Invenio-Records-Marc21 is free software; you can redistribute it and/or
// modify it under the terms of the MIT License; see LICENSE file for more
// details.

import React, { useState } from "react";
import { Icon, Button } from "semantic-ui-react";
import axios from "axios";

const apiConfig = {
  withCredentials: true,
  xsrfCookieName: "csrftoken",
  xsrfHeaderName: "X-CSRFToken",
};

export const axiosWithconfig = axios.create(apiConfig);

export const EditButton = (props) => {
  const [loading, setLoading] = useState(false);
  const recid = props.recid;
  const handleError = props.onError;
  const handleClick = () => {
    setLoading(true);
    axiosWithconfig
      .post(`/api/marc21/${recid}/draft`)
      .then((response) => {
        window.location = `/marc21/uploads/${recid}`;
      })
      .catch((error) => {
        setLoading(false);
        handleError(error.response.data.message);
      });
  };

  return (
    <Button color="orange" size="mini" onClick={handleClick} loading={loading}>
      <Icon name="edit" />
      {"Edit"}
    </Button>
  );
};

// This file is part of Invenio.
//
// Copyright (C) 2021 Graz University of Technology.
//
// Invenio-Records-Marc21 is free software; you can redistribute it and/or
// modify it under the terms of the MIT License; see LICENSE file for more
// details.

import _cloneDeep from "lodash/cloneDeep";
import _defaults from "lodash/defaults";
import _pick from "lodash/pick";
import _set from "lodash/set";

import { Field, MetadataFields } from "./fields";

export class Marc21RecordSerializer {
  constructor() {}

  depositRecordSchema = {
    access: new Field({
      fieldpath: "access",
      deserializedDefault: {
        record: "public",
        files: "public",
      },
    }),
    files: new Field({
      fieldpath: "files",
    }),
    links: new Field({
      fieldpath: "links",
    }),
    pids: new Field({
      fieldpath: "pids",
      deserializedDefault: {},
      serializedDefault: {},
    }),
    metadata: new MetadataFields({
      fieldpath: "metadata",
      deserializedDefault:
        "<record> <leader>00000nam a2200000zca4500</leader></record>",
      serializedDefault: "",
    }),
  };

  /**
   * Deserialize backend record into format compatible with frontend.
   * @method
   * @param {object} record - potentially empty object
   * @returns {object} frontend compatible record object
   */
  deserialize(record) {
    record = _cloneDeep(record);

    let deserializedRecord = record;
    deserializedRecord = _pick(deserializedRecord, [
      "access",
      "metadata",
      "id",
      "links",
      "files",
      "pids",
    ]);
    for (let key in this.depositRecordSchema) {
      deserializedRecord =
        this.depositRecordSchema[key].deserialize(deserializedRecord);
    }
    return deserializedRecord;
  }

  /**
   * Deserialize backend record errors into format compatible with frontend.
   * @method
   * @param {array} errors - array of error objects
   * @returns {object} - object representing errors
   */
  deserializeErrors(errors) {
    let deserializedErrors = {};
    for (let e of errors) {
      _set(deserializedErrors, e.field, e.messages.join(" "));
    }

    return deserializedErrors;
  }

  /**
   * Serialize record to send to the backend.
   * @method
   * @param {object} record - in frontend format
   * @returns {object} record - in API format
   *
   */
  serialize(record) {
    record = _cloneDeep(record);
    let serializedRecord = record; //this.removeEmptyValues(record);
    serializedRecord = _pick(serializedRecord, [
      "access",
      "metadata",
      "id",
      "links",
      "files",
      "pids",
    ]);
    for (let key in this.depositRecordSchema) {
      serializedRecord =
        this.depositRecordSchema[key].serialize(serializedRecord);
    }

    _defaults(serializedRecord, { metadata: {} });

    return serializedRecord;
  }
}

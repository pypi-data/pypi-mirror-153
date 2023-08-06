(self["webpackChunk_elyra_python_editor_extension"] = self["webpackChunk_elyra_python_editor_extension"] || []).push([["ui-components_lib_FormComponents_PasswordField_js-ui-components_lib_FormComponents_index_js-u-7d59f0"],{

/***/ "../../node_modules/css-loader/dist/cjs.js!../ui-components/style/formeditor.css":
/*!***************************************************************************************!*\
  !*** ../../node_modules/css-loader/dist/cjs.js!../ui-components/style/formeditor.css ***!
  \***************************************************************************************/
/***/ ((module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../../../node_modules/css-loader/dist/runtime/cssWithMappingToString.js */ "../../node_modules/css-loader/dist/runtime/cssWithMappingToString.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../../../node_modules/css-loader/dist/runtime/api.js */ "../../node_modules/css-loader/dist/runtime/api.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__);
// Imports


var ___CSS_LOADER_EXPORT___ = _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default()((_node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0___default()));
// Module
___CSS_LOADER_EXPORT___.push([module.id, "/*\n * Copyright 2018-2022 Elyra Authors\n *\n * Licensed under the Apache License, Version 2.0 (the \"License\");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n * http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an \"AS IS\" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n */\n\n.elyra-tags {\n  margin-top: 8px;\n}\n\n.rjsf > .form-group.field,\n.form-group.field.tagsField,\n.form-group.field.languageField {\n  width: 100%;\n}\n\n.panel.panel-danger.errors,\np#root__description,\nbutton.btn[type='submit'] {\n  display: none;\n}\n\nli.text-danger {\n  color: var(--jp-error-color1);\n  padding: 5px 0 0 9px;\n}\n\nform.rjsf {\n  width: 100%;\n}\n\nfieldset#root > div > fieldset {\n  display: flex;\n  flex-wrap: wrap;\n}\n\nlabel.control-label {\n  font-size: var(--jp-content-font-size2);\n  font-weight: 500;\n}\n\nfieldset#root {\n  display: flex;\n  flex-wrap: wrap;\n  width: 100%;\n  justify-content: space-between;\n}\n\n.form-group.field {\n  padding: 0px 30px 15px 0;\n  display: flex;\n  flex-direction: column;\n  width: 50%;\n  position: relative;\n  height: fit-content;\n  min-width: 400px;\n}\n\n.elyra-formEditor datalist {\n  display: none;\n}\n\n.elyra-inputTagList {\n  list-style: none;\n}\n\n.elyra-inputTag {\n  margin-left: 8px;\n  margin-right: 8px;\n}\n\nbutton.elyra-inputTag {\n  cursor: pointer;\n  background: none;\n  border: none;\n  color: var(--jp-ui-font-color2);\n  padding: 0;\n  font-size: var(--jp-ui-font-size1);\n}\n\n.field-object > fieldset > legend {\n  font-size: var(--jp-content-font-size3);\n  padding-bottom: 15px;\n  font-weight: 600;\n}\n\nlegend#root__noCategory__title {\n  display: none;\n}\n\n.form-group input[readonly] {\n  background: var(--jp-border-color3);\n}\n\n.form-group.field.field-object {\n  width: 100%;\n  padding: 0;\n}\n\n.jp-ArrayOperations button:disabled {\n  cursor: not-allowed;\n}\n\n.elyra-passwordFieldButton {\n  border: none;\n  border-radius: 5px;\n  background: var(--jp-input-active-background);\n  position: absolute;\n  right: 6px;\n  bottom: 5px;\n}\n\n.elyra-passwordFieldButton > div {\n  display: grid;\n}\n\n.elyra-passwordField {\n  position: relative;\n  display: flex;\n}\n\n.elyra-passwordFieldButton:hover {\n  background-color: var(--jp-border-color2);\n}\n\n.elyra-passwordFieldButton svg {\n  width: 25px;\n  display: flex;\n  color: var(--jp-content-font-color0);\n}\n\ninput.elyra-inputTag {\n  font-size: var(--jp-ui-font-size1);\n  background: none;\n  border: none;\n  color: var(--jp-ui-font-color2);\n  font-size: var(--jp-ui-font-size1);\n  width: 80px;\n  height: 15px;\n}\n\n.form-group .form-control {\n  padding: 8px;\n  border: 1px solid var(--jp-border-color1);\n  border-radius: 4px;\n  font-size: var(--jp-content-font-size2);\n  margin-top: 10px;\n  width: 100%;\n  background-color: var(--jp-input-active-background);\n  color: var(--jp-content-font-color0);\n}\n\n.elyra-editor-tagList {\n  list-style: none;\n  margin-left: -3px;\n  margin-top: 4px;\n}\n\n.elyra-editor-tag {\n  margin-left: 3px;\n  margin-right: 3px;\n  padding: 0 12px;\n  height: 24px;\n}\n\nbutton.elyra-editor-tag {\n  cursor: pointer;\n  color: var(--jp-ui-font-color2);\n  font-size: var(--jp-ui-font-size1);\n}\n\nbutton.elyra-editor-tag.applied-tag {\n  color: var(--jp-ui-font-color1);\n}\n\nbutton.elyra-editor-tag.unapplied-tag {\n  color: var(--jp-ui-font-color2);\n  white-space: nowrap;\n}\n\n.elyra-editor-tag.tag.unapplied-tag input {\n  border: none;\n}\n\n.elyra-formEditor h3 {\n  flex-basis: 100%;\n  margin-bottom: 15px;\n  color: var(--jp-ui-font-color1);\n}\n\n.elyra-formEditor .elyra-form-code.jp-CodeMirrorEditor {\n  background-color: var(--jp-cell-editor-background);\n  border: var(--jp-border-width) solid var(--jp-input-border-color);\n  overflow-y: auto;\n  resize: vertical;\n  min-height: 150px;\n  height: 150px;\n  padding-bottom: 10px;\n  cursor: initial;\n  margin-top: 5px;\n}\n\n.elyra-formEditor .CodeMirror.cm-s-jupyter {\n  background-color: inherit;\n  height: 100%;\n}\n\n.elyra-formEditor .elyra-formEditor-code {\n  height: auto;\n  flex-basis: 100%;\n  display: flex;\n  flex-direction: column;\n}\n\n.elyra-formEditor-formInput {\n  margin: 10px;\n  flex-basis: 45%;\n}\n\n.elyra-formEditor .elyra-formEditor-saveButton {\n  flex-basis: 100%;\n  display: flex;\n  flex-direction: column;\n  padding-bottom: 15px;\n}\n\n.elyra-formEditor .form-group.field.elyra-formEditor-form-code,\n.elyra-formEditor .form-group.field.elyra-formEditor-form-tags {\n  width: 80%;\n}\n\n.elyra-formEditor .field-description {\n  display: none;\n}\n\n.elyra-formEditor .description-wrapper:hover .field-description {\n  color: var(--jp-content-font-color1);\n  position: absolute;\n  bottom: 110%;\n  left: 50%;\n  transform: translate(-50%, -10%);\n  background-color: var(--jp-border-color3);\n  border: 1px solid var(--jp-border-color2);\n  padding: 5px;\n  border-radius: 5px;\n  display: initial;\n  max-width: 22ch;\n  width: max-content;\n  word-wrap: break-word;\n  z-index: 1;\n}\n\n.elyra-formEditor select.form-control {\n  -moz-appearance: none !important;\n  -webkit-appearance: none;\n  background-image: url(\"data:image/svg+xml;utf8,<svg fill='black' height='24' viewBox='0 0 24 24' width='24' xmlns='http://www.w3.org/2000/svg'><path d='M7 10l5 5 5-5z'/><path d='M0 0h24v24H0z' fill='none'/></svg>\");\n  background-repeat: no-repeat;\n  background-position-x: calc(100% - 4px);\n  background-position-y: 50%;\n}\n\n.elyra-formEditor\n  .label-header\n  .description-wrapper\n  p.field-description.short-title {\n  transform: translate(-20%, -10%);\n}\n\n.elyra-formEditor .form-group.field-array .label-header {\n  margin-bottom: 10px;\n}\n\n.elyra-formEditor .description-wrapper {\n  width: fit-content;\n  position: relative;\n}\n\n.elyra-formEditor .description-button {\n  border-radius: 100%;\n  margin-left: 6px;\n  border: 1px solid var(--jp-border-color1);\n  background: none;\n  color: var(--jp-border-color0);\n  padding: 2px 5px;\n}\n\n.elyra-formEditor .label-header {\n  display: flex;\n  align-items: center;\n}\n\n.elyra-formEditor .array-item {\n  display: flex;\n  margin-bottom: 15px;\n}\n\n.elyra-formEditor .field-array button {\n  border-radius: 3px;\n  margin-top: 4px;\n}\n\n.elyra-formEditor .array-item .form-group.field {\n  padding-bottom: 0;\n  padding-right: 10px;\n}\n\n.elyra-formEditor .array-item .form-group.field input {\n  margin-top: 0;\n}\n\n.elyra-formEditor .jp-ArrayOperations {\n  display: flex;\n}\n\n.elyra-formEditor .jp-ArrayOperations button {\n  width: max-content;\n}\n\n.elyra-formEditor .field.field-array {\n  width: 100%;\n}\n", "",{"version":3,"sources":["webpack://./../ui-components/style/formeditor.css"],"names":[],"mappings":"AAAA;;;;;;;;;;;;;;EAcE;;AAEF;EACE,eAAe;AACjB;;AAEA;;;EAGE,WAAW;AACb;;AAEA;;;EAGE,aAAa;AACf;;AAEA;EACE,6BAA6B;EAC7B,oBAAoB;AACtB;;AAEA;EACE,WAAW;AACb;;AAEA;EACE,aAAa;EACb,eAAe;AACjB;;AAEA;EACE,uCAAuC;EACvC,gBAAgB;AAClB;;AAEA;EACE,aAAa;EACb,eAAe;EACf,WAAW;EACX,8BAA8B;AAChC;;AAEA;EACE,wBAAwB;EACxB,aAAa;EACb,sBAAsB;EACtB,UAAU;EACV,kBAAkB;EAClB,mBAAmB;EACnB,gBAAgB;AAClB;;AAEA;EACE,aAAa;AACf;;AAEA;EACE,gBAAgB;AAClB;;AAEA;EACE,gBAAgB;EAChB,iBAAiB;AACnB;;AAEA;EACE,eAAe;EACf,gBAAgB;EAChB,YAAY;EACZ,+BAA+B;EAC/B,UAAU;EACV,kCAAkC;AACpC;;AAEA;EACE,uCAAuC;EACvC,oBAAoB;EACpB,gBAAgB;AAClB;;AAEA;EACE,aAAa;AACf;;AAEA;EACE,mCAAmC;AACrC;;AAEA;EACE,WAAW;EACX,UAAU;AACZ;;AAEA;EACE,mBAAmB;AACrB;;AAEA;EACE,YAAY;EACZ,kBAAkB;EAClB,6CAA6C;EAC7C,kBAAkB;EAClB,UAAU;EACV,WAAW;AACb;;AAEA;EACE,aAAa;AACf;;AAEA;EACE,kBAAkB;EAClB,aAAa;AACf;;AAEA;EACE,yCAAyC;AAC3C;;AAEA;EACE,WAAW;EACX,aAAa;EACb,oCAAoC;AACtC;;AAEA;EACE,kCAAkC;EAClC,gBAAgB;EAChB,YAAY;EACZ,+BAA+B;EAC/B,kCAAkC;EAClC,WAAW;EACX,YAAY;AACd;;AAEA;EACE,YAAY;EACZ,yCAAyC;EACzC,kBAAkB;EAClB,uCAAuC;EACvC,gBAAgB;EAChB,WAAW;EACX,mDAAmD;EACnD,oCAAoC;AACtC;;AAEA;EACE,gBAAgB;EAChB,iBAAiB;EACjB,eAAe;AACjB;;AAEA;EACE,gBAAgB;EAChB,iBAAiB;EACjB,eAAe;EACf,YAAY;AACd;;AAEA;EACE,eAAe;EACf,+BAA+B;EAC/B,kCAAkC;AACpC;;AAEA;EACE,+BAA+B;AACjC;;AAEA;EACE,+BAA+B;EAC/B,mBAAmB;AACrB;;AAEA;EACE,YAAY;AACd;;AAEA;EACE,gBAAgB;EAChB,mBAAmB;EACnB,+BAA+B;AACjC;;AAEA;EACE,kDAAkD;EAClD,iEAAiE;EACjE,gBAAgB;EAChB,gBAAgB;EAChB,iBAAiB;EACjB,aAAa;EACb,oBAAoB;EACpB,eAAe;EACf,eAAe;AACjB;;AAEA;EACE,yBAAyB;EACzB,YAAY;AACd;;AAEA;EACE,YAAY;EACZ,gBAAgB;EAChB,aAAa;EACb,sBAAsB;AACxB;;AAEA;EACE,YAAY;EACZ,eAAe;AACjB;;AAEA;EACE,gBAAgB;EAChB,aAAa;EACb,sBAAsB;EACtB,oBAAoB;AACtB;;AAEA;;EAEE,UAAU;AACZ;;AAEA;EACE,aAAa;AACf;;AAEA;EACE,oCAAoC;EACpC,kBAAkB;EAClB,YAAY;EACZ,SAAS;EACT,gCAAgC;EAChC,yCAAyC;EACzC,yCAAyC;EACzC,YAAY;EACZ,kBAAkB;EAClB,gBAAgB;EAChB,eAAe;EACf,kBAAkB;EAClB,qBAAqB;EACrB,UAAU;AACZ;;AAEA;EACE,gCAAgC;EAChC,wBAAwB;EACxB,sNAAsN;EACtN,4BAA4B;EAC5B,uCAAuC;EACvC,0BAA0B;AAC5B;;AAEA;;;;EAIE,gCAAgC;AAClC;;AAEA;EACE,mBAAmB;AACrB;;AAEA;EACE,kBAAkB;EAClB,kBAAkB;AACpB;;AAEA;EACE,mBAAmB;EACnB,gBAAgB;EAChB,yCAAyC;EACzC,gBAAgB;EAChB,8BAA8B;EAC9B,gBAAgB;AAClB;;AAEA;EACE,aAAa;EACb,mBAAmB;AACrB;;AAEA;EACE,aAAa;EACb,mBAAmB;AACrB;;AAEA;EACE,kBAAkB;EAClB,eAAe;AACjB;;AAEA;EACE,iBAAiB;EACjB,mBAAmB;AACrB;;AAEA;EACE,aAAa;AACf;;AAEA;EACE,aAAa;AACf;;AAEA;EACE,kBAAkB;AACpB;;AAEA;EACE,WAAW;AACb","sourcesContent":["/*\n * Copyright 2018-2022 Elyra Authors\n *\n * Licensed under the Apache License, Version 2.0 (the \"License\");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n * http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an \"AS IS\" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n */\n\n.elyra-tags {\n  margin-top: 8px;\n}\n\n.rjsf > .form-group.field,\n.form-group.field.tagsField,\n.form-group.field.languageField {\n  width: 100%;\n}\n\n.panel.panel-danger.errors,\np#root__description,\nbutton.btn[type='submit'] {\n  display: none;\n}\n\nli.text-danger {\n  color: var(--jp-error-color1);\n  padding: 5px 0 0 9px;\n}\n\nform.rjsf {\n  width: 100%;\n}\n\nfieldset#root > div > fieldset {\n  display: flex;\n  flex-wrap: wrap;\n}\n\nlabel.control-label {\n  font-size: var(--jp-content-font-size2);\n  font-weight: 500;\n}\n\nfieldset#root {\n  display: flex;\n  flex-wrap: wrap;\n  width: 100%;\n  justify-content: space-between;\n}\n\n.form-group.field {\n  padding: 0px 30px 15px 0;\n  display: flex;\n  flex-direction: column;\n  width: 50%;\n  position: relative;\n  height: fit-content;\n  min-width: 400px;\n}\n\n.elyra-formEditor datalist {\n  display: none;\n}\n\n.elyra-inputTagList {\n  list-style: none;\n}\n\n.elyra-inputTag {\n  margin-left: 8px;\n  margin-right: 8px;\n}\n\nbutton.elyra-inputTag {\n  cursor: pointer;\n  background: none;\n  border: none;\n  color: var(--jp-ui-font-color2);\n  padding: 0;\n  font-size: var(--jp-ui-font-size1);\n}\n\n.field-object > fieldset > legend {\n  font-size: var(--jp-content-font-size3);\n  padding-bottom: 15px;\n  font-weight: 600;\n}\n\nlegend#root__noCategory__title {\n  display: none;\n}\n\n.form-group input[readonly] {\n  background: var(--jp-border-color3);\n}\n\n.form-group.field.field-object {\n  width: 100%;\n  padding: 0;\n}\n\n.jp-ArrayOperations button:disabled {\n  cursor: not-allowed;\n}\n\n.elyra-passwordFieldButton {\n  border: none;\n  border-radius: 5px;\n  background: var(--jp-input-active-background);\n  position: absolute;\n  right: 6px;\n  bottom: 5px;\n}\n\n.elyra-passwordFieldButton > div {\n  display: grid;\n}\n\n.elyra-passwordField {\n  position: relative;\n  display: flex;\n}\n\n.elyra-passwordFieldButton:hover {\n  background-color: var(--jp-border-color2);\n}\n\n.elyra-passwordFieldButton svg {\n  width: 25px;\n  display: flex;\n  color: var(--jp-content-font-color0);\n}\n\ninput.elyra-inputTag {\n  font-size: var(--jp-ui-font-size1);\n  background: none;\n  border: none;\n  color: var(--jp-ui-font-color2);\n  font-size: var(--jp-ui-font-size1);\n  width: 80px;\n  height: 15px;\n}\n\n.form-group .form-control {\n  padding: 8px;\n  border: 1px solid var(--jp-border-color1);\n  border-radius: 4px;\n  font-size: var(--jp-content-font-size2);\n  margin-top: 10px;\n  width: 100%;\n  background-color: var(--jp-input-active-background);\n  color: var(--jp-content-font-color0);\n}\n\n.elyra-editor-tagList {\n  list-style: none;\n  margin-left: -3px;\n  margin-top: 4px;\n}\n\n.elyra-editor-tag {\n  margin-left: 3px;\n  margin-right: 3px;\n  padding: 0 12px;\n  height: 24px;\n}\n\nbutton.elyra-editor-tag {\n  cursor: pointer;\n  color: var(--jp-ui-font-color2);\n  font-size: var(--jp-ui-font-size1);\n}\n\nbutton.elyra-editor-tag.applied-tag {\n  color: var(--jp-ui-font-color1);\n}\n\nbutton.elyra-editor-tag.unapplied-tag {\n  color: var(--jp-ui-font-color2);\n  white-space: nowrap;\n}\n\n.elyra-editor-tag.tag.unapplied-tag input {\n  border: none;\n}\n\n.elyra-formEditor h3 {\n  flex-basis: 100%;\n  margin-bottom: 15px;\n  color: var(--jp-ui-font-color1);\n}\n\n.elyra-formEditor .elyra-form-code.jp-CodeMirrorEditor {\n  background-color: var(--jp-cell-editor-background);\n  border: var(--jp-border-width) solid var(--jp-input-border-color);\n  overflow-y: auto;\n  resize: vertical;\n  min-height: 150px;\n  height: 150px;\n  padding-bottom: 10px;\n  cursor: initial;\n  margin-top: 5px;\n}\n\n.elyra-formEditor .CodeMirror.cm-s-jupyter {\n  background-color: inherit;\n  height: 100%;\n}\n\n.elyra-formEditor .elyra-formEditor-code {\n  height: auto;\n  flex-basis: 100%;\n  display: flex;\n  flex-direction: column;\n}\n\n.elyra-formEditor-formInput {\n  margin: 10px;\n  flex-basis: 45%;\n}\n\n.elyra-formEditor .elyra-formEditor-saveButton {\n  flex-basis: 100%;\n  display: flex;\n  flex-direction: column;\n  padding-bottom: 15px;\n}\n\n.elyra-formEditor .form-group.field.elyra-formEditor-form-code,\n.elyra-formEditor .form-group.field.elyra-formEditor-form-tags {\n  width: 80%;\n}\n\n.elyra-formEditor .field-description {\n  display: none;\n}\n\n.elyra-formEditor .description-wrapper:hover .field-description {\n  color: var(--jp-content-font-color1);\n  position: absolute;\n  bottom: 110%;\n  left: 50%;\n  transform: translate(-50%, -10%);\n  background-color: var(--jp-border-color3);\n  border: 1px solid var(--jp-border-color2);\n  padding: 5px;\n  border-radius: 5px;\n  display: initial;\n  max-width: 22ch;\n  width: max-content;\n  word-wrap: break-word;\n  z-index: 1;\n}\n\n.elyra-formEditor select.form-control {\n  -moz-appearance: none !important;\n  -webkit-appearance: none;\n  background-image: url(\"data:image/svg+xml;utf8,<svg fill='black' height='24' viewBox='0 0 24 24' width='24' xmlns='http://www.w3.org/2000/svg'><path d='M7 10l5 5 5-5z'/><path d='M0 0h24v24H0z' fill='none'/></svg>\");\n  background-repeat: no-repeat;\n  background-position-x: calc(100% - 4px);\n  background-position-y: 50%;\n}\n\n.elyra-formEditor\n  .label-header\n  .description-wrapper\n  p.field-description.short-title {\n  transform: translate(-20%, -10%);\n}\n\n.elyra-formEditor .form-group.field-array .label-header {\n  margin-bottom: 10px;\n}\n\n.elyra-formEditor .description-wrapper {\n  width: fit-content;\n  position: relative;\n}\n\n.elyra-formEditor .description-button {\n  border-radius: 100%;\n  margin-left: 6px;\n  border: 1px solid var(--jp-border-color1);\n  background: none;\n  color: var(--jp-border-color0);\n  padding: 2px 5px;\n}\n\n.elyra-formEditor .label-header {\n  display: flex;\n  align-items: center;\n}\n\n.elyra-formEditor .array-item {\n  display: flex;\n  margin-bottom: 15px;\n}\n\n.elyra-formEditor .field-array button {\n  border-radius: 3px;\n  margin-top: 4px;\n}\n\n.elyra-formEditor .array-item .form-group.field {\n  padding-bottom: 0;\n  padding-right: 10px;\n}\n\n.elyra-formEditor .array-item .form-group.field input {\n  margin-top: 0;\n}\n\n.elyra-formEditor .jp-ArrayOperations {\n  display: flex;\n}\n\n.elyra-formEditor .jp-ArrayOperations button {\n  width: max-content;\n}\n\n.elyra-formEditor .field.field-array {\n  width: 100%;\n}\n"],"sourceRoot":""}]);
// Exports
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (___CSS_LOADER_EXPORT___);


/***/ }),

/***/ "../../node_modules/css-loader/dist/cjs.js!../ui-components/style/index.css":
/*!**********************************************************************************!*\
  !*** ../../node_modules/css-loader/dist/cjs.js!../ui-components/style/index.css ***!
  \**********************************************************************************/
/***/ ((module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../../../node_modules/css-loader/dist/runtime/cssWithMappingToString.js */ "../../node_modules/css-loader/dist/runtime/cssWithMappingToString.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../../../node_modules/css-loader/dist/runtime/api.js */ "../../node_modules/css-loader/dist/runtime/api.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _node_modules_css_loader_dist_cjs_js_formeditor_css__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! -!../../../node_modules/css-loader/dist/cjs.js!./formeditor.css */ "../../node_modules/css-loader/dist/cjs.js!../ui-components/style/formeditor.css");
/* harmony import */ var _node_modules_css_loader_dist_runtime_getUrl_js__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../../node_modules/css-loader/dist/runtime/getUrl.js */ "../../node_modules/css-loader/dist/runtime/getUrl.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_getUrl_js__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_getUrl_js__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _icons_r_logo_svg__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./icons/r-logo.svg */ "../ui-components/style/icons/r-logo.svg?24ea");
/* harmony import */ var _icons_r_logo_svg__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_icons_r_logo_svg__WEBPACK_IMPORTED_MODULE_4__);
// Imports





var ___CSS_LOADER_EXPORT___ = _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default()((_node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0___default()));
___CSS_LOADER_EXPORT___.i(_node_modules_css_loader_dist_cjs_js_formeditor_css__WEBPACK_IMPORTED_MODULE_2__["default"]);
var ___CSS_LOADER_URL_REPLACEMENT_0___ = _node_modules_css_loader_dist_runtime_getUrl_js__WEBPACK_IMPORTED_MODULE_3___default()((_icons_r_logo_svg__WEBPACK_IMPORTED_MODULE_4___default()));
// Module
___CSS_LOADER_EXPORT___.push([module.id, "/*\n * Copyright 2018-2022 Elyra Authors\n *\n * Licensed under the Apache License, Version 2.0 (the \"License\");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n * http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an \"AS IS\" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n */\n\n.elyra-expandableContainer-button,\n.elyra-expandableContainer-button.jp-mod-styled {\n  background-color: transparent;\n  vertical-align: middle;\n  padding: 0;\n  width: 20px;\n}\n\n.elyra-expandableContainer-button:hover {\n  cursor: pointer;\n}\n\n.elyra-expandableContainer-actionButton:hover {\n  background-color: var(--jp-layout-color1);\n}\n\n.elyra-expandableContainer-actionButton:active {\n  background-color: var(--jp-layout-color2);\n}\n\n.elyra-expandableContainer-title {\n  align-items: center;\n  display: flex;\n  flex-direction: row;\n  padding: 0px 4px;\n  height: 36px;\n}\n\n.elyra-expandableContainer-title:hover {\n  background: var(--jp-layout-color2);\n}\n\n.elyra-expandableContainer-name {\n  flex-grow: 1;\n  font-size: var(--jp-ui-font-size1);\n  white-space: nowrap;\n  overflow: hidden;\n  text-overflow: ellipsis;\n  padding: 4px 0 4px 2px;\n  line-height: 28px;\n}\n\n.elyra-expandableContainer-name:hover {\n  cursor: pointer;\n}\n\n.elyra-button {\n  background-repeat: no-repeat;\n  background-position: center;\n  border: none;\n  height: 100%;\n}\n\n.elyra-expandableContainer-details-visible {\n  overflow-x: auto;\n  overflow-y: auto;\n  display: block;\n  padding: 5px;\n  margin: 5px;\n  border: 1px solid var(--jp-border-color2);\n  border-radius: 2px;\n  color: var(--jp-ui-font-color1);\n  background-color: var(--jp-layout-color1);\n}\n\n.elyra-expandableContainer-details-visible textarea {\n  color: var(--jp-ui-font-color1);\n}\n\n.elyra-expandableContainer-details-hidden {\n  display: none;\n}\n\n.elyra-expandableContainer-action-buttons {\n  display: inline-flex;\n  align-self: flex-end;\n  height: 100%;\n}\n\n.elyra-errorDialog-messageDisplay pre {\n  min-height: 125px;\n  height: 100%;\n  width: 100%;\n  resize: none;\n  overflow-x: scroll;\n}\n\n.elyra-errorDialog-messageDisplay {\n  padding-bottom: 5px;\n  display: flex;\n  flex-direction: column;\n  height: 100%;\n  white-space: pre-line;\n}\n\n.elyra-errorDialog-messageDisplay > div:nth-child(2) {\n  margin: 15px 0;\n  display: flex;\n  flex: 1;\n  min-height: 0px;\n  flex-direction: column;\n}\n\n/* temporary fix until this is addressed in jupyterlab */\n.lm-TabBar-tabIcon svg {\n  height: auto;\n}\n\n.jp-Dialog-content {\n  resize: both;\n}\n\n.elyra-DialogDefaultButton.jp-mod-styled:hover:disabled,\n.elyra-DialogDefaultButton.jp-mod-styled:active:disabled,\n.elyra-DialogDefaultButton.jp-mod-styled:focus:disabled,\n.elyra-DialogDefaultButton.jp-mod-styled:disabled {\n  background-color: var(--jp-layout-color3);\n  opacity: 0.3;\n  pointer-events: none;\n}\n\n/* icons */\n\n[data-jp-theme-light='false'] .elyra-pieBrain-icon rect.st1,\n[data-jp-theme-light='false'] .elyra-pieBrain-icon rect.st2 {\n  fill: var(--jp-inverse-layout-color3);\n}\n\n.elyra-feedbackButton {\n  display: inline;\n  position: relative;\n}\n\n.elyra-feedbackButton[data-feedback]:not([data-feedback='']):before {\n  border: solid;\n  border-color: var(--jp-inverse-layout-color2) transparent;\n  border-width: 0 6px 6px 6px;\n  bottom: 0;\n  content: '';\n  left: 5px;\n  position: absolute;\n  z-index: 999;\n}\n\n.elyra-feedbackButton[data-feedback]:not([data-feedback='']):after {\n  background: var(--jp-inverse-layout-color2);\n  border-radius: 2px;\n  bottom: -20px;\n  color: var(--jp-ui-inverse-font-color1);\n  content: attr(data-feedback);\n  font-size: 0.75rem;\n  font-weight: 400;\n  padding: 3px 5px;\n  pointer-events: none;\n  position: absolute;\n  right: -10px;\n  text-align: center;\n  width: max-content;\n  word-wrap: break-word;\n  z-index: 999;\n}\n\n.elyra-browseFileDialog .jp-Dialog-content {\n  height: 400px;\n  width: 600px;\n}\n\n.elyra-expandableContainer-draggable:hover {\n  cursor: grab;\n}\n\n.rIcon {\n  content: url(" + ___CSS_LOADER_URL_REPLACEMENT_0___ + ");\n  height: 24px;\n  width: 14px;\n}\n", "",{"version":3,"sources":["webpack://./../ui-components/style/index.css"],"names":[],"mappings":"AAAA;;;;;;;;;;;;;;EAcE;;AAIF;;EAEE,6BAA6B;EAC7B,sBAAsB;EACtB,UAAU;EACV,WAAW;AACb;;AAEA;EACE,eAAe;AACjB;;AAEA;EACE,yCAAyC;AAC3C;;AAEA;EACE,yCAAyC;AAC3C;;AAEA;EACE,mBAAmB;EACnB,aAAa;EACb,mBAAmB;EACnB,gBAAgB;EAChB,YAAY;AACd;;AAEA;EACE,mCAAmC;AACrC;;AAEA;EACE,YAAY;EACZ,kCAAkC;EAClC,mBAAmB;EACnB,gBAAgB;EAChB,uBAAuB;EACvB,sBAAsB;EACtB,iBAAiB;AACnB;;AAEA;EACE,eAAe;AACjB;;AAEA;EACE,4BAA4B;EAC5B,2BAA2B;EAC3B,YAAY;EACZ,YAAY;AACd;;AAEA;EACE,gBAAgB;EAChB,gBAAgB;EAChB,cAAc;EACd,YAAY;EACZ,WAAW;EACX,yCAAyC;EACzC,kBAAkB;EAClB,+BAA+B;EAC/B,yCAAyC;AAC3C;;AAEA;EACE,+BAA+B;AACjC;;AAEA;EACE,aAAa;AACf;;AAEA;EACE,oBAAoB;EACpB,oBAAoB;EACpB,YAAY;AACd;;AAEA;EACE,iBAAiB;EACjB,YAAY;EACZ,WAAW;EACX,YAAY;EACZ,kBAAkB;AACpB;;AAEA;EACE,mBAAmB;EACnB,aAAa;EACb,sBAAsB;EACtB,YAAY;EACZ,qBAAqB;AACvB;;AAEA;EACE,cAAc;EACd,aAAa;EACb,OAAO;EACP,eAAe;EACf,sBAAsB;AACxB;;AAEA,wDAAwD;AACxD;EACE,YAAY;AACd;;AAEA;EACE,YAAY;AACd;;AAEA;;;;EAIE,yCAAyC;EACzC,YAAY;EACZ,oBAAoB;AACtB;;AAEA,UAAU;;AAEV;;EAEE,qCAAqC;AACvC;;AAEA;EACE,eAAe;EACf,kBAAkB;AACpB;;AAEA;EACE,aAAa;EACb,yDAAyD;EACzD,2BAA2B;EAC3B,SAAS;EACT,WAAW;EACX,SAAS;EACT,kBAAkB;EAClB,YAAY;AACd;;AAEA;EACE,2CAA2C;EAC3C,kBAAkB;EAClB,aAAa;EACb,uCAAuC;EACvC,4BAA4B;EAC5B,kBAAkB;EAClB,gBAAgB;EAChB,gBAAgB;EAChB,oBAAoB;EACpB,kBAAkB;EAClB,YAAY;EACZ,kBAAkB;EAClB,kBAAkB;EAClB,qBAAqB;EACrB,YAAY;AACd;;AAEA;EACE,aAAa;EACb,YAAY;AACd;;AAEA;EACE,YAAY;AACd;;AAEA;EACE,gDAAkC;EAClC,YAAY;EACZ,WAAW;AACb","sourcesContent":["/*\n * Copyright 2018-2022 Elyra Authors\n *\n * Licensed under the Apache License, Version 2.0 (the \"License\");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n * http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an \"AS IS\" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n */\n\n@import url('./formeditor.css');\n\n.elyra-expandableContainer-button,\n.elyra-expandableContainer-button.jp-mod-styled {\n  background-color: transparent;\n  vertical-align: middle;\n  padding: 0;\n  width: 20px;\n}\n\n.elyra-expandableContainer-button:hover {\n  cursor: pointer;\n}\n\n.elyra-expandableContainer-actionButton:hover {\n  background-color: var(--jp-layout-color1);\n}\n\n.elyra-expandableContainer-actionButton:active {\n  background-color: var(--jp-layout-color2);\n}\n\n.elyra-expandableContainer-title {\n  align-items: center;\n  display: flex;\n  flex-direction: row;\n  padding: 0px 4px;\n  height: 36px;\n}\n\n.elyra-expandableContainer-title:hover {\n  background: var(--jp-layout-color2);\n}\n\n.elyra-expandableContainer-name {\n  flex-grow: 1;\n  font-size: var(--jp-ui-font-size1);\n  white-space: nowrap;\n  overflow: hidden;\n  text-overflow: ellipsis;\n  padding: 4px 0 4px 2px;\n  line-height: 28px;\n}\n\n.elyra-expandableContainer-name:hover {\n  cursor: pointer;\n}\n\n.elyra-button {\n  background-repeat: no-repeat;\n  background-position: center;\n  border: none;\n  height: 100%;\n}\n\n.elyra-expandableContainer-details-visible {\n  overflow-x: auto;\n  overflow-y: auto;\n  display: block;\n  padding: 5px;\n  margin: 5px;\n  border: 1px solid var(--jp-border-color2);\n  border-radius: 2px;\n  color: var(--jp-ui-font-color1);\n  background-color: var(--jp-layout-color1);\n}\n\n.elyra-expandableContainer-details-visible textarea {\n  color: var(--jp-ui-font-color1);\n}\n\n.elyra-expandableContainer-details-hidden {\n  display: none;\n}\n\n.elyra-expandableContainer-action-buttons {\n  display: inline-flex;\n  align-self: flex-end;\n  height: 100%;\n}\n\n.elyra-errorDialog-messageDisplay pre {\n  min-height: 125px;\n  height: 100%;\n  width: 100%;\n  resize: none;\n  overflow-x: scroll;\n}\n\n.elyra-errorDialog-messageDisplay {\n  padding-bottom: 5px;\n  display: flex;\n  flex-direction: column;\n  height: 100%;\n  white-space: pre-line;\n}\n\n.elyra-errorDialog-messageDisplay > div:nth-child(2) {\n  margin: 15px 0;\n  display: flex;\n  flex: 1;\n  min-height: 0px;\n  flex-direction: column;\n}\n\n/* temporary fix until this is addressed in jupyterlab */\n.lm-TabBar-tabIcon svg {\n  height: auto;\n}\n\n.jp-Dialog-content {\n  resize: both;\n}\n\n.elyra-DialogDefaultButton.jp-mod-styled:hover:disabled,\n.elyra-DialogDefaultButton.jp-mod-styled:active:disabled,\n.elyra-DialogDefaultButton.jp-mod-styled:focus:disabled,\n.elyra-DialogDefaultButton.jp-mod-styled:disabled {\n  background-color: var(--jp-layout-color3);\n  opacity: 0.3;\n  pointer-events: none;\n}\n\n/* icons */\n\n[data-jp-theme-light='false'] .elyra-pieBrain-icon rect.st1,\n[data-jp-theme-light='false'] .elyra-pieBrain-icon rect.st2 {\n  fill: var(--jp-inverse-layout-color3);\n}\n\n.elyra-feedbackButton {\n  display: inline;\n  position: relative;\n}\n\n.elyra-feedbackButton[data-feedback]:not([data-feedback='']):before {\n  border: solid;\n  border-color: var(--jp-inverse-layout-color2) transparent;\n  border-width: 0 6px 6px 6px;\n  bottom: 0;\n  content: '';\n  left: 5px;\n  position: absolute;\n  z-index: 999;\n}\n\n.elyra-feedbackButton[data-feedback]:not([data-feedback='']):after {\n  background: var(--jp-inverse-layout-color2);\n  border-radius: 2px;\n  bottom: -20px;\n  color: var(--jp-ui-inverse-font-color1);\n  content: attr(data-feedback);\n  font-size: 0.75rem;\n  font-weight: 400;\n  padding: 3px 5px;\n  pointer-events: none;\n  position: absolute;\n  right: -10px;\n  text-align: center;\n  width: max-content;\n  word-wrap: break-word;\n  z-index: 999;\n}\n\n.elyra-browseFileDialog .jp-Dialog-content {\n  height: 400px;\n  width: 600px;\n}\n\n.elyra-expandableContainer-draggable:hover {\n  cursor: grab;\n}\n\n.rIcon {\n  content: url('./icons/r-logo.svg');\n  height: 24px;\n  width: 14px;\n}\n"],"sourceRoot":""}]);
// Exports
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (___CSS_LOADER_EXPORT___);


/***/ }),

/***/ "../ui-components/style/icons/clear-pipeline.svg":
/*!*******************************************************!*\
  !*** ../ui-components/style/icons/clear-pipeline.svg ***!
  \*******************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ("<svg focusable=\"false\" preserveAspectRatio=\"xMidYMid meet\" xmlns=\"http://www.w3.org/2000/svg\" fill=\"currentColor\" width=\"16\" height=\"16\" viewBox=\"0 0 32 32\" aria-hidden=\"true\">\n  <path d=\"M7 27H30V29H7zM27.38 10.51L19.45 2.59a2 2 0 00-2.83 0l-14 14a2 2 0 000 2.83L7.13 24h9.59L27.38 13.34A2 2 0 0027.38 10.51zM15.89 22H8L4 18l6.31-6.31 7.93 7.92zm3.76-3.76l-7.92-7.93L18 4 26 11.93z\"></path>\n</svg>\n");

/***/ }),

/***/ "../ui-components/style/icons/codait-piebrainlogo-jupyter-color.svg":
/*!**************************************************************************!*\
  !*** ../ui-components/style/icons/codait-piebrainlogo-jupyter-color.svg ***!
  \**************************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ("<?xml version=\"1.0\" encoding=\"utf-8\"?>\n<svg version=\"1.1\" xmlns=\"http://www.w3.org/2000/svg\" xmlns:xlink=\"http://www.w3.org/1999/xlink\" xml:space=\"preserve\"\n\tid=\"elyra-pie-brain-icon\" x=\"0px\" y=\"0px\" viewBox=\"0 0 243 225\">\n<style type=\"text/css\">\n\t.st0{clip-path:url(#SVGID_2_);}\n\t.st1{fill:#706E6F;stroke:#706E6F;stroke-width:1.9754;stroke-miterlimit:10;}\n\t.st2{fill:#706E6F;}\n\t.st3{fill:#f37726;}\n</style>\n<g class=\"elyra-pieBrain-icon\">\n\t<g>\n\t\t<defs>\n\t\t\t<path id=\"SVGID_1_\" d=\"M234,116.8c0,50.3-38.4,95.2-96,95.2l-0.3-95.2L203,48.1C221.7,65.4,234,89.8,234,116.8z\"/>\n\t\t</defs>\n\t\t<clipPath id=\"SVGID_2_\">\n\t\t\t<use xlink:href=\"#SVGID_1_\"  style=\"overflow:visible;\"/>\n\t\t</clipPath>\n\t\t<g class=\"st0\">\n\t\t\t<rect x=\"137.8\" y=\"222.6\" class=\"st1\" width=\"95.4\" height=\"7.2\"/>\n\t\t</g>\n\t\t<g class=\"st0\">\n\t\t\t<rect x=\"137.8\" y=\"242\" class=\"st1\" width=\"95.4\" height=\"7.2\"/>\n\t\t</g>\n\t\t<g class=\"st0\">\n\t\t\t<rect x=\"136.8\" y=\"163.7\" class=\"st2\" width=\"98.2\" height=\"9.2\"/>\n\t\t\t<rect x=\"136.8\" y=\"183\" class=\"st2\" width=\"98.2\" height=\"9.2\"/>\n\t\t\t<rect x=\"136.8\" y=\"202.3\" class=\"st2\" width=\"98.2\" height=\"9.2\"/>\n\t\t\t<rect x=\"136.6\" y=\"67\" class=\"st2\" width=\"98.4\" height=\"9.2\"/>\n\t\t\t<rect x=\"136.6\" y=\"47.7\" class=\"st2\" width=\"98.4\" height=\"9.2\"/>\n\t\t\t<rect x=\"136.6\" y=\"86.3\" class=\"st2\" width=\"98.4\" height=\"9.2\"/>\n\t\t\t<rect x=\"136.2\" y=\"144.3\" class=\"st2\" width=\"98.5\" height=\"9.2\"/>\n\t\t\t<rect x=\"136.8\" y=\"125\" class=\"st2\" width=\"98.1\" height=\"9.2\"/>\n\t\t\t<rect x=\"136.8\" y=\"105.7\" class=\"st2\" width=\"98\" height=\"9.2\"/>\n\t\t</g>\n\t</g>\n\t<g>\n\t\t<g>\n\t\t\t<path class=\"st3\" d=\"M107.1,13l-0.5-0.4c-1.8-1.5-3.8-2.3-5.7-2.5l-0.2,0C90.2,7,79.6,10.6,71,19.9c-2.6,2.8-4.7,6.1-6.2,9.9\n\t\t\t\tl-0.4,1l-1-0.3c-11.1-3.4-22.3-0.1-29.9,8c-8.6,9.1-11.5,23.3-7.5,36.1l0.3,0.9l-0.8,0.5C14.7,82.1,9.5,94.5,9.1,104.2\n\t\t\t\tc-0.9,19.6,7.6,28.5,16.1,34.6l0.7,0.5l-0.2,0.8c-3,9.9-2.1,20.5,2.5,29.1c7.7,14.2,23.3,20.4,38.1,15.2l1-0.4l0.4,1\n\t\t\t\tc0.9,2,2,3.8,3.3,5.3c8.2,9.7,19.9,13.3,31.4,9.7l0.2,0c1.5-0.2,2.9-0.7,4.2-1.7l0.2-0.1c3-2.3,5-6.5,5-10.5V22.4\n\t\t\t\tC111.9,19.2,110.1,15.6,107.1,13z M105.3,49.2L104,49c-2.6-0.4-6.5-1.5-10.1-4.7c-3.3-2.9-5.2-6.3-6.2-9l-6.3,2.1\n\t\t\t\tc1.3,3.5,3.8,8,8.1,11.8c5.3,4.6,10.9,6.1,14.7,6.5l1,0.1v41.4l-1.5-0.6c-4.5-1.6-9.1-2.4-13.6-2.4c-6.3,0-12.3,1.6-17.8,4.7\n\t\t\t\tc-3.4,1.9-6.4,4.3-9,7l-0.8,0.8l-0.8-0.8c-2.6-2.5-7.1-5.6-13.2-6.1c-0.6-0.1-1.2-0.1-1.9-0.1c-6.3,0-11.1,2.9-13.4,4.8l4.4,5\n\t\t\t\tc1.9-1.5,5.6-3.5,10.4-3.1c5,0.5,8.4,3.4,10,5.1l0.6,0.6l-0.4,0.7c-3.8,6.4-5.2,12.8-5.8,16.5l6.5,0.9\n\t\t\t\tc0.9-5.9,4.2-18.5,16.7-25.6c13-7.4,25.5-2.3,29.1-0.6l0.6,0.3v49.1l-1.3,0c-3.2,0-9.5,0.7-15.3,5.7c-5.3,4.6-7.5,10.4-8.4,14\n\t\t\t\tl6.5,1.3c0.7-2.5,2.3-6.9,6.2-10.3c4.2-3.7,8.7-4.1,11.1-4.1l1.1,0v27.4c0,1.9-1,3.7-1.8,4.7l-0.2,0.2l-0.2,0.1\n\t\t\t\tc-3.3,1.5-6.4,2.1-9.4,2.1c-7.5,0-13.8-4-17.7-8.7c-5.2-6.2-5.4-18-3.5-24.1c1.4-4.7,2.9-5.8,8.5-9.9l0.5-0.4\n\t\t\t\tc6.1-4.5,13.4-15.1,9.3-26.1l-6.1,2.7c2.6,7.8-3.6,15.5-7.1,18.2l-0.5,0.4c-2.1,1.6-4,2.9-5.5,4.3l-1.2,1.1l-0.7-1.4\n\t\t\t\tc-0.4-0.8-0.8-1.5-1.2-2.1c-2.2-3.5-6.1-6.1-8-7.2l-3.1,5.8c1.6,1,4.2,2.9,5.5,4.9c1,1.6,1.6,3.2,2.1,5c0.3,1,0.6,1.9,0.9,2.7\n\t\t\t\tL66,160l-0.1,0.4c-1.3,4.7-1.6,10.7-0.7,16.2l0.1,0.9l-0.9,0.3c-11.6,4.4-24.5-0.7-30.6-12c-6.9-12.7-3.4-29.9,7.7-38.9l-3.9-5.3\n\t\t\t\tc-3.4,2.7-6.3,6.1-8.6,10.1l-0.7,1.2l-1-0.8c-6.5-5.1-12.4-11.9-11.7-27.7c0.5-10.6,7.5-23,19.6-25.2l0.1,0l0.1,0\n\t\t\t\tc1.5,0.1,3,0,4.4-0.2l0.7-0.1l0.4,0.6c1.6,2.4,3.5,4.5,5.6,6.1c3.6,2.7,8,4.1,12.5,4.2L59,83.2c-2.3-0.1-5.3-0.7-8.3-2.9\n\t\t\t\tc-1.1-0.8-2.1-1.8-3-3l-0.7-0.9l0.9-0.7c2.9-2.4,4.7-5.9,5.4-10.3l-6.6-0.7c-0.6,3.9-2.7,8.3-10.9,7.9c-0.4,0-0.7,0-1.1,0\n\t\t\t\tc-0.4,0.1-0.9,0.1-1.3,0.2l-1,0.2l-0.3-1C29,61.6,31.4,50.2,38.2,43c6-6.4,15-8.8,23.3-6.2l1,0.3l-0.2,1\n\t\t\t\tc-1,5.6-0.7,11.4,0.7,16.7c3,11.3,10.3,17.8,14.2,20.5l3.6-5.5c-3.2-2.3-9-7.6-11.4-16.7c-2.7-10.3-0.2-21.6,6.4-28.8\n\t\t\t\tc4.8-5.2,14.6-12.9,26.9-6.4l0.3,0.2c0.5,0.5,2.3,2.3,2.3,4.1V49.2z\"/>\n\t\t</g>\n\t\t<g>\n\t\t\t<path class=\"st3\" d=\"M174.8,30.7c-14-13.4-32.4-20.7-51.8-20.7c-1.5,0-2.8,1.2-2.8,2.7L120,84.6c0,1.1,0.7,2.1,1.8,2.6\n\t\t\t\tc0.3,0.1,0.7,0.2,1,0.2c0.8,0,1.5-0.3,2-0.9l50-51.9C176,33.5,175.9,31.7,174.8,30.7z\"/>\n\t\t\t<g>\n\t\t\t\t<path class=\"st3\" d=\"M123.8,200.3c-1.9,0-3.5-1.5-3.5-3.5l-0.3-90.7c0-0.9,0.3-1.8,1-2.4l62.2-65.5c0.6-0.7,1.5-1.1,2.4-1.1\n\t\t\t\t\tc1,0,1.8,0.3,2.5,1c18.5,17.9,28.7,42.1,28.7,68C216.8,158.1,175.1,200.3,123.8,200.3z M127,107.6l0.3,85.7\n\t\t\t\t\tc45.9-1.8,82.6-40.2,82.6-87.1c0-22.8-8.5-44.2-24.1-60.5L127,107.6z\"/>\n\t\t\t</g>\n\t\t</g>\n\t</g>\n</g>\n</svg>\n");

/***/ }),

/***/ "../ui-components/style/icons/code-snippet.svg":
/*!*****************************************************!*\
  !*** ../ui-components/style/icons/code-snippet.svg ***!
  \*****************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ("<?xml version=\"1.0\" ?>\n<!DOCTYPE svg  PUBLIC '-//W3C//DTD SVG 1.1//EN'  'http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd'>\n<svg id=\"elyra-code-snippet-icon\" version=\"1.1\" viewBox=\"125 150 250 200\" width=\"32\" height=\"32\"  xml:space=\"preserve\" xmlns=\"http://www.w3.org/2000/svg\" xmlns:xlink=\"http://www.w3.org/1999/xlink\">\n    <g>\n        <g>\n            <polygon class=\"jp-icon3\" fill=\"#231F20\" points=\"195.568,185.811 142.681,250.173 195.568,314.534 208.077,293.962 172.44,250.173 208.077,206.384\"/>\n            <polygon class=\"jp-icon3\" fill=\"#231F20\" points=\"228.707,313 251.922,313 288.816,187 265.6,187\"/>\n            <polygon class=\"jp-icon3\" fill=\"#231F20\" points=\"303.876,185.81 291.37,206.384 327.005,250.173 291.37,293.961 303.876,314.535 356.765,250.173\"/>\n        </g>\n    </g>\n</svg>\n");

/***/ }),

/***/ "../ui-components/style/icons/container.svg":
/*!**************************************************!*\
  !*** ../ui-components/style/icons/container.svg ***!
  \**************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ("<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"32\" height=\"32\" viewBox=\"0 0 32 32\">\n    <path class=\"jp-icon3\" fill=\"#231F20\"  d=\"M28,12H20V4h8Zm-6-2h4V6H22Z\"/>\n    <path class=\"jp-icon3\" fill=\"#231F20\"  d=\"M17,15V9H9V23H23V15Zm-6-4h4v4H11Zm4,10H11V17h4Zm6,0H17V17h4Z\"/>\n    <path class=\"jp-icon3\" fill=\"#231F20\"  d=\"M26,28H6a2.0023,2.0023,0,0,1-2-2V6A2.0023,2.0023,0,0,1,6,4H16V6H6V26H26V16h2V26A2.0023,2.0023,0,0,1,26,28Z\"/>\n</svg>\n");

/***/ }),

/***/ "../ui-components/style/icons/dragdrop.svg":
/*!*************************************************!*\
  !*** ../ui-components/style/icons/dragdrop.svg ***!
  \*************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ("<svg xmlns=\"http://www.w3.org/2000/svg\" xmlns:xlink=\"http://www.w3.org/1999/xlink\" viewBox=\"0 0 213.69 200\">\n    <defs>\n        <style>\n            .cls-1{isolation:isolate;}.cls-2{fill:url(#linear-gradient);}.cls-3{fill:#909faf;}.cls-4{fill:#fff;}.cls-5{fill:#00b6cb;}.cls-6{fill:#5a6872;}.cls-7,.cls-8{fill:#dfe3e6;}.cls-7{mix-blend-mode:multiply;}\n        </style>\n        <linearGradient id=\"linear-gradient\" x1=\"100.01\" y1=\"198.49\" x2=\"100.01\" y2=\"-7.76\"\n                        gradientUnits=\"userSpaceOnUse\">\n            <stop offset=\"0\" stop-color=\"#fff\"/>\n            <stop offset=\"1\" stop-color=\"#909faf\"/>\n        </linearGradient>\n    </defs>\n    <title>Active-state_Drag-drop-file</title>\n    <g class=\"cls-1\">\n        <g id=\"Artwork\">\n            <circle class=\"cls-2\" cx=\"100.01\" cy=\"99.74\" r=\"100\"/>\n            <path class=\"cls-3\" d=\"M26.11,167.59a100,100,0,0,0,147.85,0Z\"/>\n            <circle class=\"cls-4\" cx=\"67.69\" cy=\"25.37\" r=\"2.5\"/>\n            <path class=\"cls-4\"\n                  d=\"M30.54,167.67V58.09A2.07,2.07,0,0,1,32.61,56H168.47a2.07,2.07,0,0,1,2.07,2.07V167.67Z\"/>\n            <path class=\"cls-5\"\n                  d=\"M121.55,113.66h-19v-19a2,2,0,0,0-4,0v19h-19a2,2,0,1,0,0,4h19v19a2,2,0,0,0,4,0v-19h19a2,2,0,0,0,0-4Z\"/>\n            <path class=\"cls-6\" d=\"M170.54,144.15a2,2,0,0,0,2-2v-10a2,2,0,0,0-4,0v10A2,2,0,0,0,170.54,144.15Z\"/>\n            <path class=\"cls-6\" d=\"M170.54,121.15a2,2,0,0,0,2-2v-10a2,2,0,0,0-4,0v10A2,2,0,0,0,170.54,121.15Z\"/>\n            <path class=\"cls-6\" d=\"M170.54,75.15a2,2,0,0,0,2-2v-10a2,2,0,0,0-4,0v10A2,2,0,0,0,170.54,75.15Z\"/>\n            <path class=\"cls-6\" d=\"M170.54,98.15a2,2,0,0,0,2-2v-10a2,2,0,0,0-4,0v10A2,2,0,0,0,170.54,98.15Z\"/>\n            <path class=\"cls-6\" d=\"M83,58H93a2,2,0,1,0,0-4H83a2,2,0,0,0,0,4Z\"/>\n            <path class=\"cls-6\" d=\"M106,58h10a2,2,0,1,0,0-4H106a2,2,0,0,0,0,4Z\"/>\n            <path class=\"cls-6\" d=\"M129,58h10a2,2,0,0,0,0-4H129a2,2,0,1,0,0,4Z\"/>\n            <path class=\"cls-6\" d=\"M152,58h10a2,2,0,0,0,0-4H152a2,2,0,0,0,0,4Z\"/>\n            <path class=\"cls-6\" d=\"M37,58H47a2,2,0,0,0,0-4H37a2,2,0,0,0,0,4Z\"/>\n            <path class=\"cls-6\" d=\"M72,56a2,2,0,0,0-2-2H60a2,2,0,0,0,0,4H70A2,2,0,0,0,72,56Z\"/>\n            <path class=\"cls-6\" d=\"M30.54,144.53a2,2,0,0,0,2-2v-10a2,2,0,0,0-4,0v10A2,2,0,0,0,30.54,144.53Z\"/>\n            <path class=\"cls-6\" d=\"M30.54,121.53a2,2,0,0,0,2-2v-10a2,2,0,0,0-4,0v10A2,2,0,0,0,30.54,121.53Z\"/>\n            <path class=\"cls-6\" d=\"M30.54,98.53a2,2,0,0,0,2-2v-10a2,2,0,0,0-4,0v10A2,2,0,0,0,30.54,98.53Z\"/>\n            <path class=\"cls-6\" d=\"M30.54,75.53a2,2,0,0,0,2-2v-10a2,2,0,0,0-4,0v10A2,2,0,0,0,30.54,75.53Z\"/>\n            <path class=\"cls-6\"\n                  d=\"M51,165.65H32.53s0-.07,0-.12v-10a2,2,0,0,0-4,0v10c0,.05,0,.08,0,.12H2a2,2,0,1,0,0,4H51a2,2,0,0,0,0-4Z\"/>\n            <path class=\"cls-6\" d=\"M198,165.65h-8.21a2,2,0,0,0,0,4H198a2,2,0,0,0,0-4Z\"/>\n            <path class=\"cls-6\"\n                  d=\"M178.73,165.65h-6.26a2,2,0,0,0,.07-.5v-10a2,2,0,0,0-4,0v10a2,2,0,0,0,.07.5H63.73a2,2,0,1,0,0,4h115a2,2,0,0,0,0-4Z\"/>\n            <path class=\"cls-6\"\n                  d=\"M100,3.74a96,96,0,1,1-96,96,96.11,96.11,0,0,1,96-96m0-4a100,100,0,1,0,100,100A100,100,0,0,0,100-.26Z\"/>\n            <path class=\"cls-7\"\n                  d=\"M112.49,54.07l26.13,64.7a6.5,6.5,0,0,0-3.27,7.08,6.39,6.39,0,0,0-2.74,3.36,6.53,6.53,0,0,0,1.71,6.95l2.54,2.53a4.07,4.07,0,0,0-.17,1.16v.44c0,.37,0,.75,0,1.12a10.89,10.89,0,0,0,10.83,10.71l4.7,0,5.25,0a12.11,12.11,0,0,0,8.32-3.22c1.92-1.79,3.42-3.29,4.73-4.73a14.68,14.68,0,0,0,.68-18.9L120.48,56H117.9c-.08-2.33-2.63-2-2.63-2Z\"/>\n            <path class=\"cls-4\"\n                  d=\"M209.74,105.7l-57.35,23.06a3.1,3.1,0,0,1-4-1.72L120.82,58.57a3.11,3.11,0,0,1,1.72-4L166,37.05,189.51,47.1l21.94,54.57A3.1,3.1,0,0,1,209.74,105.7Z\"/>\n            <path class=\"cls-8\"\n                  d=\"M166.89,39.17l5,12.53A2.26,2.26,0,0,0,174.86,53l12.52-5a2.21,2.21,0,0,0,1.23-1.21l-21.7-9.25A2.23,2.23,0,0,0,166.89,39.17Z\"/>\n            <path class=\"cls-6\"\n                  d=\"M213.31,100.93,191.36,46.36a2,2,0,0,0-1.07-1.1l-.77-.33-.12-.07-7.51-3.2-15.07-6.45a2,2,0,0,0-1.53,0L121.8,52.68A5.1,5.1,0,0,0,119,59.31l27.54,68.48a5.1,5.1,0,0,0,4.73,3.2,5.26,5.26,0,0,0,1.9-.37l57.34-23.07a5.08,5.08,0,0,0,2.83-6.62ZM180.25,45.31l4,1.71-10.12,4.07a.25.25,0,0,1-.19,0,.27.27,0,0,1-.14-.14l-4.07-10.13Zm29.34,58a1.1,1.1,0,0,1-.6.58l-57.34,23.07a1.1,1.1,0,0,1-1.43-.61L122.68,57.82a1.07,1.07,0,0,1,0-.84,1.09,1.09,0,0,1,.6-.59L165,39.64c0,.09.05.19.09.28l5,12.52a4.25,4.25,0,0,0,4,2.67,4.16,4.16,0,0,0,1.58-.31l12.53-5c.08,0,.16-.08.24-.12l21.23,52.78A1.11,1.11,0,0,1,209.59,103.26Z\"/>\n            <path class=\"cls-6\"\n                  d=\"M163.19,61.91a2,2,0,0,0-2.6-1.11l-20.51,8.25A2,2,0,0,0,139,71.66a2,2,0,0,0,1.85,1.25,2.17,2.17,0,0,0,.75-.14l20.51-8.25A2,2,0,0,0,163.19,61.91Z\"/>\n            <path class=\"cls-6\"\n                  d=\"M160.93,78a2,2,0,0,0-2.6-1.11l-13,5.22a2,2,0,0,0,.75,3.86,1.92,1.92,0,0,0,.74-.15l13-5.22A2,2,0,0,0,160.93,78Z\"/>\n            <path class=\"cls-6\"\n                  d=\"M164.62,87.21A2,2,0,0,0,162,86.1l-13,5.22a2,2,0,1,0,1.5,3.71l13-5.22A2,2,0,0,0,164.62,87.21Z\"/>\n            <path class=\"cls-6\"\n                  d=\"M168.35,96.47a2,2,0,0,0-2.6-1.11l-13,5.22a2,2,0,0,0-1.11,2.61,2,2,0,0,0,2.6,1.1l13-5.22A2,2,0,0,0,168.35,96.47Z\"/>\n            <path class=\"cls-6\" d=\"M169.47,104.62l-13,5.23a2,2,0,0,0,1.5,3.71l13-5.23a2,2,0,0,0-1.49-3.71Z\"/>\n            <path class=\"cls-6\"\n                  d=\"M168.34,77.05a2,2,0,0,0,.75-.15l13-5.22a2,2,0,0,0-1.5-3.71l-13,5.22a2,2,0,0,0,.75,3.86Z\"/>\n            <path class=\"cls-6\"\n                  d=\"M186.88,78.26a2,2,0,0,0-2.6-1.11l-13,5.22a2,2,0,1,0,1.49,3.71l13-5.22A2,2,0,0,0,186.88,78.26Z\"/>\n            <path class=\"cls-6\"\n                  d=\"M190.6,87.52a2,2,0,0,0-2.6-1.11l-13,5.22a2,2,0,0,0,.75,3.86,1.92,1.92,0,0,0,.74-.15l13-5.22A2,2,0,0,0,190.6,87.52Z\"/>\n            <path class=\"cls-6\" d=\"M191.73,95.67l-13,5.23a2,2,0,0,0,1.49,3.71l13-5.23a2,2,0,1,0-1.49-3.71Z\"/>\n            <path class=\"cls-4\"\n                  d=\"M155.23,147l-4.69,0a8.9,8.9,0,0,1-8.85-8.75v-1.52a2,2,0,0,1,.67-1.49c-1.21-1.21-2.42-2.41-3.62-3.62a4.51,4.51,0,0,1-1.23-4.87,4.43,4.43,0,0,1,3.46-2.9,4.45,4.45,0,0,1-.75-2.79,4.32,4.32,0,0,1,2.6-3.78,4.47,4.47,0,0,1,1.9-.44,4.23,4.23,0,0,1,1.93.47,4.59,4.59,0,0,1,.1-.51,4.49,4.49,0,0,1,2.9-3.16,4.29,4.29,0,0,1,4.45.91,4.46,4.46,0,0,1,4.4-3.6,4.61,4.61,0,0,1,2.77.92c.13.11.27.22.39.34,1.05,1.06,2.1,2.1,3.16,3.14,2.38,2.36,4.85,4.8,7.19,7.3a12.65,12.65,0,0,1,0,17.06c-1.27,1.39-2.73,2.86-4.61,4.61a10.16,10.16,0,0,1-7,2.68Z\"/>\n            <path class=\"cls-6\"\n                  d=\"M158.5,113a2.57,2.57,0,0,1,1.55.51l.2.17c3.44,3.45,7,6.83,10.3,10.39a10.71,10.71,0,0,1,0,14.34c-1.42,1.57-2.95,3-4.49,4.5a8.12,8.12,0,0,1-5.63,2.14l-5.23,0-4.65,0a6.89,6.89,0,0,1-6.87-6.8c0-.49,0-1,0-1.47l.16-.12c.65.67,1.29,1.35,2,2a1.3,1.3,0,0,0,.89.45,1,1,0,0,0,.68-.31c.42-.43.36-1-.19-1.52q-3.51-3.53-7-7a2.54,2.54,0,0,1-.75-2.8,2.44,2.44,0,0,1,2.33-1.63,2.5,2.5,0,0,1,1.68.65c.86.77,1.62,1.65,2.49,2.41a1.37,1.37,0,0,0,.86.29.78.78,0,0,0,.22,0,1,1,0,0,0,.61-.77,1.52,1.52,0,0,0-.44-1c-1.34-1.38-2.72-2.73-4.09-4.08a2.56,2.56,0,0,1-.84-2.07,2.34,2.34,0,0,1,1.44-2.1,2.48,2.48,0,0,1,1.06-.25,2.37,2.37,0,0,1,1.48.54,18,18,0,0,1,1.49,1.41c1,1,2,2,3,3a1.29,1.29,0,0,0,.9.43.9.9,0,0,0,.68-.31c.4-.41.33-1-.2-1.52-.92-.93-1.87-1.83-2.76-2.78a2.49,2.49,0,0,1,1-4.13,2.52,2.52,0,0,1,.83-.15,2.54,2.54,0,0,1,1.76.8c.92.89,1.81,1.81,2.72,2.72a1.41,1.41,0,0,0,.94.46.86.86,0,0,0,.64-.28c.44-.45.38-1-.16-1.58a5.45,5.45,0,0,1-.66-.78,2.44,2.44,0,0,1,.46-3.15,2.49,2.49,0,0,1,1.65-.61m0-4a6.48,6.48,0,0,0-4.32,1.63,6.64,6.64,0,0,0-1,1.13,6.31,6.31,0,0,0-2-.34,6.51,6.51,0,0,0-2.16.38,6.61,6.61,0,0,0-3.64,3.12c-.2,0-.42,0-.63,0a6.56,6.56,0,0,0-2.75.62,6.35,6.35,0,0,0-3.75,5.48,7.1,7.1,0,0,0,.13,1.79,6.35,6.35,0,0,0-2.73,3.37,6.49,6.49,0,0,0,1.71,6.94l2.53,2.53a4.07,4.07,0,0,0-.17,1.16v1.56A10.9,10.9,0,0,0,150.52,149l4.69,0,5.27,0a12.09,12.09,0,0,0,8.31-3.22c1.93-1.79,3.43-3.29,4.73-4.73a14.67,14.67,0,0,0-.05-19.77c-2.37-2.53-4.85-5-7.25-7.35q-1.58-1.56-3.14-3.13c-.23-.22-.44-.39-.59-.51a6.57,6.57,0,0,0-4-1.34Z\"/>\n            <path class=\"cls-4\"\n                  d=\"M109.55,35.67a3.26,3.26,0,0,1-3.25-3.25.75.75,0,0,0-1.5,0,3.26,3.26,0,0,1-3.25,3.25.75.75,0,0,0,0,1.5,3.25,3.25,0,0,1,3.25,3.25.75.75,0,0,0,1.5,0,3.25,3.25,0,0,1,3.25-3.25.75.75,0,0,0,0-1.5Z\"/>\n            <path class=\"cls-4\"\n                  d=\"M19.15,102.94a1.75,1.75,0,0,1-1.75-1.75.75.75,0,0,0-1.5,0,1.76,1.76,0,0,1-1.75,1.75.75.75,0,0,0,0,1.5,1.75,1.75,0,0,1,1.75,1.75.75.75,0,0,0,1.5,0,1.75,1.75,0,0,1,1.75-1.75.75.75,0,1,0,0-1.5Z\"/>\n        </g>\n    </g>\n</svg>\n");

/***/ }),

/***/ "../ui-components/style/icons/error.svg":
/*!**********************************************!*\
  !*** ../ui-components/style/icons/error.svg ***!
  \**********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ("<svg focusable=\"false\" preserveAspectRatio=\"xMidYMid meet\" xmlns=\"http://www.w3.org/2000/svg\" fill=\"#d32f2f\" width=\"32\" height=\"32\" viewBox=\"0 0 32 32\" aria-hidden=\"true\">\n  <circle cx=\"16\" cy=\"16\" r=\"10\"></circle>\n  <title>Error</title>\n</svg>\n");

/***/ }),

/***/ "../ui-components/style/icons/export-pipeline.svg":
/*!********************************************************!*\
  !*** ../ui-components/style/icons/export-pipeline.svg ***!
  \********************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ("<svg fill=\"currentColor\" focusable=\"false\" preserveAspectRatio=\"xMidYMid meet\" xmlns=\"http://www.w3.org/2000/svg\" width=\"16\" height=\"16\" viewBox=\"0 0 32 32\" aria-hidden=\"true\">\n\t<path d=\"M13 21L26.17 21 23.59 23.59 25 25 30 20 25 15 23.59 16.41 26.17 19 13 19 13 21z\"></path>\n\t<path d=\"M22,14V10a1,1,0,0,0-.29-.71l-7-7A1,1,0,0,0,14,2H4A2,2,0,0,0,2,4V28a2,2,0,0,0,2,2H20a2,2,0,0,0,2-2V26H20v2H4V4h8v6a2,2,0,0,0,2,2h6v2Zm-8-4V4.41L19.59,10Z\"></path>\n</svg>\n");

/***/ }),

/***/ "../ui-components/style/icons/help.svg":
/*!*********************************************!*\
  !*** ../ui-components/style/icons/help.svg ***!
  \*********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ("<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"32\" height=\"32\" viewBox=\"0 0 32 32\">\n  <polygon class=\"jp-icon3 jp-icon-selectable\" fill=\"#000000\" points=\"17 22 17 14 13 14 13 16 15 16 15 22 12 22 12 24 20 24 20 22 17 22\"/>\n  <path class=\"jp-icon3 jp-icon-selectable\" fill=\"#000000\" d=\"M16,8a1.5,1.5,0,1,0,1.5,1.5A1.5,1.5,0,0,0,16,8Z\"/>\n  <path class=\"jp-icon3 jp-icon-selectable\" fill=\"#000000\" d=\"M26,28H6a2.0023,2.0023,0,0,1-2-2V6A2.0023,2.0023,0,0,1,6,4H26a2.0023,2.0023,0,0,1,2,2V26A2.0023,2.0023,0,0,1,26,28ZM6,6V26H26V6Z\"/>\n</svg>\n");

/***/ }),

/***/ "../ui-components/style/icons/import.svg":
/*!***********************************************!*\
  !*** ../ui-components/style/icons/import.svg ***!
  \***********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ("<svg id=\"Layer_1\" data-name=\"Layer 1\" xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 32 32\">\n\t<title>Insert</title>\n\t<g class=\"jp-icon3\" fill=\"#616161\">\n\t\t<path d=\"M4,22v8H6V22h8.17l-2.58,2.59L13,26l5-5-5-5-1.41,1.41L14.17,20H6A2,2,0,0,0,4,22Z\"/>\n\t\t<path d=\"M26,2H10A2,2,0,0,0,8,4v8h2V4H26V28H18v2h8a2,2,0,0,0,2-2V4A2,2,0,0,0,26,2Z\"/>\n\t</g>\n</svg>\n");

/***/ }),

/***/ "../ui-components/style/icons/pipeline-components.svg":
/*!************************************************************!*\
  !*** ../ui-components/style/icons/pipeline-components.svg ***!
  \************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ("<svg id=\"icon\" fill=\"currentColor\" xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 32 32\">\n    <defs>\n        <style>.cls-1{fill:none;}</style>\n    </defs>\n    <title>Component Catalogs</title>\n    <path d=\"M26,14a2,2,0,0,0,2-2V6a2,2,0,0,0-2-2H20a2,2,0,0,0-2,2v6a2,2,0,0,0,2,2h2v4.1A5,5,0,0,0,18.1,22H14V20a2,2,0,0,0-2-2H10V13.9a5,5,0,1,0-2,0V18H6a2,2,0,0,0-2,2v6a2,2,0,0,0,2,2h6a2,2,0,0,0,2-2V24h4.1A5,5,0,1,0,24,18.1V14ZM6,9a3,3,0,1,1,3,3A3,3,0,0,1,6,9Zm6,17H6V20h6Zm14-3a3,3,0,1,1-3-3A3,3,0,0,1,26,23ZM20,6h6v6H20Z\" transform=\"translate(0 0)\"/>\n    <rect id=\"_Transparent_Rectangle_\" data-name=\"&lt;Transparent Rectangle&gt;\" class=\"cls-1\" width=\"32\" height=\"32\"/>\n</svg>\n");

/***/ }),

/***/ "../ui-components/style/icons/pipeline-flow.svg":
/*!******************************************************!*\
  !*** ../ui-components/style/icons/pipeline-flow.svg ***!
  \******************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<svg version=\"1.1\" xmlns=\"http://www.w3.org/2000/svg\" xmlns:xlink=\"http://www.w3.org/1999/xlink\"\n  id=\"elyra-pipeline-editor-icon\" width=\"32px\" height=\"32px\" viewBox=\"0 0 32 32\" title=\"Elyra Pipeline Editor\">\n  <g stroke=\"none\" stroke-width=\"1\" fill=\"none\" fill-rule=\"evenodd\">\n    <path class=\"jp-icon3 jp-icon-selectable\" fill=\"#000000\" d=\"M20,23 L11.86,23 C11.7609757,22.6493104 11.616411,22.3131134 11.43,22 L22,11.43 C22.6019656,11.7993928 23.293741,11.9965488 24,12 C26.0803346,12.0067496 27.8185594,10.4177446 27.9980602,8.34515757 C28.177561,6.27257049 26.7384074,4.4083819 24.6878883,4.05737018 C22.6373692,3.70635845 20.6600973,4.98571688 20.14,7 L11.86,7 C11.356433,5.04969328 9.48121328,3.77807479 7.48299948,4.03188121 C5.48478569,4.28568764 3.98701665,5.98573188 3.98701665,8 C3.98701665,10.0142681 5.48478569,11.7143124 7.48299948,11.9681188 C9.48121328,12.2219252 11.356433,10.9503067 11.86,9 L20.14,9 C20.2390243,9.35068963 20.383589,9.68688662 20.57,10 L10,20.57 C9.39803439,20.2006072 8.70625898,20.0034512 8,20 C5.91966537,19.9932504 4.18144061,21.5822554 4.00193981,23.6548424 C3.822439,25.7274295 5.26159259,27.5916181 7.31211167,27.9426298 C9.36263076,28.2936415 11.3399027,27.0142831 11.86,25 L20,25 L20,28 L28,28 L28,20 L20,20 L20,23 Z M8,10 C6.8954305,10 6,9.1045695 6,8 C6,6.8954305 6.8954305,6 8,6 C9.1045695,6 10,6.8954305 10,8 C10,8.53043298 9.78928632,9.03914081 9.41421356,9.41421356 C9.03914081,9.78928632 8.53043298,10 8,10 Z M24,6 C25.1045695,6 26,6.8954305 26,8 C26,9.1045695 25.1045695,10 24,10 C22.8954305,10 22,9.1045695 22,8 C22,6.8954305 22.8954305,6 24,6 Z M8,26 C6.8954305,26 6,25.1045695 6,24 C6,22.8954305 6.8954305,22 8,22 C9.1045695,22 10,22.8954305 10,24 C10,25.1045695 9.1045695,26 8,26 Z M22,22 L26,22 L26,26 L22,26 L22,22 Z\"></path>\n  </g>\n</svg>");

/***/ }),

/***/ "../ui-components/style/icons/py-logo.svg":
/*!************************************************!*\
  !*** ../ui-components/style/icons/py-logo.svg ***!
  \************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ("<svg width=\"32\" height=\"32\" viewBox=\"0 0 238 237\" xmlns=\"http://www.w3.org/2000/svg\" xmlns:xlink=\"http://www.w3.org/1999/xlink\" overflow=\"hidden\">\n    <g transform=\"translate(-706 314)\">\n        <path class=\"jp-icon-selectable\" d=\"M792.441-295.763C786.496-295.763 781.697-290.979 781.697-285.062 781.697-279.166 786.496-274.382 792.441-274.382 798.365-274.382 803.184-279.166 803.184-285.062 803.184-290.979 798.365-295.763 792.441-295.763ZM823.472-312.998C833.277-313.043 843.484-312.329 853.336-310.724 868.899-308.185 882-296.728 882-281.516L882-228.072C882-212.398 869.282-199.557 853.336-199.557L796.03-199.557C776.58-199.557 760.189-183.169 760.189-164.641L760.189-139 740.485-139C723.817-139 714.114-150.877 710.037-167.494 704.538-189.82 704.772-203.124 710.037-224.505 714.602-243.159 729.189-253 745.857-253L767.365-253 824.693-253 824.693-260.134 767.365-260.134 767.365-281.516C767.365-297.715 771.76-306.527 796.03-310.724 804.268-312.151 813.668-312.953 823.472-312.998Z\" fill=\"#366A96\" fill-rule=\"evenodd\"/>\n        <path class=\"jp-icon-selectable\" d=\"M857.377-117.071C851.466-117.071 846.655-112.267 846.655-106.348 846.655-100.406 851.466-95.6026 857.377-95.6026 863.31-95.6026 868.099-100.406 868.099-106.348 868.099-112.267 863.31-117.071 857.377-117.071ZM889.563-253 911.007-253C927.662-253 935.502-240.696 939.614-224.39 945.334-201.743 945.589-184.804 939.614-167.148 933.828-150 927.642-138.539 911.007-138.539L882.402-138.539 825.211-138.539 825.211-131.375 882.402-131.375 882.402-109.908C882.402-93.6435 868.205-85.4055 853.796-81.2973 832.12-75.1034 814.722-76.0513 796.606-81.2973 781.476-85.6801 768-94.6332 768-109.908L768-163.568C768-179.01 780.947-192.199 796.606-192.199L853.796-192.199C872.846-192.199 889.563-208.568 889.563-227.971Z\" fill=\"#FFC836\" fill-rule=\"evenodd\"/>\n    </g>\n</svg>\n");

/***/ }),

/***/ "../ui-components/style/icons/r-logo.svg?5796":
/*!***********************************************!*\
  !*** ../ui-components/style/icons/r-logo.svg ***!
  \***********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ("<svg xmlns=\"http://www.w3.org/2000/svg\" xmlns:xlink=\"http://www.w3.org/1999/xlink\" preserveAspectRatio=\"xMidYMid\" width=\"32\" height=\"32\" viewBox=\"0 0 724 561\">\n  <path class=\"jp-icon-selectable\" d=\"M361.453,485.937 C162.329,485.937 0.906,377.828 0.906,244.469 C0.906,111.109 162.329,3.000 361.453,3.000 C560.578,3.000 722.000,111.109 722.000,244.469 C722.000,377.828 560.578,485.937 361.453,485.937 ZM416.641,97.406 C265.289,97.406 142.594,171.314 142.594,262.484 C142.594,353.654 265.289,427.562 416.641,427.562 C567.992,427.562 679.687,377.033 679.687,262.484 C679.687,147.971 567.992,97.406 416.641,97.406 Z\" fill=\"rgb(179,179,179)\" fill-rule=\"evenodd\"/>\n  <path class=\"jp-icon-selectable\" d=\"M550.000,377.000 C550.000,377.000 571.822,383.585 584.500,390.000 C588.899,392.226 596.510,396.668 602.000,402.500 C607.378,408.212 610.000,414.000 610.000,414.000 L696.000,559.000 L557.000,559.062 L492.000,437.000 C492.000,437.000 478.690,414.131 470.500,407.500 C463.668,401.969 460.755,400.000 454.000,400.000 C449.298,400.000 420.974,400.000 420.974,400.000 L421.000,558.974 L298.000,559.026 L298.000,152.938 L545.000,152.938 C545.000,152.938 657.500,154.967 657.500,262.000 C657.500,369.033 550.000,377.000 550.000,377.000 ZM496.500,241.024 L422.037,240.976 L422.000,310.026 L496.500,310.002 C496.500,310.002 531.000,309.895 531.000,274.877 C531.000,239.155 496.500,241.024 496.500,241.024 Z\" fill=\"rgb(52,101,176)\" fill-rule=\"evenodd\"/>\n</svg>\n");

/***/ }),

/***/ "../ui-components/style/icons/runtimes.svg":
/*!*************************************************!*\
  !*** ../ui-components/style/icons/runtimes.svg ***!
  \*************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ("<svg xmlns=\"http://www.w3.org/2000/svg\" fill=\"currentColor\" width=\"32\" height=\"32\" viewBox=\"0 0 32 32\">\n    <g>\n        <rect class=\"jp-icon3\" x=\"20\" y=\"20\" width=\"10\" height=\"2\"/>\n        <rect class=\"jp-icon3\" x=\"20\" y=\"24\" width=\"10\" height=\"2\"/>\n        <rect class=\"jp-icon3\" x=\"20\" y=\"28\" width=\"10\" height=\"2\"/>\n        <path class=\"jp-icon3\" d=\"M16,20a3.9123,3.9123,0,0,1-4-4,3.9123,3.9123,0,0,1,4-4,3.9123,3.9123,0,0,1,4,4h2a6,6,0,1,0-6,6Z\"/>\n        <path class=\"jp-icon3\" d=\"M29.3047,11.0439,26.9441,6.9561a1.9977,1.9977,0,0,0-2.3728-.8946l-2.4341.8233a11.0419,11.0419,0,0,0-1.312-.7583l-.5037-2.5186A2,2,0,0,0,18.36,2H13.64a2,2,0,0,0-1.9611,1.6079l-.5037,2.5186A10.9666,10.9666,0,0,0,9.8481,6.88L7.4287,6.0615a1.9977,1.9977,0,0,0-2.3728.8946L2.6953,11.0439a2.0006,2.0006,0,0,0,.4119,2.5025l1.9309,1.6968C5.021,15.4946,5,15.7446,5,16c0,.2578.01.5127.0278.7656l-1.9206,1.688a2.0006,2.0006,0,0,0-.4119,2.5025l2.3606,4.0878a1.9977,1.9977,0,0,0,2.3728.8946l2.4341-.8233a10.9736,10.9736,0,0,0,1.312.7583l.5037,2.5186A2,2,0,0,0,13.64,30H16V28H13.64l-.71-3.5508a9.0953,9.0953,0,0,1-2.6948-1.5713l-3.4468,1.166-2.36-4.0878L7.1528,17.561a8.9263,8.9263,0,0,1-.007-3.1279L4.4275,12.0439,6.7886,7.9561l3.4267,1.1591a9.0305,9.0305,0,0,1,2.7141-1.5644L13.64,4H18.36l.71,3.5508a9.0978,9.0978,0,0,1,2.6948,1.5713l3.4468-1.166,2.36,4.0878-2.7978,2.4522L26.0923,16l2.8-2.4536A2.0006,2.0006,0,0,0,29.3047,11.0439Z\"/>\n    </g>\n</svg>\n");

/***/ }),

/***/ "../ui-components/style/icons/save-pipeline.svg":
/*!******************************************************!*\
  !*** ../ui-components/style/icons/save-pipeline.svg ***!
  \******************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ("<svg focusable=\"false\" preserveAspectRatio=\"xMidYMid meet\" fill=\"currentColor\" xmlns=\"http://www.w3.org/2000/svg\" width=\"16\" height=\"16\" viewBox=\"0 0 32 32\" aria-hidden=\"true\">\n  <path d=\"M27.71,9.29l-5-5A1,1,0,0,0,22,4H6A2,2,0,0,0,4,6V26a2,2,0,0,0,2,2H26a2,2,0,0,0,2-2V10A1,1,0,0,0,27.71,9.29ZM12,6h8v4H12Zm8,20H12V18h8Zm2,0V18a2,2,0,0,0-2-2H12a2,2,0,0,0-2,2v8H6V6h4v4a2,2,0,0,0,2,2h8a2,2,0,0,0,2-2V6.41l4,4V26Z\"></path>\n</svg>");

/***/ }),

/***/ "../ui-components/style/icons/tag.svg":
/*!********************************************!*\
  !*** ../ui-components/style/icons/tag.svg ***!
  \********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ("<svg width=\"28\" height=\"28\" viewBox=\"0 0 43 28\" xmlns=\"http://www.w3.org/2000/svg\">\n\t<g class=\"jp-icon3\" fill=\"#616161\">\n\t\t<path d=\"M28.8332 12.334L32.9998 16.5007L37.1665 12.334H28.8332Z\"/>\n\t\t<path d=\"M16.2095 21.6104C15.6873 22.1299 14.8443 22.1299 14.3248 21.6104L6.9829 14.7245C6.5724 14.3394 6.08313 13.6098 6.04786 13.0482C5.95347 11.5288 6.02002 8.61944 6.06621 7.07695C6.08281 6.51477 6.55548 6.04347 7.11804 6.03055C9.08863 5.98473 13.2638 5.93579 13.6518 6.32425L21.7369 13.639C22.256 14.1585 21.7851 15.4724 21.262 15.9946L16.2095 21.6104ZM9.77585 8.265C9.33551 7.82566 8.62351 7.82566 8.1828 8.265C7.74346 8.70571 7.74346 9.41733 8.1828 9.85667C8.62382 10.2964 9.33582 10.2964 9.77585 9.85667C10.2156 9.41733 10.2156 8.70533 9.77585 8.265Z\"/>\n\t</g>\n</svg>\n");

/***/ }),

/***/ "../ui-components/style/icons/trashIcon.svg":
/*!**************************************************!*\
  !*** ../ui-components/style/icons/trashIcon.svg ***!
  \**************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ("<svg focusable=\"false\" preserveAspectRatio=\"xMidYMid meet\" xmlns=\"http://www.w3.org/2000/svg\" width=\"16\" height=\"16\" viewBox=\"0 0 32 32\">\n\t<title>Delete item</title>\n\t<g class=\"jp-icon3\" fill=\"#616161\">\n\t\t<path d=\"M12 12H14V24H12zM18 12H20V24H18z\"></path>\n\t\t<path d=\"M4 6V8H6V28a2 2 0 002 2H24a2 2 0 002-2V8h2V6zM8 28V8H24V28zM12 2H20V4H12z\"></path>\n\t</g>\n</svg>\n");

/***/ }),

/***/ "../ui-components/style/icons/view--off.svg":
/*!**************************************************!*\
  !*** ../ui-components/style/icons/view--off.svg ***!
  \**************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ("<svg id=\"icon\" fill=\"currentColor\" xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 32 32\"><defs><style>.cls-1{fill:none;}</style></defs><title>view--off</title><path d=\"M5.24,22.51l1.43-1.42A14.06,14.06,0,0,1,3.07,16C5.1,10.93,10.7,7,16,7a12.38,12.38,0,0,1,4,.72l1.55-1.56A14.72,14.72,0,0,0,16,5,16.69,16.69,0,0,0,1.06,15.66a1,1,0,0,0,0,.68A16,16,0,0,0,5.24,22.51Z\"/><path d=\"M12,15.73a4,4,0,0,1,3.7-3.7l1.81-1.82a6,6,0,0,0-7.33,7.33Z\"/><path d=\"M30.94,15.66A16.4,16.4,0,0,0,25.2,8.22L30,3.41,28.59,2,2,28.59,3.41,30l5.1-5.1A15.29,15.29,0,0,0,16,27,16.69,16.69,0,0,0,30.94,16.34,1,1,0,0,0,30.94,15.66ZM20,16a4,4,0,0,1-6,3.44L19.44,14A4,4,0,0,1,20,16Zm-4,9a13.05,13.05,0,0,1-6-1.58l2.54-2.54a6,6,0,0,0,8.35-8.35l2.87-2.87A14.54,14.54,0,0,1,28.93,16C26.9,21.07,21.3,25,16,25Z\"/><rect id=\"_Transparent_Rectangle_\" data-name=\"&lt;Transparent Rectangle&gt;\" class=\"cls-1\" width=\"32\" height=\"32\"/></svg>");

/***/ }),

/***/ "../ui-components/style/icons/view.svg":
/*!*********************************************!*\
  !*** ../ui-components/style/icons/view.svg ***!
  \*********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ("<svg fill=\"currentColor\" id=\"icon\" xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 32 32\"><defs><style>.cls-1{fill:none;}</style></defs><title>view</title><path d=\"M30.94,15.66A16.69,16.69,0,0,0,16,5,16.69,16.69,0,0,0,1.06,15.66a1,1,0,0,0,0,.68A16.69,16.69,0,0,0,16,27,16.69,16.69,0,0,0,30.94,16.34,1,1,0,0,0,30.94,15.66ZM16,25c-5.3,0-10.9-3.93-12.93-9C5.1,10.93,10.7,7,16,7s10.9,3.93,12.93,9C26.9,21.07,21.3,25,16,25Z\" transform=\"translate(0 0)\"/><path d=\"M16,10a6,6,0,1,0,6,6A6,6,0,0,0,16,10Zm0,10a4,4,0,1,1,4-4A4,4,0,0,1,16,20Z\" transform=\"translate(0 0)\"/><rect id=\"_Transparent_Rectangle_\" data-name=\"&lt;Transparent Rectangle&gt;\" class=\"cls-1\" width=\"32\" height=\"32\"/></svg>");

/***/ }),

/***/ "../ui-components/style/index.css":
/*!****************************************!*\
  !*** ../ui-components/style/index.css ***!
  \****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! !../../../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js */ "../../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_css_loader_dist_cjs_js_index_css__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! !!../../../node_modules/css-loader/dist/cjs.js!./index.css */ "../../node_modules/css-loader/dist/cjs.js!../ui-components/style/index.css");

            

var options = {};

options.insert = "head";
options.singleton = false;

var update = _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default()(_node_modules_css_loader_dist_cjs_js_index_css__WEBPACK_IMPORTED_MODULE_1__["default"], options);



/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (_node_modules_css_loader_dist_cjs_js_index_css__WEBPACK_IMPORTED_MODULE_1__["default"].locals || {});

/***/ }),

/***/ "../ui-components/style/icons/r-logo.svg?24ea":
/*!***********************************************!*\
  !*** ../ui-components/style/icons/r-logo.svg ***!
  \***********************************************/
/***/ ((module) => {

module.exports = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink' preserveAspectRatio='xMidYMid' width='32' height='32' viewBox='0 0 724 561'%3E %3Cpath class='jp-icon-selectable' d='M361.453,485.937 C162.329,485.937 0.906,377.828 0.906,244.469 C0.906,111.109 162.329,3.000 361.453,3.000 C560.578,3.000 722.000,111.109 722.000,244.469 C722.000,377.828 560.578,485.937 361.453,485.937 ZM416.641,97.406 C265.289,97.406 142.594,171.314 142.594,262.484 C142.594,353.654 265.289,427.562 416.641,427.562 C567.992,427.562 679.687,377.033 679.687,262.484 C679.687,147.971 567.992,97.406 416.641,97.406 Z' fill='rgb(179,179,179)' fill-rule='evenodd'/%3E %3Cpath class='jp-icon-selectable' d='M550.000,377.000 C550.000,377.000 571.822,383.585 584.500,390.000 C588.899,392.226 596.510,396.668 602.000,402.500 C607.378,408.212 610.000,414.000 610.000,414.000 L696.000,559.000 L557.000,559.062 L492.000,437.000 C492.000,437.000 478.690,414.131 470.500,407.500 C463.668,401.969 460.755,400.000 454.000,400.000 C449.298,400.000 420.974,400.000 420.974,400.000 L421.000,558.974 L298.000,559.026 L298.000,152.938 L545.000,152.938 C545.000,152.938 657.500,154.967 657.500,262.000 C657.500,369.033 550.000,377.000 550.000,377.000 ZM496.500,241.024 L422.037,240.976 L422.000,310.026 L496.500,310.002 C496.500,310.002 531.000,309.895 531.000,274.877 C531.000,239.155 496.500,241.024 496.500,241.024 Z' fill='rgb(52,101,176)' fill-rule='evenodd'/%3E %3C/svg%3E"

/***/ }),

/***/ "../ui-components/lib/BrowseFileDialog.js":
/*!************************************************!*\
  !*** ../ui-components/lib/BrowseFileDialog.js ***!
  \************************************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";

/*
 * Copyright 2018-2022 Elyra Authors
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.showBrowseFileDialog = void 0;
const apputils_1 = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
const filebrowser_1 = __webpack_require__(/*! @jupyterlab/filebrowser */ "webpack/sharing/consume/default/@jupyterlab/filebrowser");
const widgets_1 = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
const BROWSE_FILE_CLASS = 'elyra-browseFileDialog';
const BROWSE_FILE_OPEN_CLASS = 'elyra-browseFileDialog-open';
/**
 * Breadcrumbs widget for browse file dialog body.
 */
class BrowseFileDialogBreadcrumbs extends filebrowser_1.BreadCrumbs {
    constructor(options) {
        super(options);
        this.model = options.model;
        this.rootPath = options.rootPath;
    }
    onUpdateRequest(msg) {
        super.onUpdateRequest(msg);
        const contents = this.model.manager.services.contents;
        const localPath = contents.localPath(this.model.path);
        // if 'rootPath' is defined prevent navigating to it's parent/grandparent directories
        if (localPath && this.rootPath && localPath.indexOf(this.rootPath) === 0) {
            const breadcrumbs = document.querySelectorAll('.elyra-browseFileDialog .jp-BreadCrumbs > span[title]');
            breadcrumbs.forEach((crumb) => {
                var _a;
                if (crumb.title.indexOf((_a = this.rootPath) !== null && _a !== void 0 ? _a : '') === 0) {
                    crumb.className = crumb.className
                        .replace('elyra-BreadCrumbs-disabled', '')
                        .trim();
                }
                else if (crumb.className.indexOf('elyra-BreadCrumbs-disabled') === -1) {
                    crumb.className += ' elyra-BreadCrumbs-disabled';
                }
            });
        }
    }
}
/**
 * Browse file widget for dialog body
 */
class BrowseFileDialog extends widgets_1.Widget {
    constructor(props) {
        super(props);
        this.model = new filebrowser_1.FilterFileBrowserModel({
            manager: props.manager,
            filter: props.filter
        });
        const layout = (this.layout = new widgets_1.PanelLayout());
        this.directoryListing = new filebrowser_1.DirListing({
            model: this.model
        });
        this.acceptFileOnDblClick = props.acceptFileOnDblClick;
        this.multiselect = props.multiselect;
        this.includeDir = props.includeDir;
        this.dirListingHandleEvent = this.directoryListing.handleEvent;
        this.directoryListing.handleEvent = (event) => {
            this.handleEvent(event);
        };
        this.breadCrumbs = new BrowseFileDialogBreadcrumbs({
            model: this.model,
            rootPath: props.rootPath
        });
        layout.addWidget(this.breadCrumbs);
        layout.addWidget(this.directoryListing);
    }
    static init(options) {
        return __awaiter(this, void 0, void 0, function* () {
            const browseFileDialog = new BrowseFileDialog(options);
            if (options.startPath) {
                if (!options.rootPath ||
                    options.startPath.indexOf(options.rootPath) === 0) {
                    yield browseFileDialog.model.cd(options.startPath);
                }
            }
            else if (options.rootPath) {
                yield browseFileDialog.model.cd(options.rootPath);
            }
            return browseFileDialog;
        });
    }
    getValue() {
        const itemsIter = this.directoryListing.selectedItems();
        const selected = [];
        let item = null;
        while ((item = itemsIter.next()) !== undefined) {
            if (this.includeDir || item.type !== 'directory') {
                selected.push(item);
            }
        }
        return selected;
    }
    handleEvent(event) {
        let modifierKey = false;
        if (event instanceof MouseEvent) {
            modifierKey =
                event.shiftKey || event.metaKey;
        }
        else if (event instanceof KeyboardEvent) {
            modifierKey =
                event.shiftKey || event.metaKey;
        }
        switch (event.type) {
            case 'keydown':
            case 'keyup':
            case 'mousedown':
            case 'mouseup':
            case 'click':
                if (this.multiselect || !modifierKey) {
                    this.dirListingHandleEvent.call(this.directoryListing, event);
                }
                break;
            case 'dblclick': {
                const clickedItem = this.directoryListing.modelForClick(event);
                if ((clickedItem === null || clickedItem === void 0 ? void 0 : clickedItem.type) === 'directory') {
                    this.dirListingHandleEvent.call(this.directoryListing, event);
                }
                else {
                    event.preventDefault();
                    event.stopPropagation();
                    if (this.acceptFileOnDblClick) {
                        const okButton = document.querySelector(`.${BROWSE_FILE_OPEN_CLASS} .jp-mod-accept`);
                        if (okButton) {
                            okButton.click();
                        }
                    }
                }
                break;
            }
            default:
                this.dirListingHandleEvent.call(this.directoryListing, event);
                break;
        }
    }
}
const showBrowseFileDialog = (manager, options) => __awaiter(void 0, void 0, void 0, function* () {
    const browseFileDialogBody = yield BrowseFileDialog.init({
        manager: manager,
        filter: options.filter,
        multiselect: options.multiselect,
        includeDir: options.includeDir,
        rootPath: options.rootPath,
        startPath: options.startPath,
        acceptFileOnDblClick: Object.prototype.hasOwnProperty.call(options, 'acceptFileOnDblClick')
            ? options.acceptFileOnDblClick
            : true
    });
    const dialog = new apputils_1.Dialog({
        title: 'Select a file',
        body: browseFileDialogBody,
        buttons: [apputils_1.Dialog.cancelButton(), apputils_1.Dialog.okButton({ label: 'Select' })]
    });
    dialog.addClass(BROWSE_FILE_CLASS);
    document.body.className += ` ${BROWSE_FILE_OPEN_CLASS}`;
    return dialog.launch().then((result) => {
        document.body.className = document.body.className
            .replace(BROWSE_FILE_OPEN_CLASS, '')
            .trim();
        if (options.rootPath && result.button.accept && result.value.length) {
            const relativeToPath = options.rootPath.endsWith('/')
                ? options.rootPath
                : options.rootPath + '/';
            result.value.forEach((val) => {
                val.path = val.path.replace(relativeToPath, '');
            });
        }
        return result;
    });
});
exports.showBrowseFileDialog = showBrowseFileDialog;
//# sourceMappingURL=BrowseFileDialog.js.map

/***/ }),

/***/ "../ui-components/lib/Dropzone.js":
/*!****************************************!*\
  !*** ../ui-components/lib/Dropzone.js ***!
  \****************************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";

var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    Object.defineProperty(o, k2, { enumerable: true, get: function() { return m[k]; } });
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (k !== "default" && Object.prototype.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
    __setModuleDefault(result, mod);
    return result;
};
var __rest = (this && this.__rest) || function (s, e) {
    var t = {};
    for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p) && e.indexOf(p) < 0)
        t[p] = s[p];
    if (s != null && typeof Object.getOwnPropertySymbols === "function")
        for (var i = 0, p = Object.getOwnPropertySymbols(s); i < p.length; i++) {
            if (e.indexOf(p[i]) < 0 && Object.prototype.propertyIsEnumerable.call(s, p[i]))
                t[p[i]] = s[p[i]];
        }
    return t;
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.Dropzone = exports.useDropzone = void 0;
const react_1 = __importStar(__webpack_require__(/*! react */ "webpack/sharing/consume/default/react"));
const useDropzone = (props) => {
    const rootRef = react_1.useRef(null);
    const handleEvent = react_1.useCallback((e) => {
        var _a, _b, _c, _d;
        e.preventDefault();
        e.stopPropagation();
        switch (e.type) {
            case 'lm-dragenter':
                (_a = props.onDragEnter) === null || _a === void 0 ? void 0 : _a.call(props, e);
                break;
            case 'lm-dragleave':
                (_b = props.onDragLeave) === null || _b === void 0 ? void 0 : _b.call(props, e);
                break;
            case 'lm-dragover':
                e.dropAction = e.proposedAction;
                (_c = props.onDragOver) === null || _c === void 0 ? void 0 : _c.call(props, e);
                break;
            case 'lm-drop':
                (_d = props.onDrop) === null || _d === void 0 ? void 0 : _d.call(props, e);
                break;
        }
    }, [props]);
    react_1.useEffect(() => {
        const node = rootRef.current;
        node === null || node === void 0 ? void 0 : node.addEventListener('lm-dragenter', handleEvent);
        node === null || node === void 0 ? void 0 : node.addEventListener('lm-dragleave', handleEvent);
        node === null || node === void 0 ? void 0 : node.addEventListener('lm-dragover', handleEvent);
        node === null || node === void 0 ? void 0 : node.addEventListener('lm-drop', handleEvent);
        return () => {
            node === null || node === void 0 ? void 0 : node.removeEventListener('lm-dragenter', handleEvent);
            node === null || node === void 0 ? void 0 : node.removeEventListener('lm-dragleave', handleEvent);
            node === null || node === void 0 ? void 0 : node.removeEventListener('lm-dragover', handleEvent);
            node === null || node === void 0 ? void 0 : node.removeEventListener('lm-drop', handleEvent);
        };
    }, [handleEvent]);
    return {
        getRootProps: () => ({
            ref: rootRef
        })
    };
};
exports.useDropzone = useDropzone;
const Dropzone = (_a) => {
    var { children } = _a, rest = __rest(_a, ["children"]);
    const { getRootProps } = exports.useDropzone(rest);
    return (react_1.default.createElement("div", Object.assign({ style: { height: '100%' } }, getRootProps()), children));
};
exports.Dropzone = Dropzone;
//# sourceMappingURL=Dropzone.js.map

/***/ }),

/***/ "../ui-components/lib/ExpandableComponent.js":
/*!***************************************************!*\
  !*** ../ui-components/lib/ExpandableComponent.js ***!
  \***************************************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";

/*
 * Copyright 2018-2022 Elyra Authors
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    Object.defineProperty(o, k2, { enumerable: true, get: function() { return m[k]; } });
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (k !== "default" && Object.prototype.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
    __setModuleDefault(result, mod);
    return result;
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.ExpandableComponent = void 0;
__webpack_require__(/*! ../style/index.css */ "../ui-components/style/index.css");
const ui_components_1 = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
const React = __importStar(__webpack_require__(/*! react */ "webpack/sharing/consume/default/react"));
const FeedbackButton_1 = __webpack_require__(/*! ./FeedbackButton */ "../ui-components/lib/FeedbackButton.js");
/**
 * The CSS class for expandable containers.
 */
const DETAILS_VISIBLE_CLASS = 'elyra-expandableContainer-details-visible';
const DETAILS_HIDDEN_CLASS = 'elyra-expandableContainer-details-hidden';
const DISPLAY_NAME_CLASS = 'elyra-expandableContainer-name';
const ELYRA_BUTTON_CLASS = 'elyra-button';
const BUTTON_CLASS = 'elyra-expandableContainer-button';
const TITLE_CLASS = 'elyra-expandableContainer-title';
const ACTION_BUTTONS_WRAPPER_CLASS = 'elyra-expandableContainer-action-buttons';
const ACTION_BUTTON_CLASS = 'elyra-expandableContainer-actionButton';
const DRAGGABLE_CLASS = 'elyra-expandableContainer-draggable';
/**
 * A React component for expandable containers.
 */
const ExpandableComponent = ({ displayName, tooltip, actionButtons = [], onExpand, onBeforeExpand, onMouseDown, children }) => {
    const [expanded, setExpandedValue] = React.useState(false);
    const handleToggleDetailsDisplay = () => {
        // Switch expanded flag
        const newExpandFlag = !expanded;
        onBeforeExpand === null || onBeforeExpand === void 0 ? void 0 : onBeforeExpand(newExpandFlag);
        setExpandedValue(newExpandFlag);
    };
    React.useEffect(() => {
        onExpand === null || onExpand === void 0 ? void 0 : onExpand(expanded);
    });
    const buttonClasses = [ELYRA_BUTTON_CLASS, BUTTON_CLASS].join(' ');
    return (React.createElement("div", null,
        React.createElement("div", { key: displayName, className: TITLE_CLASS },
            React.createElement("button", { className: buttonClasses, title: expanded ? 'Hide Details' : 'Show Details', onClick: handleToggleDetailsDisplay }, expanded ? (React.createElement(ui_components_1.caretDownIcon.react, { tag: "span", elementPosition: "center", width: "20px" })) : (React.createElement(ui_components_1.caretRightIcon.react, { tag: "span", elementPosition: "center", width: "20px" }))),
            React.createElement("span", { title: tooltip, className: onMouseDown
                    ? DISPLAY_NAME_CLASS
                    : DISPLAY_NAME_CLASS + ' ' + DRAGGABLE_CLASS, onClick: handleToggleDetailsDisplay, onMouseDown: (event) => {
                    onMouseDown === null || onMouseDown === void 0 ? void 0 : onMouseDown(event);
                } }, displayName),
            React.createElement("div", { className: ACTION_BUTTONS_WRAPPER_CLASS }, actionButtons.map((btn) => {
                var _a;
                return (React.createElement(FeedbackButton_1.FeedbackButton, { key: btn.title, title: btn.title, feedback: (_a = btn.feedback) !== null && _a !== void 0 ? _a : '', className: buttonClasses + ' ' + ACTION_BUTTON_CLASS, onClick: btn.onClick },
                    React.createElement(btn.icon.react, { tag: "span", elementPosition: "center", width: "16px" })));
            }))),
        React.createElement("div", { className: expanded ? DETAILS_VISIBLE_CLASS : DETAILS_HIDDEN_CLASS }, children)));
};
exports.ExpandableComponent = ExpandableComponent;
//# sourceMappingURL=ExpandableComponent.js.map

/***/ }),

/***/ "../ui-components/lib/ExpandableErrorDialog.js":
/*!*****************************************************!*\
  !*** ../ui-components/lib/ExpandableErrorDialog.js ***!
  \*****************************************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";

/*
 * Copyright 2018-2022 Elyra Authors
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    Object.defineProperty(o, k2, { enumerable: true, get: function() { return m[k]; } });
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (k !== "default" && Object.prototype.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
    __setModuleDefault(result, mod);
    return result;
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.ExpandableErrorDialog = void 0;
const React = __importStar(__webpack_require__(/*! react */ "webpack/sharing/consume/default/react"));
const ExpandableComponent_1 = __webpack_require__(/*! ./ExpandableComponent */ "../ui-components/lib/ExpandableComponent.js");
const MESSAGE_DISPLAY = 'elyra-errorDialog-messageDisplay';
const ERROR_DIALOG_WIDTH = 600;
const ERROR_DIALOG_HEIGHT = 400;
const JP_DIALOG_CONTENT = 'jp-Dialog-content';
const ExpandableErrorDialog = ({ reason, message, timestamp, traceback, defaultMessage }) => {
    const [collapsedSize, setCollapsedSize] = React.useState();
    const handleUpdateDialogSize = React.useCallback((expanded) => {
        const dialogNode = document.querySelector('.' + JP_DIALOG_CONTENT);
        if (dialogNode === null) {
            return;
        }
        const width = dialogNode.clientWidth;
        const height = dialogNode.clientHeight;
        if (expanded &&
            (width < ERROR_DIALOG_WIDTH || height < ERROR_DIALOG_HEIGHT)) {
            setCollapsedSize({ width, height });
            dialogNode.style.width = Math.max(width, ERROR_DIALOG_WIDTH) + 'px';
            dialogNode.style.height = Math.max(height, ERROR_DIALOG_HEIGHT) + 'px';
        }
        else if (!expanded && collapsedSize) {
            dialogNode.style.width = collapsedSize.width + 'px';
            dialogNode.style.height = collapsedSize.height + 'px';
        }
    }, [collapsedSize, setCollapsedSize]);
    return (React.createElement("div", { className: MESSAGE_DISPLAY },
        React.createElement("div", null, message),
        traceback ? (React.createElement(ExpandableComponent_1.ExpandableComponent, { displayName: "Error details: ", tooltip: "Error stack trace", onBeforeExpand: handleUpdateDialogSize },
            React.createElement("pre", null, traceback))) : null,
        React.createElement("div", null, defaultMessage)));
};
exports.ExpandableErrorDialog = ExpandableErrorDialog;
//# sourceMappingURL=ExpandableErrorDialog.js.map

/***/ }),

/***/ "../ui-components/lib/FeedbackButton.js":
/*!**********************************************!*\
  !*** ../ui-components/lib/FeedbackButton.js ***!
  \**********************************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";

/*
 * Copyright 2018-2022 Elyra Authors
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    Object.defineProperty(o, k2, { enumerable: true, get: function() { return m[k]; } });
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (k !== "default" && Object.prototype.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
    __setModuleDefault(result, mod);
    return result;
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.FeedbackButton = void 0;
__webpack_require__(/*! ../style/index.css */ "../ui-components/style/index.css");
const React = __importStar(__webpack_require__(/*! react */ "webpack/sharing/consume/default/react"));
/**
 * The CSS class for feedback buttons.
 */
const ELYRA_FEEDBACKBUTTON_CLASS = 'elyra-feedbackButton';
const FeedbackButton = ({ feedback, onClick, className, children, title }) => {
    const [showFeedback, setShowFeedback] = React.useState(false);
    const handleClick = () => {
        onClick();
        if (feedback) {
            setShowFeedback(true);
            setTimeout(() => {
                setShowFeedback(false);
            }, 750);
        }
    };
    const classes = `${ELYRA_FEEDBACKBUTTON_CLASS} ${className}`;
    return (React.createElement("button", { title: title, className: classes, onClick: handleClick, "data-feedback": showFeedback ? feedback : undefined }, children));
};
exports.FeedbackButton = FeedbackButton;
//# sourceMappingURL=FeedbackButton.js.map

/***/ }),

/***/ "../ui-components/lib/FormComponents/CodeBlock.js":
/*!********************************************************!*\
  !*** ../ui-components/lib/FormComponents/CodeBlock.js ***!
  \********************************************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";

/*
 * Copyright 2018-2022 Elyra Authors
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    Object.defineProperty(o, k2, { enumerable: true, get: function() { return m[k]; } });
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (k !== "default" && Object.prototype.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
    __setModuleDefault(result, mod);
    return result;
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.CodeBlock = void 0;
const codeeditor_1 = __webpack_require__(/*! @jupyterlab/codeeditor */ "webpack/sharing/consume/default/@jupyterlab/codeeditor");
const React = __importStar(__webpack_require__(/*! react */ "webpack/sharing/consume/default/react"));
const CodeBlock = props => {
    const codeBlockRef = React.useRef(null);
    const editorRef = React.useRef();
    // `editorServices` should never change so make it a ref.
    const servicesRef = React.useRef(props.formContext.editorServices);
    React.useEffect(() => {
        var _a, _b, _c, _d;
        const handleChange = (args) => {
            props.onChange(args.text.split('\n'));
        };
        if (codeBlockRef.current !== null) {
            editorRef.current = servicesRef.current.factoryService.newInlineEditor({
                host: codeBlockRef.current,
                model: new codeeditor_1.CodeEditor.Model({
                    value: (_b = (_a = props.formData) === null || _a === void 0 ? void 0 : _a.join('\n')) !== null && _b !== void 0 ? _b : (_c = props.schema.default) === null || _c === void 0 ? void 0 : _c.join('\n'),
                    mimeType: servicesRef.current.mimeTypeService.getMimeTypeByLanguage({
                        name: props.formContext.language,
                        codemirror_mode: props.formContext.language
                    })
                })
            });
            (_d = editorRef.current) === null || _d === void 0 ? void 0 : _d.model.value.changed.connect(handleChange);
        }
        return () => {
            var _a;
            (_a = editorRef.current) === null || _a === void 0 ? void 0 : _a.model.value.changed.disconnect(handleChange);
        };
        // NOTE: The parent component is unstable so props change frequently causing
        // new editors to be created unnecessarily. This effect on mount should only
        // run on mount. Keep in mind this could have side effects, for example if
        // the `onChange` callback actually does change.
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, []);
    React.useEffect(() => {
        if (editorRef.current !== undefined) {
            editorRef.current.model.mimeType = servicesRef.current.mimeTypeService.getMimeTypeByLanguage({
                name: props.formContext.language,
                codemirror_mode: props.formContext.language
            });
        }
    }, [props.formContext.language]);
    return React.createElement("div", { ref: codeBlockRef, className: "elyra-form-code" });
};
exports.CodeBlock = CodeBlock;
//# sourceMappingURL=CodeBlock.js.map

/***/ }),

/***/ "../ui-components/lib/FormComponents/DropDown.js":
/*!*******************************************************!*\
  !*** ../ui-components/lib/FormComponents/DropDown.js ***!
  \*******************************************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";

/*
 * Copyright 2018-2022 Elyra Authors
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    Object.defineProperty(o, k2, { enumerable: true, get: function() { return m[k]; } });
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (k !== "default" && Object.prototype.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
    __setModuleDefault(result, mod);
    return result;
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.DropDown = void 0;
const React = __importStar(__webpack_require__(/*! react */ "webpack/sharing/consume/default/react"));
const DROPDOWN_ITEM_CLASS = 'elyra-form-DropDown-item';
const DropDown = props => {
    var _a;
    const { defaultValue, formContext, schema, name, required, onChange, placeholder, formData, id } = props;
    const label = (_a = schema.title) !== null && _a !== void 0 ? _a : name;
    const [current, setValue] = React.useState(formData !== null && formData !== void 0 ? formData : defaultValue);
    React.useEffect(() => {
        setValue(formData);
    }, [formData]);
    const handleChange = (newValue) => {
        setValue(newValue);
        onChange(newValue);
    };
    return (React.createElement("div", null,
        React.createElement("input", { required: required, onChange: (event) => {
                handleChange(event.target.value);
            }, value: current !== null && current !== void 0 ? current : '', className: "form-control", list: `${label}-dataList`, placeholder: placeholder || `Create or select ${label.toLocaleLowerCase()}` }),
        React.createElement("datalist", { id: `${label}-dataList`, className: `elyra-metadataEditor-formInput ${DROPDOWN_ITEM_CLASS}`, key: "elyra-DropDown", style: { width: 300 } }, formContext.languageOptions.map((language) => {
            return React.createElement("option", { key: `${language}-${id}-option`, value: language });
        }))));
};
exports.DropDown = DropDown;
//# sourceMappingURL=DropDown.js.map

/***/ }),

/***/ "../ui-components/lib/FormComponents/PasswordField.js":
/*!************************************************************!*\
  !*** ../ui-components/lib/FormComponents/PasswordField.js ***!
  \************************************************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";

var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.PasswordField = void 0;
const react_1 = __importDefault(__webpack_require__(/*! react */ "webpack/sharing/consume/default/react"));
const __1 = __webpack_require__(/*! .. */ "../ui-components/lib/index.js");
/**
 * React component to edit and display password fields. Adds a button to hide / show text input.
 */
const PasswordField = props => {
    const { StringField } = props.registry.fields;
    const [showPassword, setShowPassword] = react_1.default.useState(false);
    return (react_1.default.createElement("div", { className: "elyra-passwordField" },
        react_1.default.createElement(StringField, Object.assign({}, props, { uiSchema: Object.assign(Object.assign({}, props.uiSchema), { 'ui:widget': showPassword ? undefined : 'password' }) })),
        react_1.default.createElement("button", { className: "elyra-passwordFieldButton", onClick: () => setShowPassword(!showPassword) }, showPassword ? react_1.default.createElement(__1.viewOffIcon.react, null) : react_1.default.createElement(__1.viewIcon.react, null))));
};
exports.PasswordField = PasswordField;
//# sourceMappingURL=PasswordField.js.map

/***/ }),

/***/ "../ui-components/lib/FormComponents/Tags.js":
/*!***************************************************!*\
  !*** ../ui-components/lib/FormComponents/Tags.js ***!
  \***************************************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";

var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.TagsField = exports.Tags = void 0;
/*
 * Copyright 2018-2022 Elyra Authors
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
const apputils_1 = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
const ui_components_1 = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
const react_1 = __importDefault(__webpack_require__(/*! react */ "webpack/sharing/consume/default/react"));
/**
 * CSS STYLING
 */
const FORM_EDITOR_TAG = 'elyra-editor-tag';
const FORM_EDITOR_TAG_PLUS_ICON = 'elyra-editor-tag-plusIcon';
const FORM_EDITOR_TAG_LIST = 'elyra-editor-tagList';
const FORM_EDITOR_INPUT_TAG = 'elyra-inputTag';
const Tags = props => {
    var _a, _b;
    const [selectedTags, setSelectedTags] = react_1.default.useState((_a = props.selectedTags) !== null && _a !== void 0 ? _a : []);
    const [tags, setTags] = react_1.default.useState((_b = props.tags) !== null && _b !== void 0 ? _b : []);
    const [addingNewTag, setAddingNewTag] = react_1.default.useState(false);
    const handleClick = (event) => {
        const target = event.target;
        const clickedTag = target.innerText;
        setSelectedTags(updateTagsCss(target, selectedTags !== null && selectedTags !== void 0 ? selectedTags : [], clickedTag));
        handleOnChange();
    };
    const handleOnChange = () => {
        props.handleChange(selectedTags, tags);
    };
    const updateTagsCss = (target, tags, clickedTag) => {
        const currentTags = tags.slice();
        if (target.classList.contains('unapplied-tag')) {
            target.classList.replace('unapplied-tag', 'applied-tag');
            currentTags.splice(-1, 0, clickedTag);
        }
        else if (target.classList.contains('applied-tag')) {
            target.classList.replace('applied-tag', 'unapplied-tag');
            const idx = currentTags.indexOf(clickedTag);
            currentTags.splice(idx, 1);
        }
        return currentTags;
    };
    const addTagOnClick = (event) => {
        setAddingNewTag(true);
        const inputElement = event.target;
        if (inputElement.value === 'Add Tag') {
            inputElement.value = '';
            inputElement.style.width = '62px';
            inputElement.style.minWidth = '62px';
        }
    };
    const addTagOnKeyDown = (event) => __awaiter(void 0, void 0, void 0, function* () {
        const inputElement = event.target;
        if (inputElement.value !== '' && event.keyCode === 13) {
            if (tags.includes(inputElement.value)) {
                event.preventDefault();
                yield apputils_1.showDialog({
                    title: 'A tag with this label already exists.',
                    buttons: [apputils_1.Dialog.okButton()]
                });
                return;
            }
            const newTag = inputElement.value;
            // update state all tag and selected tag
            setSelectedTags([...selectedTags, newTag]);
            setTags([...tags, newTag]);
            setAddingNewTag(false);
            handleOnChange();
        }
    });
    const addTagOnBlur = (event) => {
        const inputElement = event.target;
        inputElement.value = 'Add Tag';
        inputElement.style.width = '50px';
        inputElement.style.minWidth = '50px';
        inputElement.blur();
        setAddingNewTag(false);
    };
    const hasTags = tags;
    const inputBox = addingNewTag === true ? (react_1.default.createElement("ul", { className: `${FORM_EDITOR_TAG} tag unapplied-tag`, key: 'editor-new-tag' },
        react_1.default.createElement("input", { className: `${FORM_EDITOR_INPUT_TAG}`, onClick: (event) => addTagOnClick(event), onKeyDown: (event) => __awaiter(void 0, void 0, void 0, function* () {
                yield addTagOnKeyDown(event);
            }), onBlur: (event) => addTagOnBlur(event), autoFocus: true }))) : (react_1.default.createElement("button", { onClick: () => setAddingNewTag(true), className: `${FORM_EDITOR_TAG} tag unapplied-tag` },
        "Add Tag",
        react_1.default.createElement(ui_components_1.addIcon.react, { tag: "span", className: FORM_EDITOR_TAG_PLUS_ICON, elementPosition: "center", height: "16px", width: "16px", marginLeft: "2px" })));
    return (react_1.default.createElement("li", { className: FORM_EDITOR_TAG_LIST },
        hasTags
            ? tags.map((tag, index) => (() => {
                if (!selectedTags) {
                    return (react_1.default.createElement("button", { onClick: handleClick, className: `${FORM_EDITOR_TAG} tag unapplied-tag`, id: `editor-${tag}-${index}`, key: `editor-${tag}-${index}` }, tag));
                }
                if (selectedTags.includes(tag)) {
                    return (react_1.default.createElement("button", { onClick: handleClick, className: `${FORM_EDITOR_TAG} tag applied-tag`, id: `editor-${tag}-${index}`, key: `editor-${tag}-${index}` },
                        tag,
                        react_1.default.createElement(ui_components_1.checkIcon.react, { tag: "span", elementPosition: "center", height: "18px", width: "18px", marginLeft: "5px", marginRight: "-3px" })));
                }
                else {
                    return (react_1.default.createElement("button", { onClick: handleClick, className: `${FORM_EDITOR_TAG} tag unapplied-tag`, id: `editor-${tag}-${index}`, key: `editor-${tag}-${index}` }, tag));
                }
            })())
            : null,
        inputBox));
};
exports.Tags = Tags;
const TagsField = props => {
    var _a, _b;
    return (react_1.default.createElement(exports.Tags, { selectedTags: (_a = props.formData) !== null && _a !== void 0 ? _a : [], tags: (_b = props.formContext.allTags) !== null && _b !== void 0 ? _b : [], handleChange: (selectedTags, allTags) => {
            var _a, _b;
            props.onChange(selectedTags);
            (_b = (_a = props.formContext).updateAllTags) === null || _b === void 0 ? void 0 : _b.call(_a, allTags);
        } }));
};
exports.TagsField = TagsField;
//# sourceMappingURL=Tags.js.map

/***/ }),

/***/ "../ui-components/lib/FormComponents/index.js":
/*!****************************************************!*\
  !*** ../ui-components/lib/FormComponents/index.js ***!
  \****************************************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";

/*
 * Copyright 2018-2022 Elyra Authors
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    Object.defineProperty(o, k2, { enumerable: true, get: function() { return m[k]; } });
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __exportStar = (this && this.__exportStar) || function(m, exports) {
    for (var p in m) if (p !== "default" && !Object.prototype.hasOwnProperty.call(exports, p)) __createBinding(exports, m, p);
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
__exportStar(__webpack_require__(/*! ./Tags */ "../ui-components/lib/FormComponents/Tags.js"), exports);
__exportStar(__webpack_require__(/*! ./DropDown */ "../ui-components/lib/FormComponents/DropDown.js"), exports);
__exportStar(__webpack_require__(/*! ./PasswordField */ "../ui-components/lib/FormComponents/PasswordField.js"), exports);
__exportStar(__webpack_require__(/*! ./CodeBlock */ "../ui-components/lib/FormComponents/CodeBlock.js"), exports);
//# sourceMappingURL=index.js.map

/***/ }),

/***/ "../ui-components/lib/FormDialog.js":
/*!******************************************!*\
  !*** ../ui-components/lib/FormDialog.js ***!
  \******************************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";

/*
 * Copyright 2018-2022 Elyra Authors
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.enableButton = exports.disableButton = exports.showFormDialog = void 0;
__webpack_require__(/*! ../style/index.css */ "../ui-components/style/index.css");
const apputils_1 = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
const widgets_1 = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
const DEFAULT_BUTTON_CLASS = 'elyra-DialogDefaultButton';
/*
 * Validate dialog fields upon display
 * - Provides a generic validation by checking if required form fields are populated
 * - Expects required fields in dialog body to contain attribute: data-form-required
 * - Validates non-required numeric fields to only accept positive values
 *
 * @params
 *
 * options - The dialog setup options
 * formValidationFunction - Optional custom validation function
 *
 * returns a call to dialog display
 */
const showFormDialog = (options, formValidationFunction) => __awaiter(void 0, void 0, void 0, function* () {
    const dialogBody = options.body;
    const dialog = new apputils_1.Dialog(options);
    // Get dialog default action button
    const defaultButton = getDefaultButton(options, dialog.node);
    defaultButton.className += ' ' + DEFAULT_BUTTON_CLASS;
    if (formValidationFunction) {
        formValidationFunction(dialog);
    }
    else {
        if (dialogBody instanceof widgets_1.Widget) {
            const fieldsToBeValidated = new Set();
            const validateDialogButton = () => isFormValid(fieldsToBeValidated)
                ? exports.enableButton(defaultButton)
                : exports.disableButton(defaultButton);
            // Get elements that require validation and add event listeners
            dialogBody.node
                .querySelectorAll('select, input, textarea')
                .forEach((element) => {
                if (element.hasAttribute('data-form-required') ||
                    element.type === 'number') {
                    const elementTagName = element.tagName.toLowerCase();
                    if (elementTagName === 'select' || element.type === 'number') {
                        element.addEventListener('change', (event) => validateDialogButton());
                    }
                    if (['input', 'textarea'].includes(elementTagName)) {
                        element.addEventListener('keyup', (event) => validateDialogButton());
                    }
                    fieldsToBeValidated.add(element);
                }
            });
            preventDefaultDialogHandler(() => isFormValid(fieldsToBeValidated), dialog);
            validateDialogButton();
        }
    }
    return dialog.launch();
});
exports.showFormDialog = showFormDialog;
const disableButton = (button) => {
    button.setAttribute('disabled', 'disabled');
};
exports.disableButton = disableButton;
const enableButton = (button) => {
    button.removeAttribute('disabled');
};
exports.enableButton = enableButton;
const getDefaultButton = (options, node) => {
    var _a, _b, _c, _d;
    const defaultButtonIndex = (_a = options.defaultButton) !== null && _a !== void 0 ? _a : ((_c = (_b = options.buttons) === null || _b === void 0 ? void 0 : _b.length) !== null && _c !== void 0 ? _c : 0) - 1;
    return (_d = node
        .querySelector('.jp-Dialog-footer')) === null || _d === void 0 ? void 0 : _d.getElementsByTagName('button')[defaultButtonIndex];
};
// Prevent user from bypassing validation upon pressing the 'Enter' key
const preventDefaultDialogHandler = (isFormValidFn, dialog) => {
    const dialogHandleEvent = dialog.handleEvent;
    dialog.handleEvent = (event) => {
        if (event instanceof KeyboardEvent &&
            event.type === 'keydown' &&
            event.keyCode === 13) {
            // Prevent action when form dialog is not valid
            if (!isFormValidFn()) {
                event.stopPropagation();
                event.preventDefault();
            }
            else {
                dialogHandleEvent.call(dialog, event);
            }
        }
        else {
            dialogHandleEvent.call(dialog, event);
        }
    };
};
// Returns true if given element is valid
const isFieldValid = (element) => {
    if (element.type === 'number') {
        return element.value === '' || Number(element.value.trim()) > 0
            ? true
            : false;
    }
    return element.value.trim() ? true : false;
};
// Returns true if form dialog has all fields validated
const isFormValid = (fieldToBeValidated) => {
    for (const field of fieldToBeValidated.values()) {
        if (!isFieldValid(field)) {
            return false;
        }
    }
    return true;
};
//# sourceMappingURL=FormDialog.js.map

/***/ }),

/***/ "../ui-components/lib/FormEditor.js":
/*!******************************************!*\
  !*** ../ui-components/lib/FormEditor.js ***!
  \******************************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";

/*
 * Copyright 2018-2022 Elyra Authors
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    Object.defineProperty(o, k2, { enumerable: true, get: function() { return m[k]; } });
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (k !== "default" && Object.prototype.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
    __setModuleDefault(result, mod);
    return result;
};
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.FormEditor = void 0;
const core_1 = __importDefault(__webpack_require__(/*! @rjsf/core */ "../../node_modules/@rjsf/core/dist/es/index.js"));
const React = __importStar(__webpack_require__(/*! react */ "webpack/sharing/consume/default/react"));
/**
 * React component that allows for custom add / remove buttons in the array
 * field component.
 */
const ArrayTemplate = props => {
    var _a;
    return (React.createElement("div", { className: props.className },
        props.items.map(item => {
            return (React.createElement("div", { key: item.key, className: item.className },
                item.children,
                React.createElement("button", { className: "jp-mod-styled jp-mod-warn", onClick: item.onDropIndexClick(item.index), disabled: !item.hasRemove }, props.formContext.trans.__('Remove'))));
        }),
        props.canAdd && (React.createElement("button", { className: "jp-mod-styled jp-mod-reject", onClick: props.onAddClick }, (_a = props.formContext.trans.__('Add')) !== null && _a !== void 0 ? _a : 'Add'))));
};
const CustomFieldTemplate = props => {
    return (React.createElement("div", { className: props.classNames },
        props.schema.title !== undefined && props.schema.title !== ' ' ? (React.createElement("div", { className: "label-header" },
            React.createElement("label", { className: "control-label", htmlFor: props.id }, `${props.schema.title}${props.required ? '*' : ''}`),
            props.schema.description && (React.createElement("div", { className: "description-wrapper" },
                React.createElement("div", { className: "description-button" }, "?"),
                React.createElement("p", { className: `field-description ${props.schema.title.length < 10 ? 'short-title' : ''}` }, props.schema.description))))) : (undefined),
        props.children,
        props.errors));
};
/**
 * React component that wraps the RJSF form editor component.
 * Creates a uiSchema from given uihints and passes relevant information
 * to the custom renderers.
 */
const FormEditor = ({ schema, onChange, editorServices, componentRegistry, translator, originalData, allTags, languageOptions }) => {
    var _a, _b, _c;
    const [formData, setFormData] = React.useState(originalData !== null && originalData !== void 0 ? originalData : {});
    const [tags, setTags] = React.useState(allTags);
    /**
     * Generate the rjsf uiSchema from uihints in the elyra metadata schema.
     */
    const uiSchema = {
        classNames: 'elyra-formEditor'
    };
    for (const category in schema === null || schema === void 0 ? void 0 : schema.properties) {
        const properties = schema.properties[category];
        uiSchema[category] = {};
        for (const field in properties.properties) {
            uiSchema[category][field] = (_a = properties.properties[field].uihints) !== null && _a !== void 0 ? _a : {};
            uiSchema[category][field].classNames = `elyra-formEditor-form-${field}`;
        }
    }
    return (React.createElement(core_1.default, { schema: schema, formData: formData, formContext: {
            editorServices: editorServices,
            language: (_c = (_b = formData === null || formData === void 0 ? void 0 : formData['Source']) === null || _b === void 0 ? void 0 : _b.language) !== null && _c !== void 0 ? _c : '',
            allTags: tags,
            updateAllTags: (updatedTags) => {
                setTags(updatedTags);
            },
            languageOptions: languageOptions,
            trans: translator
        }, fields: componentRegistry === null || componentRegistry === void 0 ? void 0 : componentRegistry.renderers, ArrayFieldTemplate: ArrayTemplate, FieldTemplate: CustomFieldTemplate, uiSchema: uiSchema, onChange: (e) => {
            setFormData(e.formData);
            console.log(e.formData);
            onChange(e.formData, e.errors.length > 0 || false);
        }, liveValidate: true, noHtml5Validate: 
        /** noHtml5Validate is set to true to prevent the html validation from moving the focus when the live validate is called. */
        true }));
};
exports.FormEditor = FormEditor;
//# sourceMappingURL=FormEditor.js.map

/***/ }),

/***/ "../ui-components/lib/JSONComponent.js":
/*!*********************************************!*\
  !*** ../ui-components/lib/JSONComponent.js ***!
  \*********************************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";

/*
 * Copyright 2018-2022 Elyra Authors
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.JSONComponent = void 0;
const react_1 = __importDefault(__webpack_require__(/*! react */ "webpack/sharing/consume/default/react"));
const react_json_tree_1 = __importDefault(__webpack_require__(/*! react-json-tree */ "../../node_modules/react-json-tree/lib/index.js"));
// Provide an invalid theme object (this is on purpose!) to invalidate the
// react-json-tree's inline styles that override CodeMirror CSS classes
const theme = {
    scheme: 'jupyter',
    base00: 'invalid',
    base01: 'invalid',
    base02: 'invalid',
    base03: 'invalid',
    base04: 'invalid',
    base05: 'invalid',
    base06: 'invalid',
    base07: 'invalid',
    base08: 'invalid',
    base09: 'invalid',
    base0A: 'invalid',
    base0B: 'invalid',
    base0C: 'invalid',
    base0D: 'invalid',
    base0E: 'invalid',
    base0F: 'invalid'
};
/**
 * A React Component for displaying a json object
 *
 * A slimmed down copy of the `Component` class in @jupyterlab/json-extension
 */
const JSONComponent = ({ json }) => (react_1.default.createElement(react_json_tree_1.default, { data: json, theme: {
        extend: theme,
        valueLabel: 'cm-variable',
        valueText: 'cm-string',
        nestedNodeItemString: 'cm-comment'
    }, invertTheme: false, hideRoot: true, getItemString: (type, data, itemType, itemString) => Array.isArray(data) ? (
    // Always display array type and the number of items i.e. "[] 2 items".
    react_1.default.createElement("span", null,
        itemType,
        " ",
        itemString)) : Object.keys(data).length === 0 ? (
    // Only display object type when it's empty i.e. "{}".
    react_1.default.createElement("span", null, itemType)) : (null // Upstream typings don't accept null, but it should be ok
    ), labelRenderer: ([label, type]) => {
        return react_1.default.createElement("span", { className: "cm-keyword" }, `${label}: `);
    }, valueRenderer: (raw) => {
        let className = 'cm-string';
        if (typeof raw === 'number') {
            className = 'cm-number';
        }
        if (raw === 'true' || raw === 'false') {
            className = 'cm-keyword';
        }
        return react_1.default.createElement("span", { className: className }, `${raw}`);
    } }));
exports.JSONComponent = JSONComponent;
//# sourceMappingURL=JSONComponent.js.map

/***/ }),

/***/ "../ui-components/lib/RequestErrors.js":
/*!*********************************************!*\
  !*** ../ui-components/lib/RequestErrors.js ***!
  \*********************************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";

/*
 * Copyright 2018-2022 Elyra Authors
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    Object.defineProperty(o, k2, { enumerable: true, get: function() { return m[k]; } });
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (k !== "default" && Object.prototype.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
    __setModuleDefault(result, mod);
    return result;
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.RequestErrors = void 0;
const apputils_1 = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
const React = __importStar(__webpack_require__(/*! react */ "webpack/sharing/consume/default/react"));
const ExpandableErrorDialog_1 = __webpack_require__(/*! ./ExpandableErrorDialog */ "../ui-components/lib/ExpandableErrorDialog.js");
/**
 * A class for handling errors when making requests to the jupyter lab server.
 */
class RequestErrors {
    /**
     * An utility function that takes in a json object of issues and formats them
     * into a multiline string to be placed in the expandable error dialog.
     *
     * @param issues - A json object containing a list of issues
     *
     * @returns A human readable multiline string for displaying the issues
     */
    static formatIssues(issues) {
        let formatted = '';
        for (const issue of issues) {
            formatted += JSON.stringify(issue, null, 2) + '\n';
        }
        return formatted;
    }
    /**
     * Displays an error dialog showing error data and stacktrace, if available.
     *
     * @param response - The server response containing the error data
     *
     * @returns A promise that resolves with whether the dialog was accepted.
     */
    static serverError(response) {
        if (response.status === 404) {
            return this.server404(response.requestPath);
        }
        const reason = response.reason ? response.reason : '';
        const message = response.message ? response.message : '';
        const timestamp = response.timestamp ? response.timestamp : '';
        const traceback = response.issues
            ? this.formatIssues(response.issues)
            : response.traceback
                ? response.traceback
                : '';
        const defaultBody = response.timestamp
            ? 'Check the JupyterLab log for more details at ' + response.timestamp
            : 'Check the JupyterLab log for more details';
        return apputils_1.showDialog({
            title: 'Error making request',
            body: reason || message ? (React.createElement(ExpandableErrorDialog_1.ExpandableErrorDialog, { reason: reason, message: message, timestamp: timestamp, traceback: traceback, defaultMessage: defaultBody })) : (React.createElement("p", null, defaultBody)),
            buttons: [apputils_1.Dialog.okButton()]
        });
    }
    /**
     * Displays an error dialog for when a server request returns a 404.
     *
     * @returns A promise that resolves with whether the dialog was accepted.
     */
    static server404(endpoint) {
        return apputils_1.showDialog({
            title: 'Error contacting server',
            body: (React.createElement("p", null,
                "Endpoint ",
                React.createElement("code", null, endpoint),
                " not found.")),
            buttons: [apputils_1.Dialog.okButton()]
        });
    }
    /**
     * Displays a dialog for error cases during metadata calls.
     *
     * @param schemaspace - the metadata schemaspace that was being accessed when
     * the error occurred
     *
     * @param action (optional) - the pipeline action that required the metadata when
     * the error occurred
     * eg. run pipeline, export pipeline, run notebook as pipeline
     *
     * @returns A promise that resolves with whether the dialog was accepted.
     */
    static noMetadataError(schemaspace, action, schemaName) {
        return apputils_1.showDialog({
            title: action ? `Cannot ${action}` : 'Error retrieving metadata',
            body: (React.createElement("div", null,
                React.createElement("p", null,
                    "No ",
                    schemaspace,
                    " configuration",
                    schemaName && ` for ${schemaName}`,
                    ' ',
                    "is defined."),
                React.createElement("p", null, "Please create one and try again."))),
            buttons: schemaspace === 'runtime'
                ? [apputils_1.Dialog.cancelButton(), apputils_1.Dialog.okButton({ label: `Open runtimes` })]
                : [apputils_1.Dialog.okButton()]
        });
    }
}
exports.RequestErrors = RequestErrors;
//# sourceMappingURL=RequestErrors.js.map

/***/ }),

/***/ "../ui-components/lib/ThemeProvider.js":
/*!*********************************************!*\
  !*** ../ui-components/lib/ThemeProvider.js ***!
  \*********************************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";

/*
 * Copyright 2018-2022 Elyra Authors
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    Object.defineProperty(o, k2, { enumerable: true, get: function() { return m[k]; } });
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (k !== "default" && Object.prototype.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
    __setModuleDefault(result, mod);
    return result;
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.ThemeProvider = void 0;
const core_1 = __webpack_require__(/*! @material-ui/core */ "../../node_modules/@material-ui/core/esm/index.js");
const react_1 = __importStar(__webpack_require__(/*! react */ "webpack/sharing/consume/default/react"));
const pseudoClasses = [
    'checked',
    'disabled',
    'error',
    'focused',
    'focusVisible',
    'required',
    'expanded',
    'selected'
];
// Taken from material-ui and adapted to use custom prefixes for mui components.
const createGenerateClassName = () => {
    const elyraPrefix = 'elyra-';
    let ruleCounter = 0;
    const getNextCounterId = () => {
        ruleCounter += 1;
        return ruleCounter;
    };
    return (rule, styleSheet) => {
        const name = styleSheet.options.name;
        // Is a global static MUI style?
        if (name && name.indexOf('Mui') === 0 && !styleSheet.options.link) {
            // We can use a shorthand class name, we never use the keys to style the components.
            if (pseudoClasses.indexOf(rule.key) !== -1) {
                return `${elyraPrefix}Mui-${rule.key}`;
            }
            const prefix = `${elyraPrefix}${name}-${rule.key}`;
            if (!styleSheet.options.theme[Symbol.for('mui.nested')]) {
                return prefix;
            }
            return `${prefix}-${getNextCounterId()}`;
        }
        return `${elyraPrefix}jss${getNextCounterId()}`;
    };
};
// This should only ever be loaded once, but just in case...
if (window.ELYRA_generateClassName === undefined) {
    window.ELYRA_generateClassName = createGenerateClassName();
}
const overrides = {
    MuiFormControl: {
        root: {
            width: '100%'
        }
    },
    MuiButtonBase: {
        root: {
            padding: '5px 15px'
        }
    }
};
if (window.ELYRA_darkTheme === undefined) {
    window.ELYRA_darkTheme = core_1.createTheme({
        palette: {
            type: 'dark'
        },
        overrides
    });
}
if (window.ELYRA_lightTheme === undefined) {
    window.ELYRA_lightTheme = core_1.createTheme({
        palette: {
            type: 'light'
        },
        overrides
    });
}
const isLightTheme = (themeManager) => {
    // Default to light theme
    return (themeManager === null || themeManager === void 0 ? void 0 : themeManager.theme) ? themeManager.isLight(themeManager.theme) : true;
};
const ThemeProvider = ({ themeManager, children }) => {
    const [isLight, setIsLight] = react_1.useState(isLightTheme(themeManager));
    react_1.useEffect(() => {
        const updateTheme = () => {
            setIsLight(isLightTheme(themeManager));
        };
        if (themeManager) {
            themeManager.themeChanged.connect(updateTheme);
        }
        return () => {
            themeManager === null || themeManager === void 0 ? void 0 : themeManager.themeChanged.disconnect(updateTheme);
        };
    }, [themeManager]);
    return (react_1.default.createElement(core_1.StylesProvider, { generateClassName: window.ELYRA_generateClassName },
        react_1.default.createElement(core_1.ThemeProvider, { theme: isLight ? window.ELYRA_lightTheme : window.ELYRA_darkTheme }, children)));
};
exports.ThemeProvider = ThemeProvider;
//# sourceMappingURL=ThemeProvider.js.map

/***/ }),

/***/ "../ui-components/lib/icons.js":
/*!*************************************!*\
  !*** ../ui-components/lib/icons.js ***!
  \*************************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";

/*
 * Copyright 2018-2022 Elyra Authors
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.IconUtil = exports.viewOffIcon = exports.viewIcon = exports.pyIcon = exports.rIcon = exports.tagIcon = exports.helpIcon = exports.trashIcon = exports.containerIcon = exports.runtimesIcon = exports.savePipelineIcon = exports.exportPipelineIcon = exports.clearPipelineIcon = exports.errorIcon = exports.componentCatalogIcon = exports.pipelineIcon = exports.elyraIcon = exports.dragDropIcon = exports.codeSnippetIcon = exports.importIcon = void 0;
const ui_components_1 = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
const clear_pipeline_svg_1 = __importDefault(__webpack_require__(/*! ../style/icons/clear-pipeline.svg */ "../ui-components/style/icons/clear-pipeline.svg"));
const codait_piebrainlogo_jupyter_color_svg_1 = __importDefault(__webpack_require__(/*! ../style/icons/codait-piebrainlogo-jupyter-color.svg */ "../ui-components/style/icons/codait-piebrainlogo-jupyter-color.svg"));
const code_snippet_svg_1 = __importDefault(__webpack_require__(/*! ../style/icons/code-snippet.svg */ "../ui-components/style/icons/code-snippet.svg"));
const container_svg_1 = __importDefault(__webpack_require__(/*! ../style/icons/container.svg */ "../ui-components/style/icons/container.svg"));
const dragdrop_svg_1 = __importDefault(__webpack_require__(/*! ../style/icons/dragdrop.svg */ "../ui-components/style/icons/dragdrop.svg"));
const error_svg_1 = __importDefault(__webpack_require__(/*! ../style/icons/error.svg */ "../ui-components/style/icons/error.svg"));
const export_pipeline_svg_1 = __importDefault(__webpack_require__(/*! ../style/icons/export-pipeline.svg */ "../ui-components/style/icons/export-pipeline.svg"));
const help_svg_1 = __importDefault(__webpack_require__(/*! ../style/icons/help.svg */ "../ui-components/style/icons/help.svg"));
const import_svg_1 = __importDefault(__webpack_require__(/*! ../style/icons/import.svg */ "../ui-components/style/icons/import.svg"));
const pipeline_components_svg_1 = __importDefault(__webpack_require__(/*! ../style/icons/pipeline-components.svg */ "../ui-components/style/icons/pipeline-components.svg"));
const pipeline_flow_svg_1 = __importDefault(__webpack_require__(/*! ../style/icons/pipeline-flow.svg */ "../ui-components/style/icons/pipeline-flow.svg"));
const py_logo_svg_1 = __importDefault(__webpack_require__(/*! ../style/icons/py-logo.svg */ "../ui-components/style/icons/py-logo.svg"));
const r_logo_svg_1 = __importDefault(__webpack_require__(/*! ../style/icons/r-logo.svg */ "../ui-components/style/icons/r-logo.svg?5796"));
const runtimes_svg_1 = __importDefault(__webpack_require__(/*! ../style/icons/runtimes.svg */ "../ui-components/style/icons/runtimes.svg"));
const save_pipeline_svg_1 = __importDefault(__webpack_require__(/*! ../style/icons/save-pipeline.svg */ "../ui-components/style/icons/save-pipeline.svg"));
const tag_svg_1 = __importDefault(__webpack_require__(/*! ../style/icons/tag.svg */ "../ui-components/style/icons/tag.svg"));
const trashIcon_svg_1 = __importDefault(__webpack_require__(/*! ../style/icons/trashIcon.svg */ "../ui-components/style/icons/trashIcon.svg"));
const view__off_svg_1 = __importDefault(__webpack_require__(/*! ../style/icons/view--off.svg */ "../ui-components/style/icons/view--off.svg"));
const view_svg_1 = __importDefault(__webpack_require__(/*! ../style/icons/view.svg */ "../ui-components/style/icons/view.svg"));
exports.importIcon = new ui_components_1.LabIcon({
    name: 'elyra:import',
    svgstr: import_svg_1.default
});
exports.codeSnippetIcon = new ui_components_1.LabIcon({
    name: 'elyra:code-snippet',
    svgstr: code_snippet_svg_1.default
});
exports.dragDropIcon = new ui_components_1.LabIcon({
    name: 'elyra:dragdrop',
    svgstr: dragdrop_svg_1.default
});
exports.elyraIcon = new ui_components_1.LabIcon({ name: 'elyra:elyra', svgstr: codait_piebrainlogo_jupyter_color_svg_1.default });
exports.pipelineIcon = new ui_components_1.LabIcon({
    name: 'elyra:pipeline',
    svgstr: pipeline_flow_svg_1.default
});
exports.componentCatalogIcon = new ui_components_1.LabIcon({
    name: 'elyra:pipeline-components',
    svgstr: pipeline_components_svg_1.default
});
exports.errorIcon = new ui_components_1.LabIcon({
    name: 'elyra:errorIcon',
    svgstr: error_svg_1.default
});
exports.clearPipelineIcon = new ui_components_1.LabIcon({
    name: 'elyra:clear-pipeline',
    svgstr: clear_pipeline_svg_1.default
});
exports.exportPipelineIcon = new ui_components_1.LabIcon({
    name: 'elyra:export-pipeline',
    svgstr: export_pipeline_svg_1.default
});
exports.savePipelineIcon = new ui_components_1.LabIcon({
    name: 'elyra:save-pipeline',
    svgstr: save_pipeline_svg_1.default
});
exports.runtimesIcon = new ui_components_1.LabIcon({
    name: 'elyra:runtimes',
    svgstr: runtimes_svg_1.default
});
exports.containerIcon = new ui_components_1.LabIcon({
    name: 'elyra:container',
    svgstr: container_svg_1.default
});
exports.trashIcon = new ui_components_1.LabIcon({
    name: 'elyra:trashIcon',
    svgstr: trashIcon_svg_1.default
});
exports.helpIcon = new ui_components_1.LabIcon({
    name: 'elyra:helpIcon',
    svgstr: help_svg_1.default
});
exports.tagIcon = new ui_components_1.LabIcon({
    name: 'elyra:tagIcon',
    svgstr: tag_svg_1.default
});
exports.rIcon = new ui_components_1.LabIcon({
    name: 'elyra:rIcon',
    svgstr: r_logo_svg_1.default
});
exports.pyIcon = new ui_components_1.LabIcon({
    name: 'elyra:pyIcon',
    svgstr: py_logo_svg_1.default
});
exports.viewIcon = new ui_components_1.LabIcon({
    name: 'elyra:view',
    svgstr: view_svg_1.default
});
exports.viewOffIcon = new ui_components_1.LabIcon({
    name: 'elyra:viewOff',
    svgstr: view__off_svg_1.default
});
/**
 * A utilities class for handling LabIcons.
 */
class IconUtil {
    static encode(icon) {
        return 'data:image/svg+xml;utf8,' + encodeURIComponent(icon.svgstr);
    }
    static colorize(icon, fillColor, strokeColor) {
        const iconName = `${icon.name}${fillColor ? ':' + fillColor : ''}${strokeColor ? ':' + strokeColor : ''}`;
        if (this.colorizedIcons[iconName]) {
            return this.colorizedIcons[iconName];
        }
        let svgstr = icon.svgstr;
        if (fillColor) {
            svgstr = svgstr.replace(/fill="(?:(?!none).)+?"/gi, `fill="${fillColor}"`);
        }
        if (strokeColor) {
            svgstr = svgstr.replace(/stroke="(?:(?!none).)+?"/gi, `stroke="${strokeColor}"`);
        }
        const coloredIcon = ui_components_1.LabIcon.resolve({
            icon: {
                name: iconName,
                svgstr: svgstr
            }
        });
        this.colorizedIcons[iconName] = coloredIcon;
        return coloredIcon;
    }
}
exports.IconUtil = IconUtil;
IconUtil.colorizedIcons = {};
//# sourceMappingURL=icons.js.map

/***/ }),

/***/ "../ui-components/lib/index.js":
/*!*************************************!*\
  !*** ../ui-components/lib/index.js ***!
  \*************************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";

var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    Object.defineProperty(o, k2, { enumerable: true, get: function() { return m[k]; } });
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __exportStar = (this && this.__exportStar) || function(m, exports) {
    for (var p in m) if (p !== "default" && !Object.prototype.hasOwnProperty.call(exports, p)) __createBinding(exports, m, p);
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
/*
 * Copyright 2018-2022 Elyra Authors
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
__exportStar(__webpack_require__(/*! ./BrowseFileDialog */ "../ui-components/lib/BrowseFileDialog.js"), exports);
__exportStar(__webpack_require__(/*! ./ExpandableErrorDialog */ "../ui-components/lib/ExpandableErrorDialog.js"), exports);
__exportStar(__webpack_require__(/*! ./ExpandableComponent */ "../ui-components/lib/ExpandableComponent.js"), exports);
__exportStar(__webpack_require__(/*! ./FormDialog */ "../ui-components/lib/FormDialog.js"), exports);
__exportStar(__webpack_require__(/*! ./FormEditor */ "../ui-components/lib/FormEditor.js"), exports);
__exportStar(__webpack_require__(/*! ./icons */ "../ui-components/lib/icons.js"), exports);
__exportStar(__webpack_require__(/*! ./FormComponents */ "../ui-components/lib/FormComponents/index.js"), exports);
__exportStar(__webpack_require__(/*! ./JSONComponent */ "../ui-components/lib/JSONComponent.js"), exports);
__exportStar(__webpack_require__(/*! ./Dropzone */ "../ui-components/lib/Dropzone.js"), exports);
__exportStar(__webpack_require__(/*! ./RequestErrors */ "../ui-components/lib/RequestErrors.js"), exports);
__exportStar(__webpack_require__(/*! ./ThemeProvider */ "../ui-components/lib/ThemeProvider.js"), exports);
//# sourceMappingURL=index.js.map

/***/ })

}]);
//# sourceMappingURL=ui-components_lib_FormComponents_PasswordField_js-ui-components_lib_FormComponents_index_js-u-7d59f0.8d063b000f40c5b6fb9c.js.map
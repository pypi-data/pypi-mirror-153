"use strict";
(self["webpackChunk_elyra_python_editor_extension"] = self["webpackChunk_elyra_python_editor_extension"] || []).push([["script-editor_lib_index_js"],{

/***/ "../../node_modules/css-loader/dist/cjs.js!../script-editor/style/index.css":
/*!**********************************************************************************!*\
  !*** ../../node_modules/css-loader/dist/cjs.js!../script-editor/style/index.css ***!
  \**********************************************************************************/
/***/ ((module, __webpack_exports__, __webpack_require__) => {

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
___CSS_LOADER_EXPORT___.push([module.id, "/*\n * Copyright 2018-2022 Elyra Authors\n *\n * Licensed under the Apache License, Version 2.0 (the \"License\");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n * http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an \"AS IS\" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n */\n\n.elyra-ScriptEditor-OutputArea-error {\n  background-color: var(--jp-rendermime-error-background);\n}\n\n.elyra-ScriptEditor-OutputArea-child {\n  border-top: 1px solid var(--jp-border-color2);\n  border-bottom: 1px solid var(--jp-border-color2);\n}\n\n.elyra-ScriptEditor-OutputArea-prompt {\n  flex: 0 0 37px;\n  border-right: 1px solid var(--jp-border-color2);\n  display: flex;\n  justify-content: center;\n}\n\n.elyra-ScriptEditor-OutputArea-output {\n  padding: var(--jp-code-padding);\n  border: var(--jp-border-width) solid transparent;\n  margin-right: 64px;\n}\n\n.elyra-ScriptEditor-scrollTop {\n  top: 33px;\n}\n\n.elyra-ScriptEditor-scrollBottom {\n  top: 62px;\n}\n\n.elyra-ScriptEditor-scrollBottom,\n.elyra-ScriptEditor-scrollTop {\n  position: absolute;\n  right: 21px;\n  z-index: 1;\n  background-color: transparent;\n  width: 30px;\n  height: 30px;\n  border-width: 0px;\n  border-style: solid;\n  border-radius: 5px;\n}\n\nbutton.elyra-ScriptEditor-scrollTop:hover {\n  background-color: var(--jp-layout-color2);\n}\n\nbutton.elyra-ScriptEditor-scrollBottom:hover {\n  background-color: var(--jp-layout-color2);\n}\n\n.elyra-ScriptEditor-scrollBottom g[fill],\n.elyra-ScriptEditor-scrollTop g[fill] {\n  fill: var(--jp-inverse-layout-color3);\n}\n\n.jp-Document .jp-Toolbar.elyra-ScriptEditor-Toolbar {\n  justify-content: flex-start;\n}\n\nselect.elyra-ScriptEditor-KernelSelector {\n  border: none;\n  background: none;\n  color: var(--jp-ui-font-color1);\n  display: inline-block;\n  vertical-align: text-bottom;\n}\n", "",{"version":3,"sources":["webpack://./../script-editor/style/index.css"],"names":[],"mappings":"AAAA;;;;;;;;;;;;;;EAcE;;AAEF;EACE,uDAAuD;AACzD;;AAEA;EACE,6CAA6C;EAC7C,gDAAgD;AAClD;;AAEA;EACE,cAAc;EACd,+CAA+C;EAC/C,aAAa;EACb,uBAAuB;AACzB;;AAEA;EACE,+BAA+B;EAC/B,gDAAgD;EAChD,kBAAkB;AACpB;;AAEA;EACE,SAAS;AACX;;AAEA;EACE,SAAS;AACX;;AAEA;;EAEE,kBAAkB;EAClB,WAAW;EACX,UAAU;EACV,6BAA6B;EAC7B,WAAW;EACX,YAAY;EACZ,iBAAiB;EACjB,mBAAmB;EACnB,kBAAkB;AACpB;;AAEA;EACE,yCAAyC;AAC3C;;AAEA;EACE,yCAAyC;AAC3C;;AAEA;;EAEE,qCAAqC;AACvC;;AAEA;EACE,2BAA2B;AAC7B;;AAEA;EACE,YAAY;EACZ,gBAAgB;EAChB,+BAA+B;EAC/B,qBAAqB;EACrB,2BAA2B;AAC7B","sourcesContent":["/*\n * Copyright 2018-2022 Elyra Authors\n *\n * Licensed under the Apache License, Version 2.0 (the \"License\");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n * http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an \"AS IS\" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n */\n\n.elyra-ScriptEditor-OutputArea-error {\n  background-color: var(--jp-rendermime-error-background);\n}\n\n.elyra-ScriptEditor-OutputArea-child {\n  border-top: 1px solid var(--jp-border-color2);\n  border-bottom: 1px solid var(--jp-border-color2);\n}\n\n.elyra-ScriptEditor-OutputArea-prompt {\n  flex: 0 0 37px;\n  border-right: 1px solid var(--jp-border-color2);\n  display: flex;\n  justify-content: center;\n}\n\n.elyra-ScriptEditor-OutputArea-output {\n  padding: var(--jp-code-padding);\n  border: var(--jp-border-width) solid transparent;\n  margin-right: 64px;\n}\n\n.elyra-ScriptEditor-scrollTop {\n  top: 33px;\n}\n\n.elyra-ScriptEditor-scrollBottom {\n  top: 62px;\n}\n\n.elyra-ScriptEditor-scrollBottom,\n.elyra-ScriptEditor-scrollTop {\n  position: absolute;\n  right: 21px;\n  z-index: 1;\n  background-color: transparent;\n  width: 30px;\n  height: 30px;\n  border-width: 0px;\n  border-style: solid;\n  border-radius: 5px;\n}\n\nbutton.elyra-ScriptEditor-scrollTop:hover {\n  background-color: var(--jp-layout-color2);\n}\n\nbutton.elyra-ScriptEditor-scrollBottom:hover {\n  background-color: var(--jp-layout-color2);\n}\n\n.elyra-ScriptEditor-scrollBottom g[fill],\n.elyra-ScriptEditor-scrollTop g[fill] {\n  fill: var(--jp-inverse-layout-color3);\n}\n\n.jp-Document .jp-Toolbar.elyra-ScriptEditor-Toolbar {\n  justify-content: flex-start;\n}\n\nselect.elyra-ScriptEditor-KernelSelector {\n  border: none;\n  background: none;\n  color: var(--jp-ui-font-color1);\n  display: inline-block;\n  vertical-align: text-bottom;\n}\n"],"sourceRoot":""}]);
// Exports
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (___CSS_LOADER_EXPORT___);


/***/ }),

/***/ "../script-editor/style/index.css":
/*!****************************************!*\
  !*** ../script-editor/style/index.css ***!
  \****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! !../../../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js */ "../../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_css_loader_dist_cjs_js_index_css__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! !!../../../node_modules/css-loader/dist/cjs.js!./index.css */ "../../node_modules/css-loader/dist/cjs.js!../script-editor/style/index.css");

            

var options = {};

options.insert = "head";
options.singleton = false;

var update = _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default()(_node_modules_css_loader_dist_cjs_js_index_css__WEBPACK_IMPORTED_MODULE_1__["default"], options);



/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (_node_modules_css_loader_dist_cjs_js_index_css__WEBPACK_IMPORTED_MODULE_1__["default"].locals || {});

/***/ }),

/***/ "../script-editor/lib/KernelDropdown.js":
/*!**********************************************!*\
  !*** ../script-editor/lib/KernelDropdown.js ***!
  \**********************************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {


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
exports.KernelDropdown = void 0;
const apputils_1 = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
const react_1 = __importStar(__webpack_require__(/*! react */ "webpack/sharing/consume/default/react"));
const KERNEL_SELECT_CLASS = 'elyra-ScriptEditor-KernelSelector';
/**
 * A toolbar dropdown component populated with available kernel specs.
 */
// eslint-disable-next-line react/display-name
const DropDown = react_1.forwardRef(({ specs }, select) => {
    var _a, _b, _c;
    const initVal = (_c = (_b = Object.values((_a = specs.kernelspecs) !== null && _a !== void 0 ? _a : [])[0]) === null || _b === void 0 ? void 0 : _b.name) !== null && _c !== void 0 ? _c : '';
    const [selection, setSelection] = react_1.useState(initVal);
    // Note: It's normally best to avoid using an imperative handle if possible.
    // The better option would be to track state in the parent component and handle
    // the change events there as well, but I know this isn't always possible
    // alongside jupyter.
    react_1.useImperativeHandle(select, () => ({
        getSelection: () => selection
    }));
    const kernelOptions = !Object.keys(specs.kernelspecs).length ? (react_1.default.createElement("option", { key: "no-kernel", value: "no-kernel" }, "No Kernel")) : (Object.entries(specs.kernelspecs).map(([key, val]) => {
        var _a;
        return (react_1.default.createElement("option", { key: key, value: key }, (_a = val === null || val === void 0 ? void 0 : val.display_name) !== null && _a !== void 0 ? _a : key));
    }));
    return (react_1.default.createElement("select", { className: KERNEL_SELECT_CLASS, onChange: (e) => setSelection(e.target.value), value: selection }, kernelOptions));
});
/**
 * Wrap the dropDown into a React Widget in order to insert it into a Lab Toolbar Widget
 */
class KernelDropdown extends apputils_1.ReactWidget {
    /**
     * Construct a new CellTypeSwitcher widget.
     */
    constructor(specs, ref) {
        super();
        this.specs = specs;
        this.ref = ref;
    }
    render() {
        return react_1.default.createElement(DropDown, { ref: this.ref, specs: this.specs });
    }
}
exports.KernelDropdown = KernelDropdown;
//# sourceMappingURL=KernelDropdown.js.map

/***/ }),

/***/ "../script-editor/lib/ScriptEditor.js":
/*!********************************************!*\
  !*** ../script-editor/lib/ScriptEditor.js ***!
  \********************************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {


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
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.ScriptEditor = void 0;
const apputils_1 = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
const docregistry_1 = __webpack_require__(/*! @jupyterlab/docregistry */ "webpack/sharing/consume/default/@jupyterlab/docregistry");
const logconsole_1 = __webpack_require__(/*! @jupyterlab/logconsole */ "webpack/sharing/consume/default/@jupyterlab/logconsole");
const outputarea_1 = __webpack_require__(/*! @jupyterlab/outputarea */ "webpack/sharing/consume/default/@jupyterlab/outputarea");
const rendermime_1 = __webpack_require__(/*! @jupyterlab/rendermime */ "webpack/sharing/consume/default/@jupyterlab/rendermime");
const ui_components_1 = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
const widgets_1 = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
const react_1 = __importDefault(__webpack_require__(/*! react */ "webpack/sharing/consume/default/react"));
const KernelDropdown_1 = __webpack_require__(/*! ./KernelDropdown */ "../script-editor/lib/KernelDropdown.js");
const ScriptEditorController_1 = __webpack_require__(/*! ./ScriptEditorController */ "../script-editor/lib/ScriptEditorController.js");
const ScriptRunner_1 = __webpack_require__(/*! ./ScriptRunner */ "../script-editor/lib/ScriptRunner.js");
/**
 * The CSS class added to widgets.
 */
const SCRIPT_EDITOR_CLASS = 'elyra-ScriptEditor';
const OUTPUT_AREA_CLASS = 'elyra-ScriptEditor-OutputArea';
const OUTPUT_AREA_ERROR_CLASS = 'elyra-ScriptEditor-OutputArea-error';
const OUTPUT_AREA_CHILD_CLASS = 'elyra-ScriptEditor-OutputArea-child';
const OUTPUT_AREA_OUTPUT_CLASS = 'elyra-ScriptEditor-OutputArea-output';
const OUTPUT_AREA_PROMPT_CLASS = 'elyra-ScriptEditor-OutputArea-prompt';
const RUN_BUTTON_CLASS = 'elyra-ScriptEditor-Run';
const TOOLBAR_CLASS = 'elyra-ScriptEditor-Toolbar';
/**
 * A widget for script editors.
 */
class ScriptEditor extends docregistry_1.DocumentWidget {
    /**
     * Construct a new editor widget.
     */
    constructor(options) {
        super(options);
        this.initializeKernelSpecs = () => __awaiter(this, void 0, void 0, function* () {
            var _a, _b;
            const kernelSpecs = yield this.controller.getKernelSpecsByLanguage(this.getLanguage());
            this.kernelName = (_b = Object.values((_a = kernelSpecs === null || kernelSpecs === void 0 ? void 0 : kernelSpecs.kernelspecs) !== null && _a !== void 0 ? _a : [])[0]) === null || _b === void 0 ? void 0 : _b.name;
            this.kernelSelectorRef = react_1.default.createRef();
            if (kernelSpecs !== null) {
                const kernelDropDown = new KernelDropdown_1.KernelDropdown(kernelSpecs, this.kernelSelectorRef);
                this.toolbar.insertItem(3, 'select', kernelDropDown);
            }
        });
        /**
         * Function: Creates an OutputArea widget wrapped in a DockPanel.
         */
        this.createOutputAreaWidget = () => {
            // Add dockpanel wrapper for output area
            this.dockPanel = new ui_components_1.DockPanelSvg({ tabsMovable: false });
            widgets_1.Widget.attach(this.dockPanel, document.body);
            window.addEventListener('resize', () => {
                var _a;
                (_a = this.dockPanel) === null || _a === void 0 ? void 0 : _a.fit();
            });
            // Create output area widget
            const model = new outputarea_1.OutputAreaModel();
            const renderMimeRegistry = new rendermime_1.RenderMimeRegistry({ initialFactories: rendermime_1.standardRendererFactories });
            this.outputAreaWidget = new outputarea_1.OutputArea({
                rendermime: renderMimeRegistry,
                model
            });
            this.outputAreaWidget.addClass(OUTPUT_AREA_CLASS);
            const layout = this.layout;
            // TODO: Investigate SplitLayout instead of BoxLayout, for layout resizing functionality
            // const layout = this.layout as SplitLayout;
            layout.addWidget(this.dockPanel);
        };
        /**
         * Function: Clears existing output area and runs script
         * code from file editor in the selected kernel context.
         */
        this.runScript = () => __awaiter(this, void 0, void 0, function* () {
            var _c, _d;
            if (!this.runDisabled) {
                this.kernelName = (_d = (_c = this.kernelSelectorRef) === null || _c === void 0 ? void 0 : _c.current) === null || _d === void 0 ? void 0 : _d.getSelection();
                this.resetOutputArea();
                this.kernelName && this.displayOutputArea();
                yield this.runner.runScript(this.kernelName, this.context.path, this.model.value.text, this.handleKernelMsg);
            }
        });
        this.stopRun = () => __awaiter(this, void 0, void 0, function* () {
            var _e;
            yield this.runner.shutdownSession();
            if (!((_e = this.dockPanel) === null || _e === void 0 ? void 0 : _e.isEmpty)) {
                this.updatePromptText(' ');
            }
        });
        this.disableRun = (disabled) => {
            this.runDisabled = disabled;
            document.querySelector('#' + this.id + ' .' + RUN_BUTTON_CLASS).disabled = disabled;
        };
        /**
         * Function: Clears existing output area.
         */
        this.resetOutputArea = () => {
            var _a, _b, _c;
            // TODO: hide this.layout(), or set its height to 0
            (_a = this.dockPanel) === null || _a === void 0 ? void 0 : _a.hide();
            (_b = this.outputAreaWidget) === null || _b === void 0 ? void 0 : _b.model.clear();
            (_c = this.outputAreaWidget) === null || _c === void 0 ? void 0 : _c.removeClass(OUTPUT_AREA_ERROR_CLASS); // if no error class is found, command is ignored
        };
        /**
         * Function: Call back function passed to runner, that handles messages coming from the kernel.
         */
        this.handleKernelMsg = (msg) => __awaiter(this, void 0, void 0, function* () {
            let output = '';
            if (msg.status) {
                this.displayKernelStatus(msg.status);
                return;
            }
            else if (msg.error) {
                output = 'Error : ' + msg.error.type + ' - ' + msg.error.output;
                this.getOutputAreaChildWidget().addClass(OUTPUT_AREA_ERROR_CLASS);
            }
            else if (msg.output) {
                output = msg.output;
            }
            this.displayOutput(output);
        });
        this.createScrollButtons = (scrollingWidget) => {
            var _a, _b;
            const scrollUpButton = document.createElement('button');
            const scrollDownButton = document.createElement('button');
            scrollUpButton.className = 'elyra-ScriptEditor-scrollTop';
            scrollDownButton.className = 'elyra-ScriptEditor-scrollBottom';
            scrollUpButton.onclick = function () {
                scrollingWidget.node.scrollTop = 0;
            };
            scrollDownButton.onclick = function () {
                scrollingWidget.node.scrollTop = scrollingWidget.node.scrollHeight;
            };
            ui_components_1.caretUpEmptyThinIcon.element({
                container: scrollUpButton,
                elementPosition: 'center',
                title: 'Top'
            });
            ui_components_1.caretDownEmptyThinIcon.element({
                container: scrollDownButton,
                elementPosition: 'center',
                title: 'Bottom'
            });
            (_a = this.dockPanel) === null || _a === void 0 ? void 0 : _a.node.appendChild(scrollUpButton);
            (_b = this.dockPanel) === null || _b === void 0 ? void 0 : _b.node.appendChild(scrollDownButton);
        };
        /**
         * Function: Displays output area widget.
         */
        this.displayOutputArea = () => {
            var _a, _b, _c, _d;
            if (this.outputAreaWidget === undefined) {
                return;
            }
            (_a = this.dockPanel) === null || _a === void 0 ? void 0 : _a.show();
            // TODO: Set layout height to be flexible
            if (this.dockPanel !== undefined) {
                widgets_1.BoxLayout.setStretch(this.dockPanel, 1);
            }
            if ((_b = this.dockPanel) === null || _b === void 0 ? void 0 : _b.isEmpty) {
                // Add a tab to dockPanel
                this.scrollingWidget = new logconsole_1.ScrollingWidget({
                    content: this.outputAreaWidget
                });
                this.createScrollButtons(this.scrollingWidget);
                (_c = this.dockPanel) === null || _c === void 0 ? void 0 : _c.addWidget(this.scrollingWidget, { mode: 'split-bottom' });
                const outputTab = (_d = this.dockPanel) === null || _d === void 0 ? void 0 : _d.tabBars().next();
                if (outputTab !== undefined) {
                    outputTab.id = 'tab-ScriptEditor-output';
                    if (outputTab.currentTitle !== null) {
                        outputTab.currentTitle.label = 'Console Output';
                        outputTab.currentTitle.closable = true;
                    }
                    outputTab.disposed.connect((sender, args) => {
                        this.stopRun();
                        this.resetOutputArea();
                    }, this);
                }
            }
            const options = {
                name: 'stdout',
                output_type: 'stream',
                text: ['Waiting for kernel to start...']
            };
            this.outputAreaWidget.model.add(options);
            this.updatePromptText(' ');
            this.setOutputAreaClasses();
        };
        /**
         * Function: Displays kernel status, similar to notebook.
         */
        this.displayKernelStatus = (status) => {
            if (status === 'busy') {
                // TODO: Use a character that does not take any space, also not an empty string
                this.emptyOutput = true;
                this.displayOutput(' ');
                this.updatePromptText('*');
            }
            else if (status === 'idle') {
                this.updatePromptText(' ');
            }
        };
        /**
         * Function: Displays python code in OutputArea widget.
         */
        this.displayOutput = (output) => {
            var _a, _b, _c, _d;
            if (output) {
                const options = {
                    name: 'stdout',
                    output_type: 'stream',
                    text: [output]
                };
                // Stream output doesn't instantiate correctly without an initial output string
                if (this.emptyOutput) {
                    // Clears the "Waiting for kernel" message immediately
                    (_a = this.outputAreaWidget) === null || _a === void 0 ? void 0 : _a.model.clear(false);
                    (_b = this.outputAreaWidget) === null || _b === void 0 ? void 0 : _b.model.add(options);
                    this.emptyOutput = false;
                    // Clear will wait until the first output from the kernel to clear the initial string
                    (_c = this.outputAreaWidget) === null || _c === void 0 ? void 0 : _c.model.clear(true);
                }
                else {
                    (_d = this.outputAreaWidget) === null || _d === void 0 ? void 0 : _d.model.add(options);
                }
                this.updatePromptText('*');
                this.setOutputAreaClasses();
            }
        };
        this.setOutputAreaClasses = () => {
            this.getOutputAreaChildWidget().addClass(OUTPUT_AREA_CHILD_CLASS);
            this.getOutputAreaOutputWidget().addClass(OUTPUT_AREA_OUTPUT_CLASS);
            this.getOutputAreaPromptWidget().addClass(OUTPUT_AREA_PROMPT_CLASS);
        };
        /**
         * Function: Gets OutputArea child widget, where output and kernel status are displayed.
         */
        this.getOutputAreaChildWidget = () => {
            var _a;
            const outputAreaChildLayout = (_a = this.outputAreaWidget) === null || _a === void 0 ? void 0 : _a.layout;
            return outputAreaChildLayout.widgets[0];
        };
        /**
         * Function: Gets OutputArea prompt widget, where kernel status is displayed.
         */
        this.getOutputAreaOutputWidget = () => {
            const outputAreaChildLayout = this.getOutputAreaChildWidget()
                .layout;
            return outputAreaChildLayout.widgets[1];
        };
        /**
         * Function: Gets OutputArea prompt widget, where kernel status is displayed.
         */
        this.getOutputAreaPromptWidget = () => {
            const outputAreaChildLayout = this.getOutputAreaChildWidget()
                .layout;
            return outputAreaChildLayout.widgets[0];
        };
        /**
         * Function: Updates OutputArea prompt widget to display kernel status.
         */
        this.updatePromptText = (kernelStatusFlag) => {
            this.getOutputAreaPromptWidget().node.innerText =
                '[' + kernelStatusFlag + ']:';
        };
        /**
         * Function: Saves file editor content.
         */
        this.saveFile = () => __awaiter(this, void 0, void 0, function* () {
            if (this.model.readOnly) {
                return apputils_1.showDialog({
                    title: 'Cannot Save',
                    body: 'Document is read-only',
                    buttons: [apputils_1.Dialog.okButton()]
                });
            }
            void this.context.save().then(() => {
                if (!this.isDisposed) {
                    return this.context.createCheckpoint();
                }
                return;
            });
        });
        this.addClass(SCRIPT_EDITOR_CLASS);
        this.model = this.content.model;
        this.runner = new ScriptRunner_1.ScriptRunner(this.disableRun);
        this.kernelSelectorRef = null;
        this.kernelName = '';
        this.emptyOutput = true;
        this.runDisabled = false;
        this.controller = new ScriptEditorController_1.ScriptEditorController();
        // Add icon to main tab
        this.title.icon = this.getIcon();
        // Add toolbar widgets
        const saveButton = new apputils_1.ToolbarButton({
            icon: ui_components_1.saveIcon,
            onClick: this.saveFile,
            tooltip: 'Save file contents'
        });
        const runButton = new apputils_1.ToolbarButton({
            className: RUN_BUTTON_CLASS,
            icon: ui_components_1.runIcon,
            onClick: this.runScript,
            tooltip: 'Run'
        });
        const stopButton = new apputils_1.ToolbarButton({
            icon: ui_components_1.stopIcon,
            onClick: this.stopRun,
            tooltip: 'Stop'
        });
        // Populate toolbar with button widgets
        const toolbar = this.toolbar;
        toolbar.addItem('save', saveButton);
        toolbar.addItem('run', runButton);
        toolbar.addItem('stop', stopButton);
        this.toolbar.addClass(TOOLBAR_CLASS);
        // Create output area widget
        this.createOutputAreaWidget();
        this.context.ready.then(() => {
            this.initializeKernelSpecs();
        });
    }
}
exports.ScriptEditor = ScriptEditor;
//# sourceMappingURL=ScriptEditor.js.map

/***/ }),

/***/ "../script-editor/lib/ScriptEditorController.js":
/*!******************************************************!*\
  !*** ../script-editor/lib/ScriptEditorController.js ***!
  \******************************************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {


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
exports.ScriptEditorController = void 0;
const services_1 = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services");
class ScriptEditorController {
    constructor() {
        /**
         * Get available kernelspecs.
         */
        this.getKernelSpecs = () => __awaiter(this, void 0, void 0, function* () {
            yield this.kernelSpecManager.ready;
            const kernelSpecs = yield this.kernelSpecManager.specs;
            return kernelSpecs;
        });
        /**
         * Get available kernelspecs by language.
         */
        this.getKernelSpecsByLanguage = (language) => __awaiter(this, void 0, void 0, function* () {
            var _a;
            const specs = yield this.getKernelSpecs();
            Object.entries((_a = specs === null || specs === void 0 ? void 0 : specs.kernelspecs) !== null && _a !== void 0 ? _a : [])
                .filter(entry => { var _a; return ((_a = entry[1]) === null || _a === void 0 ? void 0 : _a.language.includes(language)) === false; })
                .forEach(entry => specs === null || specs === void 0 ? true : delete specs.kernelspecs[entry[0]]);
            return specs;
        });
        this.kernelSpecManager = new services_1.KernelSpecManager();
    }
}
exports.ScriptEditorController = ScriptEditorController;
//# sourceMappingURL=ScriptEditorController.js.map

/***/ }),

/***/ "../script-editor/lib/ScriptEditorWidgetFactory.js":
/*!*********************************************************!*\
  !*** ../script-editor/lib/ScriptEditorWidgetFactory.js ***!
  \*********************************************************/
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {


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
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.ScriptEditorWidgetFactory = void 0;
const docregistry_1 = __webpack_require__(/*! @jupyterlab/docregistry */ "webpack/sharing/consume/default/@jupyterlab/docregistry");
const fileeditor_1 = __webpack_require__(/*! @jupyterlab/fileeditor */ "webpack/sharing/consume/default/@jupyterlab/fileeditor");
/**
 * A widget factory for script editors.
 */
class ScriptEditorWidgetFactory extends docregistry_1.ABCWidgetFactory {
    /**
     * Construct a new editor widget factory.
     */
    constructor(options) {
        super(options.factoryOptions);
        this._services = options.editorServices;
        this.options = options;
    }
    /**
     * Create a new widget given a context.
     */
    createNewWidget(context) {
        const newDocumentEditor = this._services.factoryService.newDocumentEditor;
        const factory = options => {
            return newDocumentEditor(options);
        };
        const content = new fileeditor_1.FileEditor({
            factory,
            context,
            mimeTypeService: this._services.mimeTypeService
        });
        return this.options.instanceCreator({ content, context });
    }
}
exports.ScriptEditorWidgetFactory = ScriptEditorWidgetFactory;
//# sourceMappingURL=ScriptEditorWidgetFactory.js.map

/***/ }),

/***/ "../script-editor/lib/ScriptRunner.js":
/*!********************************************!*\
  !*** ../script-editor/lib/ScriptRunner.js ***!
  \********************************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {


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
exports.ScriptRunner = void 0;
const apputils_1 = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
const services_1 = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services");
const KERNEL_ERROR_MSG = 'Could not run script because no supporting kernel is defined.';
const SESSION_ERROR_MSG = 'Could not start session to execute script.';
/**
 * Utility class to enable running scripts files in the context of a Kernel environment
 */
class ScriptRunner {
    /**
     * Construct a new runner.
     */
    constructor(disableRun) {
        this.errorDialog = (errorMsg) => {
            this.disableRun(false);
            return apputils_1.showDialog({
                title: 'Error',
                body: errorMsg,
                buttons: [apputils_1.Dialog.okButton()]
            });
        };
        /**
         * Function: Starts a session with a proper kernel and executes code from file editor.
         */
        this.runScript = (kernelName, contextPath, code, handleKernelMsg) => __awaiter(this, void 0, void 0, function* () {
            var _a;
            if (!kernelName) {
                this.disableRun(true);
                return this.errorDialog(KERNEL_ERROR_MSG);
            }
            if (!this.sessionConnection) {
                this.disableRun(true);
                try {
                    yield this.startSession(kernelName, contextPath);
                }
                catch (e) {
                    return this.errorDialog(SESSION_ERROR_MSG);
                }
                // This is a bit weird, seems like typescript doesn't believe that `startSession`
                // can set `sessionConnection`
                this.sessionConnection = this
                    .sessionConnection;
                if (!((_a = this.sessionConnection) === null || _a === void 0 ? void 0 : _a.kernel)) {
                    // session didn't get started
                    return this.errorDialog(SESSION_ERROR_MSG);
                }
                const future = this.sessionConnection.kernel.requestExecute({ code });
                future.onIOPub = (msg) => {
                    const msgOutput = {};
                    if (msg.msg_type === 'error') {
                        msgOutput.error = {
                            type: msg.content.ename,
                            output: msg.content.evalue
                        };
                    }
                    else if (msg.msg_type === 'execute_result' ||
                        msg.msg_type === 'display_data') {
                        if ('text/plain' in msg.content.data) {
                            msgOutput.output = msg.content.data['text/plain'];
                        }
                        else {
                            // ignore
                            console.log('Ignoring received message ' + msg);
                        }
                    }
                    else if (msg.msg_type === 'stream') {
                        msgOutput.output = msg.content.text;
                    }
                    else if (msg.msg_type === 'status') {
                        msgOutput.status = msg.content.execution_state;
                    }
                    else {
                        // ignore other message types
                    }
                    // Notify UI
                    handleKernelMsg(msgOutput);
                };
                try {
                    yield future.done;
                    this.shutdownSession();
                }
                catch (e) {
                    console.log('Exception: done = ' + JSON.stringify(e));
                }
            }
        });
        /**
         * Function: Starts new kernel.
         */
        this.startSession = (kernelName, contextPath) => __awaiter(this, void 0, void 0, function* () {
            const options = {
                kernel: {
                    name: kernelName
                },
                path: contextPath,
                type: 'file',
                name: contextPath
            };
            this.sessionConnection = yield this.sessionManager.startNew(options);
            this.sessionConnection.setPath(contextPath);
            return this.sessionConnection;
        });
        /**
         * Function: Shuts down kernel.
         */
        this.shutdownSession = () => __awaiter(this, void 0, void 0, function* () {
            var _b;
            if (this.sessionConnection) {
                const name = (_b = this.sessionConnection.kernel) === null || _b === void 0 ? void 0 : _b.name;
                try {
                    this.disableRun(false);
                    yield this.sessionConnection.shutdown();
                    this.sessionConnection = null;
                    console.log(name + ' kernel shut down');
                }
                catch (e) {
                    console.log('Exception: shutdown = ' + JSON.stringify(e));
                }
            }
        });
        this.disableRun = disableRun;
        this.kernelSpecManager = new services_1.KernelSpecManager();
        this.kernelManager = new services_1.KernelManager();
        this.sessionManager = new services_1.SessionManager({
            kernelManager: this.kernelManager
        });
        this.sessionConnection = null;
    }
}
exports.ScriptRunner = ScriptRunner;
//# sourceMappingURL=ScriptRunner.js.map

/***/ }),

/***/ "../script-editor/lib/index.js":
/*!*************************************!*\
  !*** ../script-editor/lib/index.js ***!
  \*************************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {


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
__webpack_require__(/*! ../style/index.css */ "../script-editor/style/index.css");
__exportStar(__webpack_require__(/*! ./KernelDropdown */ "../script-editor/lib/KernelDropdown.js"), exports);
__exportStar(__webpack_require__(/*! ./ScriptEditor */ "../script-editor/lib/ScriptEditor.js"), exports);
__exportStar(__webpack_require__(/*! ./ScriptEditorController */ "../script-editor/lib/ScriptEditorController.js"), exports);
__exportStar(__webpack_require__(/*! ./ScriptRunner */ "../script-editor/lib/ScriptRunner.js"), exports);
__exportStar(__webpack_require__(/*! ./ScriptEditorWidgetFactory */ "../script-editor/lib/ScriptEditorWidgetFactory.js"), exports);
//# sourceMappingURL=index.js.map

/***/ })

}]);
//# sourceMappingURL=script-editor_lib_index_js.2129dc49191b9803ee39.js.map
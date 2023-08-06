"use strict";
(self["webpackChunk_elyra_theme_extension"] = self["webpackChunk_elyra_theme_extension"] || []).push([["lib_index_js"],{

/***/ "../../node_modules/css-loader/dist/cjs.js!./style/index.css":
/*!*******************************************************************!*\
  !*** ../../node_modules/css-loader/dist/cjs.js!./style/index.css ***!
  \*******************************************************************/
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
___CSS_LOADER_EXPORT___.push([module.id, "/*\n * Copyright 2018-2022 Elyra Authors\n *\n * Licensed under the Apache License, Version 2.0 (the \"License\");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n * http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an \"AS IS\" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n */\n\n.jp-LabShell {\n  background: var(--jp-layout-color3);\n}\n", "",{"version":3,"sources":["webpack://./style/index.css"],"names":[],"mappings":"AAAA;;;;;;;;;;;;;;EAcE;;AAEF;EACE,mCAAmC;AACrC","sourcesContent":["/*\n * Copyright 2018-2022 Elyra Authors\n *\n * Licensed under the Apache License, Version 2.0 (the \"License\");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n * http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an \"AS IS\" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n */\n\n.jp-LabShell {\n  background: var(--jp-layout-color3);\n}\n"],"sourceRoot":""}]);
// Exports
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (___CSS_LOADER_EXPORT___);


/***/ }),

/***/ "./style/index.css":
/*!*************************!*\
  !*** ./style/index.css ***!
  \*************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! !../../../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js */ "../../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_css_loader_dist_cjs_js_index_css__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! !!../../../node_modules/css-loader/dist/cjs.js!./index.css */ "../../node_modules/css-loader/dist/cjs.js!./style/index.css");

            

var options = {};

options.insert = "head";
options.singleton = false;

var update = _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default()(_node_modules_css_loader_dist_cjs_js_index_css__WEBPACK_IMPORTED_MODULE_1__["default"], options);



/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (_node_modules_css_loader_dist_cjs_js_index_css__WEBPACK_IMPORTED_MODULE_1__["default"].locals || {});

/***/ }),

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
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
const ui_components_1 = __webpack_require__(/*! @elyra/ui-components */ "webpack/sharing/consume/default/@elyra/ui-components/@elyra/ui-components");
const application_1 = __webpack_require__(/*! @jupyterlab/application */ "webpack/sharing/consume/default/@jupyterlab/application");
const apputils_1 = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
const launcher_1 = __webpack_require__(/*! @jupyterlab/launcher */ "webpack/sharing/consume/default/@jupyterlab/launcher");
const mainmenu_1 = __webpack_require__(/*! @jupyterlab/mainmenu */ "webpack/sharing/consume/default/@jupyterlab/mainmenu");
const translation_1 = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation");
const ui_components_2 = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
const algorithm_1 = __webpack_require__(/*! @lumino/algorithm */ "webpack/sharing/consume/default/@lumino/algorithm");
const launcher_2 = __webpack_require__(/*! ./launcher */ "./lib/launcher.js");
__webpack_require__(/*! ../style/index.css */ "./style/index.css");
const ELYRA_THEME_NAMESPACE = 'elyra-theme-extension';
/**
 * The command IDs used by the launcher plugin.
 */
const CommandIDs = {
    create: 'launcher:create',
    openHelp: 'elyra:open-help'
};
/**
 * Initialization data for the theme extension.
 */
const extension = {
    id: ELYRA_THEME_NAMESPACE,
    autoStart: true,
    requires: [translation_1.ITranslator, application_1.ILabShell, mainmenu_1.IMainMenu],
    optional: [apputils_1.ICommandPalette],
    provides: launcher_1.ILauncher,
    activate: (app, translator, labShell, mainMenu, palette) => {
        console.log('Elyra - theme extension is activated!');
        // Find the MainLogo widget in the shell and replace it with the Elyra Logo
        const widgets = app.shell.widgets('top');
        let widget = widgets.next();
        while (widget !== undefined) {
            if (widget.id === 'jp-MainLogo') {
                ui_components_1.elyraIcon.element({
                    container: widget.node,
                    justify: 'center',
                    margin: '2px 5px 2px 5px',
                    height: 'auto',
                    width: '20px'
                });
                break;
            }
            widget = widgets.next();
        }
        // Use custom Elyra launcher
        const { commands, shell } = app;
        const trans = translator.load('jupyterlab');
        const model = new launcher_2.LauncherModel();
        commands.addCommand(CommandIDs.create, {
            label: trans.__('New Launcher'),
            execute: (args) => {
                const cwd = args['cwd'] ? String(args['cwd']) : '';
                const id = `launcher-${Private.id++}`;
                const callback = (item) => {
                    labShell.add(item, 'main', { ref: id });
                };
                const launcher = new launcher_2.Launcher({
                    model,
                    cwd,
                    callback,
                    commands,
                    translator
                });
                launcher.model = model;
                launcher.title.icon = ui_components_2.launcherIcon;
                launcher.title.label = trans.__('Launcher');
                const main = new apputils_1.MainAreaWidget({ content: launcher });
                // If there are any other widgets open, remove the launcher close icon.
                main.title.closable = !!algorithm_1.toArray(labShell.widgets('main')).length;
                main.id = id;
                shell.add(main, 'main', {
                    activate: args['activate'],
                    ref: args['ref']
                });
                labShell.layoutModified.connect(() => {
                    // If there is only a launcher open, remove the close icon.
                    main.title.closable = algorithm_1.toArray(labShell.widgets('main')).length > 1;
                }, main);
                return main;
            }
        });
        if (palette) {
            palette.addItem({
                command: CommandIDs.create,
                category: trans.__('Launcher')
            });
        }
        if (labShell) {
            labShell.addButtonEnabled = true;
            labShell.addRequested.connect((sender, arg) => {
                var _a;
                // Get the ref for the current tab of the tabbar which the add button was clicked
                const ref = ((_a = arg.currentTitle) === null || _a === void 0 ? void 0 : _a.owner.id) ||
                    arg.titles[arg.titles.length - 1].owner.id;
                if (commands.hasCommand('filebrowser:create-main-launcher')) {
                    // If a file browser is defined connect the launcher to it
                    return commands.execute('filebrowser:create-main-launcher', {
                        ref
                    });
                }
                return commands.execute(CommandIDs.create, { ref });
            });
        }
        commands.addCommand(CommandIDs.openHelp, {
            label: 'Documentation',
            icon: ui_components_1.helpIcon,
            execute: (args) => {
                window.open('https://elyra.readthedocs.io/en/v3.9.0rc2/', '_blank');
            }
        });
        model.add({
            command: CommandIDs.openHelp,
            category: 'Elyra',
            rank: 10
        });
        return model;
    }
};
/**
 * The namespace for module private data.
 */
var Private;
(function (Private) {
    /**
     * The incrementing id used for launcher widgets.
     */
    // eslint-disable-next-line
    Private.id = 0;
})(Private || (Private = {}));
exports["default"] = extension;
//# sourceMappingURL=index.js.map

/***/ }),

/***/ "./lib/launcher.js":
/*!*************************!*\
  !*** ./lib/launcher.js ***!
  \*************************/
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
exports.Launcher = exports.LauncherModel = void 0;
const ui_components_1 = __webpack_require__(/*! @elyra/ui-components */ "webpack/sharing/consume/default/@elyra/ui-components/@elyra/ui-components");
const launcher_1 = __webpack_require__(/*! @jupyterlab/launcher */ "webpack/sharing/consume/default/@jupyterlab/launcher");
const algorithm_1 = __webpack_require__(/*! @lumino/algorithm */ "webpack/sharing/consume/default/@lumino/algorithm");
const React = __importStar(__webpack_require__(/*! react */ "webpack/sharing/consume/default/react"));
/**
 * The known categories of launcher items and their default ordering.
 */
const ELYRA_CATEGORY = 'Elyra';
const CommandIDs = {
    newFile: 'fileeditor:create-new',
    createNewPythonEditor: 'script-editor:create-new-python-editor',
    createNewREditor: 'script-editor:create-new-r-editor'
};
class LauncherModel extends launcher_1.LauncherModel {
    /**
     * Return an iterator of launcher items, but remove unnecessary items.
     */
    items() {
        const items = [];
        let pyEditorInstalled = false;
        let rEditorInstalled = false;
        this.itemsList.forEach(item => {
            if (item.command === CommandIDs.createNewPythonEditor) {
                pyEditorInstalled = true;
            }
            else if (item.command === CommandIDs.createNewREditor) {
                rEditorInstalled = true;
            }
        });
        if (!pyEditorInstalled && !rEditorInstalled) {
            return new algorithm_1.ArrayIterator(this.itemsList);
        }
        // Dont add tiles for new py and r files if their script editor is installed
        this.itemsList.forEach(item => {
            var _a, _b;
            if (!(item.command === CommandIDs.newFile &&
                ((pyEditorInstalled && ((_a = item.args) === null || _a === void 0 ? void 0 : _a.fileExt) === 'py') ||
                    (rEditorInstalled && ((_b = item.args) === null || _b === void 0 ? void 0 : _b.fileExt) === 'r')))) {
                items.push(item);
            }
        });
        return new algorithm_1.ArrayIterator(items);
    }
}
exports.LauncherModel = LauncherModel;
class Launcher extends launcher_1.Launcher {
    /**
     * Construct a new launcher widget.
     */
    constructor(options) {
        super(options);
        this._translator = this.translator.load('jupyterlab');
    }
    replaceCategoryIcon(category, icon) {
        const children = React.Children.map(category.props.children, child => {
            if (child.props.className === 'jp-Launcher-sectionHeader') {
                const grandchildren = React.Children.map(child.props.children, grandchild => {
                    if (grandchild.props.className !== 'jp-Launcher-sectionTitle') {
                        return React.createElement(icon.react, { stylesheet: "launcherSection" });
                    }
                    else {
                        return grandchild;
                    }
                });
                return React.cloneElement(child, child.props, grandchildren);
            }
            else {
                return child;
            }
        });
        return React.cloneElement(category, category.props, children);
    }
    /**
     * Render the launcher to virtual DOM nodes.
     */
    render() {
        // Bail if there is no model.
        if (!this.model) {
            return null;
        }
        // get the rendering from JupyterLab Launcher
        // and resort the categories
        const launcherBody = super.render();
        const launcherContent = launcherBody === null || launcherBody === void 0 ? void 0 : launcherBody.props.children;
        const launcherCategories = launcherContent.props.children;
        const categories = [];
        const knownCategories = [
            this._translator.__('Notebook'),
            this._translator.__('Console'),
            ELYRA_CATEGORY,
            this._translator.__('Other')
        ];
        // Assemble the final ordered list of categories
        // based on knownCategories.
        algorithm_1.each(knownCategories, (category, index) => {
            React.Children.forEach(launcherCategories, cat => {
                if (cat.key === category) {
                    if (cat.key === ELYRA_CATEGORY) {
                        cat = this.replaceCategoryIcon(cat, ui_components_1.elyraIcon);
                    }
                    categories.push(cat);
                }
            });
        });
        // Wrap the sections in body and content divs.
        return (React.createElement("div", { className: "jp-Launcher-body" },
            React.createElement("div", { className: "jp-Launcher-content" },
                React.createElement("div", { className: "jp-Launcher-cwd" },
                    React.createElement("h3", null, this.cwd)),
                categories)));
    }
}
exports.Launcher = Launcher;
//# sourceMappingURL=launcher.js.map

/***/ })

}]);
//# sourceMappingURL=lib_index_js.fd976f24445e851bd205.js.map
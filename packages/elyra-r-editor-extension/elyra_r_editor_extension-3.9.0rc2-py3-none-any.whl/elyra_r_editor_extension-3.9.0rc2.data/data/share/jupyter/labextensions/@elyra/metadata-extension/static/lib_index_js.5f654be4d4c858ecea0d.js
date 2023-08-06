"use strict";
(self["webpackChunk_elyra_metadata_extension"] = self["webpackChunk_elyra_metadata_extension"] || []).push([["lib_index_js"],{

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
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
const metadata_common_1 = __webpack_require__(/*! @elyra/metadata-common */ "webpack/sharing/consume/default/@elyra/metadata-common/@elyra/metadata-common");
const services_1 = __webpack_require__(/*! @elyra/services */ "webpack/sharing/consume/default/@elyra/services/@elyra/services");
const ui_components_1 = __webpack_require__(/*! @elyra/ui-components */ "../ui-components/lib/index.js");
const application_1 = __webpack_require__(/*! @jupyterlab/application */ "webpack/sharing/consume/default/@jupyterlab/application");
const apputils_1 = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
const codeeditor_1 = __webpack_require__(/*! @jupyterlab/codeeditor */ "webpack/sharing/consume/default/@jupyterlab/codeeditor");
const translation_1 = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation");
const ui_components_2 = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
const algorithm_1 = __webpack_require__(/*! @lumino/algorithm */ "webpack/sharing/consume/default/@lumino/algorithm");
const METADATA_EDITOR_ID = 'elyra-metadata-editor';
const METADATA_WIDGET_ID = 'elyra-metadata';
const commandIDs = {
    openMetadata: 'elyra-metadata:open',
    closeTabCommand: 'elyra-metadata:close'
};
/**
 * Initialization data for the metadata-extension extension.
 */
const extension = {
    id: METADATA_WIDGET_ID,
    autoStart: true,
    requires: [
        apputils_1.ICommandPalette,
        codeeditor_1.IEditorServices,
        application_1.ILabStatus,
        ui_components_2.IFormComponentRegistry,
        translation_1.ITranslator
    ],
    optional: [apputils_1.IThemeManager],
    activate: (app, palette, editorServices, status, componentRegistry, translator, themeManager) => __awaiter(void 0, void 0, void 0, function* () {
        console.log('Elyra - metadata extension is activated!');
        componentRegistry.addRenderer('code', ui_components_1.CodeBlock);
        componentRegistry.addRenderer('tags', ui_components_1.TagsField);
        componentRegistry.addRenderer('dropdown', ui_components_1.DropDown);
        componentRegistry.addRenderer('password', ui_components_1.PasswordField);
        const openMetadataEditor = (args) => {
            let widgetLabel;
            if (args.name) {
                widgetLabel = args.name;
            }
            else {
                widgetLabel = `New ${args.schema}`;
            }
            const widgetId = `${METADATA_EDITOR_ID}:${args.schemaspace}:${args.schema}:${args.name ? args.name : 'new'}`;
            const openWidget = algorithm_1.find(app.shell.widgets('main'), (widget, index) => {
                return widget.id === widgetId;
            });
            if (openWidget) {
                app.shell.activateById(widgetId);
                return;
            }
            const metadataEditorWidget = new metadata_common_1.MetadataEditorWidget(Object.assign(Object.assign({}, args), { schemaName: args.schema, editorServices,
                status,
                themeManager, translator: translator.load('jupyterlab'), componentRegistry }));
            const main = new apputils_1.MainAreaWidget({ content: metadataEditorWidget });
            main.title.label = widgetLabel;
            main.id = widgetId;
            main.title.closable = true;
            main.title.icon = ui_components_2.textEditorIcon;
            main.addClass(METADATA_EDITOR_ID);
            app.shell.add(main, 'main');
        };
        app.commands.addCommand(`${METADATA_EDITOR_ID}:open`, {
            execute: (args) => {
                openMetadataEditor(args);
            }
        });
        const openMetadataWidget = (args) => {
            const labIcon = ui_components_2.LabIcon.resolve({ icon: args.icon });
            const widgetId = `${METADATA_WIDGET_ID}:${args.schemaspace}`;
            const metadataWidget = new metadata_common_1.MetadataWidget({
                app,
                themeManager,
                display_name: args.display_name,
                schemaspace: args.schemaspace,
                icon: labIcon
            });
            metadataWidget.id = widgetId;
            metadataWidget.title.icon = labIcon;
            metadataWidget.title.caption = args.display_name;
            if (algorithm_1.find(app.shell.widgets('left'), value => value.id === widgetId) ===
                undefined) {
                app.shell.add(metadataWidget, 'left', { rank: 1000 });
            }
            app.shell.activateById(widgetId);
        };
        const openMetadataCommand = commandIDs.openMetadata;
        app.commands.addCommand(openMetadataCommand, {
            label: (args) => args['label'],
            execute: (args) => {
                // Rank has been chosen somewhat arbitrarily to give priority
                // to the running sessions widget in the sidebar.
                openMetadataWidget(args);
            }
        });
        // Add command to close metadata tab
        const closeTabCommand = commandIDs.closeTabCommand;
        app.commands.addCommand(closeTabCommand, {
            label: 'Close Tab',
            execute: args => {
                const contextNode = app.contextMenuHitTest(node => !!node.dataset.id);
                if (contextNode) {
                    const id = contextNode.dataset['id'];
                    const widget = algorithm_1.find(app.shell.widgets('left'), (widget, index) => {
                        return widget.id === id;
                    });
                    if (widget) {
                        widget.dispose();
                    }
                }
            }
        });
        app.contextMenu.addItem({
            selector: '[data-id^="elyra-metadata:"]:not([data-id$="code-snippets"]):not([data-id$="runtimes"])',
            command: closeTabCommand
        });
        try {
            const schemas = yield services_1.MetadataService.getAllSchema();
            for (const schema of schemas) {
                let icon = 'ui-components:text-editor';
                let title = schema.title;
                if (schema.uihints) {
                    if (schema.uihints.icon) {
                        icon = schema.uihints.icon;
                    }
                    if (schema.uihints.title) {
                        title = schema.uihints.title;
                    }
                }
                palette.addItem({
                    command: commandIDs.openMetadata,
                    args: {
                        label: `Manage ${title}`,
                        display_name: schema.uihints.title,
                        schemaspace: schema.schemaspace,
                        icon: icon
                    },
                    category: 'Elyra'
                });
            }
        }
        catch (error) {
            ui_components_1.RequestErrors.serverError(error);
        }
    })
};
exports["default"] = extension;
//# sourceMappingURL=index.js.map

/***/ })

}]);
//# sourceMappingURL=lib_index_js.5f654be4d4c858ecea0d.js.map
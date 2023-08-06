"use strict";
(self["webpackChunk_chameleoncloud_jupyterlab_chameleon"] = self["webpackChunk_chameleoncloud_jupyterlab_chameleon"] || []).push([["lib_index_js"],{

/***/ "./lib/artifact-sharing/filebrowser.js":
/*!*********************************************!*\
  !*** ./lib/artifact-sharing/filebrowser.js ***!
  \*********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "DirListingRenderer": () => (/* binding */ DirListingRenderer)
/* harmony export */ });
/* harmony import */ var _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/filebrowser */ "webpack/sharing/consume/default/@jupyterlab/filebrowser");
/* harmony import */ var _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_0__);

class DirListingRenderer extends _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_0__.DirListing.Renderer {
    constructor(artifactRegistry) {
        super();
        this._artifactRegistry = artifactRegistry;
    }
    populateHeaderNode(node) {
        super.populateHeaderNode(node);
        if (!this._headerIndicator) {
            this._headerIndicator = document.createElement('div');
            this._headerIndicator.className = 'chi-Something';
        }
    }
    updateItemNode(node, model, fileType) {
        super.updateItemNode(node, model, fileType);
        const artifact = this._artifactRegistry.getArtifactSync(model.path);
        if (artifact && artifact.uuid) {
            node.setAttribute('data-artifact-id', artifact.uuid);
            const artifactText = [
                `Artifact ID: ${artifact.uuid}`,
                `Artifact contents: ${artifact.versions[artifact.versions.length - 1].contents.urn}`,
                `Artifact ownership: ${artifact.ownership}`
            ].join('\n');
            node.title += `\n${artifactText}`;
        }
        else {
            delete node.dataset.artifactId;
        }
    }
}


/***/ }),

/***/ "./lib/artifact-sharing/index.js":
/*!***************************************!*\
  !*** ./lib/artifact-sharing/index.js ***!
  \***************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ArtifactSharingURL": () => (/* binding */ ArtifactSharingURL),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/application */ "webpack/sharing/consume/default/@jupyterlab/application");
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/docmanager */ "webpack/sharing/consume/default/@jupyterlab/docmanager");
/* harmony import */ var _jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/filebrowser */ "webpack/sharing/consume/default/@jupyterlab/filebrowser");
/* harmony import */ var _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_filebrowser_extension__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/filebrowser-extension */ "webpack/sharing/consume/default/@jupyterlab/filebrowser-extension");
/* harmony import */ var _jupyterlab_filebrowser_extension__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_filebrowser_extension__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @jupyterlab/mainmenu */ "webpack/sharing/consume/default/@jupyterlab/mainmenu");
/* harmony import */ var _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var _jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @jupyterlab/statedb */ "webpack/sharing/consume/default/@jupyterlab/statedb");
/* harmony import */ var _jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_7___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_7__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_8___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_8__);
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! @lumino/algorithm */ "webpack/sharing/consume/default/@lumino/algorithm");
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_9___default = /*#__PURE__*/__webpack_require__.n(_lumino_algorithm__WEBPACK_IMPORTED_MODULE_9__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_10___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_10__);
/* harmony import */ var _filebrowser__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! ./filebrowser */ "./lib/artifact-sharing/filebrowser.js");
/* harmony import */ var _registry__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! ./registry */ "./lib/artifact-sharing/registry.js");
/* harmony import */ var _tokens__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(/*! ./tokens */ "./lib/artifact-sharing/tokens.js");
/* harmony import */ var _widget__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(/*! ./widget */ "./lib/artifact-sharing/widget.js");















const PLUGIN_NAMESPACE = '@chameleoncloud/jupyterlab-chameleon';
const WIDGET_PLUGIN_ID = `${PLUGIN_NAMESPACE}:artifact-sharing`;
const FILE_BROWSER_PLUGIN_ID = `${PLUGIN_NAMESPACE}:file-browser-factory`;
const REGISTRY_PLUGIN_ID = `${PLUGIN_NAMESPACE}:artifact-registry`;
class ArtifactSharingURL {
    constructor(settings) {
        this._settings = settings;
    }
    indexUrl() {
        return this._baseUrl;
    }
    detailUrl(externalId) {
        return this._makeUrl('externalDetailEndpoint').replace('{externalId}', externalId);
    }
    createUrl(depositionId, depositionRepo) {
        return this._makeUrl('externalCreateEndpoint')
            .replace('{depositionId}', depositionId)
            .replace('{depositionRepo}', depositionRepo);
    }
    updateUrl(externalId) {
        return this._makeUrl('externalUpdateEndpoint').replace('{externalId}', externalId);
    }
    newVersionUrl(externalId, depositionId, depositionRepo) {
        return this._makeUrl('externalNewVersionEndpoint')
            .replace('{externalId}', externalId)
            .replace('{depositionId}', depositionId)
            .replace('{depositionRepo}', depositionRepo);
    }
    isExternalUrl(origin) {
        return this._baseUrl.indexOf(origin) === 0;
    }
    get _baseUrl() {
        return this._settings.get('externalBaseUrl').composite;
    }
    _makeUrl(endpoint) {
        const path = this._settings.get(endpoint).composite;
        return this._baseUrl + path;
    }
}
function createOpener(app, settings, tracker, artifactRegistry, browserHelper) {
    let widget;
    return async (workflow) => {
        const artifact = await browserHelper.currentItemArtifact();
        if (!widget || widget.isDisposed) {
            const urlFactory = new ArtifactSharingURL(settings);
            const content = new _widget__WEBPACK_IMPORTED_MODULE_14__.ArtifactSharingWidget(artifact, workflow, urlFactory, artifactRegistry);
            content.title.label =
                workflow === 'upload' ? 'Package artifact' : 'Edit artifact';
            widget = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.MainAreaWidget({ content });
            widget.id = 'artifact-sharing';
        }
        if (!widget.isAttached) {
            app.shell.add(widget, 'main');
        }
        if (!tracker.has(widget)) {
            await tracker.add(widget);
        }
        widget.update();
        app.shell.activateById(widget.id);
    };
}
const plugin = {
    id: WIDGET_PLUGIN_ID,
    requires: [
        _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_6__.ISettingRegistry,
        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ICommandPalette,
        _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILayoutRestorer,
        _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_5__.IMainMenu,
        _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_3__.IFileBrowserFactory,
        _tokens__WEBPACK_IMPORTED_MODULE_13__.IArtifactRegistry
    ],
    activate(app, settingRegistry, palette, restorer, mainMenu, fileBrowserFactory, artifactRegistry) {
        Promise.all([
            settingRegistry.load(WIDGET_PLUGIN_ID),
            app.restored,
            artifactRegistry.getArtifacts()
                .catch((err) => {
                console.error('Error fetching list of local artifacts, defaulting to empty list.');
                return [];
            })
        ])
            .then(async ([settings]) => {
            const browser = fileBrowserFactory.defaultBrowser;
            const tracker = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.WidgetTracker({
                namespace: 'artifact-sharing'
            });
            const browserHelper = new FileBrowserHelper(browser, artifactRegistry);
            const openWidget = createOpener(app, settings, tracker, artifactRegistry, browserHelper);
            const enableEdit = () => {
                const item = browserHelper.currentItem();
                return (browserHelper.canBeArtifact(item) &&
                    browserHelper.isOwnedArtifact(item));
            };
            const enableCreate = () => {
                const item = browserHelper.currentItem();
                return (browserHelper.canBeArtifact(item) &&
                    !browserHelper.isOwnedArtifact(item));
            };
            app.commands.addCommand(CommandIDs.create, {
                label: 'Package as new artifact',
                isEnabled: enableCreate,
                async execute() {
                    await openWidget('upload');
                }
            });
            app.commands.addCommand(CommandIDs.newVersion, {
                label: 'Create new artifact version',
                isEnabled: enableEdit,
                async execute() {
                    await openWidget('upload');
                }
            });
            app.commands.addCommand(CommandIDs.edit, {
                label: 'Edit artifact',
                isEnabled: enableEdit,
                async execute() {
                    await openWidget('edit');
                }
            });
            registerTopMenu(app, mainMenu);
            registerContextMenu(app);
            registerCommandPalette(palette);
            await restorer.restore(tracker, {
                command: CommandIDs.create,
                name: () => 'artifact-sharing'
            });
        })
            .catch((reason) => {
            console.trace();
            console.error(reason.message);
        });
    },
    autoStart: true
};
function registerTopMenu(app, mainMenu) {
    const menu = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_10__.Menu({ commands: app.commands });
    menu.addItem({ command: CommandIDs.create });
    menu.addItem({ command: CommandIDs.edit });
    menu.addItem({ command: CommandIDs.newVersion });
    menu.title.label = 'Share';
    mainMenu.addMenu(menu, { rank: 20 });
}
function registerCommandPalette(palette) {
    const category = 'Sharing';
    palette.addItem({ command: CommandIDs.create, category });
    palette.addItem({ command: CommandIDs.edit, category });
    palette.addItem({ command: CommandIDs.newVersion, category });
}
function registerContextMenu(app) {
    const selectorPublished = '.jp-DirListing-item[data-isdir=true][data-artifact-id]';
    const selectorNotPublished = '.jp-DirListing-item[data-isdir=true]:not([data-artifact-id])';
    app.contextMenu.addItem({
        command: CommandIDs.create,
        selector: selectorNotPublished,
        rank: 1
    });
    app.contextMenu.addItem({
        command: CommandIDs.edit,
        selector: selectorPublished,
        rank: 1
    });
    app.contextMenu.addItem({
        command: CommandIDs.newVersion,
        selector: selectorPublished,
        rank: 2
    });
}
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.create = 'artifact-sharing:create';
    CommandIDs.edit = 'artifact-sharing:edit';
    CommandIDs.newVersion = 'artifact-sharing:newVersion';
})(CommandIDs || (CommandIDs = {}));
class FileBrowserHelper {
    constructor(browser, artifactRegistry) {
        this._browser = browser;
        this._artifactRegistry = artifactRegistry;
    }
    canBeArtifact(item) {
        return item && item.type === 'directory';
    }
    isOwnedArtifact(item) {
        const artifact = this._artifactRegistry.getArtifactSync(item.path);
        return artifact && artifact.ownership === 'own';
    }
    async currentItemArtifact() {
        const item = this.currentItem();
        if (!item || item.type !== 'directory') {
            return null;
        }
        let artifact = await this._artifactRegistry.getArtifact(item.path);
        if (!artifact) {
            // Generate a new placeholder artifact for the given path.
            artifact = {
                title: "",
                short_description: "",
                authors: [],
                linked_projects: [],
                reproducibility: { enable_requests: false },
                tags: [],
                versions: [],
                newLinks: [],
                path: item.path,
                ownership: "fork"
            };
        }
        return artifact;
    }
    currentItem() {
        const selectedItems = (0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_9__.toArray)(this._browser.selectedItems());
        if (selectedItems.length > 1) {
            // Fail on multiple items selected
            return null;
        }
        else if (selectedItems.length === 1) {
            return selectedItems[0];
        }
        return this._fakeCurrentRootItem();
    }
    /**
     * Provides a fake Contents.IModel entity for the current directory the
     * browser model is on. The browser model does not supply this over a public
     * interface. For our purposes, we only really need the path anyways, so it
     * is OK. Additionally, the model is always simple as it must necessarily
     * be of type='directory'.
     */
    _fakeCurrentRootItem() {
        const { path } = this._browser.model;
        return {
            content: null,
            created: null,
            format: 'json',
            last_modified: null,
            mimetype: null,
            name: path,
            path,
            type: 'directory',
            writable: true
        };
    }
}
const fileBrowserFactoryPlugin = {
    id: FILE_BROWSER_PLUGIN_ID,
    provides: _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_3__.IFileBrowserFactory,
    requires: [_jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_2__.IDocumentManager, _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_8__.ITranslator, _tokens__WEBPACK_IMPORTED_MODULE_13__.IArtifactRegistry],
    optional: [_jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_7__.IStateDB, _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.IRouter, _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.JupyterFrontEnd.ITreeResolver],
    async activate(app, docManager, translator, artifactRegistry, state, router, tree) {
        // NOTE(jason): in order for us to have control over the rendering/styling
        // of the default JupyterLab file browser, we need control of the `renderer`
        // that is passed in to the FileBrowser widget. Unfortunately, this is not
        // surfaced to us in any easy way in JLab 2.x. But, the renderer does
        // default in any case I could find to `DirListing.defaultRenderer`. So, by
        // overriding that _before_ any widget that needs it is created, we can
        // get where we need to be.
        //
        // This factory plugin exists just so that we can defer the loading of the
        // file browser until after we shim the `defaultRenderer`.
        //
        // eslint-disable-next-line @typescript-eslint/ban-ts-comment
        // @ts-ignore: ignore our hacky overriding of a readonly property.
        _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_3__.DirListing.defaultRenderer = new _filebrowser__WEBPACK_IMPORTED_MODULE_11__.DirListingRenderer(artifactRegistry);
        // Find the existing FileBrowser factory plugin
        const factoryPlugin = _jupyterlab_filebrowser_extension__WEBPACK_IMPORTED_MODULE_4___default().find(({ id }) => {
            return id === '@jupyterlab/filebrowser-extension:factory';
        });
        return factoryPlugin.activate(app, docManager, translator, state, router, tree);
    }
};
const artifactRegistryPlugin = {
    id: REGISTRY_PLUGIN_ID,
    provides: _tokens__WEBPACK_IMPORTED_MODULE_13__.IArtifactRegistry,
    requires: [],
    activate(app) {
        return new _registry__WEBPACK_IMPORTED_MODULE_12__.ArtifactRegistry();
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ([plugin, fileBrowserFactoryPlugin, artifactRegistryPlugin]);


/***/ }),

/***/ "./lib/artifact-sharing/registry.js":
/*!******************************************!*\
  !*** ./lib/artifact-sharing/registry.js ***!
  \******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ArtifactRegistry": () => (/* binding */ ArtifactRegistry)
/* harmony export */ });
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__);


class ArtifactRegistry {
    constructor() {
        this._serverSettings = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__.ServerConnection.makeSettings();
        this._artifacts = [];
        this._artifactsFetched = false;
    }
    async createArtifact(artifact) {
        const res = await _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__.ServerConnection.makeRequest(Private.getArtifactsUrl(this._serverSettings), { method: 'POST', body: JSON.stringify(artifact) }, this._serverSettings);
        const updated = await Private.handleCreateResponse(res, artifact);
        this._updateArtifacts(updated);
        return updated;
    }
    async newArtifactVersion(artifact) {
        const res = await _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__.ServerConnection.makeRequest(Private.getArtifactsUrl(this._serverSettings), { method: 'POST', body: JSON.stringify(artifact) }, this._serverSettings);
        const version = await Private.handleNewVersionResponse(res);
        artifact.versions.push(version);
        this._updateArtifacts(artifact);
        return version;
    }
    async getArtifacts() {
        if (!this._artifactsFetched) {
            if (!this._artifactsFetchPromise) {
                this._artifactsFetchPromise = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__.ServerConnection.makeRequest(Private.getArtifactsUrl(this._serverSettings), { method: 'GET' }, this._serverSettings).then(Private.handleListResponse);
            }
            try {
                this._artifacts = await this._artifactsFetchPromise;
                this._artifactsFetched = true;
            }
            finally {
                delete this._artifactsFetchPromise;
            }
        }
        return this._artifacts;
    }
    async getArtifact(path) {
        const artifacts = await this.getArtifacts();
        return artifacts.find(a => a.path === path);
    }
    getArtifactSync(path) {
        return this._artifacts.find(a => a.path === path);
    }
    hasArtifactSync(path) {
        return !!this.getArtifactSync(path);
    }
    _updateArtifacts(artifact) {
        const indexOf = this._artifacts.findIndex(({ path }) => path === artifact.path);
        if (indexOf >= 0) {
            this._artifacts = this._artifacts
                .slice(0, indexOf)
                .concat([artifact], this._artifacts.slice(indexOf + 1));
        }
        else {
            this._artifacts = this._artifacts.concat([artifact]);
        }
    }
}
var Private;
(function (Private) {
    function getContentsUrl(settings) {
        const parts = [settings.baseUrl, 'chameleon', 'contents'];
        return _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.URLExt.join.call(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.URLExt, ...parts);
    }
    Private.getContentsUrl = getContentsUrl;
    function getArtifactsUrl(settings) {
        const parts = [settings.baseUrl, 'chameleon', 'artifacts'];
        return _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.URLExt.join.call(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.URLExt, ...parts);
    }
    Private.getArtifactsUrl = getArtifactsUrl;
    async function handleListResponse(res) {
        const { artifacts } = await res.json();
        if (!artifacts || !Array.isArray(artifacts)) {
            throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__.ServerConnection.ResponseError(res, 'Malformed response');
        }
        return artifacts;
    }
    Private.handleListResponse = handleListResponse;
    async function handleUpdateResponse(res) {
        if (res.status > 299) {
            const message = `HTTP error ${res.status} occurred updating the artifact`;
            throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__.ServerConnection.ResponseError(res, message);
        }
    }
    Private.handleUpdateResponse = handleUpdateResponse;
    async function handleNewVersionResponse(res) {
        if (!res.ok) {
            let error = JSON.stringify((await res.json()).error);
            if (!error) {
                error = "Unknown";
            }
            const message = `An error occurred creating the artifact version: ${error}`;
            throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__.ServerConnection.ResponseError(res, message);
        }
        const resJSON = await res.json();
        return resJSON;
    }
    Private.handleNewVersionResponse = handleNewVersionResponse;
    async function handleCreateResponse(res, old) {
        if (!res.ok) {
            let error = JSON.stringify((await res.json()).error);
            if (!error) {
                error = "Unknown";
            }
            const message = `An error occurred creating the artifact: ${error}`;
            throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__.ServerConnection.ResponseError(res, message);
        }
        const resJSON = await res.json();
        return {
            uuid: resJSON.uuid,
            title: resJSON.title,
            short_description: resJSON.short_description,
            long_description: resJSON.long_description,
            tags: resJSON.tags,
            authors: resJSON.authors,
            linked_projects: resJSON.linked_projects.map((urn) => ({ urn: urn })),
            reproducibility: resJSON.reproducibility,
            created_at: resJSON.created_at,
            updated_at: resJSON.updated_at,
            owner_urn: resJSON.owner_urn,
            visibility: resJSON.visibility,
            versions: resJSON.versions,
            ownership: old.ownership,
            path: old.path,
        };
    }
    Private.handleCreateResponse = handleCreateResponse;
    async function handleContentsResponse(res) {
        if (res.status > 299) {
            const message = `HTTP error ${res.status} occured uploading content`;
            throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__.ServerConnection.ResponseError(res, message);
        }
        return await res.json();
    }
    Private.handleContentsResponse = handleContentsResponse;
})(Private || (Private = {}));


/***/ }),

/***/ "./lib/artifact-sharing/tokens.js":
/*!****************************************!*\
  !*** ./lib/artifact-sharing/tokens.js ***!
  \****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ArtifactVisibility": () => (/* binding */ ArtifactVisibility),
/* harmony export */   "IArtifactRegistry": () => (/* binding */ IArtifactRegistry)
/* harmony export */ });
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__);

var ArtifactVisibility;
(function (ArtifactVisibility) {
    ArtifactVisibility["PUBLIC"] = "public";
    ArtifactVisibility["PRIVATE"] = "private";
})(ArtifactVisibility || (ArtifactVisibility = {}));
const IArtifactRegistry = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__.Token('@jupyterlab_zenodo:IZenodoRegistry');


/***/ }),

/***/ "./lib/artifact-sharing/widget.js":
/*!****************************************!*\
  !*** ./lib/artifact-sharing/widget.js ***!
  \****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ArtifactSharingComponent": () => (/* binding */ ArtifactSharingComponent),
/* harmony export */   "ArtifactSharingWidget": () => (/* binding */ ArtifactSharingWidget)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _tokens__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./tokens */ "./lib/artifact-sharing/tokens.js");



var WidgetState;
(function (WidgetState) {
    WidgetState["CONFIRM_FORM"] = "confirm-form";
    WidgetState["ARTIFACT_FORM"] = "artifact-form";
    WidgetState["WAITING"] = "waiting";
    WidgetState["SUCCESS"] = "success";
})(WidgetState || (WidgetState = {}));
class NewArtifactText extends react__WEBPACK_IMPORTED_MODULE_1__.Component {
    render() {
        return (react__WEBPACK_IMPORTED_MODULE_1__.createElement("div", null,
            react__WEBPACK_IMPORTED_MODULE_1__.createElement("h2", null, "Package new artifact"),
            react__WEBPACK_IMPORTED_MODULE_1__.createElement("p", null,
                "Packaging your work as an ",
                react__WEBPACK_IMPORTED_MODULE_1__.createElement("i", null, "artifact"),
                " makes it easier to share your Notebook(s) and related files with others. A packaged experiment:"),
            react__WEBPACK_IMPORTED_MODULE_1__.createElement("ul", null,
                react__WEBPACK_IMPORTED_MODULE_1__.createElement("li", null, "can by \u201Creplayed\u201D by any Chameleon user"),
                react__WEBPACK_IMPORTED_MODULE_1__.createElement("li", null,
                    "is displayed in",
                    ' ',
                    react__WEBPACK_IMPORTED_MODULE_1__.createElement("a", { href: this.props.urlFactory.indexUrl(), rel: "noreferrer", target: "_blank" }, "Chameleon Trovi"),
                    ' ',
                    "(artifact sharing system)"),
                react__WEBPACK_IMPORTED_MODULE_1__.createElement("li", null, "is initially private to you, but can be shared, either with specific projects, or all users"),
                react__WEBPACK_IMPORTED_MODULE_1__.createElement("li", null, "supports versioning, if you ever want to make changes")),
            react__WEBPACK_IMPORTED_MODULE_1__.createElement("p", null,
                "To learn more about Trovi, and artifact packaging, please refer to the",
                ' ',
                react__WEBPACK_IMPORTED_MODULE_1__.createElement("a", { href: "https://chameleoncloud.readthedocs.io", rel: "noreferrer", target: "_blank" }, "Chameleon documentation"),
                ".")));
    }
}
class NewArtifactSuccessText extends react__WEBPACK_IMPORTED_MODULE_1__.Component {
    render() {
        return (react__WEBPACK_IMPORTED_MODULE_1__.createElement("div", null,
            react__WEBPACK_IMPORTED_MODULE_1__.createElement("h2", null, "Your artifact was successfully packaged."),
            this.props.artifact && (react__WEBPACK_IMPORTED_MODULE_1__.createElement("p", null,
                "You can view your artifact at any time on",
                ' ',
                react__WEBPACK_IMPORTED_MODULE_1__.createElement("a", { href: this.props.urlFactory.detailUrl(this.props.artifact.uuid), target: "_blank", rel: "noreferrer" }, "Trovi"),
                ".")),
            react__WEBPACK_IMPORTED_MODULE_1__.createElement("p", null, "You may now close this window.")));
    }
}
class NewArtifactVersionText extends react__WEBPACK_IMPORTED_MODULE_1__.Component {
    render() {
        return (react__WEBPACK_IMPORTED_MODULE_1__.createElement("div", null,
            react__WEBPACK_IMPORTED_MODULE_1__.createElement("h2", null, "Create new artifact version"),
            react__WEBPACK_IMPORTED_MODULE_1__.createElement("p", null, "When you create a new version of an existing package, your package\u2019s files are re-uploaded and then saved as a new launchable artifact. Creating a new version makes sense if you make adjustments to your code or Notebooks, perhaps fixing a bug or adding additional capabilities or functionality."),
            react__WEBPACK_IMPORTED_MODULE_1__.createElement("p", null, "If you want to start a new packaged artifact, you can do so by moving the files you want included in the package to their own directory, outside of any already-published package directories."),
            react__WEBPACK_IMPORTED_MODULE_1__.createElement("p", null, "All package versions are displayed in Trovi along with your existing artifact title, description, and other metadata. You can optionally edit this metadata before saving your new version.")));
    }
}
class NewArtifactVersionSuccessText extends react__WEBPACK_IMPORTED_MODULE_1__.Component {
    render() {
        return (react__WEBPACK_IMPORTED_MODULE_1__.createElement("div", null,
            react__WEBPACK_IMPORTED_MODULE_1__.createElement("h2", null, "A new version of your artifact was created."),
            this.props.artifact && (react__WEBPACK_IMPORTED_MODULE_1__.createElement("p", null,
                "You can view your artifact at any time on",
                ' ',
                react__WEBPACK_IMPORTED_MODULE_1__.createElement("a", { href: this.props.urlFactory.detailUrl(this.props.artifact.uuid), target: "_blank", rel: "noreferrer" }, "Trovi"),
                ".")),
            react__WEBPACK_IMPORTED_MODULE_1__.createElement("p", null, "You may now close this window.")));
    }
}
class ArtifactDynamicLengthList extends react__WEBPACK_IMPORTED_MODULE_1__.Component {
    constructor(props) {
        super(props);
        const initialList = this.props.list;
        this.state = { list: initialList.length > 0 ? initialList : [this.props.newObjectGenerator()] };
    }
    addItem(index) {
        return (_) => {
            let copy = [...this.props.list];
            copy.splice(index + 1, 0, this.props.newObjectGenerator());
            return this.props.artifactUpdater(copy);
        };
    }
    removeItem(index) {
        return (_) => {
            let copy = [...this.props.list];
            copy.splice(index, 1);
            return this.props.artifactUpdater(copy);
        };
    }
    updateItem(index) {
        return (field) => {
            return (event) => {
                const value = event.target.value;
                let newList = [...this.props.list];
                newList[index] = Object.assign(Object.assign({}, newList[index]), { [field]: value });
                return this.props.artifactUpdater(newList);
            };
        };
    }
    getListForComponents() {
        if (this.props.list.length < 1) {
            return [this.props.newObjectGenerator()];
        }
        else {
            return this.props.list;
        }
    }
    render() {
        return (react__WEBPACK_IMPORTED_MODULE_1__.createElement("ul", null, this.getListForComponents().map((item, index) => (react__WEBPACK_IMPORTED_MODULE_1__.createElement("div", { key: index },
            react__WEBPACK_IMPORTED_MODULE_1__.createElement("li", null, this.props.newComponentGenerator(item, this.updateItem(index), this.props.disabled)),
            react__WEBPACK_IMPORTED_MODULE_1__.createElement("button", { type: "button", onClick: this.addItem(index), disabled: this.props.disabled }, "+"),
            react__WEBPACK_IMPORTED_MODULE_1__.createElement("button", { type: "button", onClick: this.removeItem(index), disabled: this.props.disabled }, "-"))))));
    }
}
class ArtifactAuthorComponent extends react__WEBPACK_IMPORTED_MODULE_1__.Component {
    constructor(props) {
        super(props);
    }
    hasAnyInput() {
        const author = this.props.author;
        return author.email !== "" || author.affiliation !== "" || author.full_name !== "";
    }
    render() {
        const author = this.props.author;
        return (react__WEBPACK_IMPORTED_MODULE_1__.createElement("div", { className: "authorInput" },
            react__WEBPACK_IMPORTED_MODULE_1__.createElement("label", null,
                react__WEBPACK_IMPORTED_MODULE_1__.createElement("p", null, "Full Name"),
                react__WEBPACK_IMPORTED_MODULE_1__.createElement("input", { name: "author_full_name", type: "text", placeholder: "The author's full name", required: this.hasAnyInput(), value: author.full_name, onChange: this.props.onFieldChange("full_name"), disabled: this.props.disabled })),
            react__WEBPACK_IMPORTED_MODULE_1__.createElement("label", null,
                react__WEBPACK_IMPORTED_MODULE_1__.createElement("p", null, "E-Mail Address"),
                react__WEBPACK_IMPORTED_MODULE_1__.createElement("input", { name: "author_email", type: "email", placeholder: "The author's e-mail address", required: this.hasAnyInput(), value: author.email, onChange: this.props.onFieldChange("email"), disabled: this.props.disabled })),
            react__WEBPACK_IMPORTED_MODULE_1__.createElement("label", null,
                react__WEBPACK_IMPORTED_MODULE_1__.createElement("p", null, "Affiliation"),
                react__WEBPACK_IMPORTED_MODULE_1__.createElement("input", { name: "author_affiliation", type: "text", placeholder: "The organization or group with which the author is affiliated", value: author.affiliation, onChange: this.props.onFieldChange("affiliation"), disabled: this.props.disabled }))));
    }
}
// class ArtifactLinkedProjectComponent extends React.Component<ArtifactForm.ProjectProps> {
//   constructor(props: ArtifactForm.ProjectProps) {
//     super(props);
//   }
//   render() {
//     const project = this.props.project;
//     return (
//       <div className="linkedProjectInput">
//         <label>
//           <p>URN</p>
//           {/* We just let users input a raw URN. We should probably have a dropdown of their projects... */}
//           <input
//             name="linked-Project-Urn-Input"
//             type="text"
//             placeholder="A URN describing a project"
//             onChange={this.props.onFieldChange("urn")}
//             value={project.urn}
//             disabled={this.props.disabled}
//           />
//         </label>
//       </div>
//     )
//   }
// }
// class ArtifactLinkComponent extends React.Component<ArtifactForm.LinkProps> {
//   constructor(props: ArtifactForm.LinkProps) {
//     super(props);
//   }
//   isAnythingSet(): boolean {
//     const link = this.props.link;
//     return (link.urn !== null &&
//       link.urn !== undefined &&
//       link.urn !== "") ||
//       (link.label !== null &&
//         link.label !== undefined &&
//         link.label !== "");
//   }
//   render() {
//     const link = this.props.link;
//     return (
//       <div className="linkInput">
//         <label>
//           <p>URN</p>
//           {/* This should be reworked, rather than just allowing the user to set arbitrary URNs */}
//           <input name="link_urn" type="text" placeholder="A URN string describing the link"
//             required={this.isAnythingSet()}
//             value={link.urn}
//             onChange={this.props.onFieldChange("urn")} />
//         </label>
//         <label>
//           <p>Label</p>
//           <input name="link_label" type="text" placeholder="A label which describes the link's content"
//             required={this.isAnythingSet()}
//             value={link.label}
//             onChange={this.props.onFieldChange("label")} />
//         </label>
//       </div>
//     )
//   }
// }
class ArtifactEditForm extends react__WEBPACK_IMPORTED_MODULE_1__.Component {
    isCreateForm() {
        return !this.props.artifact.uuid;
    }
    visibleOnlyOnNewVersion() {
        return this.props.artifact.uuid ? ArtifactEditForm.block : ArtifactEditForm.hidden;
    }
    render() {
        const fields = [];
        if (this.isCreateForm()) {
            fields.push(react__WEBPACK_IMPORTED_MODULE_1__.createElement("label", null,
                react__WEBPACK_IMPORTED_MODULE_1__.createElement("p", { className: "chi-ArtifactSharing-Form-Required" }, "Title"),
                react__WEBPACK_IMPORTED_MODULE_1__.createElement("input", { name: "title", type: "text", placeholder: "The title of your experiment", required: true, onChange: this.props.onChange("title") })));
            fields.push(react__WEBPACK_IMPORTED_MODULE_1__.createElement("label", null,
                react__WEBPACK_IMPORTED_MODULE_1__.createElement("p", { className: "chi-ArtifactSharing-Form-Required" }, "Short Description"),
                react__WEBPACK_IMPORTED_MODULE_1__.createElement("input", { name: "short_description", type: "text", placeholder: "A short description of your experiment", required: true, onChange: this.props.onChange("short_description") })));
            fields.push(react__WEBPACK_IMPORTED_MODULE_1__.createElement("label", null,
                react__WEBPACK_IMPORTED_MODULE_1__.createElement("p", null, "Long Description"),
                react__WEBPACK_IMPORTED_MODULE_1__.createElement("textarea", { name: "long_description", placeholder: "Long description of your experiment. Supports GitHub-flavored markdown (Optional)", onChange: this.props.onChange("long_description") })));
            fields.push(react__WEBPACK_IMPORTED_MODULE_1__.createElement("label", null,
                react__WEBPACK_IMPORTED_MODULE_1__.createElement("p", null, "Visibility"),
                react__WEBPACK_IMPORTED_MODULE_1__.createElement("select", { name: "visibility", title: "Allow other users to view your artifact", defaultValue: _tokens__WEBPACK_IMPORTED_MODULE_2__.ArtifactVisibility.PRIVATE, onChange: this.props.onChange("visibility") },
                    react__WEBPACK_IMPORTED_MODULE_1__.createElement("option", { value: _tokens__WEBPACK_IMPORTED_MODULE_2__.ArtifactVisibility.PRIVATE }, "private"),
                    react__WEBPACK_IMPORTED_MODULE_1__.createElement("option", { value: _tokens__WEBPACK_IMPORTED_MODULE_2__.ArtifactVisibility.PUBLIC }, "public"))));
        }
        return (react__WEBPACK_IMPORTED_MODULE_1__.createElement("form", { onSubmit: this.props.onSubmit, style: this.props.formVisibility },
            this.props.error && (react__WEBPACK_IMPORTED_MODULE_1__.createElement("div", { className: "chi-ArtifactSharing-ErrorMessage" }, this.props.error)),
            this.props.formText,
            react__WEBPACK_IMPORTED_MODULE_1__.createElement("fieldset", { id: "artifactFormInputs" },
                fields,
                react__WEBPACK_IMPORTED_MODULE_1__.createElement("label", null,
                    react__WEBPACK_IMPORTED_MODULE_1__.createElement("h3", null, "Authors"),
                    react__WEBPACK_IMPORTED_MODULE_1__.createElement(ArtifactDynamicLengthList, { artifactUpdater: this.props.onListChange("authors"), newComponentGenerator: (item, updater, disabled) => react__WEBPACK_IMPORTED_MODULE_1__.createElement(ArtifactAuthorComponent, { author: item, onFieldChange: updater, disabled: disabled }), newObjectGenerator: () => ({ full_name: "", email: "", affiliation: "" }), list: [...this.props.artifact.authors], disabled: !this.isCreateForm() }))),
            react__WEBPACK_IMPORTED_MODULE_1__.createElement("div", { className: "chi-ArtifactSharing-FormActions" },
                react__WEBPACK_IMPORTED_MODULE_1__.createElement("button", { className: "jp-mod-styled jp-mod-accept", type: "submit" },
                    "Upload: ",
                    react__WEBPACK_IMPORTED_MODULE_1__.createElement("code", null,
                        this.props.artifact.path,
                        "/")))));
    }
}
ArtifactEditForm.hidden = { display: 'none' };
ArtifactEditForm.block = { display: 'block' };
class ArtifactSharingComponent extends react__WEBPACK_IMPORTED_MODULE_1__.Component {
    constructor(props) {
        super(props);
        this._allStates = Object.values(WidgetState);
        this.state = {
            artifact: this.props.initialArtifact,
            currentState: WidgetState.ARTIFACT_FORM,
            errorMessage: null,
            waitMessage: null
        };
        this.onSubmit = this.onSubmit.bind(this);
        this.handleChange = this.handleChange.bind(this);
        this.handleListChange = this.handleListChange.bind(this);
    }
    handleChange(fieldName) {
        return (event) => {
            switch (fieldName) {
                case "visibility":
                    this.setState({
                        artifact: Object.assign(Object.assign({}, this.state.artifact), { visibility: event.target.value })
                    });
                    return;
                case "enable_requests":
                    this.setState({
                        artifact: Object.assign(Object.assign({}, this.state.artifact), { reproducibility: Object.assign(Object.assign({}, this.state.artifact.reproducibility), { enable_requests: event.target.checked }) })
                    });
                    return;
                case "access_hours":
                    this.setState({
                        artifact: Object.assign(Object.assign({}, this.state.artifact), { reproducibility: Object.assign(Object.assign({}, this.state.artifact.reproducibility), { access_hours: event.target.value }) })
                    });
                    return;
                default:
                    this.setState({ artifact: Object.assign(Object.assign({}, this.state.artifact), { [fieldName]: event.target.value }) });
                    return;
            }
        };
    }
    handleListChange(fieldName) {
        return (list) => {
            this.setState({ artifact: Object.assign(Object.assign({}, this.state.artifact), { [fieldName]: list }) });
        };
    }
    async onSubmit(event) {
        event.preventDefault();
        this.setState({
            currentState: WidgetState.WAITING,
            waitMessage: 'Please wait while your artifact files are uploaded'
        });
        try {
            const successState = {
                currentState: WidgetState.SUCCESS,
                errorMessage: null,
            };
            if (this.state.artifact.uuid) {
                await this.props.artifactRegistry.newArtifactVersion(this.state.artifact);
            }
            else {
                successState.artifact = await this.props.artifactRegistry.createArtifact(this.state.artifact);
            }
            this.setState(successState);
        }
        catch (e) {
            this.setState({
                currentState: WidgetState.ARTIFACT_FORM,
                errorMessage: `Failed to package artifact: ${e.message}`
            });
        }
    }
    render() {
        const hidden = { display: 'none' };
        const block = { display: 'block' };
        const visibilities = this._allStates.reduce((memo, state) => {
            memo[state] = this.state.currentState === state ? block : hidden;
            return memo;
        }, {});
        let formText;
        let successText;
        // Check if we started from an already-published artifact.
        if (this.props.initialArtifact.uuid) {
            formText = react__WEBPACK_IMPORTED_MODULE_1__.createElement(NewArtifactVersionText, { urlFactory: this.props.urlFactory });
            successText = (react__WEBPACK_IMPORTED_MODULE_1__.createElement(NewArtifactVersionSuccessText, { urlFactory: this.props.urlFactory, artifact: this.state.artifact }));
        }
        else {
            formText = react__WEBPACK_IMPORTED_MODULE_1__.createElement(NewArtifactText, { urlFactory: this.props.urlFactory });
            successText = (react__WEBPACK_IMPORTED_MODULE_1__.createElement(NewArtifactSuccessText, { urlFactory: this.props.urlFactory, artifact: this.state.artifact }));
        }
        return (react__WEBPACK_IMPORTED_MODULE_1__.createElement("div", { className: "chi-Expand" },
            react__WEBPACK_IMPORTED_MODULE_1__.createElement("div", { className: "chi-ArtifactSharing-Form", style: visibilities[WidgetState.ARTIFACT_FORM] }, this.state.currentState === WidgetState.ARTIFACT_FORM && (react__WEBPACK_IMPORTED_MODULE_1__.createElement(ArtifactEditForm, { artifact: this.state.artifact, formVisibility: visibilities[WidgetState.ARTIFACT_FORM], formText: formText, onChange: this.handleChange, onListChange: this.handleListChange, onSubmit: this.onSubmit, error: this.state.errorMessage }))),
            react__WEBPACK_IMPORTED_MODULE_1__.createElement("div", { className: "chi-ArtifactSharing-Form", style: visibilities[WidgetState.WAITING] },
                react__WEBPACK_IMPORTED_MODULE_1__.createElement("div", { className: "jp-Spinner" },
                    react__WEBPACK_IMPORTED_MODULE_1__.createElement("div", { className: "jp-SpinnerContent" }),
                    react__WEBPACK_IMPORTED_MODULE_1__.createElement("div", { className: "chi-ArtifactSharing-LoadingMessage" }, this.state.waitMessage))),
            react__WEBPACK_IMPORTED_MODULE_1__.createElement("div", { className: "chi-ArtifactSharing-Form", style: visibilities[WidgetState.SUCCESS] },
                this.state.errorMessage && (react__WEBPACK_IMPORTED_MODULE_1__.createElement("div", { className: "chi-ArtifactSharing-ErrorMessage" }, this.state.errorMessage)),
                successText)));
    }
}
class ArtifactSharingWidget extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.ReactWidget {
    constructor(artifact, workflow, urlFactory, artifactRegistry) {
        super();
        this.id = 'artifact-sharing-Widget';
        this._artifact = artifact;
        this._workflow = workflow;
        this._urlFactory = urlFactory;
        this._artifactRegistry = artifactRegistry;
    }
    render() {
        return (react__WEBPACK_IMPORTED_MODULE_1__.createElement(ArtifactSharingComponent, { initialArtifact: this._artifact, workflow: this._workflow, urlFactory: this._urlFactory, artifactRegistry: this._artifactRegistry, 
            // Disposing of a widget added to a MainContentArea will cause the
            // content area to also dispose of itself (close itself.)
            onCancel: this.dispose.bind(this) }));
    }
}


/***/ }),

/***/ "./lib/hydra-kernel/actions.js":
/*!*************************************!*\
  !*** ./lib/hydra-kernel/actions.js ***!
  \*************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ChameleonActions": () => (/* binding */ ChameleonActions)
/* harmony export */ });
var ChameleonActions;
(function (ChameleonActions) {
    function updateCellBinding(notebook, cellMeta, binding) {
        if (!notebook.model || !notebook.activeCell) {
            return;
        }
        cellMeta.setBindingName(notebook.activeCell.model, binding);
    }
    ChameleonActions.updateCellBinding = updateCellBinding;
    function removeCellBinding(notebook, cellMeta) {
        if (!notebook.model || !notebook.activeCell) {
            return;
        }
        cellMeta.removeBinding(notebook.activeCell.model);
    }
    ChameleonActions.removeCellBinding = removeCellBinding;
})(ChameleonActions || (ChameleonActions = {}));


/***/ }),

/***/ "./lib/hydra-kernel/binding.js":
/*!*************************************!*\
  !*** ./lib/hydra-kernel/binding.js ***!
  \*************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "BindingRegistry": () => (/* binding */ BindingRegistry)
/* harmony export */ });
/* harmony import */ var _jupyterlab_observables__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/observables */ "webpack/sharing/consume/default/@jupyterlab/observables");
/* harmony import */ var _jupyterlab_observables__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_observables__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @lumino/algorithm */ "webpack/sharing/consume/default/@lumino/algorithm");
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_lumino_algorithm__WEBPACK_IMPORTED_MODULE_1__);
// Copyright 2021 University of Chicago
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.


const COMM_CHANNEL = 'hydra';
class BindingRegistry {
    constructor() {
        this.isDisposed = false;
        this._bindings = new Map();
    }
    dispose() {
        this.isDisposed = true;
    }
    register(kernel) {
        if (this._bindings.has(kernel)) {
            return this._bindings.get(kernel).bindings;
        }
        const createComm = () => {
            const comm = kernel.createComm(COMM_CHANNEL);
            comm.onMsg = this._onCommMsg.bind(this);
            comm.open();
            return comm;
        };
        const tracker = {
            bindings: new _jupyterlab_observables__WEBPACK_IMPORTED_MODULE_0__.ObservableList(),
            comm: null
        };
        const onKernelConnectionStatusChanged = (_, status) => {
            if (status === 'connected') {
                if (tracker.comm) {
                    tracker.comm.dispose();
                }
                tracker.comm = createComm();
                tracker.comm.send({
                    event: 'binding_list_request',
                    bindings: (0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_1__.toArray)(tracker.bindings)
                });
            }
        };
        kernel.connectionStatusChanged.connect(onKernelConnectionStatusChanged);
        const onKernelDisposed = () => {
            console.log('kernel disposed');
            kernel.disposed.disconnect(onKernelDisposed);
            kernel.connectionStatusChanged.disconnect(onKernelConnectionStatusChanged);
            this.unregister(kernel);
        };
        kernel.disposed.connect(onKernelDisposed);
        this._bindings.set(kernel, tracker);
        return tracker.bindings;
    }
    unregister(kernel) {
        if (!this._bindings.has(kernel)) {
            return;
        }
        const { comm, bindings } = this._bindings.get(kernel);
        bindings.dispose();
        if (comm) {
            comm.onMsg = null;
            comm.close();
        }
        this._bindings.delete(kernel);
    }
    getBindings(kernel) {
        if (!this._bindings.has(kernel)) {
            throw new Error('Kernel not registered');
        }
        return this._bindings.get(kernel).bindings;
    }
    _findTrackerByCommId(commId) {
        var _a;
        for (const tracker of this._bindings.values()) {
            if (((_a = tracker.comm) === null || _a === void 0 ? void 0 : _a.commId) === commId) {
                return tracker;
            }
        }
        return null;
    }
    _onCommMsg(msg) {
        var _a, _b;
        const commId = (_a = msg === null || msg === void 0 ? void 0 : msg.content) === null || _a === void 0 ? void 0 : _a.comm_id;
        if (!commId) {
            console.log('Ignoring message without comm_id', msg);
            return;
        }
        const tracker = this._findTrackerByCommId(commId);
        if (!tracker) {
            console.log('Ignoring message from untracked comm', msg);
            return;
        }
        const data = (_b = msg === null || msg === void 0 ? void 0 : msg.content) === null || _b === void 0 ? void 0 : _b.data;
        const { event } = data || {};
        function locateBinding() {
            const binding = data.binding;
            const bindingIndex = (0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_1__.findIndex)(tracker.bindings.iter(), ({ name }, _) => name === binding.name);
            return [binding, bindingIndex];
        }
        let binding = null;
        let bindingIndex = -1;
        switch (event) {
            case 'binding_list_reply':
                tracker.bindings.clear();
                tracker.bindings.pushAll(data.bindings);
                break;
            case 'binding_update':
                [binding, bindingIndex] = locateBinding();
                if (bindingIndex > -1) {
                    tracker.bindings.set(bindingIndex, binding);
                }
                else {
                    tracker.bindings.push(binding);
                }
                break;
            case 'binding_remove':
                [binding, bindingIndex] = locateBinding();
                if (bindingIndex > -1) {
                    tracker.bindings.remove(bindingIndex);
                }
                break;
            default:
                break;
        }
    }
}
var Private;
(function (Private) {
    class BindingTracker {
    }
    Private.BindingTracker = BindingTracker;
})(Private || (Private = {}));


/***/ }),

/***/ "./lib/hydra-kernel/cell-metadata.js":
/*!*******************************************!*\
  !*** ./lib/hydra-kernel/cell-metadata.js ***!
  \*******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "CellMetadata": () => (/* binding */ CellMetadata)
/* harmony export */ });
// Copyright 2021 jasonanderson
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
const METADATA_NAMESPACE = 'chameleon';
const BINDING_NAME_METADATA_KEY = `${METADATA_NAMESPACE}.binding_name`;
class CellMetadata {
    constructor() {
        this.isDisposed = false;
        this._onBindingNameChangeHandlers = new Map();
    }
    hasBinding(cell) {
        return cell.metadata.has(BINDING_NAME_METADATA_KEY);
    }
    setBindingName(cell, name) {
        cell.metadata.set(BINDING_NAME_METADATA_KEY, name);
    }
    removeBinding(cell) {
        cell.metadata.delete(BINDING_NAME_METADATA_KEY);
    }
    getBindingName(cell) {
        return cell.metadata.get(BINDING_NAME_METADATA_KEY);
    }
    /**
     * Register callback to execute whenever a given cell's binding changes.
     */
    onBindingNameChanged(cell, fn) {
        const onChange = (metadata, changed) => {
            if (changed.key === BINDING_NAME_METADATA_KEY) {
                fn();
            }
        };
        cell.metadata.changed.connect(onChange);
        const handlers = this._onBindingNameChangeHandlers.get(cell) || [];
        this._onBindingNameChangeHandlers.set(cell, handlers.concat([onChange]));
    }
    dispose() {
        this._onBindingNameChangeHandlers.forEach((list, cell) => {
            list.forEach(fn => cell.metadata.changed.disconnect(fn));
        });
        this.isDisposed = true;
    }
}


/***/ }),

/***/ "./lib/hydra-kernel/index.js":
/*!***********************************!*\
  !*** ./lib/hydra-kernel/index.js ***!
  \***********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "HydraNotebookExtension": () => (/* binding */ HydraNotebookExtension),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/application */ "webpack/sharing/consume/default/@jupyterlab/application");
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @lumino/algorithm */ "webpack/sharing/consume/default/@lumino/algorithm");
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_lumino_algorithm__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _lumino_disposable__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @lumino/disposable */ "webpack/sharing/consume/default/@lumino/disposable");
/* harmony import */ var _lumino_disposable__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_lumino_disposable__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _status_panel__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./status-panel */ "./lib/hydra-kernel/status-panel.js");
/* harmony import */ var _tokens__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./tokens */ "./lib/hydra-kernel/tokens.js");
/* harmony import */ var _cell_metadata__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ./cell-metadata */ "./lib/hydra-kernel/cell-metadata.js");
/* harmony import */ var _toolbar_extension__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ./toolbar-extension */ "./lib/hydra-kernel/toolbar-extension.js");
/* harmony import */ var _binding__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ./binding */ "./lib/hydra-kernel/binding.js");











// Generate class names for binding display modifiers
const CELL_CLASSES = [...Array(10).keys()].map(n => `chi-binding-${n}`);
/**
 * A notebook widget extension that adds a button to the toolbar.
 */
class HydraNotebookExtension {
    constructor(bindingRegistry) {
        this.registry = bindingRegistry;
    }
    /**
     * Create a new extension object.
     */
    createNew(panel, context) {
        const cellMetadata = new _cell_metadata__WEBPACK_IMPORTED_MODULE_8__.CellMetadata();
        const switcher = new _toolbar_extension__WEBPACK_IMPORTED_MODULE_9__.CellBindingSwitcher(panel.content, cellMetadata);
        let bindings;
        panel.toolbar.insertBefore('spacer', 'changeBinding', switcher);
        // Hide the binding switch UI for non-code cells.
        panel.content.activeCellChanged.connect((notebook, cell) => {
            switcher.setHidden(!!cell && cell.model.type !== 'code');
        });
        const onBindingsChanged = (_, changed) => {
            switcher.updateBindings(bindings);
            panel.content.widgets.forEach(cellWidget => {
                if (cellWidget.model.type === 'code') {
                    Private.updateCellDisplay(cellWidget, cellMetadata, bindings);
                }
            });
            // NOTE(jason): We do NOT remove the binding metadata here even if the
            // model is removed. This is because there are many reasons why the
            // binding list could change: the kernel could be restarted for example.
            // The user can manually re-link any cell tied to a deleted binding.
        };
        const onKernelChanged = (sessionContext, changed) => {
            if (bindings) {
                bindings.changed.disconnect(onBindingsChanged);
                bindings = null;
            }
            const kernel = changed.newValue;
            if (kernel) {
                bindings = this.registry.register(changed.newValue);
                bindings.changed.connect(onBindingsChanged);
            }
        };
        const onCellsChanged = (cells, changed) => {
            const cellModel = cells.get(changed.newIndex);
            if (!(changed.type === 'add' && cellModel.type === 'code')) {
                return;
            }
            const cellWidget = panel.content.widgets.find(w => w.model === cellModel);
            /**
             * Set up the handler first; this will be triggered if we set
             * an initial value, initialize the view state.
             */
            cellMetadata.onBindingNameChanged(cellModel, () => {
                Private.updateCellDisplay(cellWidget, cellMetadata, bindings);
            });
            if (changed.newIndex > 0 &&
                !cellModel.value.text.length &&
                !cellMetadata.hasBinding(cellModel)) {
                // Automatically seed new cells added to the end w/ the prior binding.
                const previousCell = cells.get(changed.newIndex - 1);
                const previousBinding = cellMetadata.getBindingName(previousCell);
                if (previousBinding) {
                    cellMetadata.setBindingName(cellModel, previousBinding);
                }
            }
        };
        panel.model.cells.changed.connect(onCellsChanged);
        panel.sessionContext.kernelChanged.connect(onKernelChanged);
        return new _lumino_disposable__WEBPACK_IMPORTED_MODULE_5__.DisposableDelegate(() => {
            panel.model.cells.changed.disconnect(onCellsChanged);
            panel.sessionContext.kernelChanged.disconnect(onKernelChanged);
            if (bindings) {
                bindings.changed.disconnect(onBindingsChanged);
            }
            cellMetadata.dispose();
            switcher.dispose();
        });
    }
}
const plugin = {
    id: '@chameleoncloud/jupyterlab-chameleon:hydra-notebook',
    autoStart: true,
    requires: [_tokens__WEBPACK_IMPORTED_MODULE_7__.IBindingRegistry],
    activate(app, bindingRegistry) {
        app.docRegistry.addWidgetExtension('Notebook', new HydraNotebookExtension(bindingRegistry));
    }
};
var Private;
(function (Private) {
    /**
     * Update a cell's display according to its binding. Each binding
     * has its own distinct visual look so that cells belonging to the same
     * binding are visually similar.
     *
     * @param widget the Cell widget
     * @param bindings an ordered list of all known bindings
     */
    function updateCellDisplay(widget, cellMeta, bindings) {
        CELL_CLASSES.forEach(cls => widget.removeClass(cls));
        const cellBindingName = cellMeta.getBindingName(widget.model);
        const indexOf = (0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_4__.findIndex)(bindings.iter(), ({ name }, _) => name === cellBindingName);
        if (indexOf > -1) {
            const binding = bindings.get(indexOf);
            widget.addClass(CELL_CLASSES[indexOf % CELL_CLASSES.length]);
            widget.editor.model.mimeType = binding.mimeType || 'shell';
        }
        else {
            widget.editor.model.mimeType = 'python';
        }
    }
    Private.updateCellDisplay = updateCellDisplay;
})(Private || (Private = {}));
const bindingRegistryPlugin = {
    id: '@chameleoncloud/jupyterlab-chameleon:binding-registry',
    autoStart: true,
    provides: _tokens__WEBPACK_IMPORTED_MODULE_7__.IBindingRegistry,
    activate() {
        return new _binding__WEBPACK_IMPORTED_MODULE_10__.BindingRegistry();
    }
};
const statusPlugin = {
    id: '@chameleoncloud/jupyterlab-chameleon:hydra-bindings',
    autoStart: true,
    requires: [_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILabShell, _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_1__.INotebookTracker, _tokens__WEBPACK_IMPORTED_MODULE_7__.IBindingRegistry, _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__.ITranslator],
    optional: [_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILayoutRestorer],
    activate: (app, labshell, notebookTracker, bindingRegistry, translator, restorer) => {
        const trans = translator.load('jupyterlab');
        const widget = new _status_panel__WEBPACK_IMPORTED_MODULE_6__.BindingStatusPanel(labshell, notebookTracker, bindingRegistry, translator);
        widget.title.icon = _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__.offlineBoltIcon;
        widget.title.caption = trans.__('Hydra Subkernels');
        widget.id = 'chi-hydra-bindings';
        labshell.add(widget, 'right', { rank: 100 });
        if (restorer) {
            restorer.add(widget, 'chi-hydra-bindings');
        }
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ([plugin, bindingRegistryPlugin, statusPlugin]);


/***/ }),

/***/ "./lib/hydra-kernel/status-panel.js":
/*!******************************************!*\
  !*** ./lib/hydra-kernel/status-panel.js ***!
  \******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "BindingStatusPanel": () => (/* binding */ BindingStatusPanel),
/* harmony export */   "BindingListWidget": () => (/* binding */ BindingListWidget)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @lumino/algorithm */ "webpack/sharing/consume/default/@lumino/algorithm");
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_lumino_algorithm__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_5__);
// Copyright 2021 University of Chicago
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.






class BindingStatusPanel extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_4__.Widget {
    /**
     * Construct a new Side Bar Property Inspector.
     */
    constructor(labshell, notebookTracker, bindingRegistry, translator) {
        super();
        this.addClass('chi-HydraBindings');
        notebookTracker.currentChanged.connect(this._onCurrentChanged, this);
        this._currentNotebook = notebookTracker.currentWidget;
        this._bindingRegistry = bindingRegistry;
        this._labshell = labshell;
        this.translator = translator || _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__.nullTranslator;
        this._trans = this.translator.load('jupyterlab');
        const layout = (this.layout = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_4__.SingletonLayout());
        const node = document.createElement('div');
        const content = document.createElement('div');
        content.textContent = this._trans.__('Please select a Notebook that utilizes the Hydra kernel to see subkernel statuses.');
        content.className = 'chi-HydraBindings-placeholderContent';
        node.appendChild(content);
        this._placeholder = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_4__.Widget({ node });
        this._placeholder.addClass('chi-HydraBindings-placeholder');
        layout.widget = this._placeholder;
        this.refresh();
    }
    _onCurrentChanged(_, notebook) {
        if (this._currentNotebook) {
            this._currentNotebook.sessionContext.kernelChanged.disconnect(this._onKernelChanged, this);
        }
        this._currentNotebook = notebook;
        this._currentNotebook.sessionContext.kernelChanged.connect(this._onKernelChanged, this);
        this.refresh();
    }
    _onKernelChanged(_, changed) {
        this.refresh();
    }
    /**
     * Refresh the content for the current widget.
     */
    refresh() {
        var _a, _b;
        const kernel = (_b = (_a = this._currentNotebook) === null || _a === void 0 ? void 0 : _a.sessionContext.session) === null || _b === void 0 ? void 0 : _b.kernel;
        if (kernel && kernel.name === 'hydra') {
            console.log('hydra kernel detected');
            this.setContent(new BindingListWidget(this._bindingRegistry.getBindings(kernel)));
        }
        else {
            this.setContent(null);
        }
    }
    /**
     * Set the content of the sidebar panel.
     */
    setContent(content) {
        const layout = this.layout;
        if (layout.widget) {
            layout.widget.removeClass('chi-HydraBindings-content');
            layout.removeWidget(layout.widget);
        }
        if (!content) {
            content = this._placeholder;
        }
        content.addClass('chi-HydraBindings-content');
        layout.widget = content;
    }
    /**
     * Show the sidebar panel.
     */
    showPanel() {
        this._labshell.activateById(this.id);
    }
}
class BindingListWidget extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.ReactWidget {
    constructor(bindings) {
        super();
        this._bindings = bindings;
    }
    render() {
        return react__WEBPACK_IMPORTED_MODULE_5__.createElement(BindingStatusList, { bindings: this._bindings });
    }
    dispose() {
        super.dispose();
        this._bindings = null;
    }
}
class BindingStatusList extends react__WEBPACK_IMPORTED_MODULE_5__.Component {
    constructor(props) {
        super(props);
        this.state = { bindings: (0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_2__.toArray)(props.bindings.iter()) };
        props.bindings.changed.connect(this.onBindingsChanged, this);
    }
    onBindingsChanged(bindings) {
        // Translate bindings property changes to state changes so React
        // will correctly re-render the component.
        this.setState({ bindings: (0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_2__.toArray)(bindings.iter()) });
    }
    render() {
        return (react__WEBPACK_IMPORTED_MODULE_5__.createElement("div", { className: "chi-BindingStatus" },
            react__WEBPACK_IMPORTED_MODULE_5__.createElement("div", { className: "chi-BindingStatus-header" }, "Subkernels"),
            this.state.bindings.map((binding) => {
                return react__WEBPACK_IMPORTED_MODULE_5__.createElement(BindingStatus, { binding: binding });
            })));
    }
    componentWillUnmount() {
        this.props.bindings.changed.disconnect(this.onBindingsChanged, this);
    }
}
class BindingStatus extends react__WEBPACK_IMPORTED_MODULE_5__.Component {
    constructor() {
        super(...arguments);
        this.state = {
            isOpen: false
        };
        this.handleClick = () => {
            this.setState({ isOpen: !this.state.isOpen });
        };
    }
    render() {
        const binding = this.props.binding;
        const connection = binding.connection;
        const basicDisplay = (react__WEBPACK_IMPORTED_MODULE_5__.createElement("div", null,
            "Connection: ",
            connection.type,
            react__WEBPACK_IMPORTED_MODULE_5__.createElement("br", null),
            "Kernel: ",
            binding.kernel));
        let connectionDisplay;
        let sshConnection, zunConnection;
        switch (binding.connection.type) {
            case 'local':
                break;
            case 'ssh':
                sshConnection = connection;
                connectionDisplay = (react__WEBPACK_IMPORTED_MODULE_5__.createElement("div", null,
                    "SSH: ",
                    react__WEBPACK_IMPORTED_MODULE_5__.createElement("span", null,
                        sshConnection.user,
                        "@"),
                    react__WEBPACK_IMPORTED_MODULE_5__.createElement("span", null, sshConnection.host),
                    react__WEBPACK_IMPORTED_MODULE_5__.createElement("br", null),
                    "Identity file: ",
                    sshConnection.privateKeyFile));
                break;
            case 'zun':
                zunConnection = connection;
                connectionDisplay = react__WEBPACK_IMPORTED_MODULE_5__.createElement("div", null,
                    "Container: ",
                    zunConnection.containerUuid);
                break;
            default:
                break;
        }
        const progressBarStyle = {
            width: `${(binding.progress.progressRatio || 0.0) * 100}%`
        };
        const connectedStateIcon = (binding.progress.progress || '').toLowerCase() === 'idle'
            ? _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__.circleEmptyIcon
            : _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__.circleIcon;
        const statusIcon = binding.state === 'connected' ? connectedStateIcon : _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__.offlineBoltIcon;
        return (react__WEBPACK_IMPORTED_MODULE_5__.createElement("div", { className: "chi-Binding", onClick: this.handleClick },
            react__WEBPACK_IMPORTED_MODULE_5__.createElement("div", { className: "chi-BindingSummary" },
                react__WEBPACK_IMPORTED_MODULE_5__.createElement("div", { className: "chi-BindingSummary-status" },
                    react__WEBPACK_IMPORTED_MODULE_5__.createElement(statusIcon.react, null)),
                react__WEBPACK_IMPORTED_MODULE_5__.createElement("div", { className: "chi-BindingSummary-summary" },
                    react__WEBPACK_IMPORTED_MODULE_5__.createElement("div", { className: "chi-Binding-name" }, binding.name),
                    react__WEBPACK_IMPORTED_MODULE_5__.createElement("div", { className: `chi-BindingState-${binding.state}` }, binding.state),
                    react__WEBPACK_IMPORTED_MODULE_5__.createElement("div", { className: "chi-BindingState-progress" },
                        binding.progress.progress,
                        binding.progress.progressRatio && (react__WEBPACK_IMPORTED_MODULE_5__.createElement("div", { className: "chi-BindingState-progressBarContainer" },
                            react__WEBPACK_IMPORTED_MODULE_5__.createElement("span", { className: "chi-BindingState-progressBar", style: progressBarStyle })))))),
            react__WEBPACK_IMPORTED_MODULE_5__.createElement(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__.Collapse, { keepChildrenMounted: true, isOpen: this.state.isOpen },
                react__WEBPACK_IMPORTED_MODULE_5__.createElement("div", { className: "chi-BindingConnection" },
                    react__WEBPACK_IMPORTED_MODULE_5__.createElement("div", { className: "chi-BindingConnection-header" }, "Connection details"),
                    basicDisplay,
                    connectionDisplay))));
    }
}


/***/ }),

/***/ "./lib/hydra-kernel/tokens.js":
/*!************************************!*\
  !*** ./lib/hydra-kernel/tokens.js ***!
  \************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "IBindingRegistry": () => (/* binding */ IBindingRegistry)
/* harmony export */ });
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__);

const IBindingRegistry = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__.Token('@chameleoncloud/jupyter-chameleon:IBindingRegistry');


/***/ }),

/***/ "./lib/hydra-kernel/toolbar-extension.js":
/*!***********************************************!*\
  !*** ./lib/hydra-kernel/toolbar-extension.js ***!
  \***********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "CellBindingSwitcher": () => (/* binding */ CellBindingSwitcher)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @lumino/algorithm */ "webpack/sharing/consume/default/@lumino/algorithm");
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_lumino_algorithm__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _actions__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./actions */ "./lib/hydra-kernel/actions.js");





const TOOLBAR_CELLBINDING_CLASS = 'chi-Notebook-toolbarCellBindingDropdown';
/**
 * A toolbar widget that switches cell bindings.
 */
class CellBindingSwitcher extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.ReactWidget {
    /**
     * Construct a new cell type switcher.
     */
    constructor(widget, cellMeta) {
        super();
        /**
         * Handle `change` events for the HTMLSelect component.
         */
        this.handleChange = (event) => {
            if (event.target.value === '-') {
                _actions__WEBPACK_IMPORTED_MODULE_4__.ChameleonActions.removeCellBinding(this._notebook, this._cellMeta);
            }
            else {
                _actions__WEBPACK_IMPORTED_MODULE_4__.ChameleonActions.updateCellBinding(this._notebook, this._cellMeta, event.target.value);
            }
            // Return focus
            this._notebook.activate();
            this.update();
        };
        /**
         * Handle `keydown` events for the HTMLSelect component.
         */
        this.handleKeyDown = (event) => {
            if (event.keyCode === 13) {
                this._notebook.activate();
            }
        };
        this._notebook = null;
        this._cellMeta = null;
        this._bindingList = [];
        this.addClass(TOOLBAR_CELLBINDING_CLASS);
        this._notebook = widget;
        this._cellMeta = cellMeta;
        if (widget.model) {
            this.update();
        }
        widget.activeCellChanged.connect(this.update, this);
        // Follow a change in the selection.
        widget.selectionChanged.connect(this.update, this);
    }
    updateBindings(binding) {
        this._bindingList = (0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_1__.toArray)(binding.iter());
        this.update();
    }
    dispose() {
        super.dispose();
        this._bindingList = [];
    }
    render() {
        let value = '-';
        if (this._notebook.activeCell) {
            const cellModel = this._notebook.activeCell.model;
            if (this._cellMeta.hasBinding(cellModel)) {
                value = this._cellMeta.getBindingName(cellModel);
            }
        }
        return (react__WEBPACK_IMPORTED_MODULE_3__.createElement(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__.HTMLSelect
        // className={TOOLBAR_CELLTYPE_DROPDOWN_CLASS}
        , { 
            // className={TOOLBAR_CELLTYPE_DROPDOWN_CLASS}
            onChange: this.handleChange, onKeyDown: this.handleKeyDown, value: value, icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__.caretDownIcon, "aria-label": "Binding" },
            react__WEBPACK_IMPORTED_MODULE_3__.createElement("option", { value: "-" }, "META"),
            this._bindingList.map(({ name }) => (react__WEBPACK_IMPORTED_MODULE_3__.createElement("option", { key: name, value: name }, name)))));
    }
}


/***/ }),

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _artifact_sharing__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./artifact-sharing */ "./lib/artifact-sharing/index.js");
/* harmony import */ var _session_heartbeat__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./session-heartbeat */ "./lib/session-heartbeat/index.js");
/* harmony import */ var _hydra_kernel__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./hydra-kernel */ "./lib/hydra-kernel/index.js");



/**
 * Export the plugins as default.
 */
const plugins = [];
_artifact_sharing__WEBPACK_IMPORTED_MODULE_0__["default"].forEach(plugin => plugins.push(plugin));
plugins.push(_session_heartbeat__WEBPACK_IMPORTED_MODULE_1__["default"]);
_hydra_kernel__WEBPACK_IMPORTED_MODULE_2__["default"].forEach(plugin => plugins.push(plugin));
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugins);


/***/ }),

/***/ "./lib/session-heartbeat/index.js":
/*!****************************************!*\
  !*** ./lib/session-heartbeat/index.js ***!
  \****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_hub_extension__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/hub-extension */ "webpack/sharing/consume/default/@jupyterlab/hub-extension");
/* harmony import */ var _jupyterlab_hub_extension__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_hub_extension__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_3__);




class Heartbeat {
    constructor(commands) {
        this._commands = null;
        this._heartbeatTimer = null;
        this._interval = 60000; // ms
        this._serverSettings = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_3__.ServerConnection.makeSettings();
        this._commands = commands;
    }
    start() {
        this.stop();
        this._heartbeatTimer = window.setInterval(async () => {
            await this._beat();
        }, this._interval);
        // Immediately check
        this._beat();
    }
    stop() {
        window.clearTimeout(this._heartbeatTimer);
    }
    async _beat() {
        const response = await _jupyterlab_services__WEBPACK_IMPORTED_MODULE_3__.ServerConnection.makeRequest(Private.getUrl(this._serverSettings), { method: 'GET' }, this._serverSettings);
        const json = await response.json();
        if (response.status === 200) {
            console.debug(`Session ok until ${json.expires_at}`);
        }
        else if (response.status === 401) {
            this.stop();
            if (json.reauthenticate_link) {
                await this._reauthenticate(json.reauthenticate_link);
            }
            else {
                console.warn('User backend session timed out, yet there was no reauthenticate link provided.');
                // TODO: this assumes the extension is running w/in a Hub environment, really.
                this._commands.execute(_jupyterlab_hub_extension__WEBPACK_IMPORTED_MODULE_2__.CommandIDs.logout);
            }
        }
        else if (response.status === 405) {
            this.stop();
            console.debug('Disabling session heartbeat; hearbeat not supported.');
        }
    }
    async _reauthenticate(redirectUrl) {
        const dialog = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Dialog({
            title: 'Your Chameleon session has timed out.',
            body: 'We will attempt to automatically reconnect you.',
            buttons: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Dialog.okButton({ label: 'Continue' })]
        });
        const result = await dialog.launch();
        dialog.dispose();
        if (result.button.accept) {
            redirectUrl = `${redirectUrl}?next=${document.location.pathname}`;
            document.location.href = redirectUrl;
        }
    }
}
var Private;
(function (Private) {
    function getUrl(settings) {
        const parts = [settings.baseUrl, 'chameleon', 'heartbeat'];
        return _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.URLExt.join.call(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.URLExt, ...parts);
    }
    Private.getUrl = getUrl;
})(Private || (Private = {}));
const plugin = {
    activate(app) {
        Promise.all([app.restored])
            .then(async () => {
            const heartbeat = new Heartbeat(app.commands);
            heartbeat.start();
        })
            .catch(err => {
            console.error(err);
        });
    },
    id: '@chameleoncloud/jupyterlab-chameleon:sessionHeartbeatPlugin',
    autoStart: true
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);


/***/ })

}]);
//# sourceMappingURL=lib_index_js.6761124b21242aeee7c9.js.map
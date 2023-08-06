"use strict";
(self["webpackChunkjupyterlab_rsw"] = self["webpackChunkjupyterlab_rsw"] || []).push([["lib_index_js"],{

/***/ "./lib/constants.js":
/*!**************************!*\
  !*** ./lib/constants.js ***!
  \**************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "kQuartoApp": () => (/* binding */ kQuartoApp),
/* harmony export */   "kServerEndpoint": () => (/* binding */ kServerEndpoint),
/* harmony export */   "kShinyApp": () => (/* binding */ kShinyApp),
/* harmony export */   "kUrlEndpoint": () => (/* binding */ kUrlEndpoint)
/* harmony export */ });
/*
 * constants.ts
 *
 * Copyright (C) 2022 by RStudio, PBC
 *
 */
// This file shares variables with './jupyterlab_rsw/constants.py'
// Changes made to this file may need to be duplicated there.
// default process names
const kShinyApp = 'Shiny Project';
const kQuartoApp = 'Quarto Project';
// jupyterlab_rsw server extension endpoints
const kServerEndpoint = 'servers';
const kUrlEndpoint = 'url';


/***/ }),

/***/ "./lib/handler.js":
/*!************************!*\
  !*** ./lib/handler.js ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "requestAPI": () => (/* binding */ requestAPI)
/* harmony export */ });
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__);
/*
 * handler.ts
 *
 * Copyright (C) 2022 by RStudio, PBC
 *
 */


/**
 * Call the API extension
 *
 * @param endPoint API REST end point for the extension
 * @param init Initial values for the request
 * @returns The response body interpreted as JSON
 */
async function requestAPI(endPoint = '', init = {}) {
    // Make request to Jupyter API
    const settings = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeSettings();
    const requestUrl = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.URLExt.join(settings.baseUrl, 'jupyterlab-rsw', // API Namespace
    endPoint);
    let response;
    response = await _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeRequest(requestUrl, init, settings);
    let data = await response.text();
    if (data.length > 0) {
        try {
            data = JSON.parse(data);
        }
        catch (error) {
            console.log('Not a JSON response body.', response);
        }
    }
    if (!response.ok) {
        throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.ResponseError(response, data.message || data);
    }
    return data;
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
/* harmony import */ var _images_rstudio_svg__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../images/rstudio.svg */ "./images/rstudio.svg");
/* harmony import */ var _images_rstudio_panel_svg__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../images/rstudio_panel.svg */ "./images/rstudio_panel.svg");
/* harmony import */ var _widget__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./widget */ "./lib/widget.js");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_3__);
/*
 * index.ts
 *
 * Copyright (C) 2022 by RStudio, PBC
 *
 */







let homeUrl = '/home';
const rstudioIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__.LabIcon({
    name: 'jupyterlab_rsw:home-icon',
    svgstr: _images_rstudio_svg__WEBPACK_IMPORTED_MODULE_4__["default"],
});
const rstudioPanelIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__.LabIcon({
    name: 'jupyterlab_rsw:panel-icon',
    svgstr: _images_rstudio_panel_svg__WEBPACK_IMPORTED_MODULE_5__["default"],
});
function returnHome() {
    location.assign(homeUrl);
}
function registerCommands(app, palette) {
    var regex = /(s\/[\w]{5}[\w]{8}[\w]{8}\/)/g;
    const settings = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_3__.ServerConnection.makeSettings();
    homeUrl = settings.baseUrl.replace(regex, 'home/');
    // Register command to return to RStudio Workbench home
    const command = 'jupyterlab_rsw:return-home';
    app.commands.addCommand(command, {
        label: 'Return to RStudio Workbench Home',
        caption: 'Return to RStudio Workbench Home',
        execute: returnHome
    });
    palette.addItem({ command, category: 'RStudio Workbench' });
}
function addRStudioIcon(app) {
    // Add RStudio icon that returns the user to home to menu bar
    const rstudio_widget = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.Widget();
    rstudio_widget.id = 'rsw-icon';
    rstudio_widget.node.onclick = returnHome;
    rstudioIcon.element({
        container: rstudio_widget.node,
        justify: 'center',
        margin: '2px 5px 2px 5px',
        height: 'auto',
        width: '20px',
    });
    app.shell.add(rstudio_widget, 'top', { rank: 1 });
}
function addSideBar(app) {
    // Add the RSW side bar widget to the left panel
    const panel = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.Panel();
    panel.id = 'RStudio-Workbench-tab';
    panel.title.icon = rstudioPanelIcon;
    panel.addWidget(new _widget__WEBPACK_IMPORTED_MODULE_6__.RStudioWorkbenchWidget());
    app.shell.add(panel, 'left', { rank: 501 });
}
function activate(app, palette) {
    registerCommands(app, palette);
    addRStudioIcon(app);
    addSideBar(app);
}
const plugin = {
    // Initialization data for the jupyterlab_rsw extension.
    id: 'jupyterlab-rsw',
    autoStart: true,
    requires: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ICommandPalette],
    activate: activate,
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);


/***/ }),

/***/ "./lib/proxiedServersComponent.js":
/*!****************************************!*\
  !*** ./lib/proxiedServersComponent.js ***!
  \****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ProxiedServersComponent": () => (/* binding */ ProxiedServersComponent),
/* harmony export */   "Server": () => (/* binding */ Server)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__);
/*
 * proxiedServersComponent.tsx
 *
 * Copyright (C) 2022 by RStudio, PBC
 *
 */
// This file shares variables with './jupyterlab_rsw/constants.py'


const TitleComponent = (props) => {
    const headerId = ('title_component_' + props.title).replace(/\s+/g, '_');
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", null,
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("header", { id: headerId }, props.title)));
};
const ServerComponent = (props) => {
    const hyperlinkId = 'server_link_' + props.server.html_id;
    const liId = 'server_component_' + props.server.html_id;
    const serverNameId = 'server_name_' + props.server.html_id;
    const serverInfoId = 'server_info_' + props.server.html_id;
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(react__WEBPACK_IMPORTED_MODULE_0__.Fragment, { "aria-role": 'link', "aria-label": 'Open link for proxied server ' + props.server.label },
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("a", { id: hyperlinkId, target: "_blank", title: props.server.title, href: props.server.securePath },
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("li", { id: liId },
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__.launcherIcon.react, { paddingRight: 5 }),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("span", { id: serverNameId, className: 'jp-ServerName' }, props.server.label),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("span", { id: serverInfoId, className: 'jp-ServerInfo' },
                    props.server.ip,
                    ":",
                    props.server.port)))));
};
class ProxiedServersComponent extends react__WEBPACK_IMPORTED_MODULE_0__.Component {
    constructor(props) {
        super(props);
    }
    render() {
        const serverItems = this.props.servers.map((server) => react__WEBPACK_IMPORTED_MODULE_0___default().createElement(ServerComponent, { server: server }));
        return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(react__WEBPACK_IMPORTED_MODULE_0__.Fragment, null,
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(TitleComponent, { title: 'Proxied Servers' }),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", null,
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("ul", { id: 'proxied_servers_list' }, serverItems))));
    }
}
class Server {
    constructor(pid, name, port, ip, securePath) {
        this.pid = pid;
        this.label = name;
        this.port = port;
        this.ip = ip;
        this.securePath = securePath;
        this.title = securePath && securePath != '' ? securePath : 'Could not create secure url.';
        let id_str = this.label + '_' + port;
        id_str = id_str.replace(/\s+|-/g, '_'); // replace spaces with an underscore
        this.html_id = id_str.replace(/_+/g, '_'); // remove any duplicated underscores
    }
}
;


/***/ }),

/***/ "./lib/widget.js":
/*!***********************!*\
  !*** ./lib/widget.js ***!
  \***********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "RStudioWorkbenchWidget": () => (/* binding */ RStudioWorkbenchWidget)
/* harmony export */ });
/* harmony import */ var _constants__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./constants */ "./lib/constants.js");
/* harmony import */ var _handler__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./handler */ "./lib/handler.js");
/* harmony import */ var _proxiedServersComponent__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./proxiedServersComponent */ "./lib/proxiedServersComponent.js");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_2__);
/*
 * widget.tsx
 *
 * Copyright (C) 2022 by RStudio, PBC
 *
 */
// This file shares variables with './jupyterlab_rsw/constants.py'






function UseSignalComponent(props) {
    return react__WEBPACK_IMPORTED_MODULE_2___default().createElement(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.UseSignal, { signal: props.signal, initialArgs: props.servers }, (_, servers) => react__WEBPACK_IMPORTED_MODULE_2___default().createElement(_proxiedServersComponent__WEBPACK_IMPORTED_MODULE_3__.ProxiedServersComponent, { servers: servers }));
}
class RStudioWorkbenchWidget extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.ReactWidget {
    constructor() {
        super();
        this.servers = new Map();
        this._signal = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_1__.Signal(this);
        this._serverString = '';
        this._sessionUrl = '';
        this.addClass('jp-RStudioWorkbenchWidget');
    }
    getSessionUrl() {
        (0,_handler__WEBPACK_IMPORTED_MODULE_4__.requestAPI)(_constants__WEBPACK_IMPORTED_MODULE_5__.kUrlEndpoint).then((response) => {
            try {
                this._sessionUrl = response.baseSessionUrl;
            }
            catch (error) {
                console.log(`Received invalid response on GET /jupyterlab-rsw/url. \n${error}`);
            }
        }, (error) => {
            console.log(`Error on GET /jupyterlab-rsw/url. \n${error}`);
        });
    }
    requestServers() {
        (0,_handler__WEBPACK_IMPORTED_MODULE_4__.requestAPI)(_constants__WEBPACK_IMPORTED_MODULE_5__.kServerEndpoint).then((response) => {
            if (JSON.stringify(response.servers) != this._serverString) {
                this._serverString = JSON.stringify(response.servers);
                this.servers.clear();
                try {
                    response.servers.forEach((server) => {
                        this.servers.set(server.pid, [new _proxiedServersComponent__WEBPACK_IMPORTED_MODULE_3__.Server(server.pid, server.label, server.port, server.ip, `${this._sessionUrl}p/${server.secure_port}/`)]);
                    });
                    this._signal.emit(this.getServers());
                }
                catch (error) {
                    console.log(`Received invalid response on GET /jupyterlab-rsw/servers. \n${response}`);
                    return;
                }
            }
        }, (error) => {
            console.log(`Error on GET /jupyterlab-rsw/servers. \n${error}`);
        });
    }
    async onAfterAttach(msg) {
        super.onAfterAttach(msg);
        this.requestServers();
    }
    async onBeforeShow(msg) {
        super.onBeforeShow(msg);
        this.getSessionUrl();
        this.requestServers();
        this._timerID = setInterval(() => this.requestServers(), 3000);
    }
    onAfterHide(msg) {
        super.onAfterHide(msg);
        clearInterval(this._timerID);
    }
    getServers() {
        let serverArray = [];
        this.servers.forEach((value, key) => {
            serverArray = serverArray.concat(value);
        });
        return serverArray;
    }
    render() {
        return (react__WEBPACK_IMPORTED_MODULE_2___default().createElement(UseSignalComponent, { signal: this._signal, servers: this.getServers() }));
    }
}


/***/ }),

/***/ "./images/rstudio.svg":
/*!****************************!*\
  !*** ./images/rstudio.svg ***!
  \****************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ("<?xml version=\"1.0\" encoding=\"utf-8\"?>\n<!-- Generator: Adobe Illustrator 24.2.1, SVG Export Plug-In . SVG Version: 6.00 Build 0)  -->\n<svg version=\"1.1\" id=\"Layer_1\" xmlns=\"http://www.w3.org/2000/svg\" xmlns:xlink=\"http://www.w3.org/1999/xlink\" x=\"0px\" y=\"0px\"\n\t viewBox=\"0 0 215 215\" style=\"enable-background:new 0 0 215 215;\" xml:space=\"preserve\">\n<style type=\"text/css\">\n\t.st0{fill:#75AADB;}\n</style>\n<g>\n\t<path class=\"st0\" d=\"M129.5,80.4c0-12.1-8.8-16.9-20-16.9c-5.3,0-10.7,0.5-16.4,1.1v33.5l8.3,0.2C121.7,98.6,129.5,90.8,129.5,80.4\n\t\tz\"/>\n\t<path class=\"st0\" d=\"M107.5,1.5C49,1.5,1.5,49,1.5,107.5s47.5,106,106,106s106-47.5,106-106S166,1.5,107.5,1.5z M155.2,150.2h-17.6\n\t\tl-29.1-43.6H93.1v34.6h15.2v8.9H70.1v-8.9h13.1V64.5l-13.1-1.6v-8.5c5,1.1,9.3,1.9,14.7,1.9c8.1,0,16.4-1.9,24.6-1.9\n\t\tc15.8,0,30.5,7.2,30.5,24.8c0,13.6-8.1,22.2-20.8,25.9l24.6,36.2h11.5V150.2z\"/>\n</g>\n<g id=\"Black_Letters\">\n</g>\n<g id=\"Blue_Gradient_Letters\">\n</g>\n<g id=\"White_Letters\">\n</g>\n<g id=\"R_Ball\">\n</g>\n</svg>\n");

/***/ }),

/***/ "./images/rstudio_panel.svg":
/*!**********************************!*\
  !*** ./images/rstudio_panel.svg ***!
  \**********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ("<?xml version=\"1.0\" encoding=\"utf-8\"?>\n<!-- Generator: Adobe Illustrator 24.2.1, SVG Export Plug-In . SVG Version: 6.00 Build 0)  -->\n<svg version=\"1.1\" id=\"Layer_1\" xmlns=\"http://www.w3.org/2000/svg\" xmlns:xlink=\"http://www.w3.org/1999/xlink\" x=\"0px\" y=\"0px\"\n\t viewBox=\"0 0 215 215\" style=\"enable-background:new 0 0 215 215;\" xml:space=\"preserve\">\n<g>\n\t<path class=\"jp-icon3 jp-icon-selectable\" fill=\"#616161\" d=\"M129.5,80.4c0-12.1-8.8-16.9-20-16.9c-5.3,0-10.7,0.5-16.4,1.1v33.5l8.3,0.2C121.7,98.6,129.5,90.8,129.5,80.4\n\t\tz\"/>\n\t<path class=\"jp-icon3 jp-icon-selectable\" fill=\"#616161\" d=\"M107.5,1.5C49,1.5,1.5,49,1.5,107.5s47.5,106,106,106s106-47.5,106-106S166,1.5,107.5,1.5z M155.2,150.2h-17.6\n\t\tl-29.1-43.6H93.1v34.6h15.2v8.9H70.1v-8.9h13.1V64.5l-13.1-1.6v-8.5c5,1.1,9.3,1.9,14.7,1.9c8.1,0,16.4-1.9,24.6-1.9\n\t\tc15.8,0,30.5,7.2,30.5,24.8c0,13.6-8.1,22.2-20.8,25.9l24.6,36.2h11.5V150.2z\"/>\n</g>\n<g id=\"Black_Letters\">\n</g>\n<g id=\"Blue_Gradient_Letters\">\n</g>\n<g id=\"White_Letters\">\n</g>\n<g id=\"R_Ball\">\n</g>\n</svg>\n");

/***/ })

}]);
//# sourceMappingURL=lib_index_js.0f9e5472083ed8af3b75.js.map
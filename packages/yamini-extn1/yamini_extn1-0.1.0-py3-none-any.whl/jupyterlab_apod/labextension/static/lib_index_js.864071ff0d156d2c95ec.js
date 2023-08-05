"use strict";
(self["webpackChunkjupyterlab_apod"] = self["webpackChunkjupyterlab_apod"] || []).push([["lib_index_js"],{

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_1__);


;
/**
 * Initialization data for the jupyterlab_apod extension.
 */
const extension = {
    id: 'jupyterlab_apod',
    autoStart: true,
    requires: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.ICommandPalette],
    activate: async (app, palette) => {
        console.log('JupyterLab extension jupyterlab_apod is activated!');
        // Create a blank content widget inside of a MainAreaWidget
        const content = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_1__.Widget();
        content.addClass('my-apodWidget');
        const widget = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.MainAreaWidget({ content });
        widget.id = 'apod-jupyterlab';
        widget.title.label = 'Astronomy Picture';
        widget.title.closable = true;
        // Add an image element to the content
        let img = document.createElement('img');
        content.node.appendChild(img);
        let summary = document.createElement('p');
        content.node.appendChild(summary);
        // Get a random date string in YYYY-MM-DD format
        function randomDate() {
            const start = new Date(2010, 1, 1);
            const end = new Date();
            const randomDate = new Date(start.getTime() + Math.random() * (end.getTime() - start.getTime()));
            return randomDate.toISOString().slice(0, 10);
        }
        const response = await fetch(`https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY&date=${randomDate()}`);
        if (!response.ok) {
            const data = await response.json();
            if (data.error) {
                summary.innerText = data.error.message;
            }
            else {
                summary.innerText = response.statusText;
            }
        }
        else {
            const data = await response.json();
            if (data.media_type === 'image') {
                // Populate the image
                img.src = data.url;
                img.title = data.title;
                summary.innerText = data.title;
                if (data.copyright) {
                    summary.innerText += ` (Copyright ${data.copyright})`;
                }
            }
            else {
                summary.innerText = 'Random APOD fetched was not an image.';
            }
        }
        // Add an application command
        const command = 'apod:open';
        app.commands.addCommand(command, {
            label: 'Random Astronomy Picture',
            execute: () => {
                if (!widget.isAttached) {
                    // Attach the widget to the main work area if it's not there
                    app.shell.add(widget, 'main');
                }
                // Activate the widget
                app.shell.activateById(widget.id);
            }
        });
        // Add the command to the palette.
        palette.addItem({ command, category: 'Tutorial' });
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (extension);


/***/ })

}]);
//# sourceMappingURL=lib_index_js.864071ff0d156d2c95ec.js.map
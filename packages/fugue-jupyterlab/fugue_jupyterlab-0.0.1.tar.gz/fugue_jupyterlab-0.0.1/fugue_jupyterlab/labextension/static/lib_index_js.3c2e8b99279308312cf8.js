"use strict";
(self["webpackChunkfugue_jupyterlab"] = self["webpackChunkfugue_jupyterlab"] || []).push([["lib_index_js"],{

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _krassowski_jupyterlab_lsp__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @krassowski/jupyterlab-lsp */ "webpack/sharing/consume/default/@krassowski/jupyterlab-lsp");
/* harmony import */ var _krassowski_jupyterlab_lsp__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_krassowski_jupyterlab_lsp__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_codemirror__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/codemirror */ "webpack/sharing/consume/default/@jupyterlab/codemirror");
/* harmony import */ var _jupyterlab_codemirror__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_codemirror__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_fileeditor__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/fileeditor */ "webpack/sharing/consume/default/@jupyterlab/fileeditor");
/* harmony import */ var _jupyterlab_fileeditor__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_fileeditor__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _utils__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./utils */ "./lib/utils.js");






/*
Results in
LINE_MAGIC_EXTRACT
(?:^|\n)%sparksql(?: |-c|--cache|-e|--eager|-[a-z] [0-9a-zA-Z/._]+|--[a-zA-Z]+ [0-9a-zA-Z/._]+)*([^\n]*)
CELL_MAGIC_EXTRACT
(?:^|\n)%%sparksql(?: |-c|--cache|-e|--eager|-[a-z] [0-9a-zA-Z/._]+|--[a-zA-Z]+ [0-9a-zA-Z/._]+)*\n([^]*)
*/
/**
 * Code taken from https://github.com/jupyterlab/jupyterlab/blob/master/packages/codemirror/src/codemirror-ipython.ts
 * Modified to support embedded sql syntax
 */
function codeMirrorWithSqlSyntaxHighlightSupport(c) {
    /**
     * Define an IPython codemirror mode.
     *
     * It is a slightly altered Python Mode with a `?` operator.
     */
    (0,_utils__WEBPACK_IMPORTED_MODULE_5__.registerCodeMirrorFor)(c, 'fsql');
    c.CodeMirror.defineMode('ipython', (config, modeOptions) => {
        const pythonConf = {};
        for (const prop in modeOptions) {
            if (modeOptions.hasOwnProperty(prop)) {
                pythonConf[prop] = modeOptions[prop];
            }
        }
        pythonConf.name = 'python';
        pythonConf.singleOperators = new RegExp('^[\\+\\-\\*/%&|@\\^~<>!\\?]');
        pythonConf.identifiers = new RegExp('^[_A-Za-z\u00A1-\uFFFF][_A-Za-z0-9\u00A1-\uFFFF]*');
        //return c.CodeMirror.getMode(config, pythonConf);
        // Instead of returning this mode we multiplex it with SQL
        const pythonMode = c.CodeMirror.getMode(config, pythonConf);
        // get a mode for SQL
        const sqlMode = c.CodeMirror.getMode(config, 'fsql');
        // multiplex python with SQL and return it
        const multiplexedModes = (0,_utils__WEBPACK_IMPORTED_MODULE_5__.sqlCodeMirrorModesFor)('fsql', sqlMode);
        return c.CodeMirror.multiplexingMode(pythonMode, ...multiplexedModes);
    }
    // Original code has a third argument. Not sure why we don't..
    // https://github.com/jupyterlab/jupyterlab/blob/master/packages/codemirror/src/codemirror-ipython.ts
    // ,
    // 'python'
    );
}
/**
 * Initialization data for the jupyterlab_jc extension.
 */
const plugin = {
    id: 'fugue-jupyterlab:plugin',
    autoStart: true,
    optional: [],
    requires: [
        _jupyterlab_codemirror__WEBPACK_IMPORTED_MODULE_2__.ICodeMirror,
        _krassowski_jupyterlab_lsp__WEBPACK_IMPORTED_MODULE_1__.ILSPCodeExtractorsManager,
        _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_0__.ISettingRegistry,
        _jupyterlab_fileeditor__WEBPACK_IMPORTED_MODULE_4__.IEditorTracker,
        _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_3__.INotebookTracker
    ],
    activate: (app, codeMirror, lspExtractorsMgr, settingRegistry, editorTracker, tracker) => {
        /**
         * Load the settings for this extension
         *
         * @param setting Extension settings
         */
        /*function loadSetting(settings: ISettingRegistry.ISettings): void {
          // Read the settings and convert to the correct type
          const formatIndent = settings.get('formatIndent').composite as string;
          const formatUppercase = settings.get('formatUppercase').composite as boolean;
        }*/
        // Wait for the application to be restored and
        // for the settings for this plugin to be loaded
        /*Promise.all([app.restored, settingRegistry.load(Constants.SETTINGS_SECTION)])
          .then(([, settings]) => {
            // Read the settings
            loadSetting(settings);
            // Listen for your plugin setting changes using Signal
            settings.changed.connect(loadSetting);
    
          })
          .catch((reason) => {
            console.error(
              `Something went wrong when reading the settings.\n${reason}`
            );
          });*/
        // JupyterLab uses the CodeMirror library to syntax highlight code
        // within the cells. Register a multiplex CodeMirror capable of
        // highlightin SQL which is embedded in a IPython magic or within
        // a python string (delimited by markers)
        codeMirrorWithSqlSyntaxHighlightSupport(codeMirror);
        // JupyterLab-LSP relies on extractors to pull the SQL out of the cell
        // and into a virtual document which is then passed to the sql-language-server
        // for code completion evaluation
        lspExtractorsMgr.register((0,_utils__WEBPACK_IMPORTED_MODULE_5__.markerExtractor)('fsql'), 'python');
        lspExtractorsMgr.register((0,_utils__WEBPACK_IMPORTED_MODULE_5__.cellMagicExtractor)('fsql'), 'python');
        console.log('fugue-jupyterlab LSP extractors registered');
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);


/***/ }),

/***/ "./lib/utils.js":
/*!**********************!*\
  !*** ./lib/utils.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "cellMagicExtractor": () => (/* binding */ cellMagicExtractor),
/* harmony export */   "markerExtractor": () => (/* binding */ markerExtractor),
/* harmony export */   "registerCodeMirrorFor": () => (/* binding */ registerCodeMirrorFor),
/* harmony export */   "sqlCodeMirrorModesFor": () => (/* binding */ sqlCodeMirrorModesFor)
/* harmony export */ });
/* harmony import */ var _krassowski_jupyterlab_lsp__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @krassowski/jupyterlab-lsp */ "webpack/sharing/consume/default/@krassowski/jupyterlab-lsp");
/* harmony import */ var _krassowski_jupyterlab_lsp__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_krassowski_jupyterlab_lsp__WEBPACK_IMPORTED_MODULE_0__);

function cell_magic(language) {
    return `%%${language}`;
}
function start(language) {
    return `--start-${language}`;
}
function end(language) {
    return `--end-${language}`;
}
const BEGIN = '(?:^|\n)';
function sqlCodeMirrorModesFor(language, sqlMode) {
    return [
        {
            open: `${start(language)}`,
            close: `${end(language)}`,
            // parseDelimiters is set to true which considers
            // the marker as part of the SQL statement
            // it is thus syntax highlighted as a comment
            parseDelimiters: true,
            mode: sqlMode
        },
        {
            open: RegExp(`${cell_magic(language)}`),
            close: '__A MARKER THAT WILL NEVER BE MATCHED__',
            parseDelimiters: false,
            mode: sqlMode
        }
    ];
}
function cellMagicExtractor(language) {
    return new _krassowski_jupyterlab_lsp__WEBPACK_IMPORTED_MODULE_0__.RegExpForeignCodeExtractor({
        language: language,
        pattern: `${BEGIN}${cell_magic(language)}\n([^]*)`,
        foreign_capture_groups: [1],
        is_standalone: true,
        file_extension: language
    });
}
function markerExtractor(language) {
    return new _krassowski_jupyterlab_lsp__WEBPACK_IMPORTED_MODULE_0__.RegExpForeignCodeExtractor({
        language: language,
        pattern: `${start(language)}.*?\n([^]*?)${end(language)}`,
        foreign_capture_groups: [1],
        is_standalone: true,
        file_extension: language
    });
}
function set(str) {
    const obj = {}, words = str.split(' ');
    for (let i = 0; i < words.length; ++i) {
        obj[words[i]] = true;
    }
    return obj;
}
const fugue_keywords = 'fill hash rand even presort persist broadcast params process output outtransform rowcount concurrency prepartition zip print title save append parquet csv json single checkpoint weak strong deterministic yield connect sample seed take sub callback dataframe file';
/**
 * Register text editor based on file type.
 * @param c
 * @param language
 */
function registerCodeMirrorFor(c, language) {
    c.CodeMirror.defineMode(language, (config, modeOptions) => {
        const mode = c.CodeMirror.getMode(config, {
            name: 'sql',
            keywords: set(fugue_keywords +
                ' add after all alter analyze and anti archive array as asc at between bucket buckets by cache cascade case cast change clear cluster clustered codegen collection column columns comment commit compact compactions compute concatenate cost create cross cube current current_date current_timestamp database databases data dbproperties defined delete delimited deny desc describe dfs directories distinct distribute drop else end escaped except exchange exists explain export extended external false fields fileformat first following for format formatted from full function functions global grant group grouping having if ignore import in index indexes inner inpath inputformat insert intersect interval into is items join keys last lateral lazy left like limit lines list load local location lock locks logical macro map minus msck natural no not null nulls of on optimize option options or order out outer outputformat over overwrite partition partitioned partitions percent preceding principals purge range recordreader recordwriter recover reduce refresh regexp rename repair replace reset restrict revoke right rlike role roles rollback rollup row rows schema schemas select semi separated serde serdeproperties set sets show skewed sort sorted start statistics stored stratify struct table tables tablesample tblproperties temp temporary terminated then to touch transaction transactions transform true truncate unarchive unbounded uncache union unlock unset use using values view when where window with'),
            builtin: set('date datetime tinyint smallint int bigint boolean float double string binary timestamp decimal array map struct uniontype delimited serde sequencefile textfile rcfile inputformat outputformat'),
            atoms: set('false true null'),
            operatorChars: /^[*\/+\-%<>!=~&|^]/,
            dateSQL: set('time'),
            support: set('ODBCdotTable doubleQuote zerolessFloat')
        });
        return mode;
    });
    c.CodeMirror.defineMIME(`text/x-${language}`, language);
    c.CodeMirror.modeInfo.push({
        ext: [language],
        mime: `text/x-${language}`,
        mode: language,
        name: language
    });
}


/***/ })

}]);
//# sourceMappingURL=lib_index_js.3c2e8b99279308312cf8.js.map
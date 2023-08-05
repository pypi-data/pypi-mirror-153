/******/ (() => { // webpackBootstrap
/******/ 	"use strict";
/******/ 	var __webpack_modules__ = ({

/***/ 16737:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "mG": () => (/* binding */ formatSelectOptions),
/* harmony export */   "n_": () => (/* binding */ getDatasourceParameter)
/* harmony export */ });
/* unused harmony export mainMetric */
/**
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 * KIND, either express or implied.  See the License for the
 * specific language governing permissions and limitations
 * under the License.
 */
/* eslint camelcase: 0 */

function formatSelectOptions(options) {
  return options.map((opt) => [opt, opt.toString()]);
}

function getDatasourceParameter(datasourceId, datasourceType) {
  return `${datasourceId}__${datasourceType}`;
}

function mainMetric(savedMetrics) {
  // Using 'count' as default metric if it exists, otherwise using whatever one shows up first
  let metric;
  if (savedMetrics && savedMetrics.length > 0) {
    savedMetrics.forEach((m) => {
      if (m.metric_name === 'count') {
        metric = 'count';
      }
    });
    if (!metric) {
      metric = savedMetrics[0].metric_name;
    }
  }
  return metric;
}

/***/ }),

/***/ 42669:
/***/ ((__unused_webpack_module, __unused_webpack___webpack_exports__, __webpack_require__) => {


// EXTERNAL MODULE: ./node_modules/react/index.js
var react = __webpack_require__(67294);
// EXTERNAL MODULE: ./node_modules/@hot-loader/react-dom/index.js
var react_dom = __webpack_require__(9060);
// EXTERNAL MODULE: ./node_modules/@emotion/react/dist/emotion-element-99289b21.browser.esm.js + 2 modules
var emotion_element_99289b21_browser_esm = __webpack_require__(68135);
// EXTERNAL MODULE: ./src/setup/setupApp.ts + 6 modules
var setupApp = __webpack_require__(84153);
// EXTERNAL MODULE: ./src/setup/setupPlugins.ts + 38 modules
var setupPlugins = __webpack_require__(69753);
// EXTERNAL MODULE: ./src/components/DynamicPlugins/index.tsx
var DynamicPlugins = __webpack_require__(14278);
// EXTERNAL MODULE: ./node_modules/rison/js/rison.js
var rison = __webpack_require__(15926);
var rison_default = /*#__PURE__*/__webpack_require__.n(rison);
// EXTERNAL MODULE: ./node_modules/@superset-ui/core/esm/style/index.js
var style = __webpack_require__(37840);
// EXTERNAL MODULE: ./node_modules/@superset-ui/core/esm/connection/SupersetClient.js
var SupersetClient = __webpack_require__(21173);
// EXTERNAL MODULE: ./node_modules/@superset-ui/core/esm/translation/TranslatorSingleton.js + 1 modules
var TranslatorSingleton = __webpack_require__(60650);
// EXTERNAL MODULE: ./src/common/components/index.tsx
var components = __webpack_require__(82191);
// EXTERNAL MODULE: ./src/components/Button/index.tsx
var Button = __webpack_require__(35932);
// EXTERNAL MODULE: ./src/components/index.ts + 1 modules
var src_components = __webpack_require__(33346);
// EXTERNAL MODULE: ./src/components/Form/index.tsx + 1 modules
var Form = __webpack_require__(49238);
// EXTERNAL MODULE: ./src/components/Tooltip/index.tsx
var Tooltip = __webpack_require__(58593);
// EXTERNAL MODULE: ./src/explore/components/controls/VizTypeControl/VizTypeGallery.tsx
var VizTypeGallery = __webpack_require__(13284);
// EXTERNAL MODULE: ./node_modules/@emotion/react/dist/emotion-react.browser.esm.js + 1 modules
var emotion_react_browser_esm = __webpack_require__(11965);
;// CONCATENATED MODULE: ./src/addSlice/AddSliceContainer.tsx
/**
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 * KIND, either express or implied.  See the License for the
 * specific language governing permissions and limitations
 * under the License.
 */









const ESTIMATED_NAV_HEIGHT = 56;
const ELEMENTS_EXCEPT_VIZ_GALLERY = ESTIMATED_NAV_HEIGHT + 250;
const StyledContainer = style/* styled.div */.iK.div`
  ${({ theme }) => `
    flex: 1 1 auto;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    width: 100%;
    max-width: ${VizTypeGallery/* MAX_ADVISABLE_VIZ_GALLERY_WIDTH */.UB}px;
    max-height: calc(100vh - ${ESTIMATED_NAV_HEIGHT}px);
    border-radius: ${theme.gridUnit}px;
    background-color: ${theme.colors.grayscale.light5};
    margin-left: auto;
    margin-right: auto;
    padding-left: ${theme.gridUnit * 4}px;
    padding-right: ${theme.gridUnit * 4}px;
    padding-bottom: ${theme.gridUnit * 4}px;

    h3 {
      padding-bottom: ${theme.gridUnit * 3}px;
    }

    & .dataset {
      display: flex;
      flex-direction: row;
      align-items: center;
      margin-bottom: ${theme.gridUnit * 2}px;

      & > div {
        min-width: 200px;
        width: 300px;
      }

      & > span {
        color: ${theme.colors.grayscale.light1};
        margin-left: ${theme.gridUnit * 4}px;
      }
    }

    & .viz-gallery {
      border: 1px solid ${theme.colors.grayscale.light2};
      border-radius: ${theme.gridUnit}px;
      margin: ${theme.gridUnit}px 0px;
      max-height: calc(100vh - ${ELEMENTS_EXCEPT_VIZ_GALLERY}px);
      flex: 1;
    }

    & .footer {
      flex: 1;
      display: flex;
      flex-direction: row;
      justify-content: flex-end;
      align-items: center;

      & > span {
        color: ${theme.colors.grayscale.light1};
        margin-right: ${theme.gridUnit * 4}px;
      }
    }

    /* The following extra ampersands (&&&&) are used to boost selector specificity */

    &&&& .ant-steps-item-tail {
      display: none;
    }

    &&&& .ant-steps-item-icon {
      margin-right: ${theme.gridUnit * 2}px;
      width: ${theme.gridUnit * 5}px;
      height: ${theme.gridUnit * 5}px;
      line-height: ${theme.gridUnit * 5}px;
    }

    &&&& .ant-steps-item-title {
      line-height: ${theme.gridUnit * 5}px;
    }

    &&&& .ant-steps-item-content {
      overflow: unset;

      .ant-steps-item-description {
        margin-top: ${theme.gridUnit}px;
      }
    }

    &&&& .ant-tooltip-open {
      display: inline;
    }

    &&&& .ant-select-selector {
      padding: 0;
    }

    &&&& .ant-select-selection-placeholder {
      padding-left: ${theme.gridUnit * 3}px;
    }
  `}
`;
const TooltipContent = style/* styled.div */.iK.div`
  ${({ theme, hasDescription }) => `
    .tooltip-header {
      font-size: ${hasDescription ? theme.typography.sizes.l : theme.typography.sizes.s}px;
      font-weight: ${hasDescription ?
theme.typography.weights.bold :
theme.typography.weights.normal};
    }

    .tooltip-description {
      margin-top: ${theme.gridUnit * 2}px;
      display: -webkit-box;
      -webkit-line-clamp: 20;
      -webkit-box-orient: vertical;
      overflow: hidden;
      text-overflow: ellipsis;
    }
  `}
`;
const StyledLabel = style/* styled.span */.iK.span`
  ${({ theme }) => `
    position: absolute;
    left: ${theme.gridUnit * 3}px;
    right: ${theme.gridUnit * 3}px;
    overflow: hidden;
    text-overflow: ellipsis;
  `}
`;
class AddSliceContainer extends react.PureComponent {
  constructor(props) {
    super(props);
    this.state = {
      visType: null };

    this.changeDatasource = this.changeDatasource.bind(this);
    this.changeVisType = this.changeVisType.bind(this);
    this.gotoSlice = this.gotoSlice.bind(this);
    this.newLabel = this.newLabel.bind(this);
    this.loadDatasources = this.loadDatasources.bind(this);
  }
  exploreUrl() {var _this$state$datasourc;
    const formData = encodeURIComponent(JSON.stringify({
      viz_type: this.state.visType,
      datasource: (_this$state$datasourc = this.state.datasource) == null ? void 0 : _this$state$datasourc.value }));

    return `/superset/explore/?form_data=${formData}`;
  }
  gotoSlice() {
    window.location.href = this.exploreUrl();
  }
  changeDatasource(datasource) {
    this.setState({ datasource });
  }
  changeVisType(visType) {
    this.setState({ visType });
  }
  isBtnDisabled() {var _this$state$datasourc2;
    return !((_this$state$datasourc2 = this.state.datasource) != null && _this$state$datasourc2.value && this.state.visType);
  }
  newLabel(item) {
    return (0,emotion_react_browser_esm.jsx)(Tooltip/* Tooltip */.u, { mouseEnterDelay: 1, placement: "right", title: (0,emotion_react_browser_esm.jsx)(TooltipContent, { hasDescription: !!item.description },
      (0,emotion_react_browser_esm.jsx)("div", { className: "tooltip-header" }, item.table_name),
      item.description && (0,emotion_react_browser_esm.jsx)("div", { className: "tooltip-description" }, item.description)) },

    (0,emotion_react_browser_esm.jsx)(StyledLabel, null, item.table_name));

  }
  loadDatasources(search, page, pageSize) {
    const query = rison_default().encode({
      columns: ['id', 'table_name', 'description', 'datasource_type'],
      filters: [{ col: 'table_name', opr: 'ct', value: search }],
      page,
      page_size: pageSize,
      order_column: 'table_name',
      order_direction: 'asc' });

    return SupersetClient/* default.get */.Z.get({
      endpoint: `/api/v1/dataset/?q=${query}` }).
    then((response) => {
      const list = response.json.result.
      map((item) => ({
        value: `${item.id}__${item.datasource_type}`,
        customLabel: this.newLabel(item),
        label: item.table_name })).

      sort((a, b) => a.label.localeCompare(b.label));
      return {
        data: list,
        totalCount: response.json.count };

    });
  }
  render() {var _this$state$datasourc3;
    const isButtonDisabled = this.isBtnDisabled();
    return (0,emotion_react_browser_esm.jsx)(StyledContainer, null,
    (0,emotion_react_browser_esm.jsx)("h3", null, (0,TranslatorSingleton.t)('Create a new chart')),
    (0,emotion_react_browser_esm.jsx)(components/* Steps */.Rg, { direction: "vertical", size: "small" },
    (0,emotion_react_browser_esm.jsx)(components/* Steps.Step */.Rg.Step, { title: (0,emotion_react_browser_esm.jsx)(Form/* FormLabel */.lX, null, (0,TranslatorSingleton.t)('Choose a dataset')), status: (_this$state$datasourc3 = this.state.datasource) != null && _this$state$datasourc3.value ? 'finish' : 'process', description: (0,emotion_react_browser_esm.jsx)("div", { className: "dataset" },
      (0,emotion_react_browser_esm.jsx)(src_components/* Select */.P, { autoFocus: true, ariaLabel: (0,TranslatorSingleton.t)('Dataset'), name: "select-datasource", onChange: this.changeDatasource, options: this.loadDatasources, placeholder: (0,TranslatorSingleton.t)('Choose a dataset'), showSearch: true, value: this.state.datasource }),
      (0,emotion_react_browser_esm.jsx)("span", null,
      (0,TranslatorSingleton.t)('Instructions to add a dataset are available in the Superset tutorial.'), ' ',
      (0,emotion_react_browser_esm.jsx)("a", { href: "https://superset.apache.org/docs/creating-charts-dashboards/first-dashboard#adding-a-new-table", rel: "noopener noreferrer", target: "_blank" },
      (0,emotion_react_browser_esm.jsx)("i", { className: "fa fa-external-link" })))) }),



    (0,emotion_react_browser_esm.jsx)(components/* Steps.Step */.Rg.Step, { title: (0,emotion_react_browser_esm.jsx)(Form/* FormLabel */.lX, null, (0,TranslatorSingleton.t)('Choose chart type')), status: this.state.visType ? 'finish' : 'process', description: (0,emotion_react_browser_esm.jsx)(VizTypeGallery/* default */.ZP, { className: "viz-gallery", onChange: this.changeVisType, selectedViz: this.state.visType }) })),

    (0,emotion_react_browser_esm.jsx)("div", { className: "footer" },
    isButtonDisabled && (0,emotion_react_browser_esm.jsx)("span", null,
    (0,TranslatorSingleton.t)('Please select both a Dataset and a Chart type to proceed')),

    (0,emotion_react_browser_esm.jsx)(Button/* default */.Z, { buttonStyle: "primary", disabled: isButtonDisabled, onClick: this.gotoSlice },
    (0,TranslatorSingleton.t)('Create new chart'))));



  }}
// EXTERNAL MODULE: ./src/featureFlags.ts
var featureFlags = __webpack_require__(91877);
// EXTERNAL MODULE: ./src/preamble.ts + 3 modules
var preamble = __webpack_require__(26009);
;// CONCATENATED MODULE: ./src/addSlice/App.tsx
/**
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 * KIND, either express or implied.  See the License for the
 * specific language governing permissions and limitations
 * under the License.
 */









(0,setupApp/* default */.Z)();
(0,setupPlugins/* default */.Z)();
const addSliceContainer = document.getElementById('app');
const bootstrapData = JSON.parse((addSliceContainer == null ? void 0 : addSliceContainer.getAttribute('data-bootstrap')) || '{}');
(0,featureFlags/* initFeatureFlags */.fG)(bootstrapData.common.feature_flags);
const App = () => (0,emotion_react_browser_esm.jsx)(emotion_element_99289b21_browser_esm.a, { theme: preamble/* theme */.r },
(0,emotion_react_browser_esm.jsx)(DynamicPlugins/* DynamicPluginProvider */.EM, null,
(0,emotion_react_browser_esm.jsx)(AddSliceContainer, null)));


/* harmony default export */ const addSlice_App = (App);
;// CONCATENATED MODULE: ./src/addSlice/index.tsx
/**
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 * KIND, either express or implied.  See the License for the
 * specific language governing permissions and limitations
 * under the License.
 */



react_dom.render((0,emotion_react_browser_esm.jsx)(addSlice_App, null), document.getElementById('app'));

/***/ }),

/***/ 14278:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "Zn": () => (/* binding */ PluginContext),
/* harmony export */   "gp": () => (/* binding */ usePluginContext),
/* harmony export */   "EM": () => (/* binding */ DynamicPluginProvider)
/* harmony export */ });
/* harmony import */ var lodash_omitBy__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(14176);
/* harmony import */ var lodash_omitBy__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(lodash_omitBy__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(67294);
/* harmony import */ var _superset_ui_core__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(38849);
/* harmony import */ var _superset_ui_core__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(85639);
/* harmony import */ var _superset_ui_core__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(17390);
/* harmony import */ var _superset_ui_core__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(23099);
/* harmony import */ var src_featureFlags__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(91877);
/* harmony import */ var src_featureFlags__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(46415);
/* harmony import */ var _emotion_react__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(11965);
 /**
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 * KIND, either express or implied.  See the License for the
 * specific language governing permissions and limitations
 * under the License.
 */




const metadataRegistry = (0,_superset_ui_core__WEBPACK_IMPORTED_MODULE_2__/* ["default"] */ .Z)();
const dummyPluginContext = {
  loading: true,
  dynamicPlugins: {},
  keys: [],
  mountedPluginMetadata: {},
  fetchAll: () => {} };

/**
 * It is highly recommended to use the usePluginContext hook instead.
 * @see usePluginContext
 */
const PluginContext = /*#__PURE__*/react__WEBPACK_IMPORTED_MODULE_1__.createContext(dummyPluginContext);
/**
 * The plugin context provides info about what dynamic plugins are available.
 * It also provides loading info for the plugins' javascript bundles.
 *
 * Note: This does not include any information about static plugins.
 * Those are compiled into the Superset bundle at build time.
 * Dynamic plugins are added by the end user and can be any webhosted javascript.
 */
const usePluginContext = () => (0,react__WEBPACK_IMPORTED_MODULE_1__.useContext)(PluginContext);
function getRegistryData() {
  return {
    keys: metadataRegistry.keys(),
    mountedPluginMetadata: lodash_omitBy__WEBPACK_IMPORTED_MODULE_0___default()(metadataRegistry.getMap(), (value) => value === undefined) // cast required to get rid of undefined values
  };
}
function pluginContextReducer(state, action) {
  switch (action.type) {
    case 'begin':{
        const plugins = { ...state.dynamicPlugins };
        action.keys.forEach((key) => {
          plugins[key] = { key, error: null, mounting: true };
        });
        return {
          ...state,
          loading: action.keys.length > 0,
          dynamicPlugins: plugins };

      }
    case 'complete':{
        return {
          ...state,
          loading: Object.values(state.dynamicPlugins).some((plugin) => plugin.mounting && plugin.key !== action.key),
          dynamicPlugins: {
            ...state.dynamicPlugins,
            [action.key]: {
              key: action.key,
              mounting: false,
              error: action.error } } };



      }
    case 'changed keys':{
        return {
          ...state,
          ...getRegistryData() };

      }
    default:
      return state;}

}
const pluginApi = (0,_superset_ui_core__WEBPACK_IMPORTED_MODULE_3__/* ["default"] */ .Z)({
  method: 'GET',
  endpoint: '/dynamic-plugins/api/read' });

const sharedModules = {
  react: () => Promise.resolve(/* import() */).then(__webpack_require__.t.bind(__webpack_require__, 67294, 19)),
  lodash: () => Promise.resolve(/* import() */).then(__webpack_require__.t.bind(__webpack_require__, 96486, 23)),
  'react-dom': () => Promise.resolve(/* import() */).then(__webpack_require__.t.bind(__webpack_require__, 9060, 19)),
  '@superset-ui/chart-controls': () => Promise.all(/* import() */[__webpack_require__.e(1216), __webpack_require__.e(7211), __webpack_require__.e(7017), __webpack_require__.e(8483), __webpack_require__.e(5042)]).then(__webpack_require__.bind(__webpack_require__, 88483)),
  '@superset-ui/core': () => Promise.all(/* import() */[__webpack_require__.e(1216), __webpack_require__.e(7211), __webpack_require__.e(7017), __webpack_require__.e(6439)]).then(__webpack_require__.bind(__webpack_require__, 67017)) };

const DynamicPluginProvider = ({ children }) => {
  const [pluginState, dispatch] = (0,react__WEBPACK_IMPORTED_MODULE_1__.useReducer)(pluginContextReducer, dummyPluginContext, (state) => ({
    ...state,
    ...getRegistryData(),
    // eslint-disable-next-line @typescript-eslint/no-use-before-define
    fetchAll,
    loading: (0,src_featureFlags__WEBPACK_IMPORTED_MODULE_4__/* .isFeatureEnabled */ .cr)(src_featureFlags__WEBPACK_IMPORTED_MODULE_5__/* .FeatureFlag.DYNAMIC_PLUGINS */ .T.DYNAMIC_PLUGINS)
    // TODO: Write fetchByKeys
  }));
  // For now, we fetch all the plugins at the same time.
  // In the future it would be nice to fetch on an as-needed basis.
  // That will most likely depend on having a json manifest for each plugin.
  async function fetchAll() {
    try {
      await (0,_superset_ui_core__WEBPACK_IMPORTED_MODULE_6__/* .defineSharedModules */ .YW)(sharedModules);
      const { result: plugins } = await pluginApi({});
      dispatch({ type: 'begin', keys: plugins.map((plugin) => plugin.key) });
      await Promise.all(plugins.map(async (plugin) => {
        let error = null;
        try {
          await import( /* webpackIgnore: true */plugin.bundle_url);
        }
        catch (err) {
          _superset_ui_core__WEBPACK_IMPORTED_MODULE_7__/* ["default"].error */ .Z.error(`Failed to load plugin ${plugin.key} with the following error:`, err.stack);
          error = err;
        }
        dispatch({
          type: 'complete',
          key: plugin.key,
          error });

      }));
    }
    catch (error) {
      _superset_ui_core__WEBPACK_IMPORTED_MODULE_7__/* ["default"].error */ .Z.error('Failed to load dynamic plugins', error.stack || error);
    }
  }
  (0,react__WEBPACK_IMPORTED_MODULE_1__.useEffect)(() => {
    if ((0,src_featureFlags__WEBPACK_IMPORTED_MODULE_4__/* .isFeatureEnabled */ .cr)(src_featureFlags__WEBPACK_IMPORTED_MODULE_5__/* .FeatureFlag.DYNAMIC_PLUGINS */ .T.DYNAMIC_PLUGINS)) {
      fetchAll();
    }
    const registryListener = () => {
      dispatch({ type: 'changed keys' });
    };
    metadataRegistry.addListener(registryListener);
    return () => {
      metadataRegistry.removeListener(registryListener);
    };
  }, []);
  return (0,_emotion_react__WEBPACK_IMPORTED_MODULE_8__.jsx)(PluginContext.Provider, { value: pluginState },
  children);

};

/***/ }),

/***/ 1510:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "zi": () => (/* binding */ getFormData),
/* harmony export */   "on": () => (/* binding */ mergeExtraFormData),
/* harmony export */   "vk": () => (/* binding */ getExtraFormData),
/* harmony export */   "X3": () => (/* binding */ nativeFilterGate),
/* harmony export */   "Rz": () => (/* binding */ findTabsWithChartsInScope)
/* harmony export */ });
/* unused harmony export isCrossFilter */
/* harmony import */ var _superset_ui_core__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(92134);
/* harmony import */ var _superset_ui_core__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(52686);
/* harmony import */ var _superset_ui_core__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(46415);
/* harmony import */ var src_dashboard_util_extractUrlParams__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(70400);
/* harmony import */ var src_featureFlags__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(91877);
/* harmony import */ var _util_componentTypes__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(81255);
/* harmony import */ var _util_constants__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(80621);
/**
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 * KIND, either express or implied.  See the License for the
 * specific language governing permissions and limitations
 * under the License.
 */





const getFormData = ({ datasetId, cascadingFilters = {}, groupby, inputRef, defaultDataMask, controlValues, filterType, sortMetric, adhoc_filters, time_range, granularity_sqla, type }) => {var _defaultDataMask$filt;
  const otherProps = {};
  if (datasetId) {
    otherProps.datasource = `${datasetId}__table`;
  }
  if (groupby) {
    otherProps.groupby = [groupby];
  }
  if (sortMetric) {
    otherProps.sortMetric = sortMetric;
  }
  return {
    ...controlValues,
    ...otherProps,
    adhoc_filters: adhoc_filters != null ? adhoc_filters : [],
    extra_filters: [],
    extra_form_data: cascadingFilters,
    granularity_sqla,
    metrics: ['count'],
    row_limit: 1000,
    showSearch: true,
    defaultValue: defaultDataMask == null ? void 0 : (_defaultDataMask$filt = defaultDataMask.filterState) == null ? void 0 : _defaultDataMask$filt.value,
    time_range,
    time_range_endpoints: ['inclusive', 'exclusive'],
    url_params: (0,src_dashboard_util_extractUrlParams__WEBPACK_IMPORTED_MODULE_0__/* ["default"] */ .Z)('regular'),
    inView: true,
    viz_type: filterType,
    inputRef,
    type };

};
function mergeExtraFormData(originalExtra = {}, newExtra = {}) {
  const mergedExtra = {};
  _superset_ui_core__WEBPACK_IMPORTED_MODULE_3__/* .EXTRA_FORM_DATA_APPEND_KEYS.forEach */ .Ci.forEach((key) => {
    const mergedValues = [
    ...(originalExtra[key] || []),
    ...(newExtra[key] || [])];

    if (mergedValues.length) {
      mergedExtra[key] = mergedValues;
    }
  });
  _superset_ui_core__WEBPACK_IMPORTED_MODULE_3__/* .EXTRA_FORM_DATA_OVERRIDE_KEYS.forEach */ .Ay.forEach((key) => {
    const originalValue = originalExtra[key];
    if (originalValue !== undefined) {
      mergedExtra[key] = originalValue;
    }
    const newValue = newExtra[key];
    if (newValue !== undefined) {
      mergedExtra[key] = newValue;
    }
  });
  return mergedExtra;
}
function isCrossFilter(vizType) {var _getChartMetadataRegi, _getChartMetadataRegi2;
  // @ts-ignore need export from superset-ui `ItemWithValue`
  return (_getChartMetadataRegi = getChartMetadataRegistry().items[vizType]) == null ? void 0 : (_getChartMetadataRegi2 = _getChartMetadataRegi.value.behaviors) == null ? void 0 : _getChartMetadataRegi2.includes(Behavior.INTERACTIVE_CHART);
}
function getExtraFormData(dataMask, charts, filterIdsAppliedOnChart) {
  let extraFormData = {};
  filterIdsAppliedOnChart.forEach((key) => {var _dataMask$key$extraFo, _dataMask$key;
    extraFormData = mergeExtraFormData(extraFormData, (_dataMask$key$extraFo = (_dataMask$key = dataMask[key]) == null ? void 0 : _dataMask$key.extraFormData) != null ? _dataMask$key$extraFo : {});
  });
  return extraFormData;
}
function nativeFilterGate(behaviors) {
  return !behaviors.includes(_superset_ui_core__WEBPACK_IMPORTED_MODULE_4__/* .Behavior.NATIVE_FILTER */ .cg.NATIVE_FILTER) ||
  (0,src_featureFlags__WEBPACK_IMPORTED_MODULE_5__/* .isFeatureEnabled */ .cr)(_superset_ui_core__WEBPACK_IMPORTED_MODULE_6__/* .FeatureFlag.DASHBOARD_FILTERS_EXPERIMENTAL */ .T.DASHBOARD_FILTERS_EXPERIMENTAL) &&
  (0,src_featureFlags__WEBPACK_IMPORTED_MODULE_5__/* .isFeatureEnabled */ .cr)(_superset_ui_core__WEBPACK_IMPORTED_MODULE_6__/* .FeatureFlag.DASHBOARD_CROSS_FILTERS */ .T.DASHBOARD_CROSS_FILTERS) &&
  behaviors.includes(_superset_ui_core__WEBPACK_IMPORTED_MODULE_4__/* .Behavior.INTERACTIVE_CHART */ .cg.INTERACTIVE_CHART);
}
const isComponentATab = (dashboardLayout, componentId) => dashboardLayout[componentId].type === _util_componentTypes__WEBPACK_IMPORTED_MODULE_1__/* .TAB_TYPE */ .gn;
const findTabsWithChartsInScopeHelper = (dashboardLayout, chartsInScope, componentId, tabIds, tabsToHighlight) => {
  if (dashboardLayout[componentId].type === _util_componentTypes__WEBPACK_IMPORTED_MODULE_1__/* .CHART_TYPE */ .dW &&
  chartsInScope.includes(dashboardLayout[componentId].meta.chartId)) {
    tabIds.forEach(tabsToHighlight.add, tabsToHighlight);
  }
  if (dashboardLayout[componentId].children.length === 0 ||
  isComponentATab(dashboardLayout, componentId) &&
  tabsToHighlight.has(componentId)) {
    return;
  }
  dashboardLayout[componentId].children.forEach((childId) => findTabsWithChartsInScopeHelper(dashboardLayout, chartsInScope, childId, isComponentATab(dashboardLayout, childId) ? [...tabIds, childId] : tabIds, tabsToHighlight));
};
const findTabsWithChartsInScope = (dashboardLayout, chartsInScope) => {
  const dashboardRoot = dashboardLayout[_util_constants__WEBPACK_IMPORTED_MODULE_2__/* .DASHBOARD_ROOT_ID */ ._4];
  const rootChildId = dashboardRoot.children[0];
  const hasTopLevelTabs = rootChildId !== _util_constants__WEBPACK_IMPORTED_MODULE_2__/* .DASHBOARD_GRID_ID */ .PV;
  const tabsInScope = new Set();
  if (hasTopLevelTabs) {var _dashboardLayout$root;
    (_dashboardLayout$root = dashboardLayout[rootChildId].children) == null ? void 0 : _dashboardLayout$root.forEach((tabId) => findTabsWithChartsInScopeHelper(dashboardLayout, chartsInScope, tabId, [tabId], tabsInScope));
  } else
  {
    Object.values(dashboardLayout).
    filter((element) => element.type === _util_componentTypes__WEBPACK_IMPORTED_MODULE_1__/* .TAB_TYPE */ .gn).
    forEach((element) => findTabsWithChartsInScopeHelper(dashboardLayout, chartsInScope, element.id, [element.id], tabsInScope));
  }
  return tabsInScope;
};

/***/ }),

/***/ 81255:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "dW": () => (/* binding */ CHART_TYPE),
/* harmony export */   "BA": () => (/* binding */ COLUMN_TYPE),
/* harmony export */   "Vl": () => (/* binding */ DASHBOARD_HEADER_TYPE),
/* harmony export */   "BG": () => (/* binding */ DASHBOARD_GRID_TYPE),
/* harmony export */   "U0": () => (/* binding */ DASHBOARD_ROOT_TYPE),
/* harmony export */   "hE": () => (/* binding */ DIVIDER_TYPE),
/* harmony export */   "Nc": () => (/* binding */ HEADER_TYPE),
/* harmony export */   "xh": () => (/* binding */ MARKDOWN_TYPE),
/* harmony export */   "F0": () => (/* binding */ NEW_COMPONENT_SOURCE_TYPE),
/* harmony export */   "Os": () => (/* binding */ ROW_TYPE),
/* harmony export */   "yR": () => (/* binding */ TABS_TYPE),
/* harmony export */   "gn": () => (/* binding */ TAB_TYPE),
/* harmony export */   "ZP": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/**
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 * KIND, either express or implied.  See the License for the
 * specific language governing permissions and limitations
 * under the License.
 */
const CHART_TYPE = 'CHART';
const COLUMN_TYPE = 'COLUMN';
const DASHBOARD_HEADER_TYPE = 'HEADER';
const DASHBOARD_GRID_TYPE = 'GRID';
const DASHBOARD_ROOT_TYPE = 'ROOT';
const DIVIDER_TYPE = 'DIVIDER';
const HEADER_TYPE = 'HEADER';
const MARKDOWN_TYPE = 'MARKDOWN';
const NEW_COMPONENT_SOURCE_TYPE = 'NEW_COMPONENT_SOURCE';
const ROW_TYPE = 'ROW';
const TABS_TYPE = 'TABS';
const TAB_TYPE = 'TAB';
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ({
  CHART_TYPE,
  COLUMN_TYPE,
  DASHBOARD_HEADER_TYPE,
  DASHBOARD_GRID_TYPE,
  DASHBOARD_ROOT_TYPE,
  DIVIDER_TYPE,
  HEADER_TYPE,
  MARKDOWN_TYPE,
  NEW_COMPONENT_SOURCE_TYPE,
  ROW_TYPE,
  TABS_TYPE,
  TAB_TYPE });

/***/ }),

/***/ 70400:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "Z": () => (/* binding */ extractUrlParams)
/* harmony export */ });
/* harmony import */ var query_string__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(17563);
/**
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 * KIND, either express or implied.  See the License for the
 * specific language governing permissions and limitations
 * under the License.
 */

const reservedQueryParams = new Set(['standalone', 'edit']);
/**
 * Returns the url params that are used to customize queries
 */
function extractUrlParams(urlParamType) {
  const queryParams = query_string__WEBPACK_IMPORTED_MODULE_0__.parse(window.location.search);
  return Object.entries(queryParams).reduce((acc, [key, value]) => {
    if (urlParamType === 'regular' && reservedQueryParams.has(key) ||
    urlParamType === 'reserved' && !reservedQueryParams.has(key))
    return acc;
    // if multiple url params share the same key (?foo=bar&foo=baz), they will appear as an array.
    // Only one value can be used for a given query param, so we just take the first one.
    if (Array.isArray(value)) {
      return {
        ...acc,
        [key]: value[0] };

    }
    return { ...acc, [key]: value };
  }, {});
}

/***/ }),

/***/ 13284:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "UB": () => (/* binding */ MAX_ADVISABLE_VIZ_GALLERY_WIDTH),
/* harmony export */   "ZP": () => (/* binding */ VizTypeGallery)
/* harmony export */ });
/* unused harmony export VIZ_TYPE_CONTROL_TEST_ID */
/* harmony import */ var _babel_runtime_corejs3_helpers_extends__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(5872);
/* harmony import */ var _babel_runtime_corejs3_helpers_extends__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_babel_runtime_corejs3_helpers_extends__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(67294);
/* harmony import */ var fuse_js__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(74221);
/* harmony import */ var classnames__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(94184);
/* harmony import */ var classnames__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(classnames__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _superset_ui_core__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(60650);
/* harmony import */ var _superset_ui_core__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(37840);
/* harmony import */ var _superset_ui_core__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(11965);
/* harmony import */ var src_common_components__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(82191);
/* harmony import */ var src_components_Label__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(37921);
/* harmony import */ var src_components_DynamicPlugins__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(14278);
/* harmony import */ var src_components_Icons__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(38097);
/* harmony import */ var src_dashboard_components_nativeFilters_utils__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(1510);
/* harmony import */ var scroll_into_view_if_needed__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(64239);
 /**
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 * KIND, either express or implied.  See the License for the
 * specific language governing permissions and limitations
 * under the License.
 */










var SECTIONS;
(function (SECTIONS) {
  SECTIONS["ALL_CHARTS"] = "ALL_CHARTS";
  SECTIONS["CATEGORY"] = "CATEGORY";
  SECTIONS["TAGS"] = "TAGS";
  SECTIONS["RECOMMENDED_TAGS"] = "RECOMMENDED_TAGS";
})(SECTIONS || (SECTIONS = {}));
const DEFAULT_ORDER = [
'line',
'big_number',
'big_number_total',
'table',
'pivot_table_v2',
'echarts_timeseries_line',
'echarts_area',
'echarts_timeseries_bar',
'echarts_timeseries_scatter',
'pie',
'mixed_timeseries',
'filter_box',
'dist_bar',
'area',
'bar',
'deck_polygon',
'time_table',
'histogram',
'deck_scatter',
'deck_hex',
'time_pivot',
'deck_arc',
'heatmap',
'deck_grid',
'dual_line',
'deck_screengrid',
'line_multi',
'treemap',
'box_plot',
'sunburst',
'sankey',
'word_cloud',
'mapbox',
'kepler',
'cal_heatmap',
'rose',
'bubble',
'deck_geojson',
'horizon',
'deck_multi',
'compare',
'partition',
'event_flow',
'deck_path',
'graph_chart',
'world_map',
'paired_ttest',
'para',
'country_map'];

const typesWithDefaultOrder = new Set(DEFAULT_ORDER);
const THUMBNAIL_GRID_UNITS = 24;
const MAX_ADVISABLE_VIZ_GALLERY_WIDTH = 1090;
const OTHER_CATEGORY = (0,_superset_ui_core__WEBPACK_IMPORTED_MODULE_9__.t)('Other');
const ALL_CHARTS = (0,_superset_ui_core__WEBPACK_IMPORTED_MODULE_9__.t)('All charts');
const RECOMMENDED_TAGS = [(0,_superset_ui_core__WEBPACK_IMPORTED_MODULE_9__.t)('Popular'), (0,_superset_ui_core__WEBPACK_IMPORTED_MODULE_9__.t)('ECharts'), (0,_superset_ui_core__WEBPACK_IMPORTED_MODULE_9__.t)('Advanced-Analytics')];
const VIZ_TYPE_CONTROL_TEST_ID = 'viz-type-control';
const VizPickerLayout = _superset_ui_core__WEBPACK_IMPORTED_MODULE_10__/* .styled.div */ .iK.div`
  ${({ isSelectedVizMetadata }) => `
    display: grid;
    grid-template-rows: ${isSelectedVizMetadata ?
`auto minmax(100px, 1fr) minmax(200px, 35%)` :
'auto minmax(100px, 1fr)'};
    // em is used here because the sidebar should be sized to fit the longest standard tag
    grid-template-columns: minmax(14em, auto) 5fr;
    grid-template-areas:
      'sidebar search'
      'sidebar main'
      'details details';
    height: 70vh;
    overflow: auto;
  `}
`;
const SectionTitle = _superset_ui_core__WEBPACK_IMPORTED_MODULE_10__/* .styled.h3 */ .iK.h3`
  margin-top: 0;
  margin-bottom: ${({ theme }) => theme.gridUnit * 2}px;
  font-size: ${({ theme }) => theme.typography.sizes.l}px;
  font-weight: ${({ theme }) => theme.typography.weights.bold};
  line-height: ${({ theme }) => theme.gridUnit * 6}px;
`;
const LeftPane = _superset_ui_core__WEBPACK_IMPORTED_MODULE_10__/* .styled.div */ .iK.div`
  grid-area: sidebar;
  display: flex;
  flex-direction: column;
  border-right: 1px solid ${({ theme }) => theme.colors.grayscale.light2};
  overflow: auto;

  .ant-collapse .ant-collapse-item {
    .ant-collapse-header {
      font-size: ${({ theme }) => theme.typography.sizes.s}px;
      color: ${({ theme }) => theme.colors.grayscale.base};
      padding-left: ${({ theme }) => theme.gridUnit * 2}px;
      padding-bottom: ${({ theme }) => theme.gridUnit}px;
    }
    .ant-collapse-content .ant-collapse-content-box {
      display: flex;
      flex-direction: column;
      padding: 0 ${({ theme }) => theme.gridUnit * 2}px;
    }
  }
`;
const RightPane = _superset_ui_core__WEBPACK_IMPORTED_MODULE_10__/* .styled.div */ .iK.div`
  grid-area: main;
  overflow-y: auto;
`;
const SearchWrapper = _superset_ui_core__WEBPACK_IMPORTED_MODULE_10__/* .styled.div */ .iK.div`
  ${({ theme }) => `
    grid-area: search;
    margin-top: ${theme.gridUnit * 3}px;
    margin-bottom: ${theme.gridUnit}px;
    margin-left: ${theme.gridUnit * 3}px;
    margin-right: ${theme.gridUnit * 3}px;
    .ant-input-affix-wrapper {
      padding-left: ${theme.gridUnit * 2}px;
    }
  `}
`;
/** Styles to line up prefix/suffix icons in the search input */
const InputIconAlignment = _superset_ui_core__WEBPACK_IMPORTED_MODULE_10__/* .styled.div */ .iK.div`
  display: flex;
  justify-content: center;
  align-items: center;
  color: ${({ theme }) => theme.colors.grayscale.base};
`;
const SelectorLabel = _superset_ui_core__WEBPACK_IMPORTED_MODULE_10__/* .styled.button */ .iK.button`
  ${({ theme }) => `
    all: unset; // remove default button styles
    display: flex;
    flex-direction: row;
    align-items: center;
    cursor: pointer;
    margin: ${theme.gridUnit}px 0;
    padding: 0 ${theme.gridUnit}px;
    border-radius: ${theme.borderRadius}px;
    line-height: 2em;
    text-overflow: ellipsis;
    white-space: nowrap;
    position: relative;

    &:focus {
      outline: initial;
    }

    &.selected {
      background-color: ${theme.colors.primary.dark1};
      color: ${theme.colors.primary.light5};

      svg {
        color: ${theme.colors.primary.light5};
      }

      &:hover {
        .cancel {
          visibility: visible;
        }
      }
    }

    & span:first-of-type svg {
      margin-top: ${theme.gridUnit * 1.5}px;
    }

    .cancel {
      visibility: hidden;
    }
  `}
`;
const IconsPane = _superset_ui_core__WEBPACK_IMPORTED_MODULE_10__/* .styled.div */ .iK.div`
  overflow: auto;
  display: grid;
  grid-template-columns: repeat(
    auto-fill,
    ${({ theme }) => theme.gridUnit * THUMBNAIL_GRID_UNITS}px
  );
  grid-auto-rows: max-content;
  justify-content: space-evenly;
  grid-gap: ${({ theme }) => theme.gridUnit * 2}px;
  justify-items: center;
  // for some reason this padding doesn't seem to apply at the bottom of the container. Why is a mystery.
  padding: ${({ theme }) => theme.gridUnit * 2}px;
`;
const DetailsPane = (theme) => _superset_ui_core__WEBPACK_IMPORTED_MODULE_11__.css`
  grid-area: details;
  border-top: 1px solid ${theme.colors.grayscale.light2};
`;
const DetailsPopulated = (theme) => _superset_ui_core__WEBPACK_IMPORTED_MODULE_11__.css`
  padding: ${theme.gridUnit * 4}px;
  display: grid;
  grid-template-columns: 1fr 1fr;
  grid-template-rows: auto auto 1fr;
  grid-template-areas:
    'viz-name examples-header'
    'viz-tags examples'
    'description examples';
`;
// overflow hidden on the details pane and overflow auto on the description
// (plus grid layout) enables the description to scroll while the header stays in place.
const TagsWrapper = _superset_ui_core__WEBPACK_IMPORTED_MODULE_10__/* .styled.div */ .iK.div`
  grid-area: viz-tags;
  width: ${({ theme }) => theme.gridUnit * 120}px;
  padding-right: ${({ theme }) => theme.gridUnit * 14}px;
  padding-bottom: ${({ theme }) => theme.gridUnit * 2}px;
`;
const Description = _superset_ui_core__WEBPACK_IMPORTED_MODULE_10__/* .styled.p */ .iK.p`
  grid-area: description;
  overflow: auto;
  padding-right: ${({ theme }) => theme.gridUnit * 14}px;
  margin: 0;
`;
const Examples = _superset_ui_core__WEBPACK_IMPORTED_MODULE_10__/* .styled.div */ .iK.div`
  grid-area: examples;
  display: flex;
  flex-direction: row;
  flex-wrap: nowrap;
  overflow: auto;
  gap: ${({ theme }) => theme.gridUnit * 4}px;

  img {
    height: 100%;
    border-radius: ${({ theme }) => theme.gridUnit}px;
    border: 1px solid ${({ theme }) => theme.colors.grayscale.light2};
  }
`;
const thumbnailContainerCss = (theme) => _superset_ui_core__WEBPACK_IMPORTED_MODULE_11__.css`
  cursor: pointer;
  width: ${theme.gridUnit * THUMBNAIL_GRID_UNITS}px;

  img {
    min-width: ${theme.gridUnit * THUMBNAIL_GRID_UNITS}px;
    min-height: ${theme.gridUnit * THUMBNAIL_GRID_UNITS}px;
    border: 1px solid ${theme.colors.grayscale.light2};
    border-radius: ${theme.gridUnit}px;
    transition: border-color ${theme.transitionTiming};
  }

  &.selected img {
    border: 2px solid ${theme.colors.primary.light2};
  }

  &:hover:not(.selected) img {
    border: 1px solid ${theme.colors.grayscale.light1};
  }

  .viztype-label {
    margin-top: ${theme.gridUnit * 2}px;
    text-align: center;
  }
`;
function vizSortFactor(entry) {
  if (typesWithDefaultOrder.has(entry.key)) {
    return DEFAULT_ORDER.indexOf(entry.key);
  }
  return DEFAULT_ORDER.length;
}
const Thumbnail = ({ entry, selectedViz, setSelectedViz }) => {
  const theme = (0,_superset_ui_core__WEBPACK_IMPORTED_MODULE_10__/* .useTheme */ .Fg)();
  const { key, value: type } = entry;
  const isSelected = selectedViz === entry.key;
  return (0,_superset_ui_core__WEBPACK_IMPORTED_MODULE_11__.jsx)("div", { role: "button"
    // using css instead of a styled component to preserve
    // the data-test attribute
    , css: thumbnailContainerCss(theme), tabIndex: 0, className: isSelected ? 'selected' : '', onClick: () => setSelectedViz(key) },
  (0,_superset_ui_core__WEBPACK_IMPORTED_MODULE_11__.jsx)("img", { alt: type.name, width: "100%", className: `viztype-selector ${isSelected ? 'selected' : ''}`, src: type.thumbnail }),
  (0,_superset_ui_core__WEBPACK_IMPORTED_MODULE_11__.jsx)("div", { className: "viztype-label" },
  type.name));


};
/** A list of viz thumbnails, used within the viz picker modal */
const ThumbnailGallery = ({ vizEntries, ...props }) => (0,_superset_ui_core__WEBPACK_IMPORTED_MODULE_11__.jsx)(IconsPane, null,
vizEntries.map((entry) => (0,_superset_ui_core__WEBPACK_IMPORTED_MODULE_11__.jsx)(Thumbnail, _babel_runtime_corejs3_helpers_extends__WEBPACK_IMPORTED_MODULE_0___default()({ key: entry.key }, props, { entry: entry }))));

const Selector = ({ selector, sectionId, icon, isSelected, onClick, className }) => {
  const btnRef = (0,react__WEBPACK_IMPORTED_MODULE_1__.useRef)(null);
  // see Element.scrollIntoViewIfNeeded()
  // see: https://developer.mozilla.org/en-US/docs/Web/API/Element/scrollIntoViewIfNeeded
  (0,react__WEBPACK_IMPORTED_MODULE_1__.useEffect)(() => {
    if (isSelected) {
      // We need to wait for the modal to open and then scroll, so we put it in the microtask queue
      queueMicrotask(() => (0,scroll_into_view_if_needed__WEBPACK_IMPORTED_MODULE_12__["default"])(btnRef.current, {
        behavior: 'smooth',
        scrollMode: 'if-needed' }));

    }
  }, []);
  return (0,_superset_ui_core__WEBPACK_IMPORTED_MODULE_11__.jsx)(SelectorLabel, { ref: btnRef, key: selector, name: selector, className: classnames__WEBPACK_IMPORTED_MODULE_3___default()(className, isSelected && 'selected'), onClick: () => onClick(selector, sectionId) },
  icon,
  selector);

};
const doesVizMatchSelector = (viz, selector) => selector === viz.category ||
selector === OTHER_CATEGORY && viz.category == null ||
(viz.tags || []).indexOf(selector) > -1;
function VizTypeGallery(props) {var _selectedVizMetadata$;
  const { selectedViz, onChange, className } = props;
  const { mountedPluginMetadata } = (0,src_components_DynamicPlugins__WEBPACK_IMPORTED_MODULE_6__/* .usePluginContext */ .gp)();
  const searchInputRef = (0,react__WEBPACK_IMPORTED_MODULE_1__.useRef)();
  const [searchInputValue, setSearchInputValue] = (0,react__WEBPACK_IMPORTED_MODULE_1__.useState)('');
  const [isSearchFocused, setIsSearchFocused] = (0,react__WEBPACK_IMPORTED_MODULE_1__.useState)(true);
  const isActivelySearching = isSearchFocused && !!searchInputValue;
  const selectedVizMetadata = selectedViz ?
  mountedPluginMetadata[selectedViz] :
  null;
  const chartMetadata = (0,react__WEBPACK_IMPORTED_MODULE_1__.useMemo)(() => {
    const result = Object.entries(mountedPluginMetadata).
    map(([key, value]) => ({ key, value })).
    filter(({ value }) => (0,src_dashboard_components_nativeFilters_utils__WEBPACK_IMPORTED_MODULE_8__/* .nativeFilterGate */ .X3)(value.behaviors || []) && !value.deprecated);
    result.sort((a, b) => vizSortFactor(a) - vizSortFactor(b));
    return result;
  }, [mountedPluginMetadata]);
  const chartsByCategory = (0,react__WEBPACK_IMPORTED_MODULE_1__.useMemo)(() => {
    const result = {};
    chartMetadata.forEach((entry) => {
      const category = entry.value.category || OTHER_CATEGORY;
      if (!result[category]) {
        result[category] = [];
      }
      result[category].push(entry);
    });
    return result;
  }, [chartMetadata]);
  const categories = (0,react__WEBPACK_IMPORTED_MODULE_1__.useMemo)(() => Object.keys(chartsByCategory).sort((a, b) => {
    // make sure Other goes at the end
    if (a === OTHER_CATEGORY)
    return 1;
    if (b === OTHER_CATEGORY)
    return -1;
    // sort alphabetically
    return a.localeCompare(b);
  }), [chartsByCategory]);
  const chartsByTags = (0,react__WEBPACK_IMPORTED_MODULE_1__.useMemo)(() => {
    const result = {};
    chartMetadata.forEach((entry) => {
      const tags = entry.value.tags || [];
      tags.forEach((tag) => {
        if (!result[tag]) {
          result[tag] = [];
        }
        result[tag].push(entry);
      });
    });
    return result;
  }, [chartMetadata]);
  const tags = (0,react__WEBPACK_IMPORTED_MODULE_1__.useMemo)(() => Object.keys(chartsByTags).
  sort((a, b) =>
  // sort alphabetically
  a.localeCompare(b)).
  filter((tag) => RECOMMENDED_TAGS.indexOf(tag) === -1), [chartsByTags]);
  const sortedMetadata = (0,react__WEBPACK_IMPORTED_MODULE_1__.useMemo)(() => chartMetadata.sort((a, b) => a.key.localeCompare(b.key)), [chartMetadata]);
  const [activeSelector, setActiveSelector] = (0,react__WEBPACK_IMPORTED_MODULE_1__.useState)(() => (selectedVizMetadata == null ? void 0 : selectedVizMetadata.category) || RECOMMENDED_TAGS[0]);
  const [activeSection, setActiveSection] = (0,react__WEBPACK_IMPORTED_MODULE_1__.useState)(() => selectedVizMetadata != null && selectedVizMetadata.category ?
  SECTIONS.CATEGORY :
  SECTIONS.RECOMMENDED_TAGS);
  // get a fuse instance for fuzzy search
  const fuse = (0,react__WEBPACK_IMPORTED_MODULE_1__.useMemo)(() => new fuse_js__WEBPACK_IMPORTED_MODULE_2__/* ["default"] */ .Z(chartMetadata, {
    ignoreLocation: true,
    threshold: 0.3,
    keys: ['value.name', 'value.tags', 'value.description'] }),
  [chartMetadata]);
  const searchResults = (0,react__WEBPACK_IMPORTED_MODULE_1__.useMemo)(() => {
    if (searchInputValue.trim() === '') {
      return [];
    }
    return fuse.search(searchInputValue).map((result) => result.item);
  }, [searchInputValue, fuse]);
  const focusSearch = (0,react__WEBPACK_IMPORTED_MODULE_1__.useCallback)(() => {
    // "start searching" is actually a two-stage process.
    // When you first click on the search bar, the input is focused and nothing else happens.
    // Once you begin typing, the selected category is cleared and the displayed viz entries change.
    setIsSearchFocused(true);
  }, []);
  const changeSearch = (0,react__WEBPACK_IMPORTED_MODULE_1__.useCallback)((event) => setSearchInputValue(event.target.value), []);
  const stopSearching = (0,react__WEBPACK_IMPORTED_MODULE_1__.useCallback)(() => {
    // stopping a search takes you back to the category you were looking at before.
    // Unlike focusSearch, this is a simple one-step process.
    setIsSearchFocused(false);
    setSearchInputValue('');
    searchInputRef.current.blur();
  }, []);
  const clickSelector = (0,react__WEBPACK_IMPORTED_MODULE_1__.useCallback)((selector, sectionId) => {
    if (isSearchFocused) {
      stopSearching();
    }
    setActiveSelector(selector);
    setActiveSection(sectionId);
    // clear the selected viz if it is not present in the new category or tags
    const isSelectedVizCompatible = selectedVizMetadata &&
    doesVizMatchSelector(selectedVizMetadata, selector);
    if (selector !== activeSelector && !isSelectedVizCompatible) {
      onChange(null);
    }
  }, [
  stopSearching,
  isSearchFocused,
  activeSelector,
  selectedVizMetadata,
  onChange]);

  const sectionMap = (0,react__WEBPACK_IMPORTED_MODULE_1__.useMemo)(() => ({
    [SECTIONS.RECOMMENDED_TAGS]: {
      title: (0,_superset_ui_core__WEBPACK_IMPORTED_MODULE_9__.t)('Recommended tags'),
      icon: (0,_superset_ui_core__WEBPACK_IMPORTED_MODULE_11__.jsx)(src_components_Icons__WEBPACK_IMPORTED_MODULE_7__/* ["default"].Tags */ .Z.Tags, null),
      selectors: RECOMMENDED_TAGS },

    [SECTIONS.CATEGORY]: {
      title: (0,_superset_ui_core__WEBPACK_IMPORTED_MODULE_9__.t)('Category'),
      icon: (0,_superset_ui_core__WEBPACK_IMPORTED_MODULE_11__.jsx)(src_components_Icons__WEBPACK_IMPORTED_MODULE_7__/* ["default"].Category */ .Z.Category, null),
      selectors: categories },

    [SECTIONS.TAGS]: {
      title: (0,_superset_ui_core__WEBPACK_IMPORTED_MODULE_9__.t)('Tags'),
      icon: (0,_superset_ui_core__WEBPACK_IMPORTED_MODULE_11__.jsx)(src_components_Icons__WEBPACK_IMPORTED_MODULE_7__/* ["default"].Tags */ .Z.Tags, null),
      selectors: tags } }),

  [categories, tags]);
  const getVizEntriesToDisplay = () => {
    if (isActivelySearching) {
      return searchResults;
    }
    if (activeSelector === ALL_CHARTS &&
    activeSection === SECTIONS.ALL_CHARTS) {
      return sortedMetadata;
    }
    if (activeSection === SECTIONS.CATEGORY &&
    chartsByCategory[activeSelector]) {
      return chartsByCategory[activeSelector];
    }
    if ((activeSection === SECTIONS.TAGS ||
    activeSection === SECTIONS.RECOMMENDED_TAGS) &&
    chartsByTags[activeSelector]) {
      return chartsByTags[activeSelector];
    }
    return [];
  };
  return (0,_superset_ui_core__WEBPACK_IMPORTED_MODULE_11__.jsx)(VizPickerLayout, { className: className, isSelectedVizMetadata: Boolean(selectedVizMetadata) },
  (0,_superset_ui_core__WEBPACK_IMPORTED_MODULE_11__.jsx)(LeftPane, null,
  (0,_superset_ui_core__WEBPACK_IMPORTED_MODULE_11__.jsx)(Selector, { css: ({ gridUnit }) =>
    // adjust style for not being inside a collapse
    _superset_ui_core__WEBPACK_IMPORTED_MODULE_11__.css`
              margin: ${gridUnit * 2}px;
              margin-bottom: 0;
            `, sectionId: SECTIONS.ALL_CHARTS, selector: ALL_CHARTS, icon: (0,_superset_ui_core__WEBPACK_IMPORTED_MODULE_11__.jsx)(src_components_Icons__WEBPACK_IMPORTED_MODULE_7__/* ["default"].Ballot */ .Z.Ballot, null), isSelected: !isActivelySearching &&
    ALL_CHARTS === activeSelector &&
    SECTIONS.ALL_CHARTS === activeSection, onClick: clickSelector }),
  (0,_superset_ui_core__WEBPACK_IMPORTED_MODULE_11__.jsx)(src_common_components__WEBPACK_IMPORTED_MODULE_4__/* .Collapse */ .UO, { expandIconPosition: "right", ghost: true, defaultActiveKey: Object.keys(sectionMap) },
  Object.keys(sectionMap).map((sectionId) => {
    const section = sectionMap[sectionId];
    return (0,_superset_ui_core__WEBPACK_IMPORTED_MODULE_11__.jsx)(src_common_components__WEBPACK_IMPORTED_MODULE_4__/* .Collapse.Panel */ .UO.Panel, { header: (0,_superset_ui_core__WEBPACK_IMPORTED_MODULE_11__.jsx)("span", { className: "header" }, section.title), key: sectionId },
    section.selectors.map((selector) => (0,_superset_ui_core__WEBPACK_IMPORTED_MODULE_11__.jsx)(Selector, { key: selector, selector: selector, sectionId: sectionId, icon: section.icon, isSelected: !isActivelySearching &&
      selector === activeSelector &&
      sectionId === activeSection, onClick: clickSelector })));

  }))),



  (0,_superset_ui_core__WEBPACK_IMPORTED_MODULE_11__.jsx)(SearchWrapper, null,
  (0,_superset_ui_core__WEBPACK_IMPORTED_MODULE_11__.jsx)(src_common_components__WEBPACK_IMPORTED_MODULE_4__/* .Input */ .II, { type: "text", ref: searchInputRef /* cast required because emotion */, value: searchInputValue, placeholder: (0,_superset_ui_core__WEBPACK_IMPORTED_MODULE_9__.t)('Search all charts'), onChange: changeSearch, onFocus: focusSearch, prefix: (0,_superset_ui_core__WEBPACK_IMPORTED_MODULE_11__.jsx)(InputIconAlignment, null,
    (0,_superset_ui_core__WEBPACK_IMPORTED_MODULE_11__.jsx)(src_components_Icons__WEBPACK_IMPORTED_MODULE_7__/* ["default"].Search */ .Z.Search, { iconSize: "m" })),
    suffix: (0,_superset_ui_core__WEBPACK_IMPORTED_MODULE_11__.jsx)(InputIconAlignment, null,
    searchInputValue && (0,_superset_ui_core__WEBPACK_IMPORTED_MODULE_11__.jsx)(src_components_Icons__WEBPACK_IMPORTED_MODULE_7__/* ["default"].XLarge */ .Z.XLarge, { iconSize: "m", onClick: stopSearching })) })),



  (0,_superset_ui_core__WEBPACK_IMPORTED_MODULE_11__.jsx)(RightPane, null,
  (0,_superset_ui_core__WEBPACK_IMPORTED_MODULE_11__.jsx)(ThumbnailGallery, { vizEntries: getVizEntriesToDisplay(), selectedViz: selectedViz, setSelectedViz: onChange })),


  selectedVizMetadata ? (0,_superset_ui_core__WEBPACK_IMPORTED_MODULE_11__.jsx)("div", { css: (theme) => [
    DetailsPane(theme),
    DetailsPopulated(theme)] },

  (0,_superset_ui_core__WEBPACK_IMPORTED_MODULE_11__.jsx)(react__WEBPACK_IMPORTED_MODULE_1__.Fragment, null,
  (0,_superset_ui_core__WEBPACK_IMPORTED_MODULE_11__.jsx)(SectionTitle, { css: _superset_ui_core__WEBPACK_IMPORTED_MODULE_11__.css`
                grid-area: viz-name;
              ` },
  selectedVizMetadata == null ? void 0 : selectedVizMetadata.name),

  (0,_superset_ui_core__WEBPACK_IMPORTED_MODULE_11__.jsx)(TagsWrapper, null,
  selectedVizMetadata == null ? void 0 : selectedVizMetadata.tags.map((tag) => (0,_superset_ui_core__WEBPACK_IMPORTED_MODULE_11__.jsx)(src_components_Label__WEBPACK_IMPORTED_MODULE_5__/* ["default"] */ .Z, { key: tag }, tag))),

  (0,_superset_ui_core__WEBPACK_IMPORTED_MODULE_11__.jsx)(Description, null,
  (selectedVizMetadata == null ? void 0 : selectedVizMetadata.description) ||
  (0,_superset_ui_core__WEBPACK_IMPORTED_MODULE_9__.t)('No description available.')),

  (0,_superset_ui_core__WEBPACK_IMPORTED_MODULE_11__.jsx)(SectionTitle, { css: _superset_ui_core__WEBPACK_IMPORTED_MODULE_11__.css`
                grid-area: examples-header;
              ` },
  !!(selectedVizMetadata != null && (_selectedVizMetadata$ = selectedVizMetadata.exampleGallery) != null && _selectedVizMetadata$.length) && (0,_superset_ui_core__WEBPACK_IMPORTED_MODULE_9__.t)('Examples')),

  (0,_superset_ui_core__WEBPACK_IMPORTED_MODULE_11__.jsx)(Examples, null,
  ((selectedVizMetadata == null ? void 0 : selectedVizMetadata.exampleGallery) || []).map((example) => (0,_superset_ui_core__WEBPACK_IMPORTED_MODULE_11__.jsx)("img", { src: example.url, alt: example.caption, title: example.caption }))))) :


  null);

}

/***/ })

/******/ 	});
/************************************************************************/
/******/ 	// The module cache
/******/ 	var __webpack_module_cache__ = {};
/******/ 	
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/ 		// Check if module is in cache
/******/ 		var cachedModule = __webpack_module_cache__[moduleId];
/******/ 		if (cachedModule !== undefined) {
/******/ 			return cachedModule.exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = __webpack_module_cache__[moduleId] = {
/******/ 			id: moduleId,
/******/ 			loaded: false,
/******/ 			exports: {}
/******/ 		};
/******/ 	
/******/ 		// Execute the module function
/******/ 		__webpack_modules__[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/ 	
/******/ 		// Flag the module as loaded
/******/ 		module.loaded = true;
/******/ 	
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/ 	
/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = __webpack_modules__;
/******/ 	
/************************************************************************/
/******/ 	/* webpack/runtime/amd define */
/******/ 	(() => {
/******/ 		__webpack_require__.amdD = function () {
/******/ 			throw new Error('define cannot be used indirect');
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/amd options */
/******/ 	(() => {
/******/ 		__webpack_require__.amdO = {};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/chunk loaded */
/******/ 	(() => {
/******/ 		var deferred = [];
/******/ 		__webpack_require__.O = (result, chunkIds, fn, priority) => {
/******/ 			if(chunkIds) {
/******/ 				priority = priority || 0;
/******/ 				for(var i = deferred.length; i > 0 && deferred[i - 1][2] > priority; i--) deferred[i] = deferred[i - 1];
/******/ 				deferred[i] = [chunkIds, fn, priority];
/******/ 				return;
/******/ 			}
/******/ 			var notFulfilled = Infinity;
/******/ 			for (var i = 0; i < deferred.length; i++) {
/******/ 				var [chunkIds, fn, priority] = deferred[i];
/******/ 				var fulfilled = true;
/******/ 				for (var j = 0; j < chunkIds.length; j++) {
/******/ 					if ((priority & 1 === 0 || notFulfilled >= priority) && Object.keys(__webpack_require__.O).every((key) => (__webpack_require__.O[key](chunkIds[j])))) {
/******/ 						chunkIds.splice(j--, 1);
/******/ 					} else {
/******/ 						fulfilled = false;
/******/ 						if(priority < notFulfilled) notFulfilled = priority;
/******/ 					}
/******/ 				}
/******/ 				if(fulfilled) {
/******/ 					deferred.splice(i--, 1)
/******/ 					var r = fn();
/******/ 					if (r !== undefined) result = r;
/******/ 				}
/******/ 			}
/******/ 			return result;
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/compat get default export */
/******/ 	(() => {
/******/ 		// getDefaultExport function for compatibility with non-harmony modules
/******/ 		__webpack_require__.n = (module) => {
/******/ 			var getter = module && module.__esModule ?
/******/ 				() => (module['default']) :
/******/ 				() => (module);
/******/ 			__webpack_require__.d(getter, { a: getter });
/******/ 			return getter;
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/create fake namespace object */
/******/ 	(() => {
/******/ 		var getProto = Object.getPrototypeOf ? (obj) => (Object.getPrototypeOf(obj)) : (obj) => (obj.__proto__);
/******/ 		var leafPrototypes;
/******/ 		// create a fake namespace object
/******/ 		// mode & 1: value is a module id, require it
/******/ 		// mode & 2: merge all properties of value into the ns
/******/ 		// mode & 4: return value when already ns object
/******/ 		// mode & 16: return value when it's Promise-like
/******/ 		// mode & 8|1: behave like require
/******/ 		__webpack_require__.t = function(value, mode) {
/******/ 			if(mode & 1) value = this(value);
/******/ 			if(mode & 8) return value;
/******/ 			if(typeof value === 'object' && value) {
/******/ 				if((mode & 4) && value.__esModule) return value;
/******/ 				if((mode & 16) && typeof value.then === 'function') return value;
/******/ 			}
/******/ 			var ns = Object.create(null);
/******/ 			__webpack_require__.r(ns);
/******/ 			var def = {};
/******/ 			leafPrototypes = leafPrototypes || [null, getProto({}), getProto([]), getProto(getProto)];
/******/ 			for(var current = mode & 2 && value; typeof current == 'object' && !~leafPrototypes.indexOf(current); current = getProto(current)) {
/******/ 				Object.getOwnPropertyNames(current).forEach((key) => (def[key] = () => (value[key])));
/******/ 			}
/******/ 			def['default'] = () => (value);
/******/ 			__webpack_require__.d(ns, def);
/******/ 			return ns;
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/define property getters */
/******/ 	(() => {
/******/ 		// define getter functions for harmony exports
/******/ 		__webpack_require__.d = (exports, definition) => {
/******/ 			for(var key in definition) {
/******/ 				if(__webpack_require__.o(definition, key) && !__webpack_require__.o(exports, key)) {
/******/ 					Object.defineProperty(exports, key, { enumerable: true, get: definition[key] });
/******/ 				}
/******/ 			}
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/ensure chunk */
/******/ 	(() => {
/******/ 		__webpack_require__.f = {};
/******/ 		// This file contains only the entry chunk.
/******/ 		// The chunk loading function for additional chunks
/******/ 		__webpack_require__.e = (chunkId) => {
/******/ 			return Promise.all(Object.keys(__webpack_require__.f).reduce((promises, key) => {
/******/ 				__webpack_require__.f[key](chunkId, promises);
/******/ 				return promises;
/******/ 			}, []));
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/get javascript chunk filename */
/******/ 	(() => {
/******/ 		// This function allow to reference async chunks
/******/ 		__webpack_require__.u = (chunkId) => {
/******/ 			// return url for filenames not based on template
/******/ 			if (chunkId === 2441) return "2441.dfa5e377a4d92388789a.entry.js";
/******/ 			if (chunkId === 4998) return "4998.09f66519fdd63987e166.entry.js";
/******/ 			if (chunkId === 7843) return "7843.afc61acae9eefb9b3bde.entry.js";
/******/ 			if (chunkId === 3375) return "3375.e4f9f1a5608135f8e268.entry.js";
/******/ 			if (chunkId === 4654) return "4654.376ceeda9980d44386d1.entry.js";
/******/ 			if (chunkId === 741) return "741.ca4c786c52d02bb43007.entry.js";
/******/ 			if (chunkId === 6962) return "6962.9aa3349cd90f506c2685.entry.js";
/******/ 			if (chunkId === 2825) return "2825.2d0581946e936cc01b02.entry.js";
/******/ 			if (chunkId === 7173) return "7173.291601d7321c9ad3fc04.entry.js";
/******/ 			// return url for filenames based on template
/******/ 			return "" + {"3":"d1b59679b897c72fc607","57":"028e5eaba60ee1f0c2c2","71":"761512bb6df4782c0353","112":"9fcc2ab7e3decb77e68a","128":"8955b4f52bd78bda1dd5","158":"067dd46754cb5755621a","177":"daff443a6a259740b9ea","183":"7180931293c0eb958c52","215":"0d19cdfee35ccc92f701","310":"135def3410b28bde86ff","312":"6456f925ef0e593cf2fd","326":"d509c1a72e06d2acef26","336":"f9b3561fd92836a920cd","347":"c5b84ed281f1210d8bfb","363":"a6530749fb56462bc957","423":"a36f3890dfe36a082008","440":"cdd649a88561a9b538fe","547":"413b6b7ff396e4c40d94","597":"fef57e00156e5f59ea45","600":"ef265991d9c8beb1bb22","666":"97fb81e087033f41dee6","823":"46192e4039353cb4ccce","826":"f82ff59e0436c52a8bc1","992":"d42abb01dcb03b5ea79e","999":"85dd3a220ce297acafe9","1066":"277c59d1fd85de9f2b3c","1075":"94d9b1829e929831b151","1095":"586288cf34280c80b810","1174":"8f244f47294e02e761a1","1185":"feb0657fd1cd8eb8cccb","1193":"06b99aac2e27bf2ba2a8","1243":"0579edc081d4eb80453c","1256":"0a7adfa99f06991c526c","1258":"e6a4e669a75b5758e013","1263":"0ddad88e1fc0114d1dc9","1293":"f93daf14868c44bd843a","1351":"ab5b2b54ecd29ca6e21c","1391":"e1dce0f538df5a42b9b1","1398":"6bdcdfad4fffbd4b6bd8","1493":"af7d972a6a46bacab94d","1568":"6d86dc72b95d32371252","1573":"fe8cdbdb10c26e637cb5","1605":"883e261ae3ecfb0f8755","1899":"555c4cc5e9264d2e09f9","1921":"4c7a017946fccb360357","1948":"f219bf26953c4a1d0b23","2079":"653b159f3867c9459b01","2085":"fef5cc791125e768e606","2089":"e5b6d6f716371b2c550a","2105":"8059570cc5823d65fd2c","2112":"f2715e006a75d58f6e3d","2264":"cd1eeac9f037880b0212","2267":"18b27b1bb2bd5dd7aa61","2306":"3058f623f8ca8785e71b","2403":"be5f79b6b4624364c5f3","2439":"7f23ec71a8f74c2b02ec","2646":"89bf808500d87084d6b0","2698":"c093d4f54e9cb79148ef","2713":"a57d21e7160b0f553f5c","2797":"617b8ee1d3d6339e5613","2862":"39d961fce2d1638da6c2","2983":"feae373a263e065ff446","3037":"53a6f7467ab085a27986","3118":"97716f0b10d52cd6c2e5","3141":"d531ed7032b42d64dca2","3208":"700663ae83d32f467243","3240":"73ffac6083ffe185c09f","3265":"b67a755d414be1b54d86","3325":"56aebae23380bbe9f3cc","3544":"898720f9f22675673911","3558":"714cba25b1e6aa5cd799","3567":"5e62708f5889c428e82c","3606":"b0e363c89061c92d0c53","3609":"66a8179245a38943ac67","3720":"72b7898096ecd06be5b7","3749":"afee7363adc500297825","3776":"ea56451903b6130cccb7","3871":"6a529c979bb793ccbdae","3955":"9160a76cf3dea289b79e","3985":"1899b405b3888e068c7e","4018":"9b86bf500d66aeedcfdf","4022":"7ae21ee2ebb4b49b5770","4139":"2c3665b54e7fed053b35","4192":"44172484a85fb65a2009","4214":"b122b6fdbb32aae2ac9f","4266":"a68f073d5c25c1344d94","4273":"e6b35ed596fb2404f26c","4295":"26c9274aa75b3d522dcd","4319":"e66093c518bc737f25ab","4441":"3cc1e1b0ca563ea88922","4458":"8b6a6fd12fa942d44b7b","4473":"d0795555171c13d9ef52","4474":"eb2f03c6083e66304c68","4486":"3a9ea05c99b7145373c6","4572":"82211a53d1435fca9312","4579":"583c6ba0caecf59b98e3","4625":"0b2c629dc9577bcbc473","4662":"40af31a304028068f8a3","4667":"1a5286b06adb14b671fd","4732":"78da6bf13da526416f92","4757":"278b3b950a627ab829ab","4758":"f13eabe9cbc4aaa2cfd7","4794":"008094f826594e07d5af","4797":"594130c61e265833c43b","4810":"47366d32d3b5c3e2f319","4817":"84f3798572f423cea73a","4832":"084573b71fd27cb2c4bd","4851":"067006aa81cb69192dea","4972":"b58fff79c37c85d03666","4980":"9507ccb27964e1aa67cf","4981":"3322a395775b130ba94f","5019":"879aa31862b3ff694978","5042":"110054e19081d5f04ff4","5094":"7f930637b1b1da55a039","5181":"2e92104157272e3dbb37","5201":"648d8f209c1894a50b3f","5215":"7b3108b08b173dc818d0","5224":"6d6fd64a53aaa33eea22","5226":"bb22669bd991d6a73375","5249":"61d3f9c5cc5ca3f80b04","5278":"e0ec98b2bfcf70c9ea5f","5281":"046ca8aa0e202a5a4c00","5322":"3f2a7533de01a1a9a529","5330":"be15bc34dd2926179f89","5335":"e5da2df11378fb591c33","5350":"14835ad324f5a759f725","5359":"4e0cf032edde0ad08c98","5367":"22df5a0f35a4554839f1","5507":"d306225272739fb01e43","5580":"df0ecccb1e5c3185e516","5592":"e695c51628cbff6bf0fd","5641":"b743bdeff76333f134ae","5660":"7d626632b65bdef870f9","5707":"c9627a388872a8d2a957","5771":"cbf62bbc3f6f8025fdfc","5777":"f3e29f5dbb36ae1cc98e","5802":"215b013def1194b6e5f8","5816":"a4c2b603201c7f9060d7","5832":"e8a940e0c94fa25a8765","5838":"4193414073d37ecb6064","5859":"cb5e0e7bec35a79811a0","5962":"f163fa69cbd0345e0a5a","5965":"82b7fed88b88603bc8e6","5972":"09c10d24cb92e1f67b13","5998":"2cc665e33c971367a6ce","6060":"664f67503cbe3c046ed5","6061":"2b5174793a5a1a9c6fd0","6126":"c44c96942fb85a19ac1e","6150":"548accd51f5ec4ecc14b","6167":"5e75f0b0cd02b96355cf","6207":"22ede093c81ef82c5bac","6254":"a29ae9eeb81891bddab6","6259":"0e0b8e93fc11a96b30d8","6303":"1a63ee0f599081264d8c","6371":"c7bd2b4dc87e1b940ce5","6420":"eb39ad899c9c5c179291","6439":"3ab44f2f04ce952aa010","6447":"0f127715dab6bbf6fefd","6507":"3533ebbe2e94fa7a675a","6668":"a26e3bb5b59e7e16f550","6682":"19283d8df0b4e63f16db","6740":"4fb5b2f35173a25a0c16","6758":"f7d7e358ea3e78bbba35","6819":"183272dd2f7c81c4c9c8","6883":"6780ee31faa82e4825c2","6977":"58d52502f18c6376f257","6981":"7a8d6c643cb4f5df8198","7040":"52864f38c2f08a4b7cb9","7068":"c91c3fac0edd02b19a7b","7183":"15e2f1b86b261dda7daf","7219":"63a78333da5872945488","7249":"548a8e5717947f7021bd","7405":"9c51a4dd78cc59db1bf7","7460":"e0a8070ed7c2cbd41080","7584":"09582b48010b05b12a59","7610":"320e8196129209a5d403","7654":"fb32e1480e8a5e656f96","7716":"0d08811bf13191ea008a","7760":"e52f02c420204be2409d","7803":"41ad98224efd12874173","7828":"6caa255c9ddc31e8a76e","7832":"f3d5e3cbaaf9c0591048","7850":"8b44f0b0e02baa79ae77","7893":"f48cf88e5599c031944c","7922":"886bbfbb9c5b6a949f30","8130":"a049cce3576b4816c28d","8230":"7e33f6c4ebc03205cc2a","8312":"c6aae8671318f46a616b","8349":"0675c83c091a08d07837","8398":"3f920942fdd2e7b6c103","8425":"ca4e7824ea1f39c02835","8463":"1f78779088dc48ccacac","8464":"9e3d8754be49d180b08b","8616":"6fd2e49a71076366d957","8682":"6cabc2fe8f0626630fcb","8695":"448d248fb9d5f4999c24","8750":"81871e849cfbdc2c6ff1","8883":"793b3c3e9a586aa0a63b","8903":"d5428f945fee1bb47615","8924":"666a6af65fe736acd44c","8970":"22b785d53413d0d6b2e1","9013":"6ffbfae6a84d886acb37","9034":"846e409f3006a4b27fef","9052":"18c72b820a16b97d3437","9109":"befdefaa4a6a29f18775","9131":"2dcf183dac063170f0bd","9242":"063953b028f62ec0d27e","9305":"3dbe560a6cb4a6bdb9ed","9325":"d96803c30d0802740a48","9393":"598a5cabf7906fbbc188","9483":"2c17ab4038922bf895d8","9510":"d881743c10a5f4711298","9558":"78f4fa40b40a02a002d1","9574":"76474957fa0578a8fbae","9767":"d4ac455af931bb06a7dc","9794":"f331817dc4465431f2dc","9811":"61283ed5ec96a21e421e","9857":"805069f9fb25105fc8ea","9885":"47c474f256a13e3ca4a7","9893":"2c19625a4eb4da871497","9938":"19cf34d39baa7b12dab2"}[chunkId] + ".chunk.js";
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/get mini-css chunk filename */
/******/ 	(() => {
/******/ 		// This function allow to reference all chunks
/******/ 		__webpack_require__.miniCssF = (chunkId) => {
/******/ 			// return url for filenames based on template
/******/ 			return "" + chunkId + "." + {"3":"d1b59679b897c72fc607","128":"8955b4f52bd78bda1dd5","423":"a36f3890dfe36a082008","823":"46192e4039353cb4ccce","1066":"277c59d1fd85de9f2b3c","1193":"06b99aac2e27bf2ba2a8","1243":"0579edc081d4eb80453c","1391":"e1dce0f538df5a42b9b1","1921":"4c7a017946fccb360357","2862":"39d961fce2d1638da6c2","3609":"66a8179245a38943ac67","3776":"ea56451903b6130cccb7","4192":"44172484a85fb65a2009","4473":"d0795555171c13d9ef52","5278":"e0ec98b2bfcf70c9ea5f","5322":"3f2a7533de01a1a9a529","5965":"82b7fed88b88603bc8e6","6259":"0e0b8e93fc11a96b30d8","7040":"52864f38c2f08a4b7cb9","7219":"63a78333da5872945488","7828":"6caa255c9ddc31e8a76e","7893":"f48cf88e5599c031944c","8903":"d5428f945fee1bb47615","9574":"76474957fa0578a8fbae","9885":"47c474f256a13e3ca4a7","9893":"2c19625a4eb4da871497"}[chunkId] + ".chunk.css";
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/global */
/******/ 	(() => {
/******/ 		__webpack_require__.g = (function() {
/******/ 			if (typeof globalThis === 'object') return globalThis;
/******/ 			try {
/******/ 				return this || new Function('return this')();
/******/ 			} catch (e) {
/******/ 				if (typeof window === 'object') return window;
/******/ 			}
/******/ 		})();
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/harmony module decorator */
/******/ 	(() => {
/******/ 		__webpack_require__.hmd = (module) => {
/******/ 			module = Object.create(module);
/******/ 			if (!module.children) module.children = [];
/******/ 			Object.defineProperty(module, 'exports', {
/******/ 				enumerable: true,
/******/ 				set: () => {
/******/ 					throw new Error('ES Modules may not assign module.exports or exports.*, Use ESM export syntax, instead: ' + module.id);
/******/ 				}
/******/ 			});
/******/ 			return module;
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/hasOwnProperty shorthand */
/******/ 	(() => {
/******/ 		__webpack_require__.o = (obj, prop) => (Object.prototype.hasOwnProperty.call(obj, prop))
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/load script */
/******/ 	(() => {
/******/ 		var inProgress = {};
/******/ 		var dataWebpackPrefix = "unblock:";
/******/ 		// loadScript function to load a script via script tag
/******/ 		__webpack_require__.l = (url, done, key, chunkId) => {
/******/ 			if(inProgress[url]) { inProgress[url].push(done); return; }
/******/ 			var script, needAttach;
/******/ 			if(key !== undefined) {
/******/ 				var scripts = document.getElementsByTagName("script");
/******/ 				for(var i = 0; i < scripts.length; i++) {
/******/ 					var s = scripts[i];
/******/ 					if(s.getAttribute("src") == url || s.getAttribute("data-webpack") == dataWebpackPrefix + key) { script = s; break; }
/******/ 				}
/******/ 			}
/******/ 			if(!script) {
/******/ 				needAttach = true;
/******/ 				script = document.createElement('script');
/******/ 		
/******/ 				script.charset = 'utf-8';
/******/ 				script.timeout = 120;
/******/ 				if (__webpack_require__.nc) {
/******/ 					script.setAttribute("nonce", __webpack_require__.nc);
/******/ 				}
/******/ 				script.setAttribute("data-webpack", dataWebpackPrefix + key);
/******/ 				script.src = url;
/******/ 			}
/******/ 			inProgress[url] = [done];
/******/ 			var onScriptComplete = (prev, event) => {
/******/ 				// avoid mem leaks in IE.
/******/ 				script.onerror = script.onload = null;
/******/ 				clearTimeout(timeout);
/******/ 				var doneFns = inProgress[url];
/******/ 				delete inProgress[url];
/******/ 				script.parentNode && script.parentNode.removeChild(script);
/******/ 				doneFns && doneFns.forEach((fn) => (fn(event)));
/******/ 				if(prev) return prev(event);
/******/ 			}
/******/ 			;
/******/ 			var timeout = setTimeout(onScriptComplete.bind(null, undefined, { type: 'timeout', target: script }), 120000);
/******/ 			script.onerror = onScriptComplete.bind(null, script.onerror);
/******/ 			script.onload = onScriptComplete.bind(null, script.onload);
/******/ 			needAttach && document.head.appendChild(script);
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/make namespace object */
/******/ 	(() => {
/******/ 		// define __esModule on exports
/******/ 		__webpack_require__.r = (exports) => {
/******/ 			if(typeof Symbol !== 'undefined' && Symbol.toStringTag) {
/******/ 				Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
/******/ 			}
/******/ 			Object.defineProperty(exports, '__esModule', { value: true });
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/node module decorator */
/******/ 	(() => {
/******/ 		__webpack_require__.nmd = (module) => {
/******/ 			module.paths = [];
/******/ 			if (!module.children) module.children = [];
/******/ 			return module;
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/publicPath */
/******/ 	(() => {
/******/ 		__webpack_require__.p = "/static/assets/";
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/css loading */
/******/ 	(() => {
/******/ 		var createStylesheet = (chunkId, fullhref, resolve, reject) => {
/******/ 			var linkTag = document.createElement("link");
/******/ 		
/******/ 			linkTag.rel = "stylesheet";
/******/ 			linkTag.type = "text/css";
/******/ 			var onLinkComplete = (event) => {
/******/ 				// avoid mem leaks.
/******/ 				linkTag.onerror = linkTag.onload = null;
/******/ 				if (event.type === 'load') {
/******/ 					resolve();
/******/ 				} else {
/******/ 					var errorType = event && (event.type === 'load' ? 'missing' : event.type);
/******/ 					var realHref = event && event.target && event.target.href || fullhref;
/******/ 					var err = new Error("Loading CSS chunk " + chunkId + " failed.\n(" + realHref + ")");
/******/ 					err.code = "CSS_CHUNK_LOAD_FAILED";
/******/ 					err.type = errorType;
/******/ 					err.request = realHref;
/******/ 					linkTag.parentNode.removeChild(linkTag)
/******/ 					reject(err);
/******/ 				}
/******/ 			}
/******/ 			linkTag.onerror = linkTag.onload = onLinkComplete;
/******/ 			linkTag.href = fullhref;
/******/ 		
/******/ 			document.head.appendChild(linkTag);
/******/ 			return linkTag;
/******/ 		};
/******/ 		var findStylesheet = (href, fullhref) => {
/******/ 			var existingLinkTags = document.getElementsByTagName("link");
/******/ 			for(var i = 0; i < existingLinkTags.length; i++) {
/******/ 				var tag = existingLinkTags[i];
/******/ 				var dataHref = tag.getAttribute("data-href") || tag.getAttribute("href");
/******/ 				if(tag.rel === "stylesheet" && (dataHref === href || dataHref === fullhref)) return tag;
/******/ 			}
/******/ 			var existingStyleTags = document.getElementsByTagName("style");
/******/ 			for(var i = 0; i < existingStyleTags.length; i++) {
/******/ 				var tag = existingStyleTags[i];
/******/ 				var dataHref = tag.getAttribute("data-href");
/******/ 				if(dataHref === href || dataHref === fullhref) return tag;
/******/ 			}
/******/ 		};
/******/ 		var loadStylesheet = (chunkId) => {
/******/ 			return new Promise((resolve, reject) => {
/******/ 				var href = __webpack_require__.miniCssF(chunkId);
/******/ 				var fullhref = __webpack_require__.p + href;
/******/ 				if(findStylesheet(href, fullhref)) return resolve();
/******/ 				createStylesheet(chunkId, fullhref, resolve, reject);
/******/ 			});
/******/ 		}
/******/ 		// object to store loaded CSS chunks
/******/ 		var installedCssChunks = {
/******/ 			5152: 0
/******/ 		};
/******/ 		
/******/ 		__webpack_require__.f.miniCss = (chunkId, promises) => {
/******/ 			var cssChunks = {"3":1,"128":1,"423":1,"823":1,"1066":1,"1193":1,"1243":1,"1391":1,"1921":1,"2862":1,"3609":1,"3776":1,"4192":1,"4473":1,"5278":1,"5322":1,"5965":1,"6259":1,"7040":1,"7219":1,"7828":1,"7893":1,"8903":1,"9574":1,"9885":1,"9893":1};
/******/ 			if(installedCssChunks[chunkId]) promises.push(installedCssChunks[chunkId]);
/******/ 			else if(installedCssChunks[chunkId] !== 0 && cssChunks[chunkId]) {
/******/ 				promises.push(installedCssChunks[chunkId] = loadStylesheet(chunkId).then(() => {
/******/ 					installedCssChunks[chunkId] = 0;
/******/ 				}, (e) => {
/******/ 					delete installedCssChunks[chunkId];
/******/ 					throw e;
/******/ 				}));
/******/ 			}
/******/ 		};
/******/ 		
/******/ 		// no hmr
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/jsonp chunk loading */
/******/ 	(() => {
/******/ 		// no baseURI
/******/ 		
/******/ 		// object to store loaded and loading chunks
/******/ 		// undefined = chunk not loaded, null = chunk preloaded/prefetched
/******/ 		// [resolve, reject, Promise] = chunk loading, 0 = chunk loaded
/******/ 		var installedChunks = {
/******/ 			5152: 0
/******/ 		};
/******/ 		
/******/ 		__webpack_require__.f.j = (chunkId, promises) => {
/******/ 				// JSONP chunk loading for javascript
/******/ 				var installedChunkData = __webpack_require__.o(installedChunks, chunkId) ? installedChunks[chunkId] : undefined;
/******/ 				if(installedChunkData !== 0) { // 0 means "already installed".
/******/ 		
/******/ 					// a Promise means "currently loading".
/******/ 					if(installedChunkData) {
/******/ 						promises.push(installedChunkData[2]);
/******/ 					} else {
/******/ 						if(3 != chunkId) {
/******/ 							// setup Promise in chunk cache
/******/ 							var promise = new Promise((resolve, reject) => (installedChunkData = installedChunks[chunkId] = [resolve, reject]));
/******/ 							promises.push(installedChunkData[2] = promise);
/******/ 		
/******/ 							// start chunk loading
/******/ 							var url = __webpack_require__.p + __webpack_require__.u(chunkId);
/******/ 							// create error before stack unwound to get useful stacktrace later
/******/ 							var error = new Error();
/******/ 							var loadingEnded = (event) => {
/******/ 								if(__webpack_require__.o(installedChunks, chunkId)) {
/******/ 									installedChunkData = installedChunks[chunkId];
/******/ 									if(installedChunkData !== 0) installedChunks[chunkId] = undefined;
/******/ 									if(installedChunkData) {
/******/ 										var errorType = event && (event.type === 'load' ? 'missing' : event.type);
/******/ 										var realSrc = event && event.target && event.target.src;
/******/ 										error.message = 'Loading chunk ' + chunkId + ' failed.\n(' + errorType + ': ' + realSrc + ')';
/******/ 										error.name = 'ChunkLoadError';
/******/ 										error.type = errorType;
/******/ 										error.request = realSrc;
/******/ 										installedChunkData[1](error);
/******/ 									}
/******/ 								}
/******/ 							};
/******/ 							__webpack_require__.l(url, loadingEnded, "chunk-" + chunkId, chunkId);
/******/ 						} else installedChunks[chunkId] = 0;
/******/ 					}
/******/ 				}
/******/ 		};
/******/ 		
/******/ 		// no prefetching
/******/ 		
/******/ 		// no preloaded
/******/ 		
/******/ 		// no HMR
/******/ 		
/******/ 		// no HMR manifest
/******/ 		
/******/ 		__webpack_require__.O.j = (chunkId) => (installedChunks[chunkId] === 0);
/******/ 		
/******/ 		// install a JSONP callback for chunk loading
/******/ 		var webpackJsonpCallback = (parentChunkLoadingFunction, data) => {
/******/ 			var [chunkIds, moreModules, runtime] = data;
/******/ 			// add "moreModules" to the modules object,
/******/ 			// then flag all "chunkIds" as loaded and fire callback
/******/ 			var moduleId, chunkId, i = 0;
/******/ 			if(chunkIds.some((id) => (installedChunks[id] !== 0))) {
/******/ 				for(moduleId in moreModules) {
/******/ 					if(__webpack_require__.o(moreModules, moduleId)) {
/******/ 						__webpack_require__.m[moduleId] = moreModules[moduleId];
/******/ 					}
/******/ 				}
/******/ 				if(runtime) var result = runtime(__webpack_require__);
/******/ 			}
/******/ 			if(parentChunkLoadingFunction) parentChunkLoadingFunction(data);
/******/ 			for(;i < chunkIds.length; i++) {
/******/ 				chunkId = chunkIds[i];
/******/ 				if(__webpack_require__.o(installedChunks, chunkId) && installedChunks[chunkId]) {
/******/ 					installedChunks[chunkId][0]();
/******/ 				}
/******/ 				installedChunks[chunkIds[i]] = 0;
/******/ 			}
/******/ 			return __webpack_require__.O(result);
/******/ 		}
/******/ 		
/******/ 		var chunkLoadingGlobal = globalThis["webpackChunkunblock"] = globalThis["webpackChunkunblock"] || [];
/******/ 		chunkLoadingGlobal.forEach(webpackJsonpCallback.bind(null, 0));
/******/ 		chunkLoadingGlobal.push = webpackJsonpCallback.bind(null, chunkLoadingGlobal.push.bind(chunkLoadingGlobal));
/******/ 	})();
/******/ 	
/************************************************************************/
/******/ 	
/******/ 	// module factories are used so entry inlining is disabled
/******/ 	// startup
/******/ 	// Load entry module and return exports
/******/ 	__webpack_require__.O(undefined, [1216,504,7550,4772,7211,5110,7017,9968,8483,8135,7591,7341,3401,4052,621,4174], () => (__webpack_require__(26009)))
/******/ 	var __webpack_exports__ = __webpack_require__.O(undefined, [1216,504,7550,4772,7211,5110,7017,9968,8483,8135,7591,7341,3401,4052,621,4174], () => (__webpack_require__(42669)))
/******/ 	__webpack_exports__ = __webpack_require__.O(__webpack_exports__);
/******/ 	
/******/ })()
;
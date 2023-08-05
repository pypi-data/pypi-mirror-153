/******/ (() => { // webpackBootstrap
/******/ 	var __webpack_modules__ = ({

/***/ 15926:
/***/ (function(module, exports) {

var __WEBPACK_AMD_DEFINE_FACTORY__, __WEBPACK_AMD_DEFINE_ARRAY__, __WEBPACK_AMD_DEFINE_RESULT__;// Uses CommonJS, AMD or browser globals to create a module.
// Based on: https://github.com/umdjs/umd/blob/master/commonjsStrict.js
(function (root, factory) {
    if (true) {
        // AMD. Register as an anonymous module.
        !(__WEBPACK_AMD_DEFINE_ARRAY__ = [exports], __WEBPACK_AMD_DEFINE_FACTORY__ = (factory),
		__WEBPACK_AMD_DEFINE_RESULT__ = (typeof __WEBPACK_AMD_DEFINE_FACTORY__ === 'function' ?
		(__WEBPACK_AMD_DEFINE_FACTORY__.apply(exports, __WEBPACK_AMD_DEFINE_ARRAY__)) : __WEBPACK_AMD_DEFINE_FACTORY__),
		__WEBPACK_AMD_DEFINE_RESULT__ !== undefined && (module.exports = __WEBPACK_AMD_DEFINE_RESULT__));
    } else {}
}(this, function (exports) {
var rison = exports;

//////////////////////////////////////////////////
//
//  the stringifier is based on
//    http://json.org/json.js as of 2006-04-28 from json.org
//  the parser is based on 
//    http://osteele.com/sources/openlaszlo/json
//

if (typeof rison == 'undefined')
    window.rison = {};

/**
 *  rules for an uri encoder that is more tolerant than encodeURIComponent
 *
 *  encodeURIComponent passes  ~!*()-_.'
 *
 *  we also allow              ,:@$/
 *
 */
rison.uri_ok = {  // ok in url paths and in form query args
            '~': true,  '!': true,  '*': true,  '(': true,  ')': true,
            '-': true,  '_': true,  '.': true,  ',': true,
            ':': true,  '@': true,  '$': true,
            "'": true,  '/': true
};

/*
 * we divide the uri-safe glyphs into three sets
 *   <rison> - used by rison                         ' ! : ( ) ,
 *   <reserved> - not common in strings, reserved    * @ $ & ; =
 *
 * we define <identifier> as anything that's not forbidden
 */

/**
 * punctuation characters that are legal inside ids.
 */
// this var isn't actually used
//rison.idchar_punctuation = "_-./~";  

(function () {
    var l = [];
    for (var hi = 0; hi < 16; hi++) {
        for (var lo = 0; lo < 16; lo++) {
            if (hi+lo == 0) continue;
            var c = String.fromCharCode(hi*16 + lo);
            if (! /\w|[-_.\/~]/.test(c))
                l.push('\\u00' + hi.toString(16) + lo.toString(16));
        }
    }
    /**
     * characters that are illegal inside ids.
     * <rison> and <reserved> classes are illegal in ids.
     *
     */
    rison.not_idchar = l.join('')
    //idcrx = new RegExp('[' + rison.not_idchar + ']');
    //console.log('NOT', (idcrx.test(' ')) );
})();
//rison.not_idchar  = " \t\r\n\"<>[]{}'!=:(),*@$;&";
rison.not_idchar  = " '!:(),*@$";


/**
 * characters that are illegal as the start of an id
 * this is so ids can't look like numbers.
 */
rison.not_idstart = "-0123456789";


(function () {
    var idrx = '[^' + rison.not_idstart + rison.not_idchar + 
               '][^' + rison.not_idchar + ']*';

    rison.id_ok = new RegExp('^' + idrx + '$');

    // regexp to find the end of an id when parsing
    // g flag on the regexp is necessary for iterative regexp.exec()
    rison.next_id = new RegExp(idrx, 'g');
})();

/**
 * this is like encodeURIComponent() but quotes fewer characters.
 *
 * @see rison.uri_ok
 *
 * encodeURIComponent passes   ~!*()-_.'
 * rison.quote also passes   ,:@$/
 *   and quotes " " as "+" instead of "%20"
 */
rison.quote = function(x) {
    if (/^[-A-Za-z0-9~!*()_.',:@$\/]*$/.test(x))
        return x;

    return encodeURIComponent(x)
        .replace('%2C', ',', 'g')
        .replace('%3A', ':', 'g')
        .replace('%40', '@', 'g')
        .replace('%24', '$', 'g')
        .replace('%2F', '/', 'g')
        .replace('%20', '+', 'g');
};


//
//  based on json.js 2006-04-28 from json.org
//  license: http://www.json.org/license.html
//
//  hacked by nix for use in uris.
//

(function () {
    var sq = { // url-ok but quoted in strings
               "'": true,  '!': true
    },
    s = {
            array: function (x) {
                var a = ['!('], b, f, i, l = x.length, v;
                for (i = 0; i < l; i += 1) {
                    v = x[i];
                    f = s[typeof v];
                    if (f) {
                        v = f(v);
                        if (typeof v == 'string') {
                            if (b) {
                                a[a.length] = ',';
                            }
                            a[a.length] = v;
                            b = true;
                        }
                    }
                }
                a[a.length] = ')';
                return a.join('');
            },
            'boolean': function (x) {
                if (x)
                    return '!t';
                return '!f'
            },
            'null': function (x) {
                return "!n";
            },
            number: function (x) {
                if (!isFinite(x))
                    return '!n';
                // strip '+' out of exponent, '-' is ok though
                return String(x).replace(/\+/,'');
            },
            object: function (x) {
                if (x) {
                    if (x instanceof Array) {
                        return s.array(x);
                    }
                    // WILL: will this work on non-Firefox browsers?
                    if (typeof x.__prototype__ === 'object' && typeof x.__prototype__.encode_rison !== 'undefined')
                        return x.encode_rison();

                    var a = ['('], b, f, i, v, ki, ks=[];
                    for (i in x)
                        ks[ks.length] = i;
                    ks.sort();
                    for (ki = 0; ki < ks.length; ki++) {
                        i = ks[ki];
                        v = x[i];
                        f = s[typeof v];
                        if (f) {
                            v = f(v);
                            if (typeof v == 'string') {
                                if (b) {
                                    a[a.length] = ',';
                                }
                                a.push(s.string(i), ':', v);
                                b = true;
                            }
                        }
                    }
                    a[a.length] = ')';
                    return a.join('');
                }
                return '!n';
            },
            string: function (x) {
                if (x == '')
                    return "''";

                if (rison.id_ok.test(x))
                    return x;

                x = x.replace(/(['!])/g, function(a, b) {
                    if (sq[b]) return '!'+b;
                    return b;
                });
                return "'" + x + "'";
            },
            undefined: function (x) {
                throw new Error("rison can't encode the undefined value");
            }
        };


    /**
     * rison-encode a javascript structure
     *
     *  implemementation based on Douglas Crockford's json.js:
     *    http://json.org/json.js as of 2006-04-28 from json.org
     *
     */
    rison.encode = function (v) {
        return s[typeof v](v);
    };

    /**
     * rison-encode a javascript object without surrounding parens
     *
     */
    rison.encode_object = function (v) {
        if (typeof v != 'object' || v === null || v instanceof Array)
            throw new Error("rison.encode_object expects an object argument");
        var r = s[typeof v](v);
        return r.substring(1, r.length-1);
    };

    /**
     * rison-encode a javascript array without surrounding parens
     *
     */
    rison.encode_array = function (v) {
        if (!(v instanceof Array))
            throw new Error("rison.encode_array expects an array argument");
        var r = s[typeof v](v);
        return r.substring(2, r.length-1);
    };

    /**
     * rison-encode and uri-encode a javascript structure
     *
     */
    rison.encode_uri = function (v) {
        return rison.quote(s[typeof v](v));
    };

})();




//
// based on openlaszlo-json and hacked by nix for use in uris.
//
// Author: Oliver Steele
// Copyright: Copyright 2006 Oliver Steele.  All rights reserved.
// Homepage: http://osteele.com/sources/openlaszlo/json
// License: MIT License.
// Version: 1.0


/**
 * parse a rison string into a javascript structure.
 *
 * this is the simplest decoder entry point.
 *
 *  based on Oliver Steele's OpenLaszlo-JSON
 *     http://osteele.com/sources/openlaszlo/json
 */
rison.decode = function(r) {
    var errcb = function(e) { throw Error('rison decoder error: ' + e); };
    var p = new rison.parser(errcb);
    return p.parse(r);
};

/**
 * parse an o-rison string into a javascript structure.
 *
 * this simply adds parentheses around the string before parsing.
 */
rison.decode_object = function(r) {
    return rison.decode('('+r+')');
};

/**
 * parse an a-rison string into a javascript structure.
 *
 * this simply adds array markup around the string before parsing.
 */
rison.decode_array = function(r) {
    return rison.decode('!('+r+')');
};


/**
 * construct a new parser object for reuse.
 *
 * @constructor
 * @class A Rison parser class.  You should probably 
 *        use rison.decode instead. 
 * @see rison.decode
 */
rison.parser = function (errcb) {
    this.errorHandler = errcb;
};

/**
 * a string containing acceptable whitespace characters.
 * by default the rison decoder tolerates no whitespace.
 * to accept whitespace set rison.parser.WHITESPACE = " \t\n\r\f";
 */
rison.parser.WHITESPACE = "";

// expose this as-is?
rison.parser.prototype.setOptions = function (options) {
    if (options['errorHandler'])
        this.errorHandler = options.errorHandler;
};

/**
 * parse a rison string into a javascript structure.
 */
rison.parser.prototype.parse = function (str) {
    this.string = str;
    this.index = 0;
    this.message = null;
    var value = this.readValue();
    if (!this.message && this.next())
        value = this.error("unable to parse string as rison: '" + rison.encode(str) + "'");
    if (this.message && this.errorHandler)
        this.errorHandler(this.message, this.index);
    return value;
};

rison.parser.prototype.error = function (message) {
    if (typeof(console) != 'undefined')
        console.log('rison parser error: ', message);
    this.message = message;
    return undefined;
}
    
rison.parser.prototype.readValue = function () {
    var c = this.next();
    var fn = c && this.table[c];

    if (fn)
        return fn.apply(this);

    // fell through table, parse as an id

    var s = this.string;
    var i = this.index-1;

    // Regexp.lastIndex may not work right in IE before 5.5?
    // g flag on the regexp is also necessary
    rison.next_id.lastIndex = i;
    var m = rison.next_id.exec(s);

    // console.log('matched id', i, r.lastIndex);

    if (m.length > 0) {
        var id = m[0];
        this.index = i+id.length;
        return id;  // a string
    }

    if (c) return this.error("invalid character: '" + c + "'");
    return this.error("empty expression");
}

rison.parser.parse_array = function (parser) {
    var ar = [];
    var c;
    while ((c = parser.next()) != ')') {
        if (!c) return parser.error("unmatched '!('");
        if (ar.length) {
            if (c != ',')
                parser.error("missing ','");
        } else if (c == ',') {
            return parser.error("extra ','");
        } else
            --parser.index;
        var n = parser.readValue();
        if (typeof n == "undefined") return undefined;
        ar.push(n);
    }
    return ar;
};

rison.parser.bangs = {
    t: true,
    f: false,
    n: null,
    '(': rison.parser.parse_array
}

rison.parser.prototype.table = {
    '!': function () {
        var s = this.string;
        var c = s.charAt(this.index++);
        if (!c) return this.error('"!" at end of input');
        var x = rison.parser.bangs[c];
        if (typeof(x) == 'function') {
            return x.call(null, this);
        } else if (typeof(x) == 'undefined') {
            return this.error('unknown literal: "!' + c + '"');
        }
        return x;
    },
    '(': function () {
        var o = {};
        var c;
        var count = 0;
        while ((c = this.next()) != ')') {
            if (count) {
                if (c != ',')
                    this.error("missing ','");
            } else if (c == ',') {
                return this.error("extra ','");
            } else
                --this.index;
            var k = this.readValue();
            if (typeof k == "undefined") return undefined;
            if (this.next() != ':') return this.error("missing ':'");
            var v = this.readValue();
            if (typeof v == "undefined") return undefined;
            o[k] = v;
            count++;
        }
        return o;
    },
    "'": function () {
        var s = this.string;
        var i = this.index;
        var start = i;
        var segments = [];
        var c;
        while ((c = s.charAt(i++)) != "'") {
            //if (i == s.length) return this.error('unmatched "\'"');
            if (!c) return this.error('unmatched "\'"');
            if (c == '!') {
                if (start < i-1)
                    segments.push(s.slice(start, i-1));
                c = s.charAt(i++);
                if ("!'".indexOf(c) >= 0) {
                    segments.push(c);
                } else {
                    return this.error('invalid string escape: "!'+c+'"');
                }
                start = i;
            }
        }
        if (start < i-1)
            segments.push(s.slice(start, i-1));
        this.index = i;
        return segments.length == 1 ? segments[0] : segments.join('');
    },
    // Also any digit.  The statement that follows this table
    // definition fills in the digits.
    '-': function () {
        var s = this.string;
        var i = this.index;
        var start = i-1;
        var state = 'int';
        var permittedSigns = '-';
        var transitions = {
            'int+.': 'frac',
            'int+e': 'exp',
            'frac+e': 'exp'
        };
        do {
            var c = s.charAt(i++);
            if (!c) break;
            if ('0' <= c && c <= '9') continue;
            if (permittedSigns.indexOf(c) >= 0) {
                permittedSigns = '';
                continue;
            }
            state = transitions[state+'+'+c.toLowerCase()];
            if (state == 'exp') permittedSigns = '-';
        } while (state);
        this.index = --i;
        s = s.slice(start, i)
        if (s == '-') return this.error("invalid number");
        return Number(s);
    }
};
// copy table['-'] to each of table[i] | i <- '0'..'9':
(function (table) {
    for (var i = 0; i <= 9; i++)
        table[String(i)] = table['-'];
})(rison.parser.prototype.table);

// return the next non-whitespace character, or undefined
rison.parser.prototype.next = function () {
    var s = this.string;
    var i = this.index;
    do {
        if (i == s.length) return undefined;
        var c = s.charAt(i++);
    } while (rison.parser.WHITESPACE.indexOf(c) >= 0);
    this.index = i;
    return c;
};

// End of UMD module wrapper
}));


/***/ }),

/***/ 95639:
/***/ ((__unused_webpack_module, __unused_webpack___webpack_exports__, __webpack_require__) => {

"use strict";

// EXTERNAL MODULE: ./node_modules/react/index.js
var react = __webpack_require__(67294);
// EXTERNAL MODULE: ./node_modules/@hot-loader/react-dom/index.js
var react_dom = __webpack_require__(9060);
// EXTERNAL MODULE: ./node_modules/@emotion/react/dist/emotion-element-99289b21.browser.esm.js + 2 modules
var emotion_element_99289b21_browser_esm = __webpack_require__(68135);
// EXTERNAL MODULE: ./node_modules/@emotion/cache/dist/emotion-cache.browser.esm.js + 1 modules
var emotion_cache_browser_esm = __webpack_require__(23882);
// EXTERNAL MODULE: ./node_modules/@babel/runtime-corejs3/helpers/extends.js
var helpers_extends = __webpack_require__(5872);
var extends_default = /*#__PURE__*/__webpack_require__.n(helpers_extends);
// EXTERNAL MODULE: ./node_modules/lodash/debounce.js
var debounce = __webpack_require__(23279);
var debounce_default = /*#__PURE__*/__webpack_require__.n(debounce);
// EXTERNAL MODULE: ./node_modules/@superset-ui/core/esm/style/index.js
var style = __webpack_require__(37840);
// EXTERNAL MODULE: ./node_modules/@emotion/react/dist/emotion-react.browser.esm.js + 1 modules
var emotion_react_browser_esm = __webpack_require__(11965);
// EXTERNAL MODULE: ./node_modules/@babel/runtime-corejs3/core-js-stable/url-search-params.js
var url_search_params = __webpack_require__(94435);
var url_search_params_default = /*#__PURE__*/__webpack_require__.n(url_search_params);
// EXTERNAL MODULE: ./node_modules/@superset-ui/core/esm/connection/SupersetClient.js
var SupersetClient = __webpack_require__(21173);
// EXTERNAL MODULE: ./node_modules/rison/js/rison.js
var rison = __webpack_require__(15926);
var rison_default = /*#__PURE__*/__webpack_require__.n(rison);
// EXTERNAL MODULE: ./src/utils/getClientErrorObject.ts
var getClientErrorObject = __webpack_require__(98286);
;// CONCATENATED MODULE: ./src/utils/urlUtils.ts
 /**
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * 'License'); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * 'AS IS' BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 * KIND, either express or implied.  See the License for the
 * specific language governing permissions and limitations
 * under the License.
 */



function getUrlParam({ name, type }) {
  const urlParam = new (url_search_params_default())(window.location.search).get(name);
  switch (type) {
    case 'number':
      if (!urlParam) {
        return null;
      }
      if (urlParam === 'true') {
        return 1;
      }
      if (urlParam === 'false') {
        return 0;
      }
      if (!Number.isNaN(Number(urlParam))) {
        return Number(urlParam);
      }
      return null;
    case 'object':
      if (!urlParam) {
        return null;
      }
      return JSON.parse(urlParam);
    case 'boolean':
      if (!urlParam) {
        return null;
      }
      return urlParam !== 'false' && urlParam !== '0';
    case 'rison':
      if (!urlParam) {
        return null;
      }
      try {
        return rison_default().decode(urlParam);
      }
      catch {
        return null;
      }
    default:
      return urlParam;}

}
function getShortUrl(longUrl) {
  return SupersetClient/* default.post */.Z.post({
    endpoint: '/r/shortner/',
    postPayload: { data: `/${longUrl}` },
    parseMethod: 'text',
    stringify: false // the url saves with an extra set of string quotes without this
  }).
  then(({ text }) => text).
  catch((response) =>
  // @ts-ignore
  (0,getClientErrorObject/* getClientErrorObject */.O)(response).then(({ error, statusText }) => Promise.reject(error || statusText)));
}
// EXTERNAL MODULE: ./src/common/components/index.tsx
var components = __webpack_require__(82191);
// EXTERNAL MODULE: ./src/components/Tooltip/index.tsx
var Tooltip = __webpack_require__(58593);
// EXTERNAL MODULE: ./node_modules/react-router-dom/esm/react-router-dom.js
var react_router_dom = __webpack_require__(73727);
// EXTERNAL MODULE: ./node_modules/antd/es/grid/index.js
var grid = __webpack_require__(75302);
// EXTERNAL MODULE: ./node_modules/antd/es/row/index.js
var row = __webpack_require__(71230);
// EXTERNAL MODULE: ./node_modules/antd/es/col/index.js
var col = __webpack_require__(15746);
// EXTERNAL MODULE: ./src/components/Icons/index.tsx + 3 modules
var Icons = __webpack_require__(38097);
;// CONCATENATED MODULE: ./src/constants.ts
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
const DATETIME_WITH_TIME_ZONE = 'YYYY-MM-DD HH:mm:ssZ';
const TIME_WITH_MS = 'HH:mm:ss.SSS';
const BOOL_TRUE_DISPLAY = 'True';
const BOOL_FALSE_DISPLAY = 'False';
const URL_PARAMS = {
  standalone: {
    name: 'standalone',
    type: 'number' },

  preselectFilters: {
    name: 'preselect_filters',
    type: 'object' },

  nativeFilters: {
    name: 'native_filters',
    type: 'rison' },

  filterSet: {
    name: 'filter_set',
    type: 'string' },

  showFilters: {
    name: 'show_filters',
    type: 'boolean' } };


/**
 * Faster debounce delay for inputs without expensive operation.
 */
const FAST_DEBOUNCE = 250;
/**
 * Slower debounce delay for inputs with expensive API calls.
 */
const SLOW_DEBOUNCE = 500;
// EXTERNAL MODULE: ./node_modules/@superset-ui/core/esm/translation/TranslatorSingleton.js + 1 modules
var TranslatorSingleton = __webpack_require__(60650);
;// CONCATENATED MODULE: ./src/components/Menu/LanguagePicker.tsx
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




const { SubMenu } = components/* MainNav */.$t;
const StyledLabel = style/* styled.div */.iK.div`
  display: flex;
  align-items: center;

  & i {
    margin-right: ${({ theme }) => theme.gridUnit * 2}px;
  }

  & a {
    display: block;
    width: 150px;
    word-wrap: break-word;
    text-decoration: none;
  }
`;
const StyledFlag = style/* styled.i */.iK.i`
  margin-top: 2px;
`;
function LanguagePicker(props) {
  const { locale, languages, ...rest } = props;
  return (0,emotion_react_browser_esm.jsx)(SubMenu, extends_default()({ "aria-label": "Languages", title: (0,emotion_react_browser_esm.jsx)("div", { className: "f16" },
    (0,emotion_react_browser_esm.jsx)(StyledFlag, { className: `flag ${languages[locale].flag}` })),
    icon: (0,emotion_react_browser_esm.jsx)(Icons/* default.TriangleDown */.Z.TriangleDown, null) }, rest),
  Object.keys(languages).map((langKey) => (0,emotion_react_browser_esm.jsx)(components/* MainNav.Item */.$t.Item, { key: langKey, style: { whiteSpace: 'normal', height: 'auto' } },
  (0,emotion_react_browser_esm.jsx)(StyledLabel, { className: "f16" },
  (0,emotion_react_browser_esm.jsx)("i", { className: `flag ${languages[langKey].flag}` }),
  (0,emotion_react_browser_esm.jsx)("a", { href: languages[langKey].url }, languages[langKey].name)))));



}
;// CONCATENATED MODULE: ./src/components/Menu/MenuRight.tsx
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






const dropdownItems = [
{
  label: (0,TranslatorSingleton.t)('SQL query'),
  url: '/superset/sqllab?new=true',
  icon: 'fa-fw fa-search' },

{
  label: (0,TranslatorSingleton.t)('Chart'),
  url: '/chart/add',
  icon: 'fa-fw fa-bar-chart' },

{
  label: (0,TranslatorSingleton.t)('Dashboard'),
  url: '/dashboard/new',
  icon: 'fa-fw fa-dashboard' }];


const versionInfoStyles = (theme) => emotion_react_browser_esm.css`
  padding: ${theme.gridUnit * 1.5}px ${theme.gridUnit * 4}px
    ${theme.gridUnit * 4}px ${theme.gridUnit * 7}px;
  color: ${theme.colors.grayscale.base};
  font-size: ${theme.typography.sizes.xs}px;
  white-space: nowrap;
`;
const StyledI = style/* styled.div */.iK.div`
  color: ${({ theme }) => theme.colors.primary.dark1};
`;
const StyledDiv = style/* styled.div */.iK.div`
  display: flex;
  flex-direction: row;
  justify-content: ${({ align }) => align};
  align-items: center;
  margin-right: ${({ theme }) => theme.gridUnit}px;
  .ant-menu-submenu-title > svg {
    top: ${({ theme }) => theme.gridUnit * 5.25}px;
  }
`;
const StyledAnchor = style/* styled.a */.iK.a`
  padding-right: ${({ theme }) => theme.gridUnit}px;
  padding-left: ${({ theme }) => theme.gridUnit}px;
`;
const { SubMenu: MenuRight_SubMenu } = components/* MainNav */.$t;
const RightMenu = ({ align, settings, navbarRight, isFrontendRoute }) => (0,emotion_react_browser_esm.jsx)(StyledDiv, { align: align },
(0,emotion_react_browser_esm.jsx)(components/* MainNav */.$t, { mode: "horizontal" },
!navbarRight.user_is_anonymous && (0,emotion_react_browser_esm.jsx)(MenuRight_SubMenu, { title: (0,emotion_react_browser_esm.jsx)(StyledI, { className: "fa fa-plus" }), icon: (0,emotion_react_browser_esm.jsx)(Icons/* default.TriangleDown */.Z.TriangleDown, null) },
dropdownItems.map((menu) => (0,emotion_react_browser_esm.jsx)(components/* MainNav.Item */.$t.Item, { key: menu.label },
(0,emotion_react_browser_esm.jsx)("a", { href: menu.url },
(0,emotion_react_browser_esm.jsx)("i", { className: `fa ${menu.icon}` }), ' ',
menu.label)))),



(0,emotion_react_browser_esm.jsx)(MenuRight_SubMenu, { title: "Settings", icon: (0,emotion_react_browser_esm.jsx)(Icons/* default.TriangleDown */.Z.TriangleDown, { iconSize: "xl" }) },
settings.map((section, index) => {var _section$childs;return [
  (0,emotion_react_browser_esm.jsx)(components/* MainNav.ItemGroup */.$t.ItemGroup, { key: `${section.label}`, title: section.label }, (_section$childs =
  section.childs) == null ? void 0 : _section$childs.map((child) => {
    if (typeof child !== 'string') {
      return (0,emotion_react_browser_esm.jsx)(components/* MainNav.Item */.$t.Item, { key: `${child.label}` },
      isFrontendRoute(child.url) ? (0,emotion_react_browser_esm.jsx)(react_router_dom/* Link */.rU, { to: child.url || '' }, child.label) : (0,emotion_react_browser_esm.jsx)("a", { href: child.url }, child.label));

    }
    return null;
  })),

  index < settings.length - 1 && (0,emotion_react_browser_esm.jsx)(components/* MainNav.Divider */.$t.Divider, null)];}),


!navbarRight.user_is_anonymous && [
(0,emotion_react_browser_esm.jsx)(components/* MainNav.Divider */.$t.Divider, { key: "user-divider" }),
(0,emotion_react_browser_esm.jsx)(components/* MainNav.ItemGroup */.$t.ItemGroup, { key: "user-section", title: (0,TranslatorSingleton.t)('User') },
navbarRight.user_profile_url && (0,emotion_react_browser_esm.jsx)(components/* MainNav.Item */.$t.Item, { key: "profile" },
(0,emotion_react_browser_esm.jsx)("a", { href: navbarRight.user_profile_url }, (0,TranslatorSingleton.t)('Profile'))),

navbarRight.user_info_url && (0,emotion_react_browser_esm.jsx)(components/* MainNav.Item */.$t.Item, { key: "info" },
(0,emotion_react_browser_esm.jsx)("a", { href: navbarRight.user_info_url }, (0,TranslatorSingleton.t)('Info'))),

(0,emotion_react_browser_esm.jsx)(components/* MainNav.Item */.$t.Item, { key: "logout" },
(0,emotion_react_browser_esm.jsx)("a", { href: navbarRight.user_logout_url }, (0,TranslatorSingleton.t)('Logout'))))],



(navbarRight.version_string ||
navbarRight.version_sha ||
navbarRight.build_number) && [
(0,emotion_react_browser_esm.jsx)(components/* MainNav.Divider */.$t.Divider, { key: "version-info-divider" }),
(0,emotion_react_browser_esm.jsx)(components/* MainNav.ItemGroup */.$t.ItemGroup, { key: "about-section", title: (0,TranslatorSingleton.t)('About') },
(0,emotion_react_browser_esm.jsx)("div", { className: "about-section" },





navbarRight.version_string && (0,emotion_react_browser_esm.jsx)("div", { css: versionInfoStyles }, "Version: ",
navbarRight.version_string),

navbarRight.version_sha && (0,emotion_react_browser_esm.jsx)("div", { css: versionInfoStyles }, "SHA: ",
navbarRight.version_sha),

navbarRight.build_number && (0,emotion_react_browser_esm.jsx)("div", { css: versionInfoStyles }, "Build: ",
navbarRight.build_number)))]),





navbarRight.show_language_picker && (0,emotion_react_browser_esm.jsx)(LanguagePicker, { locale: navbarRight.locale, languages: navbarRight.languages })),

navbarRight.documentation_url && (0,emotion_react_browser_esm.jsx)(StyledAnchor, { href: navbarRight.documentation_url, target: "_blank", rel: "noreferrer", title: (0,TranslatorSingleton.t)('Documentation') },
(0,emotion_react_browser_esm.jsx)("i", { className: "fa fa-question" }), "\xA0"),


navbarRight.bug_report_url && (0,emotion_react_browser_esm.jsx)(StyledAnchor, { href: navbarRight.bug_report_url, target: "_blank", rel: "noreferrer", title: (0,TranslatorSingleton.t)('Report a bug') },
(0,emotion_react_browser_esm.jsx)("i", { className: "fa fa-bug" })),

navbarRight.user_is_anonymous && (0,emotion_react_browser_esm.jsx)(StyledAnchor, { href: navbarRight.user_login_url },
(0,emotion_react_browser_esm.jsx)("i", { className: "fa fa-fw fa-sign-in" }),
(0,TranslatorSingleton.t)('Login')));


/* harmony default export */ const MenuRight = (RightMenu);
;// CONCATENATED MODULE: ./src/components/Menu/Menu.tsx
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












const StyledHeader = style/* styled.header */.iK.header`
  background-color: white;
  margin-bottom: 2px;
  &:nth-last-of-type(2) nav {
    margin-bottom: 2px;
  }

  .caret {
    display: none;
  }
  .navbar-brand {
    display: flex;
    flex-direction: column;
    justify-content: center;
  }
  .navbar-brand-text {
    border-left: 1px solid ${({ theme }) => theme.colors.grayscale.light2};
    border-right: 1px solid ${({ theme }) => theme.colors.grayscale.light2};
    height: 100%;
    color: ${({ theme }) => theme.colors.grayscale.dark1};
    padding-left: ${({ theme }) => theme.gridUnit * 4}px;
    padding-right: ${({ theme }) => theme.gridUnit * 4}px;
    margin-right: ${({ theme }) => theme.gridUnit * 6}px;
    font-size: ${({ theme }) => theme.gridUnit * 4}px;
    float: left;
    display: flex;
    flex-direction: column;
    justify-content: center;

    span {
      max-width: ${({ theme }) => theme.gridUnit * 58}px;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
    @media (max-width: 1127px) {
      display: none;
    }
  }
  .main-nav .ant-menu-submenu-title > svg {
    top: ${({ theme }) => theme.gridUnit * 5.25}px;
  }
  @media (max-width: 767px) {
    .navbar-brand {
      float: none;
    }
  }
  .ant-menu-horizontal .ant-menu-item {
    height: 100%;
    line-height: inherit;
  }
  .ant-menu > .ant-menu-item > a {
    padding: ${({ theme }) => theme.gridUnit * 4}px;
  }
  @media (max-width: 767px) {
    .ant-menu-item {
      padding: 0 ${({ theme }) => theme.gridUnit * 6}px 0
        ${({ theme }) => theme.gridUnit * 3}px !important;
    }
    .ant-menu > .ant-menu-item > a {
      padding: 0px;
    }
    .main-nav .ant-menu-submenu-title > svg:nth-child(1) {
      display: none;
    }
    .ant-menu-item-active > a {
      &:hover {
        color: ${({ theme }) => theme.colors.primary.base} !important;
        background-color: transparent !important;
      }
    }
  }

  .ant-menu-item a {
    &:hover {
      color: ${({ theme }) => theme.colors.grayscale.dark1};
      background-color: ${({ theme }) => theme.colors.primary.light5};
      border-bottom: none;
      margin: 0;
      &:after {
        opacity: 1;
        width: 100%;
      }
    }
  }
`;
const { SubMenu: Menu_SubMenu } = components/* MainNav */.$t;
const { useBreakpoint } = grid/* default */.ZP;
function Menu({ data: { menu, brand, navbar_right: navbarRight, settings }, isFrontendRoute = () => false }) {
  const [showMenu, setMenu] = (0,react.useState)('horizontal');
  const screens = useBreakpoint();
  (0,react.useEffect)(() => {
    function handleResize() {
      if (window.innerWidth <= 767) {
        setMenu('inline');
      } else

      setMenu('horizontal');
    }
    handleResize();
    const windowResize = debounce_default()(() => handleResize(), 10);
    window.addEventListener('resize', windowResize);
    return () => window.removeEventListener('resize', windowResize);
  }, []);
  const standalone = getUrlParam(URL_PARAMS.standalone);
  if (standalone)
  return (0,emotion_react_browser_esm.jsx)(react.Fragment, null);
  const renderSubMenu = ({ label, childs, url, index, isFrontendRoute }) => {
    if (url && isFrontendRoute) {
      return (0,emotion_react_browser_esm.jsx)(components/* MainNav.Item */.$t.Item, { key: label, role: "presentation" },
      (0,emotion_react_browser_esm.jsx)(react_router_dom/* Link */.rU, { role: "button", to: url },
      label));


    }
    if (url) {
      return (0,emotion_react_browser_esm.jsx)(components/* MainNav.Item */.$t.Item, { key: label },
      (0,emotion_react_browser_esm.jsx)("a", { href: url }, label));

    }
    return (0,emotion_react_browser_esm.jsx)(Menu_SubMenu, { key: index, title: label, icon: showMenu === 'inline' ? (0,emotion_react_browser_esm.jsx)(react.Fragment, null) : (0,emotion_react_browser_esm.jsx)(Icons/* default.TriangleDown */.Z.TriangleDown, null) },
    childs == null ? void 0 : childs.map((child, index1) => {
      if (typeof child === 'string' && child === '-') {
        return (0,emotion_react_browser_esm.jsx)(components/* MainNav.Divider */.$t.Divider, { key: `$${index1}` });
      }
      if (typeof child !== 'string') {
        return (0,emotion_react_browser_esm.jsx)(components/* MainNav.Item */.$t.Item, { key: `${child.label}` },
        child.isFrontendRoute ? (0,emotion_react_browser_esm.jsx)(react_router_dom/* Link */.rU, { to: child.url || '' }, child.label) : (0,emotion_react_browser_esm.jsx)("a", { href: child.url }, child.label));

      }
      return null;
    }));

  };
  return (0,emotion_react_browser_esm.jsx)(StyledHeader, { className: "top", id: "main-menu", role: "navigation" },
  (0,emotion_react_browser_esm.jsx)(emotion_react_browser_esm.Global, { styles: emotion_react_browser_esm.css`
          .ant-menu-submenu.ant-menu-submenu-popup.ant-menu.ant-menu-light.ant-menu-submenu-placement-bottomLeft {
            border-radius: 0px;
          }
          .ant-menu-submenu.ant-menu-submenu-popup.ant-menu.ant-menu-light {
            border-radius: 0px;
          }
        ` }),
  (0,emotion_react_browser_esm.jsx)(row/* default */.Z, null,
  (0,emotion_react_browser_esm.jsx)(col/* default */.Z, { md: 16, xs: 24 },
  (0,emotion_react_browser_esm.jsx)(Tooltip/* Tooltip */.u, { id: "brand-tooltip", placement: "bottomLeft", title: brand.tooltip, arrowPointAtCenter: true },
  (0,emotion_react_browser_esm.jsx)("a", { className: "navbar-brand", href: brand.path },
  (0,emotion_react_browser_esm.jsx)("img", { width: brand.width, src: brand.icon, alt: brand.alt }))),


  brand.text && (0,emotion_react_browser_esm.jsx)("div", { className: "navbar-brand-text" },
  (0,emotion_react_browser_esm.jsx)("span", null, brand.text)),

  (0,emotion_react_browser_esm.jsx)(components/* MainNav */.$t, { mode: showMenu, className: "main-nav" },
  menu.map((item) => {var _item$childs;
    const props = {
      ...item,
      isFrontendRoute: isFrontendRoute(item.url),
      childs: (_item$childs = item.childs) == null ? void 0 : _item$childs.map((c) => {
        if (typeof c === 'string') {
          return c;
        }
        return {
          ...c,
          isFrontendRoute: isFrontendRoute(c.url) };

      }) };

    return renderSubMenu(props);
  }))),


  (0,emotion_react_browser_esm.jsx)(col/* default */.Z, { md: 8, xs: 24 },
  (0,emotion_react_browser_esm.jsx)(MenuRight, { align: screens.md ? 'flex-end' : 'flex-start', settings: settings, navbarRight: navbarRight, isFrontendRoute: isFrontendRoute }))));



}
// transform the menu data to reorganize components
function MenuWrapper({ data, ...rest }) {
  const newMenuData = {
    ...data };

  // Menu items that should go into settings dropdown
  const settingsMenus = {
    Security: true,
    Manage: true };

  // Cycle through menu.menu to build out cleanedMenu and settings
  const cleanedMenu = [];
  const settings = [];
  newMenuData.menu.forEach((item) => {
    if (!item) {
      return;
    }
    const children = [];
    const newItem = {
      ...item };

    // Filter childs
    if (item.childs) {
      item.childs.forEach((child) => {
        if (typeof child === 'string') {
          children.push(child);
        } else
        if (child.label) {
          children.push(child);
        }
      });
      newItem.childs = children;
    }
    if (!settingsMenus.hasOwnProperty(item.name)) {
      cleanedMenu.push(newItem);
    } else
    {
      settings.push(newItem);
    }
  });
  newMenuData.menu = cleanedMenu;
  newMenuData.settings = settings;
  return (0,emotion_react_browser_esm.jsx)(Menu, extends_default()({ data: newMenuData }, rest));
}
// EXTERNAL MODULE: ./src/preamble.ts + 3 modules
var preamble = __webpack_require__(26009);
;// CONCATENATED MODULE: ./src/views/menu.tsx
var _container$getAttribu; /**
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
// Menu App. Used in views that do not already include the Menu component in the layout.
// eg, backend rendered views







const container = document.getElementById('app');
const bootstrapJson = (_container$getAttribu = container == null ? void 0 : container.getAttribute('data-bootstrap')) != null ? _container$getAttribu : '{}';
const bootstrap = JSON.parse(bootstrapJson);
const menu = { ...bootstrap.common.menu_data };
const emotionCache = (0,emotion_cache_browser_esm/* default */.Z)({
  key: 'menu' });

const app =
// @ts-ignore: emotion types defs are incompatible between core and cache
(0,emotion_react_browser_esm.jsx)(emotion_element_99289b21_browser_esm.C, { value: emotionCache },
(0,emotion_react_browser_esm.jsx)(emotion_element_99289b21_browser_esm.a, { theme: preamble/* theme */.r },
(0,emotion_react_browser_esm.jsx)(MenuWrapper, { data: menu })));


react_dom.render(app, document.getElementById('app-menu'));

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
/******/ 			// return url for filenames based on template
/******/ 			return "" + {"57":"028e5eaba60ee1f0c2c2","112":"9fcc2ab7e3decb77e68a","158":"067dd46754cb5755621a","177":"daff443a6a259740b9ea","183":"7180931293c0eb958c52","215":"0d19cdfee35ccc92f701","310":"135def3410b28bde86ff","312":"6456f925ef0e593cf2fd","336":"f9b3561fd92836a920cd","363":"a6530749fb56462bc957","597":"fef57e00156e5f59ea45","600":"ef265991d9c8beb1bb22","826":"f82ff59e0436c52a8bc1","992":"d42abb01dcb03b5ea79e","999":"85dd3a220ce297acafe9","1075":"94d9b1829e929831b151","1174":"8f244f47294e02e761a1","1185":"feb0657fd1cd8eb8cccb","1256":"0a7adfa99f06991c526c","1263":"0ddad88e1fc0114d1dc9","1293":"f93daf14868c44bd843a","1351":"ab5b2b54ecd29ca6e21c","1398":"6bdcdfad4fffbd4b6bd8","1493":"af7d972a6a46bacab94d","1568":"6d86dc72b95d32371252","1605":"883e261ae3ecfb0f8755","1899":"555c4cc5e9264d2e09f9","2079":"653b159f3867c9459b01","2105":"8059570cc5823d65fd2c","2264":"cd1eeac9f037880b0212","2267":"18b27b1bb2bd5dd7aa61","2403":"be5f79b6b4624364c5f3","2439":"7f23ec71a8f74c2b02ec","2646":"89bf808500d87084d6b0","2698":"c093d4f54e9cb79148ef","2713":"a57d21e7160b0f553f5c","2797":"617b8ee1d3d6339e5613","2983":"feae373a263e065ff446","3141":"d531ed7032b42d64dca2","3240":"73ffac6083ffe185c09f","3265":"b67a755d414be1b54d86","3325":"56aebae23380bbe9f3cc","3544":"898720f9f22675673911","3558":"714cba25b1e6aa5cd799","3567":"5e62708f5889c428e82c","3606":"b0e363c89061c92d0c53","3749":"afee7363adc500297825","3871":"6a529c979bb793ccbdae","3955":"9160a76cf3dea289b79e","3985":"1899b405b3888e068c7e","4139":"2c3665b54e7fed053b35","4266":"a68f073d5c25c1344d94","4273":"e6b35ed596fb2404f26c","4458":"8b6a6fd12fa942d44b7b","4474":"eb2f03c6083e66304c68","4625":"0b2c629dc9577bcbc473","4662":"40af31a304028068f8a3","4667":"1a5286b06adb14b671fd","4732":"78da6bf13da526416f92","4757":"278b3b950a627ab829ab","4758":"f13eabe9cbc4aaa2cfd7","4794":"008094f826594e07d5af","4797":"594130c61e265833c43b","4810":"47366d32d3b5c3e2f319","4817":"84f3798572f423cea73a","4851":"067006aa81cb69192dea","5201":"648d8f209c1894a50b3f","5224":"6d6fd64a53aaa33eea22","5226":"bb22669bd991d6a73375","5249":"61d3f9c5cc5ca3f80b04","5281":"046ca8aa0e202a5a4c00","5330":"be15bc34dd2926179f89","5350":"14835ad324f5a759f725","5359":"4e0cf032edde0ad08c98","5367":"22df5a0f35a4554839f1","5507":"d306225272739fb01e43","5580":"df0ecccb1e5c3185e516","5592":"e695c51628cbff6bf0fd","5641":"b743bdeff76333f134ae","5707":"c9627a388872a8d2a957","5771":"cbf62bbc3f6f8025fdfc","5777":"f3e29f5dbb36ae1cc98e","5816":"a4c2b603201c7f9060d7","5832":"e8a940e0c94fa25a8765","5838":"4193414073d37ecb6064","5962":"f163fa69cbd0345e0a5a","5972":"09c10d24cb92e1f67b13","5998":"2cc665e33c971367a6ce","6126":"c44c96942fb85a19ac1e","6150":"548accd51f5ec4ecc14b","6167":"5e75f0b0cd02b96355cf","6207":"22ede093c81ef82c5bac","6254":"a29ae9eeb81891bddab6","6303":"1a63ee0f599081264d8c","6371":"c7bd2b4dc87e1b940ce5","6420":"eb39ad899c9c5c179291","6447":"0f127715dab6bbf6fefd","6507":"3533ebbe2e94fa7a675a","6668":"a26e3bb5b59e7e16f550","6682":"19283d8df0b4e63f16db","6758":"f7d7e358ea3e78bbba35","6819":"183272dd2f7c81c4c9c8","6883":"6780ee31faa82e4825c2","6981":"7a8d6c643cb4f5df8198","7183":"15e2f1b86b261dda7daf","7249":"548a8e5717947f7021bd","7405":"9c51a4dd78cc59db1bf7","7460":"e0a8070ed7c2cbd41080","7584":"09582b48010b05b12a59","7610":"320e8196129209a5d403","7654":"fb32e1480e8a5e656f96","7716":"0d08811bf13191ea008a","7760":"e52f02c420204be2409d","7803":"41ad98224efd12874173","7832":"f3d5e3cbaaf9c0591048","7850":"8b44f0b0e02baa79ae77","7922":"886bbfbb9c5b6a949f30","8312":"c6aae8671318f46a616b","8349":"0675c83c091a08d07837","8398":"3f920942fdd2e7b6c103","8425":"ca4e7824ea1f39c02835","8463":"1f78779088dc48ccacac","8682":"6cabc2fe8f0626630fcb","8695":"448d248fb9d5f4999c24","8970":"22b785d53413d0d6b2e1","9013":"6ffbfae6a84d886acb37","9052":"18c72b820a16b97d3437","9109":"befdefaa4a6a29f18775","9305":"3dbe560a6cb4a6bdb9ed","9325":"d96803c30d0802740a48","9393":"598a5cabf7906fbbc188","9510":"d881743c10a5f4711298","9558":"78f4fa40b40a02a002d1","9767":"d4ac455af931bb06a7dc","9811":"61283ed5ec96a21e421e"}[chunkId] + ".chunk.js";
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/get mini-css chunk filename */
/******/ 	(() => {
/******/ 		// This function allow to reference all chunks
/******/ 		__webpack_require__.miniCssF = (chunkId) => {
/******/ 			// return url for filenames based on template
/******/ 			return undefined;
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
/******/ 	/* webpack/runtime/jsonp chunk loading */
/******/ 	(() => {
/******/ 		// no baseURI
/******/ 		
/******/ 		// object to store loaded and loading chunks
/******/ 		// undefined = chunk not loaded, null = chunk preloaded/prefetched
/******/ 		// [resolve, reject, Promise] = chunk loading, 0 = chunk loaded
/******/ 		var installedChunks = {
/******/ 			8860: 0
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
/******/ 						if(true) { // all chunks have JS
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
/******/ 	// startup
/******/ 	// Load entry module and return exports
/******/ 	// This entry module depends on other loaded chunks and execution need to be delayed
/******/ 	__webpack_require__.O(undefined, [1216,7550,4772,5110,3727,3401], () => (__webpack_require__(26009)))
/******/ 	var __webpack_exports__ = __webpack_require__.O(undefined, [1216,7550,4772,5110,3727,3401], () => (__webpack_require__(95639)))
/******/ 	__webpack_exports__ = __webpack_require__.O(__webpack_exports__);
/******/ 	
/******/ })()
;
"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[17809],{69810:(e,t,r)=>{r.d(t,{lC:()=>o,CP:()=>s,Lm:()=>a,NC:()=>l,jP:()=>c});var i=r(63864),n=r(41682);const o=async e=>{(0,i.I)(e.config.version,2021,2,4)?await e.callWS({type:"supervisor/api",endpoint:"/supervisor/reload",method:"post"}):await e.callApi("POST","hassio/supervisor/reload")},s=async e=>(0,i.I)(e.config.version,2021,2,4)?e.callWS({type:"supervisor/api",endpoint:"/supervisor/info",method:"get"}):(0,n.rY)(await e.callApi("GET","hassio/supervisor/info")),a=async e=>(0,i.I)(e.config.version,2021,2,4)?e.callWS({type:"supervisor/api",endpoint:"/info",method:"get"}):(0,n.rY)(await e.callApi("GET","hassio/info")),l=async(e,t)=>e.callApi("GET",`hassio/${t.includes("_")?`addons/${t}`:t}/logs`),c=async(e,t)=>{(0,i.I)(e.config.version,2021,2,4)?await e.callWS({type:"supervisor/api",endpoint:"/supervisor/options",method:"post",data:t}):await e.callApi("POST","hassio/supervisor/options",t)}},17809:(e,t,r)=>{r.r(t);var i=r(37500),n=r(33310),o=r(7323);function s(){s=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(i){t.forEach((function(t){var n=t.placement;if(t.kind===i&&("static"===n||"prototype"===n)){var o="static"===n?e:r;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var i=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===i?void 0:i.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],i=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!c(e))return r.push(e);var t=this.decorateElement(e,n);r.push(t.element),r.push.apply(r,t.extras),i.push.apply(i,t.finishers)}),this),!t)return{elements:r,finishers:i};var o=this.decorateConstructor(r,t);return i.push.apply(i,o.finishers),o.finishers=i,o},addElementPlacement:function(e,t,r){var i=t[e.placement];if(!r&&-1!==i.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");i.push(e.key)},decorateElement:function(e,t){for(var r=[],i=[],n=e.decorators,o=n.length-1;o>=0;o--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,n[o])(a)||a);e=l.element,this.addElementPlacement(e,t),l.finisher&&i.push(l.finisher);var c=l.extras;if(c){for(var f=0;f<c.length;f++)this.addElementPlacement(c[f],t);r.push.apply(r,c)}}return{element:e,finishers:i,extras:r}},decorateConstructor:function(e,t){for(var r=[],i=t.length-1;i>=0;i--){var n=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[i])(n)||n);if(void 0!==o.finisher&&r.push(o.finisher),void 0!==o.elements){e=o.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return u(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?u(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=p(e.key),i=String(e.placement);if("static"!==i&&"prototype"!==i&&"own"!==i)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+i+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:r,placement:i,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:d(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=d(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var i=(0,t[r])(e);if(void 0!==i){if("function"!=typeof i)throw new TypeError("Finishers must return a constructor.");e=i}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}function a(e){var t,r=p(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var i={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(i.decorators=e.decorators),"field"===e.kind&&(i.initializer=e.value),i}function l(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function c(e){return e.decorators&&e.decorators.length}function f(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function d(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function p(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var i=r.call(e,t||"default");if("object"!=typeof i)return i;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function u(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,i=new Array(t);r<t;r++)i[r]=e[r];return i}!function(e,t,r,i){var n=s();if(i)for(var o=0;o<i.length;o++)n=i[o](n);var d=t((function(e){n.initializeInstanceElements(e,p.elements)}),r),p=n.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},i=0;i<e.length;i++){var n,o=e[i];if("method"===o.kind&&(n=t.find(r)))if(f(o.descriptor)||f(n.descriptor)){if(c(o)||c(n))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");n.descriptor=o.descriptor}else{if(c(o)){if(c(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");n.decorators=o.decorators}l(o,n)}else t.push(o)}return t}(d.d.map(a)),e);n.initializeClassElements(d.F,p.elements),n.runClassFinishers(d.F,p.finishers)}([(0,n.Mo)("ha-logo-svg")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"method",key:"render",value:function(){return i.YP`
      <svg xmlns="http://www.w3.org/2000/svg" version="1.1" viewBox="48.43 66.19 120.58 192.4"><defs><filter id="a" color-interpolation-filters="sRGB"><feGaussianBlur stdDeviation="0.51 0.5" result="blur"/></filter><filter id="b" color-interpolation-filters="sRGB"><feGaussianBlur stdDeviation="0.51 0.5" result="blur"/></filter><filter id="c" color-interpolation-filters="sRGB"><feGaussianBlur stdDeviation="0.51 0.5" result="blur"/></filter><filter id="d" color-interpolation-filters="sRGB"><feGaussianBlur stdDeviation="0.51 0.5" result="blur"/></filter><filter id="e" color-interpolation-filters="sRGB"><feGaussianBlur stdDeviation="0.51 0.5" result="blur"/></filter><filter id="f" color-interpolation-filters="sRGB"><feGaussianBlur stdDeviation="0.51 0.5" result="blur"/></filter></defs><g fill-rule="evenodd" stroke="#fff" stroke-width=".511" stroke-miterlimit="4" stroke-dasharray="0 5.616" stroke-dashoffset="7.56" stroke-opacity="1"><path d="M39.429 22.429C21.226 22.429 6.57 40.774 6.57 63.56v183.153h65.715V63.56c0-22.787-14.654-41.132-32.857-41.132z" transform="translate(46.109 57.663) scale(.39179)" opacity="1" fill="#d04400" fill-opacity=".929" filter="url(#a)"/><path d="M39.429 14.025C21.226 14.025 6.57 32.37 6.57 55.157v98.868h61.354c1.479 0 2.933.089 4.361.246V55.157c0-22.787-14.654-41.132-32.857-41.132z" transform="translate(92.823 93.978) scale(.39179)" opacity="1" fill="#f69562" fill-opacity="1" filter="url(#b)"/><path d="M39.429 8C21.226 8 6.57 26.346 6.57 49.133V88h65.715V49.133C72.286 26.346 57.632 8 39.43 8z" transform="translate(140.432 119.846) scale(.39179)" opacity="1" fill="#ffbd77" fill-opacity="1" filter="url(#c)"/><path d="M39.429 22.429C21.226 22.429 6.57 40.774 6.57 63.56v183.153h65.715V63.56c0-22.787-14.654-41.132-32.857-41.132z" transform="matrix(.39179 0 0 -.39179 46.109 267.13)" opacity="1" fill="#d04400" fill-opacity=".929" filter="url(#d)"/><path d="M39.429 14.025C21.226 14.025 6.57 32.37 6.57 55.157v98.868h61.354c1.479 0 2.933.089 4.361.246V55.157c0-22.787-14.654-41.132-32.857-41.132z" transform="matrix(.39179 0 0 -.39179 92.823 230.716)" opacity="1" fill="#f69562" fill-opacity="1" filter="url(#e)"/><path d="M39.429 8C21.226 8 6.57 26.346 6.57 49.133V88h65.715V49.133C72.286 26.346 57.632 8 39.43 8z" transform="matrix(.39179 0 0 -.39179 140.432 204.472)" opacity="1" fill="#ffbd77" fill-opacity="1" filter="url(#f)"/></g></svg>`}},{kind:"get",static:!0,key:"styles",value:function(){return i.iv`
      :host {
        display: var(--ha-icon-display, inline-flex);
        align-items: center;
        justify-content: center;
        position: relative;
        vertical-align: middle;
        fill: currentcolor;
        width: var(--mdc-icon-size, 24px);
        height: var(--mdc-icon-size, 24px);
      }
      svg {
        width: 100%;
        height: 100%;
        pointer-events: none;
        display: block;
      }
    `}}]}}),i.oi);var h=r(35460),m=r(69810),v=(r(60010),r(11654)),y=r(27322);function g(){g=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(i){t.forEach((function(t){var n=t.placement;if(t.kind===i&&("static"===n||"prototype"===n)){var o="static"===n?e:r;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var i=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===i?void 0:i.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],i=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!k(e))return r.push(e);var t=this.decorateElement(e,n);r.push(t.element),r.push.apply(r,t.extras),i.push.apply(i,t.finishers)}),this),!t)return{elements:r,finishers:i};var o=this.decorateConstructor(r,t);return i.push.apply(i,o.finishers),o.finishers=i,o},addElementPlacement:function(e,t,r){var i=t[e.placement];if(!r&&-1!==i.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");i.push(e.key)},decorateElement:function(e,t){for(var r=[],i=[],n=e.decorators,o=n.length-1;o>=0;o--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,n[o])(a)||a);e=l.element,this.addElementPlacement(e,t),l.finisher&&i.push(l.finisher);var c=l.extras;if(c){for(var f=0;f<c.length;f++)this.addElementPlacement(c[f],t);r.push.apply(r,c)}}return{element:e,finishers:i,extras:r}},decorateConstructor:function(e,t){for(var r=[],i=t.length-1;i>=0;i--){var n=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[i])(n)||n);if(void 0!==o.finisher&&r.push(o.finisher),void 0!==o.elements){e=o.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return A(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?A(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=C(e.key),i=String(e.placement);if("static"!==i&&"prototype"!==i&&"own"!==i)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+i+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:r,placement:i,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:P(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=P(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var i=(0,t[r])(e);if(void 0!==i){if("function"!=typeof i)throw new TypeError("Finishers must return a constructor.");e=i}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}function b(e){var t,r=C(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var i={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(i.decorators=e.decorators),"field"===e.kind&&(i.initializer=e.value),i}function w(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function k(e){return e.decorators&&e.decorators.length}function E(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function P(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function C(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var i=r.call(e,t||"default");if("object"!=typeof i)return i;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function A(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,i=new Array(t);r<t;r++)i[r]=e[r];return i}function S(e,t,r){return S="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,r){var i=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=D(e)););return e}(e,t);if(i){var n=Object.getOwnPropertyDescriptor(i,t);return n.get?n.get.call(r):n.value}},S(e,t,r||e)}function D(e){return D=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)},D(e)}let z=function(e,t,r,i){var n=g();if(i)for(var o=0;o<i.length;o++)n=i[o](n);var s=t((function(e){n.initializeInstanceElements(e,a.elements)}),r),a=n.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},i=0;i<e.length;i++){var n,o=e[i];if("method"===o.kind&&(n=t.find(r)))if(E(o.descriptor)||E(n.descriptor)){if(k(o)||k(n))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");n.descriptor=o.descriptor}else{if(k(o)){if(k(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");n.decorators=o.decorators}w(o,n)}else t.push(o)}return t}(s.d.map(b)),e);return n.initializeClassElements(s.F,a.elements),n.runClassFinishers(s.F,a.finishers)}(null,(function(e,t){class r extends t{constructor(...t){super(...t),e(this)}}return{F:r,d:[{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.Cb)({type:Boolean})],key:"narrow",value:void 0},{kind:"field",decorators:[(0,n.Cb)({type:Boolean})],key:"isWide",value:void 0},{kind:"field",decorators:[(0,n.Cb)({type:Boolean})],key:"showAdvanced",value:void 0},{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"route",value:void 0},{kind:"field",decorators:[(0,n.SB)()],key:"_osInfo",value:void 0},{kind:"field",decorators:[(0,n.SB)()],key:"_hassioInfo",value:void 0},{kind:"method",key:"render",value:function(){var e;const t=this.hass,r=window.CUSTOM_UI_LIST||[];return i.dy`
      <hass-subpage
        .hass=${this.hass}
        .narrow=${this.narrow}
        back-path="/config"
        .header=${this.hass.localize("ui.panel.config.info.caption")}
      >
        <div class="about">
          <a href="https://ai-speaker.com" target="_blank" rel="noreferrer">
            <ha-logo-svg title="AI-Speaker"> </ha-logo-svg>
          </a>
          <br />
          <h3>Home Assistant Core ${t.connection.haVersion}</h3>
          ${this._hassioInfo?i.dy`
                <h3>
                  Home Assistant Supervisor ${this._hassioInfo.supervisor}
                </h3>
              `:""}
          ${null!==(e=this._osInfo)&&void 0!==e&&e.version?i.dy`<h3>Home Assistant OS ${this._osInfo.version}</h3>`:""}
          <p>
            ${this.hass.localize("ui.panel.config.info.path_configuration","path",t.config.config_dir)}
          </p>
          <p class="develop">
            <a
              href=${(0,y.R)(this.hass,"/developers/credits/")}
              target="_blank"
              rel="noreferrer"
            >
              ${this.hass.localize("ui.panel.config.info.developed_by")}
            </a>
          </p>
          <p>
            ${this.hass.localize("ui.panel.config.info.license")}<br />
            ${this.hass.localize("ui.panel.config.info.source")}
            <a
              href="https://github.com/sviete/AIS-home-assistant"
              target="_blank"
              rel="noreferrer"
              >${this.hass.localize("ui.panel.config.info.server")}</a
            >
            &mdash;
            <a
              href="https://github.com/sviete/AIS-home-assistant-polymer"
              target="_blank"
              rel="noreferrer"
              >${this.hass.localize("ui.panel.config.info.frontend")}</a
            >
          </p>
          <p>
            ${this.hass.localize("ui.panel.config.info.built_using")}
            <a href="https://www.python.org" target="_blank" rel="noreferrer"
              >Python 3</a
            >,
            <a href="https://lit.dev" target="_blank" rel="noreferrer">Lit</a>,
            ${this.hass.localize("ui.panel.config.info.icons_by")}
            <a
              href="https://fonts.google.com/icons?selected=Material+Icons"
              target="_blank"
              rel="noreferrer"
              >Google</a
            >
            ${this.hass.localize("ui.common.and")}
            <a
              href="https://materialdesignicons.com/"
              target="_blank"
              rel="noreferrer"
              >Material Design Icons</a
            >.
          </p>
          <p>
            ${this.hass.localize("ui.panel.config.info.frontend_version","version","20220601.0","type","latest")}
            ${r.length>0?i.dy`
                  <div>
                    ${this.hass.localize("ui.panel.config.info.custom_uis")}
                    ${r.map((e=>i.dy`
                        <div>
                          <a href=${e.url} target="_blank"> ${e.name}</a>:
                          ${e.version}
                        </div>
                      `))}
                  </div>
                `:""}
          </p>
        </div>
      </hass-subpage>
    `}},{kind:"method",key:"firstUpdated",value:function(e){S(D(r.prototype),"firstUpdated",this).call(this,e);const t=(window.CUSTOM_UI_LIST||[]).length;setTimeout((()=>{(window.CUSTOM_UI_LIST||[]).length!==t.length&&this.requestUpdate()}),1e3),(0,o.p)(this.hass,"hassio")&&this._loadSupervisorInfo()}},{kind:"method",key:"_loadSupervisorInfo",value:async function(){const[e,t]=await Promise.all([(0,h.AP)(this.hass),(0,m.Lm)(this.hass)]);this._hassioInfo=t,this._osInfo=e}},{kind:"get",static:!0,key:"styles",value:function(){return[v.Qx,i.iv`
        :host {
          -ms-user-select: initial;
          -webkit-user-select: initial;
          -moz-user-select: initial;
        }

        .about {
          text-align: center;
          line-height: 2em;
        }

        .version {
          @apply --paper-font-headline;
        }

        .develop {
          @apply --paper-font-subhead;
        }

        .about a {
          color: var(--primary-color);
        }
        ha-logo-svg {
          padding: 12px;
          height: 180px;
          width: 180px;
        }

        h4 {
          font-weight: 400;
        }
      `]}}]}}),i.oi);customElements.define("ha-config-info",z)},27322:(e,t,r)=>{r.d(t,{R:()=>i});const i=(e,t)=>`https://${e.config.version.includes("b")?"rc":e.config.version.includes("dev")?"next":"www"}.home-assistant.io${t}`}}]);
//# sourceMappingURL=2e0e9c76.js.map
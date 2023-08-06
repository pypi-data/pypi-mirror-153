"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[83455],{46583:(e,t,i)=>{var r=i(37500),n=i(33310),o=i(8636),a=i(47181),s=i(96151);i(52039);function l(){l=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(i){t.forEach((function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach((function(r){t.forEach((function(t){var n=t.placement;if(t.kind===r&&("static"===n||"prototype"===n)){var o="static"===n?e:i;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var r=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],r=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!h(e))return i.push(e);var t=this.decorateElement(e,n);i.push(t.element),i.push.apply(i,t.extras),r.push.apply(r,t.finishers)}),this),!t)return{elements:i,finishers:r};var o=this.decorateConstructor(i,t);return r.push.apply(r,o.finishers),o.finishers=r,o},addElementPlacement:function(e,t,i){var r=t[e.placement];if(!i&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var i=[],r=[],n=e.decorators,o=n.length-1;o>=0;o--){var a=t[e.placement];a.splice(a.indexOf(e.key),1);var s=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,n[o])(s)||s);e=l.element,this.addElementPlacement(e,t),l.finisher&&r.push(l.finisher);var d=l.extras;if(d){for(var c=0;c<d.length;c++)this.addElementPlacement(d[c],t);i.push.apply(i,d)}}return{element:e,finishers:r,extras:i}},decorateConstructor:function(e,t){for(var i=[],r=t.length-1;r>=0;r--){var n=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[r])(n)||n);if(void 0!==o.finisher&&i.push(o.finisher),void 0!==o.elements){e=o.elements;for(var a=0;a<e.length-1;a++)for(var s=a+1;s<e.length;s++)if(e[a].key===e[s].key&&e[a].placement===e[s].placement)throw new TypeError("Duplicated element ("+e[a].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return m(e,t);var i=Object.prototype.toString.call(e).slice(8,-1);return"Object"===i&&e.constructor&&(i=e.constructor.name),"Map"===i||"Set"===i?Array.from(e):"Arguments"===i||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(i)?m(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=f(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:i,placement:r,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:p(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=p(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var r=(0,t[i])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}function d(e){var t,i=f(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function c(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function h(e){return e.decorators&&e.decorators.length}function u(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function p(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function f(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var r=i.call(e,t||"default");if("object"!=typeof r)return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function m(e,t){(null==t||t>e.length)&&(t=e.length);for(var i=0,r=new Array(t);i<t;i++)r[i]=e[i];return r}!function(e,t,i,r){var n=l();if(r)for(var o=0;o<r.length;o++)n=r[o](n);var a=t((function(e){n.initializeInstanceElements(e,s.elements)}),i),s=n.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},r=0;r<e.length;r++){var n,o=e[r];if("method"===o.kind&&(n=t.find(i)))if(u(o.descriptor)||u(n.descriptor)){if(h(o)||h(n))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");n.descriptor=o.descriptor}else{if(h(o)){if(h(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");n.decorators=o.decorators}c(o,n)}else t.push(o)}return t}(a.d.map(d)),e);n.initializeClassElements(a.F,s.elements),n.runClassFinishers(a.F,s.finishers)}([(0,n.Mo)("ha-expansion-panel")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.Cb)({type:Boolean,reflect:!0})],key:"expanded",value:()=>!1},{kind:"field",decorators:[(0,n.Cb)({type:Boolean,reflect:!0})],key:"outlined",value:()=>!1},{kind:"field",decorators:[(0,n.Cb)()],key:"header",value:void 0},{kind:"field",decorators:[(0,n.Cb)()],key:"secondary",value:void 0},{kind:"field",decorators:[(0,n.SB)()],key:"_showContent",value(){return this.expanded}},{kind:"field",decorators:[(0,n.IO)(".container")],key:"_container",value:void 0},{kind:"method",key:"render",value:function(){return r.dy`
      <div
        id="summary"
        @click=${this._toggleContainer}
        @keydown=${this._toggleContainer}
        role="button"
        tabindex="0"
        aria-expanded=${this.expanded}
        aria-controls="sect1"
      >
        <slot class="header" name="header">
          ${this.header}
          <slot class="secondary" name="secondary">${this.secondary}</slot>
        </slot>
        <ha-svg-icon
          .path=${"M7.41,8.58L12,13.17L16.59,8.58L18,10L12,16L6,10L7.41,8.58Z"}
          class="summary-icon ${(0,o.$)({expanded:this.expanded})}"
        ></ha-svg-icon>
      </div>
      <div
        class="container ${(0,o.$)({expanded:this.expanded})}"
        @transitionend=${this._handleTransitionEnd}
        role="region"
        aria-labelledby="summary"
        aria-hidden=${!this.expanded}
        tabindex="-1"
      >
        ${this._showContent?r.dy`<slot></slot>`:""}
      </div>
    `}},{kind:"method",key:"willUpdate",value:function(e){e.has("expanded")&&this.expanded&&(this._showContent=this.expanded)}},{kind:"method",key:"_handleTransitionEnd",value:function(){this._container.style.removeProperty("height"),this._showContent=this.expanded}},{kind:"method",key:"_toggleContainer",value:async function(e){if("keydown"===e.type&&"Enter"!==e.key&&" "!==e.key)return;e.preventDefault();const t=!this.expanded;(0,a.B)(this,"expanded-will-change",{expanded:t}),t&&(this._showContent=!0,await(0,s.y)());const i=this._container.scrollHeight;this._container.style.height=`${i}px`,t||setTimeout((()=>{this._container.style.height="0px"}),0),this.expanded=t,(0,a.B)(this,"expanded-changed",{expanded:this.expanded})}},{kind:"get",static:!0,key:"styles",value:function(){return r.iv`
      :host {
        display: block;
      }

      :host([outlined]) {
        box-shadow: none;
        border-width: 1px;
        border-style: solid;
        border-color: var(
          --ha-card-border-color,
          var(--divider-color, #e0e0e0)
        );
        border-radius: var(--ha-card-border-radius, 4px);
      }

      #summary {
        display: flex;
        padding: var(--expansion-panel-summary-padding, 0 8px);
        min-height: 48px;
        align-items: center;
        cursor: pointer;
        overflow: hidden;
        font-weight: 500;
        outline: none;
      }

      #summary:focus {
        background: var(--input-fill-color);
      }

      .summary-icon {
        transition: transform 150ms cubic-bezier(0.4, 0, 0.2, 1);
        margin-left: auto;
        margin-inline-start: auto;
        margin-inline-end: initial;
        direction: var(--direction);
      }

      .summary-icon.expanded {
        transform: rotate(180deg);
      }

      .container {
        padding: var(--expansion-panel-content-padding, 0 8px);
        overflow: hidden;
        transition: height 300ms cubic-bezier(0.4, 0, 0.2, 1);
        height: 0px;
      }

      .container.expanded {
        height: auto;
      }

      .header {
        display: block;
      }

      .secondary {
        display: block;
        color: var(--secondary-text-color);
        font-size: 12px;
      }
    `}}]}}),r.oi)},43709:(e,t,i)=>{var r=i(11581),n=i(4301),o=i(37500),a=i(33310),s=i(62359);function l(){l=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(i){t.forEach((function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach((function(r){t.forEach((function(t){var n=t.placement;if(t.kind===r&&("static"===n||"prototype"===n)){var o="static"===n?e:i;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var r=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],r=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!h(e))return i.push(e);var t=this.decorateElement(e,n);i.push(t.element),i.push.apply(i,t.extras),r.push.apply(r,t.finishers)}),this),!t)return{elements:i,finishers:r};var o=this.decorateConstructor(i,t);return r.push.apply(r,o.finishers),o.finishers=r,o},addElementPlacement:function(e,t,i){var r=t[e.placement];if(!i&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var i=[],r=[],n=e.decorators,o=n.length-1;o>=0;o--){var a=t[e.placement];a.splice(a.indexOf(e.key),1);var s=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,n[o])(s)||s);e=l.element,this.addElementPlacement(e,t),l.finisher&&r.push(l.finisher);var d=l.extras;if(d){for(var c=0;c<d.length;c++)this.addElementPlacement(d[c],t);i.push.apply(i,d)}}return{element:e,finishers:r,extras:i}},decorateConstructor:function(e,t){for(var i=[],r=t.length-1;r>=0;r--){var n=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[r])(n)||n);if(void 0!==o.finisher&&i.push(o.finisher),void 0!==o.elements){e=o.elements;for(var a=0;a<e.length-1;a++)for(var s=a+1;s<e.length;s++)if(e[a].key===e[s].key&&e[a].placement===e[s].placement)throw new TypeError("Duplicated element ("+e[a].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return m(e,t);var i=Object.prototype.toString.call(e).slice(8,-1);return"Object"===i&&e.constructor&&(i=e.constructor.name),"Map"===i||"Set"===i?Array.from(e):"Arguments"===i||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(i)?m(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=f(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:i,placement:r,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:p(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=p(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var r=(0,t[i])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}function d(e){var t,i=f(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function c(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function h(e){return e.decorators&&e.decorators.length}function u(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function p(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function f(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var r=i.call(e,t||"default");if("object"!=typeof r)return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function m(e,t){(null==t||t>e.length)&&(t=e.length);for(var i=0,r=new Array(t);i<t;i++)r[i]=e[i];return r}function y(e,t,i){return y="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,i){var r=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=v(e)););return e}(e,t);if(r){var n=Object.getOwnPropertyDescriptor(r,t);return n.get?n.get.call(i):n.value}},y(e,t,i||e)}function v(e){return v=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)},v(e)}!function(e,t,i,r){var n=l();if(r)for(var o=0;o<r.length;o++)n=r[o](n);var a=t((function(e){n.initializeInstanceElements(e,s.elements)}),i),s=n.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},r=0;r<e.length;r++){var n,o=e[r];if("method"===o.kind&&(n=t.find(i)))if(u(o.descriptor)||u(n.descriptor)){if(h(o)||h(n))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");n.descriptor=o.descriptor}else{if(h(o)){if(h(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");n.decorators=o.decorators}c(o,n)}else t.push(o)}return t}(a.d.map(d)),e);n.initializeClassElements(a.F,s.elements),n.runClassFinishers(a.F,s.finishers)}([(0,a.Mo)("ha-switch")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,a.Cb)({type:Boolean})],key:"haptic",value:()=>!1},{kind:"method",key:"firstUpdated",value:function(){y(v(i.prototype),"firstUpdated",this).call(this),this.addEventListener("change",(()=>{this.haptic&&(0,s.j)("light")}))}},{kind:"field",static:!0,key:"styles",value:()=>[n.W,o.iv`
      :host {
        --mdc-theme-secondary: var(--switch-checked-color);
      }
      .mdc-switch.mdc-switch--checked .mdc-switch__thumb {
        background-color: var(--switch-checked-button-color);
        border-color: var(--switch-checked-button-color);
      }
      .mdc-switch.mdc-switch--checked .mdc-switch__track {
        background-color: var(--switch-checked-track-color);
        border-color: var(--switch-checked-track-color);
      }
      .mdc-switch:not(.mdc-switch--checked) .mdc-switch__thumb {
        background-color: var(--switch-unchecked-button-color);
        border-color: var(--switch-unchecked-button-color);
      }
      .mdc-switch:not(.mdc-switch--checked) .mdc-switch__track {
        background-color: var(--switch-unchecked-track-color);
        border-color: var(--switch-unchecked-track-color);
      }
    `]}]}}),r.H)},18900:(e,t,i)=>{var r=i(77426),n=i(37500),o=i(33310),a=i(47181);i(53822);function s(){s=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(i){t.forEach((function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach((function(r){t.forEach((function(t){var n=t.placement;if(t.kind===r&&("static"===n||"prototype"===n)){var o="static"===n?e:i;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var r=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],r=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!c(e))return i.push(e);var t=this.decorateElement(e,n);i.push(t.element),i.push.apply(i,t.extras),r.push.apply(r,t.finishers)}),this),!t)return{elements:i,finishers:r};var o=this.decorateConstructor(i,t);return r.push.apply(r,o.finishers),o.finishers=r,o},addElementPlacement:function(e,t,i){var r=t[e.placement];if(!i&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var i=[],r=[],n=e.decorators,o=n.length-1;o>=0;o--){var a=t[e.placement];a.splice(a.indexOf(e.key),1);var s=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,n[o])(s)||s);e=l.element,this.addElementPlacement(e,t),l.finisher&&r.push(l.finisher);var d=l.extras;if(d){for(var c=0;c<d.length;c++)this.addElementPlacement(d[c],t);i.push.apply(i,d)}}return{element:e,finishers:r,extras:i}},decorateConstructor:function(e,t){for(var i=[],r=t.length-1;r>=0;r--){var n=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[r])(n)||n);if(void 0!==o.finisher&&i.push(o.finisher),void 0!==o.elements){e=o.elements;for(var a=0;a<e.length-1;a++)for(var s=a+1;s<e.length;s++)if(e[a].key===e[s].key&&e[a].placement===e[s].placement)throw new TypeError("Duplicated element ("+e[a].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return f(e,t);var i=Object.prototype.toString.call(e).slice(8,-1);return"Object"===i&&e.constructor&&(i=e.constructor.name),"Map"===i||"Set"===i?Array.from(e):"Arguments"===i||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(i)?f(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=p(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:i,placement:r,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:u(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=u(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var r=(0,t[i])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}function l(e){var t,i=p(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function d(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function c(e){return e.decorators&&e.decorators.length}function h(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function u(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function p(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var r=i.call(e,t||"default");if("object"!=typeof r)return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function f(e,t){(null==t||t>e.length)&&(t=e.length);for(var i=0,r=new Array(t);i<t;i++)r[i]=e[i];return r}!function(e,t,i,r){var n=s();if(r)for(var o=0;o<r.length;o++)n=r[o](n);var a=t((function(e){n.initializeInstanceElements(e,u.elements)}),i),u=n.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},r=0;r<e.length;r++){var n,o=e[r];if("method"===o.kind&&(n=t.find(i)))if(h(o.descriptor)||h(n.descriptor)){if(c(o)||c(n))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");n.descriptor=o.descriptor}else{if(c(o)){if(c(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");n.decorators=o.decorators}d(o,n)}else t.push(o)}return t}(a.d.map(l)),e);n.initializeClassElements(a.F,u.elements),n.runClassFinishers(a.F,u.finishers)}([(0,o.Mo)("ha-yaml-editor")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,o.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,o.Cb)()],key:"value",value:void 0},{kind:"field",decorators:[(0,o.Cb)({attribute:!1})],key:"yamlSchema",value:()=>r.oW},{kind:"field",decorators:[(0,o.Cb)()],key:"defaultValue",value:void 0},{kind:"field",decorators:[(0,o.Cb)()],key:"isValid",value:()=>!0},{kind:"field",decorators:[(0,o.Cb)()],key:"label",value:void 0},{kind:"field",decorators:[(0,o.Cb)({type:Boolean})],key:"readOnly",value:()=>!1},{kind:"field",decorators:[(0,o.Cb)({type:Boolean})],key:"required",value:()=>!1},{kind:"field",decorators:[(0,o.SB)()],key:"_yaml",value:()=>""},{kind:"method",key:"setValue",value:function(e){try{this._yaml=e&&!(e=>{if("object"!=typeof e)return!1;for(const t in e)if(Object.prototype.hasOwnProperty.call(e,t))return!1;return!0})(e)?(0,r.$w)(e,{schema:this.yamlSchema}):""}catch(t){console.error(t,e),alert(`There was an error converting to YAML: ${t}`)}}},{kind:"method",key:"firstUpdated",value:function(){this.defaultValue&&this.setValue(this.defaultValue)}},{kind:"method",key:"render",value:function(){return void 0===this._yaml?n.dy``:n.dy`
      ${this.label?n.dy`<p>${this.label}${this.required?" *":""}</p>`:""}
      <ha-code-editor
        .hass=${this.hass}
        .value=${this._yaml}
        .readOnly=${this.readOnly}
        mode="yaml"
        autocomplete-entities
        .error=${!1===this.isValid}
        @value-changed=${this._onChange}
        dir="ltr"
      ></ha-code-editor>
    `}},{kind:"method",key:"_onChange",value:function(e){let t;e.stopPropagation(),this._yaml=e.detail.value;let i=!0;if(this._yaml)try{t=(0,r.zD)(this._yaml,{schema:this.yamlSchema})}catch(e){i=!1}else t={};this.value=t,this.isValid=i,(0,a.B)(this,"value-changed",{value:t,isValid:i})}},{kind:"get",key:"yaml",value:function(){return this._yaml}}]}}),n.oi)},26765:(e,t,i)=>{i.d(t,{Ys:()=>a,g7:()=>s,D9:()=>l});var r=i(47181);const n=()=>Promise.all([i.e(85084),i.e(1281)]).then(i.bind(i,1281)),o=(e,t,i)=>new Promise((o=>{const a=t.cancel,s=t.confirm;(0,r.B)(e,"show-dialog",{dialogTag:"dialog-box",dialogImport:n,dialogParams:{...t,...i,cancel:()=>{o(!(null==i||!i.prompt)&&null),a&&a()},confirm:e=>{o(null==i||!i.prompt||e),s&&s(e)}}})})),a=(e,t)=>o(e,t),s=(e,t)=>o(e,t,{confirmation:!0}),l=(e,t)=>o(e,t,{prompt:!0})},1065:(e,t,i)=>{i.r(t),i.d(t,{aisSaveDbSettings:()=>b});i(18900),i(53822),i(46583),i(53268),i(12730);var r=i(37500),n=i(33310),o=i(77426),a=(i(60010),i(38353),i(63081),i(43709),i(13529),i(44577),i(54909),i(29925),i(31206),i(53775)),s=i(11654);function l(){l=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(i){t.forEach((function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach((function(r){t.forEach((function(t){var n=t.placement;if(t.kind===r&&("static"===n||"prototype"===n)){var o="static"===n?e:i;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var r=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],r=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!h(e))return i.push(e);var t=this.decorateElement(e,n);i.push(t.element),i.push.apply(i,t.extras),r.push.apply(r,t.finishers)}),this),!t)return{elements:i,finishers:r};var o=this.decorateConstructor(i,t);return r.push.apply(r,o.finishers),o.finishers=r,o},addElementPlacement:function(e,t,i){var r=t[e.placement];if(!i&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var i=[],r=[],n=e.decorators,o=n.length-1;o>=0;o--){var a=t[e.placement];a.splice(a.indexOf(e.key),1);var s=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,n[o])(s)||s);e=l.element,this.addElementPlacement(e,t),l.finisher&&r.push(l.finisher);var d=l.extras;if(d){for(var c=0;c<d.length;c++)this.addElementPlacement(d[c],t);i.push.apply(i,d)}}return{element:e,finishers:r,extras:i}},decorateConstructor:function(e,t){for(var i=[],r=t.length-1;r>=0;r--){var n=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[r])(n)||n);if(void 0!==o.finisher&&i.push(o.finisher),void 0!==o.elements){e=o.elements;for(var a=0;a<e.length-1;a++)for(var s=a+1;s<e.length;s++)if(e[a].key===e[s].key&&e[a].placement===e[s].placement)throw new TypeError("Duplicated element ("+e[a].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return m(e,t);var i=Object.prototype.toString.call(e).slice(8,-1);return"Object"===i&&e.constructor&&(i=e.constructor.name),"Map"===i||"Set"===i?Array.from(e):"Arguments"===i||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(i)?m(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=f(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:i,placement:r,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:p(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=p(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var r=(0,t[i])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}function d(e){var t,i=f(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function c(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function h(e){return e.decorators&&e.decorators.length}function u(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function p(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function f(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var r=i.call(e,t||"default");if("object"!=typeof r)return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function m(e,t){(null==t||t>e.length)&&(t=e.length);for(var i=0,r=new Array(t);i<t;i++)r[i]=e[i];return r}function y(e,t,i){return y="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,i){var r=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=v(e)););return e}(e,t);if(r){var n=Object.getOwnPropertyDescriptor(r,t);return n.get?n.get.call(i):n.value}},y(e,t,i||e)}function v(e){return v=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)},v(e)}const b=e=>(0,a.h)(fetch("/api/ais_file/ais_db_view",{method:"POST",credentials:"same-origin",body:JSON.stringify(e)}));!function(e,t,i,r){var n=l();if(r)for(var o=0;o<r.length;o++)n=r[o](n);var a=t((function(e){n.initializeInstanceElements(e,s.elements)}),i),s=n.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},r=0;r<e.length;r++){var n,o=e[r];if("method"===o.kind&&(n=t.find(i)))if(u(o.descriptor)||u(n.descriptor)){if(h(o)||h(n))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");n.descriptor=o.descriptor}else{if(h(o)){if(h(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");n.decorators=o.decorators}c(o,n)}else t.push(o)}return t}(a.d.map(d)),e);n.initializeClassElements(a.F,s.elements),n.runClassFinishers(a.F,s.finishers)}([(0,n.Mo)("ha-config-ais-dom-config-logs")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.Cb)()],key:"isWide",value:void 0},{kind:"field",decorators:[(0,n.Cb)({type:String})],key:"logLevel",value:()=>""},{kind:"field",decorators:[(0,n.Cb)({type:String})],key:"logDrive",value:()=>""},{kind:"field",decorators:[(0,n.Cb)({type:Number})],key:"logRotating",value:()=>1},{kind:"field",decorators:[(0,n.Cb)({type:Boolean})],key:"dbConnectionValidating",value:()=>!1},{kind:"field",decorators:[(0,n.Cb)({type:String})],key:"logModeInfo",value:()=>""},{kind:"field",decorators:[(0,n.Cb)({type:String})],key:"dbDrive",value:()=>""},{kind:"field",decorators:[(0,n.Cb)({type:String})],key:"dbEngine",value:()=>""},{kind:"field",decorators:[(0,n.Cb)({type:String})],key:"dbUser",value:()=>""},{kind:"field",decorators:[(0,n.Cb)({type:String})],key:"dbPassword",value:()=>""},{kind:"field",decorators:[(0,n.Cb)({type:String})],key:"dbServerIp",value:()=>""},{kind:"field",decorators:[(0,n.Cb)({type:String})],key:"dbServerName",value:()=>""},{kind:"field",decorators:[(0,n.Cb)({type:Number})],key:"dbKeepDays",value:()=>10},{kind:"field",decorators:[(0,n.Cb)({type:String})],key:"errorDbInfo",value:()=>""},{kind:"field",decorators:[(0,n.Cb)({type:String})],key:"messageDbInfo",value:()=>""},{kind:"field",decorators:[(0,n.Cb)({type:Boolean})],key:"dbShowLogbook",value:()=>!1},{kind:"field",decorators:[(0,n.Cb)({type:Boolean})],key:"dbShowHistory",value:()=>!1},{kind:"field",decorators:[(0,n.Cb)()],key:"dbInclude",value:()=>""},{kind:"field",decorators:[(0,n.Cb)()],key:"dbExclude",value:()=>""},{kind:"get",static:!0,key:"styles",value:function(){return[s.Qx,r.iv`
        .content {
          padding-bottom: 32px;
        }

        .border {
          margin: 32px auto 0;
          border-bottom: 1px solid rgba(0, 0, 0, 0.12);
          max-width: 1040px;
        }
        .narrow .border {
          max-width: 640px;
        }
        .card-actions {
          display: flex;
        }
        ha-card > div#card-icon {
          margin: -4px 0;
          position: absolute;
          top: 1em;
          right: 1em;
          border-radius: 25px;
        }
        .center-container {
          text-align: center;
          height: 70px;
        }

        .config-invalid {
          color: red;
          text-align: center;
          padding-bottom: 1em;
        }
        .config-valid {
          color: green;
          text-align: center;
          padding-bottom: 1em;
        }
        .inportant-info {
          color: var(--primary-color);
          font-weight: bold;
        }

        @keyframes pulse {
          0% {
            background-color: var(--card-background-color);
          }
          100% {
            background-color: orange;
          }
        }
        @keyframes pulseRed {
          0% {
            background-color: var(--card-background-color);
          }
          100% {
            background-color: red;
          }
        }
      `]}},{kind:"method",key:"getLogError",value:function(e){let t="";return e.attributes.errorInfo&&(t=e.attributes.errorInfo+" "),"debug"===this.logLevel&&(t+="Logowanie w trybie debug generuje duże ilości logów i obciąża system. Używaj go tylko podczas diagnozowania problemu. "),t}},{kind:"method",key:"isNotSeleced",value:function(e){return!e||("-"===e||""===e)}},{kind:"method",key:"getLogIconAnimationStyle",value:function(e){if(!this.isNotSeleced(this.logDrive)){if("debug"===this.logLevel)return"animation: pulseRed 2s infinite;";if("info"===this.logLevel)return"animation: pulse 4s infinite;";if("warning"===this.logLevel)return"animation: pulse 7s infinite;";if("error"===this.logLevel)return"animation: pulse 8s infinite;";if("critical"===this.logLevel)return"animation: pulse 10s infinite;"}return""}},{kind:"method",key:"getDbStatusIcon",value:function(e){if(this.isNotSeleced(e))return r.dy``;let t="mdi:database";return"SQLite (memory)"===e&&(t="mdi:memory"),"SQLite (file)"===e&&(t="mdi:file"),"PostgreSQL"===e&&(t="mdi:server"),r.dy`
      <div id="card-icon" style="animation: pulse 6s infinite;">
        <ha-icon icon=${t}></ha-icon>
      </div>
    `}},{kind:"method",key:"_getDbConnectionSettings",value:function(){const e=this.hass.states["sensor.ais_db_connection_info"].attributes;this.dbEngine=e.dbEngine,this.dbDrive=e.dbDrive,this.dbPassword=e.dbPassword,this.dbUser=e.dbUser,this.dbServerIp=e.dbServerIp,this.dbServerName=e.dbServerName,this.dbKeepDays=e.dbKeepDays,this.errorDbInfo="",this.messageDbInfo="",this.dbShowLogbook=e.dbShowLogbook,this.dbShowHistory=e.dbShowHistory,this.dbInclude=(0,o.$w)(e.dbInclude||"").trimRight(),this.dbExclude=(0,o.$w)(e.dbExclude||"").trimRight()}},{kind:"method",key:"_getLogSettings",value:function(){const e=this.hass.states["sensor.ais_logs_settings_info"].attributes;this.logDrive=e.logDrive,this.logLevel=e.logLevel,this.logRotating=e.logRotating}},{kind:"method",key:"firstUpdated",value:function(e){y(v(i.prototype),"firstUpdated",this).call(this,e),this._getDbConnectionSettings(),this._getLogSettings()}},{kind:"method",key:"render",value:function(){return r.dy`
      <hass-subpage header="Konfiguracja bramki AIS dom">
        <ha-config-section .is-wide=${this.isWide}>
          <span slot="header">Konfiguracja zapisu zdarzeń systemu</span>
          <ha-card header="Baza danych do zapisu zdarzeń">
            <!-- show db satus  -->
            ${this.getDbStatusIcon(this.dbEngine)}
            ${this.dbConnectionValidating?r.dy`<div style="width: 100%; text-align: center;">
                  <ha-circular-progress active></ha-circular-progress>
                </div>`:r.dy`
                  <div class="card-content">
                    Najprostszy wybór to baza SQLite, która nie wymaga
                    konfiguracji i może rejestrować dane w pamięci.
                    <b>Zmiany konfiguracji bazy wymagają restartu systemu.</b>
                    Baza w pamięci jest automatycznie używana, gdy włączysz
                    komponent Historia lub Dziennik.
                    <br />
                    <br />
                    <ha-icon icon="hass:chart-box" slot="suffix"></ha-icon>
                    <ha-switch
                      .checked=${this.dbShowHistory}
                      @change=${this.dbShowHistoryChanged}
                    ></ha-switch>
                    Historia - prezentowanie zdarzeń zapisanych w bazie na
                    wykresach w aplikacji
                    <br />
                    <br />

                    <ha-icon
                      icon="hass:format-list-bulleted-type"
                      slot="suffix"
                    ></ha-icon>
                    <ha-switch
                      .checked=${this.dbShowLogbook}
                      @change=${this.dbShowLogbookChanged}
                    ></ha-switch>
                    Dziennik - prezentowanie zmian zapisanych w bazie w
                    chronologicznej kolejności

                    <br /><br />

                    Wybór silnika bazy danych:
                    <br />
                    <ha-icon icon="mdi:database"></ha-icon>

                    <mwc-select
                      label-float="Silnik bazy danych"
                      label="Silnik bazy danych"
                      .value=${this.dbEngine}
                      @selected=${this.dbEngineChanged}
                    >
                      <mwc-list-item value="-">-</mwc-list-item>
                      <mwc-list-item value="SQLite (memory)"
                        >SQLite (memory)</mwc-list-item
                      >
                      <mwc-list-item value="SQLite (file)"
                        >SQLite (file)</mwc-list-item
                      >
                      <mwc-list-item value="PostgreSQL (local)"
                        >PostgreSQL (local)</mwc-list-item
                      >
                      <mwc-list-item value="MariaDB">MariaDB</mwc-list-item>
                      <mwc-list-item value="MySQL">MySQL</mwc-list-item>
                      <mwc-list-item value="PostgreSQL"
                        >PostgreSQL</mwc-list-item
                      >
                    </mwc-select>
                  </div>

                  <!-- MEMORY -->
                  ${"SQLite (memory)"===this.dbEngine?r.dy`
                        <div class="card-content">
                          Żeby utrzymać system w dobrej kondycji, codziennie
                          dokładnie o godzinie 5:15 rano, Asystent czyści pamięć
                          i usuwa zdarzenia i stany starsze niż <b>5 dni</b>.
                          <br /><br />
                          <span class="inportant-info">
                            Jeżeli zacznie brakować pamięci w systemie, to
                            automatycznie wyczyścimy całą historię bazy, żeby
                            zwolnić miejsce.
                          </span>
                          <br /><br />
                          Gdy chcesz zapisywać większą ilość dni w historii, to
                          zalecamy zapisywać zdarzenia w zdalnej bazie danych.
                        </div>
                      `:r.dy``}

                  <!-- PostgreSQL (local) -->
                  ${"PostgreSQL (local)"===this.dbEngine?r.dy`
                        <div class="card-content">
                          Żeby utrzymać system w dobrej kondycji, codziennie
                          dokładnie o godzinie 5:15 rano, Asystent czyści
                          lokalną bazę i usuwa zdarzenia i stany starsze niż
                          <b>10 dni</b>. <br /><br />
                          <span class="inportant-info">
                            Jeżeli zacznie brakować miejsca na dysku w systemie,
                            to automatycznie wyczyścimy całą historię lokalnej
                            bazy, żeby zwolnić miejsce.
                          </span>
                          <br /><br />
                          Gdy chcesz zapisywać większą ilość dni w historii, to
                          zalecamy zapisywać zdarzenia w zdalnej bazie danych.
                        </div>
                      `:r.dy``}

                  <!-- FILE -->
                  ${"SQLite (file)"===this.dbEngine?r.dy`
                        <div class="card-content">
                          Wybór dysku do zapisu bazy danych: <br />
                          <ha-icon icon="mdi:usb-flash-drive"></ha-icon>
                          <mwc-select
                            label-float="Dysk wymienny"
                            label="Dysk wymienny"
                            .value=${this.dbDrive}
                            @selected=${this.dbDriveChanged}
                          >
                            ${this.hass.states["input_select.ais_usb_flash_drives"].attributes.options.map((e=>r.dy`
                                  <mwc-list-item .value=${e}>
                                    ${e}
                                  </mwc-list-item>
                                `))} </mwc-select
                          >> <br /><br />
                        </div>
                      `:r.dy``}
                  <!-- DB -->
                  ${"MariaDB"===this.dbEngine||"MySQL"===this.dbEngine||"PostgreSQL"===this.dbEngine?r.dy`
                        <div class="card-content">
                          Parametry połączenia z bazą danych: <br />
                          <paper-input
                            placeholder="Użytkownik"
                            type="text"
                            id="db_user"
                            value=${this.dbUser}
                            @value-changed=${this.dbUserChanged}
                          >
                            <ha-icon icon="mdi:account" slot="suffix"></ha-icon>
                          </paper-input>
                          <paper-input
                            placeholder="Hasło"
                            no-label-float=""
                            type="password"
                            id="db_password"
                            .value=${this.dbPassword}
                            @value-changed=${this.dbPasswordChanged}
                          >
                            <ha-icon
                              icon="mdi:lastpass"
                              slot="suffix"
                            ></ha-icon>
                          </paper-input>
                          <paper-input
                            placeholder="IP Serwera DB"
                            no-label-float=""
                            type="text"
                            id="db_server_ip"
                            value=${this.dbServerIp}
                            @value-changed=${this.dbServerIpChanged}
                          >
                            <ha-icon
                              icon="mdi:ip-network"
                              slot="suffix"
                            ></ha-icon>
                          </paper-input>
                          <paper-input
                            placeholder="Nazwa bazy"
                            no-label-float=""
                            type="text"
                            id="db_server_name"
                            value=${this.dbServerName}
                            @value-changed=${this.dbServerNameChanged}
                          >
                            <ha-icon
                              icon="mdi:database-check"
                              slot="suffix"
                            ></ha-icon>
                          </paper-input>
                        </div>
                      `:r.dy``}
                  <div class="card-content">
                    <h1>Filtrowanie zapisu zdarzeń</h1>
                    <ha-expansion-panel
                      .header=${r.dy`<ha-icon icon="mdi:filter-plus"></ha-icon>
                        &nbsp;Wybrane do zapisywania:`}
                    >
                      <ha-code-editor
                        mode="yaml"
                        .value=${this.dbInclude}
                        @value-changed=${this.dbIncludeChanged}
                      >
                      </ha-code-editor>
                    </ha-expansion-panel>

                    <ha-expansion-panel
                      .header=${r.dy`<ha-icon
                          icon="mdi:filter-remove"
                        ></ha-icon>
                        &nbsp;Wykluczone z zapisywania:`}
                    >
                      <ha-code-editor
                        mode="yaml"
                        .value=${this.dbExclude}
                        @value-changed=${this.dbExcludeChanged}
                      >
                      </ha-code-editor>
                    </ha-expansion-panel>
                  </div>

                  <!-- KEEP DAYS -->
                  ${"SQLite (file)"===this.dbEngine||"MariaDB"===this.dbEngine||"MySQL"===this.dbEngine||"PostgreSQL"===this.dbEngine?r.dy`
                  <div class="card-content">
                    Żeby utrzymać system w dobrej kondycji, codziennie dokładnie o godzinie 5:15 rano Asystent usuwa z bazy zdarzenia i stany starsze niż <b>określona liczba dni</b>.
                    <br /><br />
                    W tym miejscu możesz określić liczbę dni, których historia ma być
                    przechowywana w bazie danych.
                    <paper-input
                      id="db_keep_days"
                      type="number"
                      value=${this.dbKeepDays}
                      @value-changed=${this.dbKeepDaysChanged}
                      maxlength="4"
                      max="9999"
                      min="1"
                      label-float="Liczba dni historii przechowywanych w bazie"
                      label="Liczba dni historii przechowywanych w bazie"
                    >
                      <ha-icon icon="mdi:calendar" slot="suffix"></ha-icon>
                    </paper-input>
                  </div>
                </div>
                `:r.dy``}
                `}

            <div class="center-container">
              <mwc-button @click="${this.saveDbSettings}">
                Sprawdź i zapisz
              </mwc-button>
            </div>

            <div class="center-content">
              <div class="config-invalid">
                <span class="text"> ${this.errorDbInfo} </span>
              </div>
              <div class="config-valid">
                <span class="text"> ${this.messageDbInfo} </span>
              </div>
            </div>
          </ha-card>
        </ha-config-section>

        <ha-config-section .is-wide=${this.isWide}>
          <span slot="header">Ustawienie zapisu logów systemu</span>
          <ha-card header=" Wybór parametrów logowania">
            <div
              id="card-icon"
              .style=${this.getLogIconAnimationStyle(this.hass.states["sensor.ais_logs_settings_info"])}
            >
              <ha-icon icon="mdi:content-save-edit"></ha-icon>
            </div>
            <div class="card-content">
              <ha-icon icon="mdi:bug-check"></ha-icon>

              <!-- <ha-paper-dropdown-menu
                label-float="Poziom logowania"
                dynamic-align=""
                label="Poziomy logowania"
              >
                <paper-listbox
                  slot="dropdown-content"
                  attr-for-selected="item-name"
                  .selected=${this.logLevel}
                  @iron-select=${this.logLevelChanged}
                > -->
              <mwc-select
                label-float="Poziomy logowania"
                label="Poziomy logowania"
                .value=${this.logLevel}
                @selected=${this.logLevelChanged}
              >
                <mwc-list-item value="critical">critical</mwc-list-item>
                <mwc-list-item value="error">error</mwc-list-item>
                <mwc-list-item value="warning">warning</mwc-list-item>
                <mwc-list-item value="info">info</mwc-list-item>
                <mwc-list-item value="debug">debug</mwc-list-item>
              </mwc-select>
              <br />

              Jeśli chcesz zapisywać logi trwale do pliku, wybierz dysk wymienny
              (USB, SD card) na którym będą zapisywane logi: <br />
              <ha-icon icon="mdi:usb-flash-drive"></ha-icon>

              <!-- <ha-paper-dropdown-menu
                label-float="Wybrany dysk"
                dynamic-align=""
                label="Dyski wymienne"
              >
                <paper-listbox
                  slot="dropdown-content"
                  attr-for-selected="item-name"
                  .selected=${this.logDrive}
                  @iron-select=${this.logDriveChanged}
                > -->
              <mwc-select
                label-float="Dysk wymienny"
                label="Dysk wymienny"
                .value=${this.logDrive}
                @selected=${this.logDriveChanged}
              >
                ${this.hass.states["input_select.ais_usb_flash_drives"].attributes.options.map((e=>r.dy`
                      <mwc-list-item .value=${e}> ${e}</mwc-list-item>
                    `))}
              </mwc-select>

              <br /><br />
              ${this.isNotSeleced(this.logDrive)?r.dy``:r.dy`
                    Możesz określić liczbę dni przechowywanych w jednym pliku.
                    Rotacja plików dziennika wykonywna jest o północy.
                    <paper-input
                      type="number"
                      .value=${this.logRotating}
                      @change=${this.logRotatingDaysChanged}
                      maxlength="4"
                      max="9999"
                      min="1"
                      label-float="Liczba dni przechowywanych w jednym pliku loga"
                      label="Liczba dni przechowywanych w jednym pliku loga"
                    >
                      <ha-icon icon="mdi:calendar" slot="suffix"></ha-icon>
                    </paper-input>
                    Zmiana dysku lub zmiana liczby dni przechowywanych będzie
                    zralizowana po restartcie systemu.
                  `}
            </div>

            <div class="card-content">
              <div class="config-invalid">
                <span class="text">
                  ${this.getLogError(this.hass.states["sensor.ais_logs_settings_info"])}
                </span>
              </div>
            </div>
            <div class="card-content">${this.logModeInfo}</div>
          </ha-card>
        </ha-config-section>
        <br />
        <br />
      </hass-subpage>
    `}},{kind:"method",key:"saveLoggerSettings",value:function(){this.hass.callService("ais_files","change_logger_settings",{log_drive:this.logDrive,log_level:this.logLevel,log_rotating:this.logRotating})}},{kind:"method",key:"logDriveChanged",value:function(e){const t=e.target.selected.value;t!==this.logDrive&&(this.logDrive=t,this.isNotSeleced(this.logDrive)?this.logModeInfo="Zapis logów do pliku wyłączony ":this.logModeInfo="Zapis logów do pliku /dyski-wymienne/"+this.logDrive+"/ais.log",this.saveLoggerSettings())}},{kind:"method",key:"logLevelChanged",value:function(e){const t=e.target.selected.value;t!==this.logLevel&&(this.logLevel=t,this.logModeInfo="Poziom logowania: "+this.logLevel,this.saveLoggerSettings())}},{kind:"method",key:"logRotatingDaysChanged",value:function(e){const t=Number(e.target.value);this.logRotating!==t&&(this.logRotating=t,1===this.logRotating?this.logModeInfo="Rotacja logów codziennie.":this.logModeInfo="Rotacja logów co "+this.logRotating+" dni.",this.saveLoggerSettings())}},{kind:"method",key:"saveDbSettings",value:async function(){this.dbConnectionValidating=!0;try{const e=await b({dbEngine:this.dbEngine,dbDrive:this.dbDrive,dbPassword:this.dbPassword,dbUser:this.dbUser,dbServerIp:this.dbServerIp,dbServerName:this.dbServerName,dbKeepDays:this.dbKeepDays,dbShowLogbook:this.dbShowLogbook,dbShowHistory:this.dbShowHistory,dbInclude:(0,o.zD)(this.dbInclude),dbExclude:(0,o.zD)(this.dbExclude,{})});this.errorDbInfo=e.error,this.messageDbInfo=e.info}catch(e){this.errorDbInfo=e}this.dbConnectionValidating=!1}},{kind:"method",key:"dbShowLogbookChanged",value:function(e){const t=e.target.checked;t!==this.dbShowLogbook&&(this.dbShowLogbook=t,this.dbShowLogbook&&this.isNotSeleced(this.dbEngine)&&(this.dbEngine="SQLite (memory)"),this.saveDbSettings())}},{kind:"method",key:"dbShowHistoryChanged",value:function(e){const t=e.target.checked;t!==this.dbShowHistory&&(this.dbShowHistory=t,this.dbShowHistory&&this.isNotSeleced(this.dbEngine)&&(this.dbEngine="SQLite (memory)"),this.saveDbSettings())}},{kind:"method",key:"dbEngineChanged",value:function(e){const t=e.target.selected.value;t!==this.dbEngine&&(this.dbEngine=t,this.isNotSeleced(t)&&(this.dbShowHistory=!1,this.dbShowLogbook=!1,this.saveDbSettings()),"SQLite (memory)"===t&&this.saveDbSettings(),"SQLite (file)"===t&&(this.dbDrive="-"))}},{kind:"method",key:"dbDriveChanged",value:function(e){const t=e.target.selected.value;t!==this.dbDrive&&(this.dbDrive=t)}},{kind:"method",key:"dbUserChanged",value:function(e){const t=e.detail.value;t!==this.dbUser&&(this.dbUser=t)}},{kind:"method",key:"dbPasswordChanged",value:function(e){const t=e.detail.value;t!==this.dbPassword&&(this.dbPassword=t)}},{kind:"method",key:"dbServerIpChanged",value:function(e){const t=e.detail.value;t!==this.dbServerIp&&(this.dbServerIp=t)}},{kind:"method",key:"dbServerNameChanged",value:function(e){const t=e.detail.value;t!==this.dbServerName&&(this.dbServerName=t)}},{kind:"method",key:"dbKeepDaysChanged",value:function(e){const t=e.detail.value;t!==this.dbKeepDays&&(this.dbKeepDays=t)}},{kind:"method",key:"dbIncludeChanged",value:function(e){e.stopPropagation(),e.detail.value.replace(/\s/g,"").length>0&&(this.dbInclude=e.detail.value)}},{kind:"method",key:"dbExcludeChanged",value:function(e){e.stopPropagation(),e.detail.value.replace(/\s/g,"").length>0&&(this.dbExclude=e.detail.value)}}]}}),r.oi)}}]);
//# sourceMappingURL=bec7946c.js.map
"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[1804],{83927:(e,t,r)=>{var i=r(92685),n=r(92038),s=r(37500),a=r(33310),o=r(47181);function c(){c=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(i){t.forEach((function(t){var n=t.placement;if(t.kind===i&&("static"===n||"prototype"===n)){var s="static"===n?e:r;this.defineClassElement(s,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var i=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===i?void 0:i.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],i=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!p(e))return r.push(e);var t=this.decorateElement(e,n);r.push(t.element),r.push.apply(r,t.extras),i.push.apply(i,t.finishers)}),this),!t)return{elements:r,finishers:i};var s=this.decorateConstructor(r,t);return i.push.apply(i,s.finishers),s.finishers=i,s},addElementPlacement:function(e,t,r){var i=t[e.placement];if(!r&&-1!==i.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");i.push(e.key)},decorateElement:function(e,t){for(var r=[],i=[],n=e.decorators,s=n.length-1;s>=0;s--){var a=t[e.placement];a.splice(a.indexOf(e.key),1);var o=this.fromElementDescriptor(e),c=this.toElementFinisherExtras((0,n[s])(o)||o);e=c.element,this.addElementPlacement(e,t),c.finisher&&i.push(c.finisher);var l=c.extras;if(l){for(var d=0;d<l.length;d++)this.addElementPlacement(l[d],t);r.push.apply(r,l)}}return{element:e,finishers:i,extras:r}},decorateConstructor:function(e,t){for(var r=[],i=t.length-1;i>=0;i--){var n=this.fromClassDescriptor(e),s=this.toClassDescriptor((0,t[i])(n)||n);if(void 0!==s.finisher&&r.push(s.finisher),void 0!==s.elements){e=s.elements;for(var a=0;a<e.length-1;a++)for(var o=a+1;o<e.length;o++)if(e[a].key===e[o].key&&e[a].placement===e[o].placement)throw new TypeError("Duplicated element ("+e[a].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return m(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?m(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=f(e.key),i=String(e.placement);if("static"!==i&&"prototype"!==i&&"own"!==i)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+i+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var s={kind:t,key:r,placement:i,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),s.initializer=e.initializer),s},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:h(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=h(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var i=(0,t[r])(e);if(void 0!==i){if("function"!=typeof i)throw new TypeError("Finishers must return a constructor.");e=i}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}function l(e){var t,r=f(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var i={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(i.decorators=e.decorators),"field"===e.kind&&(i.initializer=e.value),i}function d(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function p(e){return e.decorators&&e.decorators.length}function u(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function h(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function f(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var i=r.call(e,t||"default");if("object"!=typeof i)return i;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function m(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,i=new Array(t);r<t;r++)i[r]=e[r];return i}!function(e,t,r,i){var n=c();if(i)for(var s=0;s<i.length;s++)n=i[s](n);var a=t((function(e){n.initializeInstanceElements(e,o.elements)}),r),o=n.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===s.key&&e.placement===s.placement},i=0;i<e.length;i++){var n,s=e[i];if("method"===s.kind&&(n=t.find(r)))if(u(s.descriptor)||u(n.descriptor)){if(p(s)||p(n))throw new ReferenceError("Duplicated methods ("+s.key+") can't be decorated.");n.descriptor=s.descriptor}else{if(p(s)){if(p(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+s.key+").");n.decorators=s.decorators}d(s,n)}else t.push(s)}return t}(a.d.map(l)),e);n.initializeClassElements(a.F,o.elements),n.runClassFinishers(a.F,o.finishers)}([(0,a.Mo)("ha-formfield")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"method",key:"_labelClick",value:function(){const e=this.input;if(e)switch(e.focus(),e.tagName){case"HA-CHECKBOX":case"HA-RADIO":e.checked=!e.checked,(0,o.B)(e,"change");break;default:e.click()}}},{kind:"field",static:!0,key:"styles",value:()=>[n.W,s.iv`
      :host(:not([alignEnd])) ::slotted(ha-switch) {
        margin-right: 10px;
        margin-inline-end: 10px;
        margin-inline-start: inline;
      }
      .mdc-form-field > label {
        direction: var(--direction);
        margin-inline-start: 0;
        margin-inline-end: auto;
        padding-inline-start: 4px;
        padding-inline-end: 0;
      }
    `]}]}}),i.a)},33220:(e,t,r)=>{var i=r(62552),n=r(44973),s=r(37500);function a(){a=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(i){t.forEach((function(t){var n=t.placement;if(t.kind===i&&("static"===n||"prototype"===n)){var s="static"===n?e:r;this.defineClassElement(s,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var i=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===i?void 0:i.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],i=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!l(e))return r.push(e);var t=this.decorateElement(e,n);r.push(t.element),r.push.apply(r,t.extras),i.push.apply(i,t.finishers)}),this),!t)return{elements:r,finishers:i};var s=this.decorateConstructor(r,t);return i.push.apply(i,s.finishers),s.finishers=i,s},addElementPlacement:function(e,t,r){var i=t[e.placement];if(!r&&-1!==i.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");i.push(e.key)},decorateElement:function(e,t){for(var r=[],i=[],n=e.decorators,s=n.length-1;s>=0;s--){var a=t[e.placement];a.splice(a.indexOf(e.key),1);var o=this.fromElementDescriptor(e),c=this.toElementFinisherExtras((0,n[s])(o)||o);e=c.element,this.addElementPlacement(e,t),c.finisher&&i.push(c.finisher);var l=c.extras;if(l){for(var d=0;d<l.length;d++)this.addElementPlacement(l[d],t);r.push.apply(r,l)}}return{element:e,finishers:i,extras:r}},decorateConstructor:function(e,t){for(var r=[],i=t.length-1;i>=0;i--){var n=this.fromClassDescriptor(e),s=this.toClassDescriptor((0,t[i])(n)||n);if(void 0!==s.finisher&&r.push(s.finisher),void 0!==s.elements){e=s.elements;for(var a=0;a<e.length-1;a++)for(var o=a+1;o<e.length;o++)if(e[a].key===e[o].key&&e[a].placement===e[o].placement)throw new TypeError("Duplicated element ("+e[a].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return h(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?h(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=u(e.key),i=String(e.placement);if("static"!==i&&"prototype"!==i&&"own"!==i)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+i+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var s={kind:t,key:r,placement:i,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),s.initializer=e.initializer),s},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:p(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=p(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var i=(0,t[r])(e);if(void 0!==i){if("function"!=typeof i)throw new TypeError("Finishers must return a constructor.");e=i}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}function o(e){var t,r=u(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var i={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(i.decorators=e.decorators),"field"===e.kind&&(i.initializer=e.value),i}function c(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function l(e){return e.decorators&&e.decorators.length}function d(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function p(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function u(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var i=r.call(e,t||"default");if("object"!=typeof i)return i;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function h(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,i=new Array(t);r<t;r++)i[r]=e[r];return i}!function(e,t,r,i){var n=a();if(i)for(var s=0;s<i.length;s++)n=i[s](n);var p=t((function(e){n.initializeInstanceElements(e,u.elements)}),r),u=n.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===s.key&&e.placement===s.placement},i=0;i<e.length;i++){var n,s=e[i];if("method"===s.kind&&(n=t.find(r)))if(d(s.descriptor)||d(n.descriptor)){if(l(s)||l(n))throw new ReferenceError("Duplicated methods ("+s.key+") can't be decorated.");n.descriptor=s.descriptor}else{if(l(s)){if(l(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+s.key+").");n.decorators=s.decorators}c(s,n)}else t.push(s)}return t}(p.d.map(o)),e);n.initializeClassElements(p.F,u.elements),n.runClassFinishers(p.F,u.finishers)}([(0,r(33310).Mo)("ha-radio")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",static:!0,key:"styles",value:()=>[n.W,s.iv`
      :host {
        --mdc-theme-secondary: var(--primary-color);
      }
    `]}]}}),i.J)},43709:(e,t,r)=>{var i=r(11581),n=r(4301),s=r(37500),a=r(33310),o=r(62359);function c(){c=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(i){t.forEach((function(t){var n=t.placement;if(t.kind===i&&("static"===n||"prototype"===n)){var s="static"===n?e:r;this.defineClassElement(s,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var i=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===i?void 0:i.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],i=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!p(e))return r.push(e);var t=this.decorateElement(e,n);r.push(t.element),r.push.apply(r,t.extras),i.push.apply(i,t.finishers)}),this),!t)return{elements:r,finishers:i};var s=this.decorateConstructor(r,t);return i.push.apply(i,s.finishers),s.finishers=i,s},addElementPlacement:function(e,t,r){var i=t[e.placement];if(!r&&-1!==i.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");i.push(e.key)},decorateElement:function(e,t){for(var r=[],i=[],n=e.decorators,s=n.length-1;s>=0;s--){var a=t[e.placement];a.splice(a.indexOf(e.key),1);var o=this.fromElementDescriptor(e),c=this.toElementFinisherExtras((0,n[s])(o)||o);e=c.element,this.addElementPlacement(e,t),c.finisher&&i.push(c.finisher);var l=c.extras;if(l){for(var d=0;d<l.length;d++)this.addElementPlacement(l[d],t);r.push.apply(r,l)}}return{element:e,finishers:i,extras:r}},decorateConstructor:function(e,t){for(var r=[],i=t.length-1;i>=0;i--){var n=this.fromClassDescriptor(e),s=this.toClassDescriptor((0,t[i])(n)||n);if(void 0!==s.finisher&&r.push(s.finisher),void 0!==s.elements){e=s.elements;for(var a=0;a<e.length-1;a++)for(var o=a+1;o<e.length;o++)if(e[a].key===e[o].key&&e[a].placement===e[o].placement)throw new TypeError("Duplicated element ("+e[a].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return m(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?m(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=f(e.key),i=String(e.placement);if("static"!==i&&"prototype"!==i&&"own"!==i)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+i+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var s={kind:t,key:r,placement:i,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),s.initializer=e.initializer),s},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:h(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=h(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var i=(0,t[r])(e);if(void 0!==i){if("function"!=typeof i)throw new TypeError("Finishers must return a constructor.");e=i}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}function l(e){var t,r=f(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var i={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(i.decorators=e.decorators),"field"===e.kind&&(i.initializer=e.value),i}function d(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function p(e){return e.decorators&&e.decorators.length}function u(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function h(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function f(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var i=r.call(e,t||"default");if("object"!=typeof i)return i;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function m(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,i=new Array(t);r<t;r++)i[r]=e[r];return i}function y(e,t,r){return y="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,r){var i=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=v(e)););return e}(e,t);if(i){var n=Object.getOwnPropertyDescriptor(i,t);return n.get?n.get.call(r):n.value}},y(e,t,r||e)}function v(e){return v=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)},v(e)}!function(e,t,r,i){var n=c();if(i)for(var s=0;s<i.length;s++)n=i[s](n);var a=t((function(e){n.initializeInstanceElements(e,o.elements)}),r),o=n.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===s.key&&e.placement===s.placement},i=0;i<e.length;i++){var n,s=e[i];if("method"===s.kind&&(n=t.find(r)))if(u(s.descriptor)||u(n.descriptor)){if(p(s)||p(n))throw new ReferenceError("Duplicated methods ("+s.key+") can't be decorated.");n.descriptor=s.descriptor}else{if(p(s)){if(p(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+s.key+").");n.decorators=s.decorators}d(s,n)}else t.push(s)}return t}(a.d.map(l)),e);n.initializeClassElements(a.F,o.elements),n.runClassFinishers(a.F,o.finishers)}([(0,a.Mo)("ha-switch")],(function(e,t){class r extends t{constructor(...t){super(...t),e(this)}}return{F:r,d:[{kind:"field",decorators:[(0,a.Cb)({type:Boolean})],key:"haptic",value:()=>!1},{kind:"method",key:"firstUpdated",value:function(){y(v(r.prototype),"firstUpdated",this).call(this),this.addEventListener("change",(()=>{this.haptic&&(0,o.j)("light")}))}},{kind:"field",static:!0,key:"styles",value:()=>[n.W,s.iv`
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
    `]}]}}),i.H)},26765:(e,t,r)=>{r.d(t,{Ys:()=>a,g7:()=>o,D9:()=>c});var i=r(47181);const n=()=>Promise.all([r.e(85084),r.e(1281)]).then(r.bind(r,1281)),s=(e,t,r)=>new Promise((s=>{const a=t.cancel,o=t.confirm;(0,i.B)(e,"show-dialog",{dialogTag:"dialog-box",dialogImport:n,dialogParams:{...t,...r,cancel:()=>{s(!(null==r||!r.prompt)&&null),a&&a()},confirm:e=>{s(null==r||!r.prompt||e),o&&o(e)}}})})),a=(e,t)=>s(e,t),o=(e,t)=>s(e,t,{confirmation:!0}),c=(e,t)=>s(e,t,{prompt:!0})},49412:(e,t,r)=>{r.r(t);r(33220),r(83927),r(53268),r(12730),r(62744),r(60010),r(38353),r(63081),r(43709),r(54909),r(29925);var i=r(37500),n=r(33310),s=r(11654);function a(){a=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(i){t.forEach((function(t){var n=t.placement;if(t.kind===i&&("static"===n||"prototype"===n)){var s="static"===n?e:r;this.defineClassElement(s,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var i=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===i?void 0:i.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],i=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!l(e))return r.push(e);var t=this.decorateElement(e,n);r.push(t.element),r.push.apply(r,t.extras),i.push.apply(i,t.finishers)}),this),!t)return{elements:r,finishers:i};var s=this.decorateConstructor(r,t);return i.push.apply(i,s.finishers),s.finishers=i,s},addElementPlacement:function(e,t,r){var i=t[e.placement];if(!r&&-1!==i.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");i.push(e.key)},decorateElement:function(e,t){for(var r=[],i=[],n=e.decorators,s=n.length-1;s>=0;s--){var a=t[e.placement];a.splice(a.indexOf(e.key),1);var o=this.fromElementDescriptor(e),c=this.toElementFinisherExtras((0,n[s])(o)||o);e=c.element,this.addElementPlacement(e,t),c.finisher&&i.push(c.finisher);var l=c.extras;if(l){for(var d=0;d<l.length;d++)this.addElementPlacement(l[d],t);r.push.apply(r,l)}}return{element:e,finishers:i,extras:r}},decorateConstructor:function(e,t){for(var r=[],i=t.length-1;i>=0;i--){var n=this.fromClassDescriptor(e),s=this.toClassDescriptor((0,t[i])(n)||n);if(void 0!==s.finisher&&r.push(s.finisher),void 0!==s.elements){e=s.elements;for(var a=0;a<e.length-1;a++)for(var o=a+1;o<e.length;o++)if(e[a].key===e[o].key&&e[a].placement===e[o].placement)throw new TypeError("Duplicated element ("+e[a].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return h(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?h(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=u(e.key),i=String(e.placement);if("static"!==i&&"prototype"!==i&&"own"!==i)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+i+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var s={kind:t,key:r,placement:i,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),s.initializer=e.initializer),s},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:p(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=p(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var i=(0,t[r])(e);if(void 0!==i){if("function"!=typeof i)throw new TypeError("Finishers must return a constructor.");e=i}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}function o(e){var t,r=u(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var i={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(i.decorators=e.decorators),"field"===e.kind&&(i.initializer=e.value),i}function c(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function l(e){return e.decorators&&e.decorators.length}function d(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function p(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function u(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var i=r.call(e,t||"default");if("object"!=typeof i)return i;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function h(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,i=new Array(t);r<t;r++)i[r]=e[r];return i}!function(e,t,r,i){var n=a();if(i)for(var s=0;s<i.length;s++)n=i[s](n);var p=t((function(e){n.initializeInstanceElements(e,u.elements)}),r),u=n.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===s.key&&e.placement===s.placement},i=0;i<e.length;i++){var n,s=e[i];if("method"===s.kind&&(n=t.find(r)))if(d(s.descriptor)||d(n.descriptor)){if(l(s)||l(n))throw new ReferenceError("Duplicated methods ("+s.key+") can't be decorated.");n.descriptor=s.descriptor}else{if(l(s)){if(l(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+s.key+").");n.decorators=s.decorators}c(s,n)}else t.push(s)}return t}(p.d.map(o)),e);n.initializeClassElements(p.F,u.elements),n.runClassFinishers(p.F,u.finishers)}([(0,n.Mo)("ha-config-ais-dom-config-update")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.Cb)({type:Boolean})],key:"isWide",value:()=>!0},{kind:"field",decorators:[(0,n.Cb)({type:Boolean})],key:"validateConfigInProgress",value:()=>!1},{kind:"field",decorators:[(0,n.Cb)({type:String})],key:"validateLog",value:()=>""},{kind:"field",decorators:[(0,n.Cb)({type:String})],key:"aisButtonVersionCheckUpgrade",value:()=>""},{kind:"field",decorators:[(0,n.Cb)({type:String})],key:"backupType",value:()=>"all"},{kind:"field",decorators:[(0,n.Cb)({type:String})],key:"backupType2",value:()=>"all"},{kind:"method",key:"firstUpdated",value:async function(){}},{kind:"method",key:"render",value:function(){return i.dy`
      <hass-subpage header="Konfiguracja bramki AIS dom">
        <ha-config-section .isWide=${this.isWide}>
          <span slot="header">Oprogramowanie bramki</span>
          <span slot="introduction"
            >Możesz zaktualizować system do najnowszej wersji, wykonać kopię
            zapasową ustawień i zsynchronizować bramkę z Portalem
            Integratora</span
          >
          <ha-card header="Wersja systemu AI-Speaker">
            <div class="card-content" style="text-align:center">
              <div
                style="color:${this._getTextColor(this.hass.states["sensor.version_info"])}"
              >
                ${this.hass.states["sensor.version_info"].state}
              </div>
              <img class="versionLogo" src="/static/ais_version.png" />
              <div style="text-align:left">
                <div style="margin-top:30px;" id="ha-switch-id">
                  <ha-switch
                    .checked=${"on"===this.hass.states["input_boolean.ais_auto_update"].state}
                    @change=${this.changeAutoUpdateMode}
                    style="position: absolute; right: 20px;"
                  ></ha-switch
                  ><span
                    ><h3>
                      Autoaktualizacja
                      <ha-icon
                        icon=${"on"===this.hass.states["input_boolean.ais_auto_update"].state?"mdi:sync":"mdi:sync-off"}
                      ></ha-icon></h3
                  ></span>
                </div>
              </div>

              <div style="display: inline-block; text-align:left;">
                <div>
                  ${"on"===this.hass.states["input_boolean.ais_auto_update"].state?i.dy`Codziennie sprawdzimy i automatycznie zainstalujemy
                      dostępne aktualizacje.`:i.dy`Możesz aktualizować system samodzielnie w dogodnym
                      dla Ciebie czasie lub włączyć aktualizację automatyczną.`}
                </div>
                <div style="margin-top: 15px;">
                  Aktualizacje dostarczają najnowsze funkcjonalności oraz
                  poprawki zapewniające bezpieczeństwo i stabilność działania
                  systemu.
                  <table style="margin-top: 10px;">
                    ${this.hass.states["sensor.version_info"].attributes.update_check_time?i.dy`<tr>
                          <td>
                            <ha-icon icon=""></ha-icon>
                            Sprawdzono o
                          </td>
                          <td>
                            ${this.hass.states["sensor.version_info"].attributes.update_check_time}
                          </td>
                          <td></td>
                          <td><ha-icon icon=""></ha-icon></td>
                        </tr>`:i.dy``}
                    ${this.hass.states["sensor.version_info"].attributes.update_status?i.dy`<tr>
                          <td>
                            <ha-icon icon=""></ha-icon>
                            Status
                          </td>
                          <td>
                            ${this.getVersionName(this.hass.states["sensor.version_info"].attributes.update_status)}
                          </td>
                          <td></td>
                          <td>
                            <ha-icon
                              icon=${this.getVersionIcon(this.hass.states["sensor.version_info"].attributes.update_status)}
                            ></ha-icon>
                          </td>
                        </tr>`:i.dy``}
                    <tr style="height: 1em;"></tr>
                    ${this.hass.states["sensor.version_info"].attributes.zigbee2mqtt_current_version?i.dy`<tr>
                          <td>
                            <ha-icon icon="mdi:zigbee"></ha-icon>
                            Zigbee
                          </td>
                          <td>
                            ${this.hass.states["sensor.version_info"].attributes.zigbee2mqtt_current_version}
                          </td>
                          <td>
                            ${this.hass.states["sensor.version_info"].attributes.zigbee2mqtt_newest_version}
                          </td>
                          <td>
                            <ha-icon
                              icon=${this.hass.states["sensor.version_info"].attributes.reinstall_zigbee2mqtt?"hass:alert":"hass:check"}
                            ></ha-icon>
                          </td>
                        </tr>`:i.dy``}
                    ${this.hass.states["sensor.version_info"].attributes.zigbee2mqtt_current_version?i.dy`<tr>
                          <td>
                            <ha-icon icon="mdi:home-assistant"></ha-icon>
                            AIS HA
                          </td>
                          <td>
                            ${this.hass.states["sensor.version_info"].attributes.dom_app_current_version}
                          </td>
                          <td>
                            ${this.hass.states["sensor.version_info"].attributes.dom_app_newest_version}
                          </td>
                          <td>
                            <ha-icon
                              icon=${this.hass.states["sensor.version_info"].attributes.reinstall_dom_app?"hass:alert":"hass:check"}
                            ></ha-icon>
                          </td>
                        </tr>`:i.dy``}
                    ${this.hass.states["sensor.version_info"].attributes.android_app_current_version?i.dy`<tr>
                          <td>
                            <ha-icon icon="mdi:android"></ha-icon>
                            Android
                          </td>
                          <td>
                            ${this.hass.states["sensor.version_info"].attributes.android_app_current_version}
                          </td>
                          <td>
                            ${this.hass.states["sensor.version_info"].attributes.android_app_newest_version}
                          </td>
                          <td>
                            <ha-icon
                              icon=${this.hass.states["sensor.version_info"].attributes.reinstall_android_app?"hass:alert":"hass:check"}
                            ></ha-icon>
                          </td>
                        </tr>`:i.dy``}
                    ${this.hass.states["sensor.version_info"].attributes.linux_apt_current_version?i.dy`<tr>
                          <td>
                            <ha-icon icon="mdi:linux"></ha-icon>
                            Linux
                          </td>
                          <td>
                            ${this.hass.states["sensor.version_info"].attributes.linux_apt_current_version}
                          </td>
                          <td>
                            ${this.hass.states["sensor.version_info"].attributes.linux_apt_newest_version}
                          </td>
                          <td>
                            <ha-icon
                              icon=${this.hass.states["sensor.version_info"].attributes.reinstall_linux_apt?"hass:alert":"hass:check"}
                            ></ha-icon>
                          </td>
                        </tr>`:i.dy``}
                  </table>
                </div>
              </div>

              ${this._showUpdateButton(this.hass.states["sensor.version_info"])?i.dy` <div class="center-container">
                    <ha-call-service-button
                      class="warning"
                      .hass=${this.hass}
                      domain="ais_updater"
                      service="execute_upgrade"
                      .serviceData=${{say:!0}}
                    >
                      ${this._computeAisButtonVersionCheckUpgrade(this.hass.states["sensor.version_info"])}
                    </ha-call-service-button>
                  </div>`:i.dy`
                    <br /><br /><br />
                    ${this.hass.states["sensor.version_info"].attributes.progress?i.dy` <mwc-linear-progress
                          determinate
                          .progress=${this.hass.states["sensor.version_info"].attributes.progress}
                          .buffer=${this.hass.states["sensor.version_info"].attributes.buffer}
                        >
                        </mwc-linear-progress>`:i.dy`<mwc-linear-progress indeterminate>
                        </mwc-linear-progress>`}
                    <br />
                  `}
            </div>
          </ha-card>

          <ha-card header="Kopia konfiguracji Bramki">
            <div class="card-content">
              W tym miejscu możesz, sprawdzić poprawność ustawień bramki,
              wykonać jej kopię i przesłać ją do portalu integratora.
              <b
                >Uwaga, ponieważ konfiguracja może zawierać hasła i tokeny
                dostępu do usług, zalecamy zaszyfrować ją hasłem</b
              >. Gdy kopia jest zabezpieczona hasłem, to można ją
              otworzyć/przywrócić tylko po podaniu hasła.
              <h2>
                Nowa kopia ustawień
                <ha-icon icon="mdi:cloud-upload-outline"></ha-icon>
              </h2>
              <br />
              <div class="center-container">
                Kopia zapasowa ustawień:
                <br />
                <div class="backup-types" id="backup_type1">
                  <ha-formfield name="all" label="Wszystkich">
                    <ha-radio
                      name="bt"
                      @change=${this._handleBackupTypeValueChanged}
                      value="all"
                      .checked=${"all"===this.backupType}
                    >
                    </ha-radio>
                  </ha-formfield>
                  <ha-formfield name="ha" label="AIS HA">
                    <ha-radio
                      name="bt"
                      @change=${this._handleBackupTypeValueChanged}
                      value="ha"
                      .checked=${"ha"===this.backupType}
                    >
                    </ha-radio>
                  </ha-formfield>
                  <ha-formfield name="zigbee" label="Zigbee">
                    <ha-radio
                      name="bt"
                      @change=${this._handleBackupTypeValueChanged}
                      value="zigbee"
                      .checked=${"zigbee"===this.backupType}
                    >
                    </ha-radio>
                  </ha-formfield>
                </div>
                Przed wykonaniem nowej kopii ustawień sprawdź poprawność
                konfiguracji
              </div>
              <br />
              <div>
                ${this.validateLog?i.dy`<div class="config-invalid">
                        <mwc-button raised="" @click=${this.doBackup}>
                          Popraw i sprawdź ponownie
                        </mwc-button>
                      </div>
                      <p></p>
                      <div id="configLog" class="validate-log">
                        ${this.validateLog}
                      </div>`:i.dy` <div class="validate-container">
                      <div class="validate-result" id="result">
                        ${this.hass.states["sensor.ais_backup_info"].attributes.backup_info}
                      </div>

                      ${this.validateConfigInProgress?i.dy`<mwc-linear-progress indeterminate>
                          </mwc-linear-progress>`:i.dy` <div class="config-invalid">
                              <span class="text">
                                ${this.hass.states["sensor.ais_backup_info"].attributes.backup_error}
                              </span>
                            </div>
                            ${"1"===this.hass.states["sensor.ais_backup_info"].state?i.dy`
                                  <paper-input
                                    placeholder="hasło"
                                    no-label-float=""
                                    type="password"
                                    id="password1"
                                  ></paper-input>
                                `:i.dy``}
                            <mwc-button raised="" @click=${this.doBackup}>
                              ${"0"===this.hass.states["sensor.ais_backup_info"].state?i.dy` Sprawdź konfigurację `:i.dy``}
                              ${"1"===this.hass.states["sensor.ais_backup_info"].state?i.dy` Wykonaj kopie konfiguracji `:i.dy``}
                            </mwc-button>`}
                    </div>`}
              </div>
              ${this.hass.states["sensor.ais_backup_info"].attributes.file_size||this.hass.states["sensor.ais_backup_info"].attributes.file_zigbee_size?i.dy` <h2>
                      Przywracanie ustawień z kopii
                      <ha-icon icon="mdi:cloud-download-outline"></ha-icon>
                    </h2>
                    W tym miejscu możesz, przywrócić ustawienia bramki z kopii,
                    która zostanie pobrana z portalu integratora. Jeśli
                    zaszyfrowałeś kopię hasłem, to podaj je przed wykonaniem
                    przywracania ustawień z kopii.
                    <div class="validate-container">
                      <table style="margin-top: 40px; margin-bottom: 10px;">
                        ${this.hass.states["sensor.ais_backup_info"].attributes.file_size?i.dy` <tr>
                              <td>
                                <ha-icon icon="mdi:home-assistant"></ha-icon>
                                AIS HA
                              </td>
                              <td>
                                ${this.hass.states["sensor.ais_backup_info"].attributes.file_name}
                              </td>
                              <td>
                                ${this.hass.states["sensor.ais_backup_info"].attributes.file_size}
                              </td>
                            </tr>`:i.dy``}
                        ${this.hass.states["sensor.ais_backup_info"].attributes.file_zigbee_size?i.dy` <tr>
                              <td>
                                <ha-icon icon="mdi:zigbee"></ha-icon>
                                Zigbee
                              </td>
                              <td>
                                ${this.hass.states["sensor.ais_backup_info"].attributes.file_zigbee_name}
                              </td>
                              <td>
                                ${this.hass.states["sensor.ais_backup_info"].attributes.file_zigbee_size}
                              </td>
                            </tr>`:i.dy``}
                      </table>
                      <div class="validate-container">
                        <div class="validate-result" id="result">
                          ${this.hass.states["sensor.ais_backup_info"].attributes.restore_info}
                        </div>
                        <div class="config-invalid">
                          <span class="text">
                            ${this.hass.states["sensor.ais_backup_info"].attributes.restore_error}
                          </span>
                        </div>
                        Przywracanie ustawień z kopii:
                        <div class="center-container">
                          <div class="backup-types" id="backup_type2">
                            ${this.hass.states["sensor.ais_backup_info"].attributes.file_size&&this.hass.states["sensor.ais_backup_info"].attributes.file_zigbee_size?i.dy` <ha-formfield
                                  name="all"
                                  label="Wszystkich"
                                >
                                  <ha-radio
                                    name="bt2"
                                    @change=${this._handleBackupType2ValueChanged}
                                    value="all"
                                    .checked=${"all"===this.backupType2}
                                  >
                                  </ha-radio>
                                </ha-formfield>`:i.dy``}
                            ${this.hass.states["sensor.ais_backup_info"].attributes.file_size?i.dy` <ha-formfield name="ha" label="AIS HA">
                                  <ha-radio
                                    name="bt2"
                                    @change=${this._handleBackupType2ValueChanged}
                                    value="ha"
                                    .checked=${"ha"===this.backupType2}
                                  >
                                  </ha-radio>
                                </ha-formfield>`:i.dy``}
                            ${this.hass.states["sensor.ais_backup_info"].attributes.file_zigbee_size?i.dy` <ha-formfield
                                  name="zigbee"
                                  label="Zigbee"
                                >
                                  <ha-radio
                                    name="bt2"
                                    @change=${this._handleBackupType2ValueChanged}
                                    value="zigbee"
                                    .checked=${"zigbee"===this.backupType2}
                                  >
                                  </ha-radio>
                                </ha-formfield>`:i.dy``}
                          </div>
                          <paper-input
                            placeholder="hasło"
                            no-label-float=""
                            type="password"
                            id="password2"
                          ></paper-input>
                          <mwc-button raised="" @click=${this.restoreBackup}>
                            Przywróć konfigurację z kopii
                          </mwc-button>
                        </div>
                      </div>
                    </div>`:i.dy``}
            </div>
          </ha-card>

          <ha-card header="Synchronizacja z Portalem Integratora">
            <div class="card-content">
              Jeśli ostatnio wprowadzałeś zmiany w Portalu Integratora, takie
              jak dodanie nowych typów audio czy też dostęp do zewnętrznych
              serwisów, to przyciskiem poniżej możesz uruchomić natychmiastowe
              pobranie tych zmian na bramkę bez czekania na automatyczną
              synchronizację.
              <div class="center-container">
                <ha-call-service-button
                  class="warning"
                  .hass=${this.hass}
                  domain="script"
                  service="ais_cloud_sync"
                  >Synchronizuj z Portalem Integratora
                </ha-call-service-button>
              </div>
            </div>
          </ha-card>
        </ha-config-section>
      </hass-subpage>
    `}},{kind:"get",static:!0,key:"styles",value:function(){return[s.Qx,i.iv`
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
        .center-container {
          text-align: center;
          min-height: 70px;
        }
        table {
          width: 100%;
        }

        td:first-child {
          width: 33%;
        }

        .validate-container {
          text-align: center;
          min-height: 140px;
        }

        .validate-result {
          color: #0da035;
        }

        .config-invalid {
          text-align: center;
          color: #f44336;
        }

        .validate-log {
          white-space: pre-wrap;
          direction: ltr;
          color: #f44336;
        }
        img.versionLogo {
          max-width: 30%;
        }
      `]}},{kind:"method",key:"getVersionName",value:function(e){let t=e;return"checking"===e?t="Sprawdzanie":"outdated"===e?t="Nieaktualny":"downloading"===e?t="Pobieranie":"installing"===e?t="Instalowanie":"updated"===e?t="Aktualny":"unknown"===e?t="Nieznany":"restart"===e&&(t="Restartowanie"),t}},{kind:"method",key:"getVersionIcon",value:function(e){let t="";return"checking"===e?t="mdi:cloud-sync":"outdated"===e?t="mdi:clock-alert-outline":"downloading"===e?t="mdi:progress-download":"installing"===e?t="mdi:progress-wrench":"updated"===e?t="mdi:emoticon-happy-outline":"unknown"===e?t="mdi:help-circle-outline":"restart"===e&&(t="mdi:restart-alert"),t}},{kind:"method",key:"_handleBackupTypeValueChanged",value:function(e){const t=e.currentTarget;this.backupType=t.value}},{kind:"method",key:"_handleBackupType2ValueChanged",value:function(e){const t=e.currentTarget;this.backupType2=t.value}},{kind:"method",key:"_computeAisButtonVersionCheckUpgrade",value:function(e){const t=e.attributes;return t.reinstall_dom_app||t.reinstall_android_app||t.reinstall_linux_apt||t.reinstall_zigbee2mqtt?"outdated"===t.update_status?"Zainstaluj teraz aktualizację":"unknown"===t.update_status?"Spróbuj ponownie":"Aktualizacja -> "+this.getVersionName(t.update_status):"Sprawdź dostępność aktualizacji"}},{kind:"method",key:"_showUpdateButton",value:function(e){const t=e.attributes;return!(t.reinstall_dom_app||t.reinstall_android_app||t.reinstall_linux_apt||t.reinstall_zigbee2mqtt)||("outdated"===t.update_status||"unknown"===t.update_status)}},{kind:"method",key:"_getTextColor",value:function(e){const t=e.attributes;return t.reinstall_dom_app||t.reinstall_android_app||t.reinstall_linux_apt||t.reinstall_zigbee2mqtt?"outdated"===t.update_status?"#f44336":(t.update_status,"#ff9800"):"#0da035"}},{kind:"method",key:"changeAutoUpdateMode",value:function(){this.hass.callService("input_boolean","toggle",{entity_id:"input_boolean.ais_auto_update"})}},{kind:"method",key:"isBackupInProgress",value:function(e){return"0"!==e.state}},{kind:"method",key:"doBackup",value:function(){if("0"===this.hass.states["sensor.ais_backup_info"].state)this.validateConfigInProgress=!0,this.validateLog="",this.hass.callApi("POST","config/core/check_config").then((e=>{this.validateConfigInProgress=!1;const t="valid"===e.result?"1":"0";"0"===t?(this.hass.callService("ais_cloud","set_backup_step",{step:t,backup_error:"Konfiguracja niepoprawna"}),this.validateLog=e.errors):(this.hass.callService("ais_cloud","set_backup_step",{step:t,backup_info:"Konfiguracja poprawna można wykonać kopię"}),this.validateLog="")}));else{this.validateLog="";const e=this.shadowRoot.getElementById("password1").value,t=this.backupType;this.hass.callService("ais_cloud","do_backup",{password:e,type:t})}}},{kind:"method",key:"restoreBackup",value:function(){this.validateLog="";const e=this.shadowRoot.getElementById("password2").value,t=this.backupType2;this.hass.callService("ais_cloud","restore_backup",{password:e,type:t})}}]}}),i.oi)}}]);
//# sourceMappingURL=ec4de832.js.map
/*! For license information please see c31e320d.js.LICENSE.txt */
"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[90020,40967],{14166:(e,t,i)=>{i.d(t,{W:()=>n});var r=function(){return r=Object.assign||function(e){for(var t,i=1,r=arguments.length;i<r;i++)for(var n in t=arguments[i])Object.prototype.hasOwnProperty.call(t,n)&&(e[n]=t[n]);return e},r.apply(this,arguments)};function n(e,t,i){void 0===t&&(t=Date.now()),void 0===i&&(i={});var n=r(r({},o),i||{}),s=(+e-+t)/1e3;if(Math.abs(s)<n.second)return{value:Math.round(s),unit:"second"};var a=s/60;if(Math.abs(a)<n.minute)return{value:Math.round(a),unit:"minute"};var l=s/3600;if(Math.abs(l)<n.hour)return{value:Math.round(l),unit:"hour"};var c=s/86400;if(Math.abs(c)<n.day)return{value:Math.round(c),unit:"day"};var d=new Date(e),h=new Date(t),u=d.getFullYear()-h.getFullYear();if(Math.round(Math.abs(u))>0)return{value:Math.round(u),unit:"year"};var p=12*u+d.getMonth()-h.getMonth();if(Math.round(Math.abs(p))>0)return{value:Math.round(p),unit:"month"};var f=s/604800;return{value:Math.round(f),unit:"week"}}var o={second:45,minute:45,hour:22,day:5}},63207:(e,t,i)=>{i(65660),i(15112);var r=i(9672),n=i(87156),o=i(50856),s=i(10994);(0,r.k)({_template:o.d`
    <style>
      :host {
        @apply --layout-inline;
        @apply --layout-center-center;
        position: relative;

        vertical-align: middle;

        fill: var(--iron-icon-fill-color, currentcolor);
        stroke: var(--iron-icon-stroke-color, none);

        width: var(--iron-icon-width, 24px);
        height: var(--iron-icon-height, 24px);
        @apply --iron-icon;
      }

      :host([hidden]) {
        display: none;
      }
    </style>
`,is:"iron-icon",properties:{icon:{type:String},theme:{type:String},src:{type:String},_meta:{value:s.XY.create("iron-meta",{type:"iconset"})}},observers:["_updateIcon(_meta, isAttached)","_updateIcon(theme, isAttached)","_srcChanged(src, isAttached)","_iconChanged(icon, isAttached)"],_DEFAULT_ICONSET:"icons",_iconChanged:function(e){var t=(e||"").split(":");this._iconName=t.pop(),this._iconsetName=t.pop()||this._DEFAULT_ICONSET,this._updateIcon()},_srcChanged:function(e){this._updateIcon()},_usesIconset:function(){return this.icon||!this.src},_updateIcon:function(){this._usesIconset()?(this._img&&this._img.parentNode&&(0,n.vz)(this.root).removeChild(this._img),""===this._iconName?this._iconset&&this._iconset.removeIcon(this):this._iconsetName&&this._meta&&(this._iconset=this._meta.byKey(this._iconsetName),this._iconset?(this._iconset.applyIcon(this,this._iconName,this.theme),this.unlisten(window,"iron-iconset-added","_updateIcon")):this.listen(window,"iron-iconset-added","_updateIcon"))):(this._iconset&&this._iconset.removeIcon(this),this._img||(this._img=document.createElement("img"),this._img.style.width="100%",this._img.style.height="100%",this._img.draggable=!1),this._img.src=this.src,(0,n.vz)(this.root).appendChild(this._img))}})},15112:(e,t,i)=>{i.d(t,{P:()=>n});i(10994);var r=i(9672);class n{constructor(e){n[" "](e),this.type=e&&e.type||"default",this.key=e&&e.key,e&&"value"in e&&(this.value=e.value)}get value(){var e=this.type,t=this.key;if(e&&t)return n.types[e]&&n.types[e][t]}set value(e){var t=this.type,i=this.key;t&&i&&(t=n.types[t]=n.types[t]||{},null==e?delete t[i]:t[i]=e)}get list(){if(this.type){var e=n.types[this.type];return e?Object.keys(e).map((function(e){return o[this.type][e]}),this):[]}}byKey(e){return this.key=e,this.value}}n[" "]=function(){},n.types={};var o=n.types;(0,r.k)({is:"iron-meta",properties:{type:{type:String,value:"default"},key:{type:String},value:{type:String,notify:!0},self:{type:Boolean,observer:"_selfChanged"},__meta:{type:Boolean,computed:"__computeMeta(type, key, value)"}},hostAttributes:{hidden:!0},__computeMeta:function(e,t,i){var r=new n({type:e,key:t});return void 0!==i&&i!==r.value?r.value=i:this.value!==r.value&&(this.value=r.value),r},get list(){return this.__meta&&this.__meta.list},_selfChanged:function(e){e&&(this.value=this)},byKey:function(e){return new n({type:this.type,key:e}).value}})},66386:(e,t,i)=>{i.d(t,{GQ:()=>o});const r=window.localStorage||{};let n=window.__tokenCache;function o(){if(void 0===n.tokens)try{delete r.tokens;const e=r.hassTokens;e?(n.tokens=JSON.parse(e),n.writeEnabled=!0):n.tokens=null}catch(e){n.tokens=null}return n.tokens}n||(n=window.__tokenCache={tokens:void 0,writeEnabled:void 0})},43986:(e,t,i)=>{i.d(t,{Z:()=>n,L:()=>o});var r=i(91168);const n={s:1,min:60,h:3600,d:86400},o=(e,t)=>(0,r.Z)(parseFloat(e)*n[t])||"0"},12198:(e,t,i)=>{i.a(e,(async e=>{i.d(t,{D_:()=>o,p6:()=>a,WB:()=>c,mn:()=>h,NC:()=>p,Nh:()=>m,yQ:()=>v});var r=i(14516),n=i(54121);n.Xp&&await n.Xp;const o=(e,t)=>s(t).format(e),s=(0,r.Z)((e=>new Intl.DateTimeFormat(e.language,{weekday:"long",month:"long",day:"numeric"}))),a=(e,t)=>l(t).format(e),l=(0,r.Z)((e=>new Intl.DateTimeFormat(e.language,{year:"numeric",month:"long",day:"numeric"}))),c=(e,t)=>d(t).format(e),d=(0,r.Z)((e=>new Intl.DateTimeFormat(e.language,{year:"numeric",month:"numeric",day:"numeric"}))),h=(e,t)=>u(t).format(e),u=(0,r.Z)((e=>new Intl.DateTimeFormat(e.language,{day:"numeric",month:"short"}))),p=(e,t)=>f(t).format(e),f=(0,r.Z)((e=>new Intl.DateTimeFormat(e.language,{month:"long",year:"numeric"}))),m=(e,t)=>y(t).format(e),y=(0,r.Z)((e=>new Intl.DateTimeFormat(e.language,{month:"long"}))),v=(e,t)=>g(t).format(e),g=(0,r.Z)((e=>new Intl.DateTimeFormat(e.language,{year:"numeric"})));e()}),1)},44583:(e,t,i)=>{i.a(e,(async e=>{i.d(t,{o0:()=>s,E8:()=>l});var r=i(14516),n=i(65810),o=i(54121);o.Xp&&await o.Xp;const s=(e,t)=>a(t).format(e),a=(0,r.Z)((e=>new Intl.DateTimeFormat("en"!==e.language||(0,n.y)(e)?e.language:"en-u-hc-h23",{year:"numeric",month:"long",day:"numeric",hour:(0,n.y)(e)?"numeric":"2-digit",minute:"2-digit",hour12:(0,n.y)(e)}))),l=(e,t)=>c(t).format(e),c=(0,r.Z)((e=>new Intl.DateTimeFormat("en"!==e.language||(0,n.y)(e)?e.language:"en-u-hc-h23",{year:"numeric",month:"long",day:"numeric",hour:(0,n.y)(e)?"numeric":"2-digit",minute:"2-digit",second:"2-digit",hour12:(0,n.y)(e)})));(0,r.Z)((e=>new Intl.DateTimeFormat("en"!==e.language||(0,n.y)(e)?e.language:"en-u-hc-h23",{year:"numeric",month:"numeric",day:"numeric",hour:"numeric",minute:"2-digit",hour12:(0,n.y)(e)})));e()}),1)},49684:(e,t,i)=>{i.a(e,(async e=>{i.d(t,{mr:()=>s,Vu:()=>l,xO:()=>d});var r=i(14516),n=i(65810),o=i(54121);o.Xp&&await o.Xp;const s=(e,t)=>a(t).format(e),a=(0,r.Z)((e=>new Intl.DateTimeFormat("en"!==e.language||(0,n.y)(e)?e.language:"en-u-hc-h23",{hour:"numeric",minute:"2-digit",hour12:(0,n.y)(e)}))),l=(e,t)=>c(t).format(e),c=(0,r.Z)((e=>new Intl.DateTimeFormat("en"!==e.language||(0,n.y)(e)?e.language:"en-u-hc-h23",{hour:(0,n.y)(e)?"numeric":"2-digit",minute:"2-digit",second:"2-digit",hour12:(0,n.y)(e)}))),d=(e,t)=>h(t).format(e),h=(0,r.Z)((e=>new Intl.DateTimeFormat("en"!==e.language||(0,n.y)(e)?e.language:"en-u-hc-h23",{weekday:"long",hour:(0,n.y)(e)?"numeric":"2-digit",minute:"2-digit",hour12:(0,n.y)(e)})));e()}),1)},42141:(e,t,i)=>{function r(e){return void 0===e||Array.isArray(e)?e:[e]}i.d(t,{r:()=>r})},34007:(e,t,i)=>{i.d(t,{N:()=>n});const r=[" ",": "],n=(e,t)=>{const i=e.toLowerCase();for(const n of r){const r=`${t}${n}`;if(i.startsWith(r)){const t=e.substring(r.length);return o(t.substr(0,t.indexOf(" ")))?t:t[0].toUpperCase()+t.slice(1)}}},o=e=>e.toLowerCase()!==e},83447:(e,t,i)=>{i.d(t,{l:()=>r});const r=(e,t="_")=>{const i="àáäâãåăæąçćčđďèéěėëêęğǵḧìíïîįłḿǹńňñòóöôœøṕŕřßşśšșťțùúüûǘůűūųẃẍÿýźžż·/_,:;",r=`aaaaaaaaacccddeeeeeeegghiiiiilmnnnnooooooprrsssssttuuuuuuuuuwxyyzzz${t}${t}${t}${t}${t}${t}`,n=new RegExp(i.split("").join("|"),"g");return e.toString().toLowerCase().replace(/\s+/g,t).replace(n,(e=>r.charAt(i.indexOf(e)))).replace(/&/g,`${t}and${t}`).replace(/[^\w-]+/g,"").replace(/-/g,t).replace(new RegExp(`(${t})\\1+`,"g"),"$1").replace(new RegExp(`^${t}+`),"").replace(new RegExp(`${t}+$`),"")}},92306:(e,t,i)=>{i.d(t,{v:()=>r});const r=(e,t)=>{const i={};for(const r of e){const e=t(r);e in i?i[e].push(r):i[e]=[r]}return i}},8330:(e,t,i)=>{i.d(t,{P:()=>r});const r=(e,t,i=!0,r=!0)=>{let n,o=0;const s=(...s)=>{const a=()=>{o=!1===i?0:Date.now(),n=void 0,e(...s)},l=Date.now();o||!1!==i||(o=l);const c=t-(l-o);c<=0||c>t?(n&&(clearTimeout(n),n=void 0),o=l,e(...s)):n||!1===r||(n=window.setTimeout(a,c))};return s.cancel=()=>{clearTimeout(n),n=void 0,o=0},s}},57793:(e,t,i)=>{var r=i(37500),n=i(33310),o=i(44634);i(52039);function s(){s=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(i){t.forEach((function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach((function(r){t.forEach((function(t){var n=t.placement;if(t.kind===r&&("static"===n||"prototype"===n)){var o="static"===n?e:i;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var r=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],r=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!c(e))return i.push(e);var t=this.decorateElement(e,n);i.push(t.element),i.push.apply(i,t.extras),r.push.apply(r,t.finishers)}),this),!t)return{elements:i,finishers:r};var o=this.decorateConstructor(i,t);return r.push.apply(r,o.finishers),o.finishers=r,o},addElementPlacement:function(e,t,i){var r=t[e.placement];if(!i&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var i=[],r=[],n=e.decorators,o=n.length-1;o>=0;o--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,n[o])(a)||a);e=l.element,this.addElementPlacement(e,t),l.finisher&&r.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);i.push.apply(i,c)}}return{element:e,finishers:r,extras:i}},decorateConstructor:function(e,t){for(var i=[],r=t.length-1;r>=0;r--){var n=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[r])(n)||n);if(void 0!==o.finisher&&i.push(o.finisher),void 0!==o.elements){e=o.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return p(e,t);var i=Object.prototype.toString.call(e).slice(8,-1);return"Object"===i&&e.constructor&&(i=e.constructor.name),"Map"===i||"Set"===i?Array.from(e):"Arguments"===i||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(i)?p(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=u(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:i,placement:r,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:h(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=h(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var r=(0,t[i])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}function a(e){var t,i=u(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function l(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function c(e){return e.decorators&&e.decorators.length}function d(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function h(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function u(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var r=i.call(e,t||"default");if("object"!=typeof r)return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function p(e,t){(null==t||t>e.length)&&(t=e.length);for(var i=0,r=new Array(t);i<t;i++)r[i]=e[i];return r}!function(e,t,i,r){var n=s();if(r)for(var o=0;o<r.length;o++)n=r[o](n);var h=t((function(e){n.initializeInstanceElements(e,u.elements)}),i),u=n.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},r=0;r<e.length;r++){var n,o=e[r];if("method"===o.kind&&(n=t.find(i)))if(d(o.descriptor)||d(n.descriptor)){if(c(o)||c(n))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");n.descriptor=o.descriptor}else{if(c(o)){if(c(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");n.decorators=o.decorators}l(o,n)}else t.push(o)}return t}(h.d.map(a)),e);n.initializeClassElements(h.F,u.elements),n.runClassFinishers(h.F,u.finishers)}([(0,n.Mo)("ha-battery-icon")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.Cb)()],key:"batteryStateObj",value:void 0},{kind:"field",decorators:[(0,n.Cb)()],key:"batteryChargingStateObj",value:void 0},{kind:"method",key:"render",value:function(){return r.dy`
      <ha-svg-icon
        .path=${(0,o.$)(this.batteryStateObj,this.batteryChargingStateObj)}
      ></ha-svg-icon>
    `}}]}}),r.oi)},99282:(e,t,i)=>{var r=i(52039);class n extends r.C{connectedCallback(){super.connectedCallback(),setTimeout((()=>{this.path="ltr"===window.getComputedStyle(this).direction?"M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z":"M15.41,16.58L10.83,12L15.41,7.41L14,6L8,12L14,18L15.41,16.58Z"}),100)}}customElements.define("ha-icon-next",n)},57066:(e,t,i)=>{i.d(t,{Lo:()=>s,IO:()=>a,qv:()=>l,sG:()=>h});var r=i(97330),n=i(85415),o=i(38346);const s=(e,t)=>e.callWS({type:"config/area_registry/create",...t}),a=(e,t,i)=>e.callWS({type:"config/area_registry/update",area_id:t,...i}),l=(e,t)=>e.callWS({type:"config/area_registry/delete",area_id:t}),c=e=>e.sendMessagePromise({type:"config/area_registry/list"}).then((e=>e.sort(((e,t)=>(0,n.$)(e.name,t.name))))),d=(e,t)=>e.subscribeEvents((0,o.D)((()=>c(e).then((e=>t.setState(e,!0)))),500,!0),"area_registry_updated"),h=(e,t)=>(0,r.B)("_areaRegistry",c,d,e,t)},22814:(e,t,i)=>{i.d(t,{iI:()=>r,W2:()=>n,TZ:()=>o});location.protocol,location.host;const r=(e,t)=>e.callWS({type:"auth/sign_path",path:t}),n=async(e,t,i,r)=>e.callWS({type:"config/auth_provider/homeassistant/create",user_id:t,username:i,password:r}),o=async(e,t,i)=>e.callWS({type:"config/auth_provider/homeassistant/admin_change_password",user_id:t,password:i})},57292:(e,t,i)=>{i.d(t,{jL:()=>a,t1:()=>l,dl:()=>c,q4:()=>u,Wg:()=>p});var r=i(97330),n=i(91741),o=i(85415),s=i(38346);const a=(e,t,i)=>e.name_by_user||e.name||i&&((e,t)=>{for(const i of t||[]){const t="string"==typeof i?i:i.entity_id,r=e.states[t];if(r)return(0,n.C)(r)}})(t,i)||t.localize("ui.panel.config.devices.unnamed_device","type",t.localize(`ui.panel.config.devices.type.${e.entry_type||"device"}`)),l=(e,t,i)=>e.callWS({type:"config/device_registry/update",device_id:t,...i}),c=(e,t,i)=>e.callWS({type:"config/device_registry/remove_config_entry",device_id:t,config_entry_id:i}),d=e=>e.sendMessagePromise({type:"config/device_registry/list"}),h=(e,t)=>e.subscribeEvents((0,s.D)((()=>d(e).then((e=>t.setState(e,!0)))),500,!0),"device_registry_updated"),u=(e,t)=>(0,r.B)("_dr",d,h,e,t),p=e=>e.sort(((e,t)=>(0,o.f)(e.name||"",t.name||"")))},42916:(e,t,i)=>{i.d(t,{pD:()=>r,lf:()=>n,iP:()=>o,ZK:()=>s});const r=e=>e.callWS({type:"diagnostics/list"}),n=(e,t)=>e.callWS({type:"diagnostics/get",domain:t}),o=e=>`/api/diagnostics/config_entry/${e}`,s=(e,t)=>`/api/diagnostics/config_entry/${e}/device/${t}`},15327:(e,t,i)=>{i.d(t,{eL:()=>r,SN:()=>n,id:()=>o,fg:()=>s,j2:()=>a,JR:()=>l,Y:()=>c,iM:()=>d,Q2:()=>h,Oh:()=>u,vj:()=>p,Gc:()=>f});const r=e=>e.sendMessagePromise({type:"lovelace/resources"}),n=(e,t)=>e.callWS({type:"lovelace/resources/create",...t}),o=(e,t,i)=>e.callWS({type:"lovelace/resources/update",resource_id:t,...i}),s=(e,t)=>e.callWS({type:"lovelace/resources/delete",resource_id:t}),a=e=>e.callWS({type:"lovelace/dashboards/list"}),l=(e,t)=>e.callWS({type:"lovelace/dashboards/create",...t}),c=(e,t,i)=>e.callWS({type:"lovelace/dashboards/update",dashboard_id:t,...i}),d=(e,t)=>e.callWS({type:"lovelace/dashboards/delete",dashboard_id:t}),h=(e,t,i)=>e.sendMessagePromise({type:"lovelace/config",url_path:t,force:i}),u=(e,t,i)=>e.callWS({type:"lovelace/config/save",url_path:t,config:i}),p=(e,t)=>e.callWS({type:"lovelace/config/delete",url_path:t}),f=(e,t,i)=>e.subscribeEvents((e=>{e.data.url_path===t&&i()}),"lovelace_updated")},9893:(e,t,i)=>{i.d(t,{Qo:()=>r,kb:()=>o,cs:()=>s});const r="custom:",n=window;"customCards"in n||(n.customCards=[]);const o=n.customCards,s=e=>o.find((t=>t.type===e))},94449:(e,t,i)=>{i.d(t,{K:()=>r});const r=(e,t,i)=>e.callWS({type:"search/related",item_type:t,item_id:i})},24833:(e,t,i)=>{i.d(t,{oF:()=>d,kK:()=>h,k6:()=>u,zG:()=>p,BD:()=>f,hF:()=>y,Sk:()=>v,X4:()=>g,UJ:()=>b,Fj:()=>k,M$:()=>_});var r=i(49706),n=i(58831),o=i(22311),s=i(40095),a=i(85415),l=i(26765),c=i(81796);const d=1,h=2,u=4,p=8,f=16,m=e=>(0,s.f)(e,u)&&"number"==typeof e.in_progress,y=(e,t=!1)=>(e.state===r.uo||t&&Boolean(e.attributes.skipped_version))&&(0,s.e)(e,d),v=e=>(e=>m(e.attributes))(e)||!!e.attributes.in_progress,g=e=>m(e)||!!e.in_progress,b=(e,t)=>e.callWS({type:"update/release_notes",entity_id:t}),w=e=>Object.values(e).filter((e=>"update"===(0,o.N)(e))).sort(((e,t)=>"Home Assistant Core"===e.attributes.title?-3:"Home Assistant Core"===t.attributes.title?3:"Home Assistant Operating System"===e.attributes.title?-2:"Home Assistant Operating System"===t.attributes.title?2:"Home Assistant Supervisor"===e.attributes.title?-1:"Home Assistant Supervisor"===t.attributes.title?1:(0,a.f)(e.attributes.title||e.attributes.friendly_name||"",t.attributes.title||t.attributes.friendly_name||""))),k=(e,t=!1)=>w(e).filter((e=>y(e,t))),_=async(e,t)=>{const i=w(t.states).map((e=>e.entity_id));if(!i.length)return void(0,l.Ys)(e,{title:t.localize("ui.panel.config.updates.no_update_entities.title"),text:t.localize("ui.panel.config.updates.no_update_entities.description"),warning:!0});let r=0;const o=await t.connection.subscribeEvents((i=>{"update"===(0,n.M)(i.data.entity_id)&&(r++,(0,c.C)(e,{message:t.localize("ui.panel.config.updates.updates_refreshed",{count:r})}))}),"state_changed");await t.callService("homeassistant","update_entity",{entity_id:i}),await new Promise((e=>setTimeout(e,1e4))),o(),0===r&&(0,c.C)(e,{message:t.localize("ui.panel.config.updates.no_new_updates")})}},65253:(e,t,i)=>{i.d(t,{Pb:()=>r,CE:()=>n,uh:()=>o,r4:()=>s,Nq:()=>a,h8:()=>l,fm:()=>c,FH:()=>f});const r="system-admin",n="system-users",o=async e=>e.callWS({type:"config/auth/list"}),s=async(e,t,i,r)=>e.callWS({type:"config/auth/create",name:t,group_ids:i,local_only:r}),a=async(e,t,i)=>e.callWS({...i,type:"config/auth/update",user_id:t}),l=async(e,t)=>e.callWS({type:"config/auth/delete",user_id:t}),c=e=>e?e.trim().split(" ").slice(0,3).map((e=>e.substring(0,1))).join(""):"?",d=32143==i.j?"M12 2C6.47 2 2 6.5 2 12C2 17.5 6.5 22 12 22S22 17.5 22 12 17.5 2 12 2M12 20C7.58 20 4 16.42 4 12C4 7.58 7.58 4 12 4S20 7.58 20 12C20 16.42 16.42 20 12 20M8 14L7 8L10 10L12 7L14 10L17 8L16 14H8M8.56 16C8.22 16 8 15.78 8 15.44V15H16V15.44C16 15.78 15.78 16 15.44 16H8.56Z":null,h=32143==i.j?"M11,7H15V9H11V11H13A2,2 0 0,1 15,13V15A2,2 0 0,1 13,17H9V15H13V13H11A2,2 0 0,1 9,11V9A2,2 0 0,1 11,7M12,2A10,10 0 0,1 22,12A10,10 0 0,1 12,22A10,10 0 0,1 2,12A10,10 0 0,1 12,2M12,4A8,8 0 0,0 4,12A8,8 0 0,0 12,20A8,8 0 0,0 20,12A8,8 0 0,0 12,4Z":null,u=32143==i.j?"M12 20C7.6 20 4 16.4 4 12S7.6 4 12 4 20 7.6 20 12 16.4 20 12 20M12 2C6.5 2 2 6.5 2 12S6.5 22 12 22 22 17.5 22 12 17.5 2 12 2M11 14H13V17H16V12H18L12 7L6 12H8V17H11V14":null,p=32143==i.j?"M12 2C17.5 2 22 6.5 22 12S17.5 22 12 22 2 17.5 2 12 6.5 2 12 2M12 4C10.1 4 8.4 4.6 7.1 5.7L18.3 16.9C19.3 15.5 20 13.8 20 12C20 7.6 16.4 4 12 4M16.9 18.3L5.7 7.1C4.6 8.4 4 10.1 4 12C4 16.4 7.6 20 12 20C13.9 20 15.6 19.4 16.9 18.3Z":null,f=(e,t,i)=>{const r=[],n=t=>e.localize(`ui.panel.config.users.${t}`);return t.is_owner&&r.push([d,n("is_owner")]),i&&t.system_generated&&r.push([h,n("is_system")]),t.local_only&&r.push([u,n("is_local")]),t.is_active||r.push([p,n("is_not_active")]),r}},60010:(e,t,i)=>{var r=i(37500),n=i(33310),o=i(25516);i(2315),i(48932);function s(){s=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(i){t.forEach((function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach((function(r){t.forEach((function(t){var n=t.placement;if(t.kind===r&&("static"===n||"prototype"===n)){var o="static"===n?e:i;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var r=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],r=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!c(e))return i.push(e);var t=this.decorateElement(e,n);i.push(t.element),i.push.apply(i,t.extras),r.push.apply(r,t.finishers)}),this),!t)return{elements:i,finishers:r};var o=this.decorateConstructor(i,t);return r.push.apply(r,o.finishers),o.finishers=r,o},addElementPlacement:function(e,t,i){var r=t[e.placement];if(!i&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var i=[],r=[],n=e.decorators,o=n.length-1;o>=0;o--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,n[o])(a)||a);e=l.element,this.addElementPlacement(e,t),l.finisher&&r.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);i.push.apply(i,c)}}return{element:e,finishers:r,extras:i}},decorateConstructor:function(e,t){for(var i=[],r=t.length-1;r>=0;r--){var n=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[r])(n)||n);if(void 0!==o.finisher&&i.push(o.finisher),void 0!==o.elements){e=o.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return p(e,t);var i=Object.prototype.toString.call(e).slice(8,-1);return"Object"===i&&e.constructor&&(i=e.constructor.name),"Map"===i||"Set"===i?Array.from(e):"Arguments"===i||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(i)?p(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=u(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:i,placement:r,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:h(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=h(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var r=(0,t[i])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}function a(e){var t,i=u(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function l(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function c(e){return e.decorators&&e.decorators.length}function d(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function h(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function u(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var r=i.call(e,t||"default");if("object"!=typeof r)return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function p(e,t){(null==t||t>e.length)&&(t=e.length);for(var i=0,r=new Array(t);i<t;i++)r[i]=e[i];return r}!function(e,t,i,r){var n=s();if(r)for(var o=0;o<r.length;o++)n=r[o](n);var h=t((function(e){n.initializeInstanceElements(e,u.elements)}),i),u=n.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},r=0;r<e.length;r++){var n,o=e[r];if("method"===o.kind&&(n=t.find(i)))if(d(o.descriptor)||d(n.descriptor)){if(c(o)||c(n))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");n.descriptor=o.descriptor}else{if(c(o)){if(c(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");n.decorators=o.decorators}l(o,n)}else t.push(o)}return t}(h.d.map(a)),e);n.initializeClassElements(h.F,u.elements),n.runClassFinishers(h.F,u.finishers)}([(0,n.Mo)("hass-subpage")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.Cb)()],key:"header",value:void 0},{kind:"field",decorators:[(0,n.Cb)({type:Boolean,attribute:"main-page"})],key:"mainPage",value:()=>!1},{kind:"field",decorators:[(0,n.Cb)({type:String,attribute:"back-path"})],key:"backPath",value:void 0},{kind:"field",decorators:[(0,n.Cb)({type:Boolean,reflect:!0})],key:"narrow",value:()=>!1},{kind:"field",decorators:[(0,n.Cb)({type:Boolean})],key:"supervisor",value:()=>!1},{kind:"field",decorators:[(0,o.i)(".content")],key:"_savedScrollPos",value:void 0},{kind:"method",key:"render",value:function(){var e;return r.dy`
      <div class="toolbar">
        ${this.mainPage||null!==(e=history.state)&&void 0!==e&&e.root?r.dy`
              <ha-menu-button
                .hassio=${this.supervisor}
                .hass=${this.hass}
                .narrow=${this.narrow}
              ></ha-menu-button>
            `:this.backPath?r.dy`
              <a href=${this.backPath}>
                <ha-icon-button-arrow-prev
                  .hass=${this.hass}
                ></ha-icon-button-arrow-prev>
              </a>
            `:r.dy`
              <ha-icon-button-arrow-prev
                .hass=${this.hass}
                @click=${this._backTapped}
              ></ha-icon-button-arrow-prev>
            `}

        <div class="main-title">${this.header}</div>
        <slot name="toolbar-icon"></slot>
      </div>
      <div class="content" @scroll=${this._saveScrollPos}><slot></slot></div>
    `}},{kind:"method",decorators:[(0,n.hO)({passive:!0})],key:"_saveScrollPos",value:function(e){this._savedScrollPos=e.target.scrollTop}},{kind:"method",key:"_backTapped",value:function(){history.back()}},{kind:"get",static:!0,key:"styles",value:function(){return r.iv`
      :host {
        display: block;
        height: 100%;
        background-color: var(--primary-background-color);
      }

      :host([narrow]) {
        width: 100%;
        position: fixed;
      }

      .toolbar {
        display: flex;
        align-items: center;
        font-size: 20px;
        height: var(--header-height);
        padding: 0 16px;
        pointer-events: none;
        background-color: var(--app-header-background-color);
        font-weight: 400;
        color: var(--app-header-text-color, white);
        border-bottom: var(--app-header-border-bottom, none);
        box-sizing: border-box;
      }
      .toolbar a {
        color: var(--sidebar-text-color);
        text-decoration: none;
      }

      ha-menu-button,
      ha-icon-button-arrow-prev,
      ::slotted([slot="toolbar-icon"]) {
        pointer-events: auto;
        color: var(--sidebar-icon-color);
      }

      .main-title {
        margin: 0 0 0 24px;
        line-height: 20px;
        flex-grow: 1;
      }

      .content {
        position: relative;
        width: 100%;
        height: calc(100% - 1px - var(--header-height));
        overflow-y: auto;
        overflow: auto;
        -webkit-overflow-scrolling: touch;
      }
    `}}]}}),r.oi)},93383:(e,t,i)=>{var r=i(37500),n=i(33310),o=i(66386);i(15291),i(60010);function s(){s=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(i){t.forEach((function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach((function(r){t.forEach((function(t){var n=t.placement;if(t.kind===r&&("static"===n||"prototype"===n)){var o="static"===n?e:i;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var r=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],r=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!c(e))return i.push(e);var t=this.decorateElement(e,n);i.push(t.element),i.push.apply(i,t.extras),r.push.apply(r,t.finishers)}),this),!t)return{elements:i,finishers:r};var o=this.decorateConstructor(i,t);return r.push.apply(r,o.finishers),o.finishers=r,o},addElementPlacement:function(e,t,i){var r=t[e.placement];if(!i&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var i=[],r=[],n=e.decorators,o=n.length-1;o>=0;o--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,n[o])(a)||a);e=l.element,this.addElementPlacement(e,t),l.finisher&&r.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);i.push.apply(i,c)}}return{element:e,finishers:r,extras:i}},decorateConstructor:function(e,t){for(var i=[],r=t.length-1;r>=0;r--){var n=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[r])(n)||n);if(void 0!==o.finisher&&i.push(o.finisher),void 0!==o.elements){e=o.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return p(e,t);var i=Object.prototype.toString.call(e).slice(8,-1);return"Object"===i&&e.constructor&&(i=e.constructor.name),"Map"===i||"Set"===i?Array.from(e):"Arguments"===i||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(i)?p(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=u(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:i,placement:r,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:h(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=h(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var r=(0,t[i])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}function a(e){var t,i=u(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function l(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function c(e){return e.decorators&&e.decorators.length}function d(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function h(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function u(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var r=i.call(e,t||"default");if("object"!=typeof r)return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function p(e,t){(null==t||t>e.length)&&(t=e.length);for(var i=0,r=new Array(t);i<t;i++)r[i]=e[i];return r}!function(e,t,i,r){var n=s();if(r)for(var o=0;o<r.length;o++)n=r[o](n);var h=t((function(e){n.initializeInstanceElements(e,u.elements)}),i),u=n.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},r=0;r<e.length;r++){var n,o=e[r];if("method"===o.kind&&(n=t.find(i)))if(d(o.descriptor)||d(n.descriptor)){if(c(o)||c(n))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");n.descriptor=o.descriptor}else{if(c(o)){if(c(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");n.decorators=o.decorators}l(o,n)}else t.push(o)}return t}(h.d.map(a)),e);n.initializeClassElements(h.F,u.elements),n.runClassFinishers(h.F,u.finishers)}([(0,n.Mo)("ais-dom-iframe-view")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.Cb)()],key:"url",value:void 0},{kind:"field",decorators:[(0,n.Cb)()],key:"entities",value:void 0},{kind:"field",decorators:[(0,n.Cb)()],key:"_access_token",value:()=>""},{kind:"method",key:"render",value:function(){const e=(0,o.GQ)();return this._access_token=(null==e?void 0:e.access_token)||"",r.dy`
      <ha-card>
        ${this.entities.length?this.entities.map((e=>{let t="";try{t=this.hass.states[e.entity_id].attributes.IPAddress}catch{t=""}let i="";return""!==t&&void 0!==t?window.location.hostname.startsWith("dom-demo.")||window.location.hostname.startsWith("demo.")?r.dy`<p style="text-align: center; padding:10px;">
                    <b>BRAMKA DEMO</b><br />
                    <span style="font-size:8em" class="text"><b>🤖</b></span>
                    <br /><br />
                    <b>BRAK DOSTĘPU DO MENU URZĄDZENIA</b>
                  </p>`:(i=location.protocol+"//"+window.location.hostname+":"+window.location.port+"/api/ais_auto_proxy/"+this._access_token+"/"+t+"/80/",r.dy`
                  ${""!==t?r.dy` <iframe .src="${i}"></iframe> `:r.dy``}
                `):r.dy``})):r.dy``}
      </ha-card>
    `}},{kind:"get",static:!0,key:"styles",value:function(){return r.iv`
      iframe {
        display: block;
        width: 100%;
        height: 600px;
        border: 0;
      }
      paper-icon-button {
        color: var(--text-primary-color);
      }
    `}}]}}),r.oi)},23031:(e,t,i)=>{var r=i(37500),n=i(33310);i(3143),i(53973),i(25782),i(89194),i(22098),i(29925),i(43709);const o=()=>Promise.all([i.e(88278),i.e(85084),i.e(44281),i.e(77576),i.e(74535),i.e(77476),i.e(96045)]).then(i.bind(i,80146));function s(){s=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(i){t.forEach((function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach((function(r){t.forEach((function(t){var n=t.placement;if(t.kind===r&&("static"===n||"prototype"===n)){var o="static"===n?e:i;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var r=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],r=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!c(e))return i.push(e);var t=this.decorateElement(e,n);i.push(t.element),i.push.apply(i,t.extras),r.push.apply(r,t.finishers)}),this),!t)return{elements:i,finishers:r};var o=this.decorateConstructor(i,t);return r.push.apply(r,o.finishers),o.finishers=r,o},addElementPlacement:function(e,t,i){var r=t[e.placement];if(!i&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var i=[],r=[],n=e.decorators,o=n.length-1;o>=0;o--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,n[o])(a)||a);e=l.element,this.addElementPlacement(e,t),l.finisher&&r.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);i.push.apply(i,c)}}return{element:e,finishers:r,extras:i}},decorateConstructor:function(e,t){for(var i=[],r=t.length-1;r>=0;r--){var n=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[r])(n)||n);if(void 0!==o.finisher&&i.push(o.finisher),void 0!==o.elements){e=o.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return p(e,t);var i=Object.prototype.toString.call(e).slice(8,-1);return"Object"===i&&e.constructor&&(i=e.constructor.name),"Map"===i||"Set"===i?Array.from(e):"Arguments"===i||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(i)?p(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=u(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:i,placement:r,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:h(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=h(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var r=(0,t[i])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}function a(e){var t,i=u(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function l(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function c(e){return e.decorators&&e.decorators.length}function d(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function h(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function u(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var r=i.call(e,t||"default");if("object"!=typeof r)return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function p(e,t){(null==t||t>e.length)&&(t=e.length);for(var i=0,r=new Array(t);i<t;i++)r[i]=e[i];return r}function f(e,t,i){return f="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,i){var r=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=m(e)););return e}(e,t);if(r){var n=Object.getOwnPropertyDescriptor(r,t);return n.get?n.get.call(i):n.value}},f(e,t,i||e)}function m(e){return m=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)},m(e)}!function(e,t,i,r){var n=s();if(r)for(var o=0;o<r.length;o++)n=r[o](n);var h=t((function(e){n.initializeInstanceElements(e,u.elements)}),i),u=n.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},r=0;r<e.length;r++){var n,o=e[r];if("method"===o.kind&&(n=t.find(i)))if(d(o.descriptor)||d(n.descriptor)){if(c(o)||c(n))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");n.descriptor=o.descriptor}else{if(c(o)){if(c(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");n.decorators=o.decorators}l(o,n)}else t.push(o)}return t}(h.d.map(a)),e);n.initializeClassElements(h.F,u.elements),n.runClassFinishers(h.F,u.finishers)}([(0,n.Mo)("ha-ais-dom-rf433-config-card")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"get",static:!0,key:"styles",value:function(){return r.iv`
      ha-icon {
        width: 40px;
      }
      mwc-button {
        background-color: #727272;
      }
      .entity-id {
        color: var(--secondary-text-color);
      }
      .buttons {
        text-align: right;
        margin: 0 0 0 8px;
      }
      .disabled-entry {
        color: var(--secondary-text-color);
      }
      state-badge {
        cursor: pointer;
      }
      paper-icon-item:not(.disabled-entry) paper-item-body {
        cursor: pointer;
      }
      .div-right {
        width: 100%;
        text-align: right;
      }
      .bottom {
        font-size: 80%;
        color: var(--secondary-text-color);
      }
      div.left {
        position: absolute;
        left: 22px;
        color: var(--secondary-text-color);
      }
      form {
        display: block;
        padding: 16px;
      }
      .events {
        margin: 26px 0;
      }
      .event {
        border: 3px solid var(--divider-color);
        padding: 4px;
        margin-top: 4px;
        padding-top: 26px;
        background-repeat: no-repeat;
        background-position: right;
        background-size: 20%;
        background-image: url('data:image/svg+xml;utf-8,<svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" viewBox="0 0 5 24"><path fill="b9b2b2" fill-opacity="0.1" d="M4.93,4.93C3.12,6.74 2,9.24 2,12C2,14.76 3.12,17.26 4.93,19.07L6.34,17.66C4.89,16.22 4,14.22 4,12C4,9.79 4.89,7.78 6.34,6.34L4.93,4.93M19.07,4.93L17.66,6.34C19.11,7.78 20,9.79 20,12C20,14.22 19.11,16.22 17.66,17.66L19.07,19.07C20.88,17.26 22,14.76 22,12C22,9.24 20.88,6.74 19.07,4.93M7.76,7.76C6.67,8.85 6,10.35 6,12C6,13.65 6.67,15.15 7.76,16.24L9.17,14.83C8.45,14.11 8,13.11 8,12C8,10.89 8.45,9.89 9.17,9.17L7.76,7.76M16.24,7.76L14.83,9.17C15.55,9.89 16,10.89 16,12C16,13.11 15.55,14.11 14.83,14.83L16.24,16.24C17.33,15.15 18,13.65 18,12C18,10.35 17.33,8.85 16.24,7.76M12,10A2,2 0 0,0 10,12A2,2 0 0,0 12,14A2,2 0 0,0 14,12A2,2 0 0,0 12,10Z"></path></svg>');
      }
      .event:first-child {
        border-top: 2px solid var(--divider-color);
      }
      pre {
        margin: 0px;
        max-width: 600px;
        display: block;
        white-space: pre-wrap;
        word-wrap: break-word;
      }
      span.idx {
        color: var(--secondary-text-color);
        font-size: large;
        font-weight: bold;
      }

      div.right ha-icon {
        position: relative;
        top: -20px;
        color: var(--primary-color);
      }
    `}},{kind:"field",decorators:[(0,n.Cb)()],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.Cb)()],key:"deviceId",value:void 0},{kind:"field",decorators:[(0,n.Cb)()],key:"entities",value:void 0},{kind:"field",decorators:[(0,n.Cb)()],key:"narrow",value:void 0},{kind:"field",decorators:[(0,n.Cb)()],key:"_currentMode",value:()=>0},{kind:"field",decorators:[(0,n.Cb)()],key:"_currentModeHeader",value:()=>"Uczenie kodów RF"},{kind:"field",decorators:[(0,n.Cb)()],key:"_instructionInfo",value:()=>"Aby nauczyć Asystenta kodów pilota radiowego (lub innego urządzenia wysyłającego kody radiowe o częstotliwości 433), uruchom tryb uczenia kodów RF, naciskając przycisk poniżej."},{kind:"method",key:"render",value:function(){const e=this.hass.states["sensor.ais_dom_mqtt_rf_sensor"];return r.dy`
      <div class="content">
        <ha-card header=${this._currentModeHeader}>
          <div class="card-content">
            <p>
              ${this._instructionInfo}
            </p>
            <div class="div-right">
              <mwc-button @click=${this._handleModeSubmit} type="submit">
                ${0===this._currentMode?"Start nasłuchiwania kodów":1===this._currentMode?"Start testowania/dodawania":"Koniec testowania/dodawania"}
              </mwc-button>
            </div>
            ${0!==this._currentMode?r.dy`<div class="events">
              ${e.attributes.codes.map(((e,t)=>r.dy`
                    <div class="event" id="event_${t}">
                      <div class="right">
                        <ha-icon
                          icon="mdi:close"
                          @click=${this._handleCloseCode}
                          .data-idx=${t}
                        ></ha-icon>
                      </div>
                      <span class="idx">[${t+1}]</span> Rozpoznany kod RF:
                      <span
                        style="font-size:xx-small; width:100%; display: block; white-space: pre-wrap; word-wrap: break-word; text-align: left;"
                        >(${e.B1})</span
                      >
                      <pre>${e.B0}</pre>
                      ${2===this._currentMode?r.dy`
                            <div class="bottom">
                              <paper-input
                                label="Nazwa"
                                value="Nazwa"
                                id=${"name_"+t}
                                }
                              ></paper-input>
                              <div class="div-right">
                                <mwc-button
                                  @click=${this._handleTestCode}
                                  .data-b0=${e.B0}
                                  .data-topic=${e.topic}
                                  .data-idx=${t}
                                  type="submit"
                                >
                                  <ha-icon icon="mdi:rocket"></ha-icon>
                                  Testuj
                                </mwc-button>
                                <mwc-button
                                  @click=${this._handleSubmitEntity}
                                  .data-b0=${e.B0}
                                  .data-topic=${e.topic}
                                  .data-idx=${t}
                                  .data-ttt=${"switch"}
                                  type="submit"
                                >
                                  <ha-icon icon="mdi:flash"></ha-icon>
                                  Dodaj Przycisk
                                </mwc-button>
                                <mwc-button
                                  @click=${this._handleSubmitEntity}
                                  .data-b0=${e.B0}
                                  .data-topic=${e.topic}
                                  .data-idx=${t}
                                  .data-ttt=${"sensor"}
                                  type="submit"
                                >
                                  <ha-icon icon="mdi:motion-sensor"></ha-icon>
                                  Dodaj Czujnik
                                </mwc-button>
                              </div>
                            </div>
                          `:r.dy``}
                    </div>
                  `))}
            </div>
          </div>
          `:r.dy``}
        </ha-card>
        <mqtt-subscribe-card .hass=${this.hass}></mqtt-subscribe-card>
      </div>
    `}},{kind:"method",key:"firstUpdated",value:function(e){f(m(i.prototype),"firstUpdated",this).call(this,e),o()}},{kind:"method",key:"_handleModeSubmit",value:async function(){0===this._currentMode?(this._currentMode=1,this.hass.callService("ais_dom_device","start_rf_sniffing"),this._currentModeHeader="Nasłuchiwanie kodów RF",this._instructionInfo="Teraz wyślij kilka kodów (naciśnij kilka razy przyciski na pilocie). Po skończeniu wysyłania przejdź w tryb testowania kodów, naciskając przycisk poniżej."):1===this._currentMode?(this._currentMode=2,this.hass.callService("ais_dom_device","stop_rf_sniffing",{clear:!1}),this._currentModeHeader="Testowanie i zapisanie kodów RF",this._instructionInfo="Przetestuj odebrane kody, ten, który działa dodaj jako przycisk do systemu. By zakończyć tryb testowania/dodawania naciśnij przycisk poniżej."):2===this._currentMode&&(this._currentMode=0,this._currentModeHeader="Uczenie kodów RF",this._instructionInfo="Aby nauczyć Asystenta kodów pilota radiowego (lub innego urządzenia wysyłającego kody radiowe o częstotliwości 433), uruchom tryb uczenia kodów RF, naciskając przycisk poniżej.",this.hass.callService("ais_dom_device","stop_rf_sniffing",{clear:!0}))}},{kind:"method",key:"_handleTestCode",value:async function(e){if(null!=e.currentTarget){const t=e.currentTarget["data-b0"],i=e.currentTarget["data-topic"];this.hass.callService("ais_dom_device","send_rf_code",{topic:i,deviceId:this.deviceId,code:t})}}},{kind:"method",key:"_handleCloseCode",value:async function(e){if(null!=e.currentTarget){const t=e.currentTarget["data-idx"];this.shadowRoot.getElementById("event_"+t).style.display="none"}}},{kind:"method",key:"_handleSubmitEntity",value:async function(e){if(null!=e.currentTarget){const t=e.currentTarget["data-b0"],i=e.currentTarget["data-topic"],r=e.currentTarget["data-idx"],n=e.currentTarget["data-ttt"],o=this.shadowRoot.getElementById("name_"+r);this.hass.callService("ais_dom_device","add_ais_dom_entity",{name:o.value,topic:i,deviceId:this.deviceId,code:t,type:n}),this.shadowRoot.getElementById("event_"+r).style.display="none"}}}]}}),r.oi)},98772:(e,t,i)=>{i.a(e,(async e=>{i(25782),i(53973),i(89194);var t=i(37500),r=i(33310),n=i(58831),o=i(16023),s=(i(3143),i(22098),i(29925),i(37482)),a=i(96491),l=i(94458),c=i(91741),d=i(34007),h=i(74186),u=e([s]);function p(){p=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(i){t.forEach((function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach((function(r){t.forEach((function(t){var n=t.placement;if(t.kind===r&&("static"===n||"prototype"===n)){var o="static"===n?e:i;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var r=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],r=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!y(e))return i.push(e);var t=this.decorateElement(e,n);i.push(t.element),i.push.apply(i,t.extras),r.push.apply(r,t.finishers)}),this),!t)return{elements:i,finishers:r};var o=this.decorateConstructor(i,t);return r.push.apply(r,o.finishers),o.finishers=r,o},addElementPlacement:function(e,t,i){var r=t[e.placement];if(!i&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var i=[],r=[],n=e.decorators,o=n.length-1;o>=0;o--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,n[o])(a)||a);e=l.element,this.addElementPlacement(e,t),l.finisher&&r.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);i.push.apply(i,c)}}return{element:e,finishers:r,extras:i}},decorateConstructor:function(e,t){for(var i=[],r=t.length-1;r>=0;r--){var n=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[r])(n)||n);if(void 0!==o.finisher&&i.push(o.finisher),void 0!==o.elements){e=o.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return w(e,t);var i=Object.prototype.toString.call(e).slice(8,-1);return"Object"===i&&e.constructor&&(i=e.constructor.name),"Map"===i||"Set"===i?Array.from(e):"Arguments"===i||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(i)?w(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=b(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:i,placement:r,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:g(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=g(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var r=(0,t[i])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}function f(e){var t,i=b(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function m(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function y(e){return e.decorators&&e.decorators.length}function v(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function g(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function b(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var r=i.call(e,t||"default");if("object"!=typeof r)return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function w(e,t){(null==t||t>e.length)&&(t=e.length);for(var i=0,r=new Array(t);i<t;i++)r[i]=e[i];return r}s=(u.then?await u:u)[0];!function(e,t,i,r){var n=p();if(r)for(var o=0;o<r.length;o++)n=r[o](n);var s=t((function(e){n.initializeInstanceElements(e,a.elements)}),i),a=n.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},r=0;r<e.length;r++){var n,o=e[r];if("method"===o.kind&&(n=t.find(i)))if(v(o.descriptor)||v(n.descriptor)){if(y(o)||y(n))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");n.descriptor=o.descriptor}else{if(y(o)){if(y(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");n.decorators=o.decorators}m(o,n)}else t.push(o)}return t}(s.d.map(f)),e);n.initializeClassElements(s.F,a.elements),n.runClassFinishers(s.F,a.finishers)}([(0,r.Mo)("ha-device-entities-card")],(function(e,i){return{F:class extends i{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,r.Cb)()],key:"header",value:void 0},{kind:"field",decorators:[(0,r.Cb)()],key:"deviceName",value:void 0},{kind:"field",decorators:[(0,r.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,r.Cb)()],key:"entities",value:void 0},{kind:"field",decorators:[(0,r.Cb)()],key:"showHidden",value:()=>!1},{kind:"field",decorators:[(0,r.SB)()],key:"_extDisabledEntityEntries",value:void 0},{kind:"field",key:"_entityRows",value:()=>[]},{kind:"method",key:"shouldUpdate",value:function(e){return!e.has("hass")||1!==e.size||(this._entityRows.forEach((e=>{e.hass=this.hass})),!1)}},{kind:"method",key:"render",value:function(){if(!this.entities.length)return t.dy`
        <ha-card outlined .header=${this.header}>
          <div class="empty card-content">
            ${this.hass.localize("ui.panel.config.devices.entities.none")}
          </div>
        </ha-card>
      `;const e=[],i=[];return this._entityRows=[],this.entities.forEach((t=>{t.disabled_by?this._extDisabledEntityEntries?i.push(this._extDisabledEntityEntries[t.entity_id]||t):i.push(t):e.push(t)})),t.dy`
      <ha-card outlined .header=${this.header}>
        <div id="entities" @hass-more-info=${this._overrideMoreInfo}>
          ${e.map((e=>this.hass.states[e.entity_id]?this._renderEntity(e):this._renderEntry(e)))}
        </div>
        ${i.length?this.showHidden?t.dy`
                ${i.map((e=>this._renderEntry(e)))}
                <button class="show-more" @click=${this._toggleShowHidden}>
                  ${this.hass.localize("ui.panel.config.devices.entities.hide_disabled")}
                </button>
              `:t.dy`
                <button class="show-more" @click=${this._toggleShowHidden}>
                  ${this.hass.localize("ui.panel.config.devices.entities.hidden_entities","count",i.length)}
                </button>
              `:""}
        <div class="card-actions">
          <mwc-button @click=${this._addToLovelaceView}>
            ${this.hass.localize("ui.panel.config.devices.entities.add_entities_lovelace")}
          </mwc-button>
        </div>
      </ha-card>
    `}},{kind:"method",key:"_toggleShowHidden",value:function(){if(this.showHidden=!this.showHidden,!this.showHidden||void 0!==this._extDisabledEntityEntries)return;this._extDisabledEntityEntries={};const e=this.entities.filter((e=>e.disabled_by)),t=async()=>{if(0===e.length)return;const i=e.pop().entity_id,r=await(0,h.L3)(this.hass,i);this._extDisabledEntityEntries[i]=r,this.requestUpdate("_extDisabledEntityEntries"),t()};t(),t(),t()}},{kind:"method",key:"_renderEntity",value:function(e){const i={entity:e.entity_id},r=(0,s.m)(i);if(this.hass){r.hass=this.hass;const t=this.hass.states[e.entity_id],n=(0,d.N)((0,c.C)(t),this.deviceName.toLowerCase());e.hidden_by?i.name=`${n||(0,c.C)(t)} (${this.hass.localize("ui.panel.config.devices.entities.hidden")})`:n&&(i.name=n)}return r.entry=e,this._entityRows.push(r),t.dy` <div>${r}</div> `}},{kind:"method",key:"_renderEntry",value:function(e){const i=e.stateName||e.name||e.original_name;return t.dy`
      <paper-icon-item
        class="disabled-entry"
        .entry=${e}
        @click=${this._openEditEntry}
      >
        <ha-svg-icon
          slot="item-icon"
          .path=${(0,o.K)((0,n.M)(e.entity_id))}
        ></ha-svg-icon>
        <paper-item-body>
          <div class="name">
            ${i?(0,d.N)(i,this.deviceName.toLowerCase())||i:e.entity_id}
          </div>
        </paper-item-body>
      </paper-icon-item>
    `}},{kind:"method",key:"_overrideMoreInfo",value:function(e){e.stopPropagation();const t=e.target.entry;(0,l.R)(this,{entry:t,entity_id:t.entity_id})}},{kind:"method",key:"_openEditEntry",value:function(e){const t=e.currentTarget.entry;(0,l.R)(this,{entry:t,entity_id:t.entity_id})}},{kind:"method",key:"_addToLovelaceView",value:function(){(0,a.$)(this,this.hass,this.entities.filter((e=>!e.disabled_by)).map((e=>e.entity_id)),this.deviceName)}},{kind:"get",static:!0,key:"styles",value:function(){return t.iv`
      :host {
        display: block;
      }
      ha-icon {
        margin-left: 8px;
      }
      .entity-id {
        color: var(--secondary-text-color);
      }
      .buttons {
        text-align: right;
        margin: 0 0 0 8px;
      }
      .disabled-entry {
        color: var(--secondary-text-color);
      }
      #entities {
        margin-top: -24px; /* match the spacing between card title and content of the device info card above it */
      }
      #entities > * {
        margin: 8px 16px 8px 8px;
      }
      #entities > paper-icon-item {
        margin: 0;
      }
      paper-icon-item {
        min-height: 40px;
        padding: 0 16px;
        cursor: pointer;
        --paper-item-icon-width: 48px;
      }
      .name {
        font-size: 14px;
      }
      .empty {
        text-align: center;
      }
      button.show-more {
        color: var(--primary-color);
        text-align: left;
        cursor: pointer;
        background: none;
        border-width: initial;
        border-style: none;
        border-color: initial;
        border-image: initial;
        padding: 16px;
        font: inherit;
      }
      button.show-more:focus {
        outline: none;
        text-decoration: underline;
      }
    `}}]}}),t.oi)}))},92899:(e,t,i)=>{var r=i(37500),n=i(33310),o=(i(22098),i(57292)),s=i(11654),a=i(97058);function l(){l=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(i){t.forEach((function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach((function(r){t.forEach((function(t){var n=t.placement;if(t.kind===r&&("static"===n||"prototype"===n)){var o="static"===n?e:i;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var r=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],r=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!h(e))return i.push(e);var t=this.decorateElement(e,n);i.push(t.element),i.push.apply(i,t.extras),r.push.apply(r,t.finishers)}),this),!t)return{elements:i,finishers:r};var o=this.decorateConstructor(i,t);return r.push.apply(r,o.finishers),o.finishers=r,o},addElementPlacement:function(e,t,i){var r=t[e.placement];if(!i&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var i=[],r=[],n=e.decorators,o=n.length-1;o>=0;o--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,n[o])(a)||a);e=l.element,this.addElementPlacement(e,t),l.finisher&&r.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);i.push.apply(i,c)}}return{element:e,finishers:r,extras:i}},decorateConstructor:function(e,t){for(var i=[],r=t.length-1;r>=0;r--){var n=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[r])(n)||n);if(void 0!==o.finisher&&i.push(o.finisher),void 0!==o.elements){e=o.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return m(e,t);var i=Object.prototype.toString.call(e).slice(8,-1);return"Object"===i&&e.constructor&&(i=e.constructor.name),"Map"===i||"Set"===i?Array.from(e):"Arguments"===i||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(i)?m(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=f(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:i,placement:r,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:p(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=p(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var r=(0,t[i])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}function c(e){var t,i=f(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function d(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function h(e){return e.decorators&&e.decorators.length}function u(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function p(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function f(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var r=i.call(e,t||"default");if("object"!=typeof r)return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function m(e,t){(null==t||t>e.length)&&(t=e.length);for(var i=0,r=new Array(t);i<t;i++)r[i]=e[i];return r}function y(e,t,i){return y="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,i){var r=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=v(e)););return e}(e,t);if(r){var n=Object.getOwnPropertyDescriptor(r,t);return n.get?n.get.call(i):n.value}},y(e,t,i||e)}function v(e){return v=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)},v(e)}!function(e,t,i,r){var n=l();if(r)for(var o=0;o<r.length;o++)n=r[o](n);var s=t((function(e){n.initializeInstanceElements(e,a.elements)}),i),a=n.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},r=0;r<e.length;r++){var n,o=e[r];if("method"===o.kind&&(n=t.find(i)))if(u(o.descriptor)||u(n.descriptor)){if(h(o)||h(n))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");n.descriptor=o.descriptor}else{if(h(o)){if(h(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");n.decorators=o.decorators}d(o,n)}else t.push(o)}return t}(s.d.map(c)),e);n.initializeClassElements(s.F,a.elements),n.runClassFinishers(s.F,a.finishers)}([(0,n.Mo)("ha-device-info-card")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.Cb)()],key:"device",value:void 0},{kind:"field",decorators:[(0,n.Cb)()],key:"devices",value:void 0},{kind:"field",decorators:[(0,n.Cb)()],key:"areas",value:void 0},{kind:"field",decorators:[(0,n.Cb)()],key:"narrow",value:void 0},{kind:"method",key:"render",value:function(){return r.dy`
      <ha-card
        outlined
        .header=${this.hass.localize("ui.panel.config.devices.device_info","type",this.hass.localize(`ui.panel.config.devices.type.${this.device.entry_type||"device"}_heading`))}
      >
        <div class="card-content">
          ${this.device.model?r.dy` <div class="model">${this.device.model}</div> `:""}
          ${this.device.manufacturer?r.dy`
                <div class="manuf">
                  ${this.hass.localize("ui.panel.config.integrations.config_entry.manuf","manufacturer",this.device.manufacturer)}
                </div>
              `:""}
          ${this.device.via_device_id?r.dy`
                <div class="extra-info">
                  ${this.hass.localize("ui.panel.config.integrations.config_entry.via")}
                  <span class="hub"
                    ><a
                      href="/config/devices/device/${this.device.via_device_id}"
                      >${this._computeDeviceName(this.devices,this.device.via_device_id)}</a
                    ></span
                  >
                </div>
              `:""}
          ${this.device.sw_version?r.dy`
                <div class="extra-info">
                  ${this.hass.localize("ui.panel.config.integrations.config_entry."+("service"!==this.device.entry_type||this.device.hw_version?"firmware":"version"),"version",this.device.sw_version)}
                </div>
              `:""}
          ${this.device.hw_version?r.dy`
                <div class="extra-info">
                  ${this.hass.localize("ui.panel.config.integrations.config_entry.hardware","version",this.device.hw_version)}
                </div>
              `:""}
          <slot></slot>
        </div>
        <slot name="actions"></slot>
      </ha-card>
    `}},{kind:"method",key:"firstUpdated",value:function(e){y(v(i.prototype),"firstUpdated",this).call(this,e),(0,a.O)()}},{kind:"method",key:"_computeDeviceName",value:function(e,t){const i=e.find((e=>e.id===t));return i?(0,o.jL)(i,this.hass):`<${this.hass.localize("ui.panel.config.integrations.config_entry.unknown_via_device")}>`}},{kind:"get",static:!0,key:"styles",value:function(){return[s.Qx,r.iv`
        :host {
          display: block;
        }
        ha-card {
          flex: 1 0 100%;
          min-width: 0;
        }
        .device {
          width: 30%;
        }
        .area {
          color: var(--primary-text-color);
        }
        .extra-info {
          margin-top: 8px;
          word-wrap: break-word;
        }
        .manuf,
        .model {
          color: var(--secondary-text-color);
          word-wrap: break-word;
        }
      `]}}]}}),r.oi)},59103:(e,t,i)=>{i.d(t,{J:()=>o});var r=i(47181);const n=()=>Promise.all([i.e(85084),i.e(85788)]).then(i.bind(i,85788)),o=(e,t)=>{(0,r.B)(e,"show-dialog",{dialogTag:"dialog-device-automation",dialogImport:n,dialogParams:t})}},97058:(e,t,i)=>{i.d(t,{O:()=>n,r:()=>o});var r=i(47181);const n=()=>Promise.all([i.e(85084),i.e(44281),i.e(77576),i.e(68101),i.e(10586)]).then(i.bind(i,10586)),o=(e,t)=>{(0,r.B)(e,"show-dialog",{dialogTag:"dialog-device-registry-detail",dialogImport:n,dialogParams:t})}},32240:(e,t,i)=>{i.a(e,(async e=>{i(54444);var t=i(37500),r=i(33310),n=i(51346),o=i(14516),s=i(7323),a=i(58831),l=i(22311),c=i(91741),d=i(85415),h=i(83447),u=i(92306),p=(i(57793),i(9381),i(81545),i(10983),i(99282),i(52039),i(22814)),f=i(81582),m=i(57292),y=i(42916),v=i(74186),g=i(5986),b=i(76387),w=i(94449),k=i(26765),_=(i(48811),i(1359),i(11654)),E=i(11254),C=i(25936),x=i(97740),$=(i(88165),i(29311)),P=i(98772),A=(i(92899),i(59103)),z=i(97058),D=(i(23031),i(93383),e([P,x]));function S(){S=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(i){t.forEach((function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach((function(r){t.forEach((function(t){var n=t.placement;if(t.kind===r&&("static"===n||"prototype"===n)){var o="static"===n?e:i;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var r=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],r=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!O(e))return i.push(e);var t=this.decorateElement(e,n);i.push(t.element),i.push.apply(i,t.extras),r.push.apply(r,t.finishers)}),this),!t)return{elements:i,finishers:r};var o=this.decorateConstructor(i,t);return r.push.apply(r,o.finishers),o.finishers=r,o},addElementPlacement:function(e,t,i){var r=t[e.placement];if(!i&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var i=[],r=[],n=e.decorators,o=n.length-1;o>=0;o--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,n[o])(a)||a);e=l.element,this.addElementPlacement(e,t),l.finisher&&r.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);i.push.apply(i,c)}}return{element:e,finishers:r,extras:i}},decorateConstructor:function(e,t){for(var i=[],r=t.length-1;r>=0;r--){var n=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[r])(n)||n);if(void 0!==o.finisher&&i.push(o.finisher),void 0!==o.elements){e=o.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return L(e,t);var i=Object.prototype.toString.call(e).slice(8,-1);return"Object"===i&&e.constructor&&(i=e.constructor.name),"Map"===i||"Set"===i?Array.from(e):"Arguments"===i||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(i)?L(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=F(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:i,placement:r,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:M(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=M(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var r=(0,t[i])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}function T(e){var t,i=F(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function I(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function O(e){return e.decorators&&e.decorators.length}function j(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function M(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function F(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var r=i.call(e,t||"default");if("object"!=typeof r)return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function L(e,t){(null==t||t>e.length)&&(t=e.length);for(var i=0,r=new Array(t);i<t;i++)r[i]=e[i];return r}function R(e,t,i){return R="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,i){var r=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=B(e)););return e}(e,t);if(r){var n=Object.getOwnPropertyDescriptor(r,t);return n.get?n.get.call(i):n.value}},R(e,t,i||e)}function B(e){return B=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)},B(e)}[P,x]=D.then?await D:D;const N="M20.71,7.04C21.1,6.65 21.1,6 20.71,5.63L18.37,3.29C18,2.9 17.35,2.9 16.96,3.29L15.12,5.12L18.87,8.87M3,17.25V21H6.75L17.81,9.93L14.06,6.18L3,17.25Z",H="M17,13H13V17H11V13H7V11H11V7H13V11H17M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2Z";!function(e,t,i,r){var n=S();if(r)for(var o=0;o<r.length;o++)n=r[o](n);var s=t((function(e){n.initializeInstanceElements(e,a.elements)}),i),a=n.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},r=0;r<e.length;r++){var n,o=e[r];if("method"===o.kind&&(n=t.find(i)))if(j(o.descriptor)||j(n.descriptor)){if(O(o)||O(n))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");n.descriptor=o.descriptor}else{if(O(o)){if(O(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");n.decorators=o.decorators}I(o,n)}else t.push(o)}return t}(s.d.map(T)),e);n.initializeClassElements(s.F,a.elements),n.runClassFinishers(s.F,a.finishers)}([(0,r.Mo)("ha-config-device-page")],(function(e,x){class P extends x{constructor(...t){super(...t),e(this)}}return{F:P,d:[{kind:"field",decorators:[(0,r.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,r.Cb)()],key:"devices",value:void 0},{kind:"field",decorators:[(0,r.Cb)()],key:"entries",value:void 0},{kind:"field",decorators:[(0,r.Cb)()],key:"entities",value:void 0},{kind:"field",decorators:[(0,r.Cb)()],key:"areas",value:void 0},{kind:"field",decorators:[(0,r.Cb)()],key:"deviceId",value:void 0},{kind:"field",decorators:[(0,r.Cb)({type:Boolean,reflect:!0})],key:"narrow",value:void 0},{kind:"field",decorators:[(0,r.Cb)()],key:"isWide",value:void 0},{kind:"field",decorators:[(0,r.Cb)()],key:"showAdvanced",value:void 0},{kind:"field",decorators:[(0,r.Cb)()],key:"route",value:void 0},{kind:"field",decorators:[(0,r.SB)()],key:"_related",value:void 0},{kind:"field",decorators:[(0,r.SB)()],key:"_diagnosticDownloadLinks",value:void 0},{kind:"field",decorators:[(0,r.SB)()],key:"_deleteButtons",value:void 0},{kind:"field",decorators:[(0,r.SB)()],key:"_deviceActions",value:void 0},{kind:"field",decorators:[(0,r.SB)()],key:"_deviceAlerts",value:void 0},{kind:"field",key:"_logbookTime",value:()=>({recent:86400})},{kind:"field",key:"_device",value:()=>(0,o.Z)(((e,t)=>t?t.find((t=>t.id===e)):void 0))},{kind:"field",key:"_integrations",value:()=>(0,o.Z)(((e,t)=>t.filter((t=>e.config_entries.includes(t.entry_id)))))},{kind:"field",key:"_entities",value(){return(0,o.Z)(((e,t)=>t.filter((t=>t.device_id===e)).map((e=>({...e,stateName:this._computeEntityName(e)}))).sort(((e,t)=>(0,d.$)(e.stateName||`zzz${e.entity_id}`,t.stateName||`zzz${t.entity_id}`)))))}},{kind:"field",key:"_deviceIdInList",value:()=>(0,o.Z)((e=>[e]))},{kind:"field",key:"_entityIds",value:()=>(0,o.Z)((e=>e.map((e=>e.entity_id))))},{kind:"field",key:"_entitiesByCategory",value:()=>(0,o.Z)((e=>{const t=(0,u.v)(e,(e=>e.entity_category?e.entity_category:["sensor","binary_sensor","camera","device_tracker","weather"].includes((0,a.M)(e.entity_id))?"sensor":"control"));for(const e of["control","sensor","diagnostic","config"])e in t||(t[e]=[]);return t}))},{kind:"field",key:"_computeArea",value:()=>(0,o.Z)(((e,t)=>{if(e&&t&&t.area_id)return e.find((e=>e.area_id===t.area_id))}))},{kind:"field",key:"_batteryEntity",value(){return(0,o.Z)((e=>(0,v.eD)(this.hass,e)))}},{kind:"field",key:"_batteryChargingEntity",value(){return(0,o.Z)((e=>(0,v.Mw)(this.hass,e)))}},{kind:"method",key:"willUpdate",value:function(e){R(B(P.prototype),"willUpdate",this).call(this,e),(e.has("deviceId")||e.has("devices")||e.has("entries"))&&(this._diagnosticDownloadLinks=void 0,this._deleteButtons=void 0,this._deviceActions=void 0,this._deviceAlerts=void 0),!(this._diagnosticDownloadLinks&&this._deleteButtons&&this._deviceActions&&this._deviceAlerts)&&this.devices&&this.deviceId&&this.entries&&(this._diagnosticDownloadLinks=Math.random(),this._deleteButtons=[],this._deviceActions=[],this._deviceAlerts=[],this._getDiagnosticButtons(this._diagnosticDownloadLinks),this._getDeleteActions(),this._getDeviceActions(),this._getDeviceAlerts())}},{kind:"method",key:"firstUpdated",value:function(e){R(B(P.prototype),"firstUpdated",this).call(this,e),(0,z.O)()}},{kind:"method",key:"updated",value:function(e){R(B(P.prototype),"updated",this).call(this,e),e.has("deviceId")&&this._findRelated()}},{kind:"method",key:"render",value:function(){var e,i,r,o,a,d,h,u;const p=this._device(this.deviceId,this.devices);if(!p)return t.dy`
        <hass-error-screen
          .hass=${this.hass}
          .error=${this.hass.localize("ui.panel.config.devices.device_not_found")}
        ></hass-error-screen>
      `;const f=(0,m.jL)(p,this.hass),y=this._integrations(p,this.entries),v=this._entities(this.deviceId,this.entities),g=this._entitiesByCategory(v),b=this._batteryEntity(v),w=this._batteryChargingEntity(v),k=b?this.hass.states[b.entity_id]:void 0,_=k&&"binary_sensor"===(0,l.N)(k),C=w?this.hass.states[w.entity_id]:void 0,x=this._computeArea(this.areas,p),P=[],A=[...this._deviceActions||[]];Array.isArray(this._diagnosticDownloadLinks)&&A.push(...this._diagnosticDownloadLinks),this._deleteButtons&&A.push(...this._deleteButtons);const z=A.shift();p.disabled_by&&P.push(t.dy`
          <ha-alert alert-type="warning">
            ${this.hass.localize("ui.panel.config.devices.enabled_cause","type",this.hass.localize(`ui.panel.config.devices.type.${p.entry_type||"device"}`),"cause",this.hass.localize(`ui.panel.config.devices.disabled_by.${p.disabled_by}`))}
          </ha-alert>
          ${"user"===p.disabled_by?t.dy`
                <div class="card-actions" slot="actions">
                  <mwc-button unelevated @click=${this._enableDevice}>
                    ${this.hass.localize("ui.common.enable")}
                  </mwc-button>
                </div>
              `:""}
        `),this._renderIntegrationInfo(p,y,P);const D=(0,s.p)(this.hass,"automation")?t.dy`
          <ha-card outlined>
            <h1 class="card-header">
              ${this.hass.localize("ui.panel.config.devices.automation.automations_heading")}
              <ha-icon-button
                @click=${this._showAutomationDialog}
                .disabled=${p.disabled_by}
                .label=${p.disabled_by?this.hass.localize("ui.panel.config.devices.automation.create_disabled","type",this.hass.localize(`ui.panel.config.devices.type.${p.entry_type||"device"}`)):this.hass.localize("ui.panel.config.devices.automation.create","type",this.hass.localize(`ui.panel.config.devices.type.${p.entry_type||"device"}`))}
                .path=${H}
              ></ha-icon-button>
            </h1>
            ${null!==(e=this._related)&&void 0!==e&&null!==(i=e.automation)&&void 0!==i&&i.length?t.dy`
                  <div class="items">
                    ${this._related.automation.map((e=>{const i=this.hass.states[e];return i?t.dy`<div>
                            <a
                              href=${(0,n.o)(i.attributes.id?`/config/automation/edit/${i.attributes.id}`:void 0)}
                            >
                              <paper-item
                                .automation=${i}
                                .disabled=${!i.attributes.id}
                              >
                                <paper-item-body>
                                  ${(0,c.C)(i)}
                                </paper-item-body>
                                <ha-icon-next></ha-icon-next>
                              </paper-item>
                            </a>
                            ${i.attributes.id?"":t.dy`
                                  <paper-tooltip animation-delay="0">
                                    ${this.hass.localize("ui.panel.config.devices.cant_edit")}
                                  </paper-tooltip>
                                `}
                          </div> `:""}))}
                  </div>
                `:t.dy`
                  <div class="card-content">
                    ${this.hass.localize("ui.panel.config.devices.add_prompt","name",this.hass.localize("ui.panel.config.devices.automation.automations"),"type",this.hass.localize(`ui.panel.config.devices.type.${p.entry_type||"device"}`))}
                  </div>
                `}
          </ha-card>
        `:"",S=(0,s.p)(this.hass,"scene")&&v.length?t.dy`
            <ha-card outlined>
              <h1 class="card-header">
                ${this.hass.localize("ui.panel.config.devices.scene.scenes_heading")}

                <ha-icon-button
                  @click=${this._createScene}
                  .disabled=${p.disabled_by}
                  .label=${p.disabled_by?this.hass.localize("ui.panel.config.devices.scene.create_disabled","type",this.hass.localize(`ui.panel.config.devices.type.${p.entry_type||"device"}`)):this.hass.localize("ui.panel.config.devices.scene.create","type",this.hass.localize(`ui.panel.config.devices.type.${p.entry_type||"device"}`))}
                  .path=${H}
                ></ha-icon-button>
              </h1>
              ${null!==(r=this._related)&&void 0!==r&&null!==(o=r.scene)&&void 0!==o&&o.length?t.dy`
                    <div class="items">
                      ${this._related.scene.map((e=>{const i=this.hass.states[e];return i?t.dy`
                              <div>
                                <a
                                  href=${(0,n.o)(i.attributes.id?`/config/scene/edit/${i.attributes.id}`:void 0)}
                                >
                                  <paper-item
                                    .scene=${i}
                                    .disabled=${!i.attributes.id}
                                  >
                                    <paper-item-body>
                                      ${(0,c.C)(i)}
                                    </paper-item-body>
                                    <ha-icon-next></ha-icon-next>
                                  </paper-item>
                                </a>
                                ${i.attributes.id?"":t.dy`
                                      <paper-tooltip animation-delay="0">
                                        ${this.hass.localize("ui.panel.config.devices.cant_edit")}
                                      </paper-tooltip>
                                    `}
                              </div>
                            `:""}))}
                    </div>
                  `:t.dy`
                    <div class="card-content">
                      ${this.hass.localize("ui.panel.config.devices.add_prompt","name",this.hass.localize("ui.panel.config.devices.scene.scenes"),"type",this.hass.localize(`ui.panel.config.devices.type.${p.entry_type||"device"}`))}
                    </div>
                  `}
            </ha-card>
          `:"",T=(0,s.p)(this.hass,"script")?t.dy`
          <ha-card outlined>
            <h1 class="card-header">
              ${this.hass.localize("ui.panel.config.devices.script.scripts_heading")}
              <ha-icon-button
                @click=${this._showScriptDialog}
                .disabled=${p.disabled_by}
                .label=${p.disabled_by?this.hass.localize("ui.panel.config.devices.script.create_disabled","type",this.hass.localize(`ui.panel.config.devices.type.${p.entry_type||"device"}`)):this.hass.localize("ui.panel.config.devices.script.create","type",this.hass.localize(`ui.panel.config.devices.type.${p.entry_type||"device"}`))}
                .path=${H}
              ></ha-icon-button>
            </h1>
            ${null!==(a=this._related)&&void 0!==a&&null!==(d=a.script)&&void 0!==d&&d.length?t.dy`
                  <div class="items">
                    ${this._related.script.map((e=>{const i=this.hass.states[e];return i?t.dy`
                            <a
                              href=${`/config/script/edit/${i.entity_id}`}
                            >
                              <paper-item .script=${e}>
                                <paper-item-body>
                                  ${(0,c.C)(i)}
                                </paper-item-body>
                                <ha-icon-next></ha-icon-next>
                              </paper-item>
                            </a>
                          `:""}))}
                  </div>
                `:t.dy`
                  <div class="card-content">
                    ${this.hass.localize("ui.panel.config.devices.add_prompt","name",this.hass.localize("ui.panel.config.devices.script.scripts"),"type",this.hass.localize(`ui.panel.config.devices.type.${p.entry_type||"device"}`))}
                  </div>
                `}
          </ha-card>
        `:"";return t.dy`
      <hass-tabs-subpage
        .hass=${this.hass}
        .narrow=${this.narrow}
        .tabs=${$.configSections.devices}
        .route=${this.route}
      >
        ${this.narrow?t.dy`
                <span slot="header">${f}</span>
                <ha-icon-button
                  slot="toolbar-icon"
                  .path=${N}
                  @click=${this._showSettings}
                  .label=${this.hass.localize("ui.panel.config.devices.edit_settings")}
                ></ha-icon-button>
              `:""}
        <div class="container">
          <div class="header fullwidth">
            ${this.narrow?"":t.dy`
                    <div class="header-name">
                      <div>
                        <h1>${f}</h1>
                        ${x?t.dy`
                              <a href="/config/areas/area/${x.area_id}"
                                >${this.hass.localize("ui.panel.config.integrations.config_entry.area","area",x.name||"Unnamed Area")}</a
                              >
                            `:""}
                      </div>
                      <ha-icon-button
                        .path=${N}
                        @click=${this._showSettings}
                        .label=${this.hass.localize("ui.panel.config.devices.edit_settings")}
                      ></ha-icon-button>
                    </div>
                  `}
                <div class="header-right">
                  ${k?t.dy`
                          <div class="battery">
                            ${_?"":k.state+" %"}
                            <ha-battery-icon
                              .hass=${this.hass}
                              .batteryStateObj=${k}
                              .batteryChargingStateObj=${C}
                            ></ha-battery-icon>
                          </div>
                        `:""}
                  ${y.length?t.dy`
                          <img
                            src=${(0,E.X1)({domain:y[0].domain,type:"logo",darkOptimized:null===(h=this.hass.themes)||void 0===h?void 0:h.darkMode})}
                            referrerpolicy="no-referrer"
                            @load=${this._onImageLoad}
                            @error=${this._onImageError}
                          />
                        `:""}

                </div>
          </div>
          ${"AI-Speaker"===(null==p?void 0:p.manufacturer)&&"Rclone"!==(null==p?void 0:p.sw_version)?t.dy`<div class="column ais_device_menu">
                  <!-- ais device menu -->
                  ${"Rclone"!==(null==p?void 0:p.sw_version)?t.dy`
                        <ais-dom-iframe-view
                          .hass=${this.hass}
                          .entities=${v}
                        ></ais-dom-iframe-view>
                      `:t.dy``}
                  ${"Sonoff Bridge"===p.model?t.dy`
                        <ha-ais-dom-rf433-config-card
                          .hass=${this.hass}
                          .entities=${v}
                          .deviceId=${this.deviceId}
                        >
                        </ha-ais-dom-rf433-config-card>
                      `:t.dy``}
                  <!-- ais device menu stop -->
                </div> `:t.dy``}
          <div class="column">
              ${null!==(u=this._deviceAlerts)&&void 0!==u&&u.length?t.dy`
                      <div>
                        ${this._deviceAlerts.map((e=>t.dy`
                              <ha-alert .alertType=${e.level}>
                                ${e.text}
                              </ha-alert>
                            `))}
                      </div>
                    `:""}
              <ha-device-info-card
                .hass=${this.hass}
                .areas=${this.areas}
                .devices=${this.devices}
                .device=${p}
              >
                ${P}
                ${z||A.length?t.dy`
                        <div class="card-actions" slot="actions">
                          <div>
                            <a href=${(0,n.o)(z.href)}>
                              <mwc-button
                                class=${(0,n.o)(z.classes)}
                                .action=${z.action}
                                @click=${this._deviceActionClicked}
                              >
                                ${z.label}
                                ${z.trailingIcon?t.dy`
                                      <ha-svg-icon
                                        .path=${z.trailingIcon}
                                        slot="trailingIcon"
                                      ></ha-svg-icon>
                                    `:""}
                              </mwc-button>
                            </a>
                          </div>

                          ${A.length?t.dy`
                                <ha-button-menu corner="BOTTOM_START">
                                  <ha-icon-button
                                    slot="trigger"
                                    .label=${this.hass.localize("ui.common.menu")}
                                    .path=${"M12,16A2,2 0 0,1 14,18A2,2 0 0,1 12,20A2,2 0 0,1 10,18A2,2 0 0,1 12,16M12,10A2,2 0 0,1 14,12A2,2 0 0,1 12,14A2,2 0 0,1 10,12A2,2 0 0,1 12,10M12,4A2,2 0 0,1 14,6A2,2 0 0,1 12,8A2,2 0 0,1 10,6A2,2 0 0,1 12,4Z"}
                                  ></ha-icon-button>
                                  ${A.map((e=>t.dy`
                                      <a href=${(0,n.o)(e.href)}>
                                        <mwc-list-item
                                          class=${(0,n.o)(e.classes)}
                                          .action=${e.action}
                                          @click=${this._deviceActionClicked}
                                        >
                                          ${e.label}
                                          ${e.trailingIcon?t.dy`
                                                <ha-svg-icon
                                                  .path=${e.trailingIcon}
                                                ></ha-svg-icon>
                                              `:""}
                                        </mwc-list-item>
                                      </a>
                                    `))}
                                </ha-button-menu>
                              `:""}
                        </div>
                      `:""}
              </ha-device-info-card>
            ${this.narrow?"":[D,S,T]}
          </div>
          <div class="column">
            ${["control","sensor","config","diagnostic"].map((e=>g[e].length>0||0===v.length&&"control"===e?t.dy`
                    <ha-device-entities-card
                      .hass=${this.hass}
                      .header=${this.hass.localize(`ui.panel.config.devices.entities.${e}`)}
                      .deviceName=${f}
                      .entities=${g[e]}
                      .showHidden=${null!==p.disabled_by}
                    >
                    </ha-device-entities-card>
                  `:""))}
          </div>
          <div class="column">
            ${this.narrow?[D,S,T]:""}
            ${(0,s.p)(this.hass,"logbook")?t.dy`
                    <ha-card outlined>
                      <h1 class="card-header">
                        ${this.hass.localize("panel.logbook")}
                      </h1>
                      <ha-logbook
                        .hass=${this.hass}
                        .time=${this._logbookTime}
                        .entityIds=${this._entityIds(v)}
                        .deviceIds=${this._deviceIdInList(this.deviceId)}
                        virtualize
                        narrow
                        no-icon
                      ></ha-logbook>
                    </ha-card>
                  `:""}
            </div>
          </div>
        </ha-config-section>
      </hass-tabs-subpage>    `}},{kind:"method",key:"_getDiagnosticButtons",value:async function(e){if(!(0,s.p)(this.hass,"diagnostics"))return;const t=this._device(this.deviceId,this.devices);if(!t)return;let i=await Promise.all(this._integrations(t,this.entries).map((async e=>{if("loaded"!==e.state)return!1;let t;try{t=await(0,y.lf)(this.hass,e.domain)}catch(e){if("not_found"===e.code)return!1;throw e}return!(!t.handlers.device&&!t.handlers.config_entry)&&{link:t.handlers.device?(0,y.ZK)(e.entry_id,this.deviceId):(0,y.iP)(e.entry_id),domain:e.domain}})));i=i.filter(Boolean),this._diagnosticDownloadLinks===e&&i.length>0&&(this._diagnosticDownloadLinks=i.map((e=>({href:e.link,action:e=>this._signUrl(e),label:i.length>1?this.hass.localize("ui.panel.config.devices.download_diagnostics_integration",{integration:(0,g.Lh)(this.hass.localize,e.domain)}):this.hass.localize("ui.panel.config.devices.download_diagnostics")}))))}},{kind:"method",key:"_getDeleteActions",value:function(){const e=this._device(this.deviceId,this.devices);if(!e)return;const t=[];this._integrations(e,this.entries).forEach((e=>{"loaded"===e.state&&e.supports_remove_device&&t.push({action:async()=>{await(0,k.g7)(this,{text:this.hass.localize("ui.panel.config.devices.confirm_delete")})&&await(0,m.dl)(this.hass,this.deviceId,e.entry_id)},classes:"warning",label:t.length>1?this.hass.localize("ui.panel.config.devices.delete_device_integration",{integration:(0,g.Lh)(this.hass.localize,e.domain)}):this.hass.localize("ui.panel.config.devices.delete_device")})})),t.length>0&&(this._deleteButtons=t)}},{kind:"method",key:"_getDeviceActions",value:async function(){var e;const t=this._device(this.deviceId,this.devices);if(!t)return;const r=[],n=(null===(e=t.configuration_url)||void 0===e?void 0:e.startsWith("homeassistant://"))||!1?t.configuration_url.replace("homeassistant://","/"):t.configuration_url;n&&r.push({href:n,label:this.hass.localize(`ui.panel.config.devices.open_configuration_url_${t.entry_type||"device"}`),trailingIcon:"M14,3V5H17.59L7.76,14.83L9.17,16.24L19,6.41V10H21V3M19,19H5V5H12V3H5C3.89,3 3,3.9 3,5V19A2,2 0 0,0 5,21H19A2,2 0 0,0 21,19V12H19V19Z"});const o=this._integrations(t,this.entries).map((e=>e.domain));if(o.includes("mqtt")){const e=(await i.e(86293).then(i.bind(i,86293))).getMQTTDeviceActions(this,t);r.push(...e)}if(o.includes("zha")){const e=await i.e(22430).then(i.bind(i,22430)),n=await e.getZHADeviceActions(this,this.hass,t);r.push(...n)}if(o.includes("zwave_js")){const e=await i.e(78447).then(i.bind(i,78447)),n=await e.getZwaveDeviceActions(this,this.hass,t);r.push(...n)}this._deviceActions=r}},{kind:"method",key:"_getDeviceAlerts",value:async function(){const e=this._device(this.deviceId,this.devices);if(!e)return;const t=[];if(this._integrations(e,this.entries).map((e=>e.domain)).includes("zwave_js")){const r=await i.e(4012).then(i.bind(i,4012)),n=await r.getZwaveDeviceAlerts(this.hass,e);t.push(...n)}t.length&&(this._deviceAlerts=t)}},{kind:"method",key:"_computeEntityName",value:function(e){if(e.name)return e.name;const t=this.hass.states[e.entity_id];return t?(0,c.C)(t):null}},{kind:"method",key:"_onImageLoad",value:function(e){e.target.style.display="inline-block"}},{kind:"method",key:"_onImageError",value:function(e){e.target.style.display="none"}},{kind:"method",key:"_findRelated",value:async function(){this._related=await(0,w.K)(this.hass,"device",this.deviceId)}},{kind:"method",key:"_createScene",value:function(){const e={};this._entities(this.deviceId,this.entities).forEach((t=>{e[t.entity_id]=""})),(0,b.mR)({entities:e})}},{kind:"method",key:"_showScriptDialog",value:function(){(0,A.J)(this,{device:this._device(this.deviceId,this.devices),script:!0})}},{kind:"method",key:"_showAutomationDialog",value:function(){(0,A.J)(this,{device:this._device(this.deviceId,this.devices),script:!1})}},{kind:"method",key:"_renderIntegrationInfo",value:function(e,r,n){const o=r.map((e=>e.domain));o.includes("zha")&&(i.e(49199).then(i.bind(i,49199)),n.push(t.dy`
        <ha-device-info-zha
          .hass=${this.hass}
          .device=${e}
        ></ha-device-info-zha>
      `)),o.includes("zwave_js")&&(i.e(96747).then(i.bind(i,96747)),n.push(t.dy`
        <ha-device-info-zwave_js
          .hass=${this.hass}
          .device=${e}
        ></ha-device-info-zwave_js>
      `))}},{kind:"method",key:"_showSettings",value:async function(){const e=this._device(this.deviceId,this.devices);(0,z.r)(this,{device:e,updateEntry:async t=>{const i=e.name_by_user||e.name,r=t.name_by_user;if("user"===t.disabled_by&&"user"!==e.disabled_by)for(const i of e.config_entries)if(!this.devices.some((t=>t.id!==e.id&&t.config_entries.includes(i)))){const e=this.entries.find((e=>e.entry_id===i));if(e&&!e.disabled_by&&await(0,k.g7)(this,{title:this.hass.localize("ui.panel.config.devices.confirm_disable_config_entry","entry_name",e.title),confirmText:this.hass.localize("ui.common.yes"),dismissText:this.hass.localize("ui.common.no")})){let e;try{e=await(0,f.Ny)(this.hass,i)}catch(e){return void(0,k.Ys)(this,{title:this.hass.localize("ui.panel.config.integrations.config_entry.disable_error"),text:e.message})}e.require_restart&&(0,k.Ys)(this,{text:this.hass.localize("ui.panel.config.integrations.config_entry.disable_restart_confirm")}),delete t.disabled_by}}try{await(0,m.t1)(this.hass,this.deviceId,t)}catch(e){(0,k.Ys)(this,{title:this.hass.localize("ui.panel.config.devices.update_device_error"),text:e.message})}if(!i||!r||i===r)return;const n=this._entities(this.deviceId,this.entities),o=this.showAdvanced&&await(0,k.g7)(this,{title:this.hass.localize("ui.panel.config.devices.confirm_rename_entity_ids"),text:this.hass.localize("ui.panel.config.devices.confirm_rename_entity_ids_warning"),confirmText:this.hass.localize("ui.common.rename"),dismissText:this.hass.localize("ui.common.no"),warning:!0}),s=n.map((e=>{const t=e.name||e.stateName;let n=null,s=null;if(t&&t.includes(i)&&(s=t.replace(i,r)),o){const t=(0,h.l)(i);e.entity_id.includes(t)&&(n=e.entity_id.replace(t,(0,h.l)(r)))}if(s||n)return(0,v.Nv)(this.hass,e.entity_id,{name:s||t,new_entity_id:n||e.entity_id})}));await Promise.all(s)}})}},{kind:"method",key:"_enableDevice",value:async function(){await(0,m.t1)(this.hass,this.deviceId,{disabled_by:null})}},{kind:"method",key:"_signUrl",value:async function(e){const t=e.currentTarget.closest("a"),i=await(0,p.iI)(this.hass,t.getAttribute("href"));(0,C.N)(i.path)}},{kind:"method",key:"_deviceActionClicked",value:function(e){e.currentTarget.action&&(e.preventDefault(),e.currentTarget.action(e))}},{kind:"get",static:!0,key:"styles",value:function(){return[_.Qx,t.iv`
        .container {
          display: flex;
          flex-wrap: wrap;
          margin: auto;
          max-width: 1000px;
          margin-top: 32px;
          margin-bottom: 32px;
        }

        .card-header {
          display: flex;
          align-items: center;
          justify-content: space-between;
          padding-bottom: 12px;
        }

        .card-header ha-icon-button {
          margin-right: -8px;
          color: var(--primary-color);
          height: auto;
        }

        .device-info {
          padding: 16px;
        }

        h1 {
          margin: 0;
          font-family: var(--paper-font-headline_-_font-family);
          -webkit-font-smoothing: var(
            --paper-font-headline_-_-webkit-font-smoothing
          );
          font-size: var(--paper-font-headline_-_font-size);
          font-weight: var(--paper-font-headline_-_font-weight);
          letter-spacing: var(--paper-font-headline_-_letter-spacing);
          line-height: var(--paper-font-headline_-_line-height);
          opacity: var(--dark-primary-opacity);
        }

        .header {
          display: flex;
          justify-content: space-between;
        }

        .header-name {
          display: flex;
          align-items: center;
          padding-left: 8px;
          padding-inline-start: 8px;
          direction: var(--direction);
        }

        .column,
        .fullwidth {
          padding: 8px;
          box-sizing: border-box;
        }
        .column {
          width: 33%;
          flex-grow: 1;
        }
        .fullwidth {
          width: 100%;
          flex-grow: 1;
        }

        .header-right {
          align-self: center;
        }

        .header-right img {
          height: 30px;
        }

        .header-right {
          display: flex;
        }

        .header-right:first-child {
          width: 100%;
          justify-content: flex-end;
        }

        .header-right > *:not(:first-child) {
          margin-left: 16px;
        }

        .battery {
          align-self: center;
          align-items: center;
          display: flex;
          white-space: nowrap;
        }

        .column > *:not(:first-child) {
          margin-top: 16px;
        }

        :host([narrow]) .column {
          width: 100%;
        }

        :host([narrow]) .container {
          margin-top: 0;
        }

        paper-item {
          cursor: pointer;
          font-size: var(--paper-font-body1_-_font-size);
        }

        a {
          text-decoration: none;
          color: var(--primary-color);
        }

        ha-card a {
          color: var(--primary-text-color);
        }

        ha-svg-icon[slot="trailingIcon"] {
          display: block;
        }

        .items {
          padding-bottom: 16px;
        }

        .ais_device_menu {
          min-width: 400px;

        ha-logbook {
          height: 400px;
        }
        :host([narrow]) ha-logbook {
          height: 235px;
        }

        .card-actions {
          display: flex;
          justify-content: space-between;
          align-items: center;
        }
      `]}}]}}),t.oi)}))},94458:(e,t,i)=>{i.d(t,{T:()=>n,R:()=>s});var r=i(47181);const n=()=>Promise.all([i.e(29563),i.e(98985),i.e(24103),i.e(59799),i.e(6294),i.e(88278),i.e(85084),i.e(45507),i.e(44281),i.e(22001),i.e(69794),i.e(29925),i.e(77576),i.e(31742),i.e(49644),i.e(68101),i.e(46544),i.e(63528)]).then(i.bind(i,49070)),o=()=>document.querySelector("home-assistant").shadowRoot.querySelector("dialog-entity-editor"),s=(e,t)=>((0,r.B)(e,"show-dialog",{dialogTag:"dialog-entity-editor",dialogImport:n,dialogParams:t}),o)},88165:(e,t,i)=>{var r=i(37500),n=i(33310),o=i(8636);function s(){s=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(i){t.forEach((function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach((function(r){t.forEach((function(t){var n=t.placement;if(t.kind===r&&("static"===n||"prototype"===n)){var o="static"===n?e:i;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var r=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],r=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!c(e))return i.push(e);var t=this.decorateElement(e,n);i.push(t.element),i.push.apply(i,t.extras),r.push.apply(r,t.finishers)}),this),!t)return{elements:i,finishers:r};var o=this.decorateConstructor(i,t);return r.push.apply(r,o.finishers),o.finishers=r,o},addElementPlacement:function(e,t,i){var r=t[e.placement];if(!i&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var i=[],r=[],n=e.decorators,o=n.length-1;o>=0;o--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,n[o])(a)||a);e=l.element,this.addElementPlacement(e,t),l.finisher&&r.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);i.push.apply(i,c)}}return{element:e,finishers:r,extras:i}},decorateConstructor:function(e,t){for(var i=[],r=t.length-1;r>=0;r--){var n=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[r])(n)||n);if(void 0!==o.finisher&&i.push(o.finisher),void 0!==o.elements){e=o.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return p(e,t);var i=Object.prototype.toString.call(e).slice(8,-1);return"Object"===i&&e.constructor&&(i=e.constructor.name),"Map"===i||"Set"===i?Array.from(e):"Arguments"===i||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(i)?p(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=u(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:i,placement:r,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:h(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=h(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var r=(0,t[i])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}function a(e){var t,i=u(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function l(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function c(e){return e.decorators&&e.decorators.length}function d(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function h(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function u(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var r=i.call(e,t||"default");if("object"!=typeof r)return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function p(e,t){(null==t||t>e.length)&&(t=e.length);for(var i=0,r=new Array(t);i<t;i++)r[i]=e[i];return r}!function(e,t,i,r){var n=s();if(r)for(var o=0;o<r.length;o++)n=r[o](n);var h=t((function(e){n.initializeInstanceElements(e,u.elements)}),i),u=n.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},r=0;r<e.length;r++){var n,o=e[r];if("method"===o.kind&&(n=t.find(i)))if(d(o.descriptor)||d(n.descriptor)){if(c(o)||c(n))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");n.descriptor=o.descriptor}else{if(c(o)){if(c(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");n.decorators=o.decorators}l(o,n)}else t.push(o)}return t}(h.d.map(a)),e);n.initializeClassElements(h.F,u.elements),n.runClassFinishers(h.F,u.finishers)}([(0,n.Mo)("ha-config-section")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.Cb)()],key:"isWide",value:()=>!1},{kind:"field",decorators:[(0,n.Cb)({type:Boolean})],key:"vertical",value:()=>!1},{kind:"field",decorators:[(0,n.Cb)({type:Boolean,attribute:"full-width"})],key:"fullWidth",value:()=>!1},{kind:"method",key:"render",value:function(){return r.dy`
      <div
        class="content ${(0,o.$)({narrow:!this.isWide,"full-width":this.fullWidth})}"
      >
        <div class="header"><slot name="header"></slot></div>
        <div
          class="together layout ${(0,o.$)({narrow:!this.isWide,vertical:this.vertical||!this.isWide,horizontal:!this.vertical&&this.isWide})}"
        >
          <div class="intro"><slot name="introduction"></slot></div>
          <div class="panel flex-auto"><slot></slot></div>
        </div>
      </div>
    `}},{kind:"get",static:!0,key:"styles",value:function(){return r.iv`
      :host {
        display: block;
      }
      .content {
        padding: 28px 20px 0;
        max-width: 1040px;
        margin: 0 auto;
      }

      .layout {
        display: flex;
      }

      .horizontal {
        flex-direction: row;
      }

      .vertical {
        flex-direction: column;
      }

      .flex-auto {
        flex: 1 1 auto;
      }

      .header {
        font-family: var(--paper-font-headline_-_font-family);
        -webkit-font-smoothing: var(
          --paper-font-headline_-_-webkit-font-smoothing
        );
        font-size: var(--paper-font-headline_-_font-size);
        font-weight: var(--paper-font-headline_-_font-weight);
        letter-spacing: var(--paper-font-headline_-_letter-spacing);
        line-height: var(--paper-font-headline_-_line-height);
        opacity: var(--dark-primary-opacity);
      }

      .together {
        margin-top: 32px;
      }

      .intro {
        font-family: var(--paper-font-subhead_-_font-family);
        -webkit-font-smoothing: var(
          --paper-font-subhead_-_-webkit-font-smoothing
        );
        font-weight: var(--paper-font-subhead_-_font-weight);
        line-height: var(--paper-font-subhead_-_line-height);
        width: 100%;
        opacity: var(--dark-primary-opacity);
        font-size: 14px;
        padding-bottom: 20px;
      }

      .horizontal .intro {
        max-width: 400px;
        margin-right: 40px;
      }

      .panel {
        margin-top: -24px;
      }

      .panel ::slotted(*) {
        margin-top: 24px;
        display: block;
      }

      .narrow.content {
        max-width: 640px;
      }
      .narrow .together {
        margin-top: 20px;
      }
      .narrow .intro {
        padding-bottom: 20px;
        margin-right: 0;
        max-width: 500px;
      }

      .full-width {
        padding: 0;
      }

      .full-width .layout {
        flex-direction: column;
      }
    `}}]}}),r.oi)},97740:(e,t,i)=>{i.a(e,(async e=>{var t=i(37500),r=i(33310),n=i(7323),o=i(42141),s=i(22311),a=i(8330),l=(i(31206),i(55422)),c=i(97389),d=i(65253),h=i(44198),u=e([l,h]);function p(){p=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(i){t.forEach((function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach((function(r){t.forEach((function(t){var n=t.placement;if(t.kind===r&&("static"===n||"prototype"===n)){var o="static"===n?e:i;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var r=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],r=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!y(e))return i.push(e);var t=this.decorateElement(e,n);i.push(t.element),i.push.apply(i,t.extras),r.push.apply(r,t.finishers)}),this),!t)return{elements:i,finishers:r};var o=this.decorateConstructor(i,t);return r.push.apply(r,o.finishers),o.finishers=r,o},addElementPlacement:function(e,t,i){var r=t[e.placement];if(!i&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var i=[],r=[],n=e.decorators,o=n.length-1;o>=0;o--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,n[o])(a)||a);e=l.element,this.addElementPlacement(e,t),l.finisher&&r.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);i.push.apply(i,c)}}return{element:e,finishers:r,extras:i}},decorateConstructor:function(e,t){for(var i=[],r=t.length-1;r>=0;r--){var n=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[r])(n)||n);if(void 0!==o.finisher&&i.push(o.finisher),void 0!==o.elements){e=o.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return w(e,t);var i=Object.prototype.toString.call(e).slice(8,-1);return"Object"===i&&e.constructor&&(i=e.constructor.name),"Map"===i||"Set"===i?Array.from(e):"Arguments"===i||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(i)?w(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=b(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:i,placement:r,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:g(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=g(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var r=(0,t[i])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}function f(e){var t,i=b(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function m(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function y(e){return e.decorators&&e.decorators.length}function v(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function g(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function b(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var r=i.call(e,t||"default");if("object"!=typeof r)return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function w(e,t){(null==t||t>e.length)&&(t=e.length);for(var i=0,r=new Array(t);i<t;i++)r[i]=e[i];return r}function k(e,t,i){return k="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,i){var r=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=_(e)););return e}(e,t);if(r){var n=Object.getOwnPropertyDescriptor(r,t);return n.get?n.get.call(i):n.value}},k(e,t,i||e)}function _(e){return _=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)},_(e)}[l,h]=u.then?await u:u;const E=(e,t)=>new Date(e.getTime()-1e3*t).getTime()/1e3,C=(e,t)=>(void 0!==e||void 0!==t)&&(!e||!t||e.length!==t.length||!e.every((e=>t.includes(e))));!function(e,t,i,r){var n=p();if(r)for(var o=0;o<r.length;o++)n=r[o](n);var s=t((function(e){n.initializeInstanceElements(e,a.elements)}),i),a=n.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},r=0;r<e.length;r++){var n,o=e[r];if("method"===o.kind&&(n=t.find(i)))if(v(o.descriptor)||v(n.descriptor)){if(y(o)||y(n))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");n.descriptor=o.descriptor}else{if(y(o)){if(y(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");n.decorators=o.decorators}m(o,n)}else t.push(o)}return t}(s.d.map(f)),e);n.initializeClassElements(s.F,a.elements),n.runClassFinishers(s.F,a.finishers)}([(0,r.Mo)("ha-logbook")],(function(e,i){class h extends i{constructor(...t){super(...t),e(this)}}return{F:h,d:[{kind:"field",decorators:[(0,r.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,r.Cb)()],key:"time",value:void 0},{kind:"field",decorators:[(0,r.Cb)()],key:"entityIds",value:void 0},{kind:"field",decorators:[(0,r.Cb)()],key:"deviceIds",value:void 0},{kind:"field",decorators:[(0,r.Cb)({type:Boolean,attribute:"narrow"})],key:"narrow",value:()=>!1},{kind:"field",decorators:[(0,r.Cb)({type:Boolean,attribute:"virtualize",reflect:!0})],key:"virtualize",value:()=>!1},{kind:"field",decorators:[(0,r.Cb)({type:Boolean,attribute:"no-icon"})],key:"noIcon",value:()=>!1},{kind:"field",decorators:[(0,r.Cb)({type:Boolean,attribute:"no-name"})],key:"noName",value:()=>!1},{kind:"field",decorators:[(0,r.Cb)({type:Boolean,attribute:"relative-time"})],key:"relativeTime",value:()=>!1},{kind:"field",decorators:[(0,r.Cb)({type:Boolean})],key:"showMoreLink",value:()=>!0},{kind:"field",decorators:[(0,r.SB)()],key:"_logbookEntries",value:void 0},{kind:"field",decorators:[(0,r.SB)()],key:"_traceContexts",value:()=>({})},{kind:"field",decorators:[(0,r.SB)()],key:"_userIdToName",value:()=>({})},{kind:"field",decorators:[(0,r.SB)()],key:"_error",value:void 0},{kind:"field",key:"_subscribed",value:void 0},{kind:"field",key:"_throttleGetLogbookEntries",value(){return(0,a.P)((()=>this._getLogBookData()),1e3)}},{kind:"method",key:"render",value:function(){return(0,n.p)(this.hass,"logbook")?this._error?t.dy`<div class="no-entries">
        ${`${this.hass.localize("ui.components.logbook.retrieval_error")}: ${this._error}`}
      </div>`:void 0===this._logbookEntries?t.dy`
        <div class="progress-wrapper">
          <ha-circular-progress
            active
            alt=${this.hass.localize("ui.common.loading")}
          ></ha-circular-progress>
        </div>
      `:0===this._logbookEntries.length?t.dy`<div class="no-entries">
        ${this.hass.localize("ui.components.logbook.entries_not_found")}
      </div>`:t.dy`
      <ha-logbook-renderer
        .hass=${this.hass}
        .narrow=${this.narrow}
        .virtualize=${this.virtualize}
        .noIcon=${this.noIcon}
        .noName=${this.noName}
        .relativeTime=${this.relativeTime}
        .entries=${this._logbookEntries}
        .traceContexts=${this._traceContexts}
        .userIdToName=${this._userIdToName}
      ></ha-logbook-renderer>
    `:t.dy``}},{kind:"method",key:"refresh",value:async function(e=!1){(e||!this._subscribed&&void 0!==this._logbookEntries)&&(this._unsubscribe(),this._throttleGetLogbookEntries.cancel(),this._updateTraceContexts.cancel(),this._updateUsers.cancel(),"range"in this.time&&(0,l.tf)(this.time.range[0].toISOString(),this.time.range[1].toISOString()),this._logbookEntries=void 0,this._throttleGetLogbookEntries())}},{kind:"method",key:"updated",value:function(e){k(_(h.prototype),"updated",this).call(this,e);let t=e.has("time");for(const i of["entityIds","deviceIds"]){if(!e.has(i))continue;const r=e.get(i),n=this[i];if(C(r,n)){t=!0;break}}t&&this.refresh(!0)}},{kind:"get",key:"_filterAlwaysEmptyResults",value:function(){const e=(0,o.r)(this.entityIds),t=(0,o.r)(this.deviceIds);return(e||t)&&(!e||0===e.length)&&(!t||0===t.length)}},{kind:"method",key:"_unsubscribe",value:function(){this._subscribed&&(this._subscribed.then((e=>e?e():void 0)),this._subscribed=void 0)}},{kind:"method",key:"connectedCallback",value:function(){k(_(h.prototype),"connectedCallback",this).call(this),this.hasUpdated&&this._subscribeLogbookPeriod(this._calculateLogbookPeriod())}},{kind:"method",key:"disconnectedCallback",value:function(){k(_(h.prototype),"disconnectedCallback",this).call(this),this._unsubscribe()}},{kind:"method",key:"_unsubscribeAndEmptyEntries",value:function(){this._unsubscribe(),this._logbookEntries=[]}},{kind:"method",key:"_calculateLogbookPeriod",value:function(){const e=new Date;if("range"in this.time)return{now:e,startTime:this.time.range[0],endTime:this.time.range[1],purgeBeforePythonTime:void 0};if("recent"in this.time){const t=E(e,this.time.recent);return{now:e,startTime:new Date(1e3*t),endTime:new Date(e.getTime()+31536e6),purgeBeforePythonTime:E(e,this.time.recent)}}throw new Error("Unexpected time specified")}},{kind:"method",key:"_subscribeLogbookPeriod",value:function(e){return this._subscribed||(this._subscribed=(0,l.Yc)(this.hass,(e=>{this._processStreamMessage(e,"recent"in this.time?E(new Date,this.time.recent):void 0)}),e.startTime.toISOString(),e.endTime.toISOString(),(0,o.r)(this.entityIds),(0,o.r)(this.deviceIds)).catch((e=>{this._error=e.message,this._subscribed=void 0}))),!0}},{kind:"method",key:"_getLogBookData",value:async function(){var e;if(this._error=void 0,this._filterAlwaysEmptyResults)return void this._unsubscribeAndEmptyEntries();const t=this._calculateLogbookPeriod();t.startTime>t.now?this._unsubscribeAndEmptyEntries():(this._updateUsers(),null!==(e=this.hass.user)&&void 0!==e&&e.is_admin&&this._updateTraceContexts(),this._subscribeLogbookPeriod(t))}},{kind:"field",key:"_nonExpiredRecords",value(){return e=>this._logbookEntries?e?this._logbookEntries.filter((t=>t.when>e)):this._logbookEntries:[]}},{kind:"field",key:"_processStreamMessage",value(){return(e,t)=>{const i=[...e.events].reverse();if(!this._logbookEntries||!this._logbookEntries.length)return void(this._logbookEntries=i);if(!i.length)return;const r=this._nonExpiredRecords(t);this._logbookEntries=r.length?i[0].when>=r[0].when?i.concat(r):r.concat(i):i}}},{kind:"field",key:"_updateTraceContexts",value(){return(0,a.P)((async()=>{this._traceContexts=await(0,c.U_)(this.hass)}),6e4)}},{kind:"field",key:"_updateUsers",value(){return(0,a.P)((async()=>{var e;const t={},i=(null===(e=this.hass.user)||void 0===e?void 0:e.is_admin)&&(0,d.uh)(this.hass);for(const e of Object.values(this.hass.states))e.attributes.user_id&&"person"===(0,s.N)(e)&&(t[e.attributes.user_id]=e.attributes.friendly_name);if(i){const e=await i;for(const i of e)i.id in t||(t[i.id]=i.name)}this._userIdToName=t}),6e4)}},{kind:"get",static:!0,key:"styles",value:function(){return[t.iv`
        :host {
          display: block;
        }

        :host([virtualize]) {
          height: 100%;
        }

        .no-entries {
          text-align: center;
          padding: 16px;
          color: var(--secondary-text-color);
        }

        .progress-wrapper {
          display: flex;
          justify-content: center;
          height: 100%;
          align-items: center;
        }
      `]}}]}}),t.oi)}))},7778:(e,t,i)=>{i.d(t,{Pc:()=>o,N2:()=>s,Tw:()=>d,Xm:()=>h,ED:()=>u});var r=i(47181),n=i(9893);const o=e=>{const t=document.createElement("hui-error-card");return customElements.get("hui-error-card")?t.setConfig(e):(Promise.all([i.e(77426),i.e(55796)]).then(i.bind(i,55796)),customElements.whenDefined("hui-error-card").then((()=>{customElements.upgrade(t),t.setConfig(e)}))),t},s=(e,t)=>({type:"error",error:e,origConfig:t}),a=(e,t)=>{const i=document.createElement(e);return i.setConfig(t),i},l=(e,t)=>o(s(e,t)),c=e=>e.startsWith(n.Qo)?e.substr(n.Qo.length):void 0,d=(e,t,i,r,n,o)=>{try{return h(e,t,i,r,n,o)}catch(i){return console.error(e,t.type,i),l(i.message,t)}},h=(e,t,i,n,o,s)=>{if(!t||"object"!=typeof t)throw new Error("Config is not an object");if(!(t.type||s||o&&"entity"in t))throw new Error("No card type configured");const d=t.type?c(t.type):void 0;if(d)return((e,t)=>{if(customElements.get(e))return a(e,t);const i=l(`Custom element doesn't exist: ${e}.`,t);if(!e.includes("-"))return i;i.style.display="None";const n=window.setTimeout((()=>{i.style.display=""}),2e3);return customElements.whenDefined(e).then((()=>{clearTimeout(n),(0,r.B)(i,"ll-rebuild")})),i})(d,t);let h;if(o&&!t.type&&t.entity){h=`${o[t.entity.split(".",1)[0]]||o._domain_not_found}-entity`}else h=t.type||s;if(void 0===h)throw new Error("No type specified");const u=`hui-${h}-${e}`;if(n&&h in n)return n[h](),((e,t)=>{if(customElements.get(e))return a(e,t);const i=document.createElement(e);return customElements.whenDefined(e).then((()=>{try{customElements.upgrade(i),i.setConfig(t)}catch(e){(0,r.B)(i,"ll-rebuild")}})),i})(u,t);if(i&&i.has(h))return a(u,t);throw new Error(`Unknown type encountered: ${h}`)},u=async(e,t,i,r)=>{const n=c(e);if(n){const e=customElements.get(n);if(e)return e;if(!n.includes("-"))throw new Error(`Custom element not found: ${n}`);return new Promise(((e,t)=>{setTimeout((()=>t(new Error(`Custom element not found: ${n}`))),2e3),customElements.whenDefined(n).then((()=>e(customElements.get(n))))}))}const o=`hui-${e}-${t}`,s=customElements.get(o);if(i&&i.has(e))return s;if(r&&e in r)return s||r[e]().then((()=>customElements.get(o)));throw new Error(`Unknown type: ${e}`)}},37482:(e,t,i)=>{i.a(e,(async e=>{i.d(t,{m:()=>m,T:()=>y});var r=i(12141),n=i(31479),o=i(23266),s=i(65716),a=i(97600),l=i(83896),c=i(45340),d=(i(56427),i(23658),i(7778)),h=e([c,l,a,s,o,n,r]);[c,l,a,s,o,n,r]=h.then?await h:h;const u=new Set(["media-player-entity","scene-entity","script-entity","sensor-entity","text-entity","toggle-entity","button","call-service"]),p={"button-entity":()=>i.e(85611).then(i.bind(i,85611)),"climate-entity":()=>i.e(35642).then(i.bind(i,35642)),"cover-entity":()=>i.e(16755).then(i.bind(i,16755)),"group-entity":()=>i.e(81534).then(i.bind(i,81534)),"input-button-entity":()=>i.e(83968).then(i.bind(i,83968)),"humidifier-entity":()=>i.e(41102).then(i.bind(i,41102)),"input-datetime-entity":()=>Promise.all([i.e(29563),i.e(98985),i.e(24103),i.e(59799),i.e(6294),i.e(88278),i.e(12545),i.e(56222)]).then(i.bind(i,22350)),"input-number-entity":()=>Promise.all([i.e(29563),i.e(98985),i.e(12335)]).then(i.bind(i,12335)),"input-select-entity":()=>Promise.all([i.e(29563),i.e(24103),i.e(59799),i.e(6294),i.e(88278),i.e(91754)]).then(i.bind(i,25675)),"input-text-entity":()=>Promise.all([i.e(29563),i.e(98985),i.e(73943)]).then(i.bind(i,73943)),"lock-entity":()=>i.e(61596).then(i.bind(i,61596)),"number-entity":()=>Promise.all([i.e(29563),i.e(98985),i.e(66778)]).then(i.bind(i,66778)),"select-entity":()=>Promise.all([i.e(29563),i.e(24103),i.e(59799),i.e(6294),i.e(88278),i.e(83190)]).then(i.bind(i,35994)),"timer-entity":()=>i.e(31203).then(i.bind(i,31203)),conditional:()=>i.e(97749).then(i.bind(i,97749)),"weather-entity":()=>i.e(71850).then(i.bind(i,71850)),divider:()=>i.e(41930).then(i.bind(i,41930)),section:()=>i.e(94832).then(i.bind(i,94832)),weblink:()=>i.e(44689).then(i.bind(i,44689)),cast:()=>i.e(25840).then(i.bind(i,25840)),buttons:()=>Promise.all([i.e(42109),i.e(82137)]).then(i.bind(i,82137)),attribute:()=>Promise.resolve().then(i.bind(i,45340)),text:()=>i.e(63459).then(i.bind(i,63459))},f={_domain_not_found:"text",alert:"toggle",automation:"toggle",button:"button",climate:"climate",cover:"cover",fan:"toggle",group:"group",humidifier:"humidifier",input_boolean:"toggle",input_button:"input-button",input_number:"input-number",input_select:"input-select",input_text:"input-text",light:"toggle",lock:"lock",media_player:"media-player",number:"number",remote:"toggle",scene:"scene",script:"script",select:"select",sensor:"sensor",siren:"toggle",switch:"toggle",timer:"timer",vacuum:"toggle",water_heater:"climate",input_datetime:"input-datetime",weather:"weather"},m=e=>(0,d.Tw)("row",e,u,p,f,void 0),y=e=>(0,d.ED)(e,"row",u,p)}))},96491:(e,t,i)=>{i.d(t,{$:()=>a});var r=i(15327),n=i(26765),o=i(47512),s=i(4398);const a=async(e,t,i,a)=>{var l,c,d;t.loadFragmentTranslation("lovelace");const h=await(0,r.j2)(t),u=h.filter((e=>"storage"===e.mode)),p=null===(l=t.panels.lovelace)||void 0===l||null===(c=l.config)||void 0===c?void 0:c.mode;if("storage"!==p&&!u.length)return void(0,o.f)(e,{entities:i,yaml:!0,cardTitle:a});let f,m=null;if("storage"===p)try{f=await(0,r.Q2)(t.connection,null,!1)}catch(e){}if(!f&&u.length)for(const e of u)try{f=await(0,r.Q2)(t.connection,e.url_path,!1),m=e.url_path;break}catch(e){}f?u.length||null!==(d=f.views)&&void 0!==d&&d.length?u.length||1!==f.views.length?(0,s.i)(e,{lovelaceConfig:f,urlPath:m,allowDashboardChange:!0,actionLabel:t.localize("ui.common.next"),dashboards:h,viewSelectedCallback:(n,s,l)=>{(0,o.f)(e,{cardTitle:a,lovelaceConfig:s,saveConfig:async e=>{try{await(0,r.Oh)(t,n,e)}catch{alert(t.localize("ui.panel.config.devices.add_entities.saving_failed"))}},path:[l],entities:i})}}):(0,o.f)(e,{cardTitle:a,lovelaceConfig:f,saveConfig:async e=>{try{await(0,r.Oh)(t,null,e)}catch(e){alert(t.localize("ui.panel.config.devices.add_entities.saving_failed"))}},path:[0],entities:i}):(0,n.Ys)(e,{text:"You don't have any Lovelace views, first create a view in Lovelace."}):h.length>u.length?(0,o.f)(e,{entities:i,yaml:!0,cardTitle:a}):(0,n.Ys)(e,{text:"You don't seem to be in control of any dashboard, please take control first."})}},47512:(e,t,i)=>{i.d(t,{f:()=>o});var r=i(47181);const n=()=>Promise.all([i.e(77426),i.e(34176),i.e(53822),i.e(87683),i.e(90404),i.e(94994)]).then(i.bind(i,9444)),o=(e,t)=>{(0,r.B)(e,"show-dialog",{dialogTag:"hui-dialog-suggest-card",dialogImport:n,dialogParams:t})}},4398:(e,t,i)=>{i.d(t,{i:()=>n});var r=i(47181);const n=(e,t)=>{(0,r.B)(e,"show-dialog",{dialogTag:"hui-dialog-select-view",dialogImport:()=>Promise.all([i.e(29563),i.e(88278),i.e(85084),i.e(45507),i.e(66138)]).then(i.bind(i,66138)),dialogParams:t})}},11254:(e,t,i)=>{i.d(t,{X1:()=>r,RU:()=>n,u4:()=>o,zC:()=>s});const r=e=>e.domain.startsWith("ais_")?`https://ai-speaker.com/images/brands/${e.domain}/${e.type}.png`:`https://brands.home-assistant.io/${e.useFallback?"_/":""}${e.domain}/${e.darkOptimized?"dark_":""}${e.type}.png`,n=e=>`https://brands.home-assistant.io/hardware/${e.category}/${e.darkOptimized?"dark_":""}${e.manufacturer}${e.model?`_${e.model}`:""}.png`,o=e=>e.split("/")[4],s=e=>e.startsWith("https://brands.home-assistant.io/")},25936:(e,t,i)=>{i.d(t,{N:()=>r});const r=(e,t="")=>{const i=document.createElement("a");i.target="_blank",i.href=e,i.download=t,document.body.appendChild(i),i.dispatchEvent(new MouseEvent("click")),document.body.removeChild(i)}}}]);
//# sourceMappingURL=c31e320d.js.map
import{l as t,o as e,g as i,i as a,j as s,k as n,p as o,q as r,u as l,v as c,w as d,x as h,y as u,z as p,A as m,B as f,C as _,D as b,E as g,F as y,G as v,I as w,J as k,K as x,L as E,M as C,N as O,O as R,P as L,Q as $,R as S,S as A,T as z,U as I,V as T,W as M,X as j,Y as F,Z as B,a0 as D,a1 as P,a2 as N,a3 as H,a4 as U,a5 as V,a6 as q,a7 as X,a8 as Y,a9 as K,aa as W,ab as G,ac as J,ad as Q,ae as Z,af as tt,ag as et,ah as it,f as at,ai as st,aj as nt,ak as ot,al as rt,e as lt,am as ct,an as dt,$ as ht,ao as ut,ap as pt,_ as mt,n as ft,aq as _t,ar as bt,t as gt,as as yt,at as vt,au as wt,av as kt,aw as xt,ax as Et,s as Ct,ay as Ot,az as Rt,aA as Lt,aB as $t,aC as St,aD as At,aE as zt,aF as It,aG as Tt,aH as Mt,aI as jt,aJ as Ft,aK as Bt,aL as Dt,aM as Pt,aN as Nt,aO as Ht,aP as Ut,aQ as Vt,aR as qt,aS as Xt,aT as Yt,aU as Kt,aV as Wt,aW as Gt,aX as Jt,aY as Qt,aZ as Zt,a_ as te,a$ as ee,b0 as ie,b1 as ae,b2 as se,b3 as ne,b4 as oe,b5 as re,b6 as le,b7 as ce,b8 as de,b9 as he,ba as ue,bb as pe,bc as me,bd as fe,be as _e,bf as be,bg as ge,bh as ye,bi as ve,bj as we,bk as ke,bl as xe,bm as Ee,bn as Ce,bo as Oe,bp as Re,bq as Le,br as $e,bs as Se,bt as Ae,bu as ze,bv as Ie,bw as Te,bx as Me,by as je,bz as Fe,bA as Be,bB as De,bC as Pe,bD as Ne,bE as He,bF as Ue,bG as Ve,bH as qe,bI as Xe,bJ as Ye,bK as Ke,bL as We,bM as Ge,bN as Je,bO as Qe,bP as Ze,bQ as ti,bR as ei,bS as ii,bT as ai,bU as si,bV as ni,bW as oi,bX as ri,bY as li,bZ as ci,b_ as di,b$ as hi,c0 as ui,c1 as pi,c2 as mi,c3 as fi,c4 as _i,c5 as bi,c6 as gi,c7 as yi,c8 as vi,c9 as wi,ca as ki,cb as xi,cc as Ei,cd as Ci,ce as Oi,cf as Ri,cg as Li,ch as $i,ci as Si,cj as Ai,ck as zi,cl as Ii,cm as Ti}from"./main-4b1ba1ae.js";function Mi(i,a,s){let n,o=i;return"object"==typeof i?(o=i.slot,n=i):n={flatten:a},s?t({slot:o,flatten:a,selector:s}):e({descriptor:t=>({get(){var t,e;const i="slot"+(o?`[name=${o}]`:":not([name])"),a=null===(t=this.renderRoot)||void 0===t?void 0:t.querySelector(i);return null!==(e=null==a?void 0:a.assignedNodes(n))&&void 0!==e?e:[]},enumerable:!0,configurable:!0})})}const ji=t=>t.substr(0,t.indexOf(".")),Fi=t=>ji(t.entity_id),Bi=(t,e,i=!1)=>{let a;const s=(...s)=>{const n=i&&!a;clearTimeout(a),a=window.setTimeout((()=>{a=void 0,i||t(...s)}),e),n&&t(...s)};return s.cancel=()=>{clearTimeout(a)},s},Di=i,Pi={alert:a,air_quality:s,automation:n,calendar:o,camera:r,climate:l,configurator:c,conversation:d,counter:h,fan:u,google_assistant:p,group:m,homeassistant:f,homekit:_,image_processing:b,input_button:g,input_datetime:y,input_number:v,input_select:w,input_text:k,light:x,mailbox:E,notify:C,number:v,persistent_notification:O,person:R,plant:L,proximity:$,remote:S,scene:A,script:z,select:w,sensor:I,siren:T,simple_alarm:O,sun:M,timer:j,updater:F,vacuum:B,water_heater:D,weather:P,zone:N},Ni={apparent_power:H,aqi:s,carbon_dioxide:U,carbon_monoxide:V,current:q,date:o,energy:X,frequency:Y,gas:K,humidity:W,illuminance:G,monetary:J,nitrogen_dioxide:Q,nitrogen_monoxide:Q,nitrous_oxide:Q,ozone:Q,pm1:Q,pm10:Q,pm25:Q,power:H,power_factor:Z,pressure:tt,reactive_power:H,signal_strength:et,sulphur_dioxide:Q,temperature:D,timestamp:it,volatile_organic_compounds:Q,voltage:Y},Hi=["closed","locked","off"],Ui="on",Vi="off",qi=new Set(["camera","media_player"]),Xi=t=>{return void 0===t.attributes.friendly_name?(e=t.entity_id,e.substr(e.indexOf(".")+1)).replace(/_/g," "):t.attributes.friendly_name||"";var e},Yi="unavailable",Ki="unknown",Wi=["unavailable","unknown"],Gi=t=>{at(window,"haptic",t)};var Ji,Qi,Zi={ROOT:"mdc-form-field"},ta={LABEL_SELECTOR:".mdc-form-field > label"},ea=function(t){function e(i){var a=t.call(this,nt(nt({},e.defaultAdapter),i))||this;return a.click=function(){a.handleClick()},a}return st(e,t),Object.defineProperty(e,"cssClasses",{get:function(){return Zi},enumerable:!1,configurable:!0}),Object.defineProperty(e,"strings",{get:function(){return ta},enumerable:!1,configurable:!0}),Object.defineProperty(e,"defaultAdapter",{get:function(){return{activateInputRipple:function(){},deactivateInputRipple:function(){},deregisterInteractionHandler:function(){},registerInteractionHandler:function(){}}},enumerable:!1,configurable:!0}),e.prototype.init=function(){this.adapter.registerInteractionHandler("click",this.click)},e.prototype.destroy=function(){this.adapter.deregisterInteractionHandler("click",this.click)},e.prototype.handleClick=function(){var t=this;this.adapter.activateInputRipple(),requestAnimationFrame((function(){t.adapter.deactivateInputRipple()}))},e}(ot);const ia=null!==(Qi=null===(Ji=window.ShadyDOM)||void 0===Ji?void 0:Ji.inUse)&&void 0!==Qi&&Qi;class aa extends ct{constructor(){super(...arguments),this.disabled=!1,this.containingForm=null,this.formDataListener=t=>{this.disabled||this.setFormData(t.formData)}}findFormElement(){if(!this.shadowRoot||ia)return null;const t=this.getRootNode().querySelectorAll("form");for(const e of Array.from(t))if(e.contains(this))return e;return null}connectedCallback(){var t;super.connectedCallback(),this.containingForm=this.findFormElement(),null===(t=this.containingForm)||void 0===t||t.addEventListener("formdata",this.formDataListener)}disconnectedCallback(){var t;super.disconnectedCallback(),null===(t=this.containingForm)||void 0===t||t.removeEventListener("formdata",this.formDataListener),this.containingForm=null}click(){this.formElement&&!this.disabled&&(this.formElement.focus(),this.formElement.click())}firstUpdated(){super.firstUpdated(),this.shadowRoot&&this.mdcRoot.addEventListener("change",(t=>{this.dispatchEvent(new Event("change",t))}))}}aa.shadowRootOptions={mode:"open",delegatesFocus:!0},rt([lt({type:Boolean})],aa.prototype,"disabled",void 0);const sa=t=>(e,i)=>{if(e.constructor._observers){if(!e.constructor.hasOwnProperty("_observers")){const t=e.constructor._observers;e.constructor._observers=new Map,t.forEach(((t,i)=>e.constructor._observers.set(i,t)))}}else{e.constructor._observers=new Map;const t=e.updated;e.updated=function(e){t.call(this,e),e.forEach(((t,e)=>{const i=this.constructor._observers.get(e);void 0!==i&&i.call(this,this[e],t)}))}}e.constructor._observers.set(i,t)};class na extends ct{constructor(){super(...arguments),this.alignEnd=!1,this.spaceBetween=!1,this.nowrap=!1,this.label="",this.mdcFoundationClass=ea}createAdapter(){return{registerInteractionHandler:(t,e)=>{this.labelEl.addEventListener(t,e)},deregisterInteractionHandler:(t,e)=>{this.labelEl.removeEventListener(t,e)},activateInputRipple:async()=>{const t=this.input;if(t instanceof aa){const e=await t.ripple;e&&e.startPress()}},deactivateInputRipple:async()=>{const t=this.input;if(t instanceof aa){const e=await t.ripple;e&&e.endPress()}}}}get input(){var t,e;return null!==(e=null===(t=this.slottedInputs)||void 0===t?void 0:t[0])&&void 0!==e?e:null}render(){const t={"mdc-form-field--align-end":this.alignEnd,"mdc-form-field--space-between":this.spaceBetween,"mdc-form-field--nowrap":this.nowrap};return ht`
      <div class="mdc-form-field ${ut(t)}">
        <slot></slot>
        <label class="mdc-label"
               @click="${this._labelClick}">${this.label}</label>
      </div>`}click(){this._labelClick()}_labelClick(){const t=this.input;t&&(t.focus(),t.click())}}rt([lt({type:Boolean})],na.prototype,"alignEnd",void 0),rt([lt({type:Boolean})],na.prototype,"spaceBetween",void 0),rt([lt({type:Boolean})],na.prototype,"nowrap",void 0),rt([lt({type:String}),sa((async function(t){var e;null===(e=this.input)||void 0===e||e.setAttribute("aria-label",t)}))],na.prototype,"label",void 0),rt([dt(".mdc-form-field")],na.prototype,"mdcRoot",void 0),rt([Mi("",!0,"*")],na.prototype,"slottedInputs",void 0),rt([dt("label")],na.prototype,"labelEl",void 0);const oa=pt`.mdc-form-field{-moz-osx-font-smoothing:grayscale;-webkit-font-smoothing:antialiased;font-family:Roboto, sans-serif;font-family:var(--mdc-typography-body2-font-family, var(--mdc-typography-font-family, Roboto, sans-serif));font-size:0.875rem;font-size:var(--mdc-typography-body2-font-size, 0.875rem);line-height:1.25rem;line-height:var(--mdc-typography-body2-line-height, 1.25rem);font-weight:400;font-weight:var(--mdc-typography-body2-font-weight, 400);letter-spacing:0.0178571429em;letter-spacing:var(--mdc-typography-body2-letter-spacing, 0.0178571429em);text-decoration:inherit;text-decoration:var(--mdc-typography-body2-text-decoration, inherit);text-transform:inherit;text-transform:var(--mdc-typography-body2-text-transform, inherit);color:rgba(0, 0, 0, 0.87);color:var(--mdc-theme-text-primary-on-background, rgba(0, 0, 0, 0.87));display:inline-flex;align-items:center;vertical-align:middle}.mdc-form-field>label{margin-left:0;margin-right:auto;padding-left:4px;padding-right:0;order:0}[dir=rtl] .mdc-form-field>label,.mdc-form-field>label[dir=rtl]{margin-left:auto;margin-right:0}[dir=rtl] .mdc-form-field>label,.mdc-form-field>label[dir=rtl]{padding-left:0;padding-right:4px}.mdc-form-field--nowrap>label{text-overflow:ellipsis;overflow:hidden;white-space:nowrap}.mdc-form-field--align-end>label{margin-left:auto;margin-right:0;padding-left:0;padding-right:4px;order:-1}[dir=rtl] .mdc-form-field--align-end>label,.mdc-form-field--align-end>label[dir=rtl]{margin-left:0;margin-right:auto}[dir=rtl] .mdc-form-field--align-end>label,.mdc-form-field--align-end>label[dir=rtl]{padding-left:4px;padding-right:0}.mdc-form-field--space-between{justify-content:space-between}.mdc-form-field--space-between>label{margin:0}[dir=rtl] .mdc-form-field--space-between>label,.mdc-form-field--space-between>label[dir=rtl]{margin:0}:host{display:inline-flex}.mdc-form-field{width:100%}::slotted(*){-moz-osx-font-smoothing:grayscale;-webkit-font-smoothing:antialiased;font-family:Roboto, sans-serif;font-family:var(--mdc-typography-body2-font-family, var(--mdc-typography-font-family, Roboto, sans-serif));font-size:0.875rem;font-size:var(--mdc-typography-body2-font-size, 0.875rem);line-height:1.25rem;line-height:var(--mdc-typography-body2-line-height, 1.25rem);font-weight:400;font-weight:var(--mdc-typography-body2-font-weight, 400);letter-spacing:0.0178571429em;letter-spacing:var(--mdc-typography-body2-letter-spacing, 0.0178571429em);text-decoration:inherit;text-decoration:var(--mdc-typography-body2-text-decoration, inherit);text-transform:inherit;text-transform:var(--mdc-typography-body2-text-transform, inherit);color:rgba(0, 0, 0, 0.87);color:var(--mdc-theme-text-primary-on-background, rgba(0, 0, 0, 0.87))}::slotted(mwc-switch){margin-right:10px}[dir=rtl] ::slotted(mwc-switch),::slotted(mwc-switch[dir=rtl]){margin-left:10px}`;mt([ft("ha-formfield")],(function(t,e){return{F:class extends e{constructor(...e){super(...e),t(this)}},d:[{kind:"method",key:"_labelClick",value:function(){const t=this.input;if(t)switch(t.focus(),t.tagName){case"HA-CHECKBOX":case"HA-RADIO":t.checked=!t.checked,at(t,"change");break;default:t.click()}}},{kind:"field",static:!0,key:"styles",value:()=>[oa,pt`
      :host(:not([alignEnd])) ::slotted(ha-switch) {
        margin-right: 10px;
      }
      :host([dir="rtl"]:not([alignEnd])) ::slotted(ha-switch) {
        margin-left: 10px;
        margin-right: auto;
      }
    `]}]}}),na);var ra={CHECKED:"mdc-switch--checked",DISABLED:"mdc-switch--disabled"},la={ARIA_CHECKED_ATTR:"aria-checked",NATIVE_CONTROL_SELECTOR:".mdc-switch__native-control",RIPPLE_SURFACE_SELECTOR:".mdc-switch__thumb-underlay"},ca=function(t){function e(i){return t.call(this,nt(nt({},e.defaultAdapter),i))||this}return st(e,t),Object.defineProperty(e,"strings",{get:function(){return la},enumerable:!1,configurable:!0}),Object.defineProperty(e,"cssClasses",{get:function(){return ra},enumerable:!1,configurable:!0}),Object.defineProperty(e,"defaultAdapter",{get:function(){return{addClass:function(){},removeClass:function(){},setNativeControlChecked:function(){},setNativeControlDisabled:function(){},setNativeControlAttr:function(){}}},enumerable:!1,configurable:!0}),e.prototype.setChecked=function(t){this.adapter.setNativeControlChecked(t),this.updateAriaChecked(t),this.updateCheckedStyling(t)},e.prototype.setDisabled=function(t){this.adapter.setNativeControlDisabled(t),t?this.adapter.addClass(ra.DISABLED):this.adapter.removeClass(ra.DISABLED)},e.prototype.handleChange=function(t){var e=t.target;this.updateAriaChecked(e.checked),this.updateCheckedStyling(e.checked)},e.prototype.updateCheckedStyling=function(t){t?this.adapter.addClass(ra.CHECKED):this.adapter.removeClass(ra.CHECKED)},e.prototype.updateAriaChecked=function(t){this.adapter.setNativeControlAttr(la.ARIA_CHECKED_ATTR,""+!!t)},e}(ot);class da extends ct{constructor(){super(...arguments),this.checked=!1,this.disabled=!1,this.shouldRenderRipple=!1,this.mdcFoundationClass=ca,this.rippleHandlers=new vt((()=>(this.shouldRenderRipple=!0,this.ripple)))}changeHandler(t){this.mdcFoundation.handleChange(t),this.checked=this.formElement.checked}createAdapter(){return Object.assign(Object.assign({},wt(this.mdcRoot)),{setNativeControlChecked:t=>{this.formElement.checked=t},setNativeControlDisabled:t=>{this.formElement.disabled=t},setNativeControlAttr:(t,e)=>{this.formElement.setAttribute(t,e)}})}renderRipple(){return this.shouldRenderRipple?ht`
        <mwc-ripple
          .accent="${this.checked}"
          .disabled="${this.disabled}"
          unbounded>
        </mwc-ripple>`:""}focus(){const t=this.formElement;t&&(this.rippleHandlers.startFocus(),t.focus())}blur(){const t=this.formElement;t&&(this.rippleHandlers.endFocus(),t.blur())}click(){this.formElement&&!this.disabled&&(this.formElement.focus(),this.formElement.click())}firstUpdated(){super.firstUpdated(),this.shadowRoot&&this.mdcRoot.addEventListener("change",(t=>{this.dispatchEvent(new Event("change",t))}))}render(){return ht`
      <div class="mdc-switch">
        <div class="mdc-switch__track"></div>
        <div class="mdc-switch__thumb-underlay">
          ${this.renderRipple()}
          <div class="mdc-switch__thumb">
            <input
              type="checkbox"
              id="basic-switch"
              class="mdc-switch__native-control"
              role="switch"
              aria-label="${kt(this.ariaLabel)}"
              aria-labelledby="${kt(this.ariaLabelledBy)}"
              @change="${this.changeHandler}"
              @focus="${this.handleRippleFocus}"
              @blur="${this.handleRippleBlur}"
              @mousedown="${this.handleRippleMouseDown}"
              @mouseenter="${this.handleRippleMouseEnter}"
              @mouseleave="${this.handleRippleMouseLeave}"
              @touchstart="${this.handleRippleTouchStart}"
              @touchend="${this.handleRippleDeactivate}"
              @touchcancel="${this.handleRippleDeactivate}">
          </div>
        </div>
      </div>`}handleRippleMouseDown(t){const e=()=>{window.removeEventListener("mouseup",e),this.handleRippleDeactivate()};window.addEventListener("mouseup",e),this.rippleHandlers.startPress(t)}handleRippleTouchStart(t){this.rippleHandlers.startPress(t)}handleRippleDeactivate(){this.rippleHandlers.endPress()}handleRippleMouseEnter(){this.rippleHandlers.startHover()}handleRippleMouseLeave(){this.rippleHandlers.endHover()}handleRippleFocus(){this.rippleHandlers.startFocus()}handleRippleBlur(){this.rippleHandlers.endFocus()}}rt([lt({type:Boolean}),sa((function(t){this.mdcFoundation.setChecked(t)}))],da.prototype,"checked",void 0),rt([lt({type:Boolean}),sa((function(t){this.mdcFoundation.setDisabled(t)}))],da.prototype,"disabled",void 0),rt([_t,lt({attribute:"aria-label"})],da.prototype,"ariaLabel",void 0),rt([_t,lt({attribute:"aria-labelledby"})],da.prototype,"ariaLabelledBy",void 0),rt([dt(".mdc-switch")],da.prototype,"mdcRoot",void 0),rt([dt("input")],da.prototype,"formElement",void 0),rt([bt("mwc-ripple")],da.prototype,"ripple",void 0),rt([gt()],da.prototype,"shouldRenderRipple",void 0),rt([yt({passive:!0})],da.prototype,"handleRippleMouseDown",null),rt([yt({passive:!0})],da.prototype,"handleRippleTouchStart",null);const ha=pt`.mdc-switch__thumb-underlay{left:-14px;right:initial;top:-17px;width:48px;height:48px}[dir=rtl] .mdc-switch__thumb-underlay,.mdc-switch__thumb-underlay[dir=rtl]{left:initial;right:-14px}.mdc-switch__native-control{width:64px;height:48px}.mdc-switch{display:inline-block;position:relative;outline:none;user-select:none}.mdc-switch.mdc-switch--checked .mdc-switch__track{background-color:#018786;background-color:var(--mdc-theme-secondary, #018786)}.mdc-switch.mdc-switch--checked .mdc-switch__thumb{background-color:#018786;background-color:var(--mdc-theme-secondary, #018786);border-color:#018786;border-color:var(--mdc-theme-secondary, #018786)}.mdc-switch:not(.mdc-switch--checked) .mdc-switch__track{background-color:#000;background-color:var(--mdc-theme-on-surface, #000)}.mdc-switch:not(.mdc-switch--checked) .mdc-switch__thumb{background-color:#fff;background-color:var(--mdc-theme-surface, #fff);border-color:#fff;border-color:var(--mdc-theme-surface, #fff)}.mdc-switch__native-control{left:0;right:initial;position:absolute;top:0;margin:0;opacity:0;cursor:pointer;pointer-events:auto;transition:transform 90ms cubic-bezier(0.4, 0, 0.2, 1)}[dir=rtl] .mdc-switch__native-control,.mdc-switch__native-control[dir=rtl]{left:initial;right:0}.mdc-switch__track{box-sizing:border-box;width:36px;height:14px;border:1px solid transparent;border-radius:7px;opacity:.38;transition:opacity 90ms cubic-bezier(0.4, 0, 0.2, 1),background-color 90ms cubic-bezier(0.4, 0, 0.2, 1),border-color 90ms cubic-bezier(0.4, 0, 0.2, 1)}.mdc-switch__thumb-underlay{display:flex;position:absolute;align-items:center;justify-content:center;transform:translateX(0);transition:transform 90ms cubic-bezier(0.4, 0, 0.2, 1),background-color 90ms cubic-bezier(0.4, 0, 0.2, 1),border-color 90ms cubic-bezier(0.4, 0, 0.2, 1)}.mdc-switch__thumb{box-shadow:0px 3px 1px -2px rgba(0, 0, 0, 0.2),0px 2px 2px 0px rgba(0, 0, 0, 0.14),0px 1px 5px 0px rgba(0,0,0,.12);box-sizing:border-box;width:20px;height:20px;border:10px solid;border-radius:50%;pointer-events:none;z-index:1}.mdc-switch--checked .mdc-switch__track{opacity:.54}.mdc-switch--checked .mdc-switch__thumb-underlay{transform:translateX(16px)}[dir=rtl] .mdc-switch--checked .mdc-switch__thumb-underlay,.mdc-switch--checked .mdc-switch__thumb-underlay[dir=rtl]{transform:translateX(-16px)}.mdc-switch--checked .mdc-switch__native-control{transform:translateX(-16px)}[dir=rtl] .mdc-switch--checked .mdc-switch__native-control,.mdc-switch--checked .mdc-switch__native-control[dir=rtl]{transform:translateX(16px)}.mdc-switch--disabled{opacity:.38;pointer-events:none}.mdc-switch--disabled .mdc-switch__thumb{border-width:1px}.mdc-switch--disabled .mdc-switch__native-control{cursor:default;pointer-events:none}:host{display:inline-flex;outline:none;-webkit-tap-highlight-color:transparent}`;mt([ft("ha-switch")],(function(t,e){class i extends e{constructor(...e){super(...e),t(this)}}return{F:i,d:[{kind:"field",decorators:[lt({type:Boolean})],key:"haptic",value:()=>!1},{kind:"method",key:"firstUpdated",value:function(){xt(Et(i.prototype),"firstUpdated",this).call(this),this.addEventListener("change",(()=>{this.haptic&&Gi("light")}))}},{kind:"field",static:!0,key:"styles",value:()=>[ha,pt`
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
    `]}]}}),da);const ua=t=>void 0!==t&&!Hi.includes(t.state)&&!Wi.includes(t.state);let pa=mt(null,(function(t,e){class i extends e{constructor(...e){super(...e),t(this)}}return{F:i,d:[{kind:"field",key:"hass",value:void 0},{kind:"field",decorators:[lt()],key:"stateObj",value:void 0},{kind:"field",decorators:[lt()],key:"label",value:void 0},{kind:"field",decorators:[gt()],key:"_isOn",value:()=>!1},{kind:"method",key:"render",value:function(){if(!this.stateObj)return ht` <ha-switch disabled></ha-switch> `;if(this.stateObj.attributes.assumed_state||"unknown"===this.stateObj.state)return ht`
        <ha-icon-button
          .label=${`Turn ${Xi(this.stateObj)} off`}
          .path=${Ot}
          .disabled=${"unavailable"===this.stateObj.state}
          @click=${this._turnOff}
          class=${this._isOn||"unknown"===this.stateObj.state?"":"state-active"}
        ></ha-icon-button>
        <ha-icon-button
          .label=${`Turn ${Xi(this.stateObj)} on`}
          .path=${H}
          .disabled=${"unavailable"===this.stateObj.state}
          @click=${this._turnOn}
          class=${this._isOn?"state-active":""}
        ></ha-icon-button>
      `;const t=ht`<ha-switch
      aria-label=${`Toggle ${Xi(this.stateObj)} ${this._isOn?"off":"on"}`}
      .checked=${this._isOn}
      .disabled=${"unavailable"===this.stateObj.state}
      @change=${this._toggleChanged}
    ></ha-switch>`;return this.label?ht`
      <ha-formfield .label=${this.label}>${t}</ha-formfield>
    `:t}},{kind:"method",key:"firstUpdated",value:function(t){xt(Et(i.prototype),"firstUpdated",this).call(this,t),this.addEventListener("click",(t=>t.stopPropagation()))}},{kind:"method",key:"willUpdate",value:function(t){xt(Et(i.prototype),"willUpdate",this).call(this,t),t.has("stateObj")&&(this._isOn=ua(this.stateObj))}},{kind:"method",key:"_toggleChanged",value:function(t){const e=t.target.checked;e!==this._isOn&&this._callService(e)}},{kind:"method",key:"_turnOn",value:function(){this._callService(!0)}},{kind:"method",key:"_turnOff",value:function(){this._callService(!1)}},{kind:"method",key:"_callService",value:async function(t){if(!this.hass||!this.stateObj)return;Gi("light");const e=Fi(this.stateObj);let i,a;"lock"===e?(i="lock",a=t?"unlock":"lock"):"cover"===e?(i="cover",a=t?"open_cover":"close_cover"):"group"===e?(i="homeassistant",a=t?"turn_on":"turn_off"):(i=e,a=t?"turn_on":"turn_off");const s=this.stateObj;this._isOn=t,await this.hass.callService(i,a,{entity_id:this.stateObj.entity_id}),setTimeout((async()=>{this.stateObj===s&&(this._isOn=ua(this.stateObj))}),2e3)}},{kind:"get",static:!0,key:"styles",value:function(){return pt`
      :host {
        white-space: nowrap;
        min-width: 38px;
      }
      ha-icon-button {
        --mdc-icon-button-size: 40px;
        color: var(--ha-icon-button-inactive-color, var(--primary-text-color));
        transition: color 0.5s;
      }
      ha-icon-button.state-active {
        color: var(--ha-icon-button-active-color, var(--primary-color));
      }
      ha-switch {
        padding: 13px 5px;
      }
    `}}]}}),Ct);customElements.define("ha-entity-toggle",pa);const ma=(t,e)=>t.callWS({type:"config/entity_registry/get",entity_id:e}),fa=(t,e)=>t.callWS({type:"config/entity_registry/remove",entity_id:e}),_a=t=>t.sendMessagePromise({type:"config/entity_registry/list"}),ba=(t,e)=>t.subscribeEvents(Bi((()=>_a(t).then((t=>e.setState(t,!0)))),500,!0),"entity_registry_updated"),ga=(t,e)=>Rt("_entityRegistry",_a,ba,t,e),{H:ya}=Lt,va=t=>null===t||"object"!=typeof t&&"function"!=typeof t,wa=(t,e)=>{var i,a;return void 0===e?void 0!==(null===(i=t)||void 0===i?void 0:i._$litType$):(null===(a=t)||void 0===a?void 0:a._$litType$)===e},ka=t=>void 0===t.strings,xa=()=>document.createComment(""),Ea=(t,e,i)=>{var a;const s=t._$AA.parentNode,n=void 0===e?t._$AB:e._$AA;if(void 0===i){const e=s.insertBefore(xa(),n),a=s.insertBefore(xa(),n);i=new ya(e,a,t,t.options)}else{const e=i._$AB.nextSibling,o=i._$AM,r=o!==t;if(r){let e;null===(a=i._$AQ)||void 0===a||a.call(i,t),i._$AM=t,void 0!==i._$AP&&(e=t._$AU)!==o._$AU&&i._$AP(e)}if(e!==n||r){let t=i._$AA;for(;t!==e;){const e=t.nextSibling;s.insertBefore(t,n),t=e}}}return i},Ca=(t,e,i=t)=>(t._$AI(e,i),t),Oa={},Ra=(t,e=Oa)=>t._$AH=e,La=t=>t._$AH,$a=t=>{var e;null===(e=t._$AP)||void 0===e||e.call(t,!1,!0);let i=t._$AA;const a=t._$AB.nextSibling;for(;i!==a;){const t=i.nextSibling;i.remove(),i=t}},Sa=t=>{t._$AR()},Aa=pt`
  ha-state-icon[data-domain="alert"][data-state="on"],
  ha-state-icon[data-domain="automation"][data-state="on"],
  ha-state-icon[data-domain="binary_sensor"][data-state="on"],
  ha-state-icon[data-domain="calendar"][data-state="on"],
  ha-state-icon[data-domain="camera"][data-state="streaming"],
  ha-state-icon[data-domain="cover"][data-state="open"],
  ha-state-icon[data-domain="device_tracker"][data-state="home"],
  ha-state-icon[data-domain="fan"][data-state="on"],
  ha-state-icon[data-domain="humidifier"][data-state="on"],
  ha-state-icon[data-domain="light"][data-state="on"],
  ha-state-icon[data-domain="input_boolean"][data-state="on"],
  ha-state-icon[data-domain="lock"][data-state="unlocked"],
  ha-state-icon[data-domain="media_player"][data-state="on"],
  ha-state-icon[data-domain="media_player"][data-state="paused"],
  ha-state-icon[data-domain="media_player"][data-state="playing"],
  ha-state-icon[data-domain="remote"][data-state="on"],
  ha-state-icon[data-domain="script"][data-state="on"],
  ha-state-icon[data-domain="sun"][data-state="above_horizon"],
  ha-state-icon[data-domain="switch"][data-state="on"],
  ha-state-icon[data-domain="timer"][data-state="active"],
  ha-state-icon[data-domain="vacuum"][data-state="cleaning"],
  ha-state-icon[data-domain="group"][data-state="on"],
  ha-state-icon[data-domain="group"][data-state="home"],
  ha-state-icon[data-domain="group"][data-state="open"],
  ha-state-icon[data-domain="group"][data-state="locked"],
  ha-state-icon[data-domain="group"][data-state="problem"] {
    color: var(--paper-item-icon-active-color, #fdd835);
  }

  ha-state-icon[data-domain="climate"][data-state="cooling"] {
    color: var(--cool-color, var(--state-climate-cool-color));
  }

  ha-state-icon[data-domain="climate"][data-state="heating"] {
    color: var(--heat-color, var(--state-climate-heat-color));
  }

  ha-state-icon[data-domain="climate"][data-state="drying"] {
    color: var(--dry-color, var(--state-climate-dry-color));
  }

  ha-state-icon[data-domain="alarm_control_panel"] {
    color: var(--alarm-color-armed, var(--label-badge-red));
  }
  ha-state-icon[data-domain="alarm_control_panel"][data-state="disarmed"] {
    color: var(--alarm-color-disarmed, var(--label-badge-green));
  }
  ha-state-icon[data-domain="alarm_control_panel"][data-state="pending"],
  ha-state-icon[data-domain="alarm_control_panel"][data-state="arming"] {
    color: var(--alarm-color-pending, var(--label-badge-yellow));
    animation: pulse 1s infinite;
  }
  ha-state-icon[data-domain="alarm_control_panel"][data-state="triggered"] {
    color: var(--alarm-color-triggered, var(--label-badge-red));
    animation: pulse 1s infinite;
  }

  @keyframes pulse {
    0% {
      opacity: 1;
    }
    50% {
      opacity: 0;
    }
    100% {
      opacity: 1;
    }
  }

  ha-state-icon[data-domain="plant"][data-state="problem"],

  /* Color the icon if unavailable */
  ha-state-icon[data-state="unavailable"] {
    color: var(--state-unavailable-color);
  }
`,za=(t,e)=>0!=(t.attributes.supported_features&e),Ia=()=>import("./c.84dc03f9.js"),Ta=(t,e,i)=>new Promise((a=>{const s=e.cancel,n=e.confirm;at(t,"show-dialog",{dialogTag:"dialog-box",dialogImport:Ia,dialogParams:{...e,...i,cancel:()=>{a(!(null==i||!i.prompt)&&null),s&&s()},confirm:t=>{a(null==i||!i.prompt||t),n&&n(t)}}})})),Ma=(t,e)=>Ta(t,e),ja=(t,e)=>Ta(t,e,{confirmation:!0}),Fa=(t,e)=>Ta(t,e,{prompt:!0}),Ba=4,Da=t=>(t=>za(t,4)&&"number"==typeof t.attributes.in_progress)(t)||!!t.attributes.in_progress,Pa={10:qe,20:Xe,30:Ye,40:Ke,50:We,60:Ge,70:Je,80:Qe,90:Ze,100:xe},Na={10:ti,20:ei,30:ii,40:ai,50:si,60:ni,70:oi,80:ri,90:li,100:Ee},Ha=(t,e)=>{const i=Number(t);if(isNaN(i))return"off"===t?xe:"on"===t?Ne:He;const a=10*Math.round(i/10);return e&&i>=10?Na[a]:e?Ue:i<=5?Ve:Pa[a]},Ua=t=>{const e=null==t?void 0:t.attributes.device_class;if(e&&e in Ni)return Ni[e];if("battery"===e)return t?((t,e)=>{const i=t.state,a=e&&"on"===e.state;return Ha(i,a)})(t):xe;const i=null==t?void 0:t.attributes.unit_of_measurement;return"°C"===i||"°F"===i?D:void 0},Va=(t,e,i)=>{const a=void 0!==i?i:null==e?void 0:e.state;switch(t){case"alarm_control_panel":return(t=>{switch(t){case"armed_away":return Ft;case"armed_vacation":return jt;case"armed_home":return Mt;case"armed_night":return Tt;case"armed_custom_bypass":return It;case"pending":return zt;case"triggered":return At;case"disarmed":return St;default:return $t}})(a);case"binary_sensor":return((t,e)=>{const i="off"===t;switch(null==e?void 0:e.attributes.device_class){case"battery":return i?xe:Ce;case"battery_charging":return i?xe:Ee;case"carbon_monoxide":return i?we:ke;case"cold":return i?D:ve;case"connectivity":return i?ge:ye;case"door":return i?_e:be;case"garage_door":return i?me:fe;case"power":case"plug":return i?Qt:Zt;case"gas":case"problem":case"safety":case"tamper":return i?ue:pe;case"smoke":return i?de:he;case"heat":return i?D:ce;case"light":return i?G:le;case"lock":return i?oe:re;case"moisture":return i?se:ne;case"motion":return i?ie:ae;case"occupancy":case"presence":return i?Gt:Jt;case"opening":return i?te:ee;case"running":return i?Kt:Wt;case"sound":return i?Xt:Yt;case"update":return i?Vt:qt;case"vibration":return i?Ht:Ut;case"window":return i?Pt:Nt;default:return i?Bt:Dt}})(a,e);case"button":switch(null==e?void 0:e.attributes.device_class){case"restart":return Oi;case"update":return qt;default:return g}case"cover":return((t,e)=>{const i="closed"!==t;switch(null==e?void 0:e.attributes.device_class){case"garage":switch(t){case"opening":return Re;case"closing":return Oe;case"closed":return me;default:return fe}case"gate":switch(t){case"opening":case"closing":return Pe;case"closed":return De;default:return Be}case"door":return i?be:_e;case"damper":return i?je:Fe;case"shutter":switch(t){case"opening":return Re;case"closing":return Oe;case"closed":return Me;default:return Te}case"curtain":switch(t){case"opening":return Ie;case"closing":return ze;case"closed":return Ae;default:return Se}case"blind":case"shade":switch(t){case"opening":return Re;case"closing":return Oe;case"closed":return $e;default:return Le}case"window":switch(t){case"opening":return Re;case"closing":return Oe;case"closed":return Pt;default:return Nt}}switch(t){case"opening":return Re;case"closing":return Oe;case"closed":return Pt;default:return Nt}})(a,e);case"device_tracker":return"router"===(null==e?void 0:e.attributes.source_type)?"home"===a?wi:ki:["bluetooth","bluetooth_le"].includes(null==e?void 0:e.attributes.source_type)?"home"===a?xi:Ei:"not_home"===a?Ci:R;case"humidifier":return i&&"off"===i?yi:vi;case"input_boolean":return"on"===a?bi:gi;case"lock":switch(a){case"unlocked":return re;case"jammed":return _i;case"locking":case"unlocking":return fi;default:return oe}case"media_player":return"playing"===a?pi:mi;case"switch":switch(null==e?void 0:e.attributes.device_class){case"outlet":return"on"===a?Zt:Qt;case"switch":return"on"===a?hi:ui;default:return hi}case"sensor":{const t=Ua(e);if(t)return t;break}case"input_datetime":if(null==e||!e.attributes.has_date)return it;if(!e.attributes.has_time)return o;break;case"sun":return"above_horizon"===(null==e?void 0:e.state)?Pi[t]:di;case"update":return"on"===a?Da(e)?ci:qt:Vt}return t in Pi?Pi[t]:(console.warn(`Unable to find icon for domain ${t}`),Di)};mt([ft("ha-state-icon")],(function(t,e){return{F:class extends e{constructor(...e){super(...e),t(this)}},d:[{kind:"field",decorators:[lt({attribute:!1})],key:"state",value:void 0},{kind:"field",decorators:[lt()],key:"icon",value:void 0},{kind:"method",key:"render",value:function(){var t,e,i;return this.icon||null!==(t=this.state)&&void 0!==t&&t.attributes.icon?ht`<ha-icon
        .icon=${this.icon||(null===(e=this.state)||void 0===e?void 0:e.attributes.icon)}
      ></ha-icon>`:ht`<ha-svg-icon .path=${i=this.state,i?Va(ji(i.entity_id),i):Di}></ha-svg-icon>`}}]}}),Ct);let qa=mt(null,(function(t,e){class i extends e{constructor(...e){super(...e),t(this)}}return{F:i,d:[{kind:"field",key:"hass",value:void 0},{kind:"field",decorators:[lt()],key:"stateObj",value:void 0},{kind:"field",decorators:[lt()],key:"overrideIcon",value:void 0},{kind:"field",decorators:[lt()],key:"overrideImage",value:void 0},{kind:"field",decorators:[lt({type:Boolean})],key:"stateColor",value:void 0},{kind:"field",decorators:[lt({type:Boolean,reflect:!0,attribute:"icon"})],key:"_showIcon",value:()=>!0},{kind:"field",decorators:[gt()],key:"_iconStyle",value:()=>({})},{kind:"method",key:"render",value:function(){const t=this.stateObj;if(!t&&!this.overrideIcon&&!this.overrideImage)return ht`<div class="missing">
        <ha-svg-icon .path=${a}></ha-svg-icon>
      </div>`;if(!this._showIcon)return ht``;const e=t?Fi(t):void 0;return ht`<ha-state-icon
      style=${Ri(this._iconStyle)}
      data-domain=${kt(this.stateColor||"light"===e&&!1!==this.stateColor?e:void 0)}
      data-state=${t?(t=>{const e=t.entity_id.split(".")[0];let i=t.state;return"climate"===e&&(i=t.attributes.hvac_action),i})(t):""}
      .icon=${this.overrideIcon}
      .state=${t}
    ></ha-state-icon>`}},{kind:"method",key:"willUpdate",value:function(t){if(xt(Et(i.prototype),"willUpdate",this).call(this,t),!t.has("stateObj")&&!t.has("overrideImage")&&!t.has("overrideIcon"))return;const e=this.stateObj,a={},s={backgroundImage:""};if(this._showIcon=!0,e&&void 0===this.overrideImage)if(!e.attributes.entity_picture_local&&!e.attributes.entity_picture||this.overrideIcon){if("on"===e.state&&(!1!==this.stateColor&&e.attributes.rgb_color&&(a.color=`rgb(${e.attributes.rgb_color.join(",")})`),e.attributes.brightness&&!1!==this.stateColor)){const t=e.attributes.brightness;if("number"!=typeof t){const i=`Type error: state-badge expected number, but type of ${e.entity_id}.attributes.brightness is ${typeof t} (${t})`;console.warn(i)}a.filter=`brightness(${(t+245)/5}%)`}}else{let t=e.attributes.entity_picture_local||e.attributes.entity_picture;this.hass&&(t=this.hass.hassUrl(t)),s.backgroundImage=`url(${t})`,this._showIcon=!1}else if(this.overrideImage){let t=this.overrideImage;this.hass&&(t=this.hass.hassUrl(t)),s.backgroundImage=`url(${t})`,this._showIcon=!1}this._iconStyle=a,Object.assign(this.style,s)}},{kind:"get",static:!0,key:"styles",value:function(){return[Aa,pt`
        :host {
          position: relative;
          display: inline-block;
          width: 40px;
          color: var(--paper-item-icon-color, #44739e);
          border-radius: 50%;
          height: 40px;
          text-align: center;
          background-size: cover;
          line-height: 40px;
          vertical-align: middle;
          box-sizing: border-box;
        }
        :host(:focus) {
          outline: none;
        }
        :host(:not([icon]):focus) {
          border: 2px solid var(--divider-color);
        }
        :host([icon]:focus) {
          background: var(--divider-color);
        }
        ha-state-icon {
          transition: color 0.3s ease-in-out, filter 0.3s ease-in-out;
        }
        .missing {
          color: #fce588;
        }
      `]}}]}}),Ct);function Xa(t){const e=t.language||"en";return t.translationMetadata.translations[e]&&t.translationMetadata.translations[e].isRTL||!1}function Ya(t){return Ka(Xa(t))}function Ka(t){return t?"rtl":"ltr"}customElements.define("state-badge",qa),Li({_template:$i`
    <style>
      :host {
        display: block;
        position: absolute;
        outline: none;
        z-index: 1002;
        -moz-user-select: none;
        -ms-user-select: none;
        -webkit-user-select: none;
        user-select: none;
        cursor: default;
      }

      #tooltip {
        display: block;
        outline: none;
        @apply --paper-font-common-base;
        font-size: 10px;
        line-height: 1;
        background-color: var(--paper-tooltip-background, #616161);
        color: var(--paper-tooltip-text-color, white);
        padding: 8px;
        border-radius: 2px;
        @apply --paper-tooltip;
      }

      @keyframes keyFrameScaleUp {
        0% {
          transform: scale(0.0);
        }
        100% {
          transform: scale(1.0);
        }
      }

      @keyframes keyFrameScaleDown {
        0% {
          transform: scale(1.0);
        }
        100% {
          transform: scale(0.0);
        }
      }

      @keyframes keyFrameFadeInOpacity {
        0% {
          opacity: 0;
        }
        100% {
          opacity: var(--paper-tooltip-opacity, 0.9);
        }
      }

      @keyframes keyFrameFadeOutOpacity {
        0% {
          opacity: var(--paper-tooltip-opacity, 0.9);
        }
        100% {
          opacity: 0;
        }
      }

      @keyframes keyFrameSlideDownIn {
        0% {
          transform: translateY(-2000px);
          opacity: 0;
        }
        10% {
          opacity: 0.2;
        }
        100% {
          transform: translateY(0);
          opacity: var(--paper-tooltip-opacity, 0.9);
        }
      }

      @keyframes keyFrameSlideDownOut {
        0% {
          transform: translateY(0);
          opacity: var(--paper-tooltip-opacity, 0.9);
        }
        10% {
          opacity: 0.2;
        }
        100% {
          transform: translateY(-2000px);
          opacity: 0;
        }
      }

      .fade-in-animation {
        opacity: 0;
        animation-delay: var(--paper-tooltip-delay-in, 500ms);
        animation-name: keyFrameFadeInOpacity;
        animation-iteration-count: 1;
        animation-timing-function: ease-in;
        animation-duration: var(--paper-tooltip-duration-in, 500ms);
        animation-fill-mode: forwards;
        @apply --paper-tooltip-animation;
      }

      .fade-out-animation {
        opacity: var(--paper-tooltip-opacity, 0.9);
        animation-delay: var(--paper-tooltip-delay-out, 0ms);
        animation-name: keyFrameFadeOutOpacity;
        animation-iteration-count: 1;
        animation-timing-function: ease-in;
        animation-duration: var(--paper-tooltip-duration-out, 500ms);
        animation-fill-mode: forwards;
        @apply --paper-tooltip-animation;
      }

      .scale-up-animation {
        transform: scale(0);
        opacity: var(--paper-tooltip-opacity, 0.9);
        animation-delay: var(--paper-tooltip-delay-in, 500ms);
        animation-name: keyFrameScaleUp;
        animation-iteration-count: 1;
        animation-timing-function: ease-in;
        animation-duration: var(--paper-tooltip-duration-in, 500ms);
        animation-fill-mode: forwards;
        @apply --paper-tooltip-animation;
      }

      .scale-down-animation {
        transform: scale(1);
        opacity: var(--paper-tooltip-opacity, 0.9);
        animation-delay: var(--paper-tooltip-delay-out, 500ms);
        animation-name: keyFrameScaleDown;
        animation-iteration-count: 1;
        animation-timing-function: ease-in;
        animation-duration: var(--paper-tooltip-duration-out, 500ms);
        animation-fill-mode: forwards;
        @apply --paper-tooltip-animation;
      }

      .slide-down-animation {
        transform: translateY(-2000px);
        opacity: 0;
        animation-delay: var(--paper-tooltip-delay-out, 500ms);
        animation-name: keyFrameSlideDownIn;
        animation-iteration-count: 1;
        animation-timing-function: cubic-bezier(0.0, 0.0, 0.2, 1);
        animation-duration: var(--paper-tooltip-duration-out, 500ms);
        animation-fill-mode: forwards;
        @apply --paper-tooltip-animation;
      }

      .slide-down-animation-out {
        transform: translateY(0);
        opacity: var(--paper-tooltip-opacity, 0.9);
        animation-delay: var(--paper-tooltip-delay-out, 500ms);
        animation-name: keyFrameSlideDownOut;
        animation-iteration-count: 1;
        animation-timing-function: cubic-bezier(0.4, 0.0, 1, 1);
        animation-duration: var(--paper-tooltip-duration-out, 500ms);
        animation-fill-mode: forwards;
        @apply --paper-tooltip-animation;
      }

      .cancel-animation {
        animation-delay: -30s !important;
      }

      /* Thanks IE 10. */

      .hidden {
        display: none !important;
      }
    </style>

    <div id="tooltip" class="hidden">
      <slot></slot>
    </div>
`,is:"paper-tooltip",hostAttributes:{role:"tooltip",tabindex:-1},properties:{for:{type:String,observer:"_findTarget"},manualMode:{type:Boolean,value:!1,observer:"_manualModeChanged"},position:{type:String,value:"bottom"},fitToVisibleBounds:{type:Boolean,value:!1},offset:{type:Number,value:14},marginTop:{type:Number,value:14},animationDelay:{type:Number,value:500,observer:"_delayChange"},animationEntry:{type:String,value:""},animationExit:{type:String,value:""},animationConfig:{type:Object,value:function(){return{entry:[{name:"fade-in-animation",node:this,timing:{delay:0}}],exit:[{name:"fade-out-animation",node:this}]}}},_showing:{type:Boolean,value:!1}},listeners:{webkitAnimationEnd:"_onAnimationEnd"},get target(){var t=Si(this).parentNode,e=Si(this).getOwnerRoot();return this.for?Si(e).querySelector("#"+this.for):t.nodeType==Node.DOCUMENT_FRAGMENT_NODE?e.host:t},attached:function(){this._findTarget()},detached:function(){this.manualMode||this._removeListeners()},playAnimation:function(t){"entry"===t?this.show():"exit"===t&&this.hide()},cancelAnimation:function(){this.$.tooltip.classList.add("cancel-animation")},show:function(){if(!this._showing){if(""===Si(this).textContent.trim()){for(var t=!0,e=Si(this).getEffectiveChildNodes(),i=0;i<e.length;i++)if(""!==e[i].textContent.trim()){t=!1;break}if(t)return}this._showing=!0,this.$.tooltip.classList.remove("hidden"),this.$.tooltip.classList.remove("cancel-animation"),this.$.tooltip.classList.remove(this._getAnimationType("exit")),this.updatePosition(),this._animationPlaying=!0,this.$.tooltip.classList.add(this._getAnimationType("entry"))}},hide:function(){if(this._showing){if(this._animationPlaying)return this._showing=!1,void this._cancelAnimation();this._onAnimationFinish(),this._showing=!1,this._animationPlaying=!0}},updatePosition:function(){if(this._target&&this.offsetParent){var t=this.offset;14!=this.marginTop&&14==this.offset&&(t=this.marginTop);var e,i,a=this.offsetParent.getBoundingClientRect(),s=this._target.getBoundingClientRect(),n=this.getBoundingClientRect(),o=(s.width-n.width)/2,r=(s.height-n.height)/2,l=s.left-a.left,c=s.top-a.top;switch(this.position){case"top":e=l+o,i=c-n.height-t;break;case"bottom":e=l+o,i=c+s.height+t;break;case"left":e=l-n.width-t,i=c+r;break;case"right":e=l+s.width+t,i=c+r}this.fitToVisibleBounds?(a.left+e+n.width>window.innerWidth?(this.style.right="0px",this.style.left="auto"):(this.style.left=Math.max(0,e)+"px",this.style.right="auto"),a.top+i+n.height>window.innerHeight?(this.style.bottom=a.height-c+t+"px",this.style.top="auto"):(this.style.top=Math.max(-a.top,i)+"px",this.style.bottom="auto")):(this.style.left=e+"px",this.style.top=i+"px")}},_addListeners:function(){this._target&&(this.listen(this._target,"mouseenter","show"),this.listen(this._target,"focus","show"),this.listen(this._target,"mouseleave","hide"),this.listen(this._target,"blur","hide"),this.listen(this._target,"tap","hide")),this.listen(this.$.tooltip,"animationend","_onAnimationEnd"),this.listen(this,"mouseenter","hide")},_findTarget:function(){this.manualMode||this._removeListeners(),this._target=this.target,this.manualMode||this._addListeners()},_delayChange:function(t){500!==t&&this.updateStyles({"--paper-tooltip-delay-in":t+"ms"})},_manualModeChanged:function(){this.manualMode?this._removeListeners():this._addListeners()},_cancelAnimation:function(){this.$.tooltip.classList.remove(this._getAnimationType("entry")),this.$.tooltip.classList.remove(this._getAnimationType("exit")),this.$.tooltip.classList.remove("cancel-animation"),this.$.tooltip.classList.add("hidden")},_onAnimationFinish:function(){this._showing&&(this.$.tooltip.classList.remove(this._getAnimationType("entry")),this.$.tooltip.classList.remove("cancel-animation"),this.$.tooltip.classList.add(this._getAnimationType("exit")))},_onAnimationEnd:function(){this._animationPlaying=!1,this._showing||(this.$.tooltip.classList.remove(this._getAnimationType("exit")),this.$.tooltip.classList.add("hidden"))},_getAnimationType:function(t){if("entry"===t&&""!==this.animationEntry)return this.animationEntry;if("exit"===t&&""!==this.animationExit)return this.animationExit;if(this.animationConfig[t]&&"string"==typeof this.animationConfig[t][0].name){if(this.animationConfig[t][0].timing&&this.animationConfig[t][0].timing.delay&&0!==this.animationConfig[t][0].timing.delay){var e=this.animationConfig[t][0].timing.delay;"entry"===t?this.updateStyles({"--paper-tooltip-delay-in":e+"ms"}):"exit"===t&&this.updateStyles({"--paper-tooltip-delay-out":e+"ms"})}return this.animationConfig[t][0].name}},_removeListeners:function(){this._target&&(this.unlisten(this._target,"mouseenter","show"),this.unlisten(this._target,"focus","show"),this.unlisten(this._target,"mouseleave","hide"),this.unlisten(this._target,"blur","hide"),this.unlisten(this._target,"tap","hide")),this.unlisten(this.$.tooltip,"animationend","_onAnimationEnd"),this.unlisten(this,"mouseenter","hide")}});const Wa=t=>e=>({kind:"method",placement:"prototype",key:e.key,descriptor:{set(t){this[`__${String(e.key)}`]=t},get(){return this[`__${String(e.key)}`]},enumerable:!0,configurable:!0},finisher(i){const a=i.prototype.connectedCallback;i.prototype.connectedCallback=function(){if(a.call(this),this[e.key]){const i=this.renderRoot.querySelector(t);if(!i)return;i.scrollTop=this[e.key]}}}});function Ga(t,e,i,a){var s,n=arguments.length,o=n<3?e:null===a?a=Object.getOwnPropertyDescriptor(e,i):a;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)o=Reflect.decorate(t,e,i,a);else for(var r=t.length-1;r>=0;r--)(s=t[r])&&(o=(n<3?s(o):n>3?s(e,i,o):s(e,i))||o);return n>3&&o&&Object.defineProperty(e,i,o),o}const Ja=(t,e,i)=>{const a=new Map;for(let s=e;s<=i;s++)a.set(t[s],s);return a},Qa=Ai(class extends zi{constructor(t){if(super(t),t.type!==Ii.CHILD)throw Error("repeat() can only be used in text expressions")}dt(t,e,i){let a;void 0===i?i=e:void 0!==e&&(a=e);const s=[],n=[];let o=0;for(const e of t)s[o]=a?a(e,o):o,n[o]=i(e,o),o++;return{values:n,keys:s}}render(t,e,i){return this.dt(t,e,i).values}update(t,[e,i,a]){var s;const n=La(t),{values:o,keys:r}=this.dt(e,i,a);if(!Array.isArray(n))return this.at=r,o;const l=null!==(s=this.at)&&void 0!==s?s:this.at=[],c=[];let d,h,u=0,p=n.length-1,m=0,f=o.length-1;for(;u<=p&&m<=f;)if(null===n[u])u++;else if(null===n[p])p--;else if(l[u]===r[m])c[m]=Ca(n[u],o[m]),u++,m++;else if(l[p]===r[f])c[f]=Ca(n[p],o[f]),p--,f--;else if(l[u]===r[f])c[f]=Ca(n[u],o[f]),Ea(t,c[f+1],n[u]),u++,f--;else if(l[p]===r[m])c[m]=Ca(n[p],o[m]),Ea(t,n[u],n[p]),p--,m++;else if(void 0===d&&(d=Ja(r,m,f),h=Ja(l,u,p)),d.has(l[u]))if(d.has(l[p])){const e=h.get(r[m]),i=void 0!==e?n[e]:null;if(null===i){const e=Ea(t,n[u]);Ca(e,o[m]),c[m]=e}else c[m]=Ca(i,o[m]),Ea(t,n[u],i),n[e]=null;m++}else $a(n[p]),p--;else $a(n[u]),u++;for(;m<=f;){const e=Ea(t,c[f+1]);Ca(e,o[m]),c[m++]=e}for(;u<=p;){const t=n[u++];null!==t&&$a(t)}return this.at=r,Ra(t,c),Ti}});let Za,ts;async function es(){return ts||async function(){if(Za)return(await Za).default;Za=window.ResizeObserver;try{new Za((function(){}))}catch(t){Za=import("./c.48ac7cd1.js"),Za=(await Za).default}return ts=Za}()}const is=Symbol("virtualizerRef");class as extends Event{constructor(t){super(as.eventName,{bubbles:!0}),this.first=t.first,this.last=t.last}}as.eventName="rangeChanged";class ss extends Event{constructor(t){super(ss.eventName,{bubbles:!0}),this.first=t.first,this.last=t.last}}ss.eventName="visibilityChanged";class ns{constructor(t){if(this._benchmarkStart=null,this._layout=null,this._clippingAncestors=[],this._scrollSize=null,this._scrollError=null,this._childrenPos=null,this._childMeasurements=null,this._toBeMeasured=new Map,this._rangeChanged=!0,this._itemsChanged=!0,this._visibilityChanged=!0,this._isScroller=!1,this._sizer=null,this._hostElementRO=null,this._childrenRO=null,this._mutationObserver=null,this._mutationPromise=null,this._mutationPromiseResolver=null,this._mutationsObserved=!1,this._scrollEventListeners=[],this._scrollEventListenerOptions={passive:!0},this._loadListener=this._childLoaded.bind(this),this._scrollToIndex=null,this._items=[],this._first=-1,this._last=-1,this._firstVisible=-1,this._lastVisible=-1,this._scheduled=new WeakSet,this._measureCallback=null,this._measureChildOverride=null,!t)throw new Error("Virtualizer constructor requires a configuration object");if(!t.hostElement)throw new Error('Virtualizer configuration requires the "hostElement" property');this._init(t)}set items(t){Array.isArray(t)&&t!==this._items&&(this._itemsChanged=!0,this._items=t,this._schedule(this._updateLayout))}_init(t){this._isScroller=!!t.scroller,this._initHostElement(t),this._initLayout(t)}async _initObservers(){this._mutationObserver=new MutationObserver(this._observeMutations.bind(this));const t=await es();this._hostElementRO=new t((()=>this._hostElementSizeChanged())),this._childrenRO=new t(this._childrenSizeChanged.bind(this))}async _initLayout(t){t.layout?this.layout=t.layout:this.layout=(await import("./c.8c13a4f8.js")).FlowLayout}_initHostElement(t){const e=this._hostElement=t.hostElement;this._applyVirtualizerStyles(),e[is]=this}async connected(){await this._initObservers();const t=this._isScroller;this._clippingAncestors=function(t,e=!1){return function(t,e=!1){const i=[];let a=e?t:rs(t);for(;null!==a;)i.push(a),a=rs(a);return i}(t,e).filter((t=>"visible"!==getComputedStyle(t).overflow))}(this._hostElement,t),this._schedule(this._updateLayout),this._observeAndListen()}_observeAndListen(){this._mutationObserver.observe(this._hostElement,{childList:!0}),this._mutationPromise=new Promise((t=>this._mutationPromiseResolver=t)),this._hostElementRO.observe(this._hostElement),this._scrollEventListeners.push(window),window.addEventListener("scroll",this,this._scrollEventListenerOptions),this._clippingAncestors.forEach((t=>{t.addEventListener("scroll",this,this._scrollEventListenerOptions),this._scrollEventListeners.push(t),this._hostElementRO.observe(t)})),this._children.forEach((t=>this._childrenRO.observe(t))),this._scrollEventListeners.forEach((t=>t.addEventListener("scroll",this,this._scrollEventListenerOptions)))}disconnected(){this._scrollEventListeners.forEach((t=>t.removeEventListener("scroll",this,this._scrollEventListenerOptions))),this._scrollEventListeners=[],this._clippingAncestors=[],this._mutationObserver.disconnect(),this._hostElementRO.disconnect(),this._childrenRO.disconnect()}_applyVirtualizerStyles(){const t=this._hostElement.style;t.display=t.display||"block",t.position=t.position||"relative",t.contain=t.contain||"strict",this._isScroller&&(t.overflow=t.overflow||"auto",t.minHeight=t.minHeight||"150px")}_getSizer(){const t=this._hostElement;if(!this._sizer){let e=t.querySelector("[virtualizer-sizer]");e||(e=document.createElement("div"),e.setAttribute("virtualizer-sizer",""),t.appendChild(e)),Object.assign(e.style,{position:"absolute",margin:"-2px 0 0 0",padding:0,visibility:"hidden",fontSize:"2px"}),e.innerHTML="&nbsp;",e.setAttribute("virtualizer-sizer",""),this._sizer=e}return this._sizer}get layout(){return this._layout}set layout(t){if(this._layout===t)return;let e=null,i={};if("object"==typeof t?(void 0!==t.type&&(e=t.type),i=t):e=t,"function"==typeof e){if(this._layout instanceof e)return void(i&&(this._layout.config=i));e=new e(i)}this._layout&&(this._measureCallback=null,this._measureChildOverride=null,this._layout.removeEventListener("scrollsizechange",this),this._layout.removeEventListener("scrollerrorchange",this),this._layout.removeEventListener("itempositionchange",this),this._layout.removeEventListener("rangechange",this),this._sizeHostElement(void 0),this._hostElement.removeEventListener("load",this._loadListener,!0)),this._layout=e,this._layout&&(this._layout.measureChildren&&"function"==typeof this._layout.updateItemSizes&&("function"==typeof this._layout.measureChildren&&(this._measureChildOverride=this._layout.measureChildren),this._measureCallback=this._layout.updateItemSizes.bind(this._layout)),this._layout.addEventListener("scrollsizechange",this),this._layout.addEventListener("scrollerrorchange",this),this._layout.addEventListener("itempositionchange",this),this._layout.addEventListener("rangechange",this),this._layout.listenForChildLoadEvents&&this._hostElement.addEventListener("load",this._loadListener,!0),this._schedule(this._updateLayout))}startBenchmarking(){null===this._benchmarkStart&&(this._benchmarkStart=window.performance.now())}stopBenchmarking(){if(null!==this._benchmarkStart){const t=window.performance.now(),e=t-this._benchmarkStart,i=performance.getEntriesByName("uv-virtualizing","measure").filter((e=>e.startTime>=this._benchmarkStart&&e.startTime<t)).reduce(((t,e)=>t+e.duration),0);return this._benchmarkStart=null,{timeElapsed:e,virtualizationTime:i}}return null}_measureChildren(){const t={},e=this._children,i=this._measureChildOverride||this._measureChild;for(let a=0;a<e.length;a++){const s=e[a],n=this._first+a;(this._itemsChanged||this._toBeMeasured.has(s))&&(t[n]=i.call(this,s,this._items[n]))}this._childMeasurements=t,this._schedule(this._updateLayout),this._toBeMeasured.clear()}_measureChild(t){const{width:e,height:i}=t.getBoundingClientRect();return Object.assign({width:e,height:i},function(t){const e=window.getComputedStyle(t);return{marginTop:os(e.marginTop),marginRight:os(e.marginRight),marginBottom:os(e.marginBottom),marginLeft:os(e.marginLeft)}}(t))}set scrollToIndex(t){this._scrollToIndex=t,this._schedule(this._updateLayout)}async _schedule(t){this._scheduled.has(t)||(this._scheduled.add(t),await Promise.resolve(),this._scheduled.delete(t),t.call(this))}async _updateDOM(){const{_rangeChanged:t,_itemsChanged:e}=this;this._visibilityChanged&&(this._notifyVisibility(),this._visibilityChanged=!1),(t||e)&&(this._notifyRange(),await this._mutationPromise),this._children.forEach((t=>this._childrenRO.observe(t))),this._positionChildren(this._childrenPos),this._sizeHostElement(this._scrollSize),this._scrollError&&(this._correctScrollError(this._scrollError),this._scrollError=null),this._benchmarkStart&&"mark"in window.performance&&window.performance.mark("uv-end")}_updateLayout(){this._layout&&(this._layout.totalItems=this._items.length,null!==this._scrollToIndex&&(this._layout.scrollToIndex(this._scrollToIndex.index,this._scrollToIndex.position),this._scrollToIndex=null),this._updateView(),null!==this._childMeasurements&&(this._measureCallback&&this._measureCallback(this._childMeasurements),this._childMeasurements=null),this._layout.reflowIfNeeded(this._itemsChanged),this._benchmarkStart&&"mark"in window.performance&&window.performance.mark("uv-end"))}_handleScrollEvent(){if(this._benchmarkStart&&"mark"in window.performance){try{window.performance.measure("uv-virtualizing","uv-start","uv-end")}catch(t){console.warn("Error measuring performance data: ",t)}window.performance.mark("uv-start")}this._schedule(this._updateLayout)}handleEvent(t){switch(t.type){case"scroll":(t.currentTarget===window||this._clippingAncestors.includes(t.currentTarget))&&this._handleScrollEvent();break;case"scrollsizechange":this._scrollSize=t.detail,this._schedule(this._updateDOM);break;case"scrollerrorchange":this._scrollError=t.detail,this._schedule(this._updateDOM);break;case"itempositionchange":this._childrenPos=t.detail,this._schedule(this._updateDOM);break;case"rangechange":this._adjustRange(t.detail),this._schedule(this._updateDOM);break;default:console.warn("event not handled",t)}}get _children(){const t=[];let e=this._hostElement.firstElementChild;for(;e;)e.hasAttribute("virtualizer-sizer")||t.push(e),e=e.nextElementSibling;return t}_updateView(){const t=this._hostElement,e=this._layout;let i,a,s,n,o,r;const l=t.getBoundingClientRect();i=0,a=0,s=window.innerHeight,n=window.innerWidth;for(let t of this._clippingAncestors){const e=t.getBoundingClientRect();i=Math.max(i,e.top),a=Math.max(a,e.left),s=Math.min(s,e.bottom),n=Math.min(n,e.right)}o=i-l.top+t.scrollTop,r=a-l.left+t.scrollLeft;const c=Math.max(1,s-i),d=Math.max(1,n-a);e.viewportSize={width:d,height:c},e.viewportScroll={top:o,left:r}}_sizeHostElement(t){const e=82e5,i=t&&t.width?Math.min(e,t.width):0,a=t&&t.height?Math.min(e,t.height):0;if(this._isScroller)this._getSizer().style.transform=`translate(${i}px, ${a}px)`;else{const t=this._hostElement.style;t.minWidth=i?`${i}px`:"100%",t.minHeight=a?`${a}px`:"100%"}}_positionChildren(t){if(t){const e=this._children;Object.keys(t).forEach((i=>{const a=i-this._first,s=e[a];if(s){const{top:e,left:a,width:n,height:o,xOffset:r,yOffset:l}=t[i];s.style.position="absolute",s.style.boxSizing="border-box",s.style.transform=`translate(${a}px, ${e}px)`,void 0!==n&&(s.style.width=n+"px"),void 0!==o&&(s.style.height=o+"px"),s.style.left=void 0===r?null:r+"px",s.style.top=void 0===l?null:l+"px"}}))}}async _adjustRange(t){const{_first:e,_last:i,_firstVisible:a,_lastVisible:s}=this;this._first=t.first,this._last=t.last,this._firstVisible=t.firstVisible,this._lastVisible=t.lastVisible,this._rangeChanged=this._rangeChanged||this._first!==e||this._last!==i,this._visibilityChanged=this._visibilityChanged||this._firstVisible!==a||this._lastVisible!==s}_correctScrollError(t){const e=this._clippingAncestors[0];e?(e.scrollTop-=t.top,e.scrollLeft-=t.left):window.scroll(window.pageXOffset-t.left,window.pageYOffset-t.top)}_notifyRange(){this._hostElement.dispatchEvent(new as({first:this._first,last:this._last}))}_notifyVisibility(){this._hostElement.dispatchEvent(new ss({first:this._firstVisible,last:this._lastVisible}))}_hostElementSizeChanged(){this._schedule(this._updateLayout)}async _observeMutations(){this._mutationsObserved||(this._mutationsObserved=!0,this._mutationPromiseResolver(),this._mutationPromise=new Promise((t=>this._mutationPromiseResolver=t)),this._mutationsObserved=!1)}_childLoaded(){}_childrenSizeChanged(t){if(this._layout.measureChildren){for(const e of t)this._toBeMeasured.set(e.target,e.contentRect);this._measureChildren()}this._itemsChanged=!1,this._rangeChanged=!1}}function os(t){const e=t?parseFloat(t):NaN;return Number.isNaN(e)?0:e}function rs(t){if(null!==t.parentElement)return t.parentElement;const e=t.parentNode;return e&&e.nodeType===Node.DOCUMENT_FRAGMENT_NODE&&e.host||null}const ls=t=>t,cs=(t,e)=>ht`${e}: ${JSON.stringify(t,null,2)}`;class ds extends Ct{constructor(){super(...arguments),this._renderItem=(t,e)=>cs(t,e+this._first),this._providedRenderItem=cs,this.items=[],this.scroller=!1,this.keyFunction=ls,this._first=0,this._last=-1}set renderItem(t){this._providedRenderItem=t,this._renderItem=(e,i)=>t(e,i+this._first),this.requestUpdate()}get renderItem(){return this._providedRenderItem}set layout(t){this._layout=t,t&&this._virtualizer&&(this._virtualizer.layout=t)}get layout(){return this[is].layout}scrollToIndex(t,e="start"){this._virtualizer.scrollToIndex={index:t,position:e}}updated(){this._virtualizer&&(void 0!==this._layout&&(this._virtualizer.layout=this._layout),this._virtualizer.items=this.items)}firstUpdated(){const t=this._layout;this._virtualizer=new ns({hostElement:this,layout:t,scroller:this.scroller}),this.addEventListener("rangeChanged",(t=>{t.stopPropagation(),this._first=t.first,this._last=t.last})),this._virtualizer.connected()}connectedCallback(){super.connectedCallback(),this._virtualizer&&this._virtualizer.connected()}disconnectedCallback(){this._virtualizer&&this._virtualizer.disconnected(),super.disconnectedCallback()}createRenderRoot(){return this}render(){const{items:t,_renderItem:e,keyFunction:i}=this,a=[],s=Math.min(t.length,this._last+1);if(this._first>=0&&this._last>=this._first)for(let e=this._first;e<s;e++)a.push(t[e]);return Qa(a,i||ls,e)}}Ga([lt()],ds.prototype,"renderItem",null),Ga([lt({attribute:!1})],ds.prototype,"items",void 0),Ga([lt({reflect:!0,type:Boolean})],ds.prototype,"scroller",void 0),Ga([lt()],ds.prototype,"keyFunction",void 0),Ga([gt()],ds.prototype,"_first",void 0),Ga([gt()],ds.prototype,"_last",void 0),Ga([lt({attribute:!1})],ds.prototype,"layout",null),customElements.define("lit-virtualizer",ds);const hs=(t,e)=>t&&t.config.components.includes(e);export{Ka as A,Ui as B,Va as C,qi as D,ja as E,aa as F,fa as G,Qa as H,ma as I,Wi as U,Fi as a,ga as b,Xi as c,Bi as d,ji as e,Fa as f,Ma as g,Mi as h,Wa as i,Xa as j,hs as k,Ya as l,La as m,Ki as n,sa as o,Sa as p,Yi as q,ka as r,Ra as s,va as t,Ea as u,wa as v,Da as w,za as x,Ba as y,Vi as z};

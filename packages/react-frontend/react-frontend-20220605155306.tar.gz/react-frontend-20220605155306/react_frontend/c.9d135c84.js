import{cj as t,ck as e,cx as a,cw as i,f as n,ai as o,aj as r,ak as s,al as l,an as c,e as d,am as h,$ as p,ao as u,au as m,ap as f,n as g,t as b,ar as v,as as y,at as _,cK as k,cL as x,cl as w,cm as C,m as S,_ as T,s as I,cM as E,cI as A,h as $,cN as L,aw as R,ax as O,ch as D,cr as z,cO as M,cf as N,cJ as j,cP as F,cy as P,v as B,cQ as H,cR as G}from"./main-4b1ba1ae.js";import{v as K,m as U,s as W,u as V,p as Y,o as X,r as q,t as Z,U as Q,c as J,j as tt,e as et,k as at,n as it,q as nt,a as ot,w as rt,x as st,y as lt,B as ct,z as dt,i as ht,A as pt,C as ut,D as mt,E as ft,G as gt}from"./c.f8815787.js";import{c as bt,u as vt}from"./c.dc4d7ad9.js";import{t as yt}from"./c.dd8bad78.js";import"./c.f7a407a1.js";import{e as _t}from"./c.8d0ef0b0.js";const kt=t(class extends e{constructor(t){super(t),this.tt=new WeakMap}render(t){return[t]}update(t,[e]){if(K(this.it)&&(!K(e)||this.it.strings!==e.strings)){const e=U(t).pop();let n=this.tt.get(this.it.strings);if(void 0===n){const t=document.createDocumentFragment();n=a(i,t),n.setConnected(!1),this.tt.set(this.it.strings,n)}W(n,[e]),V(n,void 0,e)}if(K(e)){if(!K(this.it)||this.it.strings!==e.strings){const a=this.tt.get(e.strings);if(void 0!==a){const e=U(a).pop();Y(t),V(t,void 0,e),W(t,[e])}}this.it=e}else this.it=void 0;return this.render(e)}}),xt=()=>import("./c.c7a1087b.js");var wt={ACTIVE:"mdc-tab-indicator--active",FADE:"mdc-tab-indicator--fade",NO_TRANSITION:"mdc-tab-indicator--no-transition"},Ct={CONTENT_SELECTOR:".mdc-tab-indicator__content"},St=function(t){function e(a){return t.call(this,r(r({},e.defaultAdapter),a))||this}return o(e,t),Object.defineProperty(e,"cssClasses",{get:function(){return wt},enumerable:!1,configurable:!0}),Object.defineProperty(e,"strings",{get:function(){return Ct},enumerable:!1,configurable:!0}),Object.defineProperty(e,"defaultAdapter",{get:function(){return{addClass:function(){},removeClass:function(){},computeContentClientRect:function(){return{top:0,right:0,bottom:0,left:0,width:0,height:0}},setContentStyleProperty:function(){}}},enumerable:!1,configurable:!0}),e.prototype.computeContentClientRect=function(){return this.adapter.computeContentClientRect()},e}(s),Tt=function(t){function e(){return null!==t&&t.apply(this,arguments)||this}return o(e,t),e.prototype.activate=function(){this.adapter.addClass(St.cssClasses.ACTIVE)},e.prototype.deactivate=function(){this.adapter.removeClass(St.cssClasses.ACTIVE)},e}(St),It=function(t){function e(){return null!==t&&t.apply(this,arguments)||this}return o(e,t),e.prototype.activate=function(t){if(t){var e=this.computeContentClientRect(),a=t.width/e.width,i=t.left-e.left;this.adapter.addClass(St.cssClasses.NO_TRANSITION),this.adapter.setContentStyleProperty("transform","translateX("+i+"px) scaleX("+a+")"),this.computeContentClientRect(),this.adapter.removeClass(St.cssClasses.NO_TRANSITION),this.adapter.addClass(St.cssClasses.ACTIVE),this.adapter.setContentStyleProperty("transform","")}else this.adapter.addClass(St.cssClasses.ACTIVE)},e.prototype.deactivate=function(){this.adapter.removeClass(St.cssClasses.ACTIVE)},e}(St);class Et extends h{constructor(){super(...arguments),this.icon="",this.fade=!1}get mdcFoundationClass(){return this.fade?Tt:It}render(){const t={"mdc-tab-indicator__content--icon":this.icon,"material-icons":this.icon,"mdc-tab-indicator__content--underline":!this.icon};return p`
      <span class="mdc-tab-indicator ${u({"mdc-tab-indicator--fade":this.fade})}">
        <span class="mdc-tab-indicator__content ${u(t)}">${this.icon}</span>
      </span>
      `}updated(t){t.has("fade")&&this.createFoundation()}createAdapter(){return Object.assign(Object.assign({},m(this.mdcRoot)),{computeContentClientRect:()=>this.contentElement.getBoundingClientRect(),setContentStyleProperty:(t,e)=>this.contentElement.style.setProperty(t,e)})}computeContentClientRect(){return this.mdcFoundation.computeContentClientRect()}activate(t){this.mdcFoundation.activate(t)}deactivate(){this.mdcFoundation.deactivate()}}l([c(".mdc-tab-indicator")],Et.prototype,"mdcRoot",void 0),l([c(".mdc-tab-indicator__content")],Et.prototype,"contentElement",void 0),l([d()],Et.prototype,"icon",void 0),l([d({type:Boolean})],Et.prototype,"fade",void 0);const At=f`.material-icons{font-family:var(--mdc-icon-font, "Material Icons");font-weight:normal;font-style:normal;font-size:var(--mdc-icon-size, 24px);line-height:1;letter-spacing:normal;text-transform:none;display:inline-block;white-space:nowrap;word-wrap:normal;direction:ltr;-webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility;-moz-osx-font-smoothing:grayscale;font-feature-settings:"liga"}.mdc-tab-indicator .mdc-tab-indicator__content--underline{border-color:#6200ee;border-color:var(--mdc-theme-primary, #6200ee)}.mdc-tab-indicator .mdc-tab-indicator__content--icon{color:#018786;color:var(--mdc-theme-secondary, #018786)}.mdc-tab-indicator .mdc-tab-indicator__content--underline{border-top-width:2px}.mdc-tab-indicator .mdc-tab-indicator__content--icon{height:34px;font-size:34px}.mdc-tab-indicator{display:flex;position:absolute;top:0;left:0;justify-content:center;width:100%;height:100%;pointer-events:none;z-index:1}.mdc-tab-indicator__content{transform-origin:left;opacity:0}.mdc-tab-indicator__content--underline{align-self:flex-end;box-sizing:border-box;width:100%;border-top-style:solid}.mdc-tab-indicator__content--icon{align-self:center;margin:0 auto}.mdc-tab-indicator--active .mdc-tab-indicator__content{opacity:1}.mdc-tab-indicator .mdc-tab-indicator__content{transition:250ms transform cubic-bezier(0.4, 0, 0.2, 1)}.mdc-tab-indicator--no-transition .mdc-tab-indicator__content{transition:none}.mdc-tab-indicator--fade .mdc-tab-indicator__content{transition:150ms opacity linear}.mdc-tab-indicator--active.mdc-tab-indicator--fade .mdc-tab-indicator__content{transition-delay:100ms}`;let $t=class extends Et{};$t.styles=[At],$t=l([g("mwc-tab-indicator")],$t);var Lt={ACTIVE:"mdc-tab--active"},Rt={ARIA_SELECTED:"aria-selected",CONTENT_SELECTOR:".mdc-tab__content",INTERACTED_EVENT:"MDCTab:interacted",RIPPLE_SELECTOR:".mdc-tab__ripple",TABINDEX:"tabIndex",TAB_INDICATOR_SELECTOR:".mdc-tab-indicator"},Ot=function(t){function e(a){var i=t.call(this,r(r({},e.defaultAdapter),a))||this;return i.focusOnActivate=!0,i}return o(e,t),Object.defineProperty(e,"cssClasses",{get:function(){return Lt},enumerable:!1,configurable:!0}),Object.defineProperty(e,"strings",{get:function(){return Rt},enumerable:!1,configurable:!0}),Object.defineProperty(e,"defaultAdapter",{get:function(){return{addClass:function(){},removeClass:function(){},hasClass:function(){return!1},setAttr:function(){},activateIndicator:function(){},deactivateIndicator:function(){},notifyInteracted:function(){},getOffsetLeft:function(){return 0},getOffsetWidth:function(){return 0},getContentOffsetLeft:function(){return 0},getContentOffsetWidth:function(){return 0},focus:function(){}}},enumerable:!1,configurable:!0}),e.prototype.handleClick=function(){this.adapter.notifyInteracted()},e.prototype.isActive=function(){return this.adapter.hasClass(Lt.ACTIVE)},e.prototype.setFocusOnActivate=function(t){this.focusOnActivate=t},e.prototype.activate=function(t){this.adapter.addClass(Lt.ACTIVE),this.adapter.setAttr(Rt.ARIA_SELECTED,"true"),this.adapter.setAttr(Rt.TABINDEX,"0"),this.adapter.activateIndicator(t),this.focusOnActivate&&this.adapter.focus()},e.prototype.deactivate=function(){this.isActive()&&(this.adapter.removeClass(Lt.ACTIVE),this.adapter.setAttr(Rt.ARIA_SELECTED,"false"),this.adapter.setAttr(Rt.TABINDEX,"-1"),this.adapter.deactivateIndicator())},e.prototype.computeDimensions=function(){var t=this.adapter.getOffsetWidth(),e=this.adapter.getOffsetLeft(),a=this.adapter.getContentOffsetWidth(),i=this.adapter.getContentOffsetLeft();return{contentLeft:e+i,contentRight:e+i+a,rootLeft:e,rootRight:e+t}},e}(s);let Dt=0;class zt extends h{constructor(){super(...arguments),this.mdcFoundationClass=Ot,this.label="",this.icon="",this.hasImageIcon=!1,this.isFadingIndicator=!1,this.minWidth=!1,this.isMinWidthIndicator=!1,this.indicatorIcon="",this.stacked=!1,this.focusOnActivate=!0,this._active=!1,this.initFocus=!1,this.shouldRenderRipple=!1,this.useStateLayerCustomProperties=!1,this.rippleElement=null,this.rippleHandlers=new _((()=>(this.shouldRenderRipple=!0,this.ripple.then((t=>this.rippleElement=t)),this.ripple)))}get active(){return this._active}connectedCallback(){this.dir=document.dir,super.connectedCallback()}firstUpdated(){super.firstUpdated(),this.id=this.id||"mdc-tab-"+ ++Dt}render(){const t={"mdc-tab--min-width":this.minWidth,"mdc-tab--stacked":this.stacked};let e=p``;(this.hasImageIcon||this.icon)&&(e=p`
        <span class="mdc-tab__icon material-icons"><slot name="icon">${this.icon}</slot></span>`);let a=p``;return this.label&&(a=p`
        <span class="mdc-tab__text-label">${this.label}</span>`),p`
      <button
        @click="${this.handleClick}"
        class="mdc-tab ${u(t)}"
        role="tab"
        aria-selected="false"
        tabindex="-1"
        @focus="${this.focus}"
        @blur="${this.handleBlur}"
        @mousedown="${this.handleRippleMouseDown}"
        @mouseenter="${this.handleRippleMouseEnter}"
        @mouseleave="${this.handleRippleMouseLeave}"
        @touchstart="${this.handleRippleTouchStart}"
        @touchend="${this.handleRippleDeactivate}"
        @touchcancel="${this.handleRippleDeactivate}">
        <span class="mdc-tab__content">
          ${e}
          ${a}
          ${this.isMinWidthIndicator?this.renderIndicator():""}
        </span>
        ${this.isMinWidthIndicator?"":this.renderIndicator()}
        ${this.renderRipple()}
      </button>`}renderIndicator(){return p`<mwc-tab-indicator
        .icon="${this.indicatorIcon}"
        .fade="${this.isFadingIndicator}"></mwc-tab-indicator>`}renderRipple(){return this.shouldRenderRipple?p`<mwc-ripple primary
        .internalUseStateLayerCustomProperties="${this.useStateLayerCustomProperties}"></mwc-ripple>`:""}createAdapter(){return Object.assign(Object.assign({},m(this.mdcRoot)),{setAttr:(t,e)=>this.mdcRoot.setAttribute(t,e),activateIndicator:async t=>{await this.tabIndicator.updateComplete,this.tabIndicator.activate(t)},deactivateIndicator:async()=>{await this.tabIndicator.updateComplete,this.tabIndicator.deactivate()},notifyInteracted:()=>this.dispatchEvent(new CustomEvent(Ot.strings.INTERACTED_EVENT,{detail:{tabId:this.id},bubbles:!0,composed:!0,cancelable:!0})),getOffsetLeft:()=>this.offsetLeft,getOffsetWidth:()=>this.mdcRoot.offsetWidth,getContentOffsetLeft:()=>this._contentElement.offsetLeft,getContentOffsetWidth:()=>this._contentElement.offsetWidth,focus:()=>{this.initFocus?this.initFocus=!1:this.mdcRoot.focus()}})}activate(t){t||(this.initFocus=!0),this.mdcFoundation?(this.mdcFoundation.activate(t),this.setActive(this.mdcFoundation.isActive())):this.updateComplete.then((()=>{this.mdcFoundation.activate(t),this.setActive(this.mdcFoundation.isActive())}))}deactivate(){this.mdcFoundation.deactivate(),this.setActive(this.mdcFoundation.isActive())}setActive(t){const e=this.active;e!==t&&(this._active=t,this.requestUpdate("active",e))}computeDimensions(){return this.mdcFoundation.computeDimensions()}computeIndicatorClientRect(){return this.tabIndicator.computeContentClientRect()}focus(){this.mdcRoot.focus(),this.handleFocus()}handleClick(){this.handleFocus(),this.mdcFoundation.handleClick()}handleFocus(){this.handleRippleFocus()}handleBlur(){this.handleRippleBlur()}handleRippleMouseDown(t){const e=()=>{window.removeEventListener("mouseup",e),this.handleRippleDeactivate()};window.addEventListener("mouseup",e),this.rippleHandlers.startPress(t)}handleRippleTouchStart(t){this.rippleHandlers.startPress(t)}handleRippleDeactivate(){this.rippleHandlers.endPress()}handleRippleMouseEnter(){this.rippleHandlers.startHover()}handleRippleMouseLeave(){this.rippleHandlers.endHover()}handleRippleFocus(){this.rippleHandlers.startFocus()}handleRippleBlur(){this.rippleHandlers.endFocus()}get isRippleActive(){var t;return(null===(t=this.rippleElement)||void 0===t?void 0:t.isActive)||!1}}zt.shadowRootOptions={mode:"open",delegatesFocus:!0},l([c(".mdc-tab")],zt.prototype,"mdcRoot",void 0),l([c("mwc-tab-indicator")],zt.prototype,"tabIndicator",void 0),l([d()],zt.prototype,"label",void 0),l([d()],zt.prototype,"icon",void 0),l([d({type:Boolean})],zt.prototype,"hasImageIcon",void 0),l([d({type:Boolean})],zt.prototype,"isFadingIndicator",void 0),l([d({type:Boolean})],zt.prototype,"minWidth",void 0),l([d({type:Boolean})],zt.prototype,"isMinWidthIndicator",void 0),l([d({type:Boolean,reflect:!0,attribute:"active"})],zt.prototype,"active",null),l([d()],zt.prototype,"indicatorIcon",void 0),l([d({type:Boolean})],zt.prototype,"stacked",void 0),l([X((async function(t){await this.updateComplete,this.mdcFoundation.setFocusOnActivate(t)})),d({type:Boolean})],zt.prototype,"focusOnActivate",void 0),l([c(".mdc-tab__content")],zt.prototype,"_contentElement",void 0),l([b()],zt.prototype,"shouldRenderRipple",void 0),l([b()],zt.prototype,"useStateLayerCustomProperties",void 0),l([v("mwc-ripple")],zt.prototype,"ripple",void 0),l([y({passive:!0})],zt.prototype,"handleRippleTouchStart",null);const Mt=f`.material-icons{font-family:var(--mdc-icon-font, "Material Icons");font-weight:normal;font-style:normal;font-size:var(--mdc-icon-size, 24px);line-height:1;letter-spacing:normal;text-transform:none;display:inline-block;white-space:nowrap;word-wrap:normal;direction:ltr;-webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility;-moz-osx-font-smoothing:grayscale;font-feature-settings:"liga"}.mdc-tab{-moz-osx-font-smoothing:grayscale;-webkit-font-smoothing:antialiased;font-family:Roboto, sans-serif;font-family:var(--mdc-typography-button-font-family, var(--mdc-typography-font-family, Roboto, sans-serif));font-size:0.875rem;font-size:var(--mdc-typography-button-font-size, 0.875rem);line-height:2.25rem;line-height:var(--mdc-typography-button-line-height, 2.25rem);font-weight:500;font-weight:var(--mdc-typography-button-font-weight, 500);letter-spacing:0.0892857143em;letter-spacing:var(--mdc-typography-button-letter-spacing, 0.0892857143em);text-decoration:none;text-decoration:var(--mdc-typography-button-text-decoration, none);text-transform:uppercase;text-transform:var(--mdc-typography-button-text-transform, uppercase);position:relative}.mdc-tab .mdc-tab__text-label{color:rgba(0, 0, 0, 0.6)}.mdc-tab .mdc-tab__icon{color:rgba(0, 0, 0, 0.54);fill:currentColor}.mdc-tab__content{position:relative}.mdc-tab__icon{width:24px;height:24px;font-size:24px}.mdc-tab--active .mdc-tab__text-label{color:#6200ee;color:var(--mdc-theme-primary, #6200ee)}.mdc-tab--active .mdc-tab__icon{color:#6200ee;color:var(--mdc-theme-primary, #6200ee);fill:currentColor}.mdc-tab{background:none}.mdc-tab{min-width:90px;padding-right:24px;padding-left:24px;display:flex;flex:1 0 auto;justify-content:center;box-sizing:border-box;margin:0;padding-top:0;padding-bottom:0;border:none;outline:none;text-align:center;white-space:nowrap;cursor:pointer;-webkit-appearance:none;z-index:1}.mdc-tab::-moz-focus-inner{padding:0;border:0}.mdc-tab--min-width{flex:0 1 auto}.mdc-tab__content{display:flex;align-items:center;justify-content:center;height:inherit;pointer-events:none}.mdc-tab__text-label{transition:150ms color linear;display:inline-block;line-height:1;z-index:2}.mdc-tab__icon{transition:150ms color linear;z-index:2}.mdc-tab--stacked .mdc-tab__content{flex-direction:column;align-items:center;justify-content:center}.mdc-tab--stacked .mdc-tab__text-label{padding-top:6px;padding-bottom:4px}.mdc-tab--active .mdc-tab__text-label,.mdc-tab--active .mdc-tab__icon{transition-delay:100ms}.mdc-tab:not(.mdc-tab--stacked) .mdc-tab__icon+.mdc-tab__text-label{padding-left:8px;padding-right:0}[dir=rtl] .mdc-tab:not(.mdc-tab--stacked) .mdc-tab__icon+.mdc-tab__text-label,.mdc-tab:not(.mdc-tab--stacked) .mdc-tab__icon+.mdc-tab__text-label[dir=rtl]{padding-left:0;padding-right:8px}@keyframes mdc-ripple-fg-radius-in{from{animation-timing-function:cubic-bezier(0.4, 0, 0.2, 1);transform:translate(var(--mdc-ripple-fg-translate-start, 0)) scale(1)}to{transform:translate(var(--mdc-ripple-fg-translate-end, 0)) scale(var(--mdc-ripple-fg-scale, 1))}}@keyframes mdc-ripple-fg-opacity-in{from{animation-timing-function:linear;opacity:0}to{opacity:var(--mdc-ripple-fg-opacity, 0)}}@keyframes mdc-ripple-fg-opacity-out{from{animation-timing-function:linear;opacity:var(--mdc-ripple-fg-opacity, 0)}to{opacity:0}}.mdc-tab{--mdc-ripple-fg-size: 0;--mdc-ripple-left: 0;--mdc-ripple-top: 0;--mdc-ripple-fg-scale: 1;--mdc-ripple-fg-translate-end: 0;--mdc-ripple-fg-translate-start: 0;-webkit-tap-highlight-color:rgba(0,0,0,0)}.mdc-tab .mdc-tab__ripple::before,.mdc-tab .mdc-tab__ripple::after{position:absolute;border-radius:50%;opacity:0;pointer-events:none;content:""}.mdc-tab .mdc-tab__ripple::before{transition:opacity 15ms linear,background-color 15ms linear;z-index:1;z-index:var(--mdc-ripple-z-index, 1)}.mdc-tab .mdc-tab__ripple::after{z-index:0;z-index:var(--mdc-ripple-z-index, 0)}.mdc-tab.mdc-ripple-upgraded .mdc-tab__ripple::before{transform:scale(var(--mdc-ripple-fg-scale, 1))}.mdc-tab.mdc-ripple-upgraded .mdc-tab__ripple::after{top:0;left:0;transform:scale(0);transform-origin:center center}.mdc-tab.mdc-ripple-upgraded--unbounded .mdc-tab__ripple::after{top:var(--mdc-ripple-top, 0);left:var(--mdc-ripple-left, 0)}.mdc-tab.mdc-ripple-upgraded--foreground-activation .mdc-tab__ripple::after{animation:mdc-ripple-fg-radius-in 225ms forwards,mdc-ripple-fg-opacity-in 75ms forwards}.mdc-tab.mdc-ripple-upgraded--foreground-deactivation .mdc-tab__ripple::after{animation:mdc-ripple-fg-opacity-out 150ms;transform:translate(var(--mdc-ripple-fg-translate-end, 0)) scale(var(--mdc-ripple-fg-scale, 1))}.mdc-tab .mdc-tab__ripple::before,.mdc-tab .mdc-tab__ripple::after{top:calc(50% - 100%);left:calc(50% - 100%);width:200%;height:200%}.mdc-tab.mdc-ripple-upgraded .mdc-tab__ripple::after{width:var(--mdc-ripple-fg-size, 100%);height:var(--mdc-ripple-fg-size, 100%)}.mdc-tab .mdc-tab__ripple::before,.mdc-tab .mdc-tab__ripple::after{background-color:#6200ee;background-color:var(--mdc-ripple-color, var(--mdc-theme-primary, #6200ee))}.mdc-tab:hover .mdc-tab__ripple::before,.mdc-tab.mdc-ripple-surface--hover .mdc-tab__ripple::before{opacity:0.04;opacity:var(--mdc-ripple-hover-opacity, 0.04)}.mdc-tab.mdc-ripple-upgraded--background-focused .mdc-tab__ripple::before,.mdc-tab:not(.mdc-ripple-upgraded):focus .mdc-tab__ripple::before{transition-duration:75ms;opacity:0.12;opacity:var(--mdc-ripple-focus-opacity, 0.12)}.mdc-tab:not(.mdc-ripple-upgraded) .mdc-tab__ripple::after{transition:opacity 150ms linear}.mdc-tab:not(.mdc-ripple-upgraded):active .mdc-tab__ripple::after{transition-duration:75ms;opacity:0.12;opacity:var(--mdc-ripple-press-opacity, 0.12)}.mdc-tab.mdc-ripple-upgraded{--mdc-ripple-fg-opacity:var(--mdc-ripple-press-opacity, 0.12)}.mdc-tab__ripple{position:absolute;top:0;left:0;width:100%;height:100%;overflow:hidden;will-change:transform,opacity}:host{outline:none;flex:1 0 auto;display:flex;justify-content:center;-webkit-tap-highlight-color:transparent}.mdc-tab{height:var(--mdc-tab-height, 48px);margin-left:0;margin-right:0;padding-right:var(--mdc-tab-horizontal-padding, 24px);padding-left:var(--mdc-tab-horizontal-padding, 24px)}.mdc-tab--stacked{height:var(--mdc-tab-stacked-height, 72px)}.mdc-tab::-moz-focus-inner{border:0}.mdc-tab:not(.mdc-tab--stacked) .mdc-tab__icon+.mdc-tab__text-label{padding-left:8px;padding-right:0}[dir=rtl] .mdc-tab:not(.mdc-tab--stacked) .mdc-tab__icon+.mdc-tab__text-label,.mdc-tab:not(.mdc-tab--stacked) .mdc-tab__icon+.mdc-tab__text-label[dir=rtl]{padding-left:0;padding-right:8px}.mdc-tab:not(.mdc-tab--active) .mdc-tab__text-label{color:var(--mdc-tab-text-label-color-default, rgba(0, 0, 0, 0.6))}.mdc-tab:not(.mdc-tab--active) .mdc-tab__icon{color:var(--mdc-tab-color-default, rgba(0, 0, 0, 0.54))}`;let Nt=class extends zt{};Nt.styles=[Mt],Nt=l([g("mwc-tab")],Nt);var jt={ANIMATING:"mdc-tab-scroller--animating",SCROLL_AREA_SCROLL:"mdc-tab-scroller__scroll-area--scroll",SCROLL_TEST:"mdc-tab-scroller__test"},Ft={AREA_SELECTOR:".mdc-tab-scroller__scroll-area",CONTENT_SELECTOR:".mdc-tab-scroller__scroll-content"},Pt=function(t){this.adapter=t},Bt=function(t){function e(){return null!==t&&t.apply(this,arguments)||this}return o(e,t),e.prototype.getScrollPositionRTL=function(){var t=this.adapter.getScrollAreaScrollLeft(),e=this.calculateScrollEdges().right;return Math.round(e-t)},e.prototype.scrollToRTL=function(t){var e=this.calculateScrollEdges(),a=this.adapter.getScrollAreaScrollLeft(),i=this.clampScrollValue(e.right-t);return{finalScrollPosition:i,scrollDelta:i-a}},e.prototype.incrementScrollRTL=function(t){var e=this.adapter.getScrollAreaScrollLeft(),a=this.clampScrollValue(e-t);return{finalScrollPosition:a,scrollDelta:a-e}},e.prototype.getAnimatingScrollPosition=function(t){return t},e.prototype.calculateScrollEdges=function(){return{left:0,right:this.adapter.getScrollContentOffsetWidth()-this.adapter.getScrollAreaOffsetWidth()}},e.prototype.clampScrollValue=function(t){var e=this.calculateScrollEdges();return Math.min(Math.max(e.left,t),e.right)},e}(Pt),Ht=function(t){function e(){return null!==t&&t.apply(this,arguments)||this}return o(e,t),e.prototype.getScrollPositionRTL=function(t){var e=this.adapter.getScrollAreaScrollLeft();return Math.round(t-e)},e.prototype.scrollToRTL=function(t){var e=this.adapter.getScrollAreaScrollLeft(),a=this.clampScrollValue(-t);return{finalScrollPosition:a,scrollDelta:a-e}},e.prototype.incrementScrollRTL=function(t){var e=this.adapter.getScrollAreaScrollLeft(),a=this.clampScrollValue(e-t);return{finalScrollPosition:a,scrollDelta:a-e}},e.prototype.getAnimatingScrollPosition=function(t,e){return t-e},e.prototype.calculateScrollEdges=function(){var t=this.adapter.getScrollContentOffsetWidth();return{left:this.adapter.getScrollAreaOffsetWidth()-t,right:0}},e.prototype.clampScrollValue=function(t){var e=this.calculateScrollEdges();return Math.max(Math.min(e.right,t),e.left)},e}(Pt),Gt=function(t){function e(){return null!==t&&t.apply(this,arguments)||this}return o(e,t),e.prototype.getScrollPositionRTL=function(t){var e=this.adapter.getScrollAreaScrollLeft();return Math.round(e-t)},e.prototype.scrollToRTL=function(t){var e=this.adapter.getScrollAreaScrollLeft(),a=this.clampScrollValue(t);return{finalScrollPosition:a,scrollDelta:e-a}},e.prototype.incrementScrollRTL=function(t){var e=this.adapter.getScrollAreaScrollLeft(),a=this.clampScrollValue(e+t);return{finalScrollPosition:a,scrollDelta:e-a}},e.prototype.getAnimatingScrollPosition=function(t,e){return t+e},e.prototype.calculateScrollEdges=function(){return{left:this.adapter.getScrollContentOffsetWidth()-this.adapter.getScrollAreaOffsetWidth(),right:0}},e.prototype.clampScrollValue=function(t){var e=this.calculateScrollEdges();return Math.min(Math.max(e.right,t),e.left)},e}(Pt),Kt=function(t){function e(a){var i=t.call(this,r(r({},e.defaultAdapter),a))||this;return i.isAnimating=!1,i}return o(e,t),Object.defineProperty(e,"cssClasses",{get:function(){return jt},enumerable:!1,configurable:!0}),Object.defineProperty(e,"strings",{get:function(){return Ft},enumerable:!1,configurable:!0}),Object.defineProperty(e,"defaultAdapter",{get:function(){return{eventTargetMatchesSelector:function(){return!1},addClass:function(){},removeClass:function(){},addScrollAreaClass:function(){},setScrollAreaStyleProperty:function(){},setScrollContentStyleProperty:function(){},getScrollContentStyleValue:function(){return""},setScrollAreaScrollLeft:function(){},getScrollAreaScrollLeft:function(){return 0},getScrollContentOffsetWidth:function(){return 0},getScrollAreaOffsetWidth:function(){return 0},computeScrollAreaClientRect:function(){return{top:0,right:0,bottom:0,left:0,width:0,height:0}},computeScrollContentClientRect:function(){return{top:0,right:0,bottom:0,left:0,width:0,height:0}},computeHorizontalScrollbarHeight:function(){return 0}}},enumerable:!1,configurable:!0}),e.prototype.init=function(){var t=this.adapter.computeHorizontalScrollbarHeight();this.adapter.setScrollAreaStyleProperty("margin-bottom",-t+"px"),this.adapter.addScrollAreaClass(e.cssClasses.SCROLL_AREA_SCROLL)},e.prototype.getScrollPosition=function(){if(this.isRTL())return this.computeCurrentScrollPositionRTL();var t=this.calculateCurrentTranslateX();return this.adapter.getScrollAreaScrollLeft()-t},e.prototype.handleInteraction=function(){this.isAnimating&&this.stopScrollAnimation()},e.prototype.handleTransitionEnd=function(t){var a=t.target;this.isAnimating&&this.adapter.eventTargetMatchesSelector(a,e.strings.CONTENT_SELECTOR)&&(this.isAnimating=!1,this.adapter.removeClass(e.cssClasses.ANIMATING))},e.prototype.incrementScroll=function(t){0!==t&&this.animate(this.getIncrementScrollOperation(t))},e.prototype.incrementScrollImmediate=function(t){if(0!==t){var e=this.getIncrementScrollOperation(t);0!==e.scrollDelta&&(this.stopScrollAnimation(),this.adapter.setScrollAreaScrollLeft(e.finalScrollPosition))}},e.prototype.scrollTo=function(t){this.isRTL()?this.scrollToImplRTL(t):this.scrollToImpl(t)},e.prototype.getRTLScroller=function(){return this.rtlScrollerInstance||(this.rtlScrollerInstance=this.rtlScrollerFactory()),this.rtlScrollerInstance},e.prototype.calculateCurrentTranslateX=function(){var t=this.adapter.getScrollContentStyleValue("transform");if("none"===t)return 0;var e=/\((.+?)\)/.exec(t);if(!e)return 0;var a=e[1],i=k(a.split(","),6);i[0],i[1],i[2],i[3];var n=i[4];return i[5],parseFloat(n)},e.prototype.clampScrollValue=function(t){var e=this.calculateScrollEdges();return Math.min(Math.max(e.left,t),e.right)},e.prototype.computeCurrentScrollPositionRTL=function(){var t=this.calculateCurrentTranslateX();return this.getRTLScroller().getScrollPositionRTL(t)},e.prototype.calculateScrollEdges=function(){return{left:0,right:this.adapter.getScrollContentOffsetWidth()-this.adapter.getScrollAreaOffsetWidth()}},e.prototype.scrollToImpl=function(t){var e=this.getScrollPosition(),a=this.clampScrollValue(t),i=a-e;this.animate({finalScrollPosition:a,scrollDelta:i})},e.prototype.scrollToImplRTL=function(t){var e=this.getRTLScroller().scrollToRTL(t);this.animate(e)},e.prototype.getIncrementScrollOperation=function(t){if(this.isRTL())return this.getRTLScroller().incrementScrollRTL(t);var e=this.getScrollPosition(),a=t+e,i=this.clampScrollValue(a);return{finalScrollPosition:i,scrollDelta:i-e}},e.prototype.animate=function(t){var a=this;0!==t.scrollDelta&&(this.stopScrollAnimation(),this.adapter.setScrollAreaScrollLeft(t.finalScrollPosition),this.adapter.setScrollContentStyleProperty("transform","translateX("+t.scrollDelta+"px)"),this.adapter.computeScrollAreaClientRect(),requestAnimationFrame((function(){a.adapter.addClass(e.cssClasses.ANIMATING),a.adapter.setScrollContentStyleProperty("transform","none")})),this.isAnimating=!0)},e.prototype.stopScrollAnimation=function(){this.isAnimating=!1;var t=this.getAnimatingScrollPosition();this.adapter.removeClass(e.cssClasses.ANIMATING),this.adapter.setScrollContentStyleProperty("transform","translateX(0px)"),this.adapter.setScrollAreaScrollLeft(t)},e.prototype.getAnimatingScrollPosition=function(){var t=this.calculateCurrentTranslateX(),e=this.adapter.getScrollAreaScrollLeft();return this.isRTL()?this.getRTLScroller().getAnimatingScrollPosition(e,t):e-t},e.prototype.rtlScrollerFactory=function(){var t=this.adapter.getScrollAreaScrollLeft();this.adapter.setScrollAreaScrollLeft(t-1);var e=this.adapter.getScrollAreaScrollLeft();if(e<0)return this.adapter.setScrollAreaScrollLeft(t),new Ht(this.adapter);var a=this.adapter.computeScrollAreaClientRect(),i=this.adapter.computeScrollContentClientRect(),n=Math.round(i.right-a.right);return this.adapter.setScrollAreaScrollLeft(t),n===e?new Gt(this.adapter):new Bt(this.adapter)},e.prototype.isRTL=function(){return"rtl"===this.adapter.getScrollContentStyleValue("direction")},e}(s),Ut=Kt;class Wt extends h{constructor(){super(...arguments),this.mdcFoundationClass=Ut,this._scrollbarHeight=-1}_handleInteraction(){this.mdcFoundation.handleInteraction()}_handleTransitionEnd(t){this.mdcFoundation.handleTransitionEnd(t)}render(){return p`
      <div class="mdc-tab-scroller">
        <div class="mdc-tab-scroller__scroll-area"
            @wheel="${this._handleInteraction}"
            @touchstart="${this._handleInteraction}"
            @pointerdown="${this._handleInteraction}"
            @mousedown="${this._handleInteraction}"
            @keydown="${this._handleInteraction}"
            @transitionend="${this._handleTransitionEnd}">
          <div class="mdc-tab-scroller__scroll-content"><slot></slot></div>
        </div>
      </div>
      `}createAdapter(){return Object.assign(Object.assign({},m(this.mdcRoot)),{eventTargetMatchesSelector:(t,e)=>x(t,e),addScrollAreaClass:t=>this.scrollAreaElement.classList.add(t),setScrollAreaStyleProperty:(t,e)=>this.scrollAreaElement.style.setProperty(t,e),setScrollContentStyleProperty:(t,e)=>this.scrollContentElement.style.setProperty(t,e),getScrollContentStyleValue:t=>window.getComputedStyle(this.scrollContentElement).getPropertyValue(t),setScrollAreaScrollLeft:t=>this.scrollAreaElement.scrollLeft=t,getScrollAreaScrollLeft:()=>this.scrollAreaElement.scrollLeft,getScrollContentOffsetWidth:()=>this.scrollContentElement.offsetWidth,getScrollAreaOffsetWidth:()=>this.scrollAreaElement.offsetWidth,computeScrollAreaClientRect:()=>this.scrollAreaElement.getBoundingClientRect(),computeScrollContentClientRect:()=>this.scrollContentElement.getBoundingClientRect(),computeHorizontalScrollbarHeight:()=>(-1===this._scrollbarHeight&&(this.scrollAreaElement.style.overflowX="scroll",this._scrollbarHeight=this.scrollAreaElement.offsetHeight-this.scrollAreaElement.clientHeight,this.scrollAreaElement.style.overflowX=""),this._scrollbarHeight)})}getScrollPosition(){return this.mdcFoundation.getScrollPosition()}getScrollContentWidth(){return this.scrollContentElement.offsetWidth}incrementScrollPosition(t){this.mdcFoundation.incrementScroll(t)}scrollToPosition(t){this.mdcFoundation.scrollTo(t)}}l([c(".mdc-tab-scroller")],Wt.prototype,"mdcRoot",void 0),l([c(".mdc-tab-scroller__scroll-area")],Wt.prototype,"scrollAreaElement",void 0),l([c(".mdc-tab-scroller__scroll-content")],Wt.prototype,"scrollContentElement",void 0),l([y({passive:!0})],Wt.prototype,"_handleInteraction",null);const Vt=f`.mdc-tab-scroller{overflow-y:hidden}.mdc-tab-scroller.mdc-tab-scroller--animating .mdc-tab-scroller__scroll-content{transition:250ms transform cubic-bezier(0.4, 0, 0.2, 1)}.mdc-tab-scroller__test{position:absolute;top:-9999px;width:100px;height:100px;overflow-x:scroll}.mdc-tab-scroller__scroll-area{-webkit-overflow-scrolling:touch;display:flex;overflow-x:hidden}.mdc-tab-scroller__scroll-area::-webkit-scrollbar,.mdc-tab-scroller__test::-webkit-scrollbar{display:none}.mdc-tab-scroller__scroll-area--scroll{overflow-x:scroll}.mdc-tab-scroller__scroll-content{position:relative;display:flex;flex:1 0 auto;transform:none;will-change:transform}.mdc-tab-scroller--align-start .mdc-tab-scroller__scroll-content{justify-content:flex-start}.mdc-tab-scroller--align-end .mdc-tab-scroller__scroll-content{justify-content:flex-end}.mdc-tab-scroller--align-center .mdc-tab-scroller__scroll-content{justify-content:center}.mdc-tab-scroller--animating .mdc-tab-scroller__scroll-area{-webkit-overflow-scrolling:auto}:host{display:flex}.mdc-tab-scroller{flex:1}`;let Yt=class extends Wt{};Yt.styles=[Vt],Yt=l([g("mwc-tab-scroller")],Yt);var Xt={ARROW_LEFT_KEY:"ArrowLeft",ARROW_RIGHT_KEY:"ArrowRight",END_KEY:"End",ENTER_KEY:"Enter",HOME_KEY:"Home",SPACE_KEY:"Space",TAB_ACTIVATED_EVENT:"MDCTabBar:activated",TAB_SCROLLER_SELECTOR:".mdc-tab-scroller",TAB_SELECTOR:".mdc-tab"},qt={ARROW_LEFT_KEYCODE:37,ARROW_RIGHT_KEYCODE:39,END_KEYCODE:35,ENTER_KEYCODE:13,EXTRA_SCROLL_AMOUNT:20,HOME_KEYCODE:36,SPACE_KEYCODE:32},Zt=new Set;Zt.add(Xt.ARROW_LEFT_KEY),Zt.add(Xt.ARROW_RIGHT_KEY),Zt.add(Xt.END_KEY),Zt.add(Xt.HOME_KEY),Zt.add(Xt.ENTER_KEY),Zt.add(Xt.SPACE_KEY);var Qt=new Map;Qt.set(qt.ARROW_LEFT_KEYCODE,Xt.ARROW_LEFT_KEY),Qt.set(qt.ARROW_RIGHT_KEYCODE,Xt.ARROW_RIGHT_KEY),Qt.set(qt.END_KEYCODE,Xt.END_KEY),Qt.set(qt.HOME_KEYCODE,Xt.HOME_KEY),Qt.set(qt.ENTER_KEYCODE,Xt.ENTER_KEY),Qt.set(qt.SPACE_KEYCODE,Xt.SPACE_KEY);var Jt=function(t){function e(a){var i=t.call(this,r(r({},e.defaultAdapter),a))||this;return i.useAutomaticActivation=!1,i}return o(e,t),Object.defineProperty(e,"strings",{get:function(){return Xt},enumerable:!1,configurable:!0}),Object.defineProperty(e,"numbers",{get:function(){return qt},enumerable:!1,configurable:!0}),Object.defineProperty(e,"defaultAdapter",{get:function(){return{scrollTo:function(){},incrementScroll:function(){},getScrollPosition:function(){return 0},getScrollContentWidth:function(){return 0},getOffsetWidth:function(){return 0},isRTL:function(){return!1},setActiveTab:function(){},activateTabAtIndex:function(){},deactivateTabAtIndex:function(){},focusTabAtIndex:function(){},getTabIndicatorClientRectAtIndex:function(){return{top:0,right:0,bottom:0,left:0,width:0,height:0}},getTabDimensionsAtIndex:function(){return{rootLeft:0,rootRight:0,contentLeft:0,contentRight:0}},getPreviousActiveTabIndex:function(){return-1},getFocusedTabIndex:function(){return-1},getIndexOfTabById:function(){return-1},getTabListLength:function(){return 0},notifyTabActivated:function(){}}},enumerable:!1,configurable:!0}),e.prototype.setUseAutomaticActivation=function(t){this.useAutomaticActivation=t},e.prototype.activateTab=function(t){var e,a=this.adapter.getPreviousActiveTabIndex();this.indexIsInRange(t)&&t!==a&&(-1!==a&&(this.adapter.deactivateTabAtIndex(a),e=this.adapter.getTabIndicatorClientRectAtIndex(a)),this.adapter.activateTabAtIndex(t,e),this.scrollIntoView(t),this.adapter.notifyTabActivated(t))},e.prototype.handleKeyDown=function(t){var e=this.getKeyFromEvent(t);if(void 0!==e)if(this.isActivationKey(e)||t.preventDefault(),this.useAutomaticActivation){if(this.isActivationKey(e))return;var a=this.determineTargetFromKey(this.adapter.getPreviousActiveTabIndex(),e);this.adapter.setActiveTab(a),this.scrollIntoView(a)}else{var i=this.adapter.getFocusedTabIndex();if(this.isActivationKey(e))this.adapter.setActiveTab(i);else{a=this.determineTargetFromKey(i,e);this.adapter.focusTabAtIndex(a),this.scrollIntoView(a)}}},e.prototype.handleTabInteraction=function(t){this.adapter.setActiveTab(this.adapter.getIndexOfTabById(t.detail.tabId))},e.prototype.scrollIntoView=function(t){this.indexIsInRange(t)&&(0!==t?t!==this.adapter.getTabListLength()-1?this.isRTL()?this.scrollIntoViewImplRTL(t):this.scrollIntoViewImpl(t):this.adapter.scrollTo(this.adapter.getScrollContentWidth()):this.adapter.scrollTo(0))},e.prototype.determineTargetFromKey=function(t,e){var a=this.isRTL(),i=this.adapter.getTabListLength()-1,n=t;return e===Xt.END_KEY?n=i:e===Xt.ARROW_LEFT_KEY&&!a||e===Xt.ARROW_RIGHT_KEY&&a?n-=1:e===Xt.ARROW_RIGHT_KEY&&!a||e===Xt.ARROW_LEFT_KEY&&a?n+=1:n=0,n<0?n=i:n>i&&(n=0),n},e.prototype.calculateScrollIncrement=function(t,e,a,i){var n=this.adapter.getTabDimensionsAtIndex(e),o=n.contentLeft-a-i,r=n.contentRight-a-qt.EXTRA_SCROLL_AMOUNT,s=o+qt.EXTRA_SCROLL_AMOUNT;return e<t?Math.min(r,0):Math.max(s,0)},e.prototype.calculateScrollIncrementRTL=function(t,e,a,i,n){var o=this.adapter.getTabDimensionsAtIndex(e),r=n-o.contentLeft-a,s=n-o.contentRight-a-i+qt.EXTRA_SCROLL_AMOUNT,l=r-qt.EXTRA_SCROLL_AMOUNT;return e>t?Math.max(s,0):Math.min(l,0)},e.prototype.findAdjacentTabIndexClosestToEdge=function(t,e,a,i){var n=e.rootLeft-a,o=e.rootRight-a-i,r=n+o;return n<0||r<0?t-1:o>0||r>0?t+1:-1},e.prototype.findAdjacentTabIndexClosestToEdgeRTL=function(t,e,a,i,n){var o=n-e.rootLeft-i-a,r=n-e.rootRight-a,s=o+r;return o>0||s>0?t+1:r<0||s<0?t-1:-1},e.prototype.getKeyFromEvent=function(t){return Zt.has(t.key)?t.key:Qt.get(t.keyCode)},e.prototype.isActivationKey=function(t){return t===Xt.SPACE_KEY||t===Xt.ENTER_KEY},e.prototype.indexIsInRange=function(t){return t>=0&&t<this.adapter.getTabListLength()},e.prototype.isRTL=function(){return this.adapter.isRTL()},e.prototype.scrollIntoViewImpl=function(t){var e=this.adapter.getScrollPosition(),a=this.adapter.getOffsetWidth(),i=this.adapter.getTabDimensionsAtIndex(t),n=this.findAdjacentTabIndexClosestToEdge(t,i,e,a);if(this.indexIsInRange(n)){var o=this.calculateScrollIncrement(t,n,e,a);this.adapter.incrementScroll(o)}},e.prototype.scrollIntoViewImplRTL=function(t){var e=this.adapter.getScrollPosition(),a=this.adapter.getOffsetWidth(),i=this.adapter.getTabDimensionsAtIndex(t),n=this.adapter.getScrollContentWidth(),o=this.findAdjacentTabIndexClosestToEdgeRTL(t,i,e,a,n);if(this.indexIsInRange(o)){var r=this.calculateScrollIncrementRTL(t,o,e,a,n);this.adapter.incrementScroll(r)}},e}(s);class te extends h{constructor(){super(...arguments),this.mdcFoundationClass=Jt,this.activeIndex=0,this._previousActiveIndex=-1}_handleTabInteraction(t){this.mdcFoundation.handleTabInteraction(t)}_handleKeydown(t){this.mdcFoundation.handleKeyDown(t)}render(){return p`
      <div class="mdc-tab-bar" role="tablist"
          @MDCTab:interacted="${this._handleTabInteraction}"
          @keydown="${this._handleKeydown}">
        <mwc-tab-scroller><slot></slot></mwc-tab-scroller>
      </div>
      `}_getTabs(){return this.tabsSlot.assignedNodes({flatten:!0}).filter((t=>t instanceof zt))}_getTab(t){return this._getTabs()[t]}createAdapter(){return{scrollTo:t=>this.scrollerElement.scrollToPosition(t),incrementScroll:t=>this.scrollerElement.incrementScrollPosition(t),getScrollPosition:()=>this.scrollerElement.getScrollPosition(),getScrollContentWidth:()=>this.scrollerElement.getScrollContentWidth(),getOffsetWidth:()=>this.mdcRoot.offsetWidth,isRTL:()=>"rtl"===window.getComputedStyle(this.mdcRoot).getPropertyValue("direction"),setActiveTab:t=>this.mdcFoundation.activateTab(t),activateTabAtIndex:(t,e)=>{const a=this._getTab(t);void 0!==a&&a.activate(e),this._previousActiveIndex=t},deactivateTabAtIndex:t=>{const e=this._getTab(t);void 0!==e&&e.deactivate()},focusTabAtIndex:t=>{const e=this._getTab(t);void 0!==e&&e.focus()},getTabIndicatorClientRectAtIndex:t=>{const e=this._getTab(t);return void 0!==e?e.computeIndicatorClientRect():new DOMRect},getTabDimensionsAtIndex:t=>{const e=this._getTab(t);return void 0!==e?e.computeDimensions():{rootLeft:0,rootRight:0,contentLeft:0,contentRight:0}},getPreviousActiveTabIndex:()=>this._previousActiveIndex,getFocusedTabIndex:()=>{const t=this._getTabs(),e=this.getRootNode().activeElement;return t.indexOf(e)},getIndexOfTabById:t=>{const e=this._getTabs();for(let a=0;a<e.length;a++)if(e[a].id===t)return a;return-1},getTabListLength:()=>this._getTabs().length,notifyTabActivated:t=>{this.activeIndex=t,this.dispatchEvent(new CustomEvent(Jt.strings.TAB_ACTIVATED_EVENT,{detail:{index:t},bubbles:!0,cancelable:!0}))}}}firstUpdated(){}async getUpdateComplete(){const t=await super.getUpdateComplete();return await this.scrollerElement.updateComplete,void 0===this.mdcFoundation&&this.createFoundation(),t}scrollIndexIntoView(t){this.mdcFoundation.scrollIntoView(t)}}l([c(".mdc-tab-bar")],te.prototype,"mdcRoot",void 0),l([c("mwc-tab-scroller")],te.prototype,"scrollerElement",void 0),l([c("slot")],te.prototype,"tabsSlot",void 0),l([X((async function(){await this.updateComplete,this.activeIndex!==this._previousActiveIndex&&this.mdcFoundation.activateTab(this.activeIndex)})),d({type:Number})],te.prototype,"activeIndex",void 0);const ee=f`.mdc-tab-bar{width:100%}.mdc-tab{height:48px}.mdc-tab--stacked{height:72px}:host{display:block}.mdc-tab-bar{flex:1}mwc-tab{--mdc-tab-height: 48px;--mdc-tab-stacked-height: 72px}`;let ae=class extends te{};ae.styles=[ee],ae=l([g("mwc-tab-bar")],ae);const ie=(t,e)=>{var a,i;const n=t._$AN;if(void 0===n)return!1;for(const t of n)null===(i=(a=t)._$AO)||void 0===i||i.call(a,e,!1),ie(t,e);return!0},ne=t=>{let e,a;do{if(void 0===(e=t._$AM))break;a=e._$AN,a.delete(t),t=e}while(0===(null==a?void 0:a.size))},oe=t=>{for(let e;e=t._$AM;t=e){let a=e._$AN;if(void 0===a)e._$AN=a=new Set;else if(a.has(t))break;a.add(t),le(e)}};function re(t){void 0!==this._$AN?(ne(this),this._$AM=t,oe(this)):this._$AM=t}function se(t,e=!1,a=0){const i=this._$AH,n=this._$AN;if(void 0!==n&&0!==n.size)if(e)if(Array.isArray(i))for(let t=a;t<i.length;t++)ie(i[t],!1),ne(i[t]);else null!=i&&(ie(i,!1),ne(i));else ie(this,t)}const le=t=>{var e,a,i,n;t.type==w.CHILD&&(null!==(e=(i=t)._$AP)&&void 0!==e||(i._$AP=se),null!==(a=(n=t)._$AQ)&&void 0!==a||(n._$AQ=re))};class ce extends e{constructor(){super(...arguments),this._$AN=void 0}_$AT(t,e,a){super._$AT(t,e,a),oe(this),this.isConnected=t._$AU}_$AO(t,e=!0){var a,i;t!==this.isConnected&&(this.isConnected=t,t?null===(a=this.reconnected)||void 0===a||a.call(this):null===(i=this.disconnected)||void 0===i||i.call(this)),e&&(ie(this,t),ne(this))}setValue(t){if(q(this._$Ct))this._$Ct._$AI(t,this);else{const e=[...this._$Ct._$AH];e[this._$Ci]=t,this._$Ct._$AI(e,this,0)}}disconnected(){}reconnected(){}}class de{constructor(t){this.U=t}disconnect(){this.U=void 0}reconnect(t){this.U=t}deref(){return this.U}}class he{constructor(){this.Y=void 0,this.q=void 0}get(){return this.Y}pause(){var t;null!==(t=this.Y)&&void 0!==t||(this.Y=new Promise((t=>this.q=t)))}resume(){var t;null===(t=this.q)||void 0===t||t.call(this),this.Y=this.q=void 0}}const pe=t=>!Z(t)&&"function"==typeof t.then;const ue=t(class extends ce{constructor(){super(...arguments),this._$Cft=1073741823,this._$Cwt=[],this._$CG=new de(this),this._$CK=new he}render(...t){var e;return null!==(e=t.find((t=>!pe(t))))&&void 0!==e?e:C}update(t,e){const a=this._$Cwt;let i=a.length;this._$Cwt=e;const n=this._$CG,o=this._$CK;this.isConnected||this.disconnected();for(let t=0;t<e.length&&!(t>this._$Cft);t++){const r=e[t];if(!pe(r))return this._$Cft=t,r;t<i&&r===a[t]||(this._$Cft=1073741823,i=0,Promise.resolve(r).then((async t=>{for(;o.get();)await o.get();const e=n.deref();if(void 0!==e){const a=e._$Cwt.indexOf(r);a>-1&&a<e._$Cft&&(e._$Cft=a,e.setValue(t))}})))}return C}disconnected(){this._$CG.disconnect(),this._$CK.pause()}reconnected(){this._$CG.reconnect(this),this._$CK.resume()}});function me(t){return!!t&&(t instanceof Date&&!isNaN(t.valueOf()))}var fe=/-u(?:-[0-9a-z]{2,8})+/gi;function ge(t,e,a){if(void 0===a&&(a=Error),!t)throw new a(e)}function be(t,e){for(var a=e;;){if(t.has(a))return a;var i=a.lastIndexOf("-");if(!~i)return;i>=2&&"-"===a[i-2]&&(i-=2),a=a.slice(0,i)}}function ve(t,e){ge(2===e.length,"key must have 2 elements");var a=t.length,i="-".concat(e,"-"),n=t.indexOf(i);if(-1!==n){for(var o=n+4,r=o,s=o,l=!1;!l;){var c=t.indexOf("-",s);2===(-1===c?a-s:c-s)?l=!0:-1===c?(r=a,l=!0):(r=c,s=c+1)}return t.slice(o,r)}if(i="-".concat(e),-1!==(n=t.indexOf(i))&&n+3===a)return""}function ye(t,e,a,i,n,o){var r;r="lookup"===a.localeMatcher?function(t,e,a){for(var i={locale:""},n=0,o=e;n<o.length;n++){var r=o[n],s=r.replace(fe,""),l=be(t,s);if(l)return i.locale=l,r!==s&&(i.extension=r.slice(s.length+1,r.length)),i}return i.locale=a(),i}(t,e,o):function(t,e,a){var i,n={},o={},r={},s=new Set;t.forEach((function(t){var e=new Intl.Locale(t).minimize().toString(),a=Intl.getCanonicalLocales(t)[0]||t;n[e]=t,o[t]=t,r[a]=t,s.add(e),s.add(t),s.add(a)}));for(var l=0,c=e;l<c.length;l++){var d=c[l];if(i)break;var h=d.replace(fe,"");if(t.has(h)){i=h;break}if(s.has(h)){i=h;break}var p=new Intl.Locale(h),u=p.maximize().toString(),m=p.minimize().toString();if(s.has(m)){i=m;break}i=be(s,u)}return i?{locale:o[i]||r[i]||n[i]||i}:{locale:a()}}(t,e,o);for(var s=r.locale,l={locale:"",dataLocale:s},c="-u",d=0,h=i;d<h.length;d++){var p=h[d];ge(s in n,"Missing locale data for ".concat(s));var u=n[s];ge("object"==typeof u&&null!==u,"locale data ".concat(p," must be an object"));var m=u[p];ge(Array.isArray(m),"keyLocaleData for ".concat(p," must be an array"));var f=m[0];ge("string"==typeof f||null===f,"value must be string or null but got ".concat(typeof f," in key ").concat(p));var g="";if(r.extension){var b=ve(r.extension,p);void 0!==b&&(""!==b?~m.indexOf(b)&&(f=b,g="-".concat(p,"-").concat(f)):~b.indexOf("true")&&(f="true",g="-".concat(p)))}if(p in a){var v=a[p];ge("string"==typeof v||null==v,"optionsValue must be String, Undefined or Null"),~m.indexOf(v)&&v!==f&&(f=v,g="")}l[p]=f,c+=g}if(c.length>2){var y=s.indexOf("-x-");if(-1===y)s+=c;else{var _=s.slice(0,y),k=s.slice(y,s.length);s=_+c+k}s=Intl.getCanonicalLocales(s)[0]}return l.locale=s,l}function _e(t,e,a,i){var n=e.reduce((function(t,e){return t.add(e),t}),new Set);return ye(n,function(t){return Intl.getCanonicalLocales(t)}(t),{localeMatcher:(null==i?void 0:i.algorithm)||"best fit"},[],{},(function(){return a})).locale}var ke=Object.freeze({__proto__:null,match:_e,LookupSupportedLocales:function(t,e){for(var a=[],i=0,n=e;i<n.length;i++){var o=be(t,n[i].replace(fe,""));o&&a.push(o)}return a},ResolveLocale:ye}),xe=["af","ak","am","an","ar","ars","as","asa","ast","az","bal","be","bem","bez","bg","bho","bm","bn","bo","br","brx","bs","ca","ce","ceb","cgg","chr","ckb","cs","cy","da","de","doi","dsb","dv","dz","ee","el","en","eo","es","et","eu","fa","ff","fi","fil","fo","fr","fur","fy","ga","gd","gl","gsw","gu","guw","gv","ha","haw","he","hi","hnj","hr","hsb","hu","hy","ia","id","ig","ii","io","is","it","iu","ja","jbo","jgo","jmc","jv","jw","ka","kab","kaj","kcg","kde","kea","kk","kkj","kl","km","kn","ko","ks","ksb","ksh","ku","kw","ky","lag","lb","lg","lij","lkt","ln","lo","lt","lv","mas","mg","mgo","mk","ml","mn","mo","mr","ms","mt","my","nah","naq","nb","nd","ne","nl","nn","nnh","no","nqo","nr","nso","ny","nyn","om","or","os","osa","pa","pap","pcm","pl","prg","ps","pt-PT","pt","rm","ro","rof","ru","rwk","sah","saq","sat","sc","scn","sd","sdh","se","seh","ses","sg","sh","shi","si","sk","sl","sma","smi","smj","smn","sms","sn","so","sq","sr","ss","ssy","st","su","sv","sw","syr","ta","te","teo","th","ti","tig","tk","tl","tn","to","tpi","tr","ts","tzm","ug","uk","und","ur","uz","ve","vi","vo","vun","wa","wae","wo","xh","xog","yi","yo","yue","zh","zu"];var we=bt((function(t,e){Object.defineProperty(e,"__esModule",{value:!0}),e.CanonicalizeLocaleList=void 0,e.CanonicalizeLocaleList=function(t){return Intl.getCanonicalLocales(t)}}));vt(we),we.CanonicalizeLocaleList;var Ce=bt((function(t,e){Object.defineProperty(e,"__esModule",{value:!0}),e.invariant=e.UNICODE_EXTENSION_SEQUENCE_REGEX=void 0,e.UNICODE_EXTENSION_SEQUENCE_REGEX=/-u(?:-[0-9a-z]{2,8})+/gi,e.invariant=function(t,e,a){if(void 0===a&&(a=Error),!t)throw new a(e)}}));vt(Ce),Ce.invariant,Ce.UNICODE_EXTENSION_SEQUENCE_REGEX;var Se=bt((function(t,e){Object.defineProperty(e,"__esModule",{value:!0}),e.BestAvailableLocale=void 0,e.BestAvailableLocale=function(t,e){for(var a=e;;){if(t.has(a))return a;var i=a.lastIndexOf("-");if(!~i)return;i>=2&&"-"===a[i-2]&&(i-=2),a=a.slice(0,i)}}}));vt(Se),Se.BestAvailableLocale;var Te=bt((function(t,e){Object.defineProperty(e,"__esModule",{value:!0}),e.LookupMatcher=void 0,e.LookupMatcher=function(t,e,a){for(var i={locale:""},n=0,o=e;n<o.length;n++){var r=o[n],s=r.replace(Ce.UNICODE_EXTENSION_SEQUENCE_REGEX,""),l=(0,Se.BestAvailableLocale)(t,s);if(l)return i.locale=l,r!==s&&(i.extension=r.slice(s.length+1,r.length)),i}return i.locale=a(),i}}));vt(Te),Te.LookupMatcher;var Ie=bt((function(t,e){Object.defineProperty(e,"__esModule",{value:!0}),e.BestFitMatcher=void 0,e.BestFitMatcher=function(t,e,a){var i,n={},o={},r={},s=new Set;t.forEach((function(t){var e=new Intl.Locale(t).minimize().toString(),a=Intl.getCanonicalLocales(t)[0]||t;n[e]=t,o[t]=t,r[a]=t,s.add(e),s.add(t),s.add(a)}));for(var l=0,c=e;l<c.length;l++){var d=c[l];if(i)break;var h=d.replace(Ce.UNICODE_EXTENSION_SEQUENCE_REGEX,"");if(t.has(h)){i=h;break}if(s.has(h)){i=h;break}var p=new Intl.Locale(h),u=p.maximize().toString(),m=p.minimize().toString();if(s.has(m)){i=m;break}i=(0,Se.BestAvailableLocale)(s,u)}return i?{locale:o[i]||r[i]||n[i]||i}:{locale:a()}}}));vt(Ie),Ie.BestFitMatcher;var Ee=bt((function(t,e){Object.defineProperty(e,"__esModule",{value:!0}),e.UnicodeExtensionValue=void 0,e.UnicodeExtensionValue=function(t,e){(0,Ce.invariant)(2===e.length,"key must have 2 elements");var a=t.length,i="-".concat(e,"-"),n=t.indexOf(i);if(-1!==n){for(var o=n+4,r=o,s=o,l=!1;!l;){var c=t.indexOf("-",s);2===(-1===c?a-s:c-s)?l=!0:-1===c?(r=a,l=!0):(r=c,s=c+1)}return t.slice(o,r)}if(i="-".concat(e),-1!==(n=t.indexOf(i))&&n+3===a)return""}}));vt(Ee),Ee.UnicodeExtensionValue;var Ae=bt((function(t,e){Object.defineProperty(e,"__esModule",{value:!0}),e.ResolveLocale=void 0,e.ResolveLocale=function(t,e,a,i,n,o){for(var r,s=(r="lookup"===a.localeMatcher?(0,Te.LookupMatcher)(t,e,o):(0,Ie.BestFitMatcher)(t,e,o)).locale,l={locale:"",dataLocale:s},c="-u",d=0,h=i;d<h.length;d++){var p=h[d];(0,Ce.invariant)(s in n,"Missing locale data for ".concat(s));var u=n[s];(0,Ce.invariant)("object"==typeof u&&null!==u,"locale data ".concat(p," must be an object"));var m=u[p];(0,Ce.invariant)(Array.isArray(m),"keyLocaleData for ".concat(p," must be an array"));var f=m[0];(0,Ce.invariant)("string"==typeof f||null===f,"value must be string or null but got ".concat(typeof f," in key ").concat(p));var g="";if(r.extension){var b=(0,Ee.UnicodeExtensionValue)(r.extension,p);void 0!==b&&(""!==b?~m.indexOf(b)&&(f=b,g="-".concat(p,"-").concat(f)):~b.indexOf("true")&&(f="true",g="-".concat(p)))}if(p in a){var v=a[p];(0,Ce.invariant)("string"==typeof v||null==v,"optionsValue must be String, Undefined or Null"),~m.indexOf(v)&&v!==f&&(f=v,g="")}l[p]=f,c+=g}if(c.length>2){var y=s.indexOf("-x-");if(-1===y)s+=c;else{var _=s.slice(0,y),k=s.slice(y,s.length);s=_+c+k}s=Intl.getCanonicalLocales(s)[0]}return l.locale=s,l}}));vt(Ae),Ae.ResolveLocale;var $e=bt((function(t,e){Object.defineProperty(e,"__esModule",{value:!0}),e.LookupSupportedLocales=void 0,e.LookupSupportedLocales=function(t,e){for(var a=[],i=0,n=e;i<n.length;i++){var o=n[i].replace(Ce.UNICODE_EXTENSION_SEQUENCE_REGEX,""),r=(0,Se.BestAvailableLocale)(t,o);r&&a.push(r)}return a}}));vt($e),$e.LookupSupportedLocales;var Le=bt((function(t,e){Object.defineProperty(e,"__esModule",{value:!0}),e.ResolveLocale=e.LookupSupportedLocales=e.match=void 0,e.match=function(t,e,a,i){var n=e.reduce((function(t,e){return t.add(e),t}),new Set);return(0,Ae.ResolveLocale)(n,(0,we.CanonicalizeLocaleList)(t),{localeMatcher:(null==i?void 0:i.algorithm)||"best fit"},[],{},(function(){return a})).locale},Object.defineProperty(e,"LookupSupportedLocales",{enumerable:!0,get:function(){return $e.LookupSupportedLocales}});var a=Ae;Object.defineProperty(e,"ResolveLocale",{enumerable:!0,get:function(){return a.ResolveLocale}})}));vt(Le);var Re=Le.ResolveLocale,Oe=Le.LookupSupportedLocales,De=Le.match,ze=["af-NA","af","agq","ak","am","ar-AE","ar-BH","ar-DJ","ar-DZ","ar-EG","ar-EH","ar-ER","ar-IL","ar-IQ","ar-JO","ar-KM","ar-KW","ar-LB","ar-LY","ar-MA","ar-MR","ar-OM","ar-PS","ar-QA","ar-SA","ar-SD","ar-SO","ar-SS","ar-SY","ar-TD","ar-TN","ar-YE","ar","as","asa","ast","az-Cyrl","az-Latn","az","bas","be-tarask","be","bem","bez","bg","bm","bn-IN","bn","bo-IN","bo","br","brx","bs-Cyrl","bs-Latn","bs","ca-AD","ca-ES-valencia","ca-FR","ca-IT","ca","ccp-IN","ccp","ce","ceb","cgg","chr","ckb-IR","ckb","cs","cy","da-GL","da","dav","de-AT","de-BE","de-CH","de-IT","de-LI","de-LU","de","dje","doi","dsb","dua","dyo","dz","ebu","ee-TG","ee","el-CY","el","en-001","en-150","en-AE","en-AG","en-AI","en-AS","en-AT","en-AU","en-BB","en-BE","en-BI","en-BM","en-BS","en-BW","en-BZ","en-CA","en-CC","en-CH","en-CK","en-CM","en-CX","en-CY","en-DE","en-DG","en-DK","en-DM","en-ER","en-FI","en-FJ","en-FK","en-FM","en-GB","en-GD","en-GG","en-GH","en-GI","en-GM","en-GU","en-GY","en-HK","en-IE","en-IL","en-IM","en-IN","en-IO","en-JE","en-JM","en-KE","en-KI","en-KN","en-KY","en-LC","en-LR","en-LS","en-MG","en-MH","en-MO","en-MP","en-MS","en-MT","en-MU","en-MW","en-MY","en-NA","en-NF","en-NG","en-NL","en-NR","en-NU","en-NZ","en-PG","en-PH","en-PK","en-PN","en-PR","en-PW","en-RW","en-SB","en-SC","en-SD","en-SE","en-SG","en-SH","en-SI","en-SL","en-SS","en-SX","en-SZ","en-TC","en-TK","en-TO","en-TT","en-TV","en-TZ","en-UG","en-UM","en-VC","en-VG","en-VI","en-VU","en-WS","en-ZA","en-ZM","en-ZW","en","eo","es-419","es-AR","es-BO","es-BR","es-BZ","es-CL","es-CO","es-CR","es-CU","es-DO","es-EA","es-EC","es-GQ","es-GT","es-HN","es-IC","es-MX","es-NI","es-PA","es-PE","es-PH","es-PR","es-PY","es-SV","es-US","es-UY","es-VE","es","et","eu","ewo","fa-AF","fa","ff-Adlm-BF","ff-Adlm-CM","ff-Adlm-GH","ff-Adlm-GM","ff-Adlm-GW","ff-Adlm-LR","ff-Adlm-MR","ff-Adlm-NE","ff-Adlm-NG","ff-Adlm-SL","ff-Adlm-SN","ff-Adlm","ff-Latn-BF","ff-Latn-CM","ff-Latn-GH","ff-Latn-GM","ff-Latn-GN","ff-Latn-GW","ff-Latn-LR","ff-Latn-MR","ff-Latn-NE","ff-Latn-NG","ff-Latn-SL","ff-Latn","ff","fi","fil","fo-DK","fo","fr-BE","fr-BF","fr-BI","fr-BJ","fr-BL","fr-CA","fr-CD","fr-CF","fr-CG","fr-CH","fr-CI","fr-CM","fr-DJ","fr-DZ","fr-GA","fr-GF","fr-GN","fr-GP","fr-GQ","fr-HT","fr-KM","fr-LU","fr-MA","fr-MC","fr-MF","fr-MG","fr-ML","fr-MQ","fr-MR","fr-MU","fr-NC","fr-NE","fr-PF","fr-PM","fr-RE","fr-RW","fr-SC","fr-SN","fr-SY","fr-TD","fr-TG","fr-TN","fr-VU","fr-WF","fr-YT","fr","fur","fy","ga-GB","ga","gd","gl","gsw-FR","gsw-LI","gsw","gu","guz","gv","ha-GH","ha-NE","ha","haw","he","hi","hr-BA","hr","hsb","hu","hy","ia","id","ig","ii","is","it-CH","it-SM","it-VA","it","ja","jgo","jmc","jv","ka","kab","kam","kde","kea","kgp","khq","ki","kk","kkj","kl","kln","km","kn","ko-KP","ko","kok","ks-Arab","ks","ksb","ksf","ksh","ku","kw","ky","lag","lb","lg","lkt","ln-AO","ln-CF","ln-CG","ln","lo","lrc-IQ","lrc","lt","lu","luo","luy","lv","mai","mas-TZ","mas","mer","mfe","mg","mgh","mgo","mi","mk","ml","mn","mni-Beng","mni","mr","ms-BN","ms-ID","ms-SG","ms","mt","mua","my","mzn","naq","nb-SJ","nb","nd","nds-NL","nds","ne-IN","ne","nl-AW","nl-BE","nl-BQ","nl-CW","nl-SR","nl-SX","nl","nmg","nn","nnh","no","nus","nyn","om-KE","om","or","os-RU","os","pa-Arab","pa-Guru","pa","pcm","pl","ps-PK","ps","pt-AO","pt-CH","pt-CV","pt-GQ","pt-GW","pt-LU","pt-MO","pt-MZ","pt-PT","pt-ST","pt-TL","pt","qu-BO","qu-EC","qu","rm","rn","ro-MD","ro","rof","ru-BY","ru-KG","ru-KZ","ru-MD","ru-UA","ru","rw","rwk","sa","sah","saq","sat-Olck","sat","sbp","sc","sd-Arab","sd-Deva","sd","se-FI","se-SE","se","seh","ses","sg","shi-Latn","shi-Tfng","shi","si","sk","sl","smn","sn","so-DJ","so-ET","so-KE","so","sq-MK","sq-XK","sq","sr-Cyrl-BA","sr-Cyrl-ME","sr-Cyrl-XK","sr-Cyrl","sr-Latn-BA","sr-Latn-ME","sr-Latn-XK","sr-Latn","sr","su-Latn","su","sv-AX","sv-FI","sv","sw-CD","sw-KE","sw-UG","sw","ta-LK","ta-MY","ta-SG","ta","te","teo-KE","teo","tg","th","ti-ER","ti","tk","to","tr-CY","tr","tt","twq","tzm","ug","uk","und","ur-IN","ur","uz-Arab","uz-Cyrl","uz-Latn","uz","vai-Latn","vai-Vaii","vai","vi","vun","wae","wo","xh","xog","yav","yi","yo-BJ","yo","yrl-CO","yrl-VE","yrl","yue-Hans","yue-Hant","yue","zgh","zh-Hans-HK","zh-Hans-MO","zh-Hans-SG","zh-Hans","zh-Hant-HK","zh-Hant-MO","zh-Hant","zh","zu"];var Me=["af-NA","af","agq","ak","am","ar-AE","ar-BH","ar-DJ","ar-DZ","ar-EG","ar-EH","ar-ER","ar-IL","ar-IQ","ar-JO","ar-KM","ar-KW","ar-LB","ar-LY","ar-MA","ar-MR","ar-OM","ar-PS","ar-QA","ar-SA","ar-SD","ar-SO","ar-SS","ar-SY","ar-TD","ar-TN","ar-YE","ar","as","asa","ast","az-Cyrl","az-Latn","az","bas","be-tarask","be","bem","bez","bg","bm","bn-IN","bn","bo-IN","bo","br","brx","bs-Cyrl","bs-Latn","bs","ca-AD","ca-ES-valencia","ca-FR","ca-IT","ca","ccp-IN","ccp","ce","ceb","cgg","chr","ckb-IR","ckb","cs","cy","da-GL","da","dav","de-AT","de-BE","de-CH","de-IT","de-LI","de-LU","de","dje","doi","dsb","dua","dyo","dz","ebu","ee-TG","ee","el-CY","el","en-001","en-150","en-AE","en-AG","en-AI","en-AS","en-AT","en-AU","en-BB","en-BE","en-BI","en-BM","en-BS","en-BW","en-BZ","en-CA","en-CC","en-CH","en-CK","en-CM","en-CX","en-CY","en-DE","en-DG","en-DK","en-DM","en-ER","en-FI","en-FJ","en-FK","en-FM","en-GB","en-GD","en-GG","en-GH","en-GI","en-GM","en-GU","en-GY","en-HK","en-IE","en-IL","en-IM","en-IN","en-IO","en-JE","en-JM","en-KE","en-KI","en-KN","en-KY","en-LC","en-LR","en-LS","en-MG","en-MH","en-MO","en-MP","en-MS","en-MT","en-MU","en-MW","en-MY","en-NA","en-NF","en-NG","en-NL","en-NR","en-NU","en-NZ","en-PG","en-PH","en-PK","en-PN","en-PR","en-PW","en-RW","en-SB","en-SC","en-SD","en-SE","en-SG","en-SH","en-SI","en-SL","en-SS","en-SX","en-SZ","en-TC","en-TK","en-TO","en-TT","en-TV","en-TZ","en-UG","en-UM","en-VC","en-VG","en-VI","en-VU","en-WS","en-ZA","en-ZM","en-ZW","en","eo","es-419","es-AR","es-BO","es-BR","es-BZ","es-CL","es-CO","es-CR","es-CU","es-DO","es-EA","es-EC","es-GQ","es-GT","es-HN","es-IC","es-MX","es-NI","es-PA","es-PE","es-PH","es-PR","es-PY","es-SV","es-US","es-UY","es-VE","es","et","eu","ewo","fa-AF","fa","ff-Adlm-BF","ff-Adlm-CM","ff-Adlm-GH","ff-Adlm-GM","ff-Adlm-GW","ff-Adlm-LR","ff-Adlm-MR","ff-Adlm-NE","ff-Adlm-NG","ff-Adlm-SL","ff-Adlm-SN","ff-Adlm","ff-Latn-BF","ff-Latn-CM","ff-Latn-GH","ff-Latn-GM","ff-Latn-GN","ff-Latn-GW","ff-Latn-LR","ff-Latn-MR","ff-Latn-NE","ff-Latn-NG","ff-Latn-SL","ff-Latn","ff","fi","fil","fo-DK","fo","fr-BE","fr-BF","fr-BI","fr-BJ","fr-BL","fr-CA","fr-CD","fr-CF","fr-CG","fr-CH","fr-CI","fr-CM","fr-DJ","fr-DZ","fr-GA","fr-GF","fr-GN","fr-GP","fr-GQ","fr-HT","fr-KM","fr-LU","fr-MA","fr-MC","fr-MF","fr-MG","fr-ML","fr-MQ","fr-MR","fr-MU","fr-NC","fr-NE","fr-PF","fr-PM","fr-RE","fr-RW","fr-SC","fr-SN","fr-SY","fr-TD","fr-TG","fr-TN","fr-VU","fr-WF","fr-YT","fr","fur","fy","ga-GB","ga","gd","gl","gsw-FR","gsw-LI","gsw","gu","guz","gv","ha-GH","ha-NE","ha","haw","he","hi","hr-BA","hr","hsb","hu","hy","ia","id","ig","ii","is","it-CH","it-SM","it-VA","it","ja","jgo","jmc","jv","ka","kab","kam","kde","kea","kgp","khq","ki","kk","kkj","kl","kln","km","kn","ko-KP","ko","kok","ks-Arab","ks","ksb","ksf","ksh","ku","kw","ky","lag","lb","lg","lkt","ln-AO","ln-CF","ln-CG","ln","lo","lrc-IQ","lrc","lt","lu","luo","luy","lv","mai","mas-TZ","mas","mer","mfe","mg","mgh","mgo","mi","mk","ml","mn","mni-Beng","mni","mr","ms-BN","ms-ID","ms-SG","ms","mt","mua","my","mzn","naq","nb-SJ","nb","nd","nds-NL","nds","ne-IN","ne","nl-AW","nl-BE","nl-BQ","nl-CW","nl-SR","nl-SX","nl","nmg","nn","nnh","no","nus","nyn","om-KE","om","or","os-RU","os","pa-Arab","pa-Guru","pa","pcm","pl","ps-PK","ps","pt-AO","pt-CH","pt-CV","pt-GQ","pt-GW","pt-LU","pt-MO","pt-MZ","pt-PT","pt-ST","pt-TL","pt","qu-BO","qu-EC","qu","rm","rn","ro-MD","ro","rof","ru-BY","ru-KG","ru-KZ","ru-MD","ru-UA","ru","rw","rwk","sa","sah","saq","sat-Olck","sat","sbp","sc","sd-Arab","sd-Deva","sd","se-FI","se-SE","se","seh","ses","sg","shi-Latn","shi-Tfng","shi","si","sk","sl","smn","sn","so-DJ","so-ET","so-KE","so","sq-MK","sq-XK","sq","sr-Cyrl-BA","sr-Cyrl-ME","sr-Cyrl-XK","sr-Cyrl","sr-Latn-BA","sr-Latn-ME","sr-Latn-XK","sr-Latn","sr","su-Latn","su","sv-AX","sv-FI","sv","sw-CD","sw-KE","sw-UG","sw","ta-LK","ta-MY","ta-SG","ta","te","teo-KE","teo","tg","th","ti-ER","ti","tk","to","tr-CY","tr","tt","twq","tzm","ug","uk","und","ur-IN","ur","uz-Arab","uz-Cyrl","uz-Latn","uz","vai-Latn","vai-Vaii","vai","vi","vun","wae","wo","xh","xog","yav","yi","yo-BJ","yo","yrl-CO","yrl-VE","yrl","yue-Hans","yue-Hant","yue","zgh","zh-Hans-HK","zh-Hans-MO","zh-Hans-SG","zh-Hans","zh-Hant-HK","zh-Hant-MO","zh-Hant","zh","zu"];let Ne,je;!function(t){t.language="language",t.system="system",t.comma_decimal="comma_decimal",t.decimal_comma="decimal_comma",t.space_comma="space_comma",t.none="none"}(Ne||(Ne={})),function(t){t.language="language",t.system="system",t.am_pm="12",t.twenty_four="24"}(je||(je={}));const Fe={},Pe=window.localStorage||{},Be={"zh-cn":"zh-Hans","zh-sg":"zh-Hans","zh-my":"zh-Hans","zh-tw":"zh-Hant","zh-hk":"zh-Hant","zh-mo":"zh-Hant",zh:"zh-Hant"};function He(t){if(t in Fe.translations)return t;const e=t.toLowerCase();if(e in Be)return Be[e];const a=Object.keys(Fe.translations).find((t=>t.toLowerCase()===e));return a||(t.includes("-")?He(t.split("-")[0]):void 0)}const Ge=new Set,Ke=[];"Locale"in Intl&&!function(){try{return"x-private"===new Intl.Locale("und-x-private").toString()}catch(t){return!0}}()||Ke.push(import("./c.32330aef.js")),function(t){if(void 0===t&&(t="en"),!("PluralRules"in Intl)||"one"===new Intl.PluralRules("en",{minimumFractionDigits:2}).select(1)||!function(t){if(!t)return!0;var e=Array.isArray(t)?t:[t];return Intl.PluralRules.supportedLocalesOf(e).length===e.length}(t))return t?_e([t],xe,"en"):void 0}()&&(Ke.push(import("./c.009ab152.js")),Ke.push(import("./c.eb0d3bd2.js"))),function(t){if(void 0===t&&(t="en"),!("RelativeTimeFormat"in Intl)||!function(t){if(!t)return!0;var e=Array.isArray(t)?t:[t];return Intl.RelativeTimeFormat.supportedLocalesOf(e).length===e.length}(t)||!function(t){try{return"numberingSystem"in new Intl.RelativeTimeFormat(t||"en",{numeric:"auto"}).resolvedOptions()}catch(t){return!1}}(t))return De([t],ze,"en")}()&&Ke.push(import("./c.7110fca6.js")),function(t){if(void 0===t&&(t="en"),!("DateTimeFormat"in Intl)||!("formatToParts"in Intl.DateTimeFormat.prototype)||!("formatRange"in Intl.DateTimeFormat.prototype)||function(){try{return"dayPeriod"!==new Intl.DateTimeFormat("en",{hourCycle:"h11",hour:"numeric"}).formatToParts(0)[2].type}catch(t){return!1}}()||function(){try{return!!new Intl.DateTimeFormat("en",{dateStyle:"short",hour:"numeric"}).format(new Date(0))}catch(t){return!1}}()||!function(){try{return!!new Intl.DateTimeFormat(void 0,{dateStyle:"short"}).resolvedOptions().dateStyle}catch(t){return!1}}()||!function(t){if(!t)return!0;var e=Array.isArray(t)?t:[t];return Intl.DateTimeFormat.supportedLocalesOf(e).length===e.length}(t))return t?De([t],Me,"en"):void 0}()&&(Ke.push(import("./c.c27867f6.js")),Ke.push(import("./c.bf2e9998.js")));const Ue=0===Ke.length?void 0:Promise.all(Ke).then((()=>We(function(){let t=null;if(Pe.selectedLanguage)try{const e=JSON.parse(Pe.selectedLanguage);if(e&&(t=He(e),t))return t}catch(t){}if(navigator.languages)for(const e of navigator.languages)if(t=He(e),t)return t;return t=He(navigator.language),t||"en"}()))),We=async t=>{if(!Ge.has(t)){Ge.add(t);try{if(Intl.NumberFormat&&"function"==typeof Intl.NumberFormat.__addLocaleData){const e=await fetch(`/static/locale-data/intl-numberformat/${t}.json`);Intl.NumberFormat.__addLocaleData(await e.json())}if(Intl.RelativeTimeFormat&&"function"==typeof Intl.RelativeTimeFormat.__addLocaleData){const e=await fetch(`/static/locale-data/intl-relativetimeformat/${t}.json`);Intl.RelativeTimeFormat.__addLocaleData(await e.json())}if(Intl.DateTimeFormat&&"function"==typeof Intl.DateTimeFormat.__addLocaleData){const e=await fetch(`/static/locale-data/intl-datetimeformat/${t}.json`);Intl.DateTimeFormat.__addLocaleData(await e.json())}}catch(t){}}};Ue&&await Ue;const Ve=(t,e)=>Ye(e).format(t),Ye=S((t=>new Intl.DateTimeFormat(t.language,{weekday:"long",month:"long",day:"numeric"}))),Xe=(t,e)=>qe(e).format(t),qe=S((t=>new Intl.DateTimeFormat(t.language,{year:"numeric",month:"long",day:"numeric"})));S((t=>new Intl.DateTimeFormat(t.language,{year:"numeric",month:"numeric",day:"numeric"})));const Ze=(t,e)=>Qe(e).format(t),Qe=S((t=>new Intl.DateTimeFormat(t.language,{day:"numeric",month:"short"}))),Je=(t,e)=>ta(e).format(t),ta=S((t=>new Intl.DateTimeFormat(t.language,{month:"long",year:"numeric"}))),ea=(t,e)=>aa(e).format(t),aa=S((t=>new Intl.DateTimeFormat(t.language,{month:"long"}))),ia=(t,e)=>na(e).format(t),na=S((t=>new Intl.DateTimeFormat(t.language,{year:"numeric"}))),oa=S((t=>{if(t.time_format===je.language||t.time_format===je.system){const e=t.time_format===je.language?t.language:void 0,a=(new Date).toLocaleString(e);return a.includes("AM")||a.includes("PM")}return t.time_format===je.am_pm}));Ue&&await Ue;const ra=(t,e)=>sa(e).format(t),sa=S((t=>new Intl.DateTimeFormat("en"!==t.language||oa(t)?t.language:"en-u-hc-h23",{year:"numeric",month:"long",day:"numeric",hour:oa(t)?"numeric":"2-digit",minute:"2-digit",hour12:oa(t)}))),la=(t,e)=>ca(e).format(t),ca=S((t=>new Intl.DateTimeFormat("en"!==t.language||oa(t)?t.language:"en-u-hc-h23",{year:"numeric",month:"long",day:"numeric",hour:oa(t)?"numeric":"2-digit",minute:"2-digit",second:"2-digit",hour12:oa(t)})));S((t=>new Intl.DateTimeFormat("en"!==t.language||oa(t)?t.language:"en-u-hc-h23",{year:"numeric",month:"numeric",day:"numeric",hour:"numeric",minute:"2-digit",hour12:oa(t)})));const da=t=>{switch(t.number_format){case Ne.comma_decimal:return["en-US","en"];case Ne.decimal_comma:return["de","es","it"];case Ne.space_comma:return["fr","sv","cs"];case Ne.system:return;default:return t.language}},ha=(t,e,a)=>{const i=e?da(e):void 0;if(Number.isNaN=Number.isNaN||function t(e){return"number"==typeof e&&t(e)},(null==e?void 0:e.number_format)!==Ne.none&&!Number.isNaN(Number(t))&&Intl)try{return new Intl.NumberFormat(i,pa(t,a)).format(Number(t))}catch(e){return console.error(e),new Intl.NumberFormat(void 0,pa(t,a)).format(Number(t))}return"string"==typeof t?t:`${((t,e=2)=>Math.round(t*10**e)/10**e)(t,null==a?void 0:a.maximumFractionDigits).toString()}${"currency"===(null==a?void 0:a.style)?` ${a.currency}`:""}`},pa=(t,e)=>{const a={maximumFractionDigits:2,...e};if("string"!=typeof t)return a;if(!e||!e.minimumFractionDigits&&!e.maximumFractionDigits){const e=t.indexOf(".")>-1?t.split(".")[1].length:0;a.minimumFractionDigits=e,a.maximumFractionDigits=e}return a},ua=t=>t.charAt(0).toUpperCase()+t.slice(1),ma="^\\d{4}-(0[1-9]|1[0-2])-([12]\\d|0[1-9]|3[01])",fa=new RegExp(ma+"$"),ga=new RegExp(ma),ba=/^\d{4}-(0[1-9]|1[0-2])-([12]\d|0[1-9]|3[01])[T| ](((([01]\d|2[0-3])((:?)[0-5]\d)?|24:?00)([.,]\d+(?!:))?)(\8[0-5]\d([.,]\d+)?)?([zZ]|([+-])([01]\d|2[0-3]):?([0-5]\d)?)?)$/;let va;const ya=["assumed_state","attribution","custom_ui_more_info","custom_ui_state_card","device_class","editable","emulated_hue_name","emulated_hue","entity_picture","friendly_name","haaska_hidden","haaska_name","icon","initial_state","last_reset","restored","state_class","supported_features","unit_of_measurement"];function _a(t,e){if(null===e)return"—";if(Array.isArray(e)&&e.some((t=>t instanceof Object))||!Array.isArray(e)&&e instanceof Object){va||(va=import("./c.bfc7ca93.js"));const t=va.then((t=>t.dump(e)));return p`<pre>${ue(t,"")}</pre>`}if("number"==typeof e)return ha(e,t.locale);if("string"==typeof e){if(e.startsWith("http"))try{const t=new URL(e);if("http:"===t.protocol||"https:"===t.protocol)return p`<a target="_blank" rel="noreferrer" href=${e}
            >${e}</a
          >`}catch(t){}if(((t,e=!1)=>e?ga.test(t):fa.test(t))(e,!0)){if(a=e,ba.test(a)){const a=new Date(e);if(me(a))return la(a,t.locale)}const i=new Date(e);if(me(i))return Xe(i,t.locale)}}var a;return Array.isArray(e)?e.join(", "):e}T([g("ha-expansion-panel")],(function(t,e){return{F:class extends e{constructor(...e){super(...e),t(this)}},d:[{kind:"field",decorators:[d({type:Boolean,reflect:!0})],key:"expanded",value:()=>!1},{kind:"field",decorators:[d({type:Boolean,reflect:!0})],key:"outlined",value:()=>!1},{kind:"field",decorators:[d()],key:"header",value:void 0},{kind:"field",decorators:[d()],key:"secondary",value:void 0},{kind:"field",decorators:[b()],key:"_showContent",value(){return this.expanded}},{kind:"field",decorators:[c(".container")],key:"_container",value:void 0},{kind:"method",key:"render",value:function(){return p`
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
          .path=${E}
          class="summary-icon ${u({expanded:this.expanded})}"
        ></ha-svg-icon>
      </div>
      <div
        class="container ${u({expanded:this.expanded})}"
        @transitionend=${this._handleTransitionEnd}
        role="region"
        aria-labelledby="summary"
        aria-hidden=${!this.expanded}
        tabindex="-1"
      >
        ${this._showContent?p`<slot></slot>`:""}
      </div>
    `}},{kind:"method",key:"willUpdate",value:function(t){t.has("expanded")&&this.expanded&&(this._showContent=this.expanded)}},{kind:"method",key:"_handleTransitionEnd",value:function(){this._container.style.removeProperty("height"),this._showContent=this.expanded}},{kind:"method",key:"_toggleContainer",value:async function(t){if("keydown"===t.type&&"Enter"!==t.key&&" "!==t.key)return;t.preventDefault();const e=!this.expanded;n(this,"expanded-will-change",{expanded:e}),e&&(this._showContent=!0,await A());const a=this._container.scrollHeight;this._container.style.height=`${a}px`,e||setTimeout((()=>{this._container.style.height="0px"}),0),this.expanded=e,n(this,"expanded-changed",{expanded:this.expanded})}},{kind:"get",static:!0,key:"styles",value:function(){return f`
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
    `}}]}}),I),T([g("ha-attributes")],(function(t,e){return{F:class extends e{constructor(...e){super(...e),t(this)}},d:[{kind:"field",decorators:[d({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[d()],key:"stateObj",value:void 0},{kind:"field",decorators:[d({attribute:"extra-filters"})],key:"extraFilters",value:void 0},{kind:"field",decorators:[b()],key:"_expanded",value:()=>!1},{kind:"method",key:"render",value:function(){if(!this.stateObj)return p``;const t=this.computeDisplayAttributes(ya.concat(this.extraFilters?this.extraFilters.split(","):[]));return 0===t.length?p``:p`
      <ha-expansion-panel
        .header=${this.hass.localize("ui.components.attributes.expansion_header")}
        outlined
        @expanded-will-change=${this.expandedChanged}
      >
        <div class="attribute-container">
          ${this._expanded?p`
                ${t.map((t=>{return p`
                    <div class="data-entry">
                      <div class="key">${e=t,e=e.replace(/_/g," ").replace(/\bid\b/g,"ID").replace(/\bip\b/g,"IP").replace(/\bmac\b/g,"MAC").replace(/\bgps\b/g,"GPS"),ua(e)}</div>
                      <div class="value">
                        ${this.formatAttribute(t)}
                      </div>
                    </div>
                  `;var e}))}
              `:""}
        </div>
      </ha-expansion-panel>
      ${this.stateObj.attributes.attribution?p`
            <div class="attribution">
              ${this.stateObj.attributes.attribution}
            </div>
          `:""}
    `}},{kind:"get",static:!0,key:"styles",value:function(){return[$,f`
        .attribute-container {
          margin-bottom: 8px;
        }
        .data-entry {
          display: flex;
          flex-direction: row;
          justify-content: space-between;
        }
        .data-entry .value {
          max-width: 60%;
          overflow-wrap: break-word;
          text-align: right;
        }
        .key {
          flex-grow: 1;
        }
        .attribution {
          color: var(--secondary-text-color);
          text-align: center;
          margin-top: 16px;
        }
        pre {
          font-family: inherit;
          font-size: inherit;
          margin: 0px;
          overflow-wrap: break-word;
          white-space: pre-line;
        }
        hr {
          border-color: var(--divider-color);
          border-bottom: none;
          margin: 16px 0;
        }
      `]}},{kind:"method",key:"computeDisplayAttributes",value:function(t){return this.stateObj?Object.keys(this.stateObj.attributes).filter((e=>-1===t.indexOf(e))):[]}},{kind:"method",key:"formatAttribute",value:function(t){if(!this.stateObj)return"—";const e=this.stateObj.attributes[t];return _a(this.hass,e)}},{kind:"method",key:"expandedChanged",value:function(t){this._expanded=t.detail.expanded}}]}}),I);var ka=function(){return ka=Object.assign||function(t){for(var e,a=1,i=arguments.length;a<i;a++)for(var n in e=arguments[a])Object.prototype.hasOwnProperty.call(e,n)&&(t[n]=e[n]);return t},ka.apply(this,arguments)};var xa={second:45,minute:45,hour:22,day:5};Ue&&await Ue;const wa=S((t=>new Intl.RelativeTimeFormat(t.language,{numeric:"auto"}))),Ca=(t,e,a,i=!0)=>{const n=function(t,e,a){void 0===e&&(e=Date.now()),void 0===a&&(a={});var i=ka(ka({},xa),a||{}),n=(+t-+e)/1e3;if(Math.abs(n)<i.second)return{value:Math.round(n),unit:"second"};var o=n/60;if(Math.abs(o)<i.minute)return{value:Math.round(o),unit:"minute"};var r=n/3600;if(Math.abs(r)<i.hour)return{value:Math.round(r),unit:"hour"};var s=n/86400;if(Math.abs(s)<i.day)return{value:Math.round(s),unit:"day"};var l=new Date(t),c=new Date(e),d=l.getFullYear()-c.getFullYear();if(Math.round(Math.abs(d))>0)return{value:Math.round(d),unit:"year"};var h=12*d+l.getMonth()-c.getMonth();if(Math.round(Math.abs(h))>0)return{value:Math.round(h),unit:"month"};var p=n/604800;return{value:Math.round(p),unit:"week"}}(t,a);return i?wa(e).format(n.value,n.unit):Intl.NumberFormat(e.language,{style:"unit",unit:n.unit,unitDisplay:"long"}).format(Math.abs(n.value))};T([g("ha-relative-time")],(function(t,e){class a extends e{constructor(...e){super(...e),t(this)}}return{F:a,d:[{kind:"field",decorators:[d({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[d({attribute:!1})],key:"datetime",value:void 0},{kind:"field",decorators:[d({type:Boolean})],key:"capitalize",value:()=>!1},{kind:"field",key:"_interval",value:void 0},{kind:"method",key:"disconnectedCallback",value:function(){R(O(a.prototype),"disconnectedCallback",this).call(this),this._clearInterval()}},{kind:"method",key:"connectedCallback",value:function(){R(O(a.prototype),"connectedCallback",this).call(this),this.datetime&&this._startInterval()}},{kind:"method",key:"createRenderRoot",value:function(){return this}},{kind:"method",key:"firstUpdated",value:function(t){R(O(a.prototype),"firstUpdated",this).call(this,t),this._updateRelative()}},{kind:"method",key:"update",value:function(t){R(O(a.prototype),"update",this).call(this,t),this._updateRelative()}},{kind:"method",key:"_clearInterval",value:function(){this._interval&&(window.clearInterval(this._interval),this._interval=void 0)}},{kind:"method",key:"_startInterval",value:function(){this._clearInterval(),this._interval=window.setInterval((()=>this._updateRelative()),6e4)}},{kind:"method",key:"_updateRelative",value:function(){if(this.datetime){const t=Ca(new Date(this.datetime),this.hass.locale);this.innerHTML=this.capitalize?ua(t):t}else this.innerHTML=this.hass.localize("ui.components.relative_time.never")}}]}}),L),T([g("react-workflow-more-info")],(function(t,e){return{F:class extends e{constructor(...e){super(...e),t(this)}},d:[{kind:"field",decorators:[d({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[d()],key:"stateObj",value:void 0},{kind:"method",key:"render",value:function(){return this.hass&&this.stateObj?p`
        <hr />
        <div class="flex">
            <div>${this.hass.localize("ui.card.automation.last_triggered")}:</div>
            <ha-relative-time
                .hass=${this.hass}
                .datetime=${this.stateObj.attributes.last_triggered}
                capitalize
            ></ha-relative-time>
        </div>
        <div class="actions">
            <mwc-button
                @click=${this._runActions}
                .disabled=${Q.includes(this.stateObj.state)}
            >
                ${this.hass.localize("ui.card.automation.trigger")}
            </mwc-button>
        </div>
        `:p``}},{kind:"method",key:"_runActions",value:function(){yt(this.hass,this.stateObj.entity_id)}},{kind:"get",static:!0,key:"styles",value:function(){return f`
            .flex {
                display: flex;
                justify-content: space-between;
            }
            .attributes {
                margin: 8px 0;
                
            }
            .actions {
                margin: 8px 0;
                display: flex;
                flex-wrap: wrap;
                justify-content: center;
            }
            hr {
                border-color: var(--divider-color);
                border-bottom: none;
                margin: 16px 0;
            }
        `}}]}}),I);const Sa=D`
/* Most common used flex styles*/
<dom-module id="iron-flex">
  <template>
    <style>
      .layout.horizontal,
      .layout.vertical {
        display: -ms-flexbox;
        display: -webkit-flex;
        display: flex;
      }

      .layout.inline {
        display: -ms-inline-flexbox;
        display: -webkit-inline-flex;
        display: inline-flex;
      }

      .layout.horizontal {
        -ms-flex-direction: row;
        -webkit-flex-direction: row;
        flex-direction: row;
      }

      .layout.vertical {
        -ms-flex-direction: column;
        -webkit-flex-direction: column;
        flex-direction: column;
      }

      .layout.wrap {
        -ms-flex-wrap: wrap;
        -webkit-flex-wrap: wrap;
        flex-wrap: wrap;
      }

      .layout.no-wrap {
        -ms-flex-wrap: nowrap;
        -webkit-flex-wrap: nowrap;
        flex-wrap: nowrap;
      }

      .layout.center,
      .layout.center-center {
        -ms-flex-align: center;
        -webkit-align-items: center;
        align-items: center;
      }

      .layout.center-justified,
      .layout.center-center {
        -ms-flex-pack: center;
        -webkit-justify-content: center;
        justify-content: center;
      }

      .flex {
        -ms-flex: 1 1 0.000000001px;
        -webkit-flex: 1;
        flex: 1;
        -webkit-flex-basis: 0.000000001px;
        flex-basis: 0.000000001px;
      }

      .flex-auto {
        -ms-flex: 1 1 auto;
        -webkit-flex: 1 1 auto;
        flex: 1 1 auto;
      }

      .flex-none {
        -ms-flex: none;
        -webkit-flex: none;
        flex: none;
      }
    </style>
  </template>
</dom-module>
/* Basic flexbox reverse styles */
<dom-module id="iron-flex-reverse">
  <template>
    <style>
      .layout.horizontal-reverse,
      .layout.vertical-reverse {
        display: -ms-flexbox;
        display: -webkit-flex;
        display: flex;
      }

      .layout.horizontal-reverse {
        -ms-flex-direction: row-reverse;
        -webkit-flex-direction: row-reverse;
        flex-direction: row-reverse;
      }

      .layout.vertical-reverse {
        -ms-flex-direction: column-reverse;
        -webkit-flex-direction: column-reverse;
        flex-direction: column-reverse;
      }

      .layout.wrap-reverse {
        -ms-flex-wrap: wrap-reverse;
        -webkit-flex-wrap: wrap-reverse;
        flex-wrap: wrap-reverse;
      }
    </style>
  </template>
</dom-module>
/* Flexbox alignment */
<dom-module id="iron-flex-alignment">
  <template>
    <style>
      /**
       * Alignment in cross axis.
       */
      .layout.start {
        -ms-flex-align: start;
        -webkit-align-items: flex-start;
        align-items: flex-start;
      }

      .layout.center,
      .layout.center-center {
        -ms-flex-align: center;
        -webkit-align-items: center;
        align-items: center;
      }

      .layout.end {
        -ms-flex-align: end;
        -webkit-align-items: flex-end;
        align-items: flex-end;
      }

      .layout.baseline {
        -ms-flex-align: baseline;
        -webkit-align-items: baseline;
        align-items: baseline;
      }

      /**
       * Alignment in main axis.
       */
      .layout.start-justified {
        -ms-flex-pack: start;
        -webkit-justify-content: flex-start;
        justify-content: flex-start;
      }

      .layout.center-justified,
      .layout.center-center {
        -ms-flex-pack: center;
        -webkit-justify-content: center;
        justify-content: center;
      }

      .layout.end-justified {
        -ms-flex-pack: end;
        -webkit-justify-content: flex-end;
        justify-content: flex-end;
      }

      .layout.around-justified {
        -ms-flex-pack: distribute;
        -webkit-justify-content: space-around;
        justify-content: space-around;
      }

      .layout.justified {
        -ms-flex-pack: justify;
        -webkit-justify-content: space-between;
        justify-content: space-between;
      }

      /**
       * Self alignment.
       */
      .self-start {
        -ms-align-self: flex-start;
        -webkit-align-self: flex-start;
        align-self: flex-start;
      }

      .self-center {
        -ms-align-self: center;
        -webkit-align-self: center;
        align-self: center;
      }

      .self-end {
        -ms-align-self: flex-end;
        -webkit-align-self: flex-end;
        align-self: flex-end;
      }

      .self-stretch {
        -ms-align-self: stretch;
        -webkit-align-self: stretch;
        align-self: stretch;
      }

      .self-baseline {
        -ms-align-self: baseline;
        -webkit-align-self: baseline;
        align-self: baseline;
      }

      /**
       * multi-line alignment in main axis.
       */
      .layout.start-aligned {
        -ms-flex-line-pack: start;  /* IE10 */
        -ms-align-content: flex-start;
        -webkit-align-content: flex-start;
        align-content: flex-start;
      }

      .layout.end-aligned {
        -ms-flex-line-pack: end;  /* IE10 */
        -ms-align-content: flex-end;
        -webkit-align-content: flex-end;
        align-content: flex-end;
      }

      .layout.center-aligned {
        -ms-flex-line-pack: center;  /* IE10 */
        -ms-align-content: center;
        -webkit-align-content: center;
        align-content: center;
      }

      .layout.between-aligned {
        -ms-flex-line-pack: justify;  /* IE10 */
        -ms-align-content: space-between;
        -webkit-align-content: space-between;
        align-content: space-between;
      }

      .layout.around-aligned {
        -ms-flex-line-pack: distribute;  /* IE10 */
        -ms-align-content: space-around;
        -webkit-align-content: space-around;
        align-content: space-around;
      }
    </style>
  </template>
</dom-module>
/* Non-flexbox positioning helper styles */
<dom-module id="iron-flex-factors">
  <template>
    <style>
      .flex,
      .flex-1 {
        -ms-flex: 1 1 0.000000001px;
        -webkit-flex: 1;
        flex: 1;
        -webkit-flex-basis: 0.000000001px;
        flex-basis: 0.000000001px;
      }

      .flex-2 {
        -ms-flex: 2;
        -webkit-flex: 2;
        flex: 2;
      }

      .flex-3 {
        -ms-flex: 3;
        -webkit-flex: 3;
        flex: 3;
      }

      .flex-4 {
        -ms-flex: 4;
        -webkit-flex: 4;
        flex: 4;
      }

      .flex-5 {
        -ms-flex: 5;
        -webkit-flex: 5;
        flex: 5;
      }

      .flex-6 {
        -ms-flex: 6;
        -webkit-flex: 6;
        flex: 6;
      }

      .flex-7 {
        -ms-flex: 7;
        -webkit-flex: 7;
        flex: 7;
      }

      .flex-8 {
        -ms-flex: 8;
        -webkit-flex: 8;
        flex: 8;
      }

      .flex-9 {
        -ms-flex: 9;
        -webkit-flex: 9;
        flex: 9;
      }

      .flex-10 {
        -ms-flex: 10;
        -webkit-flex: 10;
        flex: 10;
      }

      .flex-11 {
        -ms-flex: 11;
        -webkit-flex: 11;
        flex: 11;
      }

      .flex-12 {
        -ms-flex: 12;
        -webkit-flex: 12;
        flex: 12;
      }
    </style>
  </template>
</dom-module>
<dom-module id="iron-positioning">
  <template>
    <style>
      .block {
        display: block;
      }

      [hidden] {
        display: none !important;
      }

      .invisible {
        visibility: hidden !important;
      }

      .relative {
        position: relative;
      }

      .fit {
        position: absolute;
        top: 0;
        right: 0;
        bottom: 0;
        left: 0;
      }

      body.fullbleed {
        margin: 0;
        height: 100vh;
      }

      .scroll {
        -webkit-overflow-scrolling: touch;
        overflow: auto;
      }

      /* fixed position */
      .fixed-bottom,
      .fixed-left,
      .fixed-right,
      .fixed-top {
        position: fixed;
      }

      .fixed-top {
        top: 0;
        left: 0;
        right: 0;
      }

      .fixed-right {
        top: 0;
        right: 0;
        bottom: 0;
      }

      .fixed-bottom {
        right: 0;
        bottom: 0;
        left: 0;
      }

      .fixed-left {
        top: 0;
        bottom: 0;
        left: 0;
      }
    </style>
  </template>
</dom-module>
`;Sa.setAttribute("style","display: none;"),document.head.appendChild(Sa.content),T([g("state-info")],(function(t,e){class a extends e{constructor(...e){super(...e),t(this)}}return{F:a,d:[{kind:"field",decorators:[d({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[d({attribute:!1})],key:"stateObj",value:void 0},{kind:"field",decorators:[d({type:Boolean})],key:"inDialog",value:()=>!1},{kind:"field",decorators:[d({type:Boolean,reflect:!0})],key:"rtl",value:()=>!1},{kind:"method",key:"render",value:function(){if(!this.hass||!this.stateObj)return p``;const t=J(this.stateObj);return p`<state-badge
        .stateObj=${this.stateObj}
        .stateColor=${!0}
      ></state-badge>
      <div class="info">
        <div class="name" .title=${t} .inDialog=${this.inDialog}>
          ${t}
        </div>
        ${this.inDialog?p`<div class="time-ago">
              <ha-relative-time
                id="last_changed"
                .hass=${this.hass}
                .datetime=${this.stateObj.last_changed}
                capitalize
              ></ha-relative-time>
              <paper-tooltip animation-delay="0" for="last_changed">
                <div>
                  <div class="row">
                    <span class="column-name">
                      ${this.hass.localize("ui.dialogs.more_info_control.last_changed")}:
                    </span>
                    <ha-relative-time
                      .hass=${this.hass}
                      .datetime=${this.stateObj.last_changed}
                      capitalize
                    ></ha-relative-time>
                  </div>
                  <div class="row">
                    <span>
                      ${this.hass.localize("ui.dialogs.more_info_control.last_updated")}:
                    </span>
                    <ha-relative-time
                      .hass=${this.hass}
                      .datetime=${this.stateObj.last_updated}
                      capitalize
                    ></ha-relative-time>
                  </div>
                </div>
              </paper-tooltip>
            </div>`:p`<div class="extra-info"><slot></slot></div>`}
      </div>`}},{kind:"method",key:"updated",value:function(t){if(R(O(a.prototype),"updated",this).call(this,t),!t.has("hass"))return;const e=t.get("hass");e&&e.locale===this.hass.locale||(this.rtl=tt(this.hass))}},{kind:"get",static:!0,key:"styles",value:function(){return f`
      :host {
        min-width: 120px;
        white-space: nowrap;
      }

      state-badge {
        float: left;
      }
      :host([rtl]) state-badge {
        float: right;
      }

      .info {
        margin-left: 56px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        height: 100%;
      }

      :host([rtl]) .info {
        margin-right: 56px;
        margin-left: 0;
        text-align: right;
      }

      .name {
        color: var(--primary-text-color);
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
      }

      .name[in-dialog],
      :host([secondary-line]) .name {
        line-height: 20px;
      }

      .time-ago,
      .extra-info,
      .extra-info > * {
        color: var(--secondary-text-color);
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
      }

      .row {
        display: flex;
        flex-direction: row;
        flex-wrap: no-wrap;
        width: 100%;
        justify-content: space-between;
        margin: 0 2px 4px 0;
      }

      .row:last-child {
        margin-bottom: 0px;
      }
    `}}]}}),I);customElements.define("react-state-card-toggle",class extends z{static get template(){return D`
            <style include="iron-flex iron-flex-alignment"></style>
            <style>
                ha-entity-toggle {
                    margin: -4px -16px -4px 0;
                    padding: 4px 16px;
                }
            </style>

            <div class="horizontal justified layout">
                ${this.stateInfoTemplate}
                <ha-entity-toggle
                    state-obj="[[stateObj]]"
                    hass="[[hass]]"
                ></ha-entity-toggle>
            </div>
        `}static get stateInfoTemplate(){return D`
            <state-info
                hass="[[hass]]"
                state-obj="[[stateObj]]"
                in-dialog="[[inDialog]]"
            ></state-info>
        `}static get properties(){return{hass:Object,stateObj:Object,inDialog:{type:Boolean,value:!1}}}});customElements.define("react-state-card-content",class extends z{static get properties(){return{hass:Object,stateObj:Object,inDialog:{type:Boolean,value:!1}}}static get observers(){return["inputChanged(hass, inDialog, stateObj)"]}inputChanged(t,e,a){if(!a||!t)return;!function(t,e,a){const i=t;let n;i.lastChild&&i.lastChild.tagName===e?n=i.lastChild:(i.lastChild&&i.removeChild(i.lastChild),n=document.createElement(e.toLowerCase())),n.setProperties?n.setProperties(a):Object.keys(a).forEach((t=>{n[t]=a[t]})),null===n.parentNode&&i.appendChild(n)}(this,"react-state-card-toggle".toUpperCase(),{hass:t,stateObj:a,inDialog:e})}});function Ta(){var t=new Date,e=t.getFullYear(),a=t.getMonth(),i=t.getDate(),n=new Date(0);return n.setFullYear(e,a,i-1),n.setHours(0,0,0,0),n}T([g("ha-header-bar")],(function(t,e){return{F:class extends e{constructor(...e){super(...e),t(this)}},d:[{kind:"method",key:"render",value:function(){return p`<header class="mdc-top-app-bar">
      <div class="mdc-top-app-bar__row">
        <section
          class="mdc-top-app-bar__section mdc-top-app-bar__section--align-start"
          id="navigation"
        >
          <slot name="navigationIcon"></slot>
          <span class="mdc-top-app-bar__title">
            <slot name="title"></slot>
          </span>
        </section>
        <section
          class="mdc-top-app-bar__section mdc-top-app-bar__section--align-end"
          id="actions"
          role="toolbar"
        >
          <slot name="actionItems"></slot>
        </section>
      </div>
    </header>`}},{kind:"get",static:!0,key:"styles",value:function(){return[M("/**\n * @license\n * Copyright Google LLC All Rights Reserved.\n *\n * Use of this source code is governed by an MIT-style license that can be\n * found in the LICENSE file at https://github.com/material-components/material-components-web/blob/master/LICENSE\n */\n.mdc-top-app-bar{background-color:#6200ee;background-color:var(--mdc-theme-primary, #6200ee);color:white;display:flex;position:fixed;flex-direction:column;justify-content:space-between;box-sizing:border-box;width:100%;z-index:4}.mdc-top-app-bar .mdc-top-app-bar__action-item,.mdc-top-app-bar .mdc-top-app-bar__navigation-icon{color:#fff;color:var(--mdc-theme-on-primary, #fff)}.mdc-top-app-bar .mdc-top-app-bar__action-item::before,.mdc-top-app-bar .mdc-top-app-bar__action-item::after,.mdc-top-app-bar .mdc-top-app-bar__navigation-icon::before,.mdc-top-app-bar .mdc-top-app-bar__navigation-icon::after{background-color:#fff;background-color:var(--mdc-ripple-color, var(--mdc-theme-on-primary, #fff))}.mdc-top-app-bar .mdc-top-app-bar__action-item:hover::before,.mdc-top-app-bar .mdc-top-app-bar__action-item.mdc-ripple-surface--hover::before,.mdc-top-app-bar .mdc-top-app-bar__navigation-icon:hover::before,.mdc-top-app-bar .mdc-top-app-bar__navigation-icon.mdc-ripple-surface--hover::before{opacity:0.08;opacity:var(--mdc-ripple-hover-opacity, 0.08)}.mdc-top-app-bar .mdc-top-app-bar__action-item.mdc-ripple-upgraded--background-focused::before,.mdc-top-app-bar .mdc-top-app-bar__action-item:not(.mdc-ripple-upgraded):focus::before,.mdc-top-app-bar .mdc-top-app-bar__navigation-icon.mdc-ripple-upgraded--background-focused::before,.mdc-top-app-bar .mdc-top-app-bar__navigation-icon:not(.mdc-ripple-upgraded):focus::before{transition-duration:75ms;opacity:0.24;opacity:var(--mdc-ripple-focus-opacity, 0.24)}.mdc-top-app-bar .mdc-top-app-bar__action-item:not(.mdc-ripple-upgraded)::after,.mdc-top-app-bar .mdc-top-app-bar__navigation-icon:not(.mdc-ripple-upgraded)::after{transition:opacity 150ms linear}.mdc-top-app-bar .mdc-top-app-bar__action-item:not(.mdc-ripple-upgraded):active::after,.mdc-top-app-bar .mdc-top-app-bar__navigation-icon:not(.mdc-ripple-upgraded):active::after{transition-duration:75ms;opacity:0.24;opacity:var(--mdc-ripple-press-opacity, 0.24)}.mdc-top-app-bar .mdc-top-app-bar__action-item.mdc-ripple-upgraded,.mdc-top-app-bar .mdc-top-app-bar__navigation-icon.mdc-ripple-upgraded{--mdc-ripple-fg-opacity:var(--mdc-ripple-press-opacity, 0.24)}.mdc-top-app-bar__row{display:flex;position:relative;box-sizing:border-box;width:100%;height:64px}.mdc-top-app-bar__section{display:inline-flex;flex:1 1 auto;align-items:center;min-width:0;padding:8px 12px;z-index:1}.mdc-top-app-bar__section--align-start{justify-content:flex-start;order:-1}.mdc-top-app-bar__section--align-end{justify-content:flex-end;order:1}.mdc-top-app-bar__title{-moz-osx-font-smoothing:grayscale;-webkit-font-smoothing:antialiased;font-family:Roboto, sans-serif;font-family:var(--mdc-typography-headline6-font-family, var(--mdc-typography-font-family, Roboto, sans-serif));font-size:1.25rem;font-size:var(--mdc-typography-headline6-font-size, 1.25rem);line-height:2rem;line-height:var(--mdc-typography-headline6-line-height, 2rem);font-weight:500;font-weight:var(--mdc-typography-headline6-font-weight, 500);letter-spacing:0.0125em;letter-spacing:var(--mdc-typography-headline6-letter-spacing, 0.0125em);text-decoration:inherit;-webkit-text-decoration:var(--mdc-typography-headline6-text-decoration, inherit);text-decoration:var(--mdc-typography-headline6-text-decoration, inherit);text-transform:inherit;text-transform:var(--mdc-typography-headline6-text-transform, inherit);padding-left:20px;padding-right:0;text-overflow:ellipsis;white-space:nowrap;overflow:hidden;z-index:1}[dir=rtl] .mdc-top-app-bar__title,.mdc-top-app-bar__title[dir=rtl]{padding-left:0;padding-right:20px}.mdc-top-app-bar--short-collapsed{border-top-left-radius:0;border-top-right-radius:0;border-bottom-right-radius:24px;border-bottom-left-radius:0}[dir=rtl] .mdc-top-app-bar--short-collapsed,.mdc-top-app-bar--short-collapsed[dir=rtl]{border-top-left-radius:0;border-top-right-radius:0;border-bottom-right-radius:0;border-bottom-left-radius:24px}.mdc-top-app-bar--short{top:0;right:auto;left:0;width:100%;transition:width 250ms cubic-bezier(0.4, 0, 0.2, 1)}[dir=rtl] .mdc-top-app-bar--short,.mdc-top-app-bar--short[dir=rtl]{right:0;left:auto}.mdc-top-app-bar--short .mdc-top-app-bar__row{height:56px}.mdc-top-app-bar--short .mdc-top-app-bar__section{padding:4px}.mdc-top-app-bar--short .mdc-top-app-bar__title{transition:opacity 200ms cubic-bezier(0.4, 0, 0.2, 1);opacity:1}.mdc-top-app-bar--short-collapsed{box-shadow:0px 2px 4px -1px rgba(0, 0, 0, 0.2),0px 4px 5px 0px rgba(0, 0, 0, 0.14),0px 1px 10px 0px rgba(0,0,0,.12);width:56px;transition:width 300ms cubic-bezier(0.4, 0, 0.2, 1)}.mdc-top-app-bar--short-collapsed .mdc-top-app-bar__title{display:none}.mdc-top-app-bar--short-collapsed .mdc-top-app-bar__action-item{transition:padding 150ms cubic-bezier(0.4, 0, 0.2, 1)}.mdc-top-app-bar--short-collapsed.mdc-top-app-bar--short-has-action-item{width:112px}.mdc-top-app-bar--short-collapsed.mdc-top-app-bar--short-has-action-item .mdc-top-app-bar__section--align-end{padding-left:0;padding-right:12px}[dir=rtl] .mdc-top-app-bar--short-collapsed.mdc-top-app-bar--short-has-action-item .mdc-top-app-bar__section--align-end,.mdc-top-app-bar--short-collapsed.mdc-top-app-bar--short-has-action-item .mdc-top-app-bar__section--align-end[dir=rtl]{padding-left:12px;padding-right:0}.mdc-top-app-bar--dense .mdc-top-app-bar__row{height:48px}.mdc-top-app-bar--dense .mdc-top-app-bar__section{padding:0 4px}.mdc-top-app-bar--dense .mdc-top-app-bar__title{padding-left:12px;padding-right:0}[dir=rtl] .mdc-top-app-bar--dense .mdc-top-app-bar__title,.mdc-top-app-bar--dense .mdc-top-app-bar__title[dir=rtl]{padding-left:0;padding-right:12px}.mdc-top-app-bar--prominent .mdc-top-app-bar__row{height:128px}.mdc-top-app-bar--prominent .mdc-top-app-bar__title{align-self:flex-end;padding-bottom:2px}.mdc-top-app-bar--prominent .mdc-top-app-bar__action-item,.mdc-top-app-bar--prominent .mdc-top-app-bar__navigation-icon{align-self:flex-start}.mdc-top-app-bar--fixed{transition:box-shadow 200ms linear}.mdc-top-app-bar--fixed-scrolled{box-shadow:0px 2px 4px -1px rgba(0, 0, 0, 0.2),0px 4px 5px 0px rgba(0, 0, 0, 0.14),0px 1px 10px 0px rgba(0,0,0,.12);transition:box-shadow 200ms linear}.mdc-top-app-bar--dense.mdc-top-app-bar--prominent .mdc-top-app-bar__row{height:96px}.mdc-top-app-bar--dense.mdc-top-app-bar--prominent .mdc-top-app-bar__section{padding:0 12px}.mdc-top-app-bar--dense.mdc-top-app-bar--prominent .mdc-top-app-bar__title{padding-left:20px;padding-right:0;padding-bottom:9px}[dir=rtl] .mdc-top-app-bar--dense.mdc-top-app-bar--prominent .mdc-top-app-bar__title,.mdc-top-app-bar--dense.mdc-top-app-bar--prominent .mdc-top-app-bar__title[dir=rtl]{padding-left:0;padding-right:20px}.mdc-top-app-bar--fixed-adjust{padding-top:64px}.mdc-top-app-bar--dense-fixed-adjust{padding-top:48px}.mdc-top-app-bar--short-fixed-adjust{padding-top:56px}.mdc-top-app-bar--prominent-fixed-adjust{padding-top:128px}.mdc-top-app-bar--dense-prominent-fixed-adjust{padding-top:96px}@media(max-width: 599px){.mdc-top-app-bar__row{height:56px}.mdc-top-app-bar__section{padding:4px}.mdc-top-app-bar--short{transition:width 200ms cubic-bezier(0.4, 0, 0.2, 1)}.mdc-top-app-bar--short-collapsed{transition:width 250ms cubic-bezier(0.4, 0, 0.2, 1)}.mdc-top-app-bar--short-collapsed .mdc-top-app-bar__section--align-end{padding-left:0;padding-right:12px}[dir=rtl] .mdc-top-app-bar--short-collapsed .mdc-top-app-bar__section--align-end,.mdc-top-app-bar--short-collapsed .mdc-top-app-bar__section--align-end[dir=rtl]{padding-left:12px;padding-right:0}.mdc-top-app-bar--prominent .mdc-top-app-bar__title{padding-bottom:6px}.mdc-top-app-bar--fixed-adjust{padding-top:56px}}\n\n/*# sourceMappingURL=mdc.top-app-bar.min.css.map*/"),f`
        .mdc-top-app-bar {
          position: static;
          color: var(--mdc-theme-on-primary, #fff);
        }
      `]}}]}}),I);const Ia=(t,e,a=!0,i=!0)=>{let n,o=0;const r=(...r)=>{const s=()=>{o=!1===a?0:Date.now(),n=void 0,t(...r)},l=Date.now();o||!1!==a||(o=l);const c=e-(l-o);c<=0||c>e?(n&&(clearTimeout(n),n=void 0),o=l,t(...r)):n||!1===i||(n=window.setTimeout(s,c))};return r.cancel=()=>{clearTimeout(n),n=void 0,o=0},r},Ea=["#44739e","#984ea3","#00d2d5","#ff7f00","#af8d00","#7f80cd","#b3e900","#c42e60","#a65628","#f781bf","#8dd3c7","#bebada","#fb8072","#80b1d3","#fdb462","#fccde5","#bc80bd","#ffed6f","#c4eaff","#cf8c00","#1b9e77","#d95f02","#e7298a","#e6ab02","#a6761d","#0097ff","#00d067","#f43600","#4ba93b","#5779bb","#927acc","#97ee3f","#bf3947","#9f5b00","#f48758","#8caed6","#f2b94f","#eff26e","#e43872","#d9b100","#9d7a00","#698cff","#d9d9d9","#00d27e","#d06800","#009f82","#c49200","#cbe8ff","#fecddf","#c27eb6","#8cd2ce","#c4b8d9","#f883b0","#a49100","#f48800","#27d0df","#a04a9b"];function Aa(t,e){return e.getPropertyValue(`--graph-color-${t+1}`)||function(t){return Ea[t%Ea.length]}(t)}T([g("ha-chart-base")],(function(t,e){class a extends e{constructor(...e){super(...e),t(this)}}return{F:a,d:[{kind:"field",key:"chart",value:void 0},{kind:"field",decorators:[d({attribute:"chart-type",reflect:!0})],key:"chartType",value:()=>"line"},{kind:"field",decorators:[d({attribute:!1})],key:"data",value:()=>({datasets:[]})},{kind:"field",decorators:[d({attribute:!1})],key:"options",value:void 0},{kind:"field",decorators:[d({attribute:!1})],key:"plugins",value:void 0},{kind:"field",decorators:[d({type:Number})],key:"height",value:void 0},{kind:"field",decorators:[b()],key:"_chartHeight",value:void 0},{kind:"field",decorators:[b()],key:"_tooltip",value:void 0},{kind:"field",decorators:[b()],key:"_hiddenDatasets",value:()=>new Set},{kind:"method",key:"firstUpdated",value:function(){this._setupChart(),this.data.datasets.forEach(((t,e)=>{t.hidden&&this._hiddenDatasets.add(e)}))}},{kind:"method",key:"willUpdate",value:function(t){if(R(O(a.prototype),"willUpdate",this).call(this,t),this.hasUpdated&&this.chart){if(t.has("plugins"))return this.chart.destroy(),void this._setupChart();t.has("chartType")&&(this.chart.config.type=this.chartType),t.has("data")&&(this._hiddenDatasets.size&&this.data.datasets.forEach(((t,e)=>{t.hidden=this._hiddenDatasets.has(e)})),this.chart.data=this.data),t.has("options")&&(this.chart.options=this._createOptions()),this.chart.update("none")}}},{kind:"method",key:"render",value:function(){var t,e,a,i;return p`
      ${!0===(null===(t=this.options)||void 0===t||null===(e=t.plugins)||void 0===e||null===(a=e.legend)||void 0===a?void 0:a.display)?p`<div class="chartLegend">
            <ul>
              ${this.data.datasets.map(((t,e)=>p`<li
                  .datasetIndex=${e}
                  @click=${this._legendClick}
                  class=${u({hidden:this._hiddenDatasets.has(e)})}
                  .title=${t.label}
                >
                  <div
                    class="bullet"
                    style=${N({backgroundColor:t.backgroundColor,borderColor:t.borderColor})}
                  ></div>
                  <div class="label">${t.label}</div>
                </li>`))}
            </ul>
          </div>`:""}
      <div
        class="chartContainer"
        style=${N({height:`${null!==(i=this.height)&&void 0!==i?i:this._chartHeight}px`,overflow:this._chartHeight?"initial":"hidden"})}
      >
        <canvas></canvas>
        ${this._tooltip?p`<div
              class="chartTooltip ${u({[this._tooltip.yAlign]:!0})}"
              style=${N({top:this._tooltip.top,left:this._tooltip.left})}
            >
              <div class="title">${this._tooltip.title}</div>
              ${this._tooltip.beforeBody?p`<div class="beforeBody">
                    ${this._tooltip.beforeBody}
                  </div>`:""}
              <div>
                <ul>
                  ${this._tooltip.body.map(((t,e)=>p`<li>
                      <div
                        class="bullet"
                        style=${N({backgroundColor:this._tooltip.labelColors[e].backgroundColor,borderColor:this._tooltip.labelColors[e].borderColor})}
                      ></div>
                      ${t.lines.join("\n")}
                    </li>`))}
                </ul>
              </div>
              ${this._tooltip.footer.length?p`<div class="footer">
                    ${this._tooltip.footer.map((t=>p`${t}<br />`))}
                  </div>`:""}
            </div>`:""}
      </div>
    `}},{kind:"method",key:"_setupChart",value:async function(){const t=this.renderRoot.querySelector("canvas").getContext("2d"),e=(await import("./c.2a7b7499.js")).Chart,a=getComputedStyle(this);e.defaults.borderColor=a.getPropertyValue("--divider-color"),e.defaults.color=a.getPropertyValue("--secondary-text-color"),this.chart=new e(t,{type:this.chartType,data:this.data,options:this._createOptions(),plugins:this._createPlugins()})}},{kind:"method",key:"_createOptions",value:function(){var t,e,a,i,n;return{...this.options,plugins:{...null===(t=this.options)||void 0===t?void 0:t.plugins,tooltip:{...null===(e=this.options)||void 0===e||null===(a=e.plugins)||void 0===a?void 0:a.tooltip,enabled:!1,external:t=>this._handleTooltip(t)},legend:{...null===(i=this.options)||void 0===i||null===(n=i.plugins)||void 0===n?void 0:n.legend,display:!1}}}}},{kind:"method",key:"_createPlugins",value:function(){var t,e;return[...this.plugins||[],{id:"afterRenderHook",afterRender:t=>{this._chartHeight=t.height},legend:{...null===(t=this.options)||void 0===t||null===(e=t.plugins)||void 0===e?void 0:e.legend,display:!1}}]}},{kind:"method",key:"_legendClick",value:function(t){if(!this.chart)return;const e=t.currentTarget.datasetIndex;this.chart.isDatasetVisible(e)?(this.chart.setDatasetVisibility(e,!1),this._hiddenDatasets.add(e)):(this.chart.setDatasetVisibility(e,!0),this._hiddenDatasets.delete(e)),this.chart.update("none"),this.requestUpdate("_hiddenDatasets")}},{kind:"method",key:"_handleTooltip",value:function(t){var e,a,i;0!==t.tooltip.opacity?this._tooltip={...t.tooltip,top:this.chart.canvas.offsetTop+t.tooltip.caretY+12+"px",left:this.chart.canvas.offsetLeft+(e=t.tooltip.caretX,a=100,i=this.clientWidth-100,Math.min(Math.max(e,a),i))-100+"px"}:this._tooltip=void 0}},{kind:"field",key:"updateChart",value(){return t=>{this.chart&&this.chart.update(t)}}},{kind:"get",static:!0,key:"styles",value:function(){return f`
      :host {
        display: block;
      }
      .chartContainer {
        overflow: hidden;
        height: 0;
        transition: height 300ms cubic-bezier(0.4, 0, 0.2, 1);
      }
      canvas {
        max-height: var(--chart-max-height, 400px);
      }
      .chartLegend {
        text-align: center;
      }
      .chartLegend li {
        cursor: pointer;
        display: inline-grid;
        grid-auto-flow: column;
        padding: 0 8px;
        box-sizing: border-box;
        align-items: center;
        color: var(--secondary-text-color);
      }
      .chartLegend .hidden {
        text-decoration: line-through;
      }
      .chartLegend .label {
        text-overflow: ellipsis;
        white-space: nowrap;
        overflow: hidden;
      }
      .chartLegend .bullet,
      .chartTooltip .bullet {
        border-width: 1px;
        border-style: solid;
        border-radius: 50%;
        display: inline-block;
        height: 16px;
        margin-right: 6px;
        width: 16px;
        flex-shrink: 0;
        box-sizing: border-box;
      }
      .chartTooltip .bullet {
        align-self: baseline;
      }
      :host([rtl]) .chartLegend .bullet,
      :host([rtl]) .chartTooltip .bullet {
        margin-right: inherit;
        margin-left: 6px;
      }
      .chartTooltip {
        padding: 8px;
        font-size: 90%;
        position: absolute;
        background: rgba(80, 80, 80, 0.9);
        color: white;
        border-radius: 4px;
        pointer-events: none;
        z-index: 1000;
        width: 200px;
        box-sizing: border-box;
      }
      :host([rtl]) .chartTooltip {
        direction: rtl;
      }
      .chartLegend ul,
      .chartTooltip ul {
        display: inline-block;
        padding: 0 0px;
        margin: 8px 0 0 0;
        width: 100%;
      }
      .chartTooltip ul {
        margin: 0 4px;
      }
      .chartTooltip li {
        display: flex;
        white-space: pre-line;
        align-items: center;
        line-height: 16px;
        padding: 4px 0;
      }
      .chartTooltip .title {
        text-align: center;
        font-weight: 500;
      }
      .chartTooltip .footer {
        font-weight: 500;
      }
      .chartTooltip .beforeBody {
        text-align: center;
        font-weight: 300;
        word-break: break-all;
      }
    `}}]}}),I);const $a=t=>{const e=parseFloat(t);return isFinite(e)?e:null};let La=T(null,(function(t,e){return{F:class extends e{constructor(...e){super(...e),t(this)}},d:[{kind:"field",decorators:[d({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[d({attribute:!1})],key:"data",value:()=>[]},{kind:"field",decorators:[d()],key:"names",value:()=>!1},{kind:"field",decorators:[d()],key:"unit",value:void 0},{kind:"field",decorators:[d()],key:"identifier",value:void 0},{kind:"field",decorators:[d({type:Boolean})],key:"isSingleDevice",value:()=>!1},{kind:"field",decorators:[d({attribute:!1})],key:"endTime",value:void 0},{kind:"field",decorators:[b()],key:"_chartData",value:void 0},{kind:"field",decorators:[b()],key:"_chartOptions",value:void 0},{kind:"method",key:"render",value:function(){return p`
      <ha-chart-base
        .data=${this._chartData}
        .options=${this._chartOptions}
        chart-type="line"
      ></ha-chart-base>
    `}},{kind:"method",key:"willUpdate",value:function(t){this.hasUpdated||(this._chartOptions={parsing:!1,animation:!1,scales:{x:{type:"time",adapters:{date:{locale:this.hass.locale}},ticks:{maxRotation:0,sampleSize:5,autoSkipPadding:20,major:{enabled:!0},font:t=>t.tick&&t.tick.major?{weight:"bold"}:{}},time:{tooltipFormat:"datetimeseconds"}},y:{ticks:{maxTicksLimit:7},title:{display:!0,text:this.unit}}},plugins:{tooltip:{mode:"nearest",callbacks:{label:t=>`${t.dataset.label}: ${ha(t.parsed.y,this.hass.locale)} ${this.unit}`}},filler:{propagate:!0},legend:{display:!this.isSingleDevice,labels:{usePointStyle:!0}}},hover:{mode:"nearest"},elements:{line:{tension:.1,borderWidth:1.5},point:{hitRadius:5}},locale:da(this.hass.locale)}),t.has("data")&&this._generateData()}},{kind:"method",key:"_generateData",value:function(){let t=0;const e=getComputedStyle(this),a=this.data,i=[];let n;if(0===a.length)return;n=this.endTime||new Date(Math.max(...a.map((t=>new Date(t.states[t.states.length-1].last_changed).getTime())))),n>new Date&&(n=new Date);const o=this.names||{};a.forEach((a=>{const r=a.domain,s=o[a.entity_id]||a.name;let l=null;const c=[],d=(t,e)=>{e&&(t>n||(c.forEach(((a,i)=>{null===e[i]&&l&&null!==l[i]&&a.data.push({x:t.getTime(),y:l[i]}),a.data.push({x:t.getTime(),y:e[i]})})),l=e))},h=(a,i=!1,n)=>{n||(n=Aa(t,e),t++),c.push({label:a,fill:!!i&&"origin",borderColor:n,backgroundColor:n+"7F",stepped:"before",pointRadius:0,data:[]})};if("thermostat"===r||"climate"===r||"water_heater"===r){const t=a.states.some((t=>{var e;return null===(e=t.attributes)||void 0===e?void 0:e.hvac_action})),i="climate"===r&&t?t=>{var e;return"heating"===(null===(e=t.attributes)||void 0===e?void 0:e.hvac_action)}:t=>"heat"===t.state,n="climate"===r&&t?t=>{var e;return"cooling"===(null===(e=t.attributes)||void 0===e?void 0:e.hvac_action)}:t=>"cool"===t.state,o=a.states.some(i),l=a.states.some(n),c=a.states.some((t=>t.attributes&&t.attributes.target_temp_high!==t.attributes.target_temp_low));h(`${this.hass.localize("ui.card.climate.current_temperature",{name:s})}`),o&&h(`${this.hass.localize("ui.card.climate.heating",{name:s})}`,!0,e.getPropertyValue("--state-climate-heat-color")),l&&h(`${this.hass.localize("ui.card.climate.cooling",{name:s})}`,!0,e.getPropertyValue("--state-climate-cool-color")),c?(h(`${this.hass.localize("ui.card.climate.target_temperature_mode",{name:s,mode:this.hass.localize("ui.card.climate.high")})}`),h(`${this.hass.localize("ui.card.climate.target_temperature_mode",{name:s,mode:this.hass.localize("ui.card.climate.low")})}`)):h(`${this.hass.localize("ui.card.climate.target_temperature_entity",{name:s})}`),a.states.forEach((t=>{if(!t.attributes)return;const e=$a(t.attributes.current_temperature),a=[e];if(o&&a.push(i(t)?e:null),l&&a.push(n(t)?e:null),c){const e=$a(t.attributes.target_temp_high),i=$a(t.attributes.target_temp_low);a.push(e,i),d(new Date(t.last_changed),a)}else{const e=$a(t.attributes.temperature);a.push(e),d(new Date(t.last_changed),a)}}))}else if("humidifier"===r)h(`${this.hass.localize("ui.card.humidifier.target_humidity_entity",{name:s})}`),h(`${this.hass.localize("ui.card.humidifier.on_entity",{name:s})}`,!0),a.states.forEach((t=>{if(!t.attributes)return;const e=$a(t.attributes.humidity),a=[e];a.push("on"===t.state?e:null),d(new Date(t.last_changed),a)}));else{let t,e;h(s);let i=null;a.states.forEach((a=>{const n=$a(a.state),o=new Date(a.last_changed);if(null!==n&&i){var r;const a=o.getTime(),s=i.getTime(),l=null===(r=e)||void 0===r?void 0:r.getTime();d(i,[(s-l)/(a-l)*(n-t)+t]),d(new Date(s+1),[null]),d(o,[n]),e=o,t=n,i=null}else null!==n&&null===i?(d(o,[n]),e=o,t=n):null===n&&null===i&&void 0!==t&&(i=o)}))}d(n,l),Array.prototype.push.apply(i,c)})),this._chartData={datasets:i}}}]}}),I);customElements.define("state-history-chart-line",La);const Ra=new Set(["battery_charging","connectivity","light","moving","plug","power","presence","running"]),Oa=new Set(["on","off","home","not_home","unavailable","unknown","idle"]),Da=new Map;let za=0;const Ma=(t,e,a)=>{if("on"!==t&&"off"!==t||!(t=>t&&"binary_sensor"===et(t.entity_id)&&"device_class"in t.attributes&&!Ra.has(t.attributes.device_class))(e)||(t="on"===t?"off":"on"),Da.has(t))return Da.get(t);if(Oa.has(t)){const e=a.getPropertyValue(`--state-${t}-color`);return Da.set(t,e),e}const i=Aa(za,a);return za++,Da.set(t,i),i};T([g("state-history-chart-timeline")],(function(t,e){return{F:class extends e{constructor(...e){super(...e),t(this)}},d:[{kind:"field",decorators:[d({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[d({attribute:!1})],key:"data",value:()=>[]},{kind:"field",decorators:[d()],key:"names",value:()=>!1},{kind:"field",decorators:[d()],key:"unit",value:void 0},{kind:"field",decorators:[d()],key:"identifier",value:void 0},{kind:"field",decorators:[d({type:Boolean})],key:"isSingleDevice",value:()=>!1},{kind:"field",decorators:[d({attribute:!1})],key:"endTime",value:void 0},{kind:"field",decorators:[b()],key:"_chartData",value:void 0},{kind:"field",decorators:[b()],key:"_chartOptions",value:void 0},{kind:"method",key:"render",value:function(){return p`
      <ha-chart-base
        .data=${this._chartData}
        .options=${this._chartOptions}
        .height=${30*this.data.length+30}
        chart-type="timeline"
      ></ha-chart-base>
    `}},{kind:"method",key:"willUpdate",value:function(t){this.hasUpdated||(this._chartOptions={maintainAspectRatio:!1,parsing:!1,animation:!1,scales:{x:{type:"timeline",position:"bottom",adapters:{date:{locale:this.hass.locale}},ticks:{autoSkip:!0,maxRotation:0,sampleSize:5,autoSkipPadding:20,major:{enabled:!0},font:t=>t.tick&&t.tick.major?{weight:"bold"}:{}},grid:{offset:!1},time:{tooltipFormat:"datetimeseconds"}},y:{type:"category",barThickness:20,offset:!0,grid:{display:!1,drawBorder:!1,drawTicks:!1},ticks:{display:1!==this.data.length},afterSetDimensions:t=>{t.maxWidth=.18*t.chart.width},position:tt(this.hass)?"right":"left"}},plugins:{tooltip:{mode:"nearest",callbacks:{title:t=>t[0].chart.data.labels[t[0].datasetIndex],beforeBody:t=>t[0].dataset.label||"",label:t=>{const e=t.dataset.data[t.dataIndex];return[e.label||"",la(e.start,this.hass.locale),la(e.end,this.hass.locale)]},labelColor:t=>({borderColor:t.dataset.data[t.dataIndex].color,backgroundColor:t.dataset.data[t.dataIndex].color})}},filler:{propagate:!0}},locale:da(this.hass.locale)}),t.has("data")&&this._generateData()}},{kind:"method",key:"_generateData",value:function(){const t=getComputedStyle(this);let e=this.data;e||(e=[]);const a=new Date(e.reduce(((t,e)=>Math.min(t,new Date(e.data[0].last_changed).getTime())),(new Date).getTime()));let i=this.endTime||new Date(e.reduce(((t,e)=>Math.max(t,new Date(e.data[e.data.length-1].last_changed).getTime())),a.getTime()));i>new Date&&(i=new Date);const n=[],o=[],r=this.names||{};e.forEach((e=>{let s,l=null,c=null,d=a;const h=r[e.entity_id]||e.name,p=[];e.data.forEach((a=>{let n=a.state;n||(n=null),new Date(a.last_changed)>i||(null===l?(l=n,c=a.state_localize,d=new Date(a.last_changed)):n!==l&&(s=new Date(a.last_changed),p.push({start:d,end:s,label:c,color:Ma(l,this.hass.states[e.entity_id],t)}),l=n,c=a.state_localize,d=s))})),null!==l&&p.push({start:d,end:i,label:c,color:Ma(l,this.hass.states[e.entity_id],t)}),o.push({data:p,label:e.entity_id}),n.push(h)})),this._chartData={labels:n,datasets:o}}},{kind:"get",static:!0,key:"styles",value:function(){return f`
      ha-chart-base {
        --chart-max-height: none;
      }
    `}}]}}),I),T([g("state-history-charts")],(function(t,e){return{F:class extends e{constructor(...e){super(...e),t(this)}},d:[{kind:"field",decorators:[d({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[d({attribute:!1})],key:"historyData",value:void 0},{kind:"field",decorators:[d({type:Boolean})],key:"names",value:()=>!1},{kind:"field",decorators:[d({attribute:!1})],key:"endTime",value:void 0},{kind:"field",decorators:[d({type:Boolean,attribute:"up-to-now"})],key:"upToNow",value:()=>!1},{kind:"field",decorators:[d({type:Boolean,attribute:"no-single"})],key:"noSingle",value:()=>!1},{kind:"field",decorators:[d({type:Boolean})],key:"isLoadingData",value:()=>!1},{kind:"method",key:"render",value:function(){if(!at(this.hass,"history"))return p` <div class="info">
        ${this.hass.localize("ui.components.history_charts.history_disabled")}
      </div>`;if(this.isLoadingData&&!this.historyData)return p` <div class="info">
        ${this.hass.localize("ui.components.history_charts.loading_history")}
      </div>`;if(this._isHistoryEmpty())return p` <div class="info">
        ${this.hass.localize("ui.components.history_charts.no_history_found")}
      </div>`;const t=this.upToNow?new Date:this.endTime||new Date;return p`
      ${this.historyData.timeline.length?p`
            <state-history-chart-timeline
              .hass=${this.hass}
              .data=${this.historyData.timeline}
              .endTime=${t}
              .noSingle=${this.noSingle}
              .names=${this.names}
            ></state-history-chart-timeline>
          `:p``}
      ${this.historyData.line.map((e=>p`
          <state-history-chart-line
            .hass=${this.hass}
            .unit=${e.unit}
            .data=${e.data}
            .identifier=${e.identifier}
            .isSingleDevice=${!this.noSingle&&e.data&&1===e.data.length}
            .endTime=${t}
            .names=${this.names}
          ></state-history-chart-line>
        `))}
    `}},{kind:"method",key:"shouldUpdate",value:function(t){return!(1===t.size&&t.has("hass"))}},{kind:"method",key:"_isHistoryEmpty",value:function(){const t=!this.historyData||!this.historyData.timeline||!this.historyData.line||0===this.historyData.timeline.length&&0===this.historyData.line.length;return!this.isLoadingData&&t}},{kind:"get",static:!0,key:"styles",value:function(){return f`
      :host {
        display: block;
        /* height of single timeline chart = 60px */
        min-height: 60px;
      }
      .info {
        text-align: center;
        line-height: 60px;
        color: var(--secondary-text-color);
      }
    `}}]}}),I),Ue&&await Ue;const Na=(t,e)=>ja(e).format(t),ja=S((t=>new Intl.DateTimeFormat("en"!==t.language||oa(t)?t.language:"en-u-hc-h23",{hour:"numeric",minute:"2-digit",hour12:oa(t)}))),Fa=(t,e)=>Pa(e).format(t),Pa=S((t=>new Intl.DateTimeFormat("en"!==t.language||oa(t)?t.language:"en-u-hc-h23",{hour:oa(t)?"numeric":"2-digit",minute:"2-digit",second:"2-digit",hour12:oa(t)})));S((t=>new Intl.DateTimeFormat("en"!==t.language||oa(t)?t.language:"en-u-hc-h23",{weekday:"long",hour:oa(t)?"numeric":"2-digit",minute:"2-digit",hour12:oa(t)})));const Ba=t=>t<10?`0${t}`:t;const Ha={s:1,min:60,h:3600,d:86400},Ga=(t,e)=>function(t){const e=Math.floor(t/3600),a=Math.floor(t%3600/60),i=Math.floor(t%3600%60);return e>0?`${e}:${Ba(a)}:${Ba(i)}`:a>0?`${a}:${Ba(i)}`:i>0?""+i:null}(parseFloat(t)*Ha[e])||"0",Ka=(t,e,a,i)=>{const n=void 0!==i?i:e.state;if(n===it||n===nt)return t(`state.default.${n}`);if((t=>!!t.attributes.unit_of_measurement||!!t.attributes.state_class)(e)){if("duration"===e.attributes.device_class&&e.attributes.unit_of_measurement&&Ha[e.attributes.unit_of_measurement])try{return Ga(n,e.attributes.unit_of_measurement)}catch(t){}if("monetary"===e.attributes.device_class)try{return ha(n,a,{style:"currency",currency:e.attributes.unit_of_measurement,minimumFractionDigits:2})}catch(t){}return`${ha(n,a)}${e.attributes.unit_of_measurement?" "+e.attributes.unit_of_measurement:""}`}const o=ot(e);if("input_datetime"===o){if(void 0===i){let t;return e.attributes.has_date&&e.attributes.has_time?(t=new Date(e.attributes.year,e.attributes.month-1,e.attributes.day,e.attributes.hour,e.attributes.minute),ra(t,a)):e.attributes.has_date?(t=new Date(e.attributes.year,e.attributes.month-1,e.attributes.day),Xe(t,a)):e.attributes.has_time?(t=new Date,t.setHours(e.attributes.hour,e.attributes.minute),Na(t,a)):e.state}try{const t=i.split(" ");if(2===t.length)return ra(new Date(t.join("T")),a);if(1===t.length){if(i.includes("-"))return Xe(new Date(`${i}T00:00`),a);if(i.includes(":")){const t=new Date;return Na(new Date(`${t.toISOString().split("T")[0]}T${i}`),a)}}return i}catch(t){return i}}if("humidifier"===o&&"on"===n&&e.attributes.humidity)return`${e.attributes.humidity} %`;if("counter"===o||"number"===o||"input_number"===o)return ha(n,a);if("button"===o||"input_button"===o||"scene"===o||"sensor"===o&&"timestamp"===e.attributes.device_class)try{return ra(new Date(n),a)}catch(t){return n}var r;return"update"===o?"on"===n?rt(e)?st(e,lt)?t("ui.card.update.installing_with_progress",{progress:e.attributes.in_progress}):t("ui.card.update.installing"):e.attributes.latest_version:e.attributes.skipped_version===e.attributes.latest_version?null!==(r=e.attributes.latest_version)&&void 0!==r?r:t("state.default.unavailable"):t("ui.card.update.up_to_date"):e.attributes.device_class&&t(`component.${o}.state.${e.attributes.device_class}.${n}`)||t(`component.${o}.state._.${n}`)||n},Ua=["climate","humidifier","water_heater"],Wa=["climate","humidifier","input_datetime","thermostat","water_heater"],Va=["temperature","current_temperature","target_temp_low","target_temp_high","hvac_action","humidity","mode"],Ya=(t,e,a,i,n=!1,o,r=!0,s)=>{let l="history/period";return a&&(l+="/"+a.toISOString()),l+="?filter_entity_id="+e,i&&(l+="&end_time="+i.toISOString()),n&&(l+="&skip_initial_state"),void 0!==o&&(l+=`&significant_changes_only=${Number(o)}`),r&&(l+="&minimal_response"),s&&(l+="&no_attributes"),t.callApi("GET",l)},Xa=(t,e)=>t.state===e.state&&(!t.attributes||!e.attributes||Va.every((a=>t.attributes[a]===e.attributes[a]))),qa=t=>"unit_of_measurement"in t.attributes||"state_class"in t.attributes,Za=(t,e,a)=>{const i={},n=[];if(!e)return{line:[],timeline:[]};e.forEach((e=>{if(0===e.length)return;const o=e[0].entity_id,r=o in t.states?t.states[o]:void 0,s=!r&&e.find((t=>t.attributes&&qa(t)));let l;l=r&&qa(r)?r.attributes.unit_of_measurement||" ":s?s.attributes.unit_of_measurement||" ":{climate:t.config.unit_system.temperature,counter:"#",humidifier:"%",input_number:"#",number:"#",water_heater:t.config.unit_system.temperature}[et(o)],l?l in i?i[l].push(e):i[l]=[e]:n.push(((t,e,a)=>{const i=[],n=a.length-1;for(const o of a)i.length>0&&o.state===i[i.length-1].state||(o.entity_id||(o.attributes=a[n].attributes,o.entity_id=a[n].entity_id),i.push({state_localize:Ka(t,o,e),state:o.state,last_changed:o.last_changed}));return{name:J(a[0]),entity_id:a[0].entity_id,data:i}})(a,t.locale,e))}));return{line:Object.keys(i).map((t=>((t,e)=>{const a=[];for(const t of e){const e=t[t.length-1],i=ot(e),n=[];for(const e of t){let t;if(Ua.includes(i)){t={state:e.state,last_changed:e.last_updated,attributes:{}};for(const a of Va)a in e.attributes&&(t.attributes[a]=e.attributes[a])}else t=e;n.length>1&&Xa(t,n[n.length-1])&&Xa(t,n[n.length-2])||n.push(t)}a.push({domain:i,name:J(e),entity_id:e.entity_id,states:n})}return{unit:t,identifier:e.map((t=>t[0].entity_id)).join(""),data:a}})(t,i[t]))),timeline:n}},Qa={};const Ja=(t,e,a,i,n)=>{const o=a.cacheKey,r=new Date,s=new Date(r);s.setHours(s.getHours()-a.hoursToShow);let l=s,c=!1,d=Qa[o+`_${a.hoursToShow}`];if(d&&l>=d.startTime&&l<=d.endTime&&d.language===n){if(l=d.endTime,c=!0,r<=d.endTime)return d.prom}else d=Qa[o]=function(t,e,a){return{prom:Promise.resolve({line:[],timeline:[]}),language:t,startTime:e,endTime:a,data:{line:[],timeline:[]}}}(n,s,r);const h=d.prom,p=!((t,e)=>!t.states[e]||Wa.includes(et(e)))(t,e);return d.prom=(async()=>{let a;try{a=(await Promise.all([h,Ya(t,e,l,r,c,void 0,!0,p)]))[1]}catch(t){throw delete Qa[o],t}const n=Za(t,a,i);return c?(ti(n.line,d.data.line),ei(n.timeline,d.data.timeline),ii(s,d.data)):d.data=n,d.data})(),d.startTime=s,d.endTime=r,d.prom},ti=(t,e)=>{t.forEach((t=>{const a=t.unit,i=e.find((t=>t.unit===a));i?t.data.forEach((t=>{const e=i.data.find((e=>t.entity_id===e.entity_id));e?e.states=e.states.concat(t.states):i.data.push(t)})):e.push(t)}))},ei=(t,e)=>{t.forEach((t=>{const a=e.find((e=>e.entity_id===t.entity_id));a?a.data=a.data.concat(t.data):e.push(t)}))},ai=(t,e)=>{if(0===e.length)return e;const a=e.findIndex((e=>new Date(e.last_changed)>t));if(0===a)return e;const i=-1===a?e.length-1:a-1;return e[i].last_changed=t,e.slice(i)},ii=(t,e)=>{e.line.forEach((e=>{e.data.forEach((e=>{e.states=ai(t,e.states)}))})),e.timeline.forEach((e=>{e.data=ai(t,e.data)}))};T([g("ha-more-info-history")],(function(t,e){class a extends e{constructor(...e){super(...e),t(this)}}return{F:a,d:[{kind:"field",decorators:[d({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[d()],key:"entityId",value:void 0},{kind:"field",decorators:[b()],key:"_stateHistory",value:void 0},{kind:"field",key:"_showMoreHref",value:()=>""},{kind:"field",key:"_throttleGetStateHistory",value(){return Ia((()=>{this._getStateHistory()}),1e4)}},{kind:"method",key:"render",value:function(){return this.entityId?p`${at(this.hass,"history")?p` <div class="header">
            <div class="title">
              ${this.hass.localize("ui.dialogs.more_info_control.history")}
            </div>
            <a href=${this._showMoreHref} @click=${this._close}
              >${this.hass.localize("ui.dialogs.more_info_control.show_more")}</a
            >
          </div>
          <state-history-charts
            up-to-now
            .hass=${this.hass}
            .historyData=${this._stateHistory}
            .isLoadingData=${!this._stateHistory}
          ></state-history-charts>`:""}`:p``}},{kind:"method",key:"updated",value:function(t){if(R(O(a.prototype),"updated",this).call(this,t),t.has("entityId")){if(this._stateHistory=void 0,!this.entityId)return;return this._showMoreHref=`/history?entity_id=${this.entityId}&start_date=${Ta().toISOString()}`,void this._throttleGetStateHistory()}if(!this.entityId||!t.has("hass"))return;const e=t.get("hass");e&&this.hass.states[this.entityId]!==(null==e?void 0:e.states[this.entityId])&&setTimeout(this._throttleGetStateHistory,1e3)}},{kind:"method",key:"_getStateHistory",value:async function(){at(this.hass,"history")&&(this._stateHistory=await Ja(this.hass,this.entityId,{cacheKey:`more_info.${this.entityId}`,hoursToShow:24},this.hass.localize,this.hass.language))}},{kind:"method",key:"_close",value:function(){setTimeout((()=>n(this,"closed")),500)}},{kind:"get",static:!0,key:"styles",value:function(){return[f`
        .header {
          display: flex;
          flex-direction: row;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 8px;
        }
        .header > a,
        a:visited {
          color: var(--primary-color);
        }
        .title {
          font-family: var(--paper-font-title_-_font-family);
          -webkit-font-smoothing: var(
            --paper-font-title_-_-webkit-font-smoothing
          );
          font-size: var(--paper-font-subhead_-_font-size);
          font-weight: var(--paper-font-title_-_font-weight);
          letter-spacing: var(--paper-font-title_-_letter-spacing);
          line-height: var(--paper-font-title_-_line-height);
        }
      `]}}]}}),I);const ni="ui.components.logbook.messages",oi={},ri=(t,e,a)=>{for(const i of a){const a=t.states[i.entity_id];i.state&&a&&(i.message=ci(t,e,i.state,a,et(i.entity_id)))}return a},si=async(t,e,a,i)=>{const n="*";i||(i=n);const o=`${e}${a}`;if(oi[o]||(oi[o]={}),i in oi[o])return oi[o][i];if(i!==n&&oi[o]["*"]){return(await oi[o]["*"]).filter((t=>t.entity_id===i))}return oi[o][i]=li(t,e,a,i!==n?i:void 0).then((t=>t.reverse())),oi[o][i]},li=(t,e,a,i,n)=>{let o={type:"logbook/get_events",start_time:e};return a&&(o={...o,end_time:a}),i?o={...o,entity_ids:i.split(",")}:n&&(o={...o,context_id:n}),t.callWS(o)},ci=(t,e,a,i,n)=>{switch(n){case"device_tracker":case"person":return"not_home"===a?e(`${ni}.was_away`):"home"===a?e(`${ni}.was_at_home`):e(`${ni}.was_at_state`,"state",a);case"sun":return e("above_horizon"===a?`${ni}.rose`:`${ni}.set`);case"binary_sensor":{const t=a===ct,n=a===dt,o=i.attributes.device_class;switch(o){case"battery":if(t)return e(`${ni}.was_low`);if(n)return e(`${ni}.was_normal`);break;case"connectivity":if(t)return e(`${ni}.was_connected`);if(n)return e(`${ni}.was_disconnected`);break;case"door":case"garage_door":case"opening":case"window":if(t)return e(`${ni}.was_opened`);if(n)return e(`${ni}.was_closed`);break;case"lock":if(t)return e(`${ni}.was_unlocked`);if(n)return e(`${ni}.was_locked`);break;case"plug":if(t)return e(`${ni}.was_plugged_in`);if(n)return e(`${ni}.was_unplugged`);break;case"presence":if(t)return e(`${ni}.was_at_home`);if(n)return e(`${ni}.was_away`);break;case"safety":if(t)return e(`${ni}.was_unsafe`);if(n)return e(`${ni}.was_safe`);break;case"cold":case"gas":case"heat":case"moisture":case"motion":case"occupancy":case"power":case"problem":case"smoke":case"sound":case"vibration":if(t)return e(`${ni}.detected_device_class`,{device_class:e(`component.binary_sensor.device_class.${o}`)});if(n)return e(`${ni}.cleared_device_class`,{device_class:e(`component.binary_sensor.device_class.${o}`)});break;case"tamper":if(t)return e(`${ni}.detected_tampering`);if(n)return e(`${ni}.cleared_tampering`)}break}case"cover":switch(a){case"open":return e(`${ni}.was_opened`);case"opening":return e(`${ni}.is_opening`);case"closing":return e(`${ni}.is_closing`);case"closed":return e(`${ni}.was_closed`)}break;case"lock":if("unlocked"===a)return e(`${ni}.was_unlocked`);if("locked"===a)return e(`${ni}.was_locked`)}return a===ct?e(`${ni}.turned_on`):a===dt?e(`${ni}.turned_off`):Q.includes(a)?e(`${ni}.became_unavailable`):t.localize(`${ni}.changed_to_state`,"state",i?Ka(e,i,t.locale,a):a)},di={script_started:"from_script"};T([g("ha-logbook-renderer")],(function(t,e){return{F:class extends e{constructor(...e){super(...e),t(this)}},d:[{kind:"field",decorators:[d({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[d({attribute:!1})],key:"userIdToName",value:()=>({})},{kind:"field",decorators:[d({attribute:!1})],key:"traceContexts",value:()=>({})},{kind:"field",decorators:[d({attribute:!1})],key:"entries",value:()=>[]},{kind:"field",decorators:[d({type:Boolean,attribute:"narrow"})],key:"narrow",value:()=>!1},{kind:"field",decorators:[d({attribute:"rtl",type:Boolean})],key:"_rtl",value:()=>!1},{kind:"field",decorators:[d({type:Boolean,attribute:"virtualize",reflect:!0})],key:"virtualize",value:()=>!1},{kind:"field",decorators:[d({type:Boolean,attribute:"no-icon"})],key:"noIcon",value:()=>!1},{kind:"field",decorators:[d({type:Boolean,attribute:"no-name"})],key:"noName",value:()=>!1},{kind:"field",decorators:[d({type:Boolean,attribute:"relative-time"})],key:"relativeTime",value:()=>!1},{kind:"field",decorators:[ht(".container")],key:"_savedScrollPos",value:void 0},{kind:"method",key:"shouldUpdate",value:function(t){const e=t.get("hass"),a=void 0===e||e.locale!==this.hass.locale;return t.has("entries")||t.has("traceContexts")||a}},{kind:"method",key:"updated",value:function(t){const e=t.get("hass");void 0!==e&&e.language===this.hass.language||(this._rtl=tt(this.hass))}},{kind:"method",key:"render",value:function(){var t;return null!==(t=this.entries)&&void 0!==t&&t.length?p`
      <div
        class="container ha-scrollbar ${u({narrow:this.narrow,rtl:this._rtl,"no-name":this.noName,"no-icon":this.noIcon})}"
        @scroll=${this._saveScrollPos}
      >
        ${this.virtualize?p`<lit-virtualizer
              scroller
              class="ha-scrollbar"
              .items=${this.entries}
              .renderItem=${this._renderLogbookItem}
            >
            </lit-virtualizer>`:this.entries.map(((t,e)=>this._renderLogbookItem(t,e)))}
      </div>
    `:p`
        <div class="container no-entries" .dir=${pt(this._rtl)}>
          ${this.hass.localize("ui.components.logbook.entries_not_found")}
        </div>
      `}},{kind:"field",key:"_renderLogbookItem",value(){return(t,e)=>{if(!t||void 0===e)return p``;const a=[],i=this.entries[e-1],n=t.entity_id?this.hass.states[t.entity_id]:void 0,o=t.context_user_id&&this.userIdToName[t.context_user_id],r=t.entity_id?et(t.entity_id):t.domain;return p`
      <div class="entry-container">
        ${0===e||null!=t&&t.when&&null!=i&&i.when&&new Date(1e3*t.when).toDateString()!==new Date(1e3*i.when).toDateString()?p`
              <h4 class="date">
                ${Xe(new Date(1e3*t.when),this.hass.locale)}
              </h4>
            `:p``}

        <div class="entry ${u({"no-entity":!t.entity_id})}">
          <div class="icon-message">
            ${this.noIcon?"":p`
                  <state-badge
                    .hass=${this.hass}
                    .overrideIcon=${t.icon||(t.domain&&!n?ut(t.domain):void 0)}
                    .overrideImage=${mt.has(r)?"":(null==n?void 0:n.attributes.entity_picture_local)||(null==n?void 0:n.attributes.entity_picture)}
                    .stateObj=${n}
                    .stateColor=${!1}
                  ></state-badge>
                `}
            <div class="message-relative_time">
              <div class="message">
                ${this.noName?"":this._renderEntity(t.entity_id,t.name)}
                ${t.message?p`${this._formatMessageWithPossibleEntity(t.message,a,t.entity_id)}`:t.source?p` ${this._formatMessageWithPossibleEntity(t.source,a,void 0,"ui.components.logbook.by")}`:""}
                ${o?` ${this.hass.localize("ui.components.logbook.by_user")} ${o}`:""}
                ${t.context_event_type?this._formatEventBy(t,a):""}
                ${t.context_message?p` ${this._formatMessageWithPossibleEntity(t.context_message,a,t.context_entity_id,"ui.components.logbook.for")}`:""}
                ${t.context_entity_id&&!a.includes(t.context_entity_id)?p` ${this.hass.localize("ui.components.logbook.for")}
                    ${this._renderEntity(t.context_entity_id,t.context_entity_id_name)}`:""}
              </div>
              <div class="secondary">
                <span
                  >${Fa(new Date(1e3*t.when),this.hass.locale)}</span
                >
                -
                <ha-relative-time
                  .hass=${this.hass}
                  .datetime=${1e3*t.when}
                  capitalize
                ></ha-relative-time>
                ${["script","automation"].includes(t.domain)&&t.context_id in this.traceContexts?p`
                      -
                      <a
                        href=${`/config/${this.traceContexts[t.context_id].domain}/trace/${"script"===this.traceContexts[t.context_id].domain?`script.${this.traceContexts[t.context_id].item_id}`:this.traceContexts[t.context_id].item_id}?run_id=${this.traceContexts[t.context_id].run_id}`}
                        @click=${this._close}
                        >${this.hass.localize("ui.components.logbook.show_trace")}</a
                      >
                    `:""}
              </div>
            </div>
          </div>
        </div>
      </div>
    `}}},{kind:"method",decorators:[y({passive:!0})],key:"_saveScrollPos",value:function(t){this._savedScrollPos=t.target.scrollTop}},{kind:"method",key:"_formatEventBy",value:function(t,e){return"call_service"===t.context_event_type?`${this.hass.localize("ui.components.logbook.from_service")} ${t.context_domain}.${t.context_service}`:"automation_triggered"===t.context_event_type?e.includes(t.context_entity_id)?"":(e.push(t.context_entity_id),p`${this.hass.localize("ui.components.logbook.from_automation")}
      ${this._renderEntity(t.context_entity_id,t.context_name)}`):t.context_name?`${this.hass.localize("ui.components.logbook.from")} ${t.context_name}`:"state_changed"===t.context_event_type?"":t.context_event_type in di?`${this.hass.localize(`ui.components.logbook.${di[t.context_event_type]}`)}`:`${this.hass.localize("ui.components.logbook.from")} ${this.hass.localize("ui.components.logbook.event")} ${t.context_event_type}`}},{kind:"method",key:"_renderEntity",value:function(t,e){const a=t&&t in this.hass.states,i=e||a&&this.hass.states[t].attributes.friendly_name||t;return a?p`<button
      class="link"
      @click=${this._entityClicked}
      .entityId=${t}
    >
      ${i}
    </button>`:i}},{kind:"method",key:"_formatMessageWithPossibleEntity",value:function(t,e,a,i){if(-1!==t.indexOf(".")){const a=t.split(" ");for(let t=0,i=a.length;t<i;t++)if(a[t]in this.hass.states){const i=a[t];if(e.includes(i))return"";e.push(i);const n=a.splice(t);return n.shift(),p` ${a.join(" ")}
          ${this._renderEntity(i,this.hass.states[i].attributes.friendly_name)}
          ${n.join(" ")}`}}if(a&&a in this.hass.states){const n=this.hass.states[a].attributes.friendly_name;if(n&&t.endsWith(n))return e.includes(a)?"":(e.push(a),t=t.substring(0,t.length-n.length),p` ${i?this.hass.localize(i):""}
        ${t} ${this._renderEntity(a,n)}`)}return t}},{kind:"method",key:"_entityClicked",value:function(t){const e=t.currentTarget.entityId;e&&(t.preventDefault(),t.stopPropagation(),n(this,"hass-more-info",{entityId:e}))}},{kind:"method",key:"_close",value:function(){setTimeout((()=>n(this,"closed")),500)}},{kind:"get",static:!0,key:"styles",value:function(){return[$,j,F,f`
        :host([virtualize]) {
          display: block;
          height: 100%;
        }

        .rtl {
          direction: ltr;
        }

        .entry-container {
          width: 100%;
        }

        .entry {
          display: flex;
          width: 100%;
          line-height: 2em;
          padding: 8px 16px;
          box-sizing: border-box;
          border-top: 1px solid var(--divider-color);
        }

        .entry.no-entity,
        .no-name .entry {
          cursor: default;
        }

        .entry:hover {
          background-color: rgba(var(--rgb-primary-text-color), 0.04);
        }

        .narrow:not(.no-icon) .time {
          margin-left: 32px;
        }

        .message-relative_time {
          display: flex;
          flex-direction: column;
        }

        .secondary {
          font-size: 12px;
          line-height: 1.7;
        }

        .secondary a {
          color: var(--secondary-text-color);
        }

        .date {
          margin: 8px 0;
          padding: 0 16px;
        }

        .narrow .date {
          padding: 0 8px;
        }

        .rtl .date {
          direction: rtl;
        }

        .icon-message {
          display: flex;
          align-items: center;
        }

        .no-entries {
          text-align: center;
          color: var(--secondary-text-color);
        }

        state-badge {
          margin-right: 16px;
          flex-shrink: 0;
          color: var(--state-icon-color);
        }

        .message {
          color: var(--primary-text-color);
        }

        .no-name .message:first-letter {
          text-transform: capitalize;
        }

        a {
          color: var(--primary-color);
        }

        .container {
          max-height: var(--logbook-max-height);
        }

        .container,
        lit-virtualizer {
          height: 100%;
        }

        lit-virtualizer {
          contain: size layout !important;
        }

        .narrow .entry {
          line-height: 1.5;
          padding: 8px;
        }

        .narrow .icon-message state-badge {
          margin-left: 0;
        }
      `]}}]}}),I),T([g("ha-logbook")],(function(t,e){class a extends e{constructor(...e){super(...e),t(this)}}return{F:a,d:[{kind:"field",decorators:[d({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[d()],key:"time",value:void 0},{kind:"field",decorators:[d()],key:"entityId",value:void 0},{kind:"field",decorators:[d({type:Boolean,attribute:"narrow"})],key:"narrow",value:()=>!1},{kind:"field",decorators:[d({type:Boolean,attribute:"virtualize",reflect:!0})],key:"virtualize",value:()=>!1},{kind:"field",decorators:[d({type:Boolean,attribute:"no-icon"})],key:"noIcon",value:()=>!1},{kind:"field",decorators:[d({type:Boolean,attribute:"no-name"})],key:"noName",value:()=>!1},{kind:"field",decorators:[d({type:Boolean,attribute:"relative-time"})],key:"relativeTime",value:()=>!1},{kind:"field",decorators:[d({type:Boolean})],key:"showMoreLink",value:()=>!0},{kind:"field",decorators:[b()],key:"_logbookEntries",value:void 0},{kind:"field",decorators:[b()],key:"_traceContexts",value:void 0},{kind:"field",decorators:[b()],key:"_userIdToName",value:()=>({})},{kind:"field",decorators:[b()],key:"_error",value:void 0},{kind:"field",key:"_lastLogbookDate",value:void 0},{kind:"field",key:"_renderId",value:()=>1},{kind:"field",key:"_throttleGetLogbookEntries",value(){return Ia((()=>this._getLogBookData()),1e4)}},{kind:"method",key:"render",value:function(){return at(this.hass,"logbook")?this._error?p`<div class="no-entries">
        ${`${this.hass.localize("ui.components.logbook.retrieval_error")}: ${this._error}`}
      </div>`:void 0===this._logbookEntries?p`
        <div class="progress-wrapper">
          <ha-circular-progress
            active
            alt=${this.hass.localize("ui.common.loading")}
          ></ha-circular-progress>
        </div>
      `:0===this._logbookEntries.length?p`<div class="no-entries">
        ${this.hass.localize("ui.components.logbook.entries_not_found")}
      </div>`:p`
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
    `:p``}},{kind:"method",key:"refresh",value:async function(t=!1){var e,a;(t||void 0!==this._logbookEntries)&&(this._throttleGetLogbookEntries.cancel(),this._updateTraceContexts.cancel(),this._updateUsers.cancel(),"range"in this.time&&(e=this.time.range[0].toISOString(),a=this.time.range[1].toISOString(),oi[`${e}${a}`]={}),this._lastLogbookDate=void 0,this._logbookEntries=void 0,this._error=void 0,this._throttleGetLogbookEntries())}},{kind:"method",key:"updated",value:function(t){if(R(O(a.prototype),"updated",this).call(this,t),t.has("time")||t.has("entityId"))return void this.refresh(!0);if(!("recent"in this.time)||!t.has("hass")||!this.entityId)return;const e=t.get("hass");e&&!_t(this.entityId).some((t=>this.hass.states[t]!==(null==e?void 0:e.states[t])))||setTimeout(this._throttleGetLogbookEntries,1e3)}},{kind:"method",key:"_getLogBookData",value:async function(){this._renderId+=1;const t=this._renderId;let e,a,i=!1;"range"in this.time?[e,a]=this.time.range:(i=!0,e=this._lastLogbookDate||new Date((new Date).getTime()-864e5),a=new Date);const n=this.entityId?_t(this.entityId):void 0;let o;if(0===(null==n?void 0:n.length))o=[];else{var r;this._updateUsers(),null!==(r=this.hass.user)&&void 0!==r&&r.is_admin&&this._updateTraceContexts();try{o=await(async(t,e,a,i)=>{const n=await t.loadBackendTranslation("device_class");return ri(t,n,await si(t,e,a,i))})(this.hass,e.toISOString(),a.toISOString(),n?n.toString():void 0)}catch(e){return void(t===this._renderId&&(this._error=e.message))}}t===this._renderId&&(this._logbookEntries=i&&this._logbookEntries?o.concat(...this._logbookEntries):o,this._lastLogbookDate=a)}},{kind:"field",key:"_updateTraceContexts",value(){return Ia((async()=>{var t,e,a;this._traceContexts=await(t=this.hass,t.callWS({type:"trace/contexts",domain:e,item_id:a}))}),6e4)}},{kind:"field",key:"_updateUsers",value(){return Ia((async()=>{var t;const e={},a=(null===(t=this.hass.user)||void 0===t?void 0:t.is_admin)&&(async t=>t.callWS({type:"config/auth/list"}))(this.hass);for(const t of Object.values(this.hass.states))t.attributes.user_id&&"person"===ot(t)&&(e[t.attributes.user_id]=t.attributes.friendly_name);if(a){const t=await a;for(const a of t)a.id in e||(e[a.id]=a.name)}this._userIdToName=e}),6e4)}},{kind:"get",static:!0,key:"styles",value:function(){return[f`
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
      `]}}]}}),I),T([g("ha-more-info-logbook")],(function(t,e){class a extends e{constructor(...e){super(...e),t(this)}}return{F:a,d:[{kind:"field",decorators:[d({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[d()],key:"entityId",value:void 0},{kind:"field",key:"_showMoreHref",value:()=>""},{kind:"field",key:"_time",value:()=>({recent:86400})},{kind:"method",key:"render",value:function(){if(!at(this.hass,"logbook")||!this.entityId)return p``;return this.hass.states[this.entityId]?p`
      <div class="header">
        <div class="title">
          ${this.hass.localize("ui.dialogs.more_info_control.logbook")}
        </div>
        <a href=${this._showMoreHref} @click=${this._close}
          >${this.hass.localize("ui.dialogs.more_info_control.show_more")}</a
        >
      </div>
      <ha-logbook
        .hass=${this.hass}
        .time=${this._time}
        .entityId=${this.entityId}
        narrow
        no-icon
        no-name
        relative-time
      ></ha-logbook>
    `:p``}},{kind:"method",key:"willUpdate",value:function(t){R(O(a.prototype),"willUpdate",this).call(this,t),t.has("entityId")&&this.entityId&&(this._showMoreHref=`/logbook?entity_id=${this.entityId}&start_date=${Ta().toISOString()}`)}},{kind:"method",key:"_close",value:function(){setTimeout((()=>n(this,"closed")),500)}},{kind:"get",static:!0,key:"styles",value:function(){return[f`
        ha-logbook {
          --logbook-max-height: 250px;
        }
        @media all and (max-width: 450px), all and (max-height: 500px) {
          ha-logbook {
            --logbook-max-height: unset;
          }
        }
        .header {
          display: flex;
          flex-direction: row;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 8px;
        }
        .header > a,
        a:visited {
          color: var(--primary-color);
        }
        .title {
          font-family: var(--paper-font-title_-_font-family);
          -webkit-font-smoothing: var(
            --paper-font-title_-_-webkit-font-smoothing
          );
          font-size: var(--paper-font-subhead_-_font-size);
          font-weight: var(--paper-font-title_-_font-weight);
          letter-spacing: var(--paper-font-title_-_letter-spacing);
          line-height: var(--paper-font-title_-_line-height);
        }
      `]}}]}}),I);customElements.define("state-card-toggle",class extends z{static get template(){return D`
      <style include="iron-flex iron-flex-alignment"></style>
      <style>
        ha-entity-toggle {
          margin: -4px -16px -4px 0;
          padding: 4px 16px;
        }
      </style>

      <div class="horizontal justified layout">
        ${this.stateInfoTemplate}
        <ha-entity-toggle
          state-obj="[[stateObj]]"
          hass="[[hass]]"
        ></ha-entity-toggle>
      </div>
    `}static get stateInfoTemplate(){return D`
      <state-info
        hass="[[hass]]"
        state-obj="[[stateObj]]"
        in-dialog="[[inDialog]]"
      ></state-info>
    `}static get properties(){return{hass:Object,stateObj:Object,inDialog:{type:Boolean,value:!1}}}});let hi=T([g("react-more-info-dialog")],(function(t,e){return{F:class extends e{constructor(...e){super(...e),t(this)}},d:[{kind:"field",decorators:[d({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[d({type:Boolean,reflect:!0})],key:"large",value:()=>!1},{kind:"field",decorators:[b()],key:"_entityId",value:void 0},{kind:"field",decorators:[b()],key:"_currTabIndex",value:()=>0},{kind:"method",key:"showDialog",value:function(t){this._entityId=t.entityId,this._entityId?this.large=!1:this.closeDialog()}},{kind:"method",key:"closeDialog",value:function(){this._entityId=void 0,this._currTabIndex=0,n(this,"dialog-closed",{dialog:this.localName})}},{kind:"method",key:"render",value:function(){if(!this._entityId)return p``;const t=this._entityId,e=this.hass.states[t];if(!e)return p``;const a=J(e);return p`
            <ha-dialog
                open
                @closed=${this.closeDialog}
                .heading=${a}
                hideActions
                data-domain=${"react"}
            >
                <div slot="heading" class="heading">
                    <ha-header-bar>
                        <ha-icon-button
                            slot="navigationIcon"
                            dialogAction="cancel"
                            .label=${this.hass.localize("ui.dialogs.more_info_control.dismiss")}
                            .path=${P}
                        ></ha-icon-button>
                        <div
                            slot="title"
                            class="main-title"
                            .title=${a}
                            @click=${this._enlarge}
                        >
                            ${a}
                        </div>
                        ${this.hass.user.is_admin?p`
                                <ha-icon-button
                                    slot="actionItems"
                                    .label=${this.hass.localize("ui.dialogs.more_info_control.settings")}
                                    .path=${B}
                                    @click=${this._gotoSettings}
                                ></ha-icon-button>
                                `:""}
                    </ha-header-bar>
                    <mwc-tab-bar
                        .activeIndex=${this._currTabIndex}
                        @MDCTabBar:activated=${this._handleTabChanged}
                    >
                        <mwc-tab
                            .label=${this.hass.localize("ui.dialogs.more_info_control.details")}
                            dialogInitialFocus
                        ></mwc-tab>
                        <mwc-tab
                            .label=${this.hass.localize("ui.dialogs.more_info_control.history")}
                        ></mwc-tab>
                    </mwc-tab-bar>
                </div>

                <div class="content" tabindex="-1" dialogInitialFocus>
                    ${kt(0===this._currTabIndex?p`
                            <react-state-card-content
                                in-dialog
                                .stateObj=${e}
                                .hass=${this.hass}
                            ></react-state-card-content>
                            <react-workflow-more-info
                                .stateObj=${e}
                                .hass=${this.hass}
                            ></react-workflow-more-info>
                            ${e.attributes.restored?p`
                                    <p>
                                        ${this.hass.localize("ui.dialogs.more_info_control.restored.not_provided")}
                                    </p>
                                    <p>
                                        ${this.hass.localize("ui.dialogs.more_info_control.restored.remove_intro")}
                                    </p>
                                    <mwc-button
                                        class="warning"
                                        @click=${this._removeEntity}
                                    >
                                        ${this.hass.localize("ui.dialogs.more_info_control.restored.remove_action")}
                                    </mwc-button>
                                `:""}
                            `:p`
                            ${this._computeShowHistoryComponent()?p`
                                <ha-more-info-history
                                    .hass=${this.hass}
                                    .entityId=${this._entityId}
                                ></ha-more-info-history>`:""}
                            ${this._computeShowLogBookComponent(t)?p`
                                <ha-more-info-logbook
                                    .hass=${this.hass}
                                    .entityId=${this._entityId}
                                ></ha-more-info-logbook>`:""}
                            `)}
                </div>
            </ha-dialog>
        `}},{kind:"method",key:"_enlarge",value:function(){this.large=!this.large}},{kind:"method",key:"_computeShowHistoryComponent",value:function(){return at(this.hass,"history")}},{kind:"method",key:"_computeShowLogBookComponent",value:function(t){if(!at(this.hass,"logbook"))return!1;return!!this.hass.states[t]}},{kind:"method",key:"_removeEntity",value:function(){const t=this._entityId;ft(this,{title:this.hass.localize("ui.dialogs.more_info_control.restored.confirm_remove_title"),text:this.hass.localize("ui.dialogs.more_info_control.restored.confirm_remove_text"),confirmText:this.hass.localize("ui.common.remove"),dismissText:this.hass.localize("ui.common.cancel"),confirm:()=>{gt(this.hass,t)}})}},{kind:"method",key:"_gotoSettings",value:function(){var t,e;H(this),t=this,e={entity_id:this._entityId},n(t,"show-dialog",{dialogTag:"dialog-entity-editor",dialogImport:xt,dialogParams:e}),this.closeDialog()}},{kind:"method",key:"_handleTabChanged",value:function(t){t.detail.index!==this._currTabIndex&&(this._currTabIndex=t.detail.index)}},{kind:"get",static:!0,key:"styles",value:function(){return[G,f`
                ha-dialog {
                    --dialog-surface-position: static;
                    --dialog-content-position: static;
                }

                ha-header-bar {
                    --mdc-theme-on-primary: var(--primary-text-color);
                    --mdc-theme-primary: var(--mdc-theme-surface);
                    flex-shrink: 0;
                    display: block;
                }
                .content {
                    outline: none;
                }
                @media all and (max-width: 450px), all and (max-height: 500px) {
                    ha-header-bar {
                        --mdc-theme-primary: var(--app-header-background-color);
                        --mdc-theme-on-primary: var(--app-header-text-color, white);
                        border-bottom: none;
                    }
                }

                .heading {
                    border-bottom: 1px solid
                    var(--mdc-dialog-scroll-divider-color, rgba(0, 0, 0, 0.12));
                }

                @media all and (min-width: 451px) and (min-height: 501px) {
                    ha-dialog {
                        --mdc-dialog-max-width: 90vw;
                    }

                    .content {
                        width: 352px;
                    }

                    ha-header-bar {
                        width: 400px;
                    }

                    .main-title {
                        overflow: hidden;
                        text-overflow: ellipsis;
                        cursor: default;
                    }

                    :host([large]) .content {
                        width: calc(90vw - 48px);
                    }

                    :host([large]) ha-dialog[data-domain="camera"] .content,
                    :host([large]) ha-header-bar {
                        width: 90vw;
                    }
                }

                react-state-card-content,
                ha-more-info-history,
                ha-more-info-logbook:not(:last-child) {
                    display: block;
                    margin-bottom: 16px;
                }
            `]}}]}}),I);var pi=Object.freeze({__proto__:null,ReactMoreInfoDialog:hi});export{Oe as a,Le as b,Xe as c,kt as d,Je as e,ia as f,ea as g,Ze as h,Re as i,Ve as j,Na as k,ke as l,Fa as m,la as n,ra as o,pi as r};

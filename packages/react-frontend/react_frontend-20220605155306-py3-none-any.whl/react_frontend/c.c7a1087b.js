import{cj as t,ck as e,d4 as i,cl as a,cm as s,_ as n,s as r,e as o,t as l,aw as d,ax as h,$ as c,f as m,ap as u,n as p,cy as _,d5 as y,cQ as g,cR as f}from"./main-4b1ba1ae.js";import{d as b}from"./c.9d135c84.js";import{c as v,I as k}from"./c.f8815787.js";import"./c.f7a407a1.js";import{S as $,s as w,a as x,f as I}from"./c.57301488.js";import"./c.dc4d7ad9.js";import"./c.dd8bad78.js";import"./c.8d0ef0b0.js";const T=t(class extends e{constructor(t){if(super(t),i(this,"_element",void 0),t.type!==a.CHILD)throw new Error("dynamicElementDirective can only be used in content bindings")}update(t,[e,i]){return this._element&&this._element.localName===e?(i&&Object.entries(i).forEach((([t,e])=>{this._element[t]=e})),s):this.render(e,i)}render(t,e){return this._element=document.createElement(t),e&&Object.entries(e).forEach((([t,e])=>{this._element[t]=e})),this._element}});n([p("ha-related-items")],(function(t,e){class i extends e{constructor(...e){super(...e),t(this)}}return{F:i,d:[{kind:"field",decorators:[o({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[o()],key:"itemType",value:void 0},{kind:"field",decorators:[o()],key:"itemId",value:void 0},{kind:"field",decorators:[l()],key:"_entries",value:void 0},{kind:"field",decorators:[l()],key:"_devices",value:void 0},{kind:"field",decorators:[l()],key:"_areas",value:void 0},{kind:"field",decorators:[l()],key:"_related",value:void 0},{kind:"method",key:"hassSubscribe",value:function(){return[w(this.hass.connection,(t=>{this._devices=t})),x(this.hass.connection,(t=>{this._areas=t}))]}},{kind:"method",key:"firstUpdated",value:function(t){d(h(i.prototype),"firstUpdated",this).call(this,t),((t,e)=>{const i=new URLSearchParams;return e&&(e.type&&i.append("type",e.type),e.domain&&i.append("domain",e.domain)),t.callApi("GET",`config/config_entries/entry?${i.toString()}`)})(this.hass).then((t=>{this._entries=t})),this.hass.loadBackendTranslation("title")}},{kind:"method",key:"updated",value:function(t){d(h(i.prototype),"updated",this).call(this,t),(t.has("itemId")||t.has("itemType"))&&this.itemId&&this.itemType&&this._findRelated()}},{kind:"method",key:"render",value:function(){return this._related?0===Object.keys(this._related).length?c`
        ${this.hass.localize("ui.components.related-items.no_related_found")}
      `:c`
      ${this._related.config_entry&&this._entries?this._related.config_entry.map((t=>{const e=this._entries.find((e=>e.entry_id===t));return e?c`
              <h3>
                ${this.hass.localize("ui.components.related-items.integration")}:
              </h3>
              <a
                href=${`/config/integrations#config_entry=${t}`}
                @click=${this._navigateAwayClose}
              >
                ${this.hass.localize(`component.${e.domain}.title`)}:
                ${e.title}
              </a>
            `:""})):""}
      ${this._related.device&&this._devices?this._related.device.map((t=>{const e=this._devices.find((e=>e.id===t));return e?c`
              <h3>
                ${this.hass.localize("ui.components.related-items.device")}:
              </h3>
              <a
                href="/config/devices/device/${t}"
                @click=${this._navigateAwayClose}
              >
                ${e.name_by_user||e.name}
              </a>
            `:""})):""}
      ${this._related.area&&this._areas?this._related.area.map((t=>{const e=this._areas.find((e=>e.area_id===t));return e?c`
              <h3>
                ${this.hass.localize("ui.components.related-items.area")}:
              </h3>
              <a
                href="/config/areas/area/${t}"
                @click=${this._navigateAwayClose}
              >
                ${e.name}
              </a>
            `:""})):""}
      ${this._related.entity?c`
            <h3>
              ${this.hass.localize("ui.components.related-items.entity")}:
            </h3>
            <ul>
              ${this._related.entity.map((t=>{const e=this.hass.states[t];return e?c`
                  <li>
                    <button
                      @click=${this._openMoreInfo}
                      .entityId=${t}
                      class="link"
                    >
                      ${e.attributes.friendly_name||t}
                    </button>
                  </li>
                `:""}))}
            </ul>
          `:""}
      ${this._related.group?c`
            <h3>${this.hass.localize("ui.components.related-items.group")}:</h3>
            <ul>
              ${this._related.group.map((t=>{const e=this.hass.states[t];return e?c`
                  <li>
                    <button
                      class="link"
                      @click=${this._openMoreInfo}
                      .entityId=${t}
                    >
                      ${e.attributes.friendly_name||e.entity_id}
                    </button>
                  </li>
                `:""}))}
            </ul>
          `:""}
      ${this._related.scene?c`
            <h3>${this.hass.localize("ui.components.related-items.scene")}:</h3>
            <ul>
              ${this._related.scene.map((t=>{const e=this.hass.states[t];return e?c`
                  <li>
                    <button
                      class="link"
                      @click=${this._openMoreInfo}
                      .entityId=${t}
                    >
                      ${e.attributes.friendly_name||e.entity_id}
                    </button>
                  </li>
                `:""}))}
            </ul>
          `:""}
      ${this._related.automation?c`
            <h3>
              ${this.hass.localize("ui.components.related-items.automation")}:
            </h3>
            <ul>
              ${this._related.automation.map((t=>{const e=this.hass.states[t];return e?c`
                  <li>
                    <button
                      class="link"
                      @click=${this._openMoreInfo}
                      .entityId=${t}
                    >
                      ${e.attributes.friendly_name||e.entity_id}
                    </button>
                  </li>
                `:""}))}
            </ul>
          `:""}
      ${this._related.script?c`
            <h3>
              ${this.hass.localize("ui.components.related-items.script")}:
            </h3>
            <ul>
              ${this._related.script.map((t=>{const e=this.hass.states[t];return e?c`
                  <li>
                    <button
                      class="link"
                      @click=${this._openMoreInfo}
                      .entityId=${t}
                    >
                      ${e.attributes.friendly_name||e.entity_id}
                    </button>
                  </li>
                `:""}))}
            </ul>
          `:""}
    `:c``}},{kind:"method",key:"_navigateAwayClose",value:async function(){await new Promise((t=>setTimeout(t,0))),m(this,"close-dialog")}},{kind:"method",key:"_findRelated",value:async function(){this._related=await I(this.hass,this.itemType,this.itemId),await this.updateComplete,m(this,"iron-resize")}},{kind:"method",key:"_openMoreInfo",value:function(t){const e=t.target.entityId;m(this,"hass-more-info",{entityId:e})}},{kind:"get",static:!0,key:"styles",value:function(){return u`
      a {
        color: var(--primary-color);
      }
      button.link {
        color: var(--primary-color);
        text-align: left;
        cursor: pointer;
        background: none;
        border-width: initial;
        border-style: none;
        border-color: initial;
        border-image: initial;
        padding: 0px;
        font: inherit;
        text-decoration: underline;
      }
      h3 {
        font-family: var(--paper-font-title_-_font-family);
        -webkit-font-smoothing: var(
          --paper-font-title_-_-webkit-font-smoothing
        );
        font-size: var(--paper-font-title_-_font-size);
        font-weight: var(--paper-font-headline-_font-weight);
        letter-spacing: var(--paper-font-title_-_letter-spacing);
        line-height: var(--paper-font-title_-_line-height);
        opacity: var(--dark-primary-opacity);
      }
    `}}]}}),$(r));const z={input_number:"entity-settings-helper-tab",input_select:"entity-settings-helper-tab",input_text:"entity-settings-helper-tab",input_boolean:"entity-settings-helper-tab",input_datetime:"entity-settings-helper-tab",counter:"entity-settings-helper-tab",timer:"entity-settings-helper-tab",input_button:"entity-settings-helper-tab"};let j=n([p("dialog-entity-editor")],(function(t,e){return{F:class extends e{constructor(...e){super(...e),t(this)}},d:[{kind:"field",decorators:[o({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[l()],key:"_params",value:void 0},{kind:"field",decorators:[l()],key:"_entry",value:void 0},{kind:"field",decorators:[l()],key:"_curTab",value:()=>"tab-settings"},{kind:"field",decorators:[l()],key:"_extraTabs",value:()=>({})},{kind:"field",decorators:[l()],key:"_settingsElementTag",value:void 0},{kind:"field",key:"_curTabIndex",value:()=>0},{kind:"method",key:"showDialog",value:function(t){this._params=t,this._entry=void 0,this._settingsElementTag=void 0,this._extraTabs={},this._getEntityReg()}},{kind:"method",key:"closeDialog",value:function(){this._params=void 0,m(this,"dialog-closed",{dialog:this.localName})}},{kind:"method",key:"render",value:function(){if(!this._params||void 0===this._entry)return c``;const t=this._params.entity_id,e=this._entry,i=this.hass.states[t];return c`
      <ha-dialog
        open
        .heading=${i?v(i):(null==e?void 0:e.name)||t}
        hideActions
        @closed=${this.closeDialog}
        @close-dialog=${this.closeDialog}
      >
        <div slot="heading">
          <ha-header-bar>
            <ha-icon-button
              slot="navigationIcon"
              .label=${this.hass.localize("ui.dialogs.entity_registry.dismiss")}
              .path=${_}
              dialogAction="cancel"
            ></ha-icon-button>
            <span slot="title">
              ${i?v(i):(null==e?void 0:e.name)||t}
            </span>
            ${i?c`
                  <ha-icon-button
                    slot="actionItems"
                    .label=${this.hass.localize("ui.dialogs.entity_registry.control")}
                    .path=${y}
                    @click=${this._openMoreInfo}
                  ></ha-icon-button>
                `:""}
          </ha-header-bar>
          <mwc-tab-bar
            .activeIndex=${this._curTabIndex}
            @MDCTabBar:activated=${this._handleTabActivated}
            @MDCTab:interacted=${this._handleTabInteracted}
          >
            <mwc-tab
              id="tab-settings"
              .label=${this.hass.localize("ui.dialogs.entity_registry.settings")}
              dialogInitialFocus
            >
            </mwc-tab>
            ${Object.entries(this._extraTabs).map((([t,e])=>c`
                <mwc-tab
                  id=${t}
                  .label=${this.hass.localize(e.translationKey)||t}
                >
                </mwc-tab>
              `))}
            <mwc-tab
              id="tab-related"
              .label=${this.hass.localize("ui.dialogs.entity_registry.related")}
            >
            </mwc-tab>
          </mwc-tab-bar>
        </div>
        <div class="wrapper">${b(this._renderTab())}</div>
      </ha-dialog>
    `}},{kind:"method",key:"_renderTab",value:function(){switch(this._curTab){case"tab-settings":return this._entry?this._settingsElementTag?c`
              ${T(this._settingsElementTag,{hass:this.hass,entry:this._entry,entityId:this._params.entity_id})}
            `:c``:c`
          <div class="content">
            ${this.hass.localize("ui.dialogs.entity_registry.no_unique_id","entity_id",this._params.entity_id,"faq_link",c`<a
                href=${t=this.hass,e="/faq/unique_id",`https://${t.config.version.includes("b")?"rc":t.config.version.includes("dev")?"next":"www"}.home-assistant.io${e}`}
                target="_blank"
                rel="noreferrer"
                >${this.hass.localize("ui.dialogs.entity_registry.faq")}</a
              >`)}
          </div>
        `;case"tab-related":return c`
          <ha-related-items
            class="content"
            .hass=${this.hass}
            .itemId=${this._params.entity_id}
            itemType="entity"
          ></ha-related-items>
        `;default:return c``}var t,e}},{kind:"method",key:"_getEntityReg",value:async function(){try{this._entry=await k(this.hass,this._params.entity_id),this._loadPlatformSettingTabs()}catch{this._entry=null}}},{kind:"method",key:"_handleTabActivated",value:function(t){this._curTabIndex=t.detail.index}},{kind:"method",key:"_handleTabInteracted",value:function(t){this._curTab=t.detail.tabId}},{kind:"method",key:"_loadPlatformSettingTabs",value:async function(){if(!this._entry)return;if(!Object.keys(z).includes(this._entry.platform))return void(this._settingsElementTag="entity-registry-settings");const t=z[this._entry.platform];await import(`./editor-tabs/settings/${t}`),this._settingsElementTag=t}},{kind:"method",key:"_openMoreInfo",value:function(){g(this),m(this,"hass-more-info",{entityId:this._params.entity_id}),this.closeDialog()}},{kind:"get",static:!0,key:"styles",value:function(){return[f,u`
        ha-header-bar {
          --mdc-theme-on-primary: var(--primary-text-color);
          --mdc-theme-primary: var(--mdc-theme-surface);
          flex-shrink: 0;
        }

        mwc-tab-bar {
          border-bottom: 1px solid
            var(--mdc-dialog-scroll-divider-color, rgba(0, 0, 0, 0.12));
        }

        ha-dialog {
          --dialog-content-position: static;
          --dialog-content-padding: 0;
          --dialog-z-index: 6;
        }

        @media all and (min-width: 451px) and (min-height: 501px) {
          .wrapper {
            min-width: 400px;
          }
        }

        .content {
          display: block;
          padding: 20px 24px;
        }

        /* overrule the ha-style-dialog max-height on small screens */
        @media all and (max-width: 450px), all and (max-height: 500px) {
          ha-header-bar {
            --mdc-theme-primary: var(--app-header-background-color);
            --mdc-theme-on-primary: var(--app-header-text-color, white);
          }
        }

        mwc-button.warning {
          --mdc-theme-primary: var(--error-color);
        }

        :host([rtl]) app-toolbar {
          direction: rtl;
          text-align: right;
        }
      `]}}]}}),r);export{j as DialogEntityEditor};

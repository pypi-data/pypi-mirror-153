import{_ as e,s as t,e as i,t as a,m as r,$ as o,r as s,f as l,h as d,n,a as c,b as h,c as u,d as w,H as k}from"./main-4b1ba1ae.js";import{c as f,U as v,d as _,a as g}from"./c.f8815787.js";import{f as b}from"./c.4ebc1e89.js";import{t as p}from"./c.dd8bad78.js";import"./c.57301488.js";e([n("react-workflow-panel")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[i({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[i({attribute:!1})],key:"react",value:void 0},{kind:"field",decorators:[i()],key:"route",value:void 0},{kind:"field",decorators:[i({type:Boolean})],key:"narrow",value:void 0},{kind:"field",decorators:[i({type:Boolean})],key:"isWide",value:void 0},{kind:"field",decorators:[i({type:Boolean})],key:"showAdvanced",value:void 0},{kind:"field",decorators:[i()],key:"workflows",value:void 0},{kind:"field",decorators:[i()],key:"_activeFilters",value:void 0},{kind:"field",decorators:[a()],key:"_filteredWorkflows",value:void 0},{kind:"field",decorators:[a()],key:"_filterValue",value:void 0},{kind:"field",key:"_workflows",value:()=>r(((e,t)=>null===t?[]:(t?e.filter((e=>t.includes(e.entity_id))):e).map((e=>({...e,name:f(e),last_triggered:e.attributes.last_triggered||void 0})))))},{kind:"field",key:"_columns",value(){return r(((e,t)=>{const i={toggle:{title:"",label:this.react.localize("ui.panel.workflow.picker.headers.toggle"),type:"icon",template:(e,t)=>o`
                        <ha-entity-toggle
                        .hass=${this.hass}
                        .stateObj=${t}
                        ></ha-entity-toggle>
                    `},name:{title:this.react.localize("ui.panel.workflow.picker.headers.name"),sortable:!0,filterable:!0,direction:"asc",grows:!0,template:e?(e,t)=>o`
                            ${e}
                            <div class="secondary">
                            ${this.react.localize("ui.card.workflow.last_triggered")}:
                            ${t.attributes.last_triggered?b(new Date(t.attributes.last_triggered),this.hass.locale):this.react.localize("ui.components.relative_time.never")}
                            </div>
                        `:void 0}};return e||(i.last_triggered={sortable:!0,width:"20%",title:this.react.localize("ui.card.workflow.last_triggered"),template:e=>o`
                    ${e?b(new Date(e),this.hass.locale):this.react.localize("ui.components.relative_time.never")}
                    `},i.trigger={label:this.react.localize("ui.panel.workflow.picker.headers.trigger"),title:o`
                    <mwc-button style="visibility: hidden">
                        ${this.react.localize("ui.card.workflow.trigger")}
                    </mwc-button>
                    `,width:"20%",template:(e,t)=>o`
                    <mwc-button
                        .workflow=${t}
                        @click=${this._triggerRunActions}
                        .disabled=${v.includes(t.state)}
                    >
                        ${this.react.localize("ui.card.workflow.trigger")}
                    </mwc-button>
                    `}),i.actions={title:"",label:this.react.localize("ui.panel.workflow.picker.headers.actions"),type:"overflow-menu",template:(e,t)=>o`
                    <ha-icon-overflow-menu
                    .hass=${this.hass}
                    .narrow=${this.narrow}
                    .items=${[{path:c,label:this.react.localize("ui.panel.workflow.picker.show_info_workflow"),action:()=>this._showInfo(t)},{path:h,label:this.react.localize("ui.card.workflow.trigger"),narrowOnly:!0,action:()=>this._runActions(t)},{path:u,disabled:!t.attributes.workflow_id,label:this.react.localize("ui.panel.workflow.picker.trace"),action:()=>{t.attributes.workflow_id&&w(`/react/workflow/trace/${t.attributes.workflow_id}`)}}]}
                    style="color: var(--secondary-text-color)"
                    >
                    </ha-icon-overflow-menu>
                `},i}))}},{kind:"method",key:"render",value:function(){return o`
        <hass-tabs-subpage-data-table
            .hass=${this.hass}
            .narrow=${this.narrow}
            back-path="/react"
            id="entity_id"
            .route=${this.route}
            .tabs=${s.react}
            .activeFilters=${this._activeFilters}
            .columns=${this._columns(this.narrow,this.hass.locale)}
            .data=${this._workflows(this.workflows,this._filteredWorkflows)}
            .noDataText=${this.react.localize("ui.panel.workflow.picker.no_workflows")}
            @clear-filter=${this._clearFilter}
        >
            <ha-button-related-filter-menu
                slot="filter-menu"
                corner="BOTTOM_START"
                .narrow=${this.narrow}
                .hass=${this.hass}
                .value=${this._filterValue}
                exclude-domains='["workflow"]'
                @related-changed=${this._relatedFilterChanged}
            >
            </ha-button-related-filter-menu>
        </hass-tabs-subpage-data-table>
      `}},{kind:"method",key:"_relatedFilterChanged",value:function(e){this._filterValue=e.detail.value,this._filterValue?(this._activeFilters=[e.detail.filter],this._filteredWorkflows=e.detail.items.workflow||null):this._clearFilter()}},{kind:"method",key:"_clearFilter",value:function(){this._filteredWorkflows=void 0,this._activeFilters=void 0,this._filterValue=void 0}},{kind:"method",key:"_showInfo",value:function(e){const t=e.entity_id;l(this,"hass-more-info",{entityId:t})}},{kind:"field",key:"_triggerRunActions",value(){return e=>{this._runActions(e.currentTarget.workflow)}}},{kind:"field",key:"_runActions",value(){return e=>{p(this.hass,e.entity_id)}}},{kind:"get",static:!0,key:"styles",value:function(){return d}}]}}),t);e([n("react-workflow-router")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[i({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[i({attribute:!1})],key:"react",value:void 0},{kind:"field",decorators:[i()],key:"isWide",value:void 0},{kind:"field",decorators:[i()],key:"narrow",value:void 0},{kind:"field",decorators:[i()],key:"showAdvanced",value:void 0},{kind:"field",key:"_debouncedUpdateWorkflows",value(){return _((e=>{const t=this._getWorkflows(this.hass.states);var i,a;i=t,a=e.workflows,i.length===a.length&&i.every(((e,t)=>e===a[t]))||(e.workflows=t)}),10)}},{kind:"field",key:"routerOptions",value:()=>({defaultPage:"dashboard",routes:{dashboard:{tag:"react-workflow-panel",cache:!0},trace:{tag:"react-workflow-trace",load:()=>import("./c.473886a6.js")}}})},{kind:"field",key:"_getWorkflows",value:()=>r((e=>Object.values(e).filter((e=>"react"===g(e)&&!e.attributes.restored))))},{kind:"method",key:"updatePageEl",value:function(e,t){if(e.hass=this.hass,e.react=this.react,e.route=this.routeTail,e.narrow=this.narrow,e.isWide=this.isWide,e.showAdvanced=this.showAdvanced,this.hass&&(e.workflows&&t?t.has("hass")&&this._debouncedUpdateWorkflows(e):e.workflows=this._getWorkflows(this.hass.states)),(!t||t.has("route"))&&"dashboard"!==this._currentPage){const t=decodeURIComponent(this.routeTail.path.substr(1));e.workflowId="new"===t?null:t}}}]}}),k);

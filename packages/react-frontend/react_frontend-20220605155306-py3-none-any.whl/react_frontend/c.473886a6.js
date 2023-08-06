import{ap as e,_ as t,cN as r,e as a,t as i,aw as o,ax as d,m as s,f as n,n as c,s as l,$ as h,cT as u,ao as v,cU as k,cV as p,X as f,cW as g,cy as _,cX as b,cY as y,cM as m,an as $,cZ as w,c_ as x,r as N,c$ as C,d0 as M,d1 as I,d2 as S,h as T}from"./main-4b1ba1ae.js";import{H as E,g as O}from"./c.f8815787.js";import{d as B}from"./c.df145067.js";import{a as j}from"./c.4ebc1e89.js";import{e as F}from"./c.8d0ef0b0.js";import"./c.57301488.js";const P=e`
  .tabs {
    background-color: var(--primary-background-color);
    border-top: 1px solid var(--divider-color);
    border-bottom: 1px solid var(--divider-color);
    display: flex;
    padding-left: 4px;
  }

  .tabs.top {
    border-top: none;
  }

  .tabs > * {
    padding: 2px 16px;
    cursor: pointer;
    position: relative;
    bottom: -1px;
    border: none;
    border-bottom: 2px solid transparent;
    user-select: none;
    background: none;
    color: var(--primary-text-color);
    outline: none;
    transition: background 15ms linear;
  }

  .tabs > *.active {
    border-bottom-color: var(--accent-color);
  }

  .tabs > *:focus,
  .tabs > *:hover {
    background: var(--secondary-background-color);
  }
`;let z;const L={key:"Mod-s",run:e=>(n(e.dom,"editor-save"),!0)};t([c("ha-code-editor")],(function(t,r){class c extends r{constructor(...e){super(...e),t(this)}}return{F:c,d:[{kind:"field",key:"codemirror",value:void 0},{kind:"field",decorators:[a()],key:"mode",value:()=>"yaml"},{kind:"field",key:"hass",value:void 0},{kind:"field",decorators:[a({type:Boolean})],key:"autofocus",value:()=>!1},{kind:"field",decorators:[a({type:Boolean})],key:"readOnly",value:()=>!1},{kind:"field",decorators:[a({type:Boolean,attribute:"autocomplete-entities"})],key:"autocompleteEntities",value:()=>!1},{kind:"field",decorators:[a()],key:"error",value:()=>!1},{kind:"field",decorators:[i()],key:"_value",value:()=>""},{kind:"field",key:"_loadedCodeMirror",value:void 0},{kind:"set",key:"value",value:function(e){this._value=e}},{kind:"get",key:"value",value:function(){return this.codemirror?this.codemirror.state.doc.toString():this._value}},{kind:"get",key:"hasComments",value:function(){if(!this.codemirror||!this._loadedCodeMirror)return!1;const e=this._loadedCodeMirror.HighlightStyle.get(this.codemirror.state,this._loadedCodeMirror.tags.comment);return!!this.shadowRoot.querySelector(`span.${e}`)}},{kind:"method",key:"connectedCallback",value:function(){o(d(c.prototype),"connectedCallback",this).call(this),this.codemirror&&!1!==this.autofocus&&this.codemirror.focus()}},{kind:"method",key:"update",value:function(e){o(d(c.prototype),"update",this).call(this,e),this.codemirror&&(e.has("mode")&&this.codemirror.dispatch({effects:this._loadedCodeMirror.langCompartment.reconfigure(this._mode)}),e.has("readOnly")&&this.codemirror.dispatch({effects:this._loadedCodeMirror.readonlyCompartment.reconfigure(this._loadedCodeMirror.EditorView.editable.of(!this.readOnly))}),e.has("_value")&&this._value!==this.value&&this.codemirror.dispatch({changes:{from:0,to:this.codemirror.state.doc.length,insert:this._value}}),e.has("error")&&this.classList.toggle("error-state",this.error))}},{kind:"method",key:"firstUpdated",value:function(e){o(d(c.prototype),"firstUpdated",this).call(this,e),this._blockKeyboardShortcuts(),this._load()}},{kind:"get",key:"_mode",value:function(){return this._loadedCodeMirror.langs[this.mode]}},{kind:"method",key:"_load",value:async function(){this._loadedCodeMirror=await(async()=>(z||(z=import("./c.f078256c.js")),z))();const e=[this._loadedCodeMirror.lineNumbers(),this._loadedCodeMirror.EditorState.allowMultipleSelections.of(!0),this._loadedCodeMirror.history(),this._loadedCodeMirror.highlightSelectionMatches(),this._loadedCodeMirror.highlightActiveLine(),this._loadedCodeMirror.drawSelection(),this._loadedCodeMirror.rectangularSelection(),this._loadedCodeMirror.keymap.of([...this._loadedCodeMirror.defaultKeymap,...this._loadedCodeMirror.searchKeymap,...this._loadedCodeMirror.historyKeymap,...this._loadedCodeMirror.tabKeyBindings,L]),this._loadedCodeMirror.langCompartment.of(this._mode),this._loadedCodeMirror.theme,this._loadedCodeMirror.Prec.fallback(this._loadedCodeMirror.highlightStyle),this._loadedCodeMirror.readonlyCompartment.of(this._loadedCodeMirror.EditorView.editable.of(!this.readOnly)),this._loadedCodeMirror.EditorView.updateListener.of((e=>this._onUpdate(e)))];!this.readOnly&&this.autocompleteEntities&&this.hass&&e.push(this._loadedCodeMirror.autocompletion({override:[this._entityCompletions.bind(this)],maxRenderedOptions:10})),this.codemirror=new this._loadedCodeMirror.EditorView({state:this._loadedCodeMirror.EditorState.create({doc:this._value,extensions:e}),root:this.shadowRoot,parent:this.shadowRoot})}},{kind:"field",key:"_getStates",value:()=>s((e=>{if(!e)return[];return Object.keys(e).map((t=>({type:"variable",label:t,detail:e[t].attributes.friendly_name,info:`State: ${e[t].state}`})))}))},{kind:"method",key:"_entityCompletions",value:function(e){const t=e.matchBefore(/[a-z_]{3,}\./);if(!t||t.from===t.to&&!e.explicit)return null;const r=this._getStates(this.hass.states);return r&&r.length?{from:Number(t.from),options:r,span:/^\w*.\w*$/}:null}},{kind:"method",key:"_blockKeyboardShortcuts",value:function(){this.addEventListener("keydown",(e=>e.stopPropagation()))}},{kind:"method",key:"_onUpdate",value:function(e){if(!e.docChanged)return;const t=this.value;t!==this._value&&(this._value=t,n(this,"value-changed",{value:this._value}))}},{kind:"get",static:!0,key:"styles",value:function(){return e`
      :host(.error-state) .cm-gutters {
        border-color: var(--error-state-color, red);
      }
    `}}]}}),r),t([c("ha-trace-config")],(function(t,r){return{F:class extends r{constructor(...e){super(...e),t(this)}},d:[{kind:"field",decorators:[a({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[a({attribute:!1})],key:"trace",value:void 0},{kind:"method",key:"render",value:function(){return h`
      <ha-code-editor
        .value=${B(this.trace.config).trimRight()}
        readOnly
        dir="ltr"
      ></ha-code-editor>
    `}},{kind:"get",static:!0,key:"styles",value:function(){return[e``]}}]}}),l);t([c("hat-graph-branch")],(function(t,r){return{F:class extends r{constructor(...e){super(...e),t(this)}},d:[{kind:"field",decorators:[a({reflect:!0,type:Boolean})],key:"disabled",value:void 0},{kind:"field",decorators:[a({type:Boolean})],key:"selected",value:void 0},{kind:"field",decorators:[a({type:Boolean})],key:"start",value:()=>!1},{kind:"field",decorators:[a({type:Boolean})],key:"short",value:()=>!1},{kind:"field",decorators:[i()],key:"_branches",value:()=>[]},{kind:"field",key:"_totalWidth",value:()=>0},{kind:"field",key:"_maxHeight",value:()=>0},{kind:"method",key:"_updateBranches",value:function(e){let t=0;const r=[],a=[];e.target.assignedElements().forEach((e=>{const i=e.clientWidth,o=e.clientHeight;a.push({x:i/2+t,height:o,start:e.hasAttribute("graphStart"),end:e.hasAttribute("graphEnd"),track:e.hasAttribute("track")}),t+=i,r.push(o)})),this._totalWidth=t,this._maxHeight=Math.max(...r),this._branches=a.sort(((e,t)=>e.track&&!t.track?1:e.track&&t.track?0:-1))}},{kind:"method",key:"render",value:function(){return h`
      <slot name="head"></slot>
      ${this.start?"":u`
            <svg
              id="top"
              width="${this._totalWidth}"
            >
              ${this._branches.map((e=>e.start?"":u`
                  <path
                    class=${v({track:e.track})}
                    d="
                      M ${this._totalWidth/2} 0
                      L ${e.x} ${20}
                      "/>
                `))}
            </svg>
          `}
      <div id="branches">
        <svg id="lines" width=${this._totalWidth} height=${this._maxHeight}>
          ${this._branches.map((e=>e.end?"":u`
                    <path
                      class=${v({track:e.track})}
                      d="
                        M ${e.x} ${e.height}
                        v ${this._maxHeight-e.height}
                        "/>
                  `))}
        </svg>
        <slot @slotchange=${this._updateBranches}></slot>
      </div>

      ${this.short?"":u`
            <svg
              id="bottom"
              width="${this._totalWidth}"
            >
              ${this._branches.map((e=>e.end?"":u`
                  <path
                    class=${v({track:e.track})}
                    d="
                      M ${e.x} 0
                      V ${10}
                      L ${this._totalWidth/2} ${30}
                      "/>
                `))}
            </svg>
          `}
    `}},{kind:"get",static:!0,key:"styles",value:function(){return e`
      :host {
        position: relative;
        display: flex;
        flex-direction: column;
        align-items: center;
      }
      :host(:focus) {
        outline: none;
      }
      #branches {
        position: relative;
        display: flex;
        flex-direction: row;
        align-items: start;
      }
      ::slotted(*) {
        z-index: 1;
      }
      ::slotted([slot="head"]) {
        margin-bottom: calc(var(--hat-graph-branch-height) / -2);
      }
      #lines {
        position: absolute;
      }
      #top {
        height: var(--hat-graph-branch-height);
      }
      #bottom {
        height: calc(var(--hat-graph-branch-height) + var(--hat-graph-spacing));
      }
      path {
        stroke: var(--stroke-clr);
        stroke-width: 2;
        fill: none;
      }
      path.track {
        stroke: var(--track-clr);
      }
      :host([disabled]) path {
        stroke: var(--disabled-clr);
      }
    `}}]}}),l),t([c("hat-graph-node")],(function(t,r){return{F:class extends r{constructor(...e){super(...e),t(this)}},d:[{kind:"field",decorators:[a()],key:"iconPath",value:void 0},{kind:"field",decorators:[a({reflect:!0,type:Boolean})],key:"disabled",value:void 0},{kind:"field",decorators:[a({reflect:!0,type:Boolean})],key:"notEnabled",value:()=>!1},{kind:"field",decorators:[a({reflect:!0,type:Boolean})],key:"graphStart",value:void 0},{kind:"field",decorators:[a({type:Boolean,attribute:"nofocus"})],key:"noFocus",value:()=>!1},{kind:"field",decorators:[a({reflect:!0,type:Number})],key:"badge",value:void 0},{kind:"method",key:"updated",value:function(e){e.has("noFocus")&&(this.hasAttribute("tabindex")||this.noFocus?void 0!==e.get("noFocus")&&this.noFocus&&this.removeAttribute("tabindex"):this.setAttribute("tabindex","0"))}},{kind:"method",key:"render",value:function(){const e=30+(this.graphStart?2:11);return h`
      <svg
        width="${40}px"
        height="${e}px"
        viewBox="-${Math.ceil(20)} -${this.graphStart?Math.ceil(e/2):Math.ceil(25)} ${40} ${e}"
      >
        ${this.graphStart?"":u`
          <path
            class="connector"
            d="
              M 0 ${-25}
              L 0 0
            "
            line-caps="round"
          />
          `}
        <g class="node">
          <circle cx="0" cy="0" r=${15} />
          }
          ${this.badge?u`
        <g class="number">
          <circle
            cx="8"
            cy=${-15}
            r="8"
          ></circle>
          <text
            x="8"
            y=${-15}
            text-anchor="middle"
            alignment-baseline="middle"
          >${this.badge>9?"9+":this.badge}</text>
        </g>
      `:""}
          <g style="pointer-events: none" transform="translate(${-12} ${-12})">
            ${this.iconPath?u`<path class="icon" d=${this.iconPath}/>`:""}
          </g>
        </g>
      </svg>
    `}},{kind:"get",static:!0,key:"styles",value:function(){return e`
      :host {
        display: flex;
        flex-direction: column;
        min-width: calc(var(--hat-graph-node-size) + var(--hat-graph-spacing));
        height: calc(
          var(--hat-graph-node-size) + var(--hat-graph-spacing) + 1px
        );
      }
      :host([graphStart]) {
        height: calc(var(--hat-graph-node-size) + 2px);
      }
      :host([track]) {
        --stroke-clr: var(--track-clr);
        --icon-clr: var(--default-icon-clr);
      }
      :host([active]) circle {
        --stroke-clr: var(--active-clr);
        --icon-clr: var(--default-icon-clr);
      }
      :host(:focus) {
        outline: none;
      }
      :host(:hover) circle {
        --stroke-clr: var(--hover-clr);
        --icon-clr: var(--default-icon-clr);
      }
      :host([notEnabled]) circle {
        --stroke-clr: var(--disabled-clr);
      }
      :host([notEnabled][active]) circle {
        --stroke-clr: var(--disabled-active-clr);
      }
      :host([notEnabled]:hover) circle {
        --stroke-clr: var(--disabled-hover-clr);
      }
      svg {
        width: 100%;
        height: 100%;
      }
      circle,
      path.connector {
        stroke: var(--stroke-clr);
        stroke-width: 2;
        fill: none;
      }
      circle {
        fill: var(--background-clr);
        stroke: var(--circle-clr, var(--stroke-clr));
      }
      .number circle {
        fill: var(--track-clr);
        stroke: none;
        stroke-width: 0;
      }
      .number text {
        font-size: smaller;
      }
      path.icon {
        fill: var(--icon-clr);
      }
    `}}]}}),l),t([c("hat-graph-spacer")],(function(t,r){return{F:class extends r{constructor(...e){super(...e),t(this)}},d:[{kind:"field",decorators:[a({reflect:!0,type:Boolean})],key:"disabled",value:void 0},{kind:"method",key:"render",value:function(){return h`
      <svg viewBox="-${5} 0 10 ${41}">
        <path
          d="
              M 0 ${41}
              V 0
            "
          line-caps="round"
        />
        }
      </svg>
    `}},{kind:"get",static:!0,key:"styles",value:function(){return e`
      :host {
        display: flex;
        flex-direction: column;
        align-items: center;
      }
      svg {
        width: var(--hat-graph-spacing);
        height: calc(
          var(--hat-graph-spacing) + var(--hat-graph-node-size) + 1px
        );
      }
      :host([track]) {
        --stroke-clr: var(--track-clr);
      }
      :host-context([disabled]) {
        --stroke-clr: var(--disabled-clr);
      }
      path {
        stroke: var(--stroke-clr);
        stroke-width: 2;
        fill: none;
      }
    `}}]}}),l),t([c("react-script-graph")],(function(t,r){class i extends r{constructor(...e){super(...e),t(this)}}return{F:i,d:[{kind:"field",decorators:[a({attribute:!1})],key:"trace",value:void 0},{kind:"field",decorators:[a({attribute:!1})],key:"selected",value:void 0},{kind:"field",key:"renderedNodes",value:()=>({})},{kind:"field",key:"trackedNodes",value:()=>({})},{kind:"method",key:"selectNode",value:function(e,t){return()=>{n(this,"graph-node-selected",{config:e,path:t})}}},{kind:"method",key:"render_actor",value:function(e,t){const r=`actor/${t}`,a=`${r}/trigger`,i=`${r}/condition`,o=this.trace&&a in this.trace.trace;this.renderedNodes[a]={config:e.trigger,path:a},o&&(this.trackedNodes[a]=this.renderedNodes[a]);const d=this.get_condition_info(i);return e.condition?h`
                <div ?track=${o&&d.track&&d.trackPass}>
                    ${this.render_actor_node(e,o,a)}
                    ${this.render_condition_node(e.condition,`${i}`,!1,!1===e.trigger.enabled)}
                </div>
            `:this.render_actor_node(e,o,a)}},{kind:"method",key:"render_actor_node",value:function(e,t,r){return h`
            <hat-graph-node
                graphStart
                ?track=${t}
                @focus=${this.selectNode(e,r)}
                ?active=${this.selected===r}
                .iconPath=${k}
                .notEnabled=${!1===e.trigger.enabled}
                tabindex=${t?"0":"-1"}
            ></hat-graph-node>`}},{kind:"method",key:"render_reactor",value:function(e,t,r=!1){const a=`reactor/${t}`,i=`${a}/event`,o=`${a}/condition`,d=this.trace&&i in this.trace.trace;this.renderedNodes[i]={config:e.event,path:i},d&&(this.trackedNodes[i]=this.renderedNodes[i]);const s=this.get_condition_info(o);return e.condition?h`
                <div ?track=${d||s.has_condition&&s.trackFailed}>
                    ${this.render_condition_node(e.condition,o,!1,!1===e.event.enabled)}
                    ${this.render_reactor_node(e,d,i,r)}
                </div>
            `:this.render_reactor_node(e,d,i,r)}},{kind:"method",key:"render_reactor_node",value:function(e,t,r,a){return h`
            <hat-graph-node
                .iconPath=${"immediate"===e.timing?p:f}
                @focus=${this.selectNode(e,r)}
                ?track=${t}
                ?active=${this.selected===r}
                .notEnabled=${a||!1===e.event.enabled}
                tabindex=${this.trace&&r in this.trace.trace?"0":"-1"}
                graphEnd 
            ></hat-graph-node>`}},{kind:"method",key:"render_condition_node",value:function(e,t,r=!1,a=!1){this.renderedNodes[t]={config:e,path:t},this.trace&&t in this.trace.trace&&(this.trackedNodes[t]=this.renderedNodes[t]);const i=this.get_condition_info(t);return h`
            <hat-graph-branch
                @focus=${this.selectNode(e,t)}
                ?track=${i.track}
                ?active=${this.selected===t}
                .notEnabled=${a||!1===e.enabled}
                tabindex=${void 0===i.trace?"-1":"0"}
                short
            >
                <hat-graph-node
                    .graphStart=${r}
                    slot="head"
                    ?track=${i.track}
                    ?active=${this.selected===t}
                    .notEnabled=${a||!1===e.enabled}
                    .iconPath=${g}
                    nofocus
                ></hat-graph-node>
                <div
                    style=${"width: 40px;"}
                    graphStart
                    graphEnd
                ></div>
                <div ?track=${i.trackPass}></div>
                <hat-graph-node
                    .iconPath=${_}
                    nofocus
                    ?track=${i.trackFailed}
                    ?active=${this.selected===t}
                    .notEnabled=${a||!1===e.enabled}
                ></hat-graph-node>
            </hat-graph-branch>
        `}},{kind:"method",key:"render_parallel_node",value:function(e,t,r=!1,a=!1){const i=this.trace&&t in this.trace.trace;this.renderedNodes[t]={config:e,path:t},i&&(this.trackedNodes[t]=this.renderedNodes[t]);const o=this.trace.trace[t];return h`
            <hat-graph-branch
                tabindex=${void 0===o?"-1":"0"}
                @focus=${this.selectNode(e,t)}
                ?track=${i}
                ?active=${this.selected===t}
                .notEnabled=${a}
                short
            >
                <hat-graph-node
                    .graphStart=${r}
                    .iconPath=${b}
                    ?track=${i}
                    ?active=${this.selected===t}
                    .notEnabled=${a}
                    slot="head"
                    nofocus
                ></hat-graph-node>
                ${F(this.trace.config.reactor).map(((e,t)=>this.render_reactor(e,t)))}
                
            </hat-graph-branch>
        `}},{kind:"method",key:"get_condition_info",value:function(e){const t=this.trace.trace[e];let r=!1,a=!1,i=!1,o=!1;if(t){a=!0;for(const e of t)if(e.result&&(r=!0,e.result.result?i=!0:o=!0),i&&o)break}return{trace:t,track:r,has_condition:a,trackPass:i,trackFailed:o}}},{kind:"method",key:"render",value:function(){const e=Object.keys(this.trackedNodes),t=F(this.trace.config.actor).map(((e,t)=>this.render_actor(e,t)));try{return h`
                <div class="parent graph-container">
                    ${h`
                        <hat-graph-branch start .short=${t.length<2}>
                            ${t}
                        </hat-graph-branch>`}
                    ${"parallel"in this.trace.config?h`
                            ${this.render_parallel_node(this.trace.config.parallel,"parallel",!1,!1)}`:h`
                            ${this.render_reactor(this.trace.config.reactor[0],0)}`}
                </div>
                <div class="actions">
                    <ha-icon-button
                        .disabled=${0===e.length||e[0]===this.selected}
                        @click=${this._previousTrackedNode}
                        .path=${y}
                    ></ha-icon-button>
                    <ha-icon-button
                        .disabled=${0===e.length||e[e.length-1]===this.selected}
                        @click=${this._nextTrackedNode}
                        .path=${m}
                    ></ha-icon-button>
                </div>
            `}catch(e){return h`
            <div class="error">
                Error rendering graph. Please download trace and share with the
                developers.
            </div>
        `}}},{kind:"method",key:"willUpdate",value:function(e){o(d(i.prototype),"willUpdate",this).call(this,e),e.has("trace")&&(this.renderedNodes={},this.trackedNodes={})}},{kind:"method",key:"updated",value:function(e){if(o(d(i.prototype),"updated",this).call(this,e),e.has("trace")){if(!this.selected||!(this.selected in this.trackedNodes)){const e=this.trackedNodes[Object.keys(this.trackedNodes)[0]];e&&n(this,"graph-node-selected",e)}if(this.trace){const e=Object.keys(this.trace.trace),t=Object.keys(this.renderedNodes).sort(((t,r)=>e.indexOf(t)-e.indexOf(r))),r={},a={};for(const e of t)a[e]=this.renderedNodes[e],e in this.trackedNodes&&(r[e]=this.trackedNodes[e]);this.renderedNodes=a,this.trackedNodes=r}}}},{kind:"method",key:"_previousTrackedNode",value:function(){const e=Object.keys(this.trackedNodes),t=e.indexOf(this.selected)-1;t>=0&&n(this,"graph-node-selected",this.trackedNodes[e[t]])}},{kind:"method",key:"_nextTrackedNode",value:function(){const e=Object.keys(this.trackedNodes),t=e.indexOf(this.selected)+1;t<e.length&&n(this,"graph-node-selected",this.trackedNodes[e[t]])}},{kind:"get",static:!0,key:"styles",value:function(){return e`
            :host {
                display: flex;
                --stroke-clr: var(--stroke-color, var(--secondary-text-color));
                --active-clr: var(--active-color, var(--primary-color));
                --track-clr: var(--track-color, var(--accent-color));
                --hover-clr: var(--hover-color, var(--primary-color));
                --disabled-clr: var(--disabled-color, var(--disabled-text-color));
                --disabled-active-clr: rgba(var(--rgb-primary-color), 0.5);
                --disabled-hover-clr: rgba(var(--rgb-primary-color), 0.7);
                --default-trigger-color: 3, 169, 244;
                --rgb-trigger-color: var(--trigger-color, var(--default-trigger-color));
                --background-clr: var(--background-color, white);
                --default-icon-clr: var(--icon-color, black);
                --icon-clr: var(--stroke-clr);

                --hat-graph-spacing: ${10}px;
                --hat-graph-node-size: ${30}px;
                --hat-graph-branch-height: ${20}px;
            }
            .graph-container {
                display: flex;
                flex-direction: column;
                align-items: center;
            }
            .actions {
                display: flex;
                flex-direction: column;
            }
            .parent {
                margin-left: 8px;
                margin-top: 16px;
            }
            .error {
                padding: 16px;
                max-width: 300px;
            }
            `}}]}}),l);t([c("react-trace-path-details")],(function(t,r){return{F:class extends r{constructor(...e){super(...e),t(this)}},d:[{kind:"field",decorators:[a({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[a({type:Boolean,reflect:!0})],key:"narrow",value:void 0},{kind:"field",decorators:[a({attribute:!1})],key:"trace",value:void 0},{kind:"field",decorators:[a({attribute:!1})],key:"selected",value:void 0},{kind:"field",decorators:[a()],key:"renderedNodes",value:()=>({})},{kind:"field",decorators:[a()],key:"trackedNodes",value:void 0},{kind:"field",decorators:[i()],key:"_view",value:()=>"config"},{kind:"method",key:"render",value:function(){return h`
            <div class="padded-box trace-info">
                ${this._renderSelectedTraceInfo()}
            </div>

            <div class="tabs top">
                ${[["config","Step Config"],["changed_variables","Changed Variables"]].map((([e,t])=>h`
                    <button
                        .view=${e}
                        class=${v({active:this._view===e})}
                        @click=${this._showTab}
                    >
                        ${t}
                    </button>
                `))}
            </div>
            ${"config"===this._view?this._renderSelectedConfig():this._renderChangedVars()}
        `}},{kind:"method",key:"_renderSelectedTraceInfo",value:function(){var e;const t=this.trace.trace;if(null===(e=this.selected)||void 0===e||!e.path)return"Select a node on the left for more information.";if(!(this.selected.path in t))return"This node was not executed and so no further trace information is available.";const r=[];let a=!1;for(const e of Object.keys(this.trace.trace)){if(a){if(e in this.renderedNodes)break}else{if(e!==this.selected.path)continue;a=!0}const i=t[e];r.push(i.map(((t,r)=>{const{path:a,timestamp:o,result:d,error:s,changed_variables:n,...c}=t;return!1===(null==d?void 0:d.enabled)?h`This node was disabled and skipped during execution so
                    no further trace information is available.`:h`
                    ${e===this.selected.path?"":h`<h2>${e.substr(this.selected.path.length+1)}</h2>`}
                    ${1===i.length?"":h`<h3>Iteration ${r+1}</h3>`}
                    Executed:
                    ${j(new Date(o),this.hass.locale)}
                    <br />
                    ${d?h`Result:
                            <pre>${B(d)}</pre>`:s?h`<div class="error">Error: ${s}</div>`:""}
                    ${0===Object.keys(c).length?"":h`<pre>${B(c)}</pre>`}
                `})))}return r}},{kind:"method",key:"_renderSelectedConfig",value:function(){var e;if(null===(e=this.selected)||void 0===e||!e.path)return"";const t=((e,t)=>{const r=t.split("/").reverse();let a=e;for(;r.length;){const e=r.pop(),t=Number(e);if(isNaN(t))a=a[e];else if(Array.isArray(a))a=a[t];else if(0!==t)throw new Error("If config is not an array, can only return index 0")}return a})(this.trace.config,this.selected.path);return t?h`
                <ha-code-editor
                    .value=${B(t).trimRight()}
                    readOnly
                    dir="ltr"
                ></ha-code-editor>`:"Unable to find config"}},{kind:"method",key:"_renderChangedVars",value:function(){const e=this.trace.trace[this.selected.path];return h`
        <div class="padded-box">
            ${e?e.map(((e,t)=>h`
                        ${t>0?h`<p>Iteration ${t+1}</p>`:""}
                        ${0===Object.keys(e.changed_variables||{}).length?"No variables changed":h`<pre>${B(e.changed_variables).trimRight()}</pre>`}
                    `)):""}
        </div>
        `}},{kind:"method",key:"_showTab",value:function(e){this._view=e.target.view}},{kind:"get",static:!0,key:"styles",value:function(){return[P,e`
                .padded-box {
                    margin: 16px;
                }

                :host(:not([narrow])) .trace-info {
                    min-height: 250px;
                }

                pre {
                    margin: 0;
                }

                .error {
                    color: var(--error-color);
                }
            `]}}]}}),l);let U=t([c("react-workflow-trace")],(function(t,r){class s extends r{constructor(...e){super(...e),t(this)}}return{F:s,d:[{kind:"field",decorators:[a({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[a()],key:"workflowId",value:void 0},{kind:"field",decorators:[a({attribute:!1})],key:"workflows",value:void 0},{kind:"field",decorators:[a({type:Boolean})],key:"isWide",value:void 0},{kind:"field",decorators:[a({type:Boolean,reflect:!0})],key:"narrow",value:void 0},{kind:"field",decorators:[a({attribute:!1})],key:"route",value:void 0},{kind:"field",decorators:[i()],key:"_entityId",value:void 0},{kind:"field",decorators:[i()],key:"_traces",value:void 0},{kind:"field",decorators:[i()],key:"_runId",value:void 0},{kind:"field",decorators:[i()],key:"_selected",value:void 0},{kind:"field",decorators:[i()],key:"_trace",value:void 0},{kind:"field",decorators:[i()],key:"_view",value:()=>"details"},{kind:"field",decorators:[$("react-script-graph")],key:"_graph",value:void 0},{kind:"method",key:"render",value:function(){var e;const t=this._entityId?this.hass.states[this._entityId]:void 0,r=this._graph,a=null==r?void 0:r.trackedNodes,i=null==r?void 0:r.renderedNodes,o=(null==t?void 0:t.attributes.friendly_name)||this._entityId;let d="";const s=h`
            <ha-icon-button
                .label=${this.hass.localize("ui.panel.config.automation.trace.refresh")}
                .path=${w}
                @click=${this._refreshTraces}
            ></ha-icon-button>
            <ha-icon-button
                .label=${this.hass.localize("ui.panel.config.automation.trace.download_trace")}
                .path=${x}
                .disabled=${!this._trace}
                @click=${this._downloadTrace}
            ></ha-icon-button>
        `;return h`
            ${d}
            <hass-tabs-subpage
                .hass=${this.hass}
                .narrow=${this.narrow}
                .route=${this.route}
                .tabs=${N.react}
            >
            ${this.narrow?h`<span slot="header">${o}</span>
                    <div slot="toolbar-icon">${s}</div>`:""}
            <div class="toolbar">
                ${this.narrow?"":h`<div>
                    ${o}
                    </div>`}
                ${this._traces&&this._traces.length>0?h`
                    <div>
                        <ha-icon-button
                            .label=${this.hass.localize("ui.panel.config.automation.trace.older_trace")}
                            .path=${C}
                            .disabled=${this._traces[this._traces.length-1].run_id===this._runId}
                            @click=${this._pickOlderTrace}
                        ></ha-icon-button>
                        <select .value=${this._runId} @change=${this._pickTrace}>
                        ${E(this._traces,(e=>e.run_id),(e=>h`<option value=${e.run_id}>
                                ${j(new Date(e.timestamp.start),this.hass.locale)}
                            </option>`))}
                        </select>
                        <ha-icon-button
                            .label=${this.hass.localize("ui.panel.config.automation.trace.newer_trace")}
                            .path=${M}
                            .disabled=${this._traces[0].run_id===this._runId}
                            @click=${this._pickNewerTrace}
                        ></ha-icon-button>
                    </div>
                    `:""}
                ${this.narrow?"":h`<div>${s}</div>`}
            </div>
    
            ${void 0===this._traces?h`<div class="container">Loading…</div>`:0===this._traces.length?h`<div class="container">No traces found</div>`:void 0===this._trace?"":h`
                    <div class="main">
                    <div class="graph">
                        <react-script-graph
                            .trace=${this._trace}
                            .selected=${null===(e=this._selected)||void 0===e?void 0:e.path}
                            @graph-node-selected=${this._pickNode}
                        ></react-script-graph>
                    </div>
    
                    <div class="info">
                        <div class="tabs top">
                            ${[["details","Step Details"],["config","Workflow Config"]].map((([e,t])=>h`
                                <button
                                    tabindex="0"
                                    .view=${e}
                                    class=${v({active:this._view===e})}
                                    @click=${this._showTab}
                                >
                                    ${t}
                                </button>
                                `))}
                        </div>
                        ${void 0===this._selected||void 0===a?"":"details"===this._view?h`
                            <react-trace-path-details
                                .hass=${this.hass}
                                .narrow=${this.narrow}
                                .trace=${this._trace}
                                .selected=${this._selected}
                                .trackedNodes=${a}
                                .renderedNodes=${i}
                            ></react-trace-path-details>
                            `:h`
                            <ha-trace-config
                                .hass=${this.hass}
                                .trace=${this._trace}
                            ></ha-trace-config>
                            `}
                    </div>
                    </div>
                `}
            </hass-tabs-subpage>
        `}},{kind:"method",key:"firstUpdated",value:function(e){if(o(d(s.prototype),"firstUpdated",this).call(this,e),!this.workflowId)return;const t=new URLSearchParams(location.search);this._loadTraces(t.get("run_id")||void 0)}},{kind:"method",key:"updated",value:function(e){if(o(d(s.prototype),"updated",this).call(this,e),e.get("workflowId")&&(this._traces=void 0,this._entityId=void 0,this._runId=void 0,this._trace=void 0,this.workflowId&&this._loadTraces()),e.has("_runId")&&this._runId&&(this._trace=void 0,this._loadTrace()),e.has("workflows")&&this.workflowId&&!this._entityId){const e=this.workflows.find((e=>e.attributes.workflow_id===this.workflowId));this._entityId=null==e?void 0:e.entity_id}}},{kind:"method",key:"_pickOlderTrace",value:function(){const e=this._traces.findIndex((e=>e.run_id===this._runId));this._runId=this._traces[e+1].run_id,this._selected=void 0}},{kind:"method",key:"_pickNewerTrace",value:function(){const e=this._traces.findIndex((e=>e.run_id===this._runId));this._runId=this._traces[e-1].run_id,this._selected=void 0}},{kind:"method",key:"_pickTrace",value:function(e){this._runId=e.target.value,this._selected=void 0}},{kind:"method",key:"_pickNode",value:function(e){this._selected=e.detail}},{kind:"method",key:"_refreshTraces",value:function(){this._loadTraces()}},{kind:"method",key:"_loadTraces",value:async function(e){if(this._traces=await I(this.hass,this.workflowId),this._traces.reverse(),e&&(this._runId=e),this._runId&&!this._traces.some((e=>e.run_id===this._runId))){if(this._runId=void 0,this._selected=void 0,e){const e=new URLSearchParams(location.search);e.delete("run_id"),history.replaceState(null,"",`${location.pathname}?${e.toString()}`)}await O(this,{text:"Chosen trace is no longer available"})}!this._runId&&this._traces.length>0&&(this._runId=this._traces[0].run_id)}},{kind:"method",key:"_loadTrace",value:async function(){const e=await S(this.hass,this.workflowId,this._runId);this._trace=e}},{kind:"method",key:"_downloadTrace",value:function(){const e=document.createElement("a");e.download=`trace ${this._entityId} ${this._trace.timestamp.start}.json`,e.href=`data:application/json;charset=utf-8,${encodeURI(JSON.stringify({trace:this._trace},void 0,2))}`,e.click()}},{kind:"method",key:"_importTrace",value:function(){const e=prompt("Enter downloaded trace");e&&(localStorage.devTrace=e,this._loadLocalTrace(e))}},{kind:"method",key:"_loadLocalStorageTrace",value:function(){localStorage.devTrace&&this._loadLocalTrace(localStorage.devTrace)}},{kind:"method",key:"_loadLocalTrace",value:function(e){const t=JSON.parse(e);this._trace=t.trace}},{kind:"method",key:"_showTab",value:function(e){this._view=e.target.view}},{kind:"get",static:!0,key:"styles",value:function(){return[T,P,e`
                .toolbar {
                  display: flex;
                  align-items: center;
                  justify-content: space-between;
                  font-size: 20px;
                  height: var(--header-height);
                  padding: 0 16px;
                  background-color: var(--primary-background-color);
                  font-weight: 400;
                  color: var(--app-header-text-color, white);
                  border-bottom: var(--app-header-border-bottom, none);
                  box-sizing: border-box;
                }
        
                .toolbar > * {
                  display: flex;
                  align-items: center;
                }
        
                :host([narrow]) .toolbar > * {
                  display: contents;
                }
        
                .main {
                  height: calc(100% - 56px);
                  display: flex;
                  background-color: var(--card-background-color);
                }
        
                :host([narrow]) .main {
                  height: auto;
                  flex-direction: column;
                }
        
                .container {
                  padding: 16px;
                }
        
                .graph {
                  border-right: 1px solid var(--divider-color);
                  overflow-x: auto;
                  max-width: 50%;
                  padding-bottom: 16px;
                }
                :host([narrow]) .graph {
                  max-width: 100%;
                  justify-content: center;
                  display: flex;
                }
        
                .info {
                  flex: 1;
                  background-color: var(--card-background-color);
                }
        
                .linkButton {
                  color: var(--primary-text-color);
                }
              `]}}]}}),l);export{U as ReactWorkflowTrace};

"use strict";(globalThis.webpackChunksuperset=globalThis.webpackChunksuperset||[]).push([[2848],{168073:(module,__webpack_exports__,__webpack_require__)=>{__webpack_require__.d(__webpack_exports__,{Z:()=>ModalTrigger});var react__WEBPACK_IMPORTED_MODULE_0__=__webpack_require__(667294),prop_types__WEBPACK_IMPORTED_MODULE_1__=__webpack_require__(45697),prop_types__WEBPACK_IMPORTED_MODULE_1___default=__webpack_require__.n(prop_types__WEBPACK_IMPORTED_MODULE_1__),src_components_Modal__WEBPACK_IMPORTED_MODULE_2__=__webpack_require__(574520),src_components_Button__WEBPACK_IMPORTED_MODULE_3__=__webpack_require__(835932),_emotion_react__WEBPACK_IMPORTED_MODULE_4__=__webpack_require__(211965),enterModule;module=__webpack_require__.hmd(module),enterModule="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.enterModule:void 0,enterModule&&enterModule(module);var __signature__="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.default.signature:function(e){return e};const propTypes={dialogClassName:prop_types__WEBPACK_IMPORTED_MODULE_1___default().string,triggerNode:prop_types__WEBPACK_IMPORTED_MODULE_1___default().node.isRequired,modalTitle:prop_types__WEBPACK_IMPORTED_MODULE_1___default().node,modalBody:prop_types__WEBPACK_IMPORTED_MODULE_1___default().node,modalFooter:prop_types__WEBPACK_IMPORTED_MODULE_1___default().node,beforeOpen:prop_types__WEBPACK_IMPORTED_MODULE_1___default().func,onExit:prop_types__WEBPACK_IMPORTED_MODULE_1___default().func,isButton:prop_types__WEBPACK_IMPORTED_MODULE_1___default().bool,className:prop_types__WEBPACK_IMPORTED_MODULE_1___default().string,tooltip:prop_types__WEBPACK_IMPORTED_MODULE_1___default().string,width:prop_types__WEBPACK_IMPORTED_MODULE_1___default().string,maxWidth:prop_types__WEBPACK_IMPORTED_MODULE_1___default().string,responsive:prop_types__WEBPACK_IMPORTED_MODULE_1___default().bool,resizable:prop_types__WEBPACK_IMPORTED_MODULE_1___default().bool,resizableConfig:prop_types__WEBPACK_IMPORTED_MODULE_1___default().object,draggable:prop_types__WEBPACK_IMPORTED_MODULE_1___default().bool,draggableConfig:prop_types__WEBPACK_IMPORTED_MODULE_1___default().object},defaultProps={beforeOpen:()=>{},onExit:()=>{},isButton:!1,className:"",modalTitle:"",resizable:!1,draggable:!1};class ModalTrigger extends react__WEBPACK_IMPORTED_MODULE_0__.Component{constructor(e){super(e),this.state={showModal:!1},this.open=this.open.bind(this),this.close=this.close.bind(this)}close(){this.setState((()=>({showModal:!1})))}open(e){e.preventDefault(),this.props.beforeOpen(),this.setState((()=>({showModal:!0})))}renderModal(){return(0,_emotion_react__WEBPACK_IMPORTED_MODULE_4__.tZ)(src_components_Modal__WEBPACK_IMPORTED_MODULE_2__.Z,{wrapClassName:this.props.dialogClassName,className:this.props.className,show:this.state.showModal,onHide:this.close,afterClose:this.props.onExit,title:this.props.modalTitle,footer:this.props.modalFooter,hideFooter:!this.props.modalFooter,width:this.props.width,maxWidth:this.props.maxWidth,responsive:this.props.responsive,resizable:this.props.resizable,resizableConfig:this.props.resizableConfig,draggable:this.props.draggable,draggableConfig:this.props.draggableConfig},this.props.modalBody)}render(){return this.props.isButton?(0,_emotion_react__WEBPACK_IMPORTED_MODULE_4__.tZ)(react__WEBPACK_IMPORTED_MODULE_0__.Fragment,null,(0,_emotion_react__WEBPACK_IMPORTED_MODULE_4__.tZ)(src_components_Button__WEBPACK_IMPORTED_MODULE_3__.Z,{className:"modal-trigger","data-test":"btn-modal-trigger",tooltip:this.props.tooltip,onClick:this.open},this.props.triggerNode),this.renderModal()):(0,_emotion_react__WEBPACK_IMPORTED_MODULE_4__.tZ)(react__WEBPACK_IMPORTED_MODULE_0__.Fragment,null,(0,_emotion_react__WEBPACK_IMPORTED_MODULE_4__.tZ)("span",{"data-test":"span-modal-trigger",onClick:this.open,role:"button"},this.props.triggerNode),this.renderModal())}__reactstandin__regenerateByEval(key,code){this[key]=eval(code)}}var reactHotLoader,leaveModule;ModalTrigger.propTypes=propTypes,ModalTrigger.defaultProps=defaultProps,reactHotLoader="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.default:void 0,reactHotLoader&&(reactHotLoader.register(propTypes,"propTypes","/Users/chenming/superset/superset-frontend/src/components/ModalTrigger/index.jsx"),reactHotLoader.register(defaultProps,"defaultProps","/Users/chenming/superset/superset-frontend/src/components/ModalTrigger/index.jsx"),reactHotLoader.register(ModalTrigger,"ModalTrigger","/Users/chenming/superset/superset-frontend/src/components/ModalTrigger/index.jsx")),leaveModule="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.leaveModule:void 0,leaveModule&&leaveModule(module)},975017:(module,__webpack_exports__,__webpack_require__)=>{__webpack_require__.d(__webpack_exports__,{Z:()=>OnPasteSelect});var _babel_runtime_corejs3_helpers_extends__WEBPACK_IMPORTED_MODULE_0__=__webpack_require__(205872),_babel_runtime_corejs3_helpers_extends__WEBPACK_IMPORTED_MODULE_0___default=__webpack_require__.n(_babel_runtime_corejs3_helpers_extends__WEBPACK_IMPORTED_MODULE_0__),react__WEBPACK_IMPORTED_MODULE_1__=__webpack_require__(667294),prop_types__WEBPACK_IMPORTED_MODULE_2__=__webpack_require__(45697),prop_types__WEBPACK_IMPORTED_MODULE_2___default=__webpack_require__.n(prop_types__WEBPACK_IMPORTED_MODULE_2__),src_components_Select__WEBPACK_IMPORTED_MODULE_3__=__webpack_require__(93719),_emotion_react__WEBPACK_IMPORTED_MODULE_4__=__webpack_require__(211965),enterModule;module=__webpack_require__.hmd(module),enterModule="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.enterModule:void 0,enterModule&&enterModule(module);var __signature__="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.default.signature:function(e){return e},reactHotLoader,leaveModule;class OnPasteSelect extends react__WEBPACK_IMPORTED_MODULE_1__.Component{constructor(e){super(e),this.onPaste=this.onPaste.bind(this)}onPaste(e){if(!this.props.isMulti)return;e.preventDefault();const t=e.clipboardData.getData("Text");if(!t)return;const r=`[${this.props.separator}]+`,o=t.split(new RegExp(r)).map((e=>e.trim())),s=this.props.isValidNewOption,n=this.props.value||[],a={},i={};this.props.options.forEach((e=>{a[e[this.props.valueKey]]=1}));let l=[];n.forEach((e=>{l.push({[this.props.labelKey]:e,[this.props.valueKey]:e}),i[e]=1})),l=l.concat(o.filter((e=>{const t=!i[e];return i[e]=1,t&&(s?s({[this.props.labelKey]:e}):!!e)})).map((e=>{const t={[this.props.labelKey]:e,[this.props.valueKey]:e};return a[e]||this.props.options.unshift(t),t}))),l.length&&this.props.onChange&&this.props.onChange(l)}render(){const{selectWrap:e,...t}=this.props;return(0,_emotion_react__WEBPACK_IMPORTED_MODULE_4__.tZ)(e,_babel_runtime_corejs3_helpers_extends__WEBPACK_IMPORTED_MODULE_0___default()({},t,{onPaste:this.onPaste}))}__reactstandin__regenerateByEval(key,code){this[key]=eval(code)}}OnPasteSelect.propTypes={separator:prop_types__WEBPACK_IMPORTED_MODULE_2___default().array,selectWrap:prop_types__WEBPACK_IMPORTED_MODULE_2___default().elementType,selectRef:prop_types__WEBPACK_IMPORTED_MODULE_2___default().func,onChange:prop_types__WEBPACK_IMPORTED_MODULE_2___default().func.isRequired,valueKey:prop_types__WEBPACK_IMPORTED_MODULE_2___default().string,labelKey:prop_types__WEBPACK_IMPORTED_MODULE_2___default().string,options:prop_types__WEBPACK_IMPORTED_MODULE_2___default().array,isMulti:prop_types__WEBPACK_IMPORTED_MODULE_2___default().bool,value:prop_types__WEBPACK_IMPORTED_MODULE_2___default().any,isValidNewOption:prop_types__WEBPACK_IMPORTED_MODULE_2___default().func,noResultsText:prop_types__WEBPACK_IMPORTED_MODULE_2___default().string,forceOverflow:prop_types__WEBPACK_IMPORTED_MODULE_2___default().bool},OnPasteSelect.defaultProps={separator:[",","\n","\t",";"],selectWrap:src_components_Select__WEBPACK_IMPORTED_MODULE_3__.Ph,valueKey:"value",labelKey:"label",options:[],isMulti:!1},reactHotLoader="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.default:void 0,reactHotLoader&&reactHotLoader.register(OnPasteSelect,"OnPasteSelect","/Users/chenming/superset/superset-frontend/src/components/Select/OnPasteSelect.jsx"),leaveModule="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.leaveModule:void 0,leaveModule&&leaveModule(module)},701836:(e,t,r)=>{r.d(t,{zQ:()=>a,zO:()=>i,xG:()=>l,x_:()=>d,pu:()=>c});var o,s=r(730381),n=r.n(s);e=r.hmd(e),(o="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.enterModule:void 0)&&o(e),"undefined"!=typeof reactHotLoaderGlobal&&reactHotLoaderGlobal.default.signature;const a=function(e,t,r="HH:mm:ss.SS"){const o=t-e;return n()(new Date(o)).utc().format(r)},i=function(){return n()().utc().valueOf()},l=function(e){return n()().subtract(e,"hours").utc().valueOf()},d=function(e){return n()().subtract(e,"days").utc().valueOf()},c=function(e){return n()().subtract(e,"years").utc().valueOf()};var p,u;(p="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.default:void 0)&&(p.register(a,"fDuration","/Users/chenming/superset/superset-frontend/src/modules/dates.js"),p.register(i,"now","/Users/chenming/superset/superset-frontend/src/modules/dates.js"),p.register(l,"epochTimeXHoursAgo","/Users/chenming/superset/superset-frontend/src/modules/dates.js"),p.register(d,"epochTimeXDaysAgo","/Users/chenming/superset/superset-frontend/src/modules/dates.js"),p.register(c,"epochTimeXYearsAgo","/Users/chenming/superset/superset-frontend/src/modules/dates.js")),(u="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.leaveModule:void 0)&&u(e)},444904:(e,t,r)=>{var o;r.d(t,{IY:()=>s,Em:()=>n,v3:()=>a,eU:()=>i,ev:()=>l,rp:()=>d,Yo:()=>c,TU:()=>p,U$:()=>u,b$:()=>g,rD:()=>_,N2:()=>m,Yn:()=>f,GJ:()=>h,iJ:()=>b,lr:()=>y,OI:()=>L}),e=r.hmd(e),(o="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.enterModule:void 0)&&o(e),"undefined"!=typeof reactHotLoaderGlobal&&reactHotLoaderGlobal.default.signature;const s={offline:"danger",failed:"danger",pending:"info",fetching:"info",running:"warning",stopped:"danger",success:"success"},n={success:"success",failed:"failed",running:"running",offline:"offline",pending:"pending"},a=["now","1 hour ago","1 day ago","7 days ago","28 days ago","90 days ago","1 year ago"],i=5,l=3,d=51,c=1024,p=2,u=864e5,g=5120,_=.9,m=8e3,f=100,h=90,b=60,y=55,L=50;var E,x;(E="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.default:void 0)&&(E.register(s,"STATE_TYPE_MAP","/Users/chenming/superset/superset-frontend/src/SqlLab/constants.ts"),E.register(n,"STATUS_OPTIONS","/Users/chenming/superset/superset-frontend/src/SqlLab/constants.ts"),E.register(a,"TIME_OPTIONS","/Users/chenming/superset/superset-frontend/src/SqlLab/constants.ts"),E.register(i,"SQL_EDITOR_GUTTER_HEIGHT","/Users/chenming/superset/superset-frontend/src/SqlLab/constants.ts"),E.register(l,"SQL_EDITOR_GUTTER_MARGIN","/Users/chenming/superset/superset-frontend/src/SqlLab/constants.ts"),E.register(d,"SQL_TOOLBAR_HEIGHT","/Users/chenming/superset/superset-frontend/src/SqlLab/constants.ts"),E.register(c,"KB_STORAGE","/Users/chenming/superset/superset-frontend/src/SqlLab/constants.ts"),E.register(p,"BYTES_PER_CHAR","/Users/chenming/superset/superset-frontend/src/SqlLab/constants.ts"),E.register(u,"LOCALSTORAGE_MAX_QUERY_AGE_MS","/Users/chenming/superset/superset-frontend/src/SqlLab/constants.ts"),E.register(g,"LOCALSTORAGE_MAX_USAGE_KB","/Users/chenming/superset/superset-frontend/src/SqlLab/constants.ts"),E.register(_,"LOCALSTORAGE_WARNING_THRESHOLD","/Users/chenming/superset/superset-frontend/src/SqlLab/constants.ts"),E.register(m,"LOCALSTORAGE_WARNING_MESSAGE_THROTTLE_MS","/Users/chenming/superset/superset-frontend/src/SqlLab/constants.ts"),E.register(f,"SQL_KEYWORD_AUTOCOMPLETE_SCORE","/Users/chenming/superset/superset-frontend/src/SqlLab/constants.ts"),E.register(h,"SQL_FUNCTIONS_AUTOCOMPLETE_SCORE","/Users/chenming/superset/superset-frontend/src/SqlLab/constants.ts"),E.register(b,"SCHEMA_AUTOCOMPLETE_SCORE","/Users/chenming/superset/superset-frontend/src/SqlLab/constants.ts"),E.register(y,"TABLE_AUTOCOMPLETE_SCORE","/Users/chenming/superset/superset-frontend/src/SqlLab/constants.ts"),E.register(L,"COLUMN_AUTOCOMPLETE_SCORE","/Users/chenming/superset/superset-frontend/src/SqlLab/constants.ts")),(x="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.leaveModule:void 0)&&x(e)},233313:(e,t,r)=>{r.d(t,{Z:()=>c});var o,s=r(444904);e=r.hmd(e),(o="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.enterModule:void 0)&&o(e),"undefined"!=typeof reactHotLoaderGlobal&&reactHotLoaderGlobal.default.signature;const n=["AND","AS","ASC","AVG","BY","CASE","COUNT","CREATE","CROSS","DATABASE","DEFAULT","DELETE","DESC","DISTINCT","DROP","ELSE","END","FOREIGN","FROM","GRANT","GROUP","HAVING","IF","INNER","INSERT","JOIN","KEY","LEFT","LIMIT","MAX","MIN","NATURAL","NOT","NULL","OFFSET","ON","OR","ORDER","OUTER","PRIMARY","REFERENCES","RIGHT","SELECT","SUM","TABLE","THEN","TYPE","UNION","UPDATE","WHEN","WHERE"],a=["BIGINT","BINARY","BIT","CHAR","DATE","DECIMAL","DOUBLE","FLOAT","INT","INTEGER","MONEY","NUMBER","NUMERIC","REAL","SET","TEXT","TIMESTAMP","VARCHAR"],i=n.concat(a),l=i.map((e=>({meta:"sql",name:e,score:s.Yn,value:e}))),d=l,c=d;var p,u;(p="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.default:void 0)&&(p.register(n,"SQL_KEYWORDS","/Users/chenming/superset/superset-frontend/src/SqlLab/utils/sqlKeywords.ts"),p.register(a,"SQL_DATA_TYPES","/Users/chenming/superset/superset-frontend/src/SqlLab/utils/sqlKeywords.ts"),p.register(i,"allKeywords","/Users/chenming/superset/superset-frontend/src/SqlLab/utils/sqlKeywords.ts"),p.register(l,"sqlKeywords","/Users/chenming/superset/superset-frontend/src/SqlLab/utils/sqlKeywords.ts"),p.register(d,"default","/Users/chenming/superset/superset-frontend/src/SqlLab/utils/sqlKeywords.ts")),(u="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.leaveModule:void 0)&&u(e)},229487:(e,t,r)=>{r.d(t,{Z:()=>u});var o,s,n,a=r(205872),i=r.n(a),l=r(211965),d=(r(667294),r(404863)),c=r(751995),p=r(87693);function u(e){const{type:t="info",description:r,showIcon:o=!0,closable:s=!0,roomBelow:n=!1,children:a}=e,u=(0,c.Fg)(),{colors:g,typography:_,gridUnit:m}=u,{alert:f,error:h,info:b,success:y}=g;let L=b,E=p.Z.InfoSolid;return"error"===t?(L=h,E=p.Z.ErrorSolid):"warning"===t?(L=f,E=p.Z.AlertSolid):"success"===t&&(L=y,E=p.Z.CircleCheckSolid),(0,l.tZ)(d.default,i()({role:"alert",showIcon:o,icon:(0,l.tZ)(E,{"aria-label":`${t} icon`}),closeText:s&&(0,l.tZ)(p.Z.XSmall,{"aria-label":"close icon"}),css:(0,l.iv)({marginBottom:n?4*m:0,padding:`${2*m}px ${3*m}px`,alignItems:"flex-start",border:0,backgroundColor:L.light2,"& .ant-alert-icon":{marginRight:2*m},"& .ant-alert-message":{color:L.dark2,fontSize:_.sizes.m,fontWeight:r?_.weights.bold:_.weights.normal},"& .ant-alert-description":{color:L.dark2,fontSize:_.sizes.m}},"","")},e),a)}e=r.hmd(e),(o="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.enterModule:void 0)&&o(e),("undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.default.signature:function(e){return e})(u,"useTheme{theme}",(()=>[c.Fg])),(s="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.default:void 0)&&s.register(u,"Alert","/Users/chenming/superset/superset-frontend/src/components/Alert/index.tsx"),(n="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.leaveModule:void 0)&&n(e)},794670:(e,t,r)=>{r.d(t,{iO:()=>p,up:()=>u,cE:()=>g,YH:()=>_,ry:()=>m,Ad:()=>f,Z5:()=>h});var o,s=r(205872),n=r.n(s),a=r(667294),i=r(967913),l=r(211965);e=r.hmd(e),(o="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.enterModule:void 0)&&o(e),"undefined"!=typeof reactHotLoaderGlobal&&reactHotLoaderGlobal.default.signature;const d={"mode/sql":()=>r.e(8883).then(r.t.bind(r,248883,23)),"mode/markdown":()=>Promise.all([r.e(9794),r.e(5802),r.e(4832),r.e(6061)]).then(r.t.bind(r,866061,23)),"mode/css":()=>Promise.all([r.e(5802),r.e(4972)]).then(r.t.bind(r,994972,23)),"mode/json":()=>r.e(8750).then(r.t.bind(r,158750,23)),"mode/yaml":()=>r.e(6977).then(r.t.bind(r,260741,23)),"mode/html":()=>Promise.all([r.e(9794),r.e(5802),r.e(4832),r.e(1258)]).then(r.t.bind(r,171258,23)),"mode/javascript":()=>Promise.all([r.e(9794),r.e(4579)]).then(r.t.bind(r,754579,23)),"theme/textmate":()=>r.e(2089).then(r.t.bind(r,302089,23)),"theme/github":()=>r.e(440).then(r.t.bind(r,550440,23)),"ext/language_tools":()=>r.e(5335).then(r.t.bind(r,375335,23))};function c(e,{defaultMode:t,defaultTheme:o,defaultTabSize:s=2,placeholder:c}={}){return(0,i.Z)((async()=>{var i,c;const{default:p}=await r.e(8616).then(r.t.bind(r,738616,23)),{default:u}=await Promise.all([r.e(1216),r.e(4981)]).then(r.bind(r,874981));await Promise.all(e.map((e=>d[e]())));const g=t||(null==(i=e.find((e=>e.startsWith("mode/"))))?void 0:i.replace("mode/","")),_=o||(null==(c=e.find((e=>e.startsWith("theme/"))))?void 0:c.replace("theme/",""));return(0,a.forwardRef)((function({keywords:e,mode:t=g,theme:r=_,tabSize:o=s,defaultValue:a="",...i},d){if(e){const r={getCompletions:(r,o,s,n,a)=>{Number.isNaN(parseInt(n,10))&&o.getMode().$id===`ace/mode/${t}`&&a(null,e)}};p.acequire("ace/ext/language_tools").setCompleters([r])}return(0,l.tZ)(u,n()({ref:d,mode:t,theme:r,tabSize:o,defaultValue:a},i))}))}),c)}const p=c(["mode/sql","theme/github","ext/language_tools"]),u=c(["mode/sql","theme/github","ext/language_tools"],{placeholder:()=>(0,l.tZ)("div",{style:{height:"100%"}},(0,l.tZ)("div",{style:{width:41,height:"100%",background:"#e8e8e8"}}),(0,l.tZ)("div",{className:"ace_content"}))}),g=c(["mode/markdown","theme/textmate"]),_=c(["mode/markdown","mode/sql","mode/json","mode/html","mode/javascript","theme/textmate"]),m=c(["mode/css","theme/github"]),f=c(["mode/json","theme/github"]),h=c(["mode/json","mode/yaml","theme/github"]);var b,y;(b="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.default:void 0)&&(b.register(d,"aceModuleLoaders","/Users/chenming/superset/superset-frontend/src/components/AsyncAceEditor/index.tsx"),b.register(c,"AsyncAceEditor","/Users/chenming/superset/superset-frontend/src/components/AsyncAceEditor/index.tsx"),b.register(p,"SQLEditor","/Users/chenming/superset/superset-frontend/src/components/AsyncAceEditor/index.tsx"),b.register(u,"FullSQLEditor","/Users/chenming/superset/superset-frontend/src/components/AsyncAceEditor/index.tsx"),b.register(g,"MarkdownEditor","/Users/chenming/superset/superset-frontend/src/components/AsyncAceEditor/index.tsx"),b.register(_,"TextAreaEditor","/Users/chenming/superset/superset-frontend/src/components/AsyncAceEditor/index.tsx"),b.register(m,"CssEditor","/Users/chenming/superset/superset-frontend/src/components/AsyncAceEditor/index.tsx"),b.register(f,"JsonEditor","/Users/chenming/superset/superset-frontend/src/components/AsyncAceEditor/index.tsx"),b.register(h,"ConfigEditor","/Users/chenming/superset/superset-frontend/src/components/AsyncAceEditor/index.tsx")),(y="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.leaveModule:void 0)&&y(e)},967913:(e,t,r)=>{r.d(t,{Z:()=>g});var o,s=r(205872),n=r.n(s),a=r(667294),i=r(838703),l=r(211965);e=r.hmd(e),(o="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.enterModule:void 0)&&o(e);var d,c,p="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.default.signature:function(e){return e};function u({width:e,height:t,showLoadingForImport:r=!1,placeholderStyle:o}){return t&&(0,l.tZ)("div",{key:"async-asm-placeholder",style:{width:e,height:t,...o}},r&&(0,l.tZ)(i.Z,{position:"floating"}))||null}function g(e,t=u){let r,o;function s(){return r||(r=e instanceof Promise?e:e()),o||r.then((e=>{o=e.default||e})),r}const i=(0,a.forwardRef)(p((function(e,r){const[i,d]=(0,a.useState)(void 0!==o);(0,a.useEffect)((()=>{let e=!0;return i||s().then((()=>{e&&d(!0)})),()=>{e=!1}}));const c=o||t;return c?(0,l.tZ)(c,n()({ref:c===o?r:null},e)):null}),"useState{[loaded, setLoaded](component !== undefined)}\nuseEffect{}"));return i.preload=s,i}(d="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.default:void 0)&&(d.register(u,"DefaultPlaceholder","/Users/chenming/superset/superset-frontend/src/components/AsyncEsmComponent/index.tsx"),d.register(g,"AsyncEsmComponent","/Users/chenming/superset/superset-frontend/src/components/AsyncEsmComponent/index.tsx")),(c="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.leaveModule:void 0)&&c(e)},843700:(e,t,r)=>{r.d(t,{Z:()=>d}),r(667294);var o,s=r(751995),n=r(46445),a=r(211965);e=r.hmd(e),(o="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.enterModule:void 0)&&o(e),"undefined"!=typeof reactHotLoaderGlobal&&reactHotLoaderGlobal.default.signature;const i=Object.assign((0,s.iK)((({light:e,bigger:t,bold:r,animateArrows:o,...s})=>(0,a.tZ)(n.Z,s)))`
    .ant-collapse-item {
      .ant-collapse-header {
        font-weight: ${({bold:e,theme:t})=>e?t.typography.weights.bold:t.typography.weights.normal};
        font-size: ${({bigger:e,theme:t})=>e?4*t.gridUnit+"px":"inherit"};

        .ant-collapse-arrow svg {
          transition: ${({animateArrows:e})=>e?"transform 0.24s":"none"};
        }

        ${({expandIconPosition:e})=>e&&"right"===e&&"\n            .anticon.anticon-right.ant-collapse-arrow > svg {\n              transform: rotate(90deg) !important;\n            }\n          "}

        ${({light:e,theme:t})=>e&&`\n            color: ${t.colors.grayscale.light4};\n            .ant-collapse-arrow svg {\n              color: ${t.colors.grayscale.light4};\n            }\n          `}

        ${({ghost:e,bordered:t,theme:r})=>e&&t&&`\n            border-bottom: 1px solid ${r.colors.grayscale.light3};\n          `}
      }
      .ant-collapse-content {
        .ant-collapse-content-box {
          .loading.inline {
            margin: ${({theme:e})=>12*e.gridUnit}px auto;
            display: block;
          }
        }
      }
    }
    .ant-collapse-item-active {
      .ant-collapse-header {
        ${({expandIconPosition:e})=>e&&"right"===e&&"\n            .anticon.anticon-right.ant-collapse-arrow > svg {\n              transform: rotate(-90deg) !important;\n            }\n          "}
      }
    }
  `,{Panel:n.Z.Panel}),l=i,d=l;var c,p;(c="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.default:void 0)&&(c.register(i,"Collapse","/Users/chenming/superset/superset-frontend/src/components/Collapse/index.tsx"),c.register(l,"default","/Users/chenming/superset/superset-frontend/src/components/Collapse/index.tsx")),(p="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.leaveModule:void 0)&&p(e)},94301:(e,t,r)=>{r.d(t,{XJ:()=>L,x3:()=>E,Tc:()=>x}),r(667294);var o,s,n=r(751995),a=r(211965),i=r(104715),l=r(835932);e=r.hmd(e),(o="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.enterModule:void 0)&&o(e),"undefined"!=typeof reactHotLoaderGlobal&&reactHotLoaderGlobal.default.signature,function(e){e[e.Small=0]="Small",e[e.Medium=1]="Medium",e[e.Big=2]="Big"}(s||(s={}));const d=n.iK.div`
  ${({theme:e})=>a.iv`
    display: flex;
    flex-direction: column;
    width: 100%;
    height: 100%;
    align-items: center;
    justify-content: center;
    padding: ${4*e.gridUnit}px;
    text-align: center;

    & .ant-empty-image svg {
      width: auto;
    }
  `}
`,c=n.iK.div``,p=n.iK.p`
  ${({theme:e})=>a.iv`
    font-size: ${e.typography.sizes.m}px;
    color: ${e.colors.grayscale.light1};
    margin: ${2*e.gridUnit}px 0 0 0;
    font-weight: ${e.typography.weights.bold};
  `}
`,u=(0,n.iK)(p)`
  ${({theme:e})=>a.iv`
    font-size: ${e.typography.sizes.l}px;
    color: ${e.colors.grayscale.light1};
    margin-top: ${4*e.gridUnit}px;
  `}
`,g=n.iK.p`
  ${({theme:e})=>a.iv`
    font-size: ${e.typography.sizes.s}px;
    color: ${e.colors.grayscale.light1};
    margin: ${2*e.gridUnit}px 0 0 0;
  `}
`,_=(0,n.iK)(g)`
  ${({theme:e})=>a.iv`
    font-size: ${e.typography.sizes.m}px;
  `}
`,m=(0,n.iK)(g)`
  ${({theme:e})=>a.iv`
    margin-top: ${e.gridUnit}px;
  `}
`,f=(0,n.iK)(l.Z)`
  ${({theme:e})=>a.iv`
    margin-top: ${4*e.gridUnit}px;
    z-index: 1;
  `}
`,h=e=>"string"==typeof e?`/static/assets/images/${e}`:e,b=e=>{switch(e){case s.Small:return{height:"50px"};case s.Medium:return{height:"80px"};case s.Big:return{height:"150px"};default:return{height:"50px"}}},y=({image:e,size:t})=>(0,a.tZ)(i.HY,{description:!1,image:h(e),imageStyle:b(t)}),L=({title:e,image:t,description:r,buttonAction:o,buttonText:n})=>(0,a.tZ)(d,null,(0,a.tZ)(y,{image:t,size:s.Big}),(0,a.tZ)(c,{css:e=>a.iv`
          max-width: ${150*e.gridUnit}px;
        `},(0,a.tZ)(u,null,e),r&&(0,a.tZ)(_,null,r),o&&n&&(0,a.tZ)(f,{buttonStyle:"primary",onClick:o},n))),E=({title:e,image:t,description:r,buttonAction:o,buttonText:n})=>(0,a.tZ)(d,null,(0,a.tZ)(y,{image:t,size:s.Medium}),(0,a.tZ)(c,{css:e=>a.iv`
          max-width: ${100*e.gridUnit}px;
        `},(0,a.tZ)(p,null,e),r&&(0,a.tZ)(g,null,r),n&&o&&(0,a.tZ)(f,{buttonStyle:"primary",onClick:o},n))),x=({title:e,image:t,description:r})=>(0,a.tZ)(d,null,(0,a.tZ)(y,{image:t,size:s.Small}),(0,a.tZ)(c,{css:e=>a.iv`
          max-width: ${75*e.gridUnit}px;
        `},(0,a.tZ)(p,null,e),r&&(0,a.tZ)(m,null,r)));var v,M;(v="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.default:void 0)&&(v.register(s,"EmptyStateSize","/Users/chenming/superset/superset-frontend/src/components/EmptyState/index.tsx"),v.register(d,"EmptyStateContainer","/Users/chenming/superset/superset-frontend/src/components/EmptyState/index.tsx"),v.register(c,"TextContainer","/Users/chenming/superset/superset-frontend/src/components/EmptyState/index.tsx"),v.register(p,"Title","/Users/chenming/superset/superset-frontend/src/components/EmptyState/index.tsx"),v.register(u,"BigTitle","/Users/chenming/superset/superset-frontend/src/components/EmptyState/index.tsx"),v.register(g,"Description","/Users/chenming/superset/superset-frontend/src/components/EmptyState/index.tsx"),v.register(_,"BigDescription","/Users/chenming/superset/superset-frontend/src/components/EmptyState/index.tsx"),v.register(m,"SmallDescription","/Users/chenming/superset/superset-frontend/src/components/EmptyState/index.tsx"),v.register(f,"ActionButton","/Users/chenming/superset/superset-frontend/src/components/EmptyState/index.tsx"),v.register(h,"getImage","/Users/chenming/superset/superset-frontend/src/components/EmptyState/index.tsx"),v.register(b,"getImageHeight","/Users/chenming/superset/superset-frontend/src/components/EmptyState/index.tsx"),v.register(y,"ImageContainer","/Users/chenming/superset/superset-frontend/src/components/EmptyState/index.tsx"),v.register(L,"EmptyStateBig","/Users/chenming/superset/superset-frontend/src/components/EmptyState/index.tsx"),v.register(E,"EmptyStateMedium","/Users/chenming/superset/superset-frontend/src/components/EmptyState/index.tsx"),v.register(x,"EmptyStateSmall","/Users/chenming/superset/superset-frontend/src/components/EmptyState/index.tsx")),(M="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.leaveModule:void 0)&&M(e)},272875:(e,t,r)=>{r.d(t,{Z:()=>c});var o,s=r(667294),n=r(455867),a=r(792869),i=r(891178),l=r(211965);e=r.hmd(e),(o="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.enterModule:void 0)&&o(e),"undefined"!=typeof reactHotLoaderGlobal&&reactHotLoaderGlobal.default.signature;const d=(0,n.t)("Unexpected error");function c({title:e=d,error:t,subtitle:r,copyText:o,link:n,stackTrace:c,source:p}){if(t){const e=(0,a.Z)().get(t.error_type);if(e)return(0,l.tZ)(e,{error:t,source:p,subtitle:r})}return(0,l.tZ)(i.Z,{level:"warning",title:e,subtitle:r,copyText:o,source:p,body:n||c?(0,l.tZ)(s.Fragment,null,n&&(0,l.tZ)("a",{href:n,target:"_blank",rel:"noopener noreferrer"},"(Request Access)"),(0,l.tZ)("br",null),c&&(0,l.tZ)("pre",null,c)):void 0})}var p,u;(p="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.default:void 0)&&(p.register(d,"DEFAULT_TITLE","/Users/chenming/superset/superset-frontend/src/components/ErrorMessage/ErrorMessageWithStackTrace.tsx"),p.register(c,"ErrorMessageWithStackTrace","/Users/chenming/superset/superset-frontend/src/components/ErrorMessage/ErrorMessageWithStackTrace.tsx")),(u="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.leaveModule:void 0)&&u(e)},838703:(e,t,r)=>{r.d(t,{Z:()=>d}),r(667294);var o,s=r(751995),n=r(294184),a=r.n(n),i=r(211965);e=r.hmd(e),(o="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.enterModule:void 0)&&o(e),"undefined"!=typeof reactHotLoaderGlobal&&reactHotLoaderGlobal.default.signature;const l=s.iK.img`
  z-index: 99;
  width: 50px;
  position: relative;
  margin: 10px;
  &.inline {
    margin: 0px;
    width: 30px;
  }
  &.inline-centered {
    margin: 0 auto;
    width: 30px;
    display: block;
  }
  &.floating {
    padding: 0;
    margin: 0;
    position: absolute;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);
  }
`;function d({position:e="floating",image:t="/static/assets/images/loading.gif",className:r}){return(0,i.tZ)(l,{className:a()("loading",e,r),alt:"Loading...",src:t,role:"status","aria-live":"polite","aria-label":"Loading"})}var c,p;(c="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.default:void 0)&&(c.register(l,"LoaderImg","/Users/chenming/superset/superset-frontend/src/components/Loading/index.tsx"),c.register(d,"Loading","/Users/chenming/superset/superset-frontend/src/components/Loading/index.tsx")),(p="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.leaveModule:void 0)&&p(e)},683862:(e,t,r)=>{r.d(t,{v:()=>d,$:()=>c});var o,s=r(751995),n=r(743865);e=r.hmd(e),(o="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.enterModule:void 0)&&o(e),"undefined"!=typeof reactHotLoaderGlobal&&reactHotLoaderGlobal.default.signature;const a=(0,s.iK)(n.Z.Item)`
  > a {
    text-decoration: none;
  }

  &.ant-menu-item {
    height: ${({theme:e})=>7*e.gridUnit}px;
    line-height: ${({theme:e})=>7*e.gridUnit}px;
    a {
      border-bottom: none;
      transition: background-color ${({theme:e})=>e.transitionTiming}s;
      &:after {
        content: '';
        position: absolute;
        bottom: -3px;
        left: 50%;
        width: 0;
        height: 3px;
        opacity: 0;
        transform: translateX(-50%);
        transition: all ${({theme:e})=>e.transitionTiming}s;
        background-color: ${({theme:e})=>e.colors.primary.base};
      }
      &:focus {
        border-bottom: none;
        background-color: transparent;
        @media (max-width: 767px) {
          background-color: ${({theme:e})=>e.colors.primary.light5};
        }
      }
    }
  }

  &.ant-menu-item,
  &.ant-dropdown-menu-item {
    span[role='button'] {
      display: inline-block;
      width: 100%;
    }
    transition-duration: 0s;
  }
`,i=(0,s.iK)(n.Z)`
  line-height: 51px;
  border: none;

  & > .ant-menu-item,
  & > .ant-menu-submenu {
    vertical-align: inherit;
    &:hover {
      color: ${({theme:e})=>e.colors.grayscale.dark1};
    }
  }

  &:not(.ant-menu-dark) > .ant-menu-submenu,
  &:not(.ant-menu-dark) > .ant-menu-item {
    &:hover {
      border-bottom: none;
    }
  }

  &:not(.ant-menu-dark) > .ant-menu-submenu,
  &:not(.ant-menu-dark) > .ant-menu-item {
    margin: 0px;
  }

  & > .ant-menu-item > a {
    padding: ${({theme:e})=>4*e.gridUnit}px;
  }
`,l=(0,s.iK)(n.Z.SubMenu)`
  color: ${({theme:e})=>e.colors.grayscale.dark1};
  border-bottom: none;
  .ant-menu-submenu-open,
  .ant-menu-submenu-active {
    background-color: ${({theme:e})=>e.colors.primary.light5};
    .ant-menu-submenu-title {
      color: ${({theme:e})=>e.colors.grayscale.dark1};
      background-color: ${({theme:e})=>e.colors.primary.light5};
      border-bottom: none;
      margin: 0;
      &:after {
        opacity: 1;
        width: calc(100% - 1);
      }
    }
  }
  .ant-menu-submenu-title {
    position: relative;
    top: ${({theme:e})=>-e.gridUnit-3}px;
    &:after {
      content: '';
      position: absolute;
      bottom: -3px;
      left: 50%;
      width: 0;
      height: 3px;
      opacity: 0;
      transform: translateX(-50%);
      transition: all ${({theme:e})=>e.transitionTiming}s;
      background-color: ${({theme:e})=>e.colors.primary.base};
    }
  }
  .ant-menu-submenu-arrow {
    top: 67%;
  }
  & > .ant-menu-submenu-title {
    padding: 0 ${({theme:e})=>6*e.gridUnit}px 0
      ${({theme:e})=>3*e.gridUnit}px !important;
    span[role='img'] {
      position: absolute;
      right: ${({theme:e})=>-e.gridUnit-2}px;
      top: ${({theme:e})=>5.25*e.gridUnit}px;
      svg {
        font-size: ${({theme:e})=>6*e.gridUnit}px;
        color: ${({theme:e})=>e.colors.grayscale.base};
      }
    }
    & > span {
      position: relative;
      top: 7px;
    }
    &:hover {
      color: ${({theme:e})=>e.colors.primary.base};
    }
  }
`,d=Object.assign(n.Z,{Item:a}),c=Object.assign(i,{Item:a,SubMenu:l,Divider:n.Z.Divider,ItemGroup:n.Z.ItemGroup});var p,u;(p="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.default:void 0)&&(p.register(a,"MenuItem","/Users/chenming/superset/superset-frontend/src/components/Menu/index.tsx"),p.register(i,"StyledNav","/Users/chenming/superset/superset-frontend/src/components/Menu/index.tsx"),p.register(l,"StyledSubMenu","/Users/chenming/superset/superset-frontend/src/components/Menu/index.tsx"),p.register(d,"Menu","/Users/chenming/superset/superset-frontend/src/components/Menu/index.tsx"),p.register(c,"MainNav","/Users/chenming/superset/superset-frontend/src/components/Menu/index.tsx")),(u="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.leaveModule:void 0)&&u(e)},509987:(e,t,r)=>{r.d(t,{Ph:()=>E,a7:()=>x,JY:()=>v,ZP:()=>U});var o,s=r(205872),n=r.n(s),a=r(682492),i=r.n(a),l=r(667294),d=r(229584),c=r(426678),p=r(795742),u=r(680454),g=r.n(u),_=r(751995),m=r(769756),f=r(747767),h=r(255083),b=r(211965);e=r.hmd(e),(o="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.enterModule:void 0)&&o(e);var y="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.default.signature:function(e){return e};function L(e){const t=(0,p.JN)(e,{withRef:!0}),r=f.ff;function o(o){let s;const{selectRef:a,labelKey:l="label",valueKey:u="value",themeConfig:y,stylesConfig:L={},optionRenderer:E,valueRenderer:x,valueRenderedAsLabel:v,onPaste:M,multi:U=!1,clearable:S,sortable:T=!0,forceOverflow:H,className:O=f.R5,classNamePrefix:G=f.t0,options:P,value:A,components:D,isMulti:w,isClearable:C,minMenuHeight:I=100,maxMenuHeight:R=220,filterOption:Z,ignoreAccents:W=!1,getOptionValue:B=(e=>"string"==typeof e?e:e[u]),getOptionLabel:$=(e=>"string"==typeof e?e:e[l]||e[u]),formatOptionLabel:k=((e,{context:t})=>"value"===t?x?x(e):$(e):E?E(e):$(e)),...K}=o,N=(0,h.dG)(A,P||[],u),q=void 0===w?U:w,z=void 0===C?S:C,j=q&&T&&Array.isArray(N)&&N.length>1,F=j?t:e,Y={...r,...D};if(j){Y.MultiValue=(V=Y.MultiValue||d.y.MultiValue,(0,p.W8)((e=>(0,b.tZ)(V,n()({},e,{innerProps:{onMouseDown:e=>{e.preventDefault(),e.stopPropagation()}}})))));const e={getHelperDimensions:({node:e})=>e.getBoundingClientRect(),axis:"xy",onSortEnd:({oldIndex:e,newIndex:t})=>{const r=g()(N,e,t);K.onChange&&K.onChange(r,{action:"set-value"})},distance:4};Object.assign(K,e)}var V;if((void 0===v?q:v)&&!L.valueContainer&&Object.assign(L,f.Qi),M){const e=Y.Input||d.y.Input;Y.Input=t=>(0,b.tZ)(e,n()({},t,{onPaste:M}))}e===m.NH&&(K.getNewOptionData=(e,t)=>({label:t||e,[u]:e,isNew:!0})),H&&Object.assign(K,{closeMenuOnScroll:e=>{var t,r,o;const n=null==(t=s)||null==(r=t.state)?void 0:r.menuIsOpen,a=e.target;return n&&a&&!(null!=(o=a.classList)&&o.contains("Select__menu-list"))},menuPosition:"fixed"});const X=(0,_.Fg)();return(0,b.tZ)(F,n()({ref:e=>{s=j&&e&&"refs"in e?e.refs.wrappedInstance:e,"function"==typeof a?a(s):a&&"current"in a&&(a.current=s)},className:O,classNamePrefix:G,isMulti:q,isClearable:z,options:P,value:N,minMenuHeight:I,maxMenuHeight:R,filterOption:void 0!==Z?Z:(0,c.c)({ignoreAccents:W}),styles:{...f.Ng,...L},theme:e=>i()(e,(0,f.uH)(X),y),formatOptionLabel:k,getOptionLabel:$,getOptionValue:B,components:Y},K))}return y(o,"useTheme{theme}",(()=>[_.Fg])),l.memo(o)}const E=L(m.lC),x=L(m.NH),v=L(m.jY),M=E,U=M;var S,T;(S="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.default:void 0)&&(S.register(L,"styled","/Users/chenming/superset/superset-frontend/src/components/Select/DeprecatedSelect.tsx"),S.register(E,"Select","/Users/chenming/superset/superset-frontend/src/components/Select/DeprecatedSelect.tsx"),S.register(x,"CreatableSelect","/Users/chenming/superset/superset-frontend/src/components/Select/DeprecatedSelect.tsx"),S.register(v,"AsyncCreatableSelect","/Users/chenming/superset/superset-frontend/src/components/Select/DeprecatedSelect.tsx"),S.register(M,"default","/Users/chenming/superset/superset-frontend/src/components/Select/DeprecatedSelect.tsx")),(T="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.leaveModule:void 0)&&T(e)},613309:(e,t,r)=>{var o,s=r(205872),n=r.n(s),a=(r(667294),r(751995)),i=r(564749),l=r(211965);e=r.hmd(e),(o="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.enterModule:void 0)&&o(e),"undefined"!=typeof reactHotLoaderGlobal&&reactHotLoaderGlobal.default.signature;const d=(0,a.iK)((e=>(0,l.tZ)(i.Z,n()({getPopupContainer:e=>e.parentNode},e))))`
  display: block;
`,c=(0,a.iK)(i.Z)`
  &.ant-select-single {
    .ant-select-selector {
      height: 36px;
      padding: 0 11px;
      background-color: ${({theme:e})=>e.colors.grayscale.light3};
      border: none;

      .ant-select-selection-search-input {
        height: 100%;
      }

      .ant-select-selection-item,
      .ant-select-selection-placeholder {
        line-height: 35px;
        color: ${({theme:e})=>e.colors.grayscale.dark1};
      }
    }
  }
`,p=Object.assign(d,{Option:i.Z.Option}),u=Object.assign(c,{Option:i.Z.Option});var g,_;(g="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.default:void 0)&&(g.register(d,"StyledNativeSelect","/Users/chenming/superset/superset-frontend/src/components/Select/NativeSelect.tsx"),g.register(c,"StyledNativeGraySelect","/Users/chenming/superset/superset-frontend/src/components/Select/NativeSelect.tsx"),g.register(p,"NativeSelect","/Users/chenming/superset/superset-frontend/src/components/Select/NativeSelect.tsx"),g.register(u,"NativeGraySelect","/Users/chenming/superset/superset-frontend/src/components/Select/NativeSelect.tsx")),(_="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.leaveModule:void 0)&&_(e)},339447:(e,t,r)=>{r.d(t,{Z:()=>p});var o,s,n,a=r(667294),i=r(274061),l=r(211965);function d(e){return Array.isArray(e)?e.findIndex((({props:{isFocused:e=!1}={}})=>e))||0:-1}function c({spacing:{baseUnit:e,lineHeight:t}}){return 4*e+t}function p({children:e,...t}){const{maxHeight:r,selectProps:o,theme:s,getStyles:n,cx:p,innerRef:u,isMulti:g,className:_}=t,{windowListRef:m,windowListInnerRef:f}=o,h=(0,a.useRef)(null),b=m||h;let{optionHeight:y}=o;y||(y=s?c(s):30);const L=y*e.length;return(0,a.useEffect)((()=>{const t=d(e);b.current&&t&&b.current.scrollToItem(t)}),[e,b]),(0,l.tZ)(i.t7,{css:n("menuList",t),className:p({"menu-list":!0,"menu-list--is-multi":g},_),ref:b,outerRef:u,innerRef:f,height:Math.min(L,r),width:"100%",itemData:e,itemCount:e.length,itemSize:y},(({data:e,index:t,style:r})=>(0,l.tZ)("div",{style:r},e[t])))}e=r.hmd(e),(o="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.enterModule:void 0)&&o(e),("undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.default.signature:function(e){return e})(p,"useRef{defaultWindowListRef}\nuseEffect{}"),(s="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.default:void 0)&&(s.register(30,"DEFAULT_OPTION_HEIGHT","/Users/chenming/superset/superset-frontend/src/components/Select/WindowedSelect/WindowedMenuList.tsx"),s.register(d,"getLastSelected","/Users/chenming/superset/superset-frontend/src/components/Select/WindowedSelect/WindowedMenuList.tsx"),s.register(c,"detectHeight","/Users/chenming/superset/superset-frontend/src/components/Select/WindowedSelect/WindowedMenuList.tsx"),s.register(p,"WindowedMenuList","/Users/chenming/superset/superset-frontend/src/components/Select/WindowedSelect/WindowedMenuList.tsx")),(n="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.leaveModule:void 0)&&n(e)},769756:(e,t,r)=>{r.d(t,{lC:()=>l,NH:()=>d,jY:()=>c});var o,s=r(537789),n=r(912766),a=r(800320),i=r(271977);e=r.hmd(e),(o="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.enterModule:void 0)&&o(e),"undefined"!=typeof reactHotLoaderGlobal&&reactHotLoaderGlobal.default.signature;const l=(0,i.ZP)(s.ZP),d=(0,i.ZP)(n.ZP),c=(0,i.ZP)(a.Z),p=l;var u,g;(u="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.default:void 0)&&(u.register(l,"WindowedSelect","/Users/chenming/superset/superset-frontend/src/components/Select/WindowedSelect/index.tsx"),u.register(d,"WindowedCreatableSelect","/Users/chenming/superset/superset-frontend/src/components/Select/WindowedSelect/index.tsx"),u.register(c,"WindowedAsyncCreatableSelect","/Users/chenming/superset/superset-frontend/src/components/Select/WindowedSelect/index.tsx"),u.register(p,"default","/Users/chenming/superset/superset-frontend/src/components/Select/WindowedSelect/index.tsx")),(g="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.leaveModule:void 0)&&g(e)},271977:(e,t,r)=>{r.d(t,{ZP:()=>g});var o,s=r(205872),n=r.n(s),a=r(667294),i=r(229584),l=r(339447),d=r(211965);e=r.hmd(e),(o="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.enterModule:void 0)&&o(e),"undefined"!=typeof reactHotLoaderGlobal&&reactHotLoaderGlobal.default.signature;const{MenuList:c}=i.y,p=100;function u({children:e,...t}){const{windowThreshold:r=p}=t.selectProps;return Array.isArray(e)&&e.length>r?(0,d.tZ)(l.Z,t,e):(0,d.tZ)(c,t,e)}function g(e){function t(t,r){const{components:o={},...s}=t,a={...o,MenuList:u};return(0,d.tZ)(e,n()({components:a,ref:r},s))}return(0,a.forwardRef)(t)}var _,m;(_="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.default:void 0)&&(_.register(c,"DefaultMenuList","/Users/chenming/superset/superset-frontend/src/components/Select/WindowedSelect/windowed.tsx"),_.register(p,"DEFAULT_WINDOW_THRESHOLD","/Users/chenming/superset/superset-frontend/src/components/Select/WindowedSelect/windowed.tsx"),_.register(u,"MenuList","/Users/chenming/superset/superset-frontend/src/components/Select/WindowedSelect/windowed.tsx"),_.register(g,"windowed","/Users/chenming/superset/superset-frontend/src/components/Select/WindowedSelect/windowed.tsx")),(m="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.leaveModule:void 0)&&m(e)},93719:(e,t,r)=>{r.d(t,{JY:()=>o.JY,a7:()=>o.a7,Ph:()=>o.Ph,ZP:()=>o.ZP});var o=r(509987);r(747767),r(975017),r(613309),"undefined"!=typeof reactHotLoaderGlobal&&reactHotLoaderGlobal.default.signature},747767:(e,t,r)=>{r.d(t,{R5:()=>l,t0:()=>d,uH:()=>p,Ng:()=>u,ff:()=>y,Qi:()=>L});var o,s=r(205872),n=r.n(s),a=(r(667294),r(211965)),i=r(229584);e=r.hmd(e),(o="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.enterModule:void 0)&&o(e),"undefined"!=typeof reactHotLoaderGlobal&&reactHotLoaderGlobal.default.signature;const l="Select",d="Select",c=e=>({primary:e.colors.success.base,danger:e.colors.error.base,warning:e.colors.warning.base,indicator:e.colors.info.base,almostBlack:e.colors.grayscale.dark1,grayDark:e.colors.grayscale.dark1,grayLight:e.colors.grayscale.light2,gray:e.colors.grayscale.light1,grayBg:e.colors.grayscale.light4,grayBgDarker:e.colors.grayscale.light3,grayBgDarkest:e.colors.grayscale.light2,grayHeading:e.colors.grayscale.light1,menuHover:e.colors.grayscale.light3,lightest:e.colors.grayscale.light5,darkest:e.colors.grayscale.dark2,grayBorder:e.colors.grayscale.light2,grayBorderLight:e.colors.grayscale.light3,grayBorderDark:e.colors.grayscale.light1,textDefault:e.colors.grayscale.dark1,textDarkest:e.colors.grayscale.dark2,dangerLight:e.colors.error.light1}),p=e=>({borderRadius:e.borderRadius,zIndex:11,colors:c(e),spacing:{baseUnit:3,menuGutter:0,controlHeight:34,lineHeight:19,fontSize:14,minWidth:"6.5em"}}),u={container:(e,{theme:{spacing:{minWidth:t}}})=>[e,a.iv`
      min-width: ${t};
    `],placeholder:e=>[e,a.iv`
      white-space: nowrap;
    `],indicatorSeparator:()=>a.iv`
    display: none;
  `,indicatorsContainer:e=>[e,a.iv`
      i {
        width: 1em;
        display: inline-block;
      }
    `],clearIndicator:e=>[e,a.iv`
      padding: 4px 0 4px 6px;
    `],control:(e,{isFocused:t,menuIsOpen:r,theme:{borderRadius:o,colors:s}})=>{const n=t&&!r;let i=s.grayBorder;return(n||r)&&(i=s.grayBorderDark),[e,a.iv`
        border-color: ${i};
        box-shadow: ${n?"inset 0 1px 1px rgba(0,0,0,.075), 0 0 0 3px rgba(0,0,0,.1)":"none"};
        border-radius: ${r?`${o}px ${o}px 0 0`:`${o}px`};
        &:hover {
          border-color: ${i};
          box-shadow: 0 1px 0 rgba(0, 0, 0, 0.06);
        }
        flex-wrap: nowrap;
        padding-left: 1px;
      `]},menu:(e,{theme:{zIndex:t}})=>[e,a.iv`
      padding-bottom: 2em;
      z-index: ${t}; /* override at least multi-page pagination */
      width: auto;
      min-width: 100%;
      max-width: 80vw;
      background: none;
      box-shadow: none;
      border: 0;
    `],menuList:(e,{theme:{borderRadius:t,colors:r}})=>[e,a.iv`
      background: ${r.lightest};
      border-radius: 0 0 ${t}px ${t}px;
      border: 1px solid ${r.grayBorderDark};
      box-shadow: 0 1px 0 rgba(0, 0, 0, 0.06);
      margin-top: -1px;
      border-top-color: ${r.grayBorderLight};
      min-width: 100%;
      width: auto;
      border-radius: 0 0 ${t}px ${t}px;
      padding-top: 0;
      padding-bottom: 0;
    `],option:(e,{isDisabled:t,isFocused:r,isSelected:o,theme:{colors:s,spacing:{lineHeight:n,fontSize:i}}})=>{let l=s.textDefault,d=s.lightest;return r?d=s.grayBgDarker:t&&(l="#ccc"),[e,a.iv`
        cursor: pointer;
        line-height: ${n}px;
        font-size: ${i}px;
        background-color: ${d};
        color: ${l};
        font-weight: ${o?600:400};
        white-space: nowrap;
        &:hover:active {
          background-color: ${s.grayBg};
        }
      `]},valueContainer:(e,{isMulti:t,hasValue:r,theme:{spacing:{baseUnit:o}}})=>[e,a.iv`
      padding-left: ${t&&r?1:3*o}px;
    `],multiValueLabel:(e,{theme:{spacing:{baseUnit:t}}})=>({...e,paddingLeft:1.2*t,paddingRight:1.2*t}),input:(e,{selectProps:t})=>{var r;return[e,a.iv`
      margin-left: 0;
      vertical-align: middle;
      ${null!=t&&t.isMulti&&null!=t&&null!=(r=t.value)&&r.length?"padding: 0 6px; width: 100%":"padding: 0; flex: 1 1 auto;"};
    `]},menuPortal:e=>({...e,zIndex:1030})},g={background:"none",border:"none",outline:"none",padding:0},{ClearIndicator:_,DropdownIndicator:m,Option:f,Input:h,SelectContainer:b}=i.y,y={SelectContainer:({children:e,...t})=>{const{selectProps:{assistiveText:r}}=t;return(0,a.tZ)("div",null,(0,a.tZ)(b,t,e),r&&(0,a.tZ)("span",{css:e=>({marginLeft:3,fontSize:e.typography.sizes.s,color:e.colors.grayscale.light1})},r))},Option:({children:e,innerProps:t,data:r,...o})=>(0,a.tZ)(f,n()({},o,{data:r,css:null!=r&&r.style?r.style:null,innerProps:t}),e),ClearIndicator:e=>(0,a.tZ)(_,e,(0,a.tZ)("i",{className:"fa"},"×")),DropdownIndicator:e=>(0,a.tZ)(m,e,(0,a.tZ)("i",{className:"fa fa-caret-"+(e.selectProps.menuIsOpen?"up":"down")})),Input:e=>{const{getStyles:t}=e;return(0,a.tZ)(h,n()({},e,{css:t("input",e),autoComplete:"chrome-off",inputStyle:g}))}},L={valueContainer:(e,{getValue:t,theme:{spacing:{baseUnit:r}},isMulti:o})=>({...e,paddingLeft:t().length>0?1:3*r,overflow:o&&t().length>0?"visible":"hidden"}),singleValue:(e,t)=>{const{getStyles:r}=t;return{...r("multiValue",t),".metric-option":r("multiValueLabel",t)}}};var E,x;(E="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.default:void 0)&&(E.register(l,"DEFAULT_CLASS_NAME","/Users/chenming/superset/superset-frontend/src/components/Select/styles.tsx"),E.register(d,"DEFAULT_CLASS_NAME_PREFIX","/Users/chenming/superset/superset-frontend/src/components/Select/styles.tsx"),E.register(c,"colors","/Users/chenming/superset/superset-frontend/src/components/Select/styles.tsx"),E.register(p,"defaultTheme","/Users/chenming/superset/superset-frontend/src/components/Select/styles.tsx"),E.register(u,"DEFAULT_STYLES","/Users/chenming/superset/superset-frontend/src/components/Select/styles.tsx"),E.register(g,"INPUT_TAG_BASE_STYLES","/Users/chenming/superset/superset-frontend/src/components/Select/styles.tsx"),E.register(_,"ClearIndicator","/Users/chenming/superset/superset-frontend/src/components/Select/styles.tsx"),E.register(m,"DropdownIndicator","/Users/chenming/superset/superset-frontend/src/components/Select/styles.tsx"),E.register(f,"Option","/Users/chenming/superset/superset-frontend/src/components/Select/styles.tsx"),E.register(h,"Input","/Users/chenming/superset/superset-frontend/src/components/Select/styles.tsx"),E.register(b,"SelectContainer","/Users/chenming/superset/superset-frontend/src/components/Select/styles.tsx"),E.register(y,"DEFAULT_COMPONENTS","/Users/chenming/superset/superset-frontend/src/components/Select/styles.tsx"),E.register(L,"VALUE_LABELED_STYLES","/Users/chenming/superset/superset-frontend/src/components/Select/styles.tsx")),(x="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.leaveModule:void 0)&&x(e)},971989:(e,t,r)=>{r.d(t,{Xv:()=>m,cl:()=>h,ZP:()=>y});var o,s=r(205872),n=r.n(s),a=(r(667294),r(211965)),i=r(751995),l=r(901350),d=r(87693);e=r.hmd(e),(o="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.enterModule:void 0)&&o(e),"undefined"!=typeof reactHotLoaderGlobal&&reactHotLoaderGlobal.default.signature;const c=({animated:e=!1,fullWidth:t=!0,allowOverflow:r=!0,...o})=>(0,a.tZ)(l.default,n()({animated:e},o,{css:e=>a.iv`
      overflow: ${r?"visible":"hidden"};

      .ant-tabs-content-holder {
        overflow: ${r?"visible":"auto"};
      }
      .ant-tabs-tab {
        flex: 1 1 auto;
        &.ant-tabs-tab-active .ant-tabs-tab-btn {
          color: inherit;
        }
        &:hover {
          .anchor-link-container {
            cursor: pointer;
            .fa.fa-link {
              visibility: visible;
            }
          }
        }
        .short-link-trigger.btn {
          padding: 0 ${e.gridUnit}px;
          & > .fa.fa-link {
            top: 0;
          }
        }
      }
      ${t&&a.iv`
        .ant-tabs-nav-list {
          width: 100%;
        }
      `};

      .ant-tabs-tab-btn {
        display: flex;
        flex: 1 1 auto;
        align-items: center;
        justify-content: center;
        font-size: ${e.typography.sizes.s}px;
        text-align: center;
        text-transform: uppercase;
        user-select: none;
        .required {
          margin-left: ${e.gridUnit/2}px;
          color: ${e.colors.error.base};
        }
      }
      .ant-tabs-ink-bar {
        background: ${e.colors.secondary.base};
      }
    `})),p=(0,i.iK)(l.default.TabPane)``,u=Object.assign(c,{TabPane:p}),g=(0,i.iK)(c)`
  .ant-tabs-content-holder {
    background: white;
  }

  & > .ant-tabs-nav {
    margin-bottom: 0;
  }

  .ant-tabs-tab-remove {
    padding-top: 0;
    padding-bottom: 0;
    height: ${({theme:e})=>6*e.gridUnit}px;
  }

  ${({fullWidth:e})=>e&&a.iv`
      .ant-tabs-nav-list {
        width: 100%;
      }
    `}
`,_=(0,i.iK)(d.Z.CancelX)`
  color: ${({theme:e})=>e.colors.grayscale.base};
`,m=Object.assign(g,{TabPane:p});m.defaultProps={type:"editable-card",fullWidth:!1,animated:{inkBar:!0,tabPane:!1}},m.TabPane.defaultProps={closeIcon:(0,a.tZ)(_,{role:"button",tabIndex:0})};const f=(0,i.iK)(m)`
  &.ant-tabs-card > .ant-tabs-nav .ant-tabs-tab {
    margin: 0 ${({theme:e})=>4*e.gridUnit}px;
    padding: ${({theme:e})=>`${3*e.gridUnit}px ${e.gridUnit}px`};
    background: transparent;
    border: none;
  }

  &.ant-tabs-card > .ant-tabs-nav .ant-tabs-ink-bar {
    visibility: visible;
  }

  .ant-tabs-tab-btn {
    font-size: ${({theme:e})=>e.typography.sizes.m}px;
  }

  .ant-tabs-tab-remove {
    margin-left: 0;
    padding-right: 0;
  }

  .ant-tabs-nav-add {
    min-width: unset !important;
    background: transparent !important;
    border: none !important;
  }
`,h=Object.assign(f,{TabPane:p}),b=u,y=b;var L,E;(L="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.default:void 0)&&(L.register(c,"StyledTabs","/Users/chenming/superset/superset-frontend/src/components/Tabs/Tabs.tsx"),L.register(p,"StyledTabPane","/Users/chenming/superset/superset-frontend/src/components/Tabs/Tabs.tsx"),L.register(u,"Tabs","/Users/chenming/superset/superset-frontend/src/components/Tabs/Tabs.tsx"),L.register(g,"StyledEditableTabs","/Users/chenming/superset/superset-frontend/src/components/Tabs/Tabs.tsx"),L.register(_,"StyledCancelXIcon","/Users/chenming/superset/superset-frontend/src/components/Tabs/Tabs.tsx"),L.register(m,"EditableTabs","/Users/chenming/superset/superset-frontend/src/components/Tabs/Tabs.tsx"),L.register(f,"StyledLineEditableTabs","/Users/chenming/superset/superset-frontend/src/components/Tabs/Tabs.tsx"),L.register(h,"LineEditableTabs","/Users/chenming/superset/superset-frontend/src/components/Tabs/Tabs.tsx"),L.register(b,"default","/Users/chenming/superset/superset-frontend/src/components/Tabs/Tabs.tsx")),(E="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.leaveModule:void 0)&&E(e)},940637:(e,t,r)=>{r.d(t,{Xv:()=>o.Xv,cl:()=>o.cl,ZP:()=>o.ZP});var o=r(971989);"undefined"!=typeof reactHotLoaderGlobal&&reactHotLoaderGlobal.default.signature},486057:(e,t,r)=>{r.d(t,{Z:()=>p});var o,s=r(211965),n=(r(667294),r(751995)),a=r(178186),i=r(87693),l=r(358593);function d({warningMarkdown:e,size:t}){const r=(0,n.Fg)();return(0,s.tZ)(l.u,{id:"warning-tooltip",title:(0,s.tZ)(a.Z,{source:e})},(0,s.tZ)(i.Z.AlertSolid,{iconColor:r.colors.alert.base,iconSize:t,css:(0,s.iv)({marginRight:2*r.gridUnit},"","")}))}e=r.hmd(e),(o="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.enterModule:void 0)&&o(e),("undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.default.signature:function(e){return e})(d,"useTheme{theme}",(()=>[n.Fg]));const c=d,p=c;var u,g;(u="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.default:void 0)&&(u.register(d,"WarningIconWithTooltip","/Users/chenming/superset/superset-frontend/src/components/WarningIconWithTooltip/index.tsx"),u.register(c,"default","/Users/chenming/superset/superset-frontend/src/components/WarningIconWithTooltip/index.tsx")),(g="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.leaveModule:void 0)&&g(e)},599543:(e,t,r)=>{r.d(t,{SJ:()=>y,wK:()=>L,gf:()=>E,gP:()=>x,p1:()=>v,_0:()=>M,zd:()=>U,hU:()=>S,E8:()=>T,JB:()=>H});var o,s,n,a=r(845220),i=r.n(a),l=r(352353),d=r.n(l),c=r(114176),p=r.n(c),u=r(618446),g=r.n(u),_=r(714670),m=r.n(_),f=r(14890),h=r(964417),b=r.n(h);function y(e,t,r){const o={...e[t]},s={...r};return s.id||(s.id=m().generate()),o[s.id]=s,{...e,[t]:o}}function L(e,t,r,o){const s={...e[t]};return s[r.id]={...s[r.id],...o},{...e,[t]:s}}function E(e,t,r,o,s="id"){const n=[];return e[t].forEach((e=>{r[s]===e[s]?n.push({...e,...o}):n.push(e)})),{...e,[t]:n}}function x(e,t,r,o="id"){const s=[];return e[t].forEach((e=>{r[o]!==e[o]&&s.push(e)})),{...e,[t]:s}}function v(e,t){let r;return e.forEach((e=>{e.id===t&&(r=e)})),r}function M(e,t,r,o=!1){const s={...r};s.id||(s.id=m().generate());const n={};return n[t]=o?[s,...e[t]]:[...e[t],s],{...e,...n}}function U(e,t,r,o=!1){const s=[...r];s.forEach((e=>{e.id||(e.id=m().generate())}));const n={};return n[t]=o?[...s,...e[t]]:[...e[t],...s],{...e,...n}}function S(e=!0,t={}){const{paths:r,config:o}=t,s=f.qC;return e?s(b()(r,o)):s()}function T(e,t){if(!e||!t)return!1;if(e.length!==t.length)return!1;const{length:r}=e;for(let o=0;o<r;o+=1)if(e[o]!==t[o])return!1;return!0}function H(e,t,r={ignoreUndefined:!1,ignoreNull:!1}){let o=e,s=t;return r.ignoreUndefined&&(o=p()(o,d()),s=p()(s,d())),r.ignoreNull&&(o=p()(o,i()),s=p()(s,i())),g()(o,s)}e=r.hmd(e),(o="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.enterModule:void 0)&&o(e),"undefined"!=typeof reactHotLoaderGlobal&&reactHotLoaderGlobal.default.signature,(s="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.default:void 0)&&(s.register(y,"addToObject","/Users/chenming/superset/superset-frontend/src/reduxUtils.ts"),s.register(L,"alterInObject","/Users/chenming/superset/superset-frontend/src/reduxUtils.ts"),s.register(E,"alterInArr","/Users/chenming/superset/superset-frontend/src/reduxUtils.ts"),s.register(x,"removeFromArr","/Users/chenming/superset/superset-frontend/src/reduxUtils.ts"),s.register(v,"getFromArr","/Users/chenming/superset/superset-frontend/src/reduxUtils.ts"),s.register(M,"addToArr","/Users/chenming/superset/superset-frontend/src/reduxUtils.ts"),s.register(U,"extendArr","/Users/chenming/superset/superset-frontend/src/reduxUtils.ts"),s.register(S,"initEnhancer","/Users/chenming/superset/superset-frontend/src/reduxUtils.ts"),s.register(T,"areArraysShallowEqual","/Users/chenming/superset/superset-frontend/src/reduxUtils.ts"),s.register(H,"areObjectsEqual","/Users/chenming/superset/superset-frontend/src/reduxUtils.ts")),(n="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.leaveModule:void 0)&&n(e)}}]);
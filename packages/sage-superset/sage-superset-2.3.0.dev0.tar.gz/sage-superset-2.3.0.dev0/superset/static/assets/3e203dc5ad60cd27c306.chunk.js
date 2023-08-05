"use strict";(globalThis.webpackChunksuperset=globalThis.webpackChunksuperset||[]).push([[7633],{715073:(e,t,r)=>{r.r(t),r.d(t,{default:()=>T});var s,a=r(667294),o=r(751995),n=r(455867),i=r(431069),l=r(730381),u=r.n(l),d=r(440768),c=r(414114),p=r(34858),g=r(620755),y=r(976697),h=r(495413),m=r(550859),b=r(358593),f=r(242110),v=r(833743),w=r(600120),Z=r(427600),q=r(400012),x=r(87693),C=r(824527),L=r(211965);e=r.hmd(e),(s="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.enterModule:void 0)&&s(e);var U="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.default.signature:function(e){return e};const S=(0,o.iK)(m.Z)`
  table .table-cell {
    vertical-align: top;
  }
`;f.Z.registerLanguage("sql",v.Z);const H=(0,o.iK)(f.Z)`
  height: ${({theme:e})=>26*e.gridUnit}px;
  overflow: hidden !important; /* needed to override inline styles */
  text-overflow: ellipsis;
  white-space: nowrap;
`,Q=o.iK.div`
  .count {
    margin-left: 5px;
    color: ${({theme:e})=>e.colors.primary.base};
    text-decoration: underline;
    cursor: pointer;
  }
`,$=o.iK.div`
  color: ${({theme:e})=>e.colors.grayscale.dark2};
`;function D({addDangerToast:e,addSuccessToast:t}){const{state:{loading:r,resourceCount:s,resourceCollection:l},fetchData:c}=(0,p.Yi)("query",(0,n.t)("Query history"),e,!1),[f,v]=(0,a.useState)(),U=(0,o.Fg)(),D=(0,a.useCallback)((t=>{i.Z.get({endpoint:`/api/v1/query/${t}`}).then((({json:e={}})=>{v({...e.result})}),(0,d.v$)((t=>e((0,n.t)("There was an issue previewing the selected query. %s",t)))))}),[e]),k={activeChild:"Query history",...h.Y},T=[{id:q.J.start_time,desc:!0}],R=(0,a.useMemo)((()=>[{Cell:({row:{original:{status:e}}})=>{const t={name:null,label:""};return"success"===e?(t.name=(0,L.tZ)(x.Z.Check,{iconColor:U.colors.success.base}),t.label=(0,n.t)("Success")):"failed"===e||"stopped"===e?(t.name=(0,L.tZ)(x.Z.XSmall,{iconColor:"failed"===e?U.colors.error.base:U.colors.grayscale.base}),t.label=(0,n.t)("Failed")):"running"===e?(t.name=(0,L.tZ)(x.Z.Running,{iconColor:U.colors.primary.base}),t.label=(0,n.t)("Running")):"timed_out"===e?(t.name=(0,L.tZ)(x.Z.Offline,{iconColor:U.colors.grayscale.light1}),t.label=(0,n.t)("Offline")):"scheduled"!==e&&"pending"!==e||(t.name=(0,L.tZ)(x.Z.Queued,{iconColor:U.colors.grayscale.base}),t.label=(0,n.t)("Scheduled")),(0,L.tZ)(b.u,{title:t.label,placement:"bottom"},(0,L.tZ)("span",null,t.name))},accessor:q.J.status,size:"xs",disableSortBy:!0},{accessor:q.J.start_time,Header:(0,n.t)("Time"),size:"xl",Cell:({row:{original:{start_time:e,end_time:t}}})=>{const r=u().utc(e).local().format(Z.v2).split(" "),s=(0,L.tZ)(a.Fragment,null,r[0]," ",(0,L.tZ)("br",null),r[1]);return t?(0,L.tZ)(b.u,{title:(0,n.t)("Duration: %s",u()(u().utc(t-e)).format(Z.n2)),placement:"bottom"},(0,L.tZ)("span",null,s)):s}},{accessor:q.J.tab_name,Header:(0,n.t)("Tab name"),size:"xl"},{accessor:q.J.database_name,Header:(0,n.t)("Database"),size:"xl"},{accessor:q.J.database,hidden:!0},{accessor:q.J.schema,Header:(0,n.t)("Schema"),size:"xl"},{Cell:({row:{original:{sql_tables:e=[]}}})=>{const t=e.map((e=>e.table)),r=t.length>0?t.shift():"";return t.length?(0,L.tZ)(Q,null,(0,L.tZ)("span",null,r),(0,L.tZ)(y.Z,{placement:"right",title:(0,n.t)("TABLES"),trigger:"click",content:(0,L.tZ)(a.Fragment,null,t.map((e=>(0,L.tZ)($,{key:e},e))))},(0,L.tZ)("span",{className:"count"},"(+",t.length,")"))):r},accessor:q.J.sql_tables,Header:(0,n.t)("Tables"),size:"xl",disableSortBy:!0},{accessor:q.J.user_first_name,Header:(0,n.t)("User"),size:"xl",Cell:({row:{original:{user:e}}})=>e?`${e.first_name} ${e.last_name}`:""},{accessor:q.J.user,hidden:!0},{accessor:q.J.rows,Header:(0,n.t)("Rows"),size:"md"},{accessor:q.J.sql,Header:(0,n.t)("SQL"),Cell:({row:{original:e,id:t}})=>(0,L.tZ)("div",{tabIndex:0,role:"button","data-test":`open-sql-preview-${t}`,onClick:()=>v(e)},(0,L.tZ)(H,{language:"sql",style:w.Z},(0,d.IB)(e.sql,4)))},{Header:(0,n.t)("Actions"),id:"actions",disableSortBy:!0,Cell:({row:{original:{id:e}}})=>(0,L.tZ)(b.u,{title:(0,n.t)("Open query in SQL Lab"),placement:"bottom"},(0,L.tZ)("a",{href:`/superset/sqllab?queryId=${e}`},(0,L.tZ)(x.Z.Full,{iconColor:U.colors.grayscale.base})))}]),[]),_=(0,a.useMemo)((()=>[{Header:(0,n.t)("Database"),id:"database",input:"select",operator:m.p.relationOneMany,unfilteredLabel:"All",fetchSelects:(0,d.tm)("query","database",(0,d.v$)((t=>e((0,n.t)("An error occurred while fetching database values: %s",t))))),paginate:!0},{Header:(0,n.t)("State"),id:"status",input:"select",operator:m.p.equals,unfilteredLabel:"All",fetchSelects:(0,d.wk)("query","status",(0,d.v$)((t=>e((0,n.t)("An error occurred while fetching schema values: %s",t))))),paginate:!0},{Header:(0,n.t)("User"),id:"user",input:"select",operator:m.p.relationOneMany,unfilteredLabel:"All",fetchSelects:(0,d.tm)("query","user",(0,d.v$)((t=>e((0,n.t)("An error occurred while fetching user values: %s",t))))),paginate:!0},{Header:(0,n.t)("Time range"),id:"start_time",input:"datetime_range",operator:m.p.between},{Header:(0,n.t)("Search by query text"),id:"sql",input:"search",operator:m.p.contains}]),[e]);return(0,L.tZ)(a.Fragment,null,(0,L.tZ)(g.Z,k),f&&(0,L.tZ)(C.Z,{onHide:()=>v(void 0),query:f,queries:l,fetchData:D,openInSqlLab:e=>window.location.assign(`/superset/sqllab?queryId=${e}`),show:!0}),(0,L.tZ)(S,{className:"query-history-list-view",columns:R,count:s,data:l,fetchData:c,filters:_,initialSort:T,loading:r,pageSize:25,highlightRowId:null==f?void 0:f.id}))}U(D,"useListViewResource{{ state: { loading, resourceCount: queryCount, resourceCollection: queries }, fetchData, }}\nuseState{[queryCurrentlyPreviewing, setQueryCurrentlyPreviewing]}\nuseTheme{theme}\nuseCallback{handleQueryPreview}\nuseMemo{columns}\nuseMemo{filters}",(()=>[p.Yi,o.Fg]));const k=(0,c.Z)(D),T=k;var R,_;(R="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.default:void 0)&&(R.register(25,"PAGE_SIZE","/Users/chenming/superset/superset-frontend/src/views/CRUD/data/query/QueryList.tsx"),R.register(4,"SQL_PREVIEW_MAX_LINES","/Users/chenming/superset/superset-frontend/src/views/CRUD/data/query/QueryList.tsx"),R.register(S,"TopAlignedListView","/Users/chenming/superset/superset-frontend/src/views/CRUD/data/query/QueryList.tsx"),R.register(H,"StyledSyntaxHighlighter","/Users/chenming/superset/superset-frontend/src/views/CRUD/data/query/QueryList.tsx"),R.register(Q,"StyledTableLabel","/Users/chenming/superset/superset-frontend/src/views/CRUD/data/query/QueryList.tsx"),R.register($,"StyledPopoverItem","/Users/chenming/superset/superset-frontend/src/views/CRUD/data/query/QueryList.tsx"),R.register(D,"QueryList","/Users/chenming/superset/superset-frontend/src/views/CRUD/data/query/QueryList.tsx"),R.register(k,"default","/Users/chenming/superset/superset-frontend/src/views/CRUD/data/query/QueryList.tsx")),(_="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.leaveModule:void 0)&&_(e)},824527:(e,t,r)=>{r.d(t,{Z:()=>x});var s,a=r(667294),o=r(751995),n=r(455867),i=r(574520),l=r(294184),u=r.n(l),d=r(835932),c=r(414114),p=r(331673),g=r(14025),y=r(211965);e=r.hmd(e),(s="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.enterModule:void 0)&&s(e);var h="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.default.signature:function(e){return e};const m=o.iK.div`
  color: ${({theme:e})=>e.colors.secondary.light2};
  font-size: ${({theme:e})=>e.typography.sizes.s-1}px;
  margin-bottom: 0;
  text-transform: uppercase;
`,b=o.iK.div`
  color: ${({theme:e})=>e.colors.grayscale.dark2};
  font-size: ${({theme:e})=>e.typography.sizes.m-1}px;
  padding: 4px 0 24px 0;
`,f=o.iK.div`
  margin: 0 0 ${({theme:e})=>6*e.gridUnit}px 0;
`,v=o.iK.div`
  display: inline;
  font-size: ${({theme:e})=>e.typography.sizes.s}px;
  padding: ${({theme:e})=>2*e.gridUnit}px
    ${({theme:e})=>4*e.gridUnit}px;
  margin-right: ${({theme:e})=>4*e.gridUnit}px;
  color: ${({theme:e})=>e.colors.secondary.dark1};

  &.active,
  &:focus,
  &:hover {
    background: ${({theme:e})=>e.colors.secondary.light4};
    border-bottom: none;
    border-radius: ${({theme:e})=>e.borderRadius}px;
    margin-bottom: ${({theme:e})=>2*e.gridUnit}px;
  }

  &:hover:not(.active) {
    background: ${({theme:e})=>e.colors.secondary.light5};
  }
`,w=(0,o.iK)(i.Z)`
  .ant-modal-body {
    padding: ${({theme:e})=>6*e.gridUnit}px;
  }

  pre {
    font-size: ${({theme:e})=>e.typography.sizes.xs}px;
    font-weight: ${({theme:e})=>e.typography.weights.normal};
    line-height: ${({theme:e})=>e.typography.sizes.l}px;
    height: 375px;
    border: none;
  }
`;function Z({onHide:e,openInSqlLab:t,queries:r,query:s,fetchData:o,show:i,addDangerToast:l,addSuccessToast:c}){const{handleKeyPress:h,handleDataChange:Z,disablePrevious:q,disableNext:x}=(0,g.C)({queries:r,currentQueryId:s.id,fetchData:o}),[C,L]=(0,a.useState)("user"),{id:U,sql:S,executed_sql:H}=s;return(0,y.tZ)("div",{role:"none",onKeyUp:h},(0,y.tZ)(w,{onHide:e,show:i,title:(0,n.t)("Query preview"),footer:[(0,y.tZ)(d.Z,{"data-test":"previous-query",key:"previous-query",disabled:q,onClick:()=>Z(!0)},(0,n.t)("Previous")),(0,y.tZ)(d.Z,{"data-test":"next-query",key:"next-query",disabled:x,onClick:()=>Z(!1)},(0,n.t)("Next")),(0,y.tZ)(d.Z,{"data-test":"open-in-sql-lab",key:"open-in-sql-lab",buttonStyle:"primary",onClick:()=>t(U)},(0,n.t)("Open in SQL Lab"))]},(0,y.tZ)(m,null,(0,n.t)("Tab name")),(0,y.tZ)(b,null,s.tab_name),(0,y.tZ)(f,null,(0,y.tZ)(v,{role:"button","data-test":"toggle-user-sql",className:u()({active:"user"===C}),onClick:()=>L("user")},(0,n.t)("User query")),(0,y.tZ)(v,{role:"button","data-test":"toggle-executed-sql",className:u()({active:"executed"===C}),onClick:()=>L("executed")},(0,n.t)("Executed query"))),(0,y.tZ)(p.Z,{addDangerToast:l,addSuccessToast:c,language:"sql"},("user"===C?S:H)||"")))}h(Z,"useQueryPreviewState{{ handleKeyPress, handleDataChange, disablePrevious, disableNext }}\nuseState{[currentTab, setCurrentTab]('user')}",(()=>[g.C]));const q=(0,c.Z)(Z),x=q;var C,L;(C="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.default:void 0)&&(C.register(m,"QueryTitle","/Users/chenming/superset/superset-frontend/src/views/CRUD/data/query/QueryPreviewModal.tsx"),C.register(b,"QueryLabel","/Users/chenming/superset/superset-frontend/src/views/CRUD/data/query/QueryPreviewModal.tsx"),C.register(f,"QueryViewToggle","/Users/chenming/superset/superset-frontend/src/views/CRUD/data/query/QueryPreviewModal.tsx"),C.register(v,"TabButton","/Users/chenming/superset/superset-frontend/src/views/CRUD/data/query/QueryPreviewModal.tsx"),C.register(w,"StyledModal","/Users/chenming/superset/superset-frontend/src/views/CRUD/data/query/QueryPreviewModal.tsx"),C.register(Z,"QueryPreviewModal","/Users/chenming/superset/superset-frontend/src/views/CRUD/data/query/QueryPreviewModal.tsx"),C.register(q,"default","/Users/chenming/superset/superset-frontend/src/views/CRUD/data/query/QueryPreviewModal.tsx")),(L="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.leaveModule:void 0)&&L(e)}}]);
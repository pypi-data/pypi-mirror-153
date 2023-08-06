"use strict";(globalThis.webpackChunksuperset=globalThis.webpackChunksuperset||[]).push([[9173],{727989:(e,t,a)=>{a.d(t,{Z:()=>v});var r,s=a(667294),o=a(751995),n=a(455867),i=a(835932),l=a(574520),d=a(104715),u=a(34858),c=a(211965);e=a.hmd(e),(r="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.enterModule:void 0)&&r(e);var p="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.default.signature:function(e){return e};const m=o.iK.div`
  display: block;
  color: ${({theme:e})=>e.colors.grayscale.base};
  font-size: ${({theme:e})=>e.typography.sizes.s-1}px;
`,g=o.iK.div`
  padding-bottom: ${({theme:e})=>2*e.gridUnit}px;
  padding-top: ${({theme:e})=>2*e.gridUnit}px;

  & > div {
    margin: ${({theme:e})=>e.gridUnit}px 0;
  }

  &.extra-container {
    padding-top: 8px;
  }

  .confirm-overwrite {
    margin-bottom: ${({theme:e})=>2*e.gridUnit}px;
  }

  .input-container {
    display: flex;
    align-items: center;

    label {
      display: flex;
      margin-right: ${({theme:e})=>2*e.gridUnit}px;
    }

    i {
      margin: 0 ${({theme:e})=>e.gridUnit}px;
    }
  }

  input,
  textarea {
    flex: 1 1 auto;
  }

  textarea {
    height: 160px;
    resize: none;
  }

  input::placeholder,
  textarea::placeholder {
    color: ${({theme:e})=>e.colors.grayscale.light1};
  }

  textarea,
  input[type='text'],
  input[type='number'] {
    padding: ${({theme:e})=>1.5*e.gridUnit}px
      ${({theme:e})=>2*e.gridUnit}px;
    border-style: none;
    border: 1px solid ${({theme:e})=>e.colors.grayscale.light2};
    border-radius: ${({theme:e})=>e.gridUnit}px;

    &[name='name'] {
      flex: 0 1 auto;
      width: 40%;
    }

    &[name='sqlalchemy_uri'] {
      margin-right: ${({theme:e})=>3*e.gridUnit}px;
    }
  }
`,h=({resourceName:e,resourceLabel:t,passwordsNeededMessage:a,confirmOverwriteMessage:r,addDangerToast:o,onModelImport:p,show:h,onHide:y,passwordFields:v=[],setPasswordFields:f=(()=>{})})=>{const[b,w]=(0,s.useState)(!0),[S,x]=(0,s.useState)({}),[Z,C]=(0,s.useState)(!1),[q,L]=(0,s.useState)(!1),[H,k]=(0,s.useState)([]),[D,U]=(0,s.useState)(!1),M=()=>{k([]),f([]),x({}),C(!1),L(!1),U(!1)},{state:{alreadyExists:$,passwordsNeeded:E},importResource:G}=(0,u.PW)(e,t,(e=>{M(),o(e)}));(0,s.useEffect)((()=>{f(E),E.length>0&&U(!1)}),[E,f]),(0,s.useEffect)((()=>{C($.length>0),$.length>0&&U(!1)}),[$,C]);return b&&h&&w(!1),(0,c.tZ)(l.Z,{name:"model",className:"import-model-modal",disablePrimaryButton:0===H.length||Z&&!q||D,onHandledPrimaryAction:()=>{var e;(null==(e=H[0])?void 0:e.originFileObj)instanceof File&&(U(!0),G(H[0].originFileObj,S,q).then((e=>{e&&(M(),p())})))},onHide:()=>{w(!0),y(),M()},primaryButtonName:Z?(0,n.t)("Overwrite"):(0,n.t)("Import"),primaryButtonType:Z?"danger":"primary",width:"750px",show:h,title:(0,c.tZ)("h4",null,(0,n.t)("Import %s",t))},(0,c.tZ)(g,null,(0,c.tZ)(d.gq,{name:"modelFile",id:"modelFile","data-test":"model-file-input",accept:".yaml,.json,.yml,.zip",fileList:H,onChange:e=>{k([{...e.file,status:"done"}])},onRemove:e=>(k(H.filter((t=>t.uid!==e.uid))),!1),customRequest:()=>{}},(0,c.tZ)(i.Z,{loading:D},"Select file"))),0===v.length?null:(0,c.tZ)(s.Fragment,null,(0,c.tZ)("h5",null,"Database passwords"),(0,c.tZ)(m,null,a),v.map((e=>(0,c.tZ)(g,{key:`password-for-${e}`},(0,c.tZ)("div",{className:"control-label"},e,(0,c.tZ)("span",{className:"required"},"*")),(0,c.tZ)("input",{name:`password-${e}`,autoComplete:`password-${e}`,type:"password",value:S[e],onChange:t=>x({...S,[e]:t.target.value})}))))),Z?(0,c.tZ)(s.Fragment,null,(0,c.tZ)(g,null,(0,c.tZ)("div",{className:"confirm-overwrite"},r),(0,c.tZ)("div",{className:"control-label"},(0,n.t)('Type "%s" to confirm',(0,n.t)("OVERWRITE"))),(0,c.tZ)("input",{"data-test":"overwrite-modal-input",id:"overwrite",type:"text",onChange:e=>{var t,a;const r=null!=(t=null==(a=e.currentTarget)?void 0:a.value)?t:"";L(r.toUpperCase()===(0,n.t)("OVERWRITE"))}}))):null)};p(h,"useState{[isHidden, setIsHidden](true)}\nuseState{[passwords, setPasswords]({})}\nuseState{[needsOverwriteConfirm, setNeedsOverwriteConfirm](false)}\nuseState{[confirmedOverwrite, setConfirmedOverwrite](false)}\nuseState{[fileList, setFileList]([])}\nuseState{[importingModel, setImportingModel](false)}\nuseImportResource{{ state: { alreadyExists, passwordsNeeded }, importResource, }}\nuseEffect{}\nuseEffect{}",(()=>[u.PW]));const y=h,v=y;var f,b;(f="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.default:void 0)&&(f.register(m,"HelperMessage","/Users/chenming/superset/superset-frontend/src/components/ImportModal/index.tsx"),f.register(g,"StyledInputContainer","/Users/chenming/superset/superset-frontend/src/components/ImportModal/index.tsx"),f.register(h,"ImportModelsModal","/Users/chenming/superset/superset-frontend/src/components/ImportModal/index.tsx"),f.register(y,"default","/Users/chenming/superset/superset-frontend/src/components/ImportModal/index.tsx")),(b="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.leaveModule:void 0)&&b(e)},129848:(e,t,a)=>{a.d(t,{Z:()=>u}),a(667294);var r,s=a(751995),o=a(358593),n=a(87693),i=a(211965);e=a.hmd(e),(r="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.enterModule:void 0)&&r(e),"undefined"!=typeof reactHotLoaderGlobal&&reactHotLoaderGlobal.default.signature;const l=s.iK.span`
  white-space: nowrap;
  min-width: 100px;
  svg,
  i {
    margin-right: 8px;

    &:hover {
      path {
        fill: ${({theme:e})=>e.colors.primary.base};
      }
    }
  }
`,d=s.iK.span`
  color: ${({theme:e})=>e.colors.grayscale.base};
`;function u({actions:e}){return(0,i.tZ)(l,{className:"actions"},e.map(((e,t)=>{const a=n.Z[e.icon];return e.tooltip?(0,i.tZ)(o.u,{id:`${e.label}-tooltip`,title:e.tooltip,placement:e.placement,key:t},(0,i.tZ)(d,{role:"button",tabIndex:0,className:"action-button","data-test":e.label,onClick:e.onClick},(0,i.tZ)(a,null))):(0,i.tZ)(d,{role:"button",tabIndex:0,className:"action-button",onClick:e.onClick,"data-test":e.label,key:t},(0,i.tZ)(a,null))})))}var c,p;(c="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.default:void 0)&&(c.register(l,"StyledActions","/Users/chenming/superset/superset-frontend/src/components/ListView/ActionsBar.tsx"),c.register(d,"ActionWrapper","/Users/chenming/superset/superset-frontend/src/components/ListView/ActionsBar.tsx"),c.register(u,"ActionsBar","/Users/chenming/superset/superset-frontend/src/components/ListView/ActionsBar.tsx")),(p="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.leaveModule:void 0)&&p(e)},952607:(e,t,a)=>{a.r(t),a.d(t,{default:()=>P});var r,s=a(455867),o=a(751995),n=a(431069),i=a(667294),l=a(115926),d=a.n(l),u=a(730381),c=a.n(u),p=a(440768),m=a(976697),g=a(414114),h=a(34858),y=a(419259),v=a(232228),f=a(620755),b=a(550859),w=a(838703),S=a(217198),x=a(129848),Z=a(358593),C=a(495413),q=a(710222),L=a(591877),H=a(727989),k=a(87693),D=a(684858),U=a(211965);e=a.hmd(e),(r="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.enterModule:void 0)&&r(e);var M="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.default.signature:function(e){return e};const $=(0,s.t)('The passwords for the databases below are needed in order to import them together with the saved queries. Please note that the "Secure Extra" and "Certificate" sections of the database configuration are not present in export files, and should be added manually after the import if they are needed.'),E=(0,s.t)("You are importing one or more saved queries that already exist. Overwriting might cause you to lose some of your work. Are you sure you want to overwrite?"),G=o.iK.div`
  .count {
    margin-left: 5px;
    color: ${({theme:e})=>e.colors.primary.base};
    text-decoration: underline;
    cursor: pointer;
  }
`,Q=o.iK.div`
  color: ${({theme:e})=>e.colors.grayscale.dark2};
`;function T({addDangerToast:e,addSuccessToast:t,user:a}){const{state:{loading:r,resourceCount:o,resourceCollection:l,bulkSelectEnabled:u},hasPerm:g,fetchData:M,toggleBulkSelect:T,refreshData:_}=(0,h.Yi)("saved_query",(0,s.t)("Saved queries"),e),[P,R]=(0,i.useState)(null),[I,N]=(0,i.useState)(null),[O,z]=(0,i.useState)(!1),[A,F]=(0,i.useState)([]),[B,K]=(0,i.useState)(!1),V=g("can_write"),W=g("can_write"),j=g("can_write"),Y=g("can_export")&&(0,L.cr)(L.TT.VERSIONED_EXPORT),X=(0,i.useCallback)((t=>{n.Z.get({endpoint:`/api/v1/saved_query/${t}`}).then((({json:e={}})=>{N({...e.result})}),(0,p.v$)((t=>e((0,s.t)("There was an issue previewing the selected query %s",t)))))}),[e]),J={activeChild:"Saved queries",...C.Y},ee=[];j&&ee.push({name:(0,s.t)("Bulk select"),onClick:T,buttonStyle:"secondary"}),ee.push({name:(0,U.tZ)(i.Fragment,null,(0,U.tZ)("i",{className:"fa fa-plus"})," ",(0,s.t)("Query")),onClick:()=>{window.open(`${window.location.origin}/superset/sqllab?new=true`)},buttonStyle:"primary"}),V&&(0,L.cr)(L.TT.VERSIONED_EXPORT)&&ee.push({name:(0,U.tZ)(Z.u,{id:"import-tooltip",title:(0,s.t)("Import queries"),placement:"bottomRight","data-test":"import-tooltip-test"},(0,U.tZ)(k.Z.Import,{"data-test":"import-icon"})),buttonStyle:"link",onClick:()=>{z(!0)},"data-test":"import-button"}),J.buttons=ee;const te=e=>{window.open(`${window.location.origin}/superset/sqllab?savedQueryId=${e}`)},ae=(0,i.useCallback)((a=>{(0,q.Z)(`${window.location.origin}/superset/sqllab?savedQueryId=${a}`).then((()=>{t((0,s.t)("Link Copied!"))})).catch((()=>{e((0,s.t)("Sorry, your browser does not support copying."))}))}),[e,t]),re=e=>{const t=e.map((({id:e})=>e));(0,v.Z)("saved_query",t,(()=>{K(!1)})),K(!0)},se=[{id:"changed_on_delta_humanized",desc:!0}],oe=(0,i.useMemo)((()=>[{accessor:"label",Header:(0,s.t)("Name")},{accessor:"database.database_name",Header:(0,s.t)("Database"),size:"xl"},{accessor:"database",hidden:!0,disableSortBy:!0},{accessor:"schema",Header:(0,s.t)("Schema"),size:"xl"},{Cell:({row:{original:{sql_tables:e=[]}}})=>{const t=e.map((e=>e.table)),a=(null==t?void 0:t.shift())||"";return t.length?(0,U.tZ)(G,null,(0,U.tZ)("span",null,a),(0,U.tZ)(m.Z,{placement:"right",title:(0,s.t)("TABLES"),trigger:"click",content:(0,U.tZ)(i.Fragment,null,t.map((e=>(0,U.tZ)(Q,{key:e},e))))},(0,U.tZ)("span",{className:"count"},"(+",t.length,")"))):a},accessor:"sql_tables",Header:(0,s.t)("Tables"),size:"xl",disableSortBy:!0},{Cell:({row:{original:{created_on:e}}})=>{const t=new Date(e),a=new Date(Date.UTC(t.getFullYear(),t.getMonth(),t.getDate(),t.getHours(),t.getMinutes(),t.getSeconds(),t.getMilliseconds()));return c()(a).fromNow()},Header:(0,s.t)("Created on"),accessor:"created_on",size:"xl"},{Cell:({row:{original:{changed_on_delta_humanized:e}}})=>e,Header:(0,s.t)("Modified"),accessor:"changed_on_delta_humanized",size:"xl"},{Cell:({row:{original:e}})=>{const t=[{label:"preview-action",tooltip:(0,s.t)("Query preview"),placement:"bottom",icon:"Binoculars",onClick:()=>{X(e.id)}},W&&{label:"edit-action",tooltip:(0,s.t)("Edit query"),placement:"bottom",icon:"Edit",onClick:()=>te(e.id)},{label:"copy-action",tooltip:(0,s.t)("Copy query URL"),placement:"bottom",icon:"Copy",onClick:()=>ae(e.id)},Y&&{label:"export-action",tooltip:(0,s.t)("Export query"),placement:"bottom",icon:"Share",onClick:()=>re([e])},j&&{label:"delete-action",tooltip:(0,s.t)("Delete query"),placement:"bottom",icon:"Trash",onClick:()=>R(e)}].filter((e=>!!e));return(0,U.tZ)(x.Z,{actions:t})},Header:(0,s.t)("Actions"),id:"actions",disableSortBy:!0}]),[j,W,Y,ae,X]),ne=(0,i.useMemo)((()=>[{Header:(0,s.t)("Database"),id:"database",input:"select",operator:b.p.relationOneMany,unfilteredLabel:"All",fetchSelects:(0,p.tm)("saved_query","database",(0,p.v$)((t=>e((0,s.t)("An error occurred while fetching dataset datasource values: %s",t))))),paginate:!0},{Header:(0,s.t)("Schema"),id:"schema",input:"select",operator:b.p.equals,unfilteredLabel:"All",fetchSelects:(0,p.wk)("saved_query","schema",(0,p.v$)((t=>e((0,s.t)("An error occurred while fetching schema values: %s",t))))),paginate:!0},{Header:(0,s.t)("Search"),id:"label",input:"search",operator:b.p.allText}]),[e]);return(0,U.tZ)(i.Fragment,null,(0,U.tZ)(f.Z,J),P&&(0,U.tZ)(S.Z,{description:(0,s.t)("This action will permanently delete the saved query."),onConfirm:()=>{P&&(({id:a,label:r})=>{n.Z.delete({endpoint:`/api/v1/saved_query/${a}`}).then((()=>{_(),R(null),t((0,s.t)("Deleted: %s",r))}),(0,p.v$)((t=>e((0,s.t)("There was an issue deleting %s: %s",r,t)))))})(P)},onHide:()=>R(null),open:!0,title:(0,s.t)("Delete Query?")}),I&&(0,U.tZ)(D.Z,{fetchData:X,onHide:()=>N(null),savedQuery:I,queries:l,openInSqlLab:te,show:!0}),(0,U.tZ)(y.Z,{title:(0,s.t)("Please confirm"),description:(0,s.t)("Are you sure you want to delete the selected queries?"),onConfirm:a=>{n.Z.delete({endpoint:`/api/v1/saved_query/?q=${d().encode(a.map((({id:e})=>e)))}`}).then((({json:e={}})=>{_(),t(e.message)}),(0,p.v$)((t=>e((0,s.t)("There was an issue deleting the selected queries: %s",t)))))}},(e=>{const t=[];return j&&t.push({key:"delete",name:(0,s.t)("Delete"),onSelect:e,type:"danger"}),Y&&t.push({key:"export",name:(0,s.t)("Export"),type:"primary",onSelect:re}),(0,U.tZ)(b.Z,{className:"saved_query-list-view",columns:oe,count:o,data:l,fetchData:M,filters:ne,initialSort:se,loading:r,pageSize:25,bulkActions:t,bulkSelectEnabled:u,disableBulkSelect:T,highlightRowId:null==I?void 0:I.id})})),(0,U.tZ)(H.Z,{resourceName:"saved_query",resourceLabel:(0,s.t)("queries"),passwordsNeededMessage:$,confirmOverwriteMessage:E,addDangerToast:e,addSuccessToast:t,onModelImport:()=>{z(!1),_(),t((0,s.t)("Query imported"))},show:O,onHide:()=>{z(!1)},passwordFields:A,setPasswordFields:F}),B&&(0,U.tZ)(w.Z,null))}M(T,"useListViewResource{{ state: { loading, resourceCount: queryCount, resourceCollection: queries, bulkSelectEnabled, }, hasPerm, fetchData, toggleBulkSelect, refreshData, }}\nuseState{[queryCurrentlyDeleting, setQueryCurrentlyDeleting](null)}\nuseState{[savedQueryCurrentlyPreviewing, setSavedQueryCurrentlyPreviewing](null)}\nuseState{[importingSavedQuery, showImportModal](false)}\nuseState{[passwordFields, setPasswordFields]([])}\nuseState{[preparingExport, setPreparingExport](false)}\nuseCallback{handleSavedQueryPreview}\nuseCallback{copyQueryLink}\nuseMemo{columns}\nuseMemo{filters}",(()=>[h.Yi]));const _=(0,g.Z)(T),P=_;var R,I;(R="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.default:void 0)&&(R.register(25,"PAGE_SIZE","/Users/chenming/superset/superset-frontend/src/views/CRUD/data/savedquery/SavedQueryList.tsx"),R.register($,"PASSWORDS_NEEDED_MESSAGE","/Users/chenming/superset/superset-frontend/src/views/CRUD/data/savedquery/SavedQueryList.tsx"),R.register(E,"CONFIRM_OVERWRITE_MESSAGE","/Users/chenming/superset/superset-frontend/src/views/CRUD/data/savedquery/SavedQueryList.tsx"),R.register(G,"StyledTableLabel","/Users/chenming/superset/superset-frontend/src/views/CRUD/data/savedquery/SavedQueryList.tsx"),R.register(Q,"StyledPopoverItem","/Users/chenming/superset/superset-frontend/src/views/CRUD/data/savedquery/SavedQueryList.tsx"),R.register(T,"SavedQueryList","/Users/chenming/superset/superset-frontend/src/views/CRUD/data/savedquery/SavedQueryList.tsx"),R.register(_,"default","/Users/chenming/superset/superset-frontend/src/views/CRUD/data/savedquery/SavedQueryList.tsx")),(I="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.leaveModule:void 0)&&I(e)},684858:(e,t,a)=>{a.d(t,{Z:()=>f}),a(667294);var r,s=a(751995),o=a(455867),n=a(574520),i=a(835932),l=a(331673),d=a(414114),u=a(14025),c=a(211965);e=a.hmd(e),(r="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.enterModule:void 0)&&r(e);var p="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.default.signature:function(e){return e};const m=s.iK.div`
  color: ${({theme:e})=>e.colors.secondary.light2};
  font-size: ${({theme:e})=>e.typography.sizes.s-1}px;
  margin-bottom: 0;
  text-transform: uppercase;
`,g=s.iK.div`
  color: ${({theme:e})=>e.colors.grayscale.dark2};
  font-size: ${({theme:e})=>e.typography.sizes.m-1}px;
  padding: 4px 0 16px 0;
`,h=(0,s.iK)(n.Z)`
  .ant-modal-content {
  }

  .ant-modal-body {
    padding: 24px;
  }

  pre {
    font-size: ${({theme:e})=>e.typography.sizes.xs}px;
    font-weight: ${({theme:e})=>e.typography.weights.normal};
    line-height: ${({theme:e})=>e.typography.sizes.l}px;
    height: 375px;
    border: none;
  }
`,y=({fetchData:e,onHide:t,openInSqlLab:a,queries:r,savedQuery:s,show:n,addDangerToast:d,addSuccessToast:p})=>{const{handleKeyPress:y,handleDataChange:v,disablePrevious:f,disableNext:b}=(0,u.C)({queries:r,currentQueryId:s.id,fetchData:e});return(0,c.tZ)("div",{role:"none",onKeyUp:y},(0,c.tZ)(h,{onHide:t,show:n,title:(0,o.t)("Query preview"),footer:[(0,c.tZ)(i.Z,{"data-test":"previous-saved-query",key:"previous-saved-query",disabled:f,onClick:()=>v(!0)},(0,o.t)("Previous")),(0,c.tZ)(i.Z,{"data-test":"next-saved-query",key:"next-saved-query",disabled:b,onClick:()=>v(!1)},(0,o.t)("Next")),(0,c.tZ)(i.Z,{"data-test":"open-in-sql-lab",key:"open-in-sql-lab",buttonStyle:"primary",onClick:()=>a(s.id)},(0,o.t)("Open in SQL Lab"))]},(0,c.tZ)(m,null,(0,o.t)("Query name")),(0,c.tZ)(g,null,s.label),(0,c.tZ)(l.Z,{language:"sql",addDangerToast:d,addSuccessToast:p},s.sql||"")))};p(y,"useQueryPreviewState{{ handleKeyPress, handleDataChange, disablePrevious, disableNext }}",(()=>[u.C]));const v=(0,d.Z)(y),f=v;var b,w;(b="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.default:void 0)&&(b.register(m,"QueryTitle","/Users/chenming/superset/superset-frontend/src/views/CRUD/data/savedquery/SavedQueryPreviewModal.tsx"),b.register(g,"QueryLabel","/Users/chenming/superset/superset-frontend/src/views/CRUD/data/savedquery/SavedQueryPreviewModal.tsx"),b.register(h,"StyledModal","/Users/chenming/superset/superset-frontend/src/views/CRUD/data/savedquery/SavedQueryPreviewModal.tsx"),b.register(y,"SavedQueryPreviewModal","/Users/chenming/superset/superset-frontend/src/views/CRUD/data/savedquery/SavedQueryPreviewModal.tsx"),b.register(v,"default","/Users/chenming/superset/superset-frontend/src/views/CRUD/data/savedquery/SavedQueryPreviewModal.tsx")),(w="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.leaveModule:void 0)&&w(e)}}]);
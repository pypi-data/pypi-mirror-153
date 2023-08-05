"use strict";(globalThis.webpackChunksuperset=globalThis.webpackChunksuperset||[]).push([[4502],{727989:(e,t,a)=>{a.d(t,{Z:()=>f});var s,o=a(667294),r=a(751995),n=a(455867),l=a(835932),i=a(574520),d=a(104715),u=a(34858),c=a(211965);e=a.hmd(e),(s="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.enterModule:void 0)&&s(e);var p="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.default.signature:function(e){return e};const m=r.iK.div`
  display: block;
  color: ${({theme:e})=>e.colors.grayscale.base};
  font-size: ${({theme:e})=>e.typography.sizes.s-1}px;
`,b=r.iK.div`
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
`,h=({resourceName:e,resourceLabel:t,passwordsNeededMessage:a,confirmOverwriteMessage:s,addDangerToast:r,onModelImport:p,show:h,onHide:g,passwordFields:f=[],setPasswordFields:v=(()=>{})})=>{const[w,y]=(0,o.useState)(!0),[Z,x]=(0,o.useState)({}),[D,_]=(0,o.useState)(!1),[S,C]=(0,o.useState)(!1),[L,H]=(0,o.useState)([]),[E,U]=(0,o.useState)(!1),M=()=>{H([]),v([]),x({}),_(!1),C(!1),U(!1)},{state:{alreadyExists:R,passwordsNeeded:I},importResource:G}=(0,u.PW)(e,t,(e=>{M(),r(e)}));(0,o.useEffect)((()=>{v(I),I.length>0&&U(!1)}),[I,v]),(0,o.useEffect)((()=>{_(R.length>0),R.length>0&&U(!1)}),[R,_]);return w&&h&&y(!1),(0,c.tZ)(i.Z,{name:"model",className:"import-model-modal",disablePrimaryButton:0===L.length||D&&!S||E,onHandledPrimaryAction:()=>{var e;(null==(e=L[0])?void 0:e.originFileObj)instanceof File&&(U(!0),G(L[0].originFileObj,Z,S).then((e=>{e&&(M(),p())})))},onHide:()=>{y(!0),g(),M()},primaryButtonName:D?(0,n.t)("Overwrite"):(0,n.t)("Import"),primaryButtonType:D?"danger":"primary",width:"750px",show:h,title:(0,c.tZ)("h4",null,(0,n.t)("Import %s",t))},(0,c.tZ)(b,null,(0,c.tZ)(d.gq,{name:"modelFile",id:"modelFile","data-test":"model-file-input",accept:".yaml,.json,.yml,.zip",fileList:L,onChange:e=>{H([{...e.file,status:"done"}])},onRemove:e=>(H(L.filter((t=>t.uid!==e.uid))),!1),customRequest:()=>{}},(0,c.tZ)(l.Z,{loading:E},"Select file"))),0===f.length?null:(0,c.tZ)(o.Fragment,null,(0,c.tZ)("h5",null,"Database passwords"),(0,c.tZ)(m,null,a),f.map((e=>(0,c.tZ)(b,{key:`password-for-${e}`},(0,c.tZ)("div",{className:"control-label"},e,(0,c.tZ)("span",{className:"required"},"*")),(0,c.tZ)("input",{name:`password-${e}`,autoComplete:`password-${e}`,type:"password",value:Z[e],onChange:t=>x({...Z,[e]:t.target.value})}))))),D?(0,c.tZ)(o.Fragment,null,(0,c.tZ)(b,null,(0,c.tZ)("div",{className:"confirm-overwrite"},s),(0,c.tZ)("div",{className:"control-label"},(0,n.t)('Type "%s" to confirm',(0,n.t)("OVERWRITE"))),(0,c.tZ)("input",{"data-test":"overwrite-modal-input",id:"overwrite",type:"text",onChange:e=>{var t,a;const s=null!=(t=null==(a=e.currentTarget)?void 0:a.value)?t:"";C(s.toUpperCase()===(0,n.t)("OVERWRITE"))}}))):null)};p(h,"useState{[isHidden, setIsHidden](true)}\nuseState{[passwords, setPasswords]({})}\nuseState{[needsOverwriteConfirm, setNeedsOverwriteConfirm](false)}\nuseState{[confirmedOverwrite, setConfirmedOverwrite](false)}\nuseState{[fileList, setFileList]([])}\nuseState{[importingModel, setImportingModel](false)}\nuseImportResource{{ state: { alreadyExists, passwordsNeeded }, importResource, }}\nuseEffect{}\nuseEffect{}",(()=>[u.PW]));const g=h,f=g;var v,w;(v="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.default:void 0)&&(v.register(m,"HelperMessage","/Users/chenming/superset/superset-frontend/src/components/ImportModal/index.tsx"),v.register(b,"StyledInputContainer","/Users/chenming/superset/superset-frontend/src/components/ImportModal/index.tsx"),v.register(h,"ImportModelsModal","/Users/chenming/superset/superset-frontend/src/components/ImportModal/index.tsx"),v.register(g,"default","/Users/chenming/superset/superset-frontend/src/components/ImportModal/index.tsx")),(w="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.leaveModule:void 0)&&w(e)},495413:(e,t,a)=>{a.d(t,{Y:()=>r});var s,o=a(455867);e=a.hmd(e),(s="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.enterModule:void 0)&&s(e),"undefined"!=typeof reactHotLoaderGlobal&&reactHotLoaderGlobal.default.signature;const r={name:(0,o.t)("Data"),tabs:[{name:"Databases",label:(0,o.t)("Databases"),url:"/databaseview/list/",usesRouter:!0},{name:"Datasets",label:(0,o.t)("Datasets"),url:"/tablemodelview/list/",usesRouter:!0},{name:"Saved queries",label:(0,o.t)("Saved queries"),url:"/savedqueryview/list/",usesRouter:!0},{name:"Query history",label:(0,o.t)("Query history"),url:"/superset/sqllab/history/",usesRouter:!0}]};var n,l;(n="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.default:void 0)&&n.register(r,"commonMenuData","/Users/chenming/superset/superset-frontend/src/views/CRUD/data/common.ts"),(l="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.leaveModule:void 0)&&l(e)},430075:(e,t,a)=>{a.r(t),a.d(t,{default:()=>R});var s,o=a(455867),r=a(751995),n=a(431069),l=a(667294),i=a(838703),d=a(591877),u=a(34858),c=a(440768),p=a(414114),m=a(620755),b=a(217198),h=a(358593),g=a(87693),f=a(550859),v=a(495413),w=a(727989),y=a(232228),Z=a(603506),x=a(211965);e=a.hmd(e),(s="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.enterModule:void 0)&&s(e);var D="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.default.signature:function(e){return e};const _=(0,o.t)('The passwords for the databases below are needed in order to import them. Please note that the "Secure Extra" and "Certificate" sections of the database configuration are not present in export files, and should be added manually after the import if they are needed.'),S=(0,o.t)("You are importing one or more databases that already exist. Overwriting might cause you to lose some of your work. Are you sure you want to overwrite?"),C=(0,r.iK)(g.Z.Check)`
  color: ${({theme:e})=>e.colors.grayscale.dark1};
`,L=(0,r.iK)(g.Z.CancelX)`
  color: ${({theme:e})=>e.colors.grayscale.dark1};
`,H=r.iK.div`
  color: ${({theme:e})=>e.colors.grayscale.base};

  .action-button {
    display: inline-block;
    height: 100%;
  }
`;function E({value:e}){return e?(0,x.tZ)(C,null):(0,x.tZ)(L,null)}function U({addDangerToast:e,addSuccessToast:t}){const{state:{loading:a,resourceCount:s,resourceCollection:r},hasPerm:p,fetchData:D,refreshData:C}=(0,u.Yi)("database",(0,o.t)("database"),e),[L,U]=(0,l.useState)(!1),[M,R]=(0,l.useState)(null),[I,G]=(0,l.useState)(null),[$,N]=(0,l.useState)(!1),[O,T]=(0,l.useState)([]),[k,A]=(0,l.useState)(!1);function q({database:e=null,modalOpen:t=!1}={}){G(e),U(t)}const F=p("can_write"),P=p("can_write"),z=p("can_write"),B=p("can_export")&&(0,d.cr)(d.TT.VERSIONED_EXPORT),Q={activeChild:"Databases",...v.Y};F&&(Q.buttons=[{"data-test":"btn-create-database",name:(0,x.tZ)(l.Fragment,null,(0,x.tZ)("i",{className:"fa fa-plus"})," ",(0,o.t)("Database")," "),buttonStyle:"primary",onClick:()=>{q({modalOpen:!0})}}],(0,d.cr)(d.TT.VERSIONED_EXPORT)&&Q.buttons.push({name:(0,x.tZ)(h.u,{id:"import-tooltip",title:(0,o.t)("Import databases"),placement:"bottomRight"},(0,x.tZ)(g.Z.Import,{"data-test":"import-button"})),buttonStyle:"link",onClick:()=>{N(!0)}}));const V=(0,l.useMemo)((()=>[{accessor:"database_name",Header:(0,o.t)("Database")},{accessor:"backend",Header:(0,o.t)("Backend"),size:"lg",disableSortBy:!0},{accessor:"allow_run_async",Header:(0,x.tZ)(h.u,{id:"allow-run-async-header-tooltip",title:(0,o.t)("Asynchronous query execution"),placement:"top"},(0,x.tZ)("span",null,(0,o.t)("AQE"))),Cell:({row:{original:{allow_run_async:e}}})=>(0,x.tZ)(E,{value:e}),size:"sm"},{accessor:"allow_dml",Header:(0,x.tZ)(h.u,{id:"allow-dml-header-tooltip",title:(0,o.t)("Allow data manipulation language"),placement:"top"},(0,x.tZ)("span",null,(0,o.t)("DML"))),Cell:({row:{original:{allow_dml:e}}})=>(0,x.tZ)(E,{value:e}),size:"sm"},{accessor:"allow_file_upload",Header:(0,o.t)("CSV upload"),Cell:({row:{original:{allow_file_upload:e}}})=>(0,x.tZ)(E,{value:e}),size:"md"},{accessor:"expose_in_sqllab",Header:(0,o.t)("Expose in SQL Lab"),Cell:({row:{original:{expose_in_sqllab:e}}})=>(0,x.tZ)(E,{value:e}),size:"md"},{accessor:"created_by",disableSortBy:!0,Header:(0,o.t)("Created by"),Cell:({row:{original:{created_by:e}}})=>e?`${e.first_name} ${e.last_name}`:"",size:"xl"},{Cell:({row:{original:{changed_on_delta_humanized:e}}})=>e,Header:(0,o.t)("Last modified"),accessor:"changed_on_delta_humanized",size:"xl"},{Cell:({row:{original:e}})=>P||z||B?(0,x.tZ)(H,{className:"actions"},z&&(0,x.tZ)("span",{role:"button",tabIndex:0,className:"action-button","data-test":"database-delete",onClick:()=>{return t=e,n.Z.get({endpoint:`/api/v1/database/${t.id}/related_objects/`}).then((({json:e={}})=>{R({...t,chart_count:e.charts.count,dashboard_count:e.dashboards.count,sqllab_tab_count:e.sqllab_tab_states.count})})).catch((0,c.v$)((e=>(0,o.t)("An error occurred while fetching database related data: %s",e))));var t}},(0,x.tZ)(h.u,{id:"delete-action-tooltip",title:(0,o.t)("Delete database"),placement:"bottom"},(0,x.tZ)(g.Z.Trash,null))),B&&(0,x.tZ)(h.u,{id:"export-action-tooltip",title:(0,o.t)("Export"),placement:"bottom"},(0,x.tZ)("span",{role:"button",tabIndex:0,className:"action-button",onClick:()=>{var t;void 0!==(t=e).id&&((0,y.Z)("database",[t.id],(()=>{A(!1)})),A(!0))}},(0,x.tZ)(g.Z.Share,null))),P&&(0,x.tZ)(h.u,{id:"edit-action-tooltip",title:(0,o.t)("Edit"),placement:"bottom"},(0,x.tZ)("span",{role:"button","data-test":"database-edit",tabIndex:0,className:"action-button",onClick:()=>q({database:e,modalOpen:!0})},(0,x.tZ)(g.Z.EditAlt,{"data-test":"edit-alt"})))):null,Header:(0,o.t)("Actions"),id:"actions",hidden:!P&&!z,disableSortBy:!0}]),[z,P,B]),Y=(0,l.useMemo)((()=>[{Header:(0,o.t)("Expose in SQL Lab"),id:"expose_in_sqllab",input:"select",operator:f.p.equals,unfilteredLabel:"All",selects:[{label:"Yes",value:!0},{label:"No",value:!1}]},{Header:(0,x.tZ)(h.u,{id:"allow-run-async-filter-header-tooltip",title:(0,o.t)("Asynchronous query execution"),placement:"top"},(0,x.tZ)("span",null,(0,o.t)("AQE"))),id:"allow_run_async",input:"select",operator:f.p.equals,unfilteredLabel:"All",selects:[{label:"Yes",value:!0},{label:"No",value:!1}]},{Header:(0,o.t)("Search"),id:"database_name",input:"search",operator:f.p.contains}]),[]);return(0,x.tZ)(l.Fragment,null,(0,x.tZ)(m.Z,Q),(0,x.tZ)(Z.Z,{databaseId:null==I?void 0:I.id,show:L,onHide:q,onDatabaseAdd:()=>{C()}}),M&&(0,x.tZ)(b.Z,{description:(0,o.t)("The database %s is linked to %s charts that appear on %s dashboards and users have %s SQL Lab tabs using this database open. Are you sure you want to continue? Deleting the database will break those objects.",M.database_name,M.chart_count,M.dashboard_count,M.sqllab_tab_count),onConfirm:()=>{M&&function({id:a,database_name:s}){n.Z.delete({endpoint:`/api/v1/database/${a}`}).then((()=>{C(),t((0,o.t)("Deleted: %s",s)),R(null)}),(0,c.v$)((t=>e((0,o.t)("There was an issue deleting %s: %s",s,t)))))}(M)},onHide:()=>R(null),open:!0,title:(0,o.t)("Delete Database?")}),(0,x.tZ)(f.Z,{className:"database-list-view",columns:V,count:s,data:r,fetchData:D,filters:Y,initialSort:[{id:"changed_on_delta_humanized",desc:!0}],loading:a,pageSize:25}),(0,x.tZ)(w.Z,{resourceName:"database",resourceLabel:(0,o.t)("database"),passwordsNeededMessage:_,confirmOverwriteMessage:S,addDangerToast:e,addSuccessToast:t,onModelImport:()=>{N(!1),C(),t((0,o.t)("Database imported"))},show:$,onHide:()=>{N(!1)},passwordFields:O,setPasswordFields:T}),k&&(0,x.tZ)(i.Z,null))}D(U,"useListViewResource{{ state: { loading, resourceCount: databaseCount, resourceCollection: databases, }, hasPerm, fetchData, refreshData, }}\nuseState{[databaseModalOpen, setDatabaseModalOpen](false)}\nuseState{[databaseCurrentlyDeleting, setDatabaseCurrentlyDeleting](null)}\nuseState{[currentDatabase, setCurrentDatabase](null)}\nuseState{[importingDatabase, showImportModal](false)}\nuseState{[passwordFields, setPasswordFields]([])}\nuseState{[preparingExport, setPreparingExport](false)}\nuseMemo{columns}\nuseMemo{filters}",(()=>[u.Yi]));const M=(0,p.Z)(U),R=M;var I,G;(I="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.default:void 0)&&(I.register(25,"PAGE_SIZE","/Users/chenming/superset/superset-frontend/src/views/CRUD/data/database/DatabaseList.tsx"),I.register(_,"PASSWORDS_NEEDED_MESSAGE","/Users/chenming/superset/superset-frontend/src/views/CRUD/data/database/DatabaseList.tsx"),I.register(S,"CONFIRM_OVERWRITE_MESSAGE","/Users/chenming/superset/superset-frontend/src/views/CRUD/data/database/DatabaseList.tsx"),I.register(C,"IconCheck","/Users/chenming/superset/superset-frontend/src/views/CRUD/data/database/DatabaseList.tsx"),I.register(L,"IconCancelX","/Users/chenming/superset/superset-frontend/src/views/CRUD/data/database/DatabaseList.tsx"),I.register(H,"Actions","/Users/chenming/superset/superset-frontend/src/views/CRUD/data/database/DatabaseList.tsx"),I.register(E,"BooleanDisplay","/Users/chenming/superset/superset-frontend/src/views/CRUD/data/database/DatabaseList.tsx"),I.register(U,"DatabaseList","/Users/chenming/superset/superset-frontend/src/views/CRUD/data/database/DatabaseList.tsx"),I.register(M,"default","/Users/chenming/superset/superset-frontend/src/views/CRUD/data/database/DatabaseList.tsx")),(G="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.leaveModule:void 0)&&G(e)}}]);
"use strict";(globalThis.webpackChunksuperset=globalThis.webpackChunksuperset||[]).push([[1611],{129848:(t,e,n)=>{n.d(e,{Z:()=>c}),n(667294);var a,o=n(751995),s=n(358593),r=n(87693),l=n(211965);t=n.hmd(t),(a="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.enterModule:void 0)&&a(t),"undefined"!=typeof reactHotLoaderGlobal&&reactHotLoaderGlobal.default.signature;const i=o.iK.span`
  white-space: nowrap;
  min-width: 100px;
  svg,
  i {
    margin-right: 8px;

    &:hover {
      path {
        fill: ${({theme:t})=>t.colors.primary.base};
      }
    }
  }
`,d=o.iK.span`
  color: ${({theme:t})=>t.colors.grayscale.base};
`;function c({actions:t}){return(0,l.tZ)(i,{className:"actions"},t.map(((t,e)=>{const n=r.Z[t.icon];return t.tooltip?(0,l.tZ)(s.u,{id:`${t.label}-tooltip`,title:t.tooltip,placement:t.placement,key:e},(0,l.tZ)(d,{role:"button",tabIndex:0,className:"action-button","data-test":t.label,onClick:t.onClick},(0,l.tZ)(n,null))):(0,l.tZ)(d,{role:"button",tabIndex:0,className:"action-button",onClick:t.onClick,"data-test":t.label,key:e},(0,l.tZ)(n,null))})))}var u,m;(u="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.default:void 0)&&(u.register(i,"StyledActions","/Users/chenming/superset/superset-frontend/src/components/ListView/ActionsBar.tsx"),u.register(d,"ActionWrapper","/Users/chenming/superset/superset-frontend/src/components/ListView/ActionsBar.tsx"),u.register(c,"ActionsBar","/Users/chenming/superset/superset-frontend/src/components/ListView/ActionsBar.tsx")),(m="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.leaveModule:void 0)&&m(t)},92659:(t,e,n)=>{n.r(e),n.d(e,{default:()=>S});var a,o=n(667294),s=n(505977),r=n(473727),l=n(455867),i=n(431069),d=n(751995),c=n(730381),u=n.n(c),m=n(115926),h=n.n(m),p=n(129848),f=n(835932),g=n(419259),b=n(217198),y=n(550859),Z=n(620755),_=n(998286),v=n(414114),L=n(34858),A=n(440768),x=n(536120),w=n(211965);function H({addDangerToast:t,addSuccessToast:e}){const{annotationLayerId:n}=(0,s.UO)(),{state:{loading:a,resourceCount:c,resourceCollection:m,bulkSelectEnabled:v},fetchData:H,refreshData:C,toggleBulkSelect:S}=(0,L.Yi)(`annotation_layer/${n}/annotation`,(0,l.t)("annotation"),t,!1),[D,k]=(0,o.useState)(!1),[U,$]=(0,o.useState)(""),[G,M]=(0,o.useState)(null),[E,N]=(0,o.useState)(null),R=t=>{M(t),k(!0)},T=(0,o.useCallback)((async function(){try{const t=await i.Z.get({endpoint:`/api/v1/annotation_layer/${n}`});$(t.json.result.name)}catch(e){await(0,_.O)(e).then((({error:e})=>{t(e.error||e.statusText||e)}))}}),[n]);(0,o.useEffect)((()=>{T()}),[T]);const B=[{id:"short_descr",desc:!0}],Y=(0,o.useMemo)((()=>[{accessor:"short_descr",Header:(0,l.t)("Label")},{accessor:"long_descr",Header:(0,l.t)("Description")},{Cell:({row:{original:{start_dttm:t}}})=>u()(new Date(t)).format("ll"),Header:(0,l.t)("Start"),accessor:"start_dttm"},{Cell:({row:{original:{end_dttm:t}}})=>u()(new Date(t)).format("ll"),Header:(0,l.t)("End"),accessor:"end_dttm"},{Cell:({row:{original:t}})=>{const e=[{label:"edit-action",tooltip:(0,l.t)("Edit annotation"),placement:"bottom",icon:"Edit",onClick:()=>R(t)},{label:"delete-action",tooltip:(0,l.t)("Delete annotation"),placement:"bottom",icon:"Trash",onClick:()=>N(t)}];return(0,w.tZ)(p.Z,{actions:e})},Header:(0,l.t)("Actions"),id:"actions",disableSortBy:!0}]),[!0,!0]),I=[];I.push({name:(0,w.tZ)(o.Fragment,null,(0,w.tZ)("i",{className:"fa fa-plus"})," ",(0,l.t)("Annotation")),buttonStyle:"primary",onClick:()=>{R(null)}}),I.push({name:(0,l.t)("Bulk select"),onClick:S,buttonStyle:"secondary","data-test":"annotation-bulk-select"});const j=d.iK.div`
    display: flex;
    flex-direction: row;

    a,
    Link {
      margin-left: 16px;
      font-size: 12px;
      font-weight: normal;
      text-decoration: underline;
    }
  `;let K=!0;try{(0,s.k6)()}catch(t){K=!1}const O=(0,w.tZ)(f.Z,{buttonStyle:"primary",onClick:()=>{R(null)}},(0,w.tZ)(o.Fragment,null,(0,w.tZ)("i",{className:"fa fa-plus"})," ",(0,l.t)("Annotation"))),P={message:(0,l.t)("No annotation yet"),slot:O};return(0,w.tZ)(o.Fragment,null,(0,w.tZ)(Z.Z,{name:(0,w.tZ)(j,null,(0,w.tZ)("span",null,(0,l.t)(`Annotation Layer ${U}`)),(0,w.tZ)("span",null,K?(0,w.tZ)(r.rU,{to:"/annotationlayermodelview/list/"},"Back to all"):(0,w.tZ)("a",{href:"/annotationlayermodelview/list/"},"Back to all"))),buttons:I}),(0,w.tZ)(x.Z,{addDangerToast:t,addSuccessToast:e,annotation:G,show:D,onAnnotationAdd:()=>C(),annnotationLayerId:n,onHide:()=>k(!1)}),E&&(0,w.tZ)(b.Z,{description:(0,l.t)(`Are you sure you want to delete ${null==E?void 0:E.short_descr}?`),onConfirm:()=>{E&&(({id:a,short_descr:o})=>{i.Z.delete({endpoint:`/api/v1/annotation_layer/${n}/annotation/${a}`}).then((()=>{C(),N(null),e((0,l.t)("Deleted: %s",o))}),(0,A.v$)((e=>t((0,l.t)("There was an issue deleting %s: %s",o,e)))))})(E)},onHide:()=>N(null),open:!0,title:(0,l.t)("Delete Annotation?")}),(0,w.tZ)(g.Z,{title:(0,l.t)("Please confirm"),description:(0,l.t)("Are you sure you want to delete the selected annotations?"),onConfirm:a=>{i.Z.delete({endpoint:`/api/v1/annotation_layer/${n}/annotation/?q=${h().encode(a.map((({id:t})=>t)))}`}).then((({json:t={}})=>{C(),e(t.message)}),(0,A.v$)((e=>t((0,l.t)("There was an issue deleting the selected annotations: %s",e)))))}},(t=>{const e=[{key:"delete",name:(0,l.t)("Delete"),onSelect:t,type:"danger"}];return(0,w.tZ)(y.Z,{className:"annotations-list-view",bulkActions:e,bulkSelectEnabled:v,columns:Y,count:c,data:m,disableBulkSelect:S,emptyState:P,fetchData:H,initialSort:B,loading:a,pageSize:25})})))}t=n.hmd(t),(a="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.enterModule:void 0)&&a(t),("undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.default.signature:function(t){return t})(H,"useParams{{ annotationLayerId }}\nuseListViewResource{{ state: { loading, resourceCount: annotationsCount, resourceCollection: annotations, bulkSelectEnabled, }, fetchData, refreshData, toggleBulkSelect, }}\nuseState{[annotationModalOpen, setAnnotationModalOpen](false)}\nuseState{[annotationLayerName, setAnnotationLayerName]('')}\nuseState{[currentAnnotation, setCurrentAnnotation](null)}\nuseState{[annotationCurrentlyDeleting, setAnnotationCurrentlyDeleting](null)}\nuseCallback{fetchAnnotationLayer}\nuseEffect{}\nuseMemo{columns}\nuseHistory{}",(()=>[s.UO,L.Yi,s.k6]));const C=(0,v.Z)(H),S=C;var D,k;(D="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.default:void 0)&&(D.register(25,"PAGE_SIZE","/Users/chenming/superset/superset-frontend/src/views/CRUD/annotation/AnnotationList.tsx"),D.register(H,"AnnotationList","/Users/chenming/superset/superset-frontend/src/views/CRUD/annotation/AnnotationList.tsx"),D.register(C,"default","/Users/chenming/superset/superset-frontend/src/views/CRUD/annotation/AnnotationList.tsx")),(k="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.leaveModule:void 0)&&k(t)},536120:(t,e,n)=>{n.d(e,{Z:()=>A});var a,o=n(667294),s=n(751995),r=n(455867),l=n(34858),i=n(662276),d=n(730381),c=n.n(d),u=n(87693),m=n(574520),h=n(440768),p=n(414114),f=n(794670),g=n(211965);t=n.hmd(t),(a="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.enterModule:void 0)&&a(t);var b="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.default.signature:function(t){return t};const y=s.iK.div`
  margin: ${({theme:t})=>2*t.gridUnit}px auto
    ${({theme:t})=>4*t.gridUnit}px auto;
`,Z=(0,s.iK)(f.Ad)`
  border-radius: ${({theme:t})=>t.borderRadius}px;
  border: 1px solid ${({theme:t})=>t.colors.secondary.light2};
`,_=s.iK.div`
  margin-bottom: ${({theme:t})=>5*t.gridUnit}px;

  .control-label {
    margin-bottom: ${({theme:t})=>2*t.gridUnit}px;
  }

  .required {
    margin-left: ${({theme:t})=>t.gridUnit/2}px;
    color: ${({theme:t})=>t.colors.error.base};
  }

  textarea {
    flex: 1 1 auto;
    height: ${({theme:t})=>17*t.gridUnit}px;
    resize: none;
    width: 100%;
  }

  textarea,
  input[type='text'] {
    padding: ${({theme:t})=>1.5*t.gridUnit}px
      ${({theme:t})=>2*t.gridUnit}px;
    border: 1px solid ${({theme:t})=>t.colors.grayscale.light2};
    border-radius: ${({theme:t})=>t.gridUnit}px;
  }

  input[type='text'] {
    width: 65%;
  }
`,v=({addDangerToast:t,addSuccessToast:e,annnotationLayerId:n,annotation:a=null,onAnnotationAdd:s,onHide:d,show:p})=>{var f,b;const[v,L]=(0,o.useState)(!0),[A,x]=(0,o.useState)(null),w=null!==a,{state:{loading:H,resource:C},fetchResource:S,createResource:D,updateResource:k}=(0,l.LE)(`annotation_layer/${n}/annotation`,(0,r.t)("annotation"),t),U=()=>{x({short_descr:"",start_dttm:"",end_dttm:"",json_metadata:"",long_descr:""})},$=()=>{w?x(C):U(),d()},G=t=>{const{target:e}=t,n={...A,end_dttm:A?A.end_dttm:"",short_descr:A?A.short_descr:"",start_dttm:A?A.start_dttm:""};n[e.name]=e.value,x(n)};return(0,o.useEffect)((()=>{if(w&&(!A||!A.id||a&&a.id!==A.id||p)){if(a&&null!==a.id&&!H){const t=a.id||0;S(t)}}else w||A&&!A.id&&!p||U()}),[a]),(0,o.useEffect)((()=>{C&&x(C)}),[C]),(0,o.useEffect)((()=>{var t,e,n;A&&null!=(t=A.short_descr)&&t.length&&null!=(e=A.start_dttm)&&e.length&&null!=(n=A.end_dttm)&&n.length?L(!1):L(!0)}),[A?A.short_descr:"",A?A.start_dttm:"",A?A.end_dttm:""]),(0,g.tZ)(m.Z,{disablePrimaryButton:v,onHandledPrimaryAction:()=>{if(w){if(A&&A.id){const t=A.id;delete A.id,delete A.created_by,delete A.changed_by,delete A.changed_on_delta_humanized,delete A.layer,k(t,A).then((t=>{t&&(s&&s(),$(),e((0,r.t)("The annotation has been updated")))}))}}else A&&D(A).then((t=>{t&&(s&&s(),$(),e((0,r.t)("The annotation has been saved")))}))},onHide:$,primaryButtonName:w?(0,r.t)("Save"):(0,r.t)("Add"),show:p,width:"55%",title:(0,g.tZ)("h4",{"data-test":"annotaion-modal-title"},w?(0,g.tZ)(u.Z.EditAlt,{css:h.xL}):(0,g.tZ)(u.Z.PlusLarge,{css:h.xL}),w?(0,r.t)("Edit annotation"):(0,r.t)("Add annotation"))},(0,g.tZ)(y,null,(0,g.tZ)("h4",null,(0,r.t)("Basic information"))),(0,g.tZ)(_,null,(0,g.tZ)("div",{className:"control-label"},(0,r.t)("Annotation name"),(0,g.tZ)("span",{className:"required"},"*")),(0,g.tZ)("input",{name:"short_descr",onChange:G,type:"text",value:null==A?void 0:A.short_descr})),(0,g.tZ)(_,null,(0,g.tZ)("div",{className:"control-label"},(0,r.t)("date"),(0,g.tZ)("span",{className:"required"},"*")),(0,g.tZ)(i.S,{format:"YYYY-MM-DD HH:mm",onChange:(t,e)=>{const n={...A,end_dttm:A&&e[1].length?c()(e[1]).format("YYYY-MM-DD HH:mm"):"",short_descr:A?A.short_descr:"",start_dttm:A&&e[0].length?c()(e[0]).format("YYYY-MM-DD HH:mm"):""};x(n)},showTime:{format:"hh:mm a"},use12Hours:!0,value:null!=A&&null!=(f=A.start_dttm)&&f.length||null!=A&&null!=(b=A.end_dttm)&&b.length?[c()(A.start_dttm),c()(A.end_dttm)]:null})),(0,g.tZ)(y,null,(0,g.tZ)("h4",null,(0,r.t)("Additional information"))),(0,g.tZ)(_,null,(0,g.tZ)("div",{className:"control-label"},(0,r.t)("description")),(0,g.tZ)("textarea",{name:"long_descr",value:A?A.long_descr:"",placeholder:(0,r.t)("Description (this can be seen in the list)"),onChange:G})),(0,g.tZ)(_,null,(0,g.tZ)("div",{className:"control-label"},(0,r.t)("JSON metadata")),(0,g.tZ)(Z,{onChange:t=>{const e={...A,end_dttm:A?A.end_dttm:"",json_metadata:t,short_descr:A?A.short_descr:"",start_dttm:A?A.start_dttm:""};x(e)},value:A&&A.json_metadata?A.json_metadata:"",width:"100%",height:"120px"})))};b(v,"useState{[disableSave, setDisableSave](true)}\nuseState{[currentAnnotation, setCurrentAnnotation](null)}\nuseSingleViewResource{{ state: { loading, resource }, fetchResource, createResource, updateResource, }}\nuseEffect{}\nuseEffect{}\nuseEffect{}",(()=>[l.LE]));const L=(0,p.Z)(v),A=L;var x,w;(x="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.default:void 0)&&(x.register(y,"StyledAnnotationTitle","/Users/chenming/superset/superset-frontend/src/views/CRUD/annotation/AnnotationModal.tsx"),x.register(Z,"StyledJsonEditor","/Users/chenming/superset/superset-frontend/src/views/CRUD/annotation/AnnotationModal.tsx"),x.register(_,"AnnotationContainer","/Users/chenming/superset/superset-frontend/src/views/CRUD/annotation/AnnotationModal.tsx"),x.register(v,"AnnotationModal","/Users/chenming/superset/superset-frontend/src/views/CRUD/annotation/AnnotationModal.tsx"),x.register(L,"default","/Users/chenming/superset/superset-frontend/src/views/CRUD/annotation/AnnotationModal.tsx")),(w="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.leaveModule:void 0)&&w(t)}}]);
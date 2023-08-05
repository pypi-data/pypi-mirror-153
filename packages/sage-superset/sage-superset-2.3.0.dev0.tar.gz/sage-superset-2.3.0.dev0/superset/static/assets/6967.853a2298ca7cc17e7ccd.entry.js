"use strict";(globalThis.webpackChunksuperset=globalThis.webpackChunksuperset||[]).push([[6967],{789719:(e,t,a)=>{a.d(t,{Z:()=>_});var n=a(667294),r=a(751995),s=a(835932),o=a(87693);function l(){return l=Object.assign||function(e){for(var t=1;t<arguments.length;t++){var a=arguments[t];for(var n in a)Object.prototype.hasOwnProperty.call(a,n)&&(e[n]=a[n])}return e},l.apply(this,arguments)}const i={position:"absolute",bottom:0,left:0,height:0,overflow:"hidden","padding-top":0,"padding-bottom":0,border:"none"},d=["box-sizing","width","font-size","font-weight","font-family","font-style","letter-spacing","text-indent","white-space","word-break","overflow-wrap","padding-left","padding-right"];function c(e,t){for(;e&&t--;)e=e.previousElementSibling;return e}const u={basedOn:void 0,className:"",component:"div",ellipsis:"…",maxLine:1,onReflow(){},text:"",trimRight:!0,winWidth:void 0},p=Object.keys(u);class m extends n.Component{constructor(e){super(e),this.state={text:e.text,clamped:!1},this.units=[],this.maxLine=0,this.canvas=null}componentDidMount(){this.initCanvas(),this.reflow(this.props)}componentDidUpdate(e){e.winWidth!==this.props.winWidth&&this.copyStyleToCanvas(),this.props!==e&&this.reflow(this.props)}componentWillUnmount(){this.canvas.parentNode.removeChild(this.canvas)}setState(e,t){return void 0!==e.clamped&&(this.clamped=e.clamped),super.setState(e,t)}initCanvas(){if(this.canvas)return;const e=this.canvas=document.createElement("div");e.className=`LinesEllipsis-canvas ${this.props.className}`,e.setAttribute("aria-hidden","true"),this.copyStyleToCanvas(),Object.keys(i).forEach((t=>{e.style[t]=i[t]})),document.body.appendChild(e)}copyStyleToCanvas(){const e=window.getComputedStyle(this.target);d.forEach((t=>{this.canvas.style[t]=e[t]}))}reflow(e){const t=e.basedOn||(/^[\x00-\x7F]+$/.test(e.text)?"words":"letters");switch(t){case"words":this.units=e.text.split(/\b|(?=\W)/);break;case"letters":this.units=Array.from(e.text);break;default:throw new Error(`Unsupported options basedOn: ${t}`)}this.maxLine=+e.maxLine||1,this.canvas.innerHTML=this.units.map((e=>`<span class='LinesEllipsis-unit'>${e}</span>`)).join("");const a=this.putEllipsis(this.calcIndexes()),n=a>-1,r={clamped:n,text:n?this.units.slice(0,a).join(""):e.text};this.setState(r,e.onReflow.bind(this,r))}calcIndexes(){const e=[0];let t=this.canvas.firstElementChild;if(!t)return e;let a=0,n=1,r=t.offsetTop;for(;(t=t.nextElementSibling)&&(t.offsetTop>r&&(n++,e.push(a),r=t.offsetTop),a++,!(n>this.maxLine)););return e}putEllipsis(e){if(e.length<=this.maxLine)return-1;const t=e[this.maxLine],a=this.units.slice(0,t),n=this.canvas.children[t].offsetTop;this.canvas.innerHTML=a.map(((e,t)=>`<span class='LinesEllipsis-unit'>${e}</span>`)).join("")+`<wbr><span class='LinesEllipsis-ellipsis'>${this.props.ellipsis}</span>`;const r=this.canvas.lastElementChild;let s=c(r,2);for(;s&&(r.offsetTop>n||r.offsetHeight>s.offsetHeight||r.offsetTop>s.offsetTop);)this.canvas.removeChild(s),s=c(r,2),a.pop();return a.length}isClamped(){return this.clamped}render(){const{text:e,clamped:t}=this.state,a=this.props,{component:r,ellipsis:s,trimRight:o,className:i}=a,d=function(e,t){if(null==e)return{};var a,n,r={},s=Object.keys(e);for(n=0;n<s.length;n++)a=s[n],t.indexOf(a)>=0||(r[a]=e[a]);return r}(a,["component","ellipsis","trimRight","className"]);return n.createElement(r,l({className:`LinesEllipsis ${t?"LinesEllipsis--clamped":""} ${i}`,ref:e=>this.target=e},function(e,t){if(!e||"object"!=typeof e)return e;const a={};return Object.keys(e).forEach((n=>{t.indexOf(n)>-1||(a[n]=e[n])})),a}(d,p)),t&&o?e.replace(/[\s\uFEFF\xA0]+$/,""):e,n.createElement("wbr",null),t&&n.createElement("span",{className:"LinesEllipsis-ellipsis"},s))}}m.defaultProps=u;const h=m;var g,b=a(211965);e=a.hmd(e),(g="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.enterModule:void 0)&&g(e),"undefined"!=typeof reactHotLoaderGlobal&&reactHotLoaderGlobal.default.signature;const f=(0,r.iK)(s.Z)`
  height: auto;
  display: flex;
  flex-direction: column;
  padding: 0;
`,v=r.iK.div`
  padding: ${({theme:e})=>4*e.gridUnit}px;
  height: ${({theme:e})=>18*e.gridUnit}px;
  margin: ${({theme:e})=>3*e.gridUnit}px 0;

  .default-db-icon {
    font-size: 36px;
    color: ${({theme:e})=>e.colors.grayscale.base};
    margin-right: 0;
    span:first-of-type {
      margin-right: 0;
    }
  }

  &:first-of-type {
    margin-right: 0;
  }

  img {
    width: ${({theme:e})=>10*e.gridUnit}px;
    height: ${({theme:e})=>10*e.gridUnit}px;
    margin: 0;
    &:first-of-type {
      margin-right: 0;
    }
  }
  svg {
    &:first-of-type {
      margin-right: 0;
    }
  }
`,y=r.iK.div`
  max-height: calc(1.5em * 2);
  white-space: break-spaces;

  &:first-of-type {
    margin-right: 0;
  }

  .LinesEllipsis {
    &:first-of-type {
      margin-right: 0;
    }
  }
`,x=r.iK.div`
  padding: ${({theme:e})=>4*e.gridUnit}px 0;
  border-radius: 0 0 ${({theme:e})=>e.borderRadius}px
    ${({theme:e})=>e.borderRadius}px;
  background-color: ${({theme:e})=>e.colors.grayscale.light4};
  width: 100%;
  line-height: 1.5em;
  overflow: hidden;
  white-space: no-wrap;
  text-overflow: ellipsis;

  &:first-of-type {
    margin-right: 0;
  }
`,Z=(0,r.iK)((({icon:e,altText:t,buttonText:a,...n})=>(0,b.tZ)(f,n,(0,b.tZ)(v,null,e&&(0,b.tZ)("img",{src:e,alt:t}),!e&&(0,b.tZ)(o.Z.DatabaseOutlined,{className:"default-db-icon","aria-label":"default-icon"})),(0,b.tZ)(x,null,(0,b.tZ)(y,null,(0,b.tZ)(h,{text:a,maxLine:"2",basedOn:"words",trimRight:!0}))))))`
  text-transform: none;
  background-color: ${({theme:e})=>e.colors.grayscale.light5};
  font-weight: ${({theme:e})=>e.typography.weights.normal};
  color: ${({theme:e})=>e.colors.grayscale.dark2};
  border: 1px solid ${({theme:e})=>e.colors.grayscale.light2};
  margin: 0;
  width: 100%;

  &:hover,
  &:focus {
    background-color: ${({theme:e})=>e.colors.grayscale.light5};
    color: ${({theme:e})=>e.colors.grayscale.dark2};
    border: 1px solid ${({theme:e})=>e.colors.grayscale.light2};
    box-shadow: 4px 4px 20px ${({theme:e})=>e.colors.grayscale.light2};
  }
`,C=Z,_=C;var w,U;(w="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.default:void 0)&&(w.register(f,"StyledButton","/Users/chenming/superset/superset-frontend/src/components/IconButton/index.tsx"),w.register(v,"StyledImage","/Users/chenming/superset/superset-frontend/src/components/IconButton/index.tsx"),w.register(y,"StyledInner","/Users/chenming/superset/superset-frontend/src/components/IconButton/index.tsx"),w.register(x,"StyledBottom","/Users/chenming/superset/superset-frontend/src/components/IconButton/index.tsx"),w.register(Z,"IconButton","/Users/chenming/superset/superset-frontend/src/components/IconButton/index.tsx"),w.register(C,"default","/Users/chenming/superset/superset-frontend/src/components/IconButton/index.tsx")),(U="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.leaveModule:void 0)&&U(e)},849576:(e,t,a)=>{a.d(t,{Z:()=>f});var n,r=a(667294),s=a(751995),o=a(87693),l=a(211965);e=a.hmd(e),(n="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.enterModule:void 0)&&n(e);var i="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.default.signature:function(e){return e};const d=s.iK.label`
  cursor: pointer;
  display: inline-block;
  margin-bottom: 0;
`,c=(0,s.iK)(o.Z.CheckboxHalf)`
  color: ${({theme:e})=>e.colors.primary.base};
  cursor: pointer;
`,u=(0,s.iK)(o.Z.CheckboxOff)`
  color: ${({theme:e})=>e.colors.grayscale.base};
  cursor: pointer;
`,p=(0,s.iK)(o.Z.CheckboxOn)`
  color: ${({theme:e})=>e.colors.primary.base};
  cursor: pointer;
`,m=s.iK.input`
  &[type='checkbox'] {
    cursor: pointer;
    opacity: 0;
    position: absolute;
    left: 3px;
    margin: 0;
    top: 4px;
  }
`,h=s.iK.div`
  cursor: pointer;
  display: inline-block;
  position: relative;
`,g=(0,r.forwardRef)(i((({indeterminate:e,id:t,checked:a,onChange:n,title:s="",labelText:o=""},i)=>{const g=(0,r.useRef)(),b=i||g;return(0,r.useEffect)((()=>{b.current.indeterminate=e}),[b,e]),(0,l.tZ)(r.Fragment,null,(0,l.tZ)(h,null,e&&(0,l.tZ)(c,null),!e&&a&&(0,l.tZ)(p,null),!e&&!a&&(0,l.tZ)(u,null),(0,l.tZ)(m,{name:t,id:t,type:"checkbox",ref:b,checked:a,onChange:n})),(0,l.tZ)(d,{title:s,htmlFor:t},o))}),"useRef{defaultRef}\nuseEffect{}")),b=g,f=b;var v,y;(v="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.default:void 0)&&(v.register(d,"CheckboxLabel","/Users/chenming/superset/superset-frontend/src/components/IndeterminateCheckbox/index.tsx"),v.register(c,"CheckboxHalf","/Users/chenming/superset/superset-frontend/src/components/IndeterminateCheckbox/index.tsx"),v.register(u,"CheckboxOff","/Users/chenming/superset/superset-frontend/src/components/IndeterminateCheckbox/index.tsx"),v.register(p,"CheckboxOn","/Users/chenming/superset/superset-frontend/src/components/IndeterminateCheckbox/index.tsx"),v.register(m,"HiddenInput","/Users/chenming/superset/superset-frontend/src/components/IndeterminateCheckbox/index.tsx"),v.register(h,"InputContainer","/Users/chenming/superset/superset-frontend/src/components/IndeterminateCheckbox/index.tsx"),v.register(g,"IndeterminateCheckbox","/Users/chenming/superset/superset-frontend/src/components/IndeterminateCheckbox/index.tsx"),v.register(b,"default","/Users/chenming/superset/superset-frontend/src/components/IndeterminateCheckbox/index.tsx")),(y="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.leaveModule:void 0)&&y(e)},523419:(e,t,a)=>{a.d(t,{FQ:()=>u,xP:()=>p,WT:()=>m,qm:()=>h,Uy:()=>g,w_:()=>b,Wj:()=>f,mB:()=>v});var n,r=a(667294),s=a(455867),o=a(104715),l=a(608272),i=a(187858),d=a(853199),c=a(211965);e=a.hmd(e),(n="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.enterModule:void 0)&&n(e),"undefined"!=typeof reactHotLoaderGlobal&&reactHotLoaderGlobal.default.signature;const u=({required:e,changeMethods:t,getValidation:a,validationErrors:n,db:r})=>{var o;return(0,c.tZ)(i.Z,{id:"host",name:"host",value:null==r||null==(o=r.parameters)?void 0:o.host,required:e,hasTooltip:!0,tooltipText:(0,s.t)("This can be either an IP address (e.g. 127.0.0.1) or a domain name (e.g. mydatabase.com)."),validationMethods:{onBlur:a},errorMessage:null==n?void 0:n.host,placeholder:(0,s.t)("e.g. 127.0.0.1"),className:"form-group-w-50",label:(0,s.t)("Host"),onChange:t.onParametersChange})},p=({required:e,changeMethods:t,getValidation:a,validationErrors:n,db:o})=>{var l;return(0,c.tZ)(r.Fragment,null,(0,c.tZ)(i.Z,{id:"port",name:"port",type:"number",required:e,value:null==o||null==(l=o.parameters)?void 0:l.port,validationMethods:{onBlur:a},errorMessage:null==n?void 0:n.port,placeholder:(0,s.t)("e.g. 5432"),className:"form-group-w-50",label:"Port",onChange:t.onParametersChange}))},m=({required:e,changeMethods:t,getValidation:a,validationErrors:n,db:r})=>{var o;return(0,c.tZ)(i.Z,{id:"database",name:"database",required:e,value:null==r||null==(o=r.parameters)?void 0:o.database,validationMethods:{onBlur:a},errorMessage:null==n?void 0:n.database,placeholder:(0,s.t)("e.g. world_population"),label:(0,s.t)("Database name"),onChange:t.onParametersChange,helpText:(0,s.t)("Copy the name of the  database you are trying to connect to.")})},h=({required:e,changeMethods:t,getValidation:a,validationErrors:n,db:r})=>{var o;return(0,c.tZ)(i.Z,{id:"username",name:"username",required:e,value:null==r||null==(o=r.parameters)?void 0:o.username,validationMethods:{onBlur:a},errorMessage:null==n?void 0:n.username,placeholder:(0,s.t)("e.g. Analytics"),label:(0,s.t)("Username"),onChange:t.onParametersChange})},g=({required:e,changeMethods:t,getValidation:a,validationErrors:n,db:r,isEditMode:o})=>{var l;return(0,c.tZ)(i.Z,{id:"password",name:"password",required:e,type:o&&"password",value:null==r||null==(l=r.parameters)?void 0:l.password,validationMethods:{onBlur:a},errorMessage:null==n?void 0:n.password,placeholder:(0,s.t)("e.g. ********"),label:(0,s.t)("Password"),onChange:t.onParametersChange})},b=({changeMethods:e,getValidation:t,validationErrors:a,db:n})=>(0,c.tZ)(r.Fragment,null,(0,c.tZ)(i.Z,{id:"database_name",name:"database_name",required:!0,value:null==n?void 0:n.database_name,validationMethods:{onBlur:t},errorMessage:null==a?void 0:a.database_name,placeholder:"",label:(0,s.t)("Display Name"),onChange:e.onChange,helpText:(0,s.t)("Pick a nickname for this database to display as in Superset.")})),f=({required:e,changeMethods:t,getValidation:a,validationErrors:n,db:r})=>(0,c.tZ)(i.Z,{id:"query_input",name:"query_input",required:e,value:(null==r?void 0:r.query_input)||"",validationMethods:{onBlur:a},errorMessage:null==n?void 0:n.query,placeholder:(0,s.t)("e.g. param1=value1&param2=value2"),label:(0,s.t)("Additional Parameters"),onChange:t.onQueryChange,helpText:(0,s.t)("Add additional custom parameters")}),v=({isEditMode:e,changeMethods:t,db:a,sslForced:n})=>{var r;return(0,c.tZ)("div",{css:e=>(0,d.bC)(e)},(0,c.tZ)(o.KU,{disabled:n&&!e,checked:(null==a||null==(r=a.parameters)?void 0:r.encryption)||n,onChange:e=>{t.onParametersChange({target:{type:"toggle",name:"encryption",checked:!0,value:e}})}}),(0,c.tZ)("span",{css:d.ob},"SSL"),(0,c.tZ)(l.Z,{tooltip:(0,s.t)('SSL Mode "require" will be used.'),placement:"right",viewBox:"0 -5 24 24"}))};var y,x;(y="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.default:void 0)&&(y.register(u,"hostField","/Users/chenming/superset/superset-frontend/src/views/CRUD/data/database/DatabaseModal/DatabaseConnectionForm/CommonParameters.tsx"),y.register(p,"portField","/Users/chenming/superset/superset-frontend/src/views/CRUD/data/database/DatabaseModal/DatabaseConnectionForm/CommonParameters.tsx"),y.register(m,"databaseField","/Users/chenming/superset/superset-frontend/src/views/CRUD/data/database/DatabaseModal/DatabaseConnectionForm/CommonParameters.tsx"),y.register(h,"usernameField","/Users/chenming/superset/superset-frontend/src/views/CRUD/data/database/DatabaseModal/DatabaseConnectionForm/CommonParameters.tsx"),y.register(g,"passwordField","/Users/chenming/superset/superset-frontend/src/views/CRUD/data/database/DatabaseModal/DatabaseConnectionForm/CommonParameters.tsx"),y.register(b,"displayField","/Users/chenming/superset/superset-frontend/src/views/CRUD/data/database/DatabaseModal/DatabaseConnectionForm/CommonParameters.tsx"),y.register(f,"queryField","/Users/chenming/superset/superset-frontend/src/views/CRUD/data/database/DatabaseModal/DatabaseConnectionForm/CommonParameters.tsx"),y.register(v,"forceSSLField","/Users/chenming/superset/superset-frontend/src/views/CRUD/data/database/DatabaseModal/DatabaseConnectionForm/CommonParameters.tsx")),(x="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.leaveModule:void 0)&&x(e)},747196:(e,t,a)=>{a.d(t,{N:()=>f});var n,r=a(667294),s=a(455867),o=a(104715),l=a(608272),i=a(902857),d=a(493695),c=a(853199),u=a(211965);e=a.hmd(e),(n="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.enterModule:void 0)&&n(e);var p,m="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.default.signature:function(e){return e};!function(e){e[e.jsonUpload=0]="jsonUpload",e[e.copyPaste=1]="copyPaste"}(p||(p={}));const h={gsheets:"service_account_info",bigquery:"credentials_info"},g=e=>"true"===e;var b={name:"s5xdrg",styles:"display:flex;align-items:center"};const f=({changeMethods:e,isEditMode:t,db:a,editNewDb:n})=>{var m,f,v;const[y,x]=(0,r.useState)(p.jsonUpload.valueOf()),[Z,C]=(0,r.useState)(null),[_,w]=(0,r.useState)(!0),U="gsheets"===(null==a?void 0:a.engine)?!t&&!_:!t,D=t&&"{}"!==(null==a?void 0:a.encrypted_extra),L=(null==a?void 0:a.engine)&&h[a.engine],S="object"==typeof(null==a||null==(m=a.parameters)?void 0:m[L])?JSON.stringify(null==a||null==(f=a.parameters)?void 0:f[L]):null==a||null==(v=a.parameters)?void 0:v[L];return(0,u.tZ)(c.sv,null,"gsheets"===(null==a?void 0:a.engine)&&(0,u.tZ)("div",{className:"catalog-type-select"},(0,u.tZ)(i.Z,{css:e=>(0,c.tu)(e),required:!0},(0,s.t)("Type of Google Sheets allowed")),(0,u.tZ)(o.IZ,{style:{width:"100%"},defaultValue:D?"false":"true",onChange:e=>w(g(e))},(0,u.tZ)(o.IZ.Option,{value:"true",key:1},(0,s.t)("Publicly shared sheets only")),(0,u.tZ)(o.IZ.Option,{value:"false",key:2},(0,s.t)("Public and privately shared sheets")))),U&&(0,u.tZ)(r.Fragment,null,(0,u.tZ)(i.Z,{required:!0},(0,s.t)("How do you want to enter service account credentials?")),(0,u.tZ)(o.IZ,{defaultValue:y,style:{width:"100%"},onChange:e=>x(e)},(0,u.tZ)(o.IZ.Option,{value:p.jsonUpload},(0,s.t)("Upload JSON file")),(0,u.tZ)(o.IZ.Option,{value:p.copyPaste},(0,s.t)("Copy and Paste JSON credentials")))),y===p.copyPaste||t||n?(0,u.tZ)("div",{className:"input-container"},(0,u.tZ)(i.Z,{required:!0},(0,s.t)("Service Account")),(0,u.tZ)("textarea",{className:"input-form",name:L,value:S,onChange:e.onParametersChange,placeholder:"Paste content of service credentials JSON file here"}),(0,u.tZ)("span",{className:"label-paste"},(0,s.t)("Copy and paste the entire service account .json file here"))):U&&(0,u.tZ)("div",{className:"input-container",css:e=>(0,c.bC)(e)},(0,u.tZ)("div",{css:b},(0,u.tZ)(i.Z,{required:!0},(0,s.t)("Upload Credentials")),(0,u.tZ)(l.Z,{tooltip:(0,s.t)("Use the JSON file you automatically downloaded when creating your service account."),viewBox:"0 0 24 24"})),!Z&&(0,u.tZ)(o.C0,{className:"input-upload-btn",onClick:()=>{var e,t;return null==(e=document)||null==(t=e.getElementById("selectedFile"))?void 0:t.click()}},(0,s.t)("Choose File")),Z&&(0,u.tZ)("div",{className:"input-upload-current"},Z,(0,u.tZ)(d.Z,{onClick:()=>{C(null),e.onParametersChange({target:{name:L,value:""}})}})),(0,u.tZ)("input",{id:"selectedFile",className:"input-upload",type:"file",onChange:async t=>{var a,n;let r;t.target.files&&(r=t.target.files[0]),C(null==(a=r)?void 0:a.name),e.onParametersChange({target:{type:null,name:L,value:await(null==(n=r)?void 0:n.text()),checked:!1}}),document.getElementById("selectedFile").value=null}})))};var v,y;m(f,"useState{[uploadOption, setUploadOption](CredentialInfoOptions.jsonUpload.valueOf())}\nuseState{[fileToUpload, setFileToUpload](null)}\nuseState{[isPublic, setIsPublic](true)}"),(v="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.default:void 0)&&(v.register(p,"CredentialInfoOptions","/Users/chenming/superset/superset-frontend/src/views/CRUD/data/database/DatabaseModal/DatabaseConnectionForm/EncryptedField.tsx"),v.register(h,"encryptedCredentialsMap","/Users/chenming/superset/superset-frontend/src/views/CRUD/data/database/DatabaseModal/DatabaseConnectionForm/EncryptedField.tsx"),v.register(g,"castStringToBoolean","/Users/chenming/superset/superset-frontend/src/views/CRUD/data/database/DatabaseModal/DatabaseConnectionForm/EncryptedField.tsx"),v.register(f,"EncryptedField","/Users/chenming/superset/superset-frontend/src/views/CRUD/data/database/DatabaseModal/DatabaseConnectionForm/EncryptedField.tsx")),(y="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.leaveModule:void 0)&&y(e)},241644:(e,t,a)=>{a.d(t,{O:()=>u});var n,r=a(667294),s=a(455867),o=a(187858),l=a(902857),i=a(154549),d=a(853199),c=a(211965);e=a.hmd(e),(n="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.enterModule:void 0)&&n(e),"undefined"!=typeof reactHotLoaderGlobal&&reactHotLoaderGlobal.default.signature;const u=({required:e,changeMethods:t,getValidation:a,validationErrors:n,db:u})=>{const p=(null==u?void 0:u.catalog)||[],m=n||{};return(0,c.tZ)(d.ed,null,(0,c.tZ)("h4",{className:"gsheet-title"},(0,s.t)("Connect Google Sheets as tables to this database")),(0,c.tZ)("div",null,null==p?void 0:p.map(((n,d)=>{var u,h;return(0,c.tZ)(r.Fragment,null,(0,c.tZ)(l.Z,{className:"catalog-label",required:!0},(0,s.t)("Google Sheet Name and URL")),(0,c.tZ)("div",{className:"catalog-name"},(0,c.tZ)(o.Z,{className:"catalog-name-input",required:e,validationMethods:{onBlur:a},errorMessage:null==(u=m[d])?void 0:u.name,placeholder:(0,s.t)("Enter a name for this sheet"),onChange:e=>{t.onParametersChange({target:{type:`catalog-${d}`,name:"name",value:e.target.value}})},value:n.name}),(null==p?void 0:p.length)>1&&(0,c.tZ)(i.Z,{className:"catalog-delete",onClick:()=>t.onRemoveTableCatalog(d)})),(0,c.tZ)(o.Z,{className:"catalog-name-url",required:e,validationMethods:{onBlur:a},errorMessage:null==(h=m[d])?void 0:h.url,placeholder:(0,s.t)("Paste the shareable Google Sheet URL here"),onChange:e=>t.onParametersChange({target:{type:`catalog-${d}`,name:"value",value:e.target.value}}),value:n.value}))})),(0,c.tZ)(d.OD,{className:"catalog-add-btn",onClick:()=>{t.onAddTableCatalog()}},"+ ",(0,s.t)("Add sheet"))))};var p,m;(p="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.default:void 0)&&p.register(u,"TableCatalog","/Users/chenming/superset/superset-frontend/src/views/CRUD/data/database/DatabaseModal/DatabaseConnectionForm/TableCatalog.tsx"),(m="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.leaveModule:void 0)&&m(e)},809034:(e,t,a)=>{a.d(t,{N:()=>i}),a(667294);var n,r=a(455867),s=a(187858),o=a(211965);e=a.hmd(e),(n="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.enterModule:void 0)&&n(e),"undefined"!=typeof reactHotLoaderGlobal&&reactHotLoaderGlobal.default.signature;const l={account:{helpText:(0,r.t)("Copy the account name of that database you are trying to connect to."),placeholder:"e.g. world_population"},warehouse:{placeholder:"e.g. compute_wh",className:"form-group-w-50"},role:{placeholder:"e.g. AccountAdmin",className:"form-group-w-50"}},i=({required:e,changeMethods:t,getValidation:a,validationErrors:n,db:r,field:i})=>{var d;return(0,o.tZ)(s.Z,{id:i,name:i,required:e,value:null==r||null==(d=r.parameters)?void 0:d[i],validationMethods:{onBlur:a},errorMessage:null==n?void 0:n[i],placeholder:l[i].placeholder,helpText:l[i].helpText,label:i,onChange:t.onParametersChange,className:l[i].className||i})};var d,c;(d="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.default:void 0)&&(d.register(l,"FIELD_TEXT_MAP","/Users/chenming/superset/superset-frontend/src/views/CRUD/data/database/DatabaseModal/DatabaseConnectionForm/ValidatedInputField.tsx"),d.register(i,"validatedInputField","/Users/chenming/superset/superset-frontend/src/views/CRUD/data/database/DatabaseModal/DatabaseConnectionForm/ValidatedInputField.tsx")),(c="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.leaveModule:void 0)&&c(e)},804904:(e,t,a)=>{a.d(t,{ZP:()=>b});var n,r=a(667294),s=a(523419),o=a(809034),l=a(747196),i=a(241644),d=a(853199),c=a(211965);e=a.hmd(e),(n="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.enterModule:void 0)&&n(e),"undefined"!=typeof reactHotLoaderGlobal&&reactHotLoaderGlobal.default.signature;const u=["host","port","database","username","password","database_name","credentials_info","service_account_info","catalog","query","encryption","account","warehouse","role"],p={host:s.FQ,port:s.xP,database:s.WT,username:s.qm,password:s.Uy,database_name:s.w_,query:s.Wj,encryption:s.mB,credentials_info:l.N,service_account_info:l.N,catalog:i.O,warehouse:o.N,role:o.N,account:o.N},m=({dbModel:{parameters:e},onParametersChange:t,onChange:a,onQueryChange:n,onParametersUploadFileChange:s,onAddTableCatalog:o,onRemoveTableCatalog:l,validationErrors:i,getValidation:m,db:h,isEditMode:g=!1,sslForced:b,editNewDb:f})=>(0,c.tZ)(r.Fragment,null,(0,c.tZ)("div",{css:e=>[d.$G,(0,d.ro)(e)]},e&&u.filter((t=>Object.keys(e.properties).includes(t)||"database_name"===t)).map((r=>{var d;return p[r]({required:null==(d=e.required)?void 0:d.includes(r),changeMethods:{onParametersChange:t,onChange:a,onQueryChange:n,onParametersUploadFileChange:s,onAddTableCatalog:o,onRemoveTableCatalog:l},validationErrors:i,getValidation:m,db:h,key:r,field:r,isEditMode:g,sslForced:b,editNewDb:f})})))),h=p,g=m,b=g;var f,v;(f="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.default:void 0)&&(f.register(u,"FormFieldOrder","/Users/chenming/superset/superset-frontend/src/views/CRUD/data/database/DatabaseModal/DatabaseConnectionForm/index.tsx"),f.register(p,"FORM_FIELD_MAP","/Users/chenming/superset/superset-frontend/src/views/CRUD/data/database/DatabaseModal/DatabaseConnectionForm/index.tsx"),f.register(m,"DatabaseConnectionForm","/Users/chenming/superset/superset-frontend/src/views/CRUD/data/database/DatabaseModal/DatabaseConnectionForm/index.tsx"),f.register(h,"FormFieldMap","/Users/chenming/superset/superset-frontend/src/views/CRUD/data/database/DatabaseModal/DatabaseConnectionForm/index.tsx"),f.register(g,"default","/Users/chenming/superset/superset-frontend/src/views/CRUD/data/database/DatabaseModal/DatabaseConnectionForm/index.tsx")),(v="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.leaveModule:void 0)&&v(e)},222607:(e,t,a)=>{a.d(t,{Z:()=>h});var n,r=a(211965),s=(a(667294),a(294184)),o=a.n(s),l=a(455867),i=a(608272),d=a(849576),c=a(843700),u=a(853199);e=a.hmd(e),(n="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.enterModule:void 0)&&n(e),"undefined"!=typeof reactHotLoaderGlobal&&reactHotLoaderGlobal.default.signature;const p=({db:e,onInputChange:t,onTextChange:a,onEditorChange:n,onExtraInputChange:s,onExtraEditorChange:p})=>{var m,h,g,b,f,v,y,x,Z,C,_;const w=!(null==e||!e.expose_in_sqllab),U=!!(null!=e&&e.allow_ctas||null!=e&&e.allow_cvas);return(0,r.tZ)(c.Z,{expandIconPosition:"right",accordion:!0,css:e=>(0,u.ls)(e)},(0,r.tZ)(c.Z.Panel,{header:(0,r.tZ)("div",null,(0,r.tZ)("h4",null,"SQL Lab"),(0,r.tZ)("p",{className:"helper"},"Adjust how this database will interact with SQL Lab.")),key:"1"},(0,r.tZ)(u.j5,{css:u.R6},(0,r.tZ)("div",{className:"input-container"},(0,r.tZ)(d.Z,{id:"expose_in_sqllab",indeterminate:!1,checked:!(null==e||!e.expose_in_sqllab),onChange:t,labelText:(0,l.t)("Expose database in SQL Lab")}),(0,r.tZ)(i.Z,{tooltip:(0,l.t)("Allow this database to be queried in SQL Lab")})),(0,r.tZ)(u.J7,{className:o()("expandable",{open:w,"ctas-open":U})},(0,r.tZ)(u.j5,{css:u.R6},(0,r.tZ)("div",{className:"input-container"},(0,r.tZ)(d.Z,{id:"allow_ctas",indeterminate:!1,checked:!(null==e||!e.allow_ctas),onChange:t,labelText:(0,l.t)("Allow CREATE TABLE AS")}),(0,r.tZ)(i.Z,{tooltip:(0,l.t)("Allow creation of new tables based on queries")}))),(0,r.tZ)(u.j5,{css:u.R6},(0,r.tZ)("div",{className:"input-container"},(0,r.tZ)(d.Z,{id:"allow_cvas",indeterminate:!1,checked:!(null==e||!e.allow_cvas),onChange:t,labelText:(0,l.t)("Allow CREATE VIEW AS")}),(0,r.tZ)(i.Z,{tooltip:(0,l.t)("Allow creation of new views based on queries")})),(0,r.tZ)(u.j5,{className:o()("expandable",{open:U})},(0,r.tZ)("div",{className:"control-label"},(0,l.t)("CTAS & CVAS SCHEMA")),(0,r.tZ)("div",{className:"input-container"},(0,r.tZ)("input",{type:"text",name:"force_ctas_schema",value:(null==e?void 0:e.force_ctas_schema)||"",placeholder:(0,l.t)("Create or select schema..."),onChange:t})),(0,r.tZ)("div",{className:"helper"},(0,l.t)("Force all tables and views to be created in this schema when clicking CTAS or CVAS in SQL Lab.")))),(0,r.tZ)(u.j5,{css:u.R6},(0,r.tZ)("div",{className:"input-container"},(0,r.tZ)(d.Z,{id:"allow_dml",indeterminate:!1,checked:!(null==e||!e.allow_dml),onChange:t,labelText:(0,l.t)("Allow DML")}),(0,r.tZ)(i.Z,{tooltip:(0,l.t)("Allow manipulation of the database using non-SELECT statements such as UPDATE, DELETE, CREATE, etc.")}))),(0,r.tZ)(u.j5,{css:u.R6},(0,r.tZ)("div",{className:"input-container"},(0,r.tZ)(d.Z,{id:"allow_multi_schema_metadata_fetch",indeterminate:!1,checked:!(null==e||!e.allow_multi_schema_metadata_fetch),onChange:t,labelText:(0,l.t)("Allow Multi Schema Metadata Fetch")}),(0,r.tZ)(i.Z,{tooltip:(0,l.t)("Allow SQL Lab to fetch a list of all tables and all views across all database schemas. For large data warehouse with thousands of tables, this can be expensive and put strain on the system.")}))),(0,r.tZ)(u.j5,{css:u.R6},(0,r.tZ)("div",{className:"input-container"},(0,r.tZ)(d.Z,{id:"cost_estimate_enabled",indeterminate:!1,checked:!(null==e||null==(m=e.extra_json)||!m.cost_estimate_enabled),onChange:s,labelText:(0,l.t)("Enable query cost estimation")}),(0,r.tZ)(i.Z,{tooltip:(0,l.t)("For Presto and Postgres, shows a button to compute cost before running a query.")}))),(0,r.tZ)(u.j5,null,(0,r.tZ)("div",{className:"input-container"},(0,r.tZ)(d.Z,{id:"allows_virtual_table_explore",indeterminate:!1,checked:!(null==e||null==(h=e.extra_json)||!h.allows_virtual_table_explore),onChange:s,labelText:(0,l.t)("Allow this database to be explored")}),(0,r.tZ)(i.Z,{tooltip:(0,l.t)("When enabled, users are able to visualize SQL Lab results in Explore.")})))))),(0,r.tZ)(c.Z.Panel,{header:(0,r.tZ)("div",null,(0,r.tZ)("h4",null,"Performance"),(0,r.tZ)("p",{className:"helper"},"Adjust performance settings of this database.")),key:"2"},(0,r.tZ)(u.j5,{className:"mb-8"},(0,r.tZ)("div",{className:"control-label"},(0,l.t)("Chart cache timeout")),(0,r.tZ)("div",{className:"input-container"},(0,r.tZ)("input",{type:"number",name:"cache_timeout",value:(null==e?void 0:e.cache_timeout)||"",placeholder:(0,l.t)("Enter duration in seconds"),onChange:t})),(0,r.tZ)("div",{className:"helper"},(0,l.t)("Duration (in seconds) of the caching timeout for charts of this database. A timeout of 0 indicates that the cache never expires. Note this defaults to the global timeout if undefined."))),(0,r.tZ)(u.j5,null,(0,r.tZ)("div",{className:"control-label"},(0,l.t)("Schema cache timeout")),(0,r.tZ)("div",{className:"input-container"},(0,r.tZ)("input",{type:"number",name:"schema_cache_timeout",value:(null==e||null==(g=e.extra_json)||null==(b=g.metadata_cache_timeout)?void 0:b.schema_cache_timeout)||"",placeholder:(0,l.t)("Enter duration in seconds"),onChange:s,"data-test":"schema-cache-timeout-test"})),(0,r.tZ)("div",{className:"helper"},(0,l.t)("Duration (in seconds) of the metadata caching timeout for schemas of this database. If left unset, the cache never expires."))),(0,r.tZ)(u.j5,null,(0,r.tZ)("div",{className:"control-label"},(0,l.t)("Table cache timeout")),(0,r.tZ)("div",{className:"input-container"},(0,r.tZ)("input",{type:"number",name:"table_cache_timeout",value:(null==e||null==(f=e.extra_json)||null==(v=f.metadata_cache_timeout)?void 0:v.table_cache_timeout)||"",placeholder:(0,l.t)("Enter duration in seconds"),onChange:s,"data-test":"table-cache-timeout-test"})),(0,r.tZ)("div",{className:"helper"},(0,l.t)("Duration (in seconds) of the metadata caching timeout for tables of this database. If left unset, the cache never expires. "))),(0,r.tZ)(u.j5,{css:(0,r.iv)({no_margin_bottom:u.R6},"","")},(0,r.tZ)("div",{className:"input-container"},(0,r.tZ)(d.Z,{id:"allow_run_async",indeterminate:!1,checked:!(null==e||!e.allow_run_async),onChange:t,labelText:(0,l.t)("Asynchronous query execution")}),(0,r.tZ)(i.Z,{tooltip:(0,l.t)("Operate the database in asynchronous mode, meaning that the queries are executed on remote workers as opposed to on the web server itself. This assumes that you have a Celery worker setup as well as a results backend. Refer to the installation docs for more information.")}))),(0,r.tZ)(u.j5,{css:(0,r.iv)({no_margin_bottom:u.R6},"","")},(0,r.tZ)("div",{className:"input-container"},(0,r.tZ)(d.Z,{id:"cancel_query_on_windows_unload",indeterminate:!1,checked:!(null==e||null==(y=e.extra_json)||!y.cancel_query_on_windows_unload),onChange:s,labelText:(0,l.t)("Cancel query on window unload event")}),(0,r.tZ)(i.Z,{tooltip:(0,l.t)("Terminate running queries when browser window closed or navigated to another page. Available for Presto, Hive, MySQL, Postgres and Snowflake databases.")})))),(0,r.tZ)(c.Z.Panel,{header:(0,r.tZ)("div",null,(0,r.tZ)("h4",null,"Security"),(0,r.tZ)("p",{className:"helper"},"Add extra connection information.")),key:"3"},(0,r.tZ)(u.j5,null,(0,r.tZ)("div",{className:"control-label"},(0,l.t)("Secure extra")),(0,r.tZ)("div",{className:"input-container"},(0,r.tZ)(u.YT,{name:"encrypted_extra",value:(null==e?void 0:e.encrypted_extra)||"",placeholder:(0,l.t)("Secure extra"),onChange:e=>n({json:e,name:"encrypted_extra"}),width:"100%",height:"160px"})),(0,r.tZ)("div",{className:"helper"},(0,r.tZ)("div",null,(0,l.t)("JSON string containing additional connection configuration. This is used to provide connection information for systems like Hive, Presto and BigQuery which do not conform to the username:password syntax normally used by SQLAlchemy.")))),(0,r.tZ)(u.j5,null,(0,r.tZ)("div",{className:"control-label"},(0,l.t)("Root certificate")),(0,r.tZ)("div",{className:"input-container"},(0,r.tZ)("textarea",{name:"server_cert",value:(null==e?void 0:e.server_cert)||"",placeholder:(0,l.t)("Enter CA_BUNDLE"),onChange:a})),(0,r.tZ)("div",{className:"helper"},(0,l.t)("Optional CA_BUNDLE contents to validate HTTPS requests. Only available on certain database engines."))),(0,r.tZ)(u.j5,null,(0,r.tZ)("div",{className:"control-label"},(0,l.t)("Schemas allowed for CSV upload")),(0,r.tZ)("div",{className:"input-container"},(0,r.tZ)("input",{type:"text",name:"schemas_allowed_for_file_upload",value:((null==e||null==(x=e.extra_json)?void 0:x.schemas_allowed_for_file_upload)||[]).join(","),placeholder:"schema1,schema2",onChange:s})),(0,r.tZ)("div",{className:"helper"},(0,l.t)("A comma-separated list of schemas that CSVs are allowed to upload to."))),(0,r.tZ)(u.j5,{css:(0,r.iv)({no_margin_bottom:u.R6},"","")},(0,r.tZ)("div",{className:"input-container"},(0,r.tZ)(d.Z,{id:"impersonate_user",indeterminate:!1,checked:!(null==e||!e.impersonate_user),onChange:t,labelText:(0,l.t)("Impersonate logged in user (Presto, Trino, Drill, Hive, and GSheets)")}),(0,r.tZ)(i.Z,{tooltip:(0,l.t)("If Presto or Trino, all the queries in SQL Lab are going to be executed as the currently logged on user who must have permission to run them. If Hive and hive.server2.enable.doAs is enabled, will run the queries as service account, but impersonate the currently logged on user via hive.server2.proxy.user property.")}))),(0,r.tZ)(u.j5,{css:(0,r.iv)({...u.R6},"","")},(0,r.tZ)("div",{className:"input-container"},(0,r.tZ)(d.Z,{id:"allow_file_upload",indeterminate:!1,checked:!(null==e||!e.allow_file_upload),onChange:t,labelText:(0,l.t)("Allow data upload")}),(0,r.tZ)(i.Z,{tooltip:(0,l.t)("If selected, please set the schemas allowed for data upload in Extra.")})))),(0,r.tZ)(c.Z.Panel,{header:(0,r.tZ)("div",null,(0,r.tZ)("h4",null,"Other"),(0,r.tZ)("p",{className:"helper"},"Additional settings.")),key:"4"},(0,r.tZ)(u.j5,null,(0,r.tZ)("div",{className:"control-label"},(0,l.t)("Metadata Parameters")),(0,r.tZ)("div",{className:"input-container"},(0,r.tZ)(u.YT,{name:"metadata_params",value:(null==e||null==(Z=e.extra_json)?void 0:Z.metadata_params)||"",placeholder:(0,l.t)("Metadata Parameters"),onChange:e=>p({json:e,name:"metadata_params"}),width:"100%",height:"160px"})),(0,r.tZ)("div",{className:"helper"},(0,r.tZ)("div",null,(0,l.t)("The metadata_params object gets unpacked into the sqlalchemy.MetaData call.")))),(0,r.tZ)(u.j5,null,(0,r.tZ)("div",{className:"control-label"},(0,l.t)("Engine Parameters")),(0,r.tZ)("div",{className:"input-container"},(0,r.tZ)(u.YT,{name:"engine_params",value:(null==e||null==(C=e.extra_json)?void 0:C.engine_params)||"",placeholder:(0,l.t)("Engine Parameters"),onChange:e=>p({json:e,name:"engine_params"}),width:"100%",height:"160px"})),(0,r.tZ)("div",{className:"helper"},(0,r.tZ)("div",null,(0,l.t)("The engine_params object gets unpacked into the sqlalchemy.create_engine call.")))),(0,r.tZ)(u.j5,null,(0,r.tZ)("div",{className:"control-label","data-test":"version-label-test"},(0,l.t)("Version")),(0,r.tZ)("div",{className:"input-container","data-test":"version-spinbutton-test"},(0,r.tZ)("input",{type:"number",name:"version",value:(null==e||null==(_=e.extra_json)?void 0:_.version)||"",placeholder:(0,l.t)("Version number"),onChange:s})),(0,r.tZ)("div",{className:"helper"},(0,l.t)("Specify the database version. This should be used with Presto in order to enable query cost estimation.")))))},m=p,h=m;var g,b;(g="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.default:void 0)&&(g.register(p,"ExtraOptions","/Users/chenming/superset/superset-frontend/src/views/CRUD/data/database/DatabaseModal/ExtraOptions.tsx"),g.register(m,"default","/Users/chenming/superset/superset-frontend/src/views/CRUD/data/database/DatabaseModal/ExtraOptions.tsx")),(b="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.leaveModule:void 0)&&b(e)},854790:(e,t,a)=>{a.d(t,{s:()=>d,Z:()=>h});var n,r=a(667294),s=a(34858),o=a(853199),l=a(211965);e=a.hmd(e),(n="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.enterModule:void 0)&&n(e),"undefined"!=typeof reactHotLoaderGlobal&&reactHotLoaderGlobal.default.signature;const i=(0,s.z)(),d=i?i.support:"https://superset.apache.org/docs/databases/installing-database-drivers",c={postgresql:"https://superset.apache.org/docs/databases/postgres",mssql:"https://superset.apache.org/docs/databases/sql-server",gsheets:"https://superset.apache.org/docs/databases/google-sheets"},u=e=>e?i?i[e]||i.default:c[e]?c[e]:`https://superset.apache.org/docs/databases/${e}`:null,p=({isLoading:e,isEditMode:t,useSqlAlchemyForm:a,hasConnectedDb:n,db:s,dbName:c,dbModel:p,editNewDb:m})=>{const h=(0,l.tZ)(o.mI,null,(0,l.tZ)(o._7,null,null==s?void 0:s.backend),(0,l.tZ)(o.ZM,null,c)),g=(0,l.tZ)(o.mI,null,(0,l.tZ)("p",{className:"helper-top"}," STEP 2 OF 2 "),(0,l.tZ)("h4",null,"Enter Primary Credentials"),(0,l.tZ)("p",{className:"helper-bottom"},"Need help? Learn how to connect your database"," ",(0,l.tZ)("a",{href:(null==i?void 0:i.default)||d,target:"_blank",rel:"noopener noreferrer"},"here"),".")),b=(0,l.tZ)(o.SS,null,(0,l.tZ)(o.mI,null,(0,l.tZ)("p",{className:"helper-top"}," STEP 3 OF 3 "),(0,l.tZ)("h4",{className:"step-3-text"},"Your database was successfully connected! Here are some optional settings for your database"),(0,l.tZ)("p",{className:"helper-bottom"},"Need help? Learn more about"," ",(0,l.tZ)("a",{href:u(null==s?void 0:s.engine),target:"_blank",rel:"noopener noreferrer"},"connecting to ",p.name,".")))),f=(0,l.tZ)(o.SS,null,(0,l.tZ)(o.mI,null,(0,l.tZ)("p",{className:"helper-top"}," STEP 2 OF 3 "),(0,l.tZ)("h4",null,"Enter the required ",p.name," credentials"),(0,l.tZ)("p",{className:"helper-bottom"},"Need help? Learn more about"," ",(0,l.tZ)("a",{href:u(null==s?void 0:s.engine),target:"_blank",rel:"noopener noreferrer"},"connecting to ",p.name,".")))),v=(0,l.tZ)(o.mI,null,(0,l.tZ)("div",{className:"select-db"},(0,l.tZ)("p",{className:"helper-top"}," STEP 1 OF 3 "),(0,l.tZ)("h4",null,"Select a database to connect")));return e?(0,l.tZ)(r.Fragment,null):t?h:a?g:n&&!m?b:s||m?f:v},m=p,h=m;var g,b;(g="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.default:void 0)&&(g.register(i,"supersetTextDocs","/Users/chenming/superset/superset-frontend/src/views/CRUD/data/database/DatabaseModal/ModalHeader.tsx"),g.register(d,"DOCUMENTATION_LINK","/Users/chenming/superset/superset-frontend/src/views/CRUD/data/database/DatabaseModal/ModalHeader.tsx"),g.register(c,"irregularDocumentationLinks","/Users/chenming/superset/superset-frontend/src/views/CRUD/data/database/DatabaseModal/ModalHeader.tsx"),g.register(u,"documentationLink","/Users/chenming/superset/superset-frontend/src/views/CRUD/data/database/DatabaseModal/ModalHeader.tsx"),g.register(p,"ModalHeader","/Users/chenming/superset/superset-frontend/src/views/CRUD/data/database/DatabaseModal/ModalHeader.tsx"),g.register(m,"default","/Users/chenming/superset/superset-frontend/src/views/CRUD/data/database/DatabaseModal/ModalHeader.tsx")),(b="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.leaveModule:void 0)&&b(e)},89728:(e,t,a)=>{a.d(t,{Z:()=>p});var n,r=a(667294),s=a(455867),o=a(208911),l=a(835932),i=a(853199),d=a(211965);e=a.hmd(e),(n="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.enterModule:void 0)&&n(e),"undefined"!=typeof reactHotLoaderGlobal&&reactHotLoaderGlobal.default.signature;const c=({db:e,onInputChange:t,testConnection:a,conf:n,isEditMode:c=!1,testInProgress:u=!1})=>{let p,m;var h,g;return o.Z&&(p=null==(h=o.Z.DB_MODAL_SQLALCHEMY_FORM)?void 0:h.SQLALCHEMY_DOCS_URL,m=null==(g=o.Z.DB_MODAL_SQLALCHEMY_FORM)?void 0:g.SQLALCHEMY_DOCS_URL),(0,d.tZ)(r.Fragment,null,(0,d.tZ)(i.j5,null,(0,d.tZ)("div",{className:"control-label"},(0,s.t)("Display Name"),(0,d.tZ)("span",{className:"required"},"*")),(0,d.tZ)("div",{className:"input-container"},(0,d.tZ)("input",{type:"text",name:"database_name","data-test":"database-name-input",value:(null==e?void 0:e.database_name)||"",placeholder:(0,s.t)("Name your database"),onChange:t})),(0,d.tZ)("div",{className:"helper"},(0,s.t)("Pick a name to help you identify this database."))),(0,d.tZ)(i.j5,null,(0,d.tZ)("div",{className:"control-label"},(0,s.t)("SQLAlchemy URI"),(0,d.tZ)("span",{className:"required"},"*")),(0,d.tZ)("div",{className:"input-container"},(0,d.tZ)("input",{type:"text",name:"sqlalchemy_uri","data-test":"sqlalchemy-uri-input",value:(null==e?void 0:e.sqlalchemy_uri)||"",autoComplete:"off",placeholder:(0,s.t)("dialect+driver://username:password@host:port/database"),onChange:t})),(0,d.tZ)("div",{className:"helper"},(0,s.t)("Refer to the")," ",(0,d.tZ)("a",{href:p||(null==n?void 0:n.SQLALCHEMY_DOCS_URL)||"",target:"_blank",rel:"noopener noreferrer"},m||(null==n?void 0:n.SQLALCHEMY_DISPLAY_TEXT)||"")," ",(0,s.t)("for more information on how to structure your URI."))),(0,d.tZ)(l.Z,{onClick:a,disabled:u,cta:!0,buttonStyle:"link",css:e=>(0,i.Gy)(e)},(0,s.t)("Test connection")))},u=c,p=u;var m,h;(m="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.default:void 0)&&(m.register(c,"SqlAlchemyTab","/Users/chenming/superset/superset-frontend/src/views/CRUD/data/database/DatabaseModal/SqlAlchemyForm.tsx"),m.register(u,"default","/Users/chenming/superset/superset-frontend/src/views/CRUD/data/database/DatabaseModal/SqlAlchemyForm.tsx")),(h="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.leaveModule:void 0)&&h(e)},603506:(e,t,a)=>{a.d(t,{Z:()=>H});var n,r=a(455867),s=a(593185),o=a(667294),l=a(940637),i=a(104715),d=a(229487),c=a(574520),u=a(835932),p=a(789719),m=a(608272),h=a(414114),g=a(34858),b=a(301483),f=a(163727),v=a(838703),y=a(222607),x=a(89728),Z=a(804904),C=a(853199),_=a(854790),w=a(211965);e=a.hmd(e),(n="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.enterModule:void 0)&&n(e);var U="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.default.signature:function(e){return e};const D={gsheets:{message:"Why do I need to create a database?",description:"To begin using your Google Sheets, you need to create a database first. Databases are used as a way to identify your data so that it can be queried and visualized. This database will hold all of your individual Google Sheets you choose to connect here."}},L={CONNECTION_MISSING_PARAMETERS_ERROR:{message:(0,r.t)("Missing Required Fields"),description:(0,r.t)("Please complete all required fields.")},CONNECTION_INVALID_HOSTNAME_ERROR:{message:(0,r.t)("Could not verify the host"),description:(0,r.t)("The host is invalid. Please verify that this field is entered correctly.")},CONNECTION_PORT_CLOSED_ERROR:{message:(0,r.t)("Port is closed"),description:(0,r.t)("Please verify that port is open to connect.")},CONNECTION_INVALID_PORT_ERROR:{message:(0,r.t)("Invalid Port Number"),description:(0,r.t)("The port must be a whole number less than or equal to 65535.")},CONNECTION_ACCESS_DENIED_ERROR:{message:(0,r.t)("Invalid account information"),description:(0,r.t)("Either the username or password is incorrect.")},CONNECTION_INVALID_PASSWORD_ERROR:{message:(0,r.t)("Invalid account information"),description:(0,r.t)("Either the username or password is incorrect.")},INVALID_PAYLOAD_SCHEMA_ERROR:{message:(0,r.t)("Incorrect Fields"),description:(0,r.t)("Please make sure all fields are filled out correctly")},TABLE_DOES_NOT_EXIST_ERROR:{message:(0,r.t)("URL could not be identified"),description:(0,r.t)('The URL could not be identified. Please check for typos and make sure that "Type of google sheet allowed" selection matches the input')}};var S;function M(e,t){var a,n,r,s;const o={...e||{}};let l,i={},d="",c={allows_virtual_table_explore:!0};switch(t.type){case S.extraEditorChange:return{...o,extra_json:{...o.extra_json,[t.payload.name]:t.payload.json}};case S.extraInputChange:var u;return"schema_cache_timeout"===t.payload.name||"table_cache_timeout"===t.payload.name?{...o,extra_json:{...o.extra_json,metadata_cache_timeout:{...null==(u=o.extra_json)?void 0:u.metadata_cache_timeout,[t.payload.name]:t.payload.value}}}:"schemas_allowed_for_file_upload"===t.payload.name?{...o,extra_json:{...o.extra_json,schemas_allowed_for_file_upload:(t.payload.value||"").split(",")}}:{...o,extra_json:{...o.extra_json,[t.payload.name]:"checkbox"===t.payload.type?t.payload.checked:t.payload.value}};case S.inputChange:return"checkbox"===t.payload.type?{...o,[t.payload.name]:t.payload.checked}:{...o,[t.payload.name]:t.payload.value};case S.parametersChange:if(void 0!==o.catalog&&null!=(a=t.payload.type)&&a.startsWith("catalog")){var p,m;const e=null==(p=t.payload.type)?void 0:p.split("-")[1];((null==o?void 0:o.catalog[e])||{})[t.payload.name]=t.payload.value;const a={};return null==(m=o.catalog)||m.map((e=>{a[e.name]=e.value})),{...o,parameters:{...o.parameters,catalog:a}}}return{...o,parameters:{...o.parameters,[t.payload.name]:t.payload.value}};case S.addTableCatalogSheet:return void 0!==o.catalog?{...o,catalog:[...o.catalog,{name:"",value:""}]}:{...o,catalog:[{name:"",value:""}]};case S.removeTableCatalogSheet:return null==(n=o.catalog)||n.splice(t.payload.indexToDelete,1),{...o};case S.editorChange:return{...o,[t.payload.name]:t.payload.json};case S.queryChange:return{...o,parameters:{...o.parameters,query:Object.fromEntries(new URLSearchParams(t.payload.value))},query_input:t.payload.value};case S.textChange:return{...o,[t.payload.name]:t.payload.value};case S.fetched:var h,g,b;if(t.payload.extra&&(l={...JSON.parse(t.payload.extra||"")},c={...JSON.parse(t.payload.extra||""),metadata_params:JSON.stringify(null==(h=l)?void 0:h.metadata_params),engine_params:JSON.stringify(null==(g=l)?void 0:g.engine_params),schemas_allowed_for_file_upload:null==(b=l)?void 0:b.schemas_allowed_for_file_upload}),i=(null==(r=t.payload)||null==(s=r.parameters)?void 0:s.query)||{},d=Object.entries(i).map((([e,t])=>`${e}=${t}`)).join("&"),t.payload.encrypted_extra&&t.payload.configuration_method===f.j.DYNAMIC_FORM){var v,y;const e=Object.keys((null==(v=l)||null==(y=v.engine_params)?void 0:y.catalog)||{}).map((e=>{var t,a;return{name:e,value:null==(t=l)||null==(a=t.engine_params)?void 0:a.catalog[e]}}));return{...t.payload,engine:t.payload.backend||o.engine,configuration_method:t.payload.configuration_method,extra_json:c,catalog:e,parameters:t.payload.parameters,query_input:d}}return{...t.payload,encrypted_extra:t.payload.encrypted_extra||"",engine:t.payload.backend||o.engine,configuration_method:t.payload.configuration_method,extra_json:c,parameters:t.payload.parameters,query_input:d};case S.dbSelected:case S.configMethodChange:return{...t.payload};case S.reset:default:return null}}!function(e){e[e.configMethodChange=0]="configMethodChange",e[e.dbSelected=1]="dbSelected",e[e.editorChange=2]="editorChange",e[e.fetched=3]="fetched",e[e.inputChange=4]="inputChange",e[e.parametersChange=5]="parametersChange",e[e.reset=6]="reset",e[e.textChange=7]="textChange",e[e.extraInputChange=8]="extraInputChange",e[e.extraEditorChange=9]="extraEditorChange",e[e.addTableCatalogSheet=10]="addTableCatalogSheet",e[e.removeTableCatalogSheet=11]="removeTableCatalogSheet",e[e.queryChange=12]="queryChange"}(S||(S={}));const E="1",N=e=>JSON.stringify({...e,metadata_params:JSON.parse((null==e?void 0:e.metadata_params)||"{}"),engine_params:JSON.parse((null==e?void 0:e.engine_params)||"{}"),schemas_allowed_for_file_upload:((null==e?void 0:e.schemas_allowed_for_file_upload)||[]).filter((e=>""!==e))}),$=({addDangerToast:e,addSuccessToast:t,onDatabaseAdd:a,onHide:n,show:h,databaseId:U,dbEngine:$})=>{var k;const[H,R]=(0,o.useReducer)(M,null),[T,G]=(0,o.useState)(E),[A,O]=(0,g.cb)(),[I,F,P]=(0,g.h1)(),[j,q]=(0,o.useState)(!1),[z,B]=(0,o.useState)(""),[K,V]=(0,o.useState)(!1),[Q,Y]=(0,o.useState)(!1),[J,W]=(0,o.useState)(!1),X=(0,b.c)(),ee=(0,g.rM)(),te=(0,g.jb)(),ae=!!U,ne=(0,s.c)(s.T.FORCE_DATABASE_CONNECTIONS_SSL),re=te||!(null==H||!H.engine||!D[H.engine]),se=(null==H?void 0:H.configuration_method)===f.j.SQLALCHEMY_URI,oe=ae||se,{state:{loading:le,resource:ie,error:de},fetchResource:ce,createResource:ue,updateResource:pe,clearError:me}=(0,g.LE)("database",(0,r.t)("database"),e),he=I||de,ge=e=>e&&0===Object.keys(e).length,be=(null==A||null==(k=A.databases)?void 0:k.find((e=>e.engine===(ae?null==H?void 0:H.backend:null==H?void 0:H.engine))))||{},fe=()=>{R({type:S.reset}),q(!1),P(null),me(),V(!1),n()},ve=async()=>{var e;const{id:n,...s}=H||{},o=JSON.parse(JSON.stringify(s));if(o.configuration_method===f.j.DYNAMIC_FORM){if(await F(o,!0),I&&!ge(I))return;const e=ae?o.parameters_schema.properties:null==be?void 0:be.parameters.properties,t=JSON.parse(o.encrypted_extra||"{}");Object.keys(e||{}).forEach((a=>{var n,r,s,l;e[a]["x-encrypted-extra"]&&null!=(n=o.parameters)&&n[a]&&("object"==typeof(null==(r=o.parameters)?void 0:r[a])?(t[a]=null==(s=o.parameters)?void 0:s[a],o.parameters[a]=JSON.stringify(o.parameters[a])):t[a]=JSON.parse((null==(l=o.parameters)?void 0:l[a])||"{}"))})),o.encrypted_extra=JSON.stringify(t),"gsheets"===o.engine&&(o.impersonate_user=!0)}null!=o&&null!=(e=o.parameters)&&e.catalog&&(o.extra_json={engine_params:JSON.stringify({catalog:o.parameters.catalog})}),null!=o&&o.extra_json&&(o.extra=N(null==o?void 0:o.extra_json)),null!=H&&H.id?(Y(!0),await pe(H.id,o,o.configuration_method===f.j.DYNAMIC_FORM)&&(a&&a(),K||(fe(),t((0,r.t)("Database settings updated"))))):H&&(Y(!0),await ue(o,o.configuration_method===f.j.DYNAMIC_FORM)&&(q(!0),a&&a(),oe&&(fe(),t((0,r.t)("Database connected"))))),V(!1),Y(!1)},ye=(e,t)=>{R({type:e,payload:t})},xe=e=>{if("Other"===e)R({type:S.dbSelected,payload:{database_name:e,configuration_method:f.j.SQLALCHEMY_URI,engine:void 0}});else{const t=null==A?void 0:A.databases.filter((t=>t.name===e))[0],{engine:a,parameters:n}=t,r=void 0!==n;R({type:S.dbSelected,payload:{database_name:e,engine:a,configuration_method:r?f.j.DYNAMIC_FORM:f.j.SQLALCHEMY_URI}})}R({type:S.addTableCatalogSheet})},Ze=()=>{ie&&ce(ie.id),V(!0)},Ce=()=>{K&&q(!1),R({type:S.reset})},_e=()=>H?!j||K?(0,w.tZ)(o.Fragment,null,(0,w.tZ)(C.OD,{key:"back",onClick:Ce},(0,r.t)("Back")),(0,w.tZ)(C.OD,{key:"submit",buttonStyle:"primary",onClick:ve},(0,r.t)("Connect"))):(0,w.tZ)(o.Fragment,null,(0,w.tZ)(C.OD,{key:"back",onClick:Ze},(0,r.t)("Back")),(0,w.tZ)(C.OD,{key:"submit",buttonStyle:"primary",onClick:ve,"data-test":"modal-confirm-button"},(0,r.t)("Finish"))):[];(0,o.useEffect)((()=>{h&&(G(E),O(),Y(!0)),U&&h&&ae&&U&&(le||ce(U).catch((t=>e((0,r.t)("Sorry there was an error fetching database information: %s",t.message)))))}),[h,U]),(0,o.useEffect)((()=>{ie&&(R({type:S.fetched,payload:ie}),B(ie.database_name))}),[ie]),(0,o.useEffect)((()=>{Q&&Y(!1),A&&$&&xe($)}),[A]);const we=()=>{if(ge(de)||ge(I)&&!((null==I?void 0:I.error_type)in L))return(0,w.tZ)(o.Fragment,null);var e,t;if(I)return(0,w.tZ)(d.Z,{type:"error",css:e=>(0,C.gH)(e),message:(null==(e=L[null==I?void 0:I.error_type])?void 0:e.message)||(null==I?void 0:I.error_type),description:(null==(t=L[null==I?void 0:I.error_type])?void 0:t.description)||JSON.stringify(I),showIcon:!0,closable:!1});const a="object"==typeof de?Object.values(de):[];return(0,w.tZ)(d.Z,{type:"error",css:e=>(0,C.gH)(e),message:(0,r.t)("Database Creation Error"),description:(null==a?void 0:a[0])||de})};return oe?(0,w.tZ)(c.Z,{css:e=>[C.B2,C.jo,(0,C.fj)(e),(0,C.qS)(e),(0,C.xk)(e)],name:"database","data-test":"database-modal",onHandledPrimaryAction:ve,onHide:fe,primaryButtonName:ae?(0,r.t)("Save"):(0,r.t)("Connect"),width:"500px",centered:!0,show:h,title:(0,w.tZ)("h4",null,ae?(0,r.t)("Edit database"):(0,r.t)("Connect a database")),footer:ae?(0,w.tZ)(o.Fragment,null,(0,w.tZ)(C.OD,{key:"close",onClick:fe},(0,r.t)("Close")),(0,w.tZ)(C.OD,{key:"submit",buttonStyle:"primary",onClick:ve},(0,r.t)("Finish"))):_e()},(0,w.tZ)(C.SS,null,(0,w.tZ)(C.GK,null,(0,w.tZ)(_.Z,{isLoading:Q,isEditMode:ae,useSqlAlchemyForm:se,hasConnectedDb:j,db:H,dbName:z,dbModel:be}))),(0,w.tZ)(l.ZP,{defaultActiveKey:E,activeKey:T,onTabClick:e=>{G(e)},animated:{inkBar:!0,tabPane:!0}},(0,w.tZ)(l.ZP.TabPane,{tab:(0,w.tZ)("span",null,(0,r.t)("Basic")),key:"1"},se?(0,w.tZ)(C.LC,null,(0,w.tZ)(x.Z,{db:H,onInputChange:({target:e})=>ye(S.inputChange,{type:e.type,name:e.name,checked:e.checked,value:e.value}),conf:X,testConnection:()=>{var a;if(null==H||!H.sqlalchemy_uri)return void e((0,r.t)("Please enter a SQLAlchemy URI to test"));const n={sqlalchemy_uri:(null==H?void 0:H.sqlalchemy_uri)||"",database_name:(null==H||null==(a=H.database_name)?void 0:a.trim())||void 0,impersonate_user:(null==H?void 0:H.impersonate_user)||void 0,extra:N(null==H?void 0:H.extra_json)||void 0,encrypted_extra:(null==H?void 0:H.encrypted_extra)||"",server_cert:(null==H?void 0:H.server_cert)||void 0};W(!0),(0,g.xx)(n,(t=>{W(!1),e(t)}),(e=>{W(!1),t(e)}))},isEditMode:ae,testInProgress:J}),(Se=(null==H?void 0:H.backend)||(null==H?void 0:H.engine),void 0!==(null==A||null==(Me=A.databases)||null==(Ee=Me.find((e=>e.backend===Se||e.engine===Se)))?void 0:Ee.parameters)&&!ae&&(0,w.tZ)("div",{css:e=>(0,C.bC)(e)},(0,w.tZ)(u.Z,{buttonStyle:"link",onClick:()=>R({type:S.configMethodChange,payload:{database_name:null==H?void 0:H.database_name,configuration_method:f.j.DYNAMIC_FORM,engine:null==H?void 0:H.engine}}),css:e=>(0,C.iz)(e)},(0,r.t)("Connect this database using the dynamic form instead")),(0,w.tZ)(m.Z,{tooltip:(0,r.t)("Click this link to switch to an alternate form that exposes only the required fields needed to connect this database."),viewBox:"0 -6 24 24"})))):(0,w.tZ)(Z.ZP,{isEditMode:!0,sslForced:ne,dbModel:be,db:H,onParametersChange:({target:e})=>ye(S.parametersChange,{type:e.type,name:e.name,checked:e.checked,value:e.value}),onChange:({target:e})=>ye(S.textChange,{name:e.name,value:e.value}),onQueryChange:({target:e})=>ye(S.queryChange,{name:e.name,value:e.value}),onAddTableCatalog:()=>R({type:S.addTableCatalogSheet}),onRemoveTableCatalog:e=>R({type:S.removeTableCatalogSheet,payload:{indexToDelete:e}}),getValidation:()=>F(H),validationErrors:I}),!ae&&(0,w.tZ)(C.u_,null,(0,w.tZ)(d.Z,{closable:!1,css:e=>(0,C.Yd)(e),message:"Additional fields may be required",showIcon:!0,description:(0,w.tZ)(o.Fragment,null,(0,r.t)("Select databases require additional fields to be completed in the Advanced tab to successfully connect the database. Learn what requirements your databases has "),(0,w.tZ)("a",{href:_.s,target:"_blank",rel:"noopener noreferrer",className:"additional-fields-alert-description"},(0,r.t)("here")),"."),type:"info"}))),(0,w.tZ)(l.ZP.TabPane,{tab:(0,w.tZ)("span",null,(0,r.t)("Advanced")),key:"2"},(0,w.tZ)(y.Z,{db:H,onInputChange:({target:e})=>ye(S.inputChange,{type:e.type,name:e.name,checked:e.checked,value:e.value}),onTextChange:({target:e})=>ye(S.textChange,{name:e.name,value:e.value}),onEditorChange:e=>ye(S.editorChange,e),onExtraInputChange:({target:e})=>{ye(S.extraInputChange,{type:e.type,name:e.name,checked:e.checked,value:e.value})},onExtraEditorChange:e=>{ye(S.extraEditorChange,e)}}),he&&we()))):(0,w.tZ)(c.Z,{css:e=>[C.jo,(0,C.fj)(e),(0,C.qS)(e),(0,C.xk)(e)],name:"database",onHandledPrimaryAction:ve,onHide:fe,primaryButtonName:j?(0,r.t)("Finish"):(0,r.t)("Connect"),width:"500px",centered:!0,show:h,title:(0,w.tZ)("h4",null,(0,r.t)("Connect a database")),footer:_e()},j?(0,w.tZ)(o.Fragment,null,(0,w.tZ)(_.Z,{isLoading:Q,isEditMode:ae,useSqlAlchemyForm:se,hasConnectedDb:j,db:H,dbName:z,dbModel:be,editNewDb:K}),K?(0,w.tZ)(Z.ZP,{isEditMode:!0,sslForced:ne,dbModel:be,db:H,onParametersChange:({target:e})=>ye(S.parametersChange,{type:e.type,name:e.name,checked:e.checked,value:e.value}),onChange:({target:e})=>ye(S.textChange,{name:e.name,value:e.value}),onQueryChange:({target:e})=>ye(S.queryChange,{name:e.name,value:e.value}),onAddTableCatalog:()=>R({type:S.addTableCatalogSheet}),onRemoveTableCatalog:e=>R({type:S.removeTableCatalogSheet,payload:{indexToDelete:e}}),getValidation:()=>F(H),validationErrors:I}):(0,w.tZ)(y.Z,{db:H,onInputChange:({target:e})=>ye(S.inputChange,{type:e.type,name:e.name,checked:e.checked,value:e.value}),onTextChange:({target:e})=>ye(S.textChange,{name:e.name,value:e.value}),onEditorChange:e=>ye(S.editorChange,e),onExtraInputChange:({target:e})=>{ye(S.extraInputChange,{type:e.type,name:e.name,checked:e.checked,value:e.value})},onExtraEditorChange:e=>ye(S.extraEditorChange,e)})):(0,w.tZ)(o.Fragment,null,!Q&&(H?(0,w.tZ)(o.Fragment,null,(0,w.tZ)(_.Z,{isLoading:Q,isEditMode:ae,useSqlAlchemyForm:se,hasConnectedDb:j,db:H,dbName:z,dbModel:be}),re&&(()=>{var e,t,a,n,r;const{hostname:s}=window.location;let o=(null==te||null==(e=te.REGIONAL_IPS)?void 0:e.default)||"";const l=(null==te?void 0:te.REGIONAL_IPS)||{};return Object.entries(l).forEach((([e,t])=>{const a=new RegExp(e);s.match(a)&&(o=t)})),(null==H?void 0:H.engine)&&(0,w.tZ)(C.u_,null,(0,w.tZ)(d.Z,{closable:!1,css:e=>(0,C.Yd)(e),type:"info",showIcon:!0,message:(null==(t=D[H.engine])?void 0:t.message)||(null==te||null==(a=te.DEFAULT)?void 0:a.message),description:(null==(n=D[H.engine])?void 0:n.description)||(null==te||null==(r=te.DEFAULT)?void 0:r.description)+o}))})(),(0,w.tZ)(Z.ZP,{db:H,sslForced:ne,dbModel:be,onAddTableCatalog:()=>{R({type:S.addTableCatalogSheet})},onQueryChange:({target:e})=>ye(S.queryChange,{name:e.name,value:e.value}),onRemoveTableCatalog:e=>{R({type:S.removeTableCatalogSheet,payload:{indexToDelete:e}})},onParametersChange:({target:e})=>ye(S.parametersChange,{type:e.type,name:e.name,checked:e.checked,value:e.value}),onChange:({target:e})=>ye(S.textChange,{name:e.name,value:e.value}),getValidation:()=>F(H),validationErrors:I}),(0,w.tZ)("div",{css:e=>(0,C.bC)(e)},(0,w.tZ)(u.Z,{"data-test":"sqla-connect-btn",buttonStyle:"link",onClick:()=>R({type:S.configMethodChange,payload:{engine:H.engine,configuration_method:f.j.SQLALCHEMY_URI,database_name:H.database_name}}),css:C.Hd},(0,r.t)("Connect this database with a SQLAlchemy URI string instead")),(0,w.tZ)(m.Z,{tooltip:(0,r.t)("Click this link to switch to an alternate form that allows you to input the SQLAlchemy URL for this database manually."),viewBox:"0 -6 24 24"})),he&&we()):(0,w.tZ)(C.Q0,null,(0,w.tZ)(_.Z,{isLoading:Q,isEditMode:ae,useSqlAlchemyForm:se,hasConnectedDb:j,db:H,dbName:z,dbModel:be}),(0,w.tZ)("div",{className:"preferred"},null==A||null==(Le=A.databases)?void 0:Le.filter((e=>e.preferred)).map((e=>(0,w.tZ)(p.Z,{className:"preferred-item",onClick:()=>xe(e.name),buttonText:e.name,icon:null==ee?void 0:ee[e.engine]})))),(0,w.tZ)("div",{className:"available"},(0,w.tZ)("h4",{className:"available-label"},(0,r.t)("Or choose from a list of other databases we support:")),(0,w.tZ)("div",{className:"control-label"},(0,r.t)("Supported databases")),(0,w.tZ)(i.IZ,{className:"available-select",onChange:xe,placeholder:(0,r.t)("Choose a database...")},null==(Ue=[...(null==A?void 0:A.databases)||[]])?void 0:Ue.sort(((e,t)=>e.name.localeCompare(t.name))).map((e=>(0,w.tZ)(i.IZ.Option,{value:e.name,key:e.name},e.name))),(0,w.tZ)(i.IZ.Option,{value:"Other",key:"Other"},(0,r.t)("Other"))),(0,w.tZ)(d.Z,{showIcon:!0,closable:!1,css:e=>(0,C.Yd)(e),type:"info",message:(null==te||null==(De=te.ADD_DATABASE)?void 0:De.message)||(0,r.t)("Want to add a new database?"),description:null!=te&&te.ADD_DATABASE?(0,w.tZ)(o.Fragment,null,(0,r.t)("Any databases that allow connections via SQL Alchemy URIs can be added. "),(0,w.tZ)("a",{href:null==te?void 0:te.ADD_DATABASE.contact_link,target:"_blank",rel:"noopener noreferrer"},null==te?void 0:te.ADD_DATABASE.contact_description_link)," ",null==te?void 0:te.ADD_DATABASE.description):(0,w.tZ)(o.Fragment,null,(0,r.t)("Any databases that allow connections via SQL Alchemy URIs can be added. Learn about how to connect a database driver "),(0,w.tZ)("a",{href:_.s,target:"_blank",rel:"noopener noreferrer"},(0,r.t)("here")),".")}))))),Q&&(0,w.tZ)(v.Z,null));var Ue,De,Le,Se,Me,Ee};U($,"useReducer{[db, setDB](null)}\nuseState{[tabKey, setTabKey](DEFAULT_TAB_KEY)}\nuseAvailableDatabases{[availableDbs, getAvailableDbs]}\nuseDatabaseValidation{[validationErrors, getValidation, setValidationErrors]}\nuseState{[hasConnectedDb, setHasConnectedDb](false)}\nuseState{[dbName, setDbName]('')}\nuseState{[editNewDb, setEditNewDb](false)}\nuseState{[isLoading, setLoading](false)}\nuseState{[testInProgress, setTestInProgress](false)}\nuseCommonConf{conf}\nuseSingleViewResource{{ state: { loading: dbLoading, resource: dbFetched, error: dbErrors }, fetchResource, createResource, updateResource, clearError, }}\nuseEffect{}\nuseEffect{}\nuseEffect{}",(()=>[g.cb,g.h1,b.c,g.LE]));const k=(0,h.Z)($),H=k;var R,T;(R="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.default:void 0)&&(R.register(D,"engineSpecificAlertMapping","/Users/chenming/superset/superset-frontend/src/views/CRUD/data/database/DatabaseModal/index.tsx"),R.register(L,"errorAlertMapping","/Users/chenming/superset/superset-frontend/src/views/CRUD/data/database/DatabaseModal/index.tsx"),R.register(S,"ActionType","/Users/chenming/superset/superset-frontend/src/views/CRUD/data/database/DatabaseModal/index.tsx"),R.register(M,"dbReducer","/Users/chenming/superset/superset-frontend/src/views/CRUD/data/database/DatabaseModal/index.tsx"),R.register(E,"DEFAULT_TAB_KEY","/Users/chenming/superset/superset-frontend/src/views/CRUD/data/database/DatabaseModal/index.tsx"),R.register(N,"serializeExtra","/Users/chenming/superset/superset-frontend/src/views/CRUD/data/database/DatabaseModal/index.tsx"),R.register($,"DatabaseModal","/Users/chenming/superset/superset-frontend/src/views/CRUD/data/database/DatabaseModal/index.tsx"),R.register(k,"default","/Users/chenming/superset/superset-frontend/src/views/CRUD/data/database/DatabaseModal/index.tsx")),(T="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.leaveModule:void 0)&&T(e)},853199:(e,t,a)=>{a.d(t,{R6:()=>i,tu:()=>d,mI:()=>c,ls:()=>u,B2:()=>p,jo:()=>m,bC:()=>h,ob:()=>g,$G:()=>b,fj:()=>f,Yd:()=>v,u_:()=>y,gH:()=>x,qS:()=>Z,Gy:()=>C,xk:()=>_,ro:()=>w,j5:()=>U,YT:()=>D,J7:()=>L,LC:()=>S,Hd:()=>M,iz:()=>E,GK:()=>N,_7:()=>H,ZM:()=>R,sv:()=>T,Q0:()=>G,OD:()=>A,SS:()=>O,ed:()=>I});var n,r=a(211965),s=a(751995),o=a(794670),l=a(835932);e=a.hmd(e),(n="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.enterModule:void 0)&&n(e),"undefined"!=typeof reactHotLoaderGlobal&&reactHotLoaderGlobal.default.signature;const i=r.iv`
  margin-bottom: 0;
`,d=e=>r.iv`
  margin-bottom: ${2*e.gridUnit}px;
`,c=s.iK.header`
  border-bottom: ${({theme:e})=>`${.25*e.gridUnit}px solid\n    ${e.colors.grayscale.light2};`}
  padding: ${({theme:e})=>2*e.gridUnit}px
    ${({theme:e})=>4*e.gridUnit}px;
  line-height: ${({theme:e})=>6*e.gridUnit}px;

  .helper-top {
    padding-bottom: 0;
    color: ${({theme:e})=>e.colors.grayscale.base};
    font-size: ${({theme:e})=>e.typography.sizes.s-1}px;
    margin: 0;
  }

  .helper-bottom {
    padding-top: 0;
    color: ${({theme:e})=>e.colors.grayscale.base};
    font-size: ${({theme:e})=>e.typography.sizes.s-1}px;
    margin: 0;
  }

  h4 {
    color: ${({theme:e})=>e.colors.grayscale.dark2};
    font-weight: bold;
    font-size: ${({theme:e})=>e.typography.sizes.l}px;
    margin: 0;
    padding: 0;
    line-height: ${({theme:e})=>8*e.gridUnit}px;
  }

  .select-db {
    padding-bottom: ${({theme:e})=>2*e.gridUnit}px;
    .helper {
      margin: 0;
    }

    h4 {
      margin: 0 0 ${({theme:e})=>4*e.gridUnit}px;
    }
  }
`,u=e=>r.iv`
  .ant-collapse-header {
    padding-top: ${3.5*e.gridUnit}px;
    padding-bottom: ${2.5*e.gridUnit}px;

    .anticon.ant-collapse-arrow {
      top: calc(50% - ${6}px);
    }
    .helper {
      color: ${e.colors.grayscale.base};
    }
  }
  h4 {
    font-size: 16px;
    font-weight: bold;
    margin-top: 0;
    margin-bottom: ${e.gridUnit}px;
  }
  p.helper {
    margin-bottom: 0;
    padding: 0;
  }
`,p=r.iv`
  .ant-tabs-top {
    margin-top: 0;
  }
  .ant-tabs-top > .ant-tabs-nav {
    margin-bottom: 0;
  }
  .ant-tabs-tab {
    margin-right: 0;
  }
`,m=r.iv`
  .ant-modal-body {
    padding-left: 0;
    padding-right: 0;
    padding-top: 0;
  }
`,h=e=>r.iv`
  margin-bottom: ${5*e.gridUnit}px;
  svg {
    margin-bottom: ${.25*e.gridUnit}px;
  }
`,g=e=>r.iv`
  padding-left: ${2*e.gridUnit}px;
`,b=e=>r.iv`
  padding: ${4*e.gridUnit}px ${4*e.gridUnit}px 0;
`,f=e=>r.iv`
  .ant-select-dropdown {
    height: ${40*e.gridUnit}px;
  }

  .ant-modal-header {
    padding: ${4.5*e.gridUnit}px ${4*e.gridUnit}px
      ${4*e.gridUnit}px;
  }

  .ant-modal-close-x .close {
    color: ${e.colors.grayscale.dark1};
    opacity: 1;
  }

  .ant-modal-title > h4 {
    font-weight: bold;
  }

  .ant-modal-body {
    height: ${180.5*e.gridUnit}px;
  }

  .ant-modal-footer {
    height: ${16.25*e.gridUnit}px;
  }
`,v=e=>r.iv`
  border: 1px solid ${e.colors.info.base};
  padding: ${4*e.gridUnit}px;
  margin: ${4*e.gridUnit}px 0;

  .ant-alert-message {
    color: ${e.colors.info.dark2};
    font-size: ${e.typography.sizes.s+1}px;
    font-weight: bold;
  }

  .ant-alert-description {
    color: ${e.colors.info.dark2};
    font-size: ${e.typography.sizes.s+1}px;
    line-height: ${4*e.gridUnit}px;

    a {
      text-decoration: underline;
    }

    .ant-alert-icon {
      margin-right: ${2.5*e.gridUnit}px;
      font-size: ${e.typography.sizes.l+1}px;
      position: relative;
      top: ${e.gridUnit/4}px;
    }
  }
`,y=s.iK.div`
  margin: 0 ${({theme:e})=>4*e.gridUnit}px -${({theme:e})=>4*e.gridUnit}px;
`,x=e=>r.iv`
  border: ${e.colors.error.base} 1px solid;
  padding: ${4*e.gridUnit}px;
  margin: ${8*e.gridUnit}px ${4*e.gridUnit}px;
  color: ${e.colors.error.dark2};
  .ant-alert-message {
    font-size: ${e.typography.sizes.s+1}px;
    font-weight: bold;
  }
  .ant-alert-description {
    font-size: ${e.typography.sizes.s+1}px;
    line-height: ${4*e.gridUnit}px;
    .ant-alert-icon {
      margin-right: ${2.5*e.gridUnit}px;
      font-size: ${e.typography.sizes.l+1}px;
      position: relative;
      top: ${e.gridUnit/4}px;
    }
  }
`,Z=e=>r.iv`
  .required {
    margin-left: ${e.gridUnit/2}px;
    color: ${e.colors.error.base};
  }

  .helper {
    display: block;
    padding: ${e.gridUnit}px 0;
    color: ${e.colors.grayscale.light1};
    font-size: ${e.typography.sizes.s-1}px;
    text-align: left;
  }
`,C=e=>r.iv`
  width: 100%;
  border: 1px solid ${e.colors.primary.dark2};
  color: ${e.colors.primary.dark2};
  &:hover,
  &:focus {
    border: 1px solid ${e.colors.primary.dark1};
    color: ${e.colors.primary.dark1};
  }
`,_=e=>r.iv`
  .form-group {
    margin-bottom: ${4*e.gridUnit}px;
    &-w-50 {
      display: inline-block;
      width: ${`calc(50% - ${4*e.gridUnit}px)`};
      & + .form-group-w-50 {
        margin-left: ${8*e.gridUnit}px;
        margin-bottom: ${10*e.gridUnit}px;
      }
    }
  }
  .control-label {
    color: ${e.colors.grayscale.dark1};
    font-size: ${e.typography.sizes.s-1}px;
  }
  .helper {
    color: ${e.colors.grayscale.light1};
    font-size: ${e.typography.sizes.s-1}px;
    margin-top: ${1.5*e.gridUnit}px;
  }
  .ant-tabs-content-holder {
    overflow: auto;
    max-height: 475px;
  }
`,w=e=>r.iv`
  label {
    color: ${e.colors.grayscale.dark1};
    font-size: ${e.typography.sizes.s-1}px;
    margin-bottom: 0;
  }
`,U=s.iK.div`
  margin-bottom: ${({theme:e})=>6*e.gridUnit}px;
  &.mb-0 {
    margin-bottom: 0;
  }
  &.mb-8 {
    margin-bottom: ${({theme:e})=>2*e.gridUnit}px;
  }

  .control-label {
    color: ${({theme:e})=>e.colors.grayscale.dark1};
    font-size: ${({theme:e})=>e.typography.sizes.s-1}px;
    margin-bottom: ${({theme:e})=>2*e.gridUnit}px;
  }

  &.extra-container {
    padding-top: 8px;
  }

  .input-container {
    display: flex;
    align-items: top;

    label {
      display: flex;
      margin-left: ${({theme:e})=>2*e.gridUnit}px;
      margin-top: ${({theme:e})=>.75*e.gridUnit}px;
      font-family: ${({theme:e})=>e.typography.families.sansSerif};
      font-size: ${({theme:e})=>e.typography.sizes.m}px;
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
  }
  &.expandable {
    height: 0;
    overflow: hidden;
    transition: height 0.25s;
    margin-left: ${({theme:e})=>8*e.gridUnit}px;
    margin-bottom: 0;
    padding: 0;
    .control-label {
      margin-bottom: 0;
    }
    &.open {
      height: ${102}px;
      padding-right: ${({theme:e})=>5*e.gridUnit}px;
    }
  }
`,D=(0,s.iK)(o.Ad)`
  flex: 1 1 auto;
  border: 1px solid ${({theme:e})=>e.colors.grayscale.light2};
  border-radius: ${({theme:e})=>e.gridUnit}px;
`,L=s.iK.div`
  padding-top: ${({theme:e})=>e.gridUnit}px;
  .input-container {
    padding-top: ${({theme:e})=>e.gridUnit}px;
    padding-bottom: ${({theme:e})=>e.gridUnit}px;
  }
  &.expandable {
    height: 0;
    overflow: hidden;
    transition: height 0.25s;
    margin-left: ${({theme:e})=>7*e.gridUnit}px;
    &.open {
      height: ${255}px;
      &.ctas-open {
        height: ${357}px;
      }
    }
  }
`,S=s.iK.div`
  padding: 0 ${({theme:e})=>4*e.gridUnit}px;
  margin-top: ${({theme:e})=>6*e.gridUnit}px;
`,M=e=>r.iv`
  font-weight: 400;
  text-transform: initial;
  padding-right: ${2*e.gridUnit}px;
`,E=e=>r.iv`
  font-weight: 400;
  text-transform: initial;
  padding: ${8*e.gridUnit}px 0 0;
  margin-left: 0px;
`,N=s.iK.div`
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 0px;

  .helper {
    color: ${({theme:e})=>e.colors.grayscale.base};
    font-size: ${({theme:e})=>e.typography.sizes.s-1}px;
    margin: 0px;
  }
`,$=s.iK.div`
  color: ${({theme:e})=>e.colors.grayscale.dark2};
  font-weight: bold;
  font-size: ${({theme:e})=>e.typography.sizes.m}px;
`,k=s.iK.div`
  color: ${({theme:e})=>e.colors.grayscale.dark1};
  font-size: ${({theme:e})=>e.typography.sizes.s}px;
`,H=s.iK.div`
  color: ${({theme:e})=>e.colors.grayscale.light1};
  font-size: ${({theme:e})=>e.typography.sizes.s-1}px;
  text-transform: uppercase;
`,R=s.iK.div`
  color: ${({theme:e})=>e.colors.grayscale.dark1};
  font-size: ${({theme:e})=>e.typography.sizes.l}px;
  font-weight: bold;
`,T=s.iK.div`
  .catalog-type-select {
    margin: 0 0 20px;
  }

  .label-select {
    text-transform: uppercase;
    color: ${({theme:e})=>e.colors.grayscale.dark1};
    font-size: 11px;
    margin: 0 5px ${({theme:e})=>2*e.gridUnit}px;
  }

  .label-paste {
    color: ${({theme:e})=>e.colors.grayscale.light1};
    font-size: 11px;
    line-height: 16px;
  }

  .input-container {
    margin: ${({theme:e})=>7*e.gridUnit}px 0;
    display: flex;
    flex-direction: column;
}
  }
  .input-form {
    height: 100px;
    width: 100%;
    border: 1px solid ${({theme:e})=>e.colors.grayscale.light2};
    border-radius: ${({theme:e})=>e.gridUnit}px;
    resize: vertical;
    padding: ${({theme:e})=>1.5*e.gridUnit}px
      ${({theme:e})=>2*e.gridUnit}px;
    &::placeholder {
      color: ${({theme:e})=>e.colors.grayscale.light1};
    }
  }

  .input-container {
    .input-upload {
      display: none;
    }
    .input-upload-current {
      display: flex;
      justify-content: space-between;
    }
    .input-upload-btn {
      width: ${({theme:e})=>32*e.gridUnit}px
    }
  }`,G=s.iK.div`
  .preferred {
    .superset-button {
      margin-left: 0;
    }
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    margin: ${({theme:e})=>4*e.gridUnit}px;
  }

  .preferred-item {
    width: 32%;
    margin-bottom: ${({theme:e})=>2.5*e.gridUnit}px;
  }

  .available {
    margin: ${({theme:e})=>4*e.gridUnit}px;
    .available-label {
      font-size: ${({theme:e})=>1.1*e.typography.sizes.l}px;
      font-weight: bold;
      margin: ${({theme:e})=>6*e.gridUnit}px 0;
    }
    .available-select {
      width: 100%;
    }
  }

  .label-available-select {
    text-transform: uppercase;
    font-size: ${({theme:e})=>e.typography.sizes.s-1}px;
  }

  .control-label {
    color: ${({theme:e})=>e.colors.grayscale.dark1};
    font-size: ${({theme:e})=>e.typography.sizes.s-1}px;
    margin-bottom: ${({theme:e})=>2*e.gridUnit}px;
  }
`,A=(0,s.iK)(l.Z)`
  width: ${({theme:e})=>40*e.gridUnit}px;
`,O=s.iK.div`
  position: sticky;
  top: 0;
  z-index: ${({theme:e})=>e.zIndex.max};
  background: ${({theme:e})=>e.colors.grayscale.light5};
`,I=s.iK.div`
  margin-bottom: 16px;

  .catalog-type-select {
    margin: 0 0 20px;
  }

  .gsheet-title {
    font-size: ${({theme:e})=>1.1*e.typography.sizes.l}px;
    font-weight: bold;
    margin: ${({theme:e})=>10*e.gridUnit}px 0 16px;
  }

  .catalog-label {
    margin: 0 0 7px;
  }

  .catalog-name {
    display: flex;
    .catalog-name-input {
      width: 95%;
      margin-bottom: 0px;
    }
  }

  .catalog-name-url {
    margin: 4px 0;
    width: 95%;
  }

  .catalog-delete {
    align-self: center;
    background: ${({theme:e})=>e.colors.grayscale.light4};
    margin: 5px 5px 8px 5px;
  }

  .catalog-add-btn {
    width: 95%;
  }
`;var F,P;(F="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.default:void 0)&&(F.register(102,"CTAS_CVAS_SCHEMA_FORM_HEIGHT","/Users/chenming/superset/superset-frontend/src/views/CRUD/data/database/DatabaseModal/styles.ts"),F.register(255,"EXPOSE_IN_SQLLAB_FORM_HEIGHT","/Users/chenming/superset/superset-frontend/src/views/CRUD/data/database/DatabaseModal/styles.ts"),F.register(357,"EXPOSE_ALL_FORM_HEIGHT","/Users/chenming/superset/superset-frontend/src/views/CRUD/data/database/DatabaseModal/styles.ts"),F.register(12,"anticonHeight","/Users/chenming/superset/superset-frontend/src/views/CRUD/data/database/DatabaseModal/styles.ts"),F.register(i,"no_margin_bottom","/Users/chenming/superset/superset-frontend/src/views/CRUD/data/database/DatabaseModal/styles.ts"),F.register(d,"labelMarginBotton","/Users/chenming/superset/superset-frontend/src/views/CRUD/data/database/DatabaseModal/styles.ts"),F.register((e=>r.iv`
  margin-bottom: ${4*e.gridUnit}px;
`),"marginBottom","/Users/chenming/superset/superset-frontend/src/views/CRUD/data/database/DatabaseModal/styles.ts"),F.register(c,"StyledFormHeader","/Users/chenming/superset/superset-frontend/src/views/CRUD/data/database/DatabaseModal/styles.ts"),F.register(u,"antdCollapseStyles","/Users/chenming/superset/superset-frontend/src/views/CRUD/data/database/DatabaseModal/styles.ts"),F.register(p,"antDTabsStyles","/Users/chenming/superset/superset-frontend/src/views/CRUD/data/database/DatabaseModal/styles.ts"),F.register(m,"antDModalNoPaddingStyles","/Users/chenming/superset/superset-frontend/src/views/CRUD/data/database/DatabaseModal/styles.ts"),F.register(h,"infoTooltip","/Users/chenming/superset/superset-frontend/src/views/CRUD/data/database/DatabaseModal/styles.ts"),F.register(g,"toggleStyle","/Users/chenming/superset/superset-frontend/src/views/CRUD/data/database/DatabaseModal/styles.ts"),F.register(b,"formScrollableStyles","/Users/chenming/superset/superset-frontend/src/views/CRUD/data/database/DatabaseModal/styles.ts"),F.register(f,"antDModalStyles","/Users/chenming/superset/superset-frontend/src/views/CRUD/data/database/DatabaseModal/styles.ts"),F.register(v,"antDAlertStyles","/Users/chenming/superset/superset-frontend/src/views/CRUD/data/database/DatabaseModal/styles.ts"),F.register(y,"StyledAlertMargin","/Users/chenming/superset/superset-frontend/src/views/CRUD/data/database/DatabaseModal/styles.ts"),F.register(x,"antDErrorAlertStyles","/Users/chenming/superset/superset-frontend/src/views/CRUD/data/database/DatabaseModal/styles.ts"),F.register(Z,"formHelperStyles","/Users/chenming/superset/superset-frontend/src/views/CRUD/data/database/DatabaseModal/styles.ts"),F.register(C,"wideButton","/Users/chenming/superset/superset-frontend/src/views/CRUD/data/database/DatabaseModal/styles.ts"),F.register(_,"formStyles","/Users/chenming/superset/superset-frontend/src/views/CRUD/data/database/DatabaseModal/styles.ts"),F.register(w,"validatedFormStyles","/Users/chenming/superset/superset-frontend/src/views/CRUD/data/database/DatabaseModal/styles.ts"),F.register(U,"StyledInputContainer","/Users/chenming/superset/superset-frontend/src/views/CRUD/data/database/DatabaseModal/styles.ts"),F.register(D,"StyledJsonEditor","/Users/chenming/superset/superset-frontend/src/views/CRUD/data/database/DatabaseModal/styles.ts"),F.register(L,"StyledExpandableForm","/Users/chenming/superset/superset-frontend/src/views/CRUD/data/database/DatabaseModal/styles.ts"),F.register(S,"StyledAlignment","/Users/chenming/superset/superset-frontend/src/views/CRUD/data/database/DatabaseModal/styles.ts"),F.register(M,"buttonLinkStyles","/Users/chenming/superset/superset-frontend/src/views/CRUD/data/database/DatabaseModal/styles.ts"),F.register(E,"alchemyButtonLinkStyles","/Users/chenming/superset/superset-frontend/src/views/CRUD/data/database/DatabaseModal/styles.ts"),F.register(N,"TabHeader","/Users/chenming/superset/superset-frontend/src/views/CRUD/data/database/DatabaseModal/styles.ts"),F.register($,"CreateHeaderTitle","/Users/chenming/superset/superset-frontend/src/views/CRUD/data/database/DatabaseModal/styles.ts"),F.register(k,"CreateHeaderSubtitle","/Users/chenming/superset/superset-frontend/src/views/CRUD/data/database/DatabaseModal/styles.ts"),F.register(H,"EditHeaderTitle","/Users/chenming/superset/superset-frontend/src/views/CRUD/data/database/DatabaseModal/styles.ts"),F.register(R,"EditHeaderSubtitle","/Users/chenming/superset/superset-frontend/src/views/CRUD/data/database/DatabaseModal/styles.ts"),F.register(T,"CredentialInfoForm","/Users/chenming/superset/superset-frontend/src/views/CRUD/data/database/DatabaseModal/styles.ts"),F.register(G,"SelectDatabaseStyles","/Users/chenming/superset/superset-frontend/src/views/CRUD/data/database/DatabaseModal/styles.ts"),F.register(A,"StyledFooterButton","/Users/chenming/superset/superset-frontend/src/views/CRUD/data/database/DatabaseModal/styles.ts"),F.register(O,"StyledStickyHeader","/Users/chenming/superset/superset-frontend/src/views/CRUD/data/database/DatabaseModal/styles.ts"),F.register(I,"StyledCatalogTable","/Users/chenming/superset/superset-frontend/src/views/CRUD/data/database/DatabaseModal/styles.ts")),(P="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.leaveModule:void 0)&&P(e)},301483:(e,t,a)=>{a.d(t,{c:()=>l});var n,r,s,o=a(137703);function l(){return(0,o.v9)((e=>{var t;return null==e||null==(t=e.common)?void 0:t.conf}))}e=a.hmd(e),(n="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.enterModule:void 0)&&n(e),("undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.default.signature:function(e){return e})(l,"useSelector{}",(()=>[o.v9])),(r="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.default:void 0)&&r.register(l,"useCommonConf","/Users/chenming/superset/superset-frontend/src/views/CRUD/data/database/state.ts"),(s="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.leaveModule:void 0)&&s(e)},163727:(e,t,a)=>{var n,r,s,o;a.d(t,{j:()=>r}),e=a.hmd(e),(n="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.enterModule:void 0)&&n(e),"undefined"!=typeof reactHotLoaderGlobal&&reactHotLoaderGlobal.default.signature,function(e){e.SQLALCHEMY_URI="sqlalchemy_form",e.DYNAMIC_FORM="dynamic_form"}(r||(r={})),(s="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.default:void 0)&&s.register(r,"CONFIGURATION_METHOD","/Users/chenming/superset/superset-frontend/src/views/CRUD/data/database/types.ts"),(o="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.leaveModule:void 0)&&o(e)},188104:(e,t,a)=>{a.d(t,{Z:()=>m});var n,r=a(205872),s=a.n(r),o=(a(667294),a(683862)),l=a(751995),i=a(87693),d=a(211965);e=a.hmd(e),(n="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.enterModule:void 0)&&n(e),"undefined"!=typeof reactHotLoaderGlobal&&reactHotLoaderGlobal.default.signature;const{SubMenu:c}=o.$,u=l.iK.div`
  display: flex;
  align-items: center;

  & i {
    margin-right: ${({theme:e})=>2*e.gridUnit}px;
  }

  & a {
    display: block;
    width: 150px;
    word-wrap: break-word;
    text-decoration: none;
  }
`,p=l.iK.i`
  margin-top: 2px;
`;function m(e){const{locale:t,languages:a,...n}=e;return(0,d.tZ)(c,s()({"aria-label":"Languages",title:(0,d.tZ)("div",{className:"f16"},(0,d.tZ)(p,{className:`flag ${a[t].flag}`})),icon:(0,d.tZ)(i.Z.TriangleDown,null)},n),Object.keys(a).map((e=>(0,d.tZ)(o.$.Item,{key:e,style:{whiteSpace:"normal",height:"auto"}},(0,d.tZ)(u,{className:"f16"},(0,d.tZ)("i",{className:`flag ${a[e].flag}`}),(0,d.tZ)("a",{href:a[e].url},a[e].name))))))}var h,g;(h="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.default:void 0)&&(h.register(c,"SubMenu","/Users/chenming/superset/superset-frontend/src/views/components/LanguagePicker.tsx"),h.register(u,"StyledLabel","/Users/chenming/superset/superset-frontend/src/views/components/LanguagePicker.tsx"),h.register(p,"StyledFlag","/Users/chenming/superset/superset-frontend/src/views/components/LanguagePicker.tsx"),h.register(m,"LanguagePicker","/Users/chenming/superset/superset-frontend/src/views/components/LanguagePicker.tsx")),(g="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.leaveModule:void 0)&&g(e)},456967:(e,t,a)=>{a.d(t,{Z:()=>D});var n,r=a(205872),s=a.n(r),o=a(23279),l=a.n(o),i=a(667294),d=a(751995),c=a(211965),u=a(23525),p=a(104715),m=a(683862),h=a(358593),g=a(473727),b=a(87693),f=a(229147),v=a(427600),y=a(199939);e=a.hmd(e),(n="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.enterModule:void 0)&&n(e);var x="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.default.signature:function(e){return e};const Z=d.iK.header`
  background-color: white;
  margin-bottom: 2px;
  &:nth-last-of-type(2) nav {
    margin-bottom: 2px;
  }

  .caret {
    display: none;
  }
  .navbar-brand {
    display: flex;
    flex-direction: column;
    justify-content: center;
  }
  .navbar-brand-text {
    border-left: 1px solid ${({theme:e})=>e.colors.grayscale.light2};
    border-right: 1px solid ${({theme:e})=>e.colors.grayscale.light2};
    height: 100%;
    color: ${({theme:e})=>e.colors.grayscale.dark1};
    padding-left: ${({theme:e})=>4*e.gridUnit}px;
    padding-right: ${({theme:e})=>4*e.gridUnit}px;
    margin-right: ${({theme:e})=>6*e.gridUnit}px;
    font-size: ${({theme:e})=>4*e.gridUnit}px;
    float: left;
    display: flex;
    flex-direction: column;
    justify-content: center;

    span {
      max-width: ${({theme:e})=>58*e.gridUnit}px;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
    @media (max-width: 1127px) {
      display: none;
    }
  }
  .main-nav .ant-menu-submenu-title > svg {
    top: ${({theme:e})=>5.25*e.gridUnit}px;
  }
  @media (max-width: 767px) {
    .navbar-brand {
      float: none;
    }
  }
  .ant-menu-horizontal .ant-menu-item {
    height: 100%;
    line-height: inherit;
  }
  .ant-menu > .ant-menu-item > a {
    padding: ${({theme:e})=>4*e.gridUnit}px;
  }
  @media (max-width: 767px) {
    .ant-menu-item {
      padding: 0 ${({theme:e})=>6*e.gridUnit}px 0
        ${({theme:e})=>3*e.gridUnit}px !important;
    }
    .ant-menu > .ant-menu-item > a {
      padding: 0px;
    }
    .main-nav .ant-menu-submenu-title > svg:nth-child(1) {
      display: none;
    }
    .ant-menu-item-active > a {
      &:hover {
        color: ${({theme:e})=>e.colors.primary.base} !important;
        background-color: transparent !important;
      }
    }
  }

  .ant-menu-item a {
    &:hover {
      color: ${({theme:e})=>e.colors.grayscale.dark1};
      background-color: ${({theme:e})=>e.colors.primary.light5};
      border-bottom: none;
      margin: 0;
      &:after {
        opacity: 1;
        width: 100%;
      }
    }
  }
`,C=e=>c.iv`
  .ant-menu-submenu.ant-menu-submenu-popup.ant-menu.ant-menu-light.ant-menu-submenu-placement-bottomLeft {
    border-radius: 0px;
  }
  .ant-menu-submenu.ant-menu-submenu-popup.ant-menu.ant-menu-light {
    border-radius: 0px;
  }
  .ant-menu-vertical > .ant-menu-submenu.data-menu > .ant-menu-submenu-title {
    height: 28px;
    i {
      padding-right: ${2*e.gridUnit}px;
      margin-left: ${1.75*e.gridUnit}px;
    }
  }
`,{SubMenu:_}=m.$,{useBreakpoint:w}=p.rj;function U({data:{menu:e,brand:t,navbar_right:a,settings:n},isFrontendRoute:r=(()=>!1)}){const[s,o]=(0,i.useState)("horizontal"),x=w(),U=(0,f.fG)(),D=(0,d.Fg)();return(0,i.useEffect)((()=>{function e(){window.innerWidth<=767?o("inline"):o("horizontal")}e();const t=l()((()=>e()),10);return window.addEventListener("resize",t),()=>window.removeEventListener("resize",t)}),[]),(0,u.e)(v.KD.standalone)||U.hideNav?(0,c.tZ)(i.Fragment,null):(0,c.tZ)(Z,{className:"top",id:"main-menu",role:"navigation"},(0,c.tZ)(c.xB,{styles:C(D)}),(0,c.tZ)(p.X2,null,(0,c.tZ)(p.JX,{md:16,xs:24},(0,c.tZ)(h.u,{id:"brand-tooltip",placement:"bottomLeft",title:t.tooltip,arrowPointAtCenter:!0},(0,c.tZ)("a",{className:"navbar-brand",href:t.path},(0,c.tZ)("img",{width:t.width,src:t.icon,alt:t.alt}))),t.text&&(0,c.tZ)("div",{className:"navbar-brand-text"},(0,c.tZ)("span",null,t.text)),(0,c.tZ)(m.$,{mode:s,"data-test":"navbar-top",className:"main-nav"},e.map((e=>{var t;return(({label:e,childs:t,url:a,index:n,isFrontendRoute:r})=>a&&r?(0,c.tZ)(m.$.Item,{key:e,role:"presentation"},(0,c.tZ)(g.rU,{role:"button",to:a},e)):a?(0,c.tZ)(m.$.Item,{key:e},(0,c.tZ)("a",{href:a},e)):(0,c.tZ)(_,{key:n,title:e,icon:"inline"===s?(0,c.tZ)(i.Fragment,null):(0,c.tZ)(b.Z.TriangleDown,null)},null==t?void 0:t.map(((t,a)=>"string"==typeof t&&"-"===t&&"Data"!==e?(0,c.tZ)(m.$.Divider,{key:`$${a}`}):"string"!=typeof t?(0,c.tZ)(m.$.Item,{key:`${t.label}`},t.isFrontendRoute?(0,c.tZ)(g.rU,{to:t.url||""},t.label):(0,c.tZ)("a",{href:t.url},t.label)):null))))({...e,isFrontendRoute:r(e.url),childs:null==(t=e.childs)?void 0:t.map((e=>"string"==typeof e?e:{...e,isFrontendRoute:r(e.url)}))})})))),(0,c.tZ)(p.JX,{md:8,xs:24},(0,c.tZ)(y.Z,{align:x.md?"flex-end":"flex-start",settings:n,navbarRight:a,isFrontendRoute:r}))))}function D({data:e,...t}){const a={...e},n={Security:!0,Manage:!0},r=[],o=[];return a.menu.forEach((e=>{if(!e)return;const t=[],a={...e};e.childs&&(e.childs.forEach((e=>{("string"==typeof e||e.label)&&t.push(e)})),a.childs=t),n.hasOwnProperty(e.name)?o.push(a):r.push(a)})),a.menu=r,a.settings=o,(0,c.tZ)(U,s()({data:a},t))}var L,S;x(U,"useState{[showMenu, setMenu]('horizontal')}\nuseBreakpoint{screens}\nuseUiConfig{uiConig}\nuseTheme{theme}\nuseEffect{}",(()=>[w,f.fG,d.Fg])),(L="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.default:void 0)&&(L.register(Z,"StyledHeader","/Users/chenming/superset/superset-frontend/src/views/components/Menu.tsx"),L.register(C,"globalStyles","/Users/chenming/superset/superset-frontend/src/views/components/Menu.tsx"),L.register(_,"SubMenu","/Users/chenming/superset/superset-frontend/src/views/components/Menu.tsx"),L.register(w,"useBreakpoint","/Users/chenming/superset/superset-frontend/src/views/components/Menu.tsx"),L.register(U,"Menu","/Users/chenming/superset/superset-frontend/src/views/components/Menu.tsx"),L.register(D,"MenuWrapper","/Users/chenming/superset/superset-frontend/src/views/components/Menu.tsx")),(S="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.leaveModule:void 0)&&S(e)},199939:(e,t,a)=>{a.d(t,{Z:()=>U});var n,r=a(667294),s=a(683862),o=a(211965),l=a(751995),i=a(455867),d=a(473727),c=a(87693),u=a(870695),p=a(137703),m=a(188104),h=a(603506),g=a(440768),b=a(927345);e=a.hmd(e),(n="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.enterModule:void 0)&&n(e);var f="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.default.signature:function(e){return e};const v=e=>o.iv`
  padding: ${1.5*e.gridUnit}px ${4*e.gridUnit}px
    ${4*e.gridUnit}px ${7*e.gridUnit}px;
  color: ${e.colors.grayscale.base};
  font-size: ${e.typography.sizes.xs}px;
  white-space: nowrap;
`,y=l.iK.div`
  color: ${({theme:e})=>e.colors.primary.dark1};
`,x=l.iK.div`
  display: flex;
  flex-direction: row;
  justify-content: ${({align:e})=>e};
  align-items: center;
  margin-right: ${({theme:e})=>e.gridUnit}px;
  .ant-menu-submenu-title > svg {
    top: ${({theme:e})=>5.25*e.gridUnit}px;
  }
`,Z=l.iK.a`
  padding-right: ${({theme:e})=>e.gridUnit}px;
  padding-left: ${({theme:e})=>e.gridUnit}px;
`,{SubMenu:C}=s.$,_=({align:e,settings:t,navbarRight:a,isFrontendRoute:n})=>{const{roles:l}=(0,p.v9)((e=>e.user)),{CSV_EXTENSIONS:f,COLUMNAR_EXTENSIONS:_,EXCEL_EXTENSIONS:w,ALLOWED_EXTENSIONS:U,HAS_GSHEETS_INSTALLED:D}=(0,p.v9)((e=>e.common.conf)),[L,S]=(0,r.useState)(!1),[M,E]=(0,r.useState)(""),N=(0,u.Z)("can_sqllab","Superset",l),$=(0,u.Z)("can_write","Dashboard",l),k=(0,u.Z)("can_write","Chart",l),H=(0,u.Z)("can_write","Database",l),R=(0,u.Z)("can_this_form_get","CsvToDatabaseView",l),T=(0,u.Z)("can_this_form_get","ColumnarToDatabaseView",l),G=(0,u.Z)("can_this_form_get","ExcelToDatabaseView",l),A=R||T||G,O=N||k||$,I=[{label:(0,i.t)("Data"),icon:"fa-database",childs:[{label:(0,i.t)("Connect database"),name:b.Z.DB_CONNECTION,perm:H},{label:(0,i.t)("Connect Google Sheet"),name:b.Z.GOOGLE_SHEETS,perm:H&&D},{label:(0,i.t)("Upload CSV to database"),name:"Upload a CSV",url:"/csvtodatabaseview/form",perm:f&&R},{label:(0,i.t)("Upload columnar file to database"),name:"Upload a Columnar file",url:"/columnartodatabaseview/form",perm:_&&T},{label:(0,i.t)("Upload Excel file to database"),name:"Upload Excel",url:"/exceltodatabaseview/form",perm:w&&G}]},{label:(0,i.t)("SQL query"),url:"/superset/sqllab?new=true",icon:"fa-fw fa-search",perm:"can_sqllab",view:"Superset"},{label:(0,i.t)("Chart"),url:"/chart/add",icon:"fa-fw fa-bar-chart",perm:"can_write",view:"Chart"},{label:(0,i.t)("Dashboard"),url:"/dashboard/new",icon:"fa-fw fa-dashboard",perm:"can_write",view:"Dashboard"}],F=e=>(0,o.tZ)(r.Fragment,null,(0,o.tZ)("i",{"data-test":`menu-item-${e.label}`,className:`fa ${e.icon}`}),e.label);return(0,o.tZ)(x,{align:e},(0,o.tZ)(h.Z,{onHide:()=>{E(""),S(!1)},show:L,dbEngine:M}),(0,o.tZ)(s.$,{selectable:!1,mode:"horizontal",onClick:e=>{e.key===b.Z.DB_CONNECTION?S(!0):e.key===b.Z.GOOGLE_SHEETS&&(S(!0),E("Google Sheets"))}},!a.user_is_anonymous&&O&&(0,o.tZ)(C,{"data-test":"new-dropdown",title:(0,o.tZ)(y,{"data-test":"new-dropdown-icon",className:"fa fa-plus"}),icon:(0,o.tZ)(c.Z.TriangleDown,null)},I.map((e=>e.childs?H||A?(0,o.tZ)(C,{key:"sub2",className:"data-menu",title:F(e)},e.childs.map(((e,t)=>"string"!=typeof e&&e.name&&(0,g.jE)(e.perm,U)?(0,o.tZ)(r.Fragment,null,2===t&&(0,o.tZ)(s.$.Divider,null),(0,o.tZ)(s.$.Item,{key:e.name},e.url?(0,o.tZ)("a",{href:e.url}," ",e.label," "):e.label)):null))):null:(0,u.Z)(e.perm,e.view,l)&&(0,o.tZ)(s.$.Item,{key:e.label},(0,o.tZ)("a",{href:e.url},(0,o.tZ)("i",{"data-test":`menu-item-${e.label}`,className:`fa ${e.icon}`})," ",e.label))))),(0,o.tZ)(C,{title:(0,i.t)("Settings"),icon:(0,o.tZ)(c.Z.TriangleDown,{iconSize:"xl"})},t.map(((e,a)=>{var r;return[(0,o.tZ)(s.$.ItemGroup,{key:`${e.label}`,title:e.label},null==(r=e.childs)?void 0:r.map((e=>"string"!=typeof e?(0,o.tZ)(s.$.Item,{key:`${e.label}`},n(e.url)?(0,o.tZ)(d.rU,{to:e.url||""},e.label):(0,o.tZ)("a",{href:e.url},e.label)):null))),a<t.length-1&&(0,o.tZ)(s.$.Divider,null)]})),!a.user_is_anonymous&&[(0,o.tZ)(s.$.Divider,{key:"user-divider"}),(0,o.tZ)(s.$.ItemGroup,{key:"user-section",title:(0,i.t)("User")},a.user_profile_url&&(0,o.tZ)(s.$.Item,{key:"profile"},(0,o.tZ)("a",{href:a.user_profile_url},(0,i.t)("Profile"))),a.user_info_url&&(0,o.tZ)(s.$.Item,{key:"info"},(0,o.tZ)("a",{href:a.user_info_url},(0,i.t)("Info"))),(0,o.tZ)(s.$.Item,{key:"logout"},(0,o.tZ)("a",{href:a.user_logout_url},(0,i.t)("Logout"))))],(a.version_string||a.version_sha)&&[(0,o.tZ)(s.$.Divider,{key:"version-info-divider"}),(0,o.tZ)(s.$.ItemGroup,{key:"about-section",title:(0,i.t)("About")},(0,o.tZ)("div",{className:"about-section"},a.show_watermark&&(0,o.tZ)("div",{css:v},(0,i.t)("Powered by Apache Superset")),a.version_string&&(0,o.tZ)("div",{css:v},"Version: ",a.version_string),a.version_sha&&(0,o.tZ)("div",{css:v},"SHA: ",a.version_sha),a.build_number&&(0,o.tZ)("div",{css:v},"Build: ",a.build_number)))]),a.show_language_picker&&(0,o.tZ)(m.Z,{locale:a.locale,languages:a.languages})),a.documentation_url&&(0,o.tZ)(Z,{href:a.documentation_url,target:"_blank",rel:"noreferrer",title:(0,i.t)("Documentation")},(0,o.tZ)("i",{className:"fa fa-question"})," "),a.bug_report_url&&(0,o.tZ)(Z,{href:a.bug_report_url,target:"_blank",rel:"noreferrer",title:(0,i.t)("Report a bug")},(0,o.tZ)("i",{className:"fa fa-bug"})),a.user_is_anonymous&&(0,o.tZ)(Z,{href:a.user_login_url},(0,o.tZ)("i",{className:"fa fa-fw fa-sign-in"}),(0,i.t)("Login")))};f(_,"useSelector{{ roles }}\nuseSelector{{ CSV_EXTENSIONS, COLUMNAR_EXTENSIONS, EXCEL_EXTENSIONS, ALLOWED_EXTENSIONS, HAS_GSHEETS_INSTALLED, }}\nuseState{[showModal, setShowModal](false)}\nuseState{[engine, setEngine]('')}",(()=>[p.v9,p.v9]));const w=_,U=w;var D,L;(D="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.default:void 0)&&(D.register(v,"versionInfoStyles","/Users/chenming/superset/superset-frontend/src/views/components/MenuRight.tsx"),D.register(y,"StyledI","/Users/chenming/superset/superset-frontend/src/views/components/MenuRight.tsx"),D.register(x,"StyledDiv","/Users/chenming/superset/superset-frontend/src/views/components/MenuRight.tsx"),D.register(Z,"StyledAnchor","/Users/chenming/superset/superset-frontend/src/views/components/MenuRight.tsx"),D.register(C,"SubMenu","/Users/chenming/superset/superset-frontend/src/views/components/MenuRight.tsx"),D.register(_,"RightMenu","/Users/chenming/superset/superset-frontend/src/views/components/MenuRight.tsx"),D.register(w,"default","/Users/chenming/superset/superset-frontend/src/views/components/MenuRight.tsx")),(L="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.leaveModule:void 0)&&L(e)},927345:(e,t,a)=>{var n,r,s,o;a.d(t,{Z:()=>r}),e=a.hmd(e),(n="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.enterModule:void 0)&&n(e),"undefined"!=typeof reactHotLoaderGlobal&&reactHotLoaderGlobal.default.signature,function(e){e.GOOGLE_SHEETS="gsheets",e.DB_CONNECTION="dbconnection"}(r||(r={})),(s="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.default:void 0)&&s.register(r,"GlobalMenuDataOptions","/Users/chenming/superset/superset-frontend/src/views/components/types.ts"),(o="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.leaveModule:void 0)&&o(e)}}]);
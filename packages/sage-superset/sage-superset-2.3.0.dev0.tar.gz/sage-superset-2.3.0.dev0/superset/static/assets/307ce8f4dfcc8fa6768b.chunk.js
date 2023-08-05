"use strict";(globalThis.webpackChunksuperset=globalThis.webpackChunksuperset||[]).push([[9502],{817486:(e,t,r)=>{r.d(t,{B:()=>p});var a,o=r(205872),n=r.n(o),s=(r(667294),r(785631)),l=r(455867),i=r(751995),d=r(361247),c=r(211965);e=r.hmd(e),(a="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.enterModule:void 0)&&a(e),"undefined"!=typeof reactHotLoaderGlobal&&reactHotLoaderGlobal.default.signature;const u={everyText:(0,l.t)("every"),emptyMonths:(0,l.t)("every month"),emptyMonthDays:(0,l.t)("every day of the month"),emptyMonthDaysShort:(0,l.t)("day of the month"),emptyWeekDays:(0,l.t)("every day of the week"),emptyWeekDaysShort:(0,l.t)("day of the week"),emptyHours:(0,l.t)("every hour"),emptyMinutes:(0,l.t)("every minute"),emptyMinutesForHourPeriod:(0,l.t)("every"),yearOption:(0,l.t)("year"),monthOption:(0,l.t)("month"),weekOption:(0,l.t)("week"),dayOption:(0,l.t)("day"),hourOption:(0,l.t)("hour"),minuteOption:(0,l.t)("minute"),rebootOption:(0,l.t)("reboot"),prefixPeriod:(0,l.t)("Every"),prefixMonths:(0,l.t)("in"),prefixMonthDays:(0,l.t)("on"),prefixWeekDays:(0,l.t)("on"),prefixWeekDaysForMonthAndYearPeriod:(0,l.t)("and"),prefixHours:(0,l.t)("at"),prefixMinutes:(0,l.t)(":"),prefixMinutesForHourPeriod:(0,l.t)("at"),suffixMinutesForHourPeriod:(0,l.t)("minute(s)"),errorInvalidCron:(0,l.t)("Invalid cron expression"),clearButtonText:(0,l.t)("Clear"),weekDays:[(0,l.t)("Sunday"),(0,l.t)("Monday"),(0,l.t)("Tuesday"),(0,l.t)("Wednesday"),(0,l.t)("Thursday"),(0,l.t)("Friday"),(0,l.t)("Saturday")],months:[(0,l.t)("January"),(0,l.t)("February"),(0,l.t)("March"),(0,l.t)("April"),(0,l.t)("May"),(0,l.t)("June"),(0,l.t)("July"),(0,l.t)("August"),(0,l.t)("September"),(0,l.t)("October"),(0,l.t)("November"),(0,l.t)("December")],altWeekDays:[(0,l.t)("SUN"),(0,l.t)("MON"),(0,l.t)("TUE"),(0,l.t)("WED"),(0,l.t)("THU"),(0,l.t)("FRI"),(0,l.t)("SAT")],altMonths:[(0,l.t)("JAN"),(0,l.t)("FEB"),(0,l.t)("MAR"),(0,l.t)("APR"),(0,l.t)("MAY"),(0,l.t)("JUN"),(0,l.t)("JUL"),(0,l.t)("AUG"),(0,l.t)("SEP"),(0,l.t)("OCT"),(0,l.t)("NOV"),(0,l.t)("DEC")]},p=(0,i.iK)((e=>(0,c.tZ)(s.ZP,{getPopupContainer:e=>e.parentElement},(0,c.tZ)(d.Z,n()({locale:u},e)))))`
  .react-js-cron-select:not(.react-js-cron-custom-select) > div:first-of-type,
  .react-js-cron-custom-select {
    border-radius: ${({theme:e})=>e.gridUnit}px;
    background-color: ${({theme:e})=>e.colors.grayscale.light4} !important;
  }
  .react-js-cron-custom-select > div:first-of-type {
    border-radius: ${({theme:e})=>e.gridUnit}px;
  }
`;var m,h;(m="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.default:void 0)&&(m.register(u,"LOCALE","/Users/chenming/superset/superset-frontend/src/components/CronPicker/CronPicker.tsx"),m.register(p,"CronPicker","/Users/chenming/superset/superset-frontend/src/components/CronPicker/CronPicker.tsx")),(h="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.leaveModule:void 0)&&h(e)},215428:(e,t,r)=>{r.d(t,{CronPicker:()=>a.B});var a=r(817486);"undefined"!=typeof reactHotLoaderGlobal&&reactHotLoaderGlobal.default.signature},128181:(e,t,r)=>{r.d(t,{Z:()=>f});var a,o=r(667294),n=r(730381),s=r.n(n),l=r(751995),i=r(455867),d=r(87693),c=r(211965);e=r.hmd(e),(a="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.enterModule:void 0)&&a(e);var u="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.default.signature:function(e){return e};s().updateLocale("en",{calendar:{lastDay:"[Yesterday at] LTS",sameDay:"[Today at] LTS",nextDay:"[Tomorrow at] LTS",lastWeek:"[last] dddd [at] LTS",nextWeek:"dddd [at] LTS",sameElse:"L"}});const p=l.iK.span`
  color: ${({theme:e})=>e.colors.grayscale.base};
`,m=(0,l.iK)(d.Z.Refresh)`
  color: ${({theme:e})=>e.colors.primary.base};
  width: auto;
  height: ${({theme:e})=>5*e.gridUnit}px;
  position: relative;
  top: ${({theme:e})=>e.gridUnit}px;
  left: ${({theme:e})=>e.gridUnit}px;
  cursor: pointer;
`,h=({updatedAt:e,update:t})=>{const[r,a]=(0,o.useState)(s()(e));return(0,o.useEffect)((()=>{a((()=>s()(e)));const t=setInterval((()=>{a((()=>s()(e)))}),6e4);return()=>clearInterval(t)}),[e]),(0,c.tZ)(p,null,(0,i.t)("Last Updated %s",r.isValid()?r.calendar():"--"),t&&(0,c.tZ)(m,{onClick:t}))};u(h,"useState{[timeSince, setTimeSince](moment(updatedAt))}\nuseEffect{}");const g=h,f=g;var v,b;(v="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.default:void 0)&&(v.register(6e4,"REFRESH_INTERVAL","/Users/chenming/superset/superset-frontend/src/components/LastUpdated/index.tsx"),v.register(p,"TextStyles","/Users/chenming/superset/superset-frontend/src/components/LastUpdated/index.tsx"),v.register(m,"Refresh","/Users/chenming/superset/superset-frontend/src/components/LastUpdated/index.tsx"),v.register(h,"LastUpdated","/Users/chenming/superset/superset-frontend/src/components/LastUpdated/index.tsx"),v.register(g,"default","/Users/chenming/superset/superset-frontend/src/components/LastUpdated/index.tsx")),(b="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.leaveModule:void 0)&&b(e)},129848:(e,t,r)=>{r.d(t,{Z:()=>c}),r(667294);var a,o=r(751995),n=r(358593),s=r(87693),l=r(211965);e=r.hmd(e),(a="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.enterModule:void 0)&&a(e),"undefined"!=typeof reactHotLoaderGlobal&&reactHotLoaderGlobal.default.signature;const i=o.iK.span`
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
`,d=o.iK.span`
  color: ${({theme:e})=>e.colors.grayscale.base};
`;function c({actions:e}){return(0,l.tZ)(i,{className:"actions"},e.map(((e,t)=>{const r=s.Z[e.icon];return e.tooltip?(0,l.tZ)(n.u,{id:`${e.label}-tooltip`,title:e.tooltip,placement:e.placement,key:t},(0,l.tZ)(d,{role:"button",tabIndex:0,className:"action-button","data-test":e.label,onClick:e.onClick},(0,l.tZ)(r,null))):(0,l.tZ)(d,{role:"button",tabIndex:0,className:"action-button",onClick:e.onClick,"data-test":e.label,key:t},(0,l.tZ)(r,null))})))}var u,p;(u="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.default:void 0)&&(u.register(i,"StyledActions","/Users/chenming/superset/superset-frontend/src/components/ListView/ActionsBar.tsx"),u.register(d,"ActionWrapper","/Users/chenming/superset/superset-frontend/src/components/ListView/ActionsBar.tsx"),u.register(c,"ActionsBar","/Users/chenming/superset/superset-frontend/src/components/ListView/ActionsBar.tsx")),(p="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.leaveModule:void 0)&&p(e)},112441:(e,t,r)=>{r.d(t,{r:()=>i}),r(667294);var a,o=r(751995),n=r(840987),s=r(211965);e=r.hmd(e),(a="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.enterModule:void 0)&&a(e),"undefined"!=typeof reactHotLoaderGlobal&&reactHotLoaderGlobal.default.signature;const l=(0,o.iK)(n.Z)`
  .ant-switch-checked {
    background-color: ${({theme:e})=>e.colors.primary.base};
  }
`,i=e=>(0,s.tZ)(l,e);var d,c;(d="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.default:void 0)&&(d.register(l,"StyledSwitch","/Users/chenming/superset/superset-frontend/src/components/Switch/index.tsx"),d.register(i,"Switch","/Users/chenming/superset/superset-frontend/src/components/Switch/index.tsx")),(c="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.leaveModule:void 0)&&c(e)},898978:(e,t,r)=>{r.d(t,{Z:()=>T});var a,o=r(211965),n=r(667294),s=r(480008),l=r.n(s),i=r(455867),d=r(104715);e=r.hmd(e),(a="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.enterModule:void 0)&&a(e);var c="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.default.signature:function(e){return e};const u={name:"GMT Standard Time",value:"Africa/Abidjan"},p="400px",m={"-300-240":["Eastern Standard Time","Eastern Daylight Time"],"-360-300":["Central Standard Time","Central Daylight Time"],"-420-360":["Mountain Standard Time","Mountain Daylight Time"],"-420-420":["Mountain Standard Time - Phoenix","Mountain Standard Time - Phoenix"],"-480-420":["Pacific Standard Time","Pacific Daylight Time"],"-540-480":["Alaska Standard Time","Alaska Daylight Time"],"-600-600":["Hawaii Standard Time","Hawaii Daylight Time"],60120:["Central European Time","Central European Daylight Time"],"00":[u.name,u.name],"060":["GMT Standard Time - London","British Summer Time"]},h=l()(),g=l()([2021,1]),f=l()([2021,7]),v=e=>g.tz(e).utcOffset().toString()+f.tz(e).utcOffset().toString(),b=e=>{var t,r;const a=v(e);return(h.tz(e).isDST()?null==(t=m[a])?void 0:t[1]:null==(r=m[a])?void 0:r[0])||e},y=l().tz.countries().map((e=>l().tz.zonesForCountry(e,!0))).flat(),Z=[];y.forEach((e=>{Z.find((t=>v(t.name)===v(e.name)))||Z.push(e)}));const x=Z.map((e=>({label:`GMT ${l().tz(h,e.name).format("Z")} (${b(e.name)})`,value:e.name,offsets:v(e.name),timezoneName:e.name}))),S=(e,t)=>l().tz(h,e.timezoneName).utcOffset()-l().tz(h,t.timezoneName).utcOffset();x.sort(S);const C=e=>{var t;return(null==(t=x.find((t=>t.offsets===v(e))))?void 0:t.value)||u.value},L=({onTimezoneChange:e,timezone:t})=>{const r=(0,n.useMemo)((()=>C(t||l().tz.guess())),[t]);return(0,n.useEffect)((()=>{t!==r&&e(r)}),[r,e,t]),(0,o.tZ)(d.Ph,{ariaLabel:(0,i.t)("Timezone selector"),css:(0,o.iv)({minWidth:p},"",""),onChange:t=>e(t),value:r,options:x,sortComparator:S})};c(L,"useMemo{validTimezone}\nuseEffect{}");const U=L,T=U;var N,_;(N="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.default:void 0)&&(N.register(u,"DEFAULT_TIMEZONE","/Users/chenming/superset/superset-frontend/src/components/TimezoneSelector/index.tsx"),N.register(p,"MIN_SELECT_WIDTH","/Users/chenming/superset/superset-frontend/src/components/TimezoneSelector/index.tsx"),N.register(m,"offsetsToName","/Users/chenming/superset/superset-frontend/src/components/TimezoneSelector/index.tsx"),N.register(h,"currentDate","/Users/chenming/superset/superset-frontend/src/components/TimezoneSelector/index.tsx"),N.register(g,"JANUARY","/Users/chenming/superset/superset-frontend/src/components/TimezoneSelector/index.tsx"),N.register(f,"JULY","/Users/chenming/superset/superset-frontend/src/components/TimezoneSelector/index.tsx"),N.register(v,"getOffsetKey","/Users/chenming/superset/superset-frontend/src/components/TimezoneSelector/index.tsx"),N.register(b,"getTimezoneName","/Users/chenming/superset/superset-frontend/src/components/TimezoneSelector/index.tsx"),N.register(y,"ALL_ZONES","/Users/chenming/superset/superset-frontend/src/components/TimezoneSelector/index.tsx"),N.register(Z,"TIMEZONES","/Users/chenming/superset/superset-frontend/src/components/TimezoneSelector/index.tsx"),N.register(x,"TIMEZONE_OPTIONS","/Users/chenming/superset/superset-frontend/src/components/TimezoneSelector/index.tsx"),N.register(S,"TIMEZONE_OPTIONS_SORT_COMPARATOR","/Users/chenming/superset/superset-frontend/src/components/TimezoneSelector/index.tsx"),N.register(C,"matchTimezoneToOptions","/Users/chenming/superset/superset-frontend/src/components/TimezoneSelector/index.tsx"),N.register(L,"TimezoneSelector","/Users/chenming/superset/superset-frontend/src/components/TimezoneSelector/index.tsx"),N.register(U,"default","/Users/chenming/superset/superset-frontend/src/components/TimezoneSelector/index.tsx")),(_="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.leaveModule:void 0)&&_(e)},962563:(e,t,r)=>{r.r(t),r.d(t,{default:()=>D});var a,o=r(667294),n=r(505977),s=r(455867),l=r(405568),i=r(751995),d=r(431069),c=r(730381),u=r.n(c),p=r(129848),m=r(835932),h=r(776698),g=r(358593),f=r(550859),v=r(620755),b=r(112441),y=r(427600),Z=r(414114),x=r(246714),S=r(528853),C=r(419259),L=r(217198),U=r(128181),T=r(34858),N=r(440768),_=r(590584),R=r(802849),A=r(211965);e=r.hmd(e),(a="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.enterModule:void 0)&&a(e);var w="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.default.signature:function(e){return e};const H={[R.Z.Success]:(0,s.t)("Success"),[R.Z.Working]:(0,s.t)("Working"),[R.Z.Error]:(0,s.t)("Error"),[R.Z.Noop]:(0,s.t)("Not triggered"),[R.Z.Grace]:(0,s.t)("On Grace")},G=(0,l.Z)({requestType:"rison",method:"DELETE",endpoint:"/api/v1/report/"}),E=i.iK.div`
  width: 100%;
  padding: 0 ${({theme:e})=>4*e.gridUnit}px
    ${({theme:e})=>3*e.gridUnit}px;
  background-color: ${({theme:e})=>e.colors.grayscale.light5};
`;function M({addDangerToast:e,isReportEnabled:t=!1,user:r,addSuccessToast:a}){const l=t?(0,s.t)("report"):(0,s.t)("alert"),i=t?(0,s.t)("reports"):(0,s.t)("alerts"),c=t?"Reports":"Alerts",Z=(0,o.useMemo)((()=>[{id:"type",operator:f.p.equals,value:t?"Report":"Alert"}]),[t]),{state:{loading:M,resourceCount:k,resourceCollection:D,bulkSelectEnabled:O,lastFetched:$},hasPerm:z,fetchData:I,refreshData:P,toggleBulkSelect:j}=(0,T.Yi)("report",(0,s.t)("reports"),e,!0,void 0,Z),{updateResource:F}=(0,T.LE)("report",(0,s.t)("reports"),e),[q,B]=(0,o.useState)(!1),[V,W]=(0,o.useState)(null),[K,Y]=(0,o.useState)(null);function J(e){W(e),B(!0)}const X=z("can_write"),Q=z("can_write"),ee=z("can_write");(0,o.useEffect)((()=>{O&&Q&&j()}),[t]);const te=[{id:"name",desc:!0}],re=(0,o.useMemo)((()=>[{Cell:({row:{original:{last_state:e}}})=>(0,A.tZ)(x.Z,{state:e,isReportEnabled:t}),accessor:"last_state",size:"xs",disableSortBy:!0},{Cell:({row:{original:{last_eval_dttm:e}}})=>e?u().utc(e).local().format(y.v2):"",accessor:"last_eval_dttm",Header:(0,s.t)("Last run"),size:"lg"},{accessor:"name",Header:(0,s.t)("Name"),size:"xl"},{Header:(0,s.t)("Schedule"),accessor:"crontab_humanized",size:"xl",Cell:({row:{original:{crontab_humanized:e=""}}})=>(0,A.tZ)(g.u,{title:e,placement:"topLeft"},(0,A.tZ)("span",null,e))},{Cell:({row:{original:{recipients:e}}})=>e.map((e=>(0,A.tZ)(S.Z,{key:e.id,type:e.type}))),accessor:"recipients",Header:(0,s.t)("Notification method"),disableSortBy:!0,size:"xl"},{accessor:"created_by",disableSortBy:!0,hidden:!0,size:"xl"},{Cell:({row:{original:{owners:e=[]}}})=>(0,A.tZ)(h.Z,{users:e}),Header:(0,s.t)("Owners"),id:"owners",disableSortBy:!0,size:"xl"},{Cell:({row:{original:e}})=>(0,A.tZ)(b.r,{"data-test":"toggle-active",checked:e.active,onClick:t=>((e,t)=>{if(e&&e.id){const r=e.id;F(r,{active:t}).then((()=>{P()}))}})(e,t),size:"small"}),Header:(0,s.t)("Active"),accessor:"active",id:"active",size:"xl"},{Cell:w((({row:{original:e}})=>{const t=(0,n.k6)(),r=[X?{label:"execution-log-action",tooltip:(0,s.t)("Execution log"),placement:"bottom",icon:"Note",onClick:()=>t.push(`/${e.type.toLowerCase()}/${e.id}/log`)}:null,X?{label:"edit-action",tooltip:(0,s.t)("Edit"),placement:"bottom",icon:"Edit",onClick:()=>J(e)}:null,Q?{label:"delete-action",tooltip:(0,s.t)("Delete"),placement:"bottom",icon:"Trash",onClick:()=>Y(e)}:null].filter((e=>null!==e));return(0,A.tZ)(p.Z,{actions:r})}),"useHistory{history}",(()=>[n.k6])),Header:(0,s.t)("Actions"),id:"actions",hidden:!X&&!Q,disableSortBy:!0,size:"xl"}]),[Q,X,t]),ae=[];ee&&ae.push({name:(0,A.tZ)(o.Fragment,null,(0,A.tZ)("i",{className:"fa fa-plus"})," ",l),buttonStyle:"primary",onClick:()=>{J(null)}}),Q&&ae.push({name:(0,s.t)("Bulk select"),onClick:j,buttonStyle:"secondary","data-test":"bulk-select-toggle"});const oe=(0,A.tZ)(m.Z,{buttonStyle:"primary",onClick:()=>J(null)},(0,A.tZ)("i",{className:"fa fa-plus"})," ",l),ne={message:(0,s.t)("No %s yet",i),slot:ee?oe:null},se=(0,o.useMemo)((()=>[{Header:(0,s.t)("Created by"),id:"created_by",input:"select",operator:f.p.relationOneMany,unfilteredLabel:"All",fetchSelects:(0,N.tm)("report","created_by",(0,N.v$)((e=>(0,s.t)("An error occurred while fetching created by values: %s",e))),r),paginate:!0},{Header:(0,s.t)("Status"),id:"last_state",input:"select",operator:f.p.equals,unfilteredLabel:"Any",selects:[{label:H[R.Z.Success],value:R.Z.Success},{label:H[R.Z.Working],value:R.Z.Working},{label:H[R.Z.Error],value:R.Z.Error},{label:H[R.Z.Noop],value:R.Z.Noop},{label:H[R.Z.Grace],value:R.Z.Grace}]},{Header:(0,s.t)("Search"),id:"name",input:"search",operator:f.p.contains}]),[]);return(0,A.tZ)(o.Fragment,null,(0,A.tZ)(v.Z,{activeChild:c,name:(0,s.t)("Alerts & reports"),tabs:[{name:"Alerts",label:(0,s.t)("Alerts"),url:"/alert/list/",usesRouter:!0,"data-test":"alert-list"},{name:"Reports",label:(0,s.t)("Reports"),url:"/report/list/",usesRouter:!0,"data-test":"report-list"}],buttons:ae},(0,A.tZ)(E,null,(0,A.tZ)(U.Z,{updatedAt:$,update:()=>P()}))),(0,A.tZ)(_.Z,{alert:V,addDangerToast:e,layer:V,onHide:()=>{B(!1),W(null),P()},show:q,isReport:t,key:(null==V?void 0:V.id)||`${(new Date).getTime()}`}),K&&(0,A.tZ)(L.Z,{description:(0,s.t)("This action will permanently delete %s.",K.name),onConfirm:()=>{K&&(({id:t,name:r})=>{d.Z.delete({endpoint:`/api/v1/report/${t}`}).then((()=>{P(),Y(null),a((0,s.t)("Deleted: %s",r))}),(0,N.v$)((t=>e((0,s.t)("There was an issue deleting %s: %s",r,t)))))})(K)},onHide:()=>Y(null),open:!0,title:(0,s.t)("Delete %s?",l)}),(0,A.tZ)(C.Z,{title:(0,s.t)("Please confirm"),description:(0,s.t)("Are you sure you want to delete the selected %s?",i),onConfirm:async t=>{try{const{message:e}=await G(t.map((({id:e})=>e)));P(),a(e)}catch(t){(0,N.v$)((t=>e((0,s.t)("There was an issue deleting the selected %s: %s",i,t))))(t)}}},(e=>{const t=Q?[{key:"delete",name:(0,s.t)("Delete"),onSelect:e,type:"danger"}]:[];return(0,A.tZ)(f.Z,{className:"alerts-list-view",columns:re,count:k,data:D,emptyState:ne,fetchData:I,filters:se,initialSort:te,loading:M,bulkActions:t,bulkSelectEnabled:O,disableBulkSelect:j,pageSize:25})})))}w(M,"useMemo{initalFilters}\nuseListViewResource{{ state: { loading, resourceCount: alertsCount, resourceCollection: alerts, bulkSelectEnabled, lastFetched, }, hasPerm, fetchData, refreshData, toggleBulkSelect, }}\nuseSingleViewResource{{ updateResource }}\nuseState{[alertModalOpen, setAlertModalOpen](false)}\nuseState{[currentAlert, setCurrentAlert](null)}\nuseState{[currentAlertDeleting, setCurrentAlertDeleting](null)}\nuseEffect{}\nuseMemo{columns}\nuseMemo{filters}",(()=>[T.Yi,T.LE]));const k=(0,Z.Z)(M),D=k;var O,$;(O="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.default:void 0)&&(O.register(25,"PAGE_SIZE","/Users/chenming/superset/superset-frontend/src/views/CRUD/alert/AlertList.tsx"),O.register(H,"AlertStateLabel","/Users/chenming/superset/superset-frontend/src/views/CRUD/alert/AlertList.tsx"),O.register(G,"deleteAlerts","/Users/chenming/superset/superset-frontend/src/views/CRUD/alert/AlertList.tsx"),O.register(E,"RefreshContainer","/Users/chenming/superset/superset-frontend/src/views/CRUD/alert/AlertList.tsx"),O.register(M,"AlertList","/Users/chenming/superset/superset-frontend/src/views/CRUD/alert/AlertList.tsx"),O.register(k,"default","/Users/chenming/superset/superset-frontend/src/views/CRUD/alert/AlertList.tsx")),($="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.leaveModule:void 0)&&$(e)},590584:(e,t,r)=>{r.d(t,{j:()=>$,Z:()=>W});var a,o=r(211965),n=r(667294),s=r(455867),l=r(751995),i=r(431069),d=r(115926),c=r.n(d),u=r(34858),p=r(87693),m=r(112441),h=r(574520),g=r(898978),f=r(287183),v=r(281315),b=r(591877),y=r(414114),Z=r(104715),x=r(542878),S=r(301483),C=r(409882),L=r(856400),U=r(62557);e=r.hmd(e),(a="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.enterModule:void 0)&&a(e);var T="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.default.signature:function(e){return e};const N=["pivot_table","pivot_table_v2","table","paired_ttest"],_=["Email"],R="PNG",A=[{label:(0,s.t)("< (Smaller than)"),value:"<"},{label:(0,s.t)("> (Larger than)"),value:">"},{label:(0,s.t)("<= (Smaller or equal)"),value:"<="},{label:(0,s.t)(">= (Larger or equal)"),value:">="},{label:(0,s.t)("== (Is equal)"),value:"=="},{label:(0,s.t)("!= (Is not equal)"),value:"!="},{label:(0,s.t)("Not null"),value:"not null"}],w=[{label:(0,s.t)("None"),value:0},{label:(0,s.t)("30 days"),value:30},{label:(0,s.t)("60 days"),value:60},{label:(0,s.t)("90 days"),value:90}],H="0 * * * *",G={active:!0,creation_method:"alerts_reports",crontab:H,log_retention:90,working_timeout:3600,name:"",owners:[],recipients:[],sql:"",validator_config_json:{},validator_type:"",force_screenshot:!1,grace_period:void 0},E=(0,l.iK)(h.Z)`
  .ant-modal-body {
    overflow: initial;
  }
`,M=e=>o.iv`
  margin: auto ${2*e.gridUnit}px auto 0;
  color: ${e.colors.grayscale.base};
`,k=l.iK.div`
  display: flex;
  min-width: 1000px;
  flex-direction: column;

  .header-section {
    display: flex;
    flex: 0 0 auto;
    align-items: center;
    width: 100%;
    padding: ${({theme:e})=>4*e.gridUnit}px;
    border-bottom: 1px solid ${({theme:e})=>e.colors.grayscale.light2};
  }

  .column-section {
    display: flex;
    flex: 1 1 auto;

    .column {
      flex: 1 1 auto;
      min-width: calc(33.33% - ${({theme:e})=>8*e.gridUnit}px);
      padding: ${({theme:e})=>4*e.gridUnit}px;

      .async-select {
        margin: 10px 0 20px;
      }

      &.condition {
        border-right: 1px solid ${({theme:e})=>e.colors.grayscale.light2};
      }

      &.message {
        border-left: 1px solid ${({theme:e})=>e.colors.grayscale.light2};
      }
    }
  }

  .inline-container {
    display: flex;
    flex-direction: row;
    align-items: center;
    &.wrap {
      flex-wrap: wrap;
    }

    > div {
      flex: 1 1 auto;
    }

    &.add-margin {
      margin-bottom: 5px;
    }

    .styled-input {
      margin: 0 0 0 10px;

      input {
        flex: 0 0 auto;
      }
    }
  }
`,D=l.iK.div`
  display: flex;
  align-items: center;
  margin: ${({theme:e})=>2*e.gridUnit}px auto
    ${({theme:e})=>4*e.gridUnit}px auto;

  h4 {
    margin: 0;
  }

  .required {
    margin-left: ${({theme:e})=>e.gridUnit}px;
    color: ${({theme:e})=>e.colors.error.base};
  }
`,O=l.iK.div`
  display: flex;
  align-items: center;
  margin-top: 10px;

  .switch-label {
    margin-left: 10px;
  }
`,$=l.iK.div`
  flex: 1;
  margin: ${({theme:e})=>2*e.gridUnit}px;
  margin-top: 0;

  .helper {
    display: block;
    color: ${({theme:e})=>e.colors.grayscale.base};
    font-size: ${({theme:e})=>e.typography.sizes.s-1}px;
    padding: ${({theme:e})=>e.gridUnit}px 0;
    text-align: left;
  }

  .required {
    margin-left: ${({theme:e})=>e.gridUnit/2}px;
    color: ${({theme:e})=>e.colors.error.base};
  }

  .input-container {
    display: flex;
    align-items: center;

    > div {
      width: 100%;
    }

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

  input[disabled] {
    color: ${({theme:e})=>e.colors.grayscale.base};
  }

  textarea {
    height: 300px;
    resize: none;
  }

  input::placeholder,
  textarea::placeholder {
    color: ${({theme:e})=>e.colors.grayscale.light1};
  }

  textarea,
  input[type='text'],
  input[type='number'] {
    padding: ${({theme:e})=>e.gridUnit}px
      ${({theme:e})=>2*e.gridUnit}px;
    border-style: none;
    border: 1px solid ${({theme:e})=>e.colors.grayscale.light2};
    border-radius: ${({theme:e})=>e.gridUnit}px;

    &[name='description'] {
      flex: 1 1 auto;
    }
  }

  .input-label {
    margin-left: 10px;
  }
`,z=(0,l.iK)(f.Y)`
  display: block;
  line-height: ${({theme:e})=>7*e.gridUnit}px;
`,I=(0,l.iK)(f.Y.Group)`
  margin-left: ${({theme:e})=>5.5*e.gridUnit}px;
`,P=(0,l.iK)(Z.r4)`
  margin-left: ${({theme:e})=>5.5*e.gridUnit}px;
`,j=l.iK.div`
  color: ${({theme:e})=>e.colors.primary.dark1};
  cursor: pointer;

  i {
    margin-right: ${({theme:e})=>2*e.gridUnit}px;
  }

  &.disabled {
    color: ${({theme:e})=>e.colors.grayscale.light1};
    cursor: default;
  }
`,F=e=>o.iv`
  margin: ${3*e.gridUnit}px 0;
`,q=({status:e="active",onClick:t})=>"hidden"===e?null:(0,o.tZ)(j,{className:e,onClick:()=>{"disabled"!==e&&t()}},(0,o.tZ)("i",{className:"fa fa-plus"})," ","active"===e?(0,s.t)("Add notification method"):(0,s.t)("Add delivery method")),B=({addDangerToast:e,onAdd:t,onHide:r,show:a,alert:l=null,isReport:d=!1})=>{var h,y,Z,T,j,B,V;const W=(0,S.c)(),K=(null==W?void 0:W.ALERT_REPORTS_NOTIFICATION_METHODS)||_,[Y,J]=(0,n.useState)(!0),[X,Q]=(0,n.useState)(),[ee,te]=(0,n.useState)(!0),[re,ae]=(0,n.useState)("dashboard"),[oe,ne]=(0,n.useState)(R),[se,le]=(0,n.useState)(!1),[ie,de]=(0,n.useState)(!1),[ce,ue]=(0,n.useState)([]),[pe,me]=(0,n.useState)([]),[he,ge]=(0,n.useState)([]),[fe,ve]=(0,n.useState)(""),be=null!==l,ye="chart"===re&&((0,b.cr)(b.TT.ALERTS_ATTACH_REPORTS)||d),[Ze,xe]=(0,n.useState)("active"),[Se,Ce]=(0,n.useState)([]),Le=(e,t)=>{const r=Se.slice();r[e]=t,Ce(r),void 0!==t.method&&"hidden"!==Ze&&xe("active")},Ue=e=>{const t=Se.slice();t.splice(e,1),Ce(t),xe("active")},{state:{loading:Te,resource:Ne,error:_e},fetchResource:Re,createResource:Ae,updateResource:we,clearError:He}=(0,u.LE)("report",(0,s.t)("report"),e),Ge=()=>{He(),te(!0),r(),Ce([]),Q({...G}),xe("active")},Ee=(0,n.useMemo)((()=>(e="",t,r)=>{const a=c().encode({filter:e,page:t,page_size:r});return i.Z.get({endpoint:`/api/v1/report/related/created_by?q=${a}`}).then((e=>({data:e.json.result.map((e=>({value:e.value,label:e.text}))),totalCount:e.json.count})))}),[]),Me=(0,n.useCallback)((e=>{const t=e||(null==X?void 0:X.database);if(!t||t.label)return null;let r;return ce.forEach((e=>{e.value!==t.value&&e.value!==t.id||(r=e)})),r}),[null==X?void 0:X.database,ce]),ke=(e,t)=>{Q((r=>({...r,[e]:t})))},De=(0,n.useMemo)((()=>(e="",t,r)=>{const a=c().encode({filter:e,page:t,page_size:r});return i.Z.get({endpoint:`/api/v1/report/related/database?q=${a}`}).then((e=>{const t=e.json.result.map((e=>({value:e.value,label:e.text})));return ue(t),{data:t,totalCount:e.json.count}}))}),[]),Oe=X&&X.database&&!X.database.label;(0,n.useEffect)((()=>{Oe&&ke("database",Me())}),[Oe,Me]);const $e=(0,n.useMemo)((()=>(e="",t,r)=>{const a=c().encode_uri({filter:e,page:t,page_size:r});return i.Z.get({endpoint:`/api/v1/report/related/dashboard?q=${a}`}).then((e=>{const t=e.json.result.map((e=>({value:e.value,label:e.text})));return me(t),{data:t,totalCount:e.json.count}}))}),[]),ze=e=>{const t=e||(null==X?void 0:X.dashboard);if(!t||t.label)return null;let r;return pe.forEach((e=>{e.value!==t.value&&e.value!==t.id||(r=e)})),r},Ie=(0,n.useCallback)((e=>{const t=e||(null==X?void 0:X.chart);if(!t||t.label)return null;let r;return he.forEach((e=>{e.value!==t.value&&e.value!==t.id||(r=e)})),r}),[he,null==X?void 0:X.chart]),Pe=X&&X.chart&&!X.chart.label;(0,n.useEffect)((()=>{Pe&&ke("chart",Ie())}),[Ie,Pe]);const je=(0,n.useMemo)((()=>(e="",t,r)=>{const a=c().encode_uri({filter:e,page:t,page_size:r});return i.Z.get({endpoint:`/api/v1/report/related/chart?q=${a}`}).then((e=>{const t=e.json.result.map((e=>({value:e.value,label:e.text})));return ge(t),{data:t,totalCount:e.json.count}}))}),[]),Fe=e=>{const{target:t}=e;ke(t.name,t.value)},qe=e=>{const{target:t}=e,r=+t.value;ke(t.name,0===r?null:r?Math.max(r,1):r)};(0,n.useEffect)((()=>{if(be&&(null==X||!X.id||(null==l?void 0:l.id)!==X.id||ee&&a)){if(l&&null!==l.id&&!Te&&!_e){const e=l.id||0;Re(e)}}else!be&&(!X||X.id||ee&&a)&&(Q({...G}),Ce([]),xe("active"))}),[l]),(0,n.useEffect)((()=>{if(Ne){const e=(Ne.recipients||[]).map((e=>{const t="string"==typeof e.recipient_config_json?JSON.parse(e.recipient_config_json):{};return{method:e.type,recipients:t.target||e.recipient_config_json,options:K}}));Ce(e),xe(e.length===K.length?"hidden":"active"),ae(Ne.chart?"chart":"dashboard"),ne(Ne.chart&&Ne.report_format||R);const t="string"==typeof Ne.validator_config_json?JSON.parse(Ne.validator_config_json):Ne.validator_config_json;de("not null"===Ne.validator_type),Ne.chart&&ve(Ne.chart.viz_type),le(Ne.force_screenshot),Q({...Ne,chart:Ne.chart?Ie(Ne.chart)||{value:Ne.chart.id,label:Ne.chart.slice_name}:void 0,dashboard:Ne.dashboard?ze(Ne.dashboard)||{value:Ne.dashboard.id,label:Ne.dashboard.dashboard_title}:void 0,database:Ne.database?Me(Ne.database)||{value:Ne.database.id,label:Ne.database.database_name}:void 0,owners:((null==l?void 0:l.owners)||[]).map((e=>({value:e.value||e.id,label:e.label||`${e.first_name} ${e.last_name}`}))),validator_config_json:"not null"===Ne.validator_type?{op:"not null"}:t})}}),[Ne]);const Be=X||{};return(0,n.useEffect)((()=>{var e,t,r,a,o,n;X&&null!=(e=X.name)&&e.length&&null!=(t=X.owners)&&t.length&&null!=(r=X.crontab)&&r.length&&void 0!==X.working_timeout&&("dashboard"===re&&X.dashboard||"chart"===re&&X.chart)&&(()=>{if(!Se.length)return!1;let e=!1;return Se.forEach((t=>{var r;t.method&&null!=(r=t.recipients)&&r.length&&(e=!0)})),e})()&&(d||X.database&&null!=(a=X.sql)&&a.length&&(ie||null!=(o=X.validator_config_json)&&o.op)&&(ie||void 0!==(null==(n=X.validator_config_json)?void 0:n.threshold)))?J(!1):J(!0)}),[Be.name,Be.owners,Be.database,Be.sql,Be.validator_config_json,Be.crontab,Be.working_timeout,Be.dashboard,Be.chart,re,Se,ie]),ee&&a&&te(!1),(0,o.tZ)(E,{className:"no-content-padding",responsive:!0,disablePrimaryButton:Y,onHandledPrimaryAction:()=>{var e,r,a;const o=[];Se.forEach((e=>{e.method&&e.recipients.length&&o.push({recipient_config_json:{target:e.recipients},type:e.method})}));const n="chart"===re&&!d,s={...X,type:d?"Report":"Alert",force_screenshot:n||se,validator_type:ie?"not null":"operator",validator_config_json:ie?{}:null==X?void 0:X.validator_config_json,chart:"chart"===re?null==X||null==(e=X.chart)?void 0:e.value:null,dashboard:"dashboard"===re?null==X||null==(r=X.dashboard)?void 0:r.value:null,database:null==X||null==(a=X.database)?void 0:a.value,owners:((null==X?void 0:X.owners)||[]).map((e=>e.value||e.id)),recipients:o,report_format:"dashboard"===re?R:oe||R};if(s.recipients&&!s.recipients.length&&delete s.recipients,s.context_markdown="string",be){if(X&&X.id){const e=X.id;delete s.id,delete s.created_by,delete s.last_eval_dttm,delete s.last_state,delete s.last_value,delete s.last_value_row_json,we(e,s).then((e=>{e&&(t&&t(),Ge())}))}}else X&&Ae(s).then((e=>{e&&(t&&t(e),Ge())}))},onHide:Ge,primaryButtonName:be?(0,s.t)("Save"):(0,s.t)("Add"),show:a,width:"100%",maxWidth:"1450px",title:(0,o.tZ)("h4",{"data-test":"alert-report-modal-title"},be?(0,o.tZ)(p.Z.EditAlt,{css:M}):(0,o.tZ)(p.Z.PlusLarge,{css:M}),be&&d?(0,s.t)("Edit Report"):be?(0,s.t)("Edit Alert"):d?(0,s.t)("Add Report"):(0,s.t)("Add Alert"))},(0,o.tZ)(k,null,(0,o.tZ)("div",{className:"header-section"},(0,o.tZ)($,null,(0,o.tZ)("div",{className:"control-label"},d?(0,s.t)("Report name"):(0,s.t)("Alert name"),(0,o.tZ)("span",{className:"required"},"*")),(0,o.tZ)("div",{className:"input-container"},(0,o.tZ)("input",{type:"text",name:"name",value:X?X.name:"",placeholder:d?(0,s.t)("Report name"):(0,s.t)("Alert name"),onChange:Fe}))),(0,o.tZ)($,null,(0,o.tZ)("div",{className:"control-label"},(0,s.t)("Owners"),(0,o.tZ)("span",{className:"required"},"*")),(0,o.tZ)("div",{"data-test":"owners-select",className:"input-container"},(0,o.tZ)(v.ZP,{ariaLabel:(0,s.t)("Owners"),allowClear:!0,name:"owners",mode:"multiple",value:(null==X?void 0:X.owners)||[],options:Ee,onChange:e=>{ke("owners",e||[])}}))),(0,o.tZ)($,null,(0,o.tZ)("div",{className:"control-label"},(0,s.t)("Description")),(0,o.tZ)("div",{className:"input-container"},(0,o.tZ)("input",{type:"text",name:"description",value:X&&X.description||"",placeholder:(0,s.t)("Description"),onChange:Fe}))),(0,o.tZ)(O,null,(0,o.tZ)(m.r,{onChange:e=>{ke("active",e)},checked:!X||X.active}),(0,o.tZ)("div",{className:"switch-label"},"Active"))),(0,o.tZ)("div",{className:"column-section"},!d&&(0,o.tZ)("div",{className:"column condition"},(0,o.tZ)(D,null,(0,o.tZ)("h4",null,(0,s.t)("Alert condition"))),(0,o.tZ)($,null,(0,o.tZ)("div",{className:"control-label"},(0,s.t)("Database"),(0,o.tZ)("span",{className:"required"},"*")),(0,o.tZ)("div",{className:"input-container"},(0,o.tZ)(v.ZP,{ariaLabel:(0,s.t)("Database"),name:"source",value:null!=X&&null!=(h=X.database)&&h.label&&null!=X&&null!=(y=X.database)&&y.value?{value:X.database.value,label:X.database.label}:void 0,options:De,onChange:e=>{ke("database",e||[])}}))),(0,o.tZ)($,null,(0,o.tZ)("div",{className:"control-label"},(0,s.t)("SQL Query"),(0,o.tZ)("span",{className:"required"},"*")),(0,o.tZ)(x.Z,{name:"sql",language:"sql",offerEditInModal:!1,minLines:15,maxLines:15,onChange:e=>{ke("sql",e||"")},readOnly:!1,initialValue:null==Ne?void 0:Ne.sql,key:null==X?void 0:X.id})),(0,o.tZ)("div",{className:"inline-container wrap"},(0,o.tZ)($,null,(0,o.tZ)("div",{className:"control-label"},(0,s.t)("Trigger Alert If..."),(0,o.tZ)("span",{className:"required"},"*")),(0,o.tZ)("div",{className:"input-container"},(0,o.tZ)(v.ZP,{ariaLabel:(0,s.t)("Condition"),onChange:e=>{var t;de("not null"===e);const r={op:e,threshold:X?null==(t=X.validator_config_json)?void 0:t.threshold:void 0};ke("validator_config_json",r)},placeholder:"Condition",value:(null==X||null==(Z=X.validator_config_json)?void 0:Z.op)||void 0,options:A}))),(0,o.tZ)($,null,(0,o.tZ)("div",{className:"control-label"},(0,s.t)("Value")," ",(0,o.tZ)(C.V,{tooltip:(0,s.t)("Threshold value should be double precision number")}),(0,o.tZ)("span",{className:"required"},"*")),(0,o.tZ)("div",{className:"input-container"},(0,o.tZ)("input",{type:"number",name:"threshold",disabled:ie,value:X&&X.validator_config_json&&void 0!==X.validator_config_json.threshold?X.validator_config_json.threshold:"",placeholder:(0,s.t)("Value"),onChange:e=>{var t;const{target:r}=e,a={op:X?null==(t=X.validator_config_json)?void 0:t.op:void 0,threshold:r.value};ke("validator_config_json",a)}}))))),(0,o.tZ)("div",{className:"column schedule"},(0,o.tZ)(D,null,(0,o.tZ)("h4",null,d?(0,s.t)("Report schedule"):(0,s.t)("Alert condition schedule")),(0,o.tZ)("span",{className:"required"},"*")),(0,o.tZ)(L.C,{value:(null==X?void 0:X.crontab)||H,onChange:e=>ke("crontab",e)}),(0,o.tZ)("div",{className:"control-label"},(0,s.t)("Timezone")),(0,o.tZ)("div",{className:"input-container",css:e=>F(e)},(0,o.tZ)(g.Z,{onTimezoneChange:e=>{ke("timezone",e)},timezone:null==X?void 0:X.timezone})),(0,o.tZ)(D,null,(0,o.tZ)("h4",null,(0,s.t)("Schedule settings"))),(0,o.tZ)($,null,(0,o.tZ)("div",{className:"control-label"},(0,s.t)("Log retention"),(0,o.tZ)("span",{className:"required"},"*")),(0,o.tZ)("div",{className:"input-container"},(0,o.tZ)(v.ZP,{ariaLabel:(0,s.t)("Log retention"),placeholder:(0,s.t)("Log retention"),onChange:e=>{ke("log_retention",e)},value:"number"==typeof(null==X?void 0:X.log_retention)?null==X?void 0:X.log_retention:90,options:w,sortComparator:(0,v.mj)("value")}))),(0,o.tZ)($,null,(0,o.tZ)("div",{className:"control-label"},(0,s.t)("Working timeout"),(0,o.tZ)("span",{className:"required"},"*")),(0,o.tZ)("div",{className:"input-container"},(0,o.tZ)("input",{type:"number",min:"1",name:"working_timeout",value:(null==X?void 0:X.working_timeout)||"",placeholder:(0,s.t)("Time in seconds"),onChange:qe}),(0,o.tZ)("span",{className:"input-label"},"seconds"))),!d&&(0,o.tZ)($,null,(0,o.tZ)("div",{className:"control-label"},(0,s.t)("Grace period")),(0,o.tZ)("div",{className:"input-container"},(0,o.tZ)("input",{type:"number",min:"1",name:"grace_period",value:(null==X?void 0:X.grace_period)||"",placeholder:(0,s.t)("Time in seconds"),onChange:qe}),(0,o.tZ)("span",{className:"input-label"},"seconds")))),(0,o.tZ)("div",{className:"column message"},(0,o.tZ)(D,null,(0,o.tZ)("h4",null,(0,s.t)("Message content")),(0,o.tZ)("span",{className:"required"},"*")),(0,o.tZ)(f.Y.Group,{onChange:e=>{const{target:t}=e;le(!1),setTimeout((()=>ae(t.value)),200)},value:re},(0,o.tZ)(z,{value:"dashboard"},(0,s.t)("Dashboard")),(0,o.tZ)(z,{value:"chart"},(0,s.t)("Chart"))),(0,o.tZ)(v.ZP,{ariaLabel:(0,s.t)("Chart"),css:(0,o.iv)({display:"chart"===re?"inline":"none"},"",""),name:"chart",value:null!=X&&null!=(T=X.chart)&&T.label&&null!=X&&null!=(j=X.chart)&&j.value?{value:X.chart.value,label:X.chart.label}:void 0,options:je,onChange:e=>{(e=>{i.Z.get({endpoint:`/api/v1/chart/${e.value}`}).then((e=>ve(e.json.result.viz_type)))})(e),ke("chart",e||void 0),ke("dashboard",null)}}),(0,o.tZ)(v.ZP,{ariaLabel:(0,s.t)("Dashboard"),css:(0,o.iv)({display:"dashboard"===re?"inline":"none"},"",""),name:"dashboard",value:null!=X&&null!=(B=X.dashboard)&&B.label&&null!=X&&null!=(V=X.dashboard)&&V.value?{value:X.dashboard.value,label:X.dashboard.label}:void 0,options:$e,onChange:e=>{ke("dashboard",e||void 0),ke("chart",null)}}),ye&&(0,o.tZ)(n.Fragment,null,(0,o.tZ)("div",{className:"inline-container"},(0,o.tZ)(I,{onChange:e=>{const{target:t}=e;ne(t.value)},value:oe},(0,o.tZ)(z,{value:"PNG"},(0,s.t)("Send as PNG")),(0,o.tZ)(z,{value:"CSV"},(0,s.t)("Send as CSV")),N.includes(fe)&&(0,o.tZ)(z,{value:"TEXT"},(0,s.t)("Send as text"))))),(d||"dashboard"===re)&&(0,o.tZ)("div",{className:"inline-container"},(0,o.tZ)(P,{"data-test":"bypass-cache",className:"checkbox",checked:se,onChange:e=>{le(e.target.checked)}},"Ignore cache when generating screenshot")),(0,o.tZ)(D,null,(0,o.tZ)("h4",null,(0,s.t)("Notification method")),(0,o.tZ)("span",{className:"required"},"*")),Se.map(((e,t)=>(0,o.tZ)(U.K,{setting:e,index:t,key:`NotificationMethod-${t}`,onUpdate:Le,onRemove:Ue}))),(0,o.tZ)(q,{"data-test":"notification-add",status:Ze,onClick:()=>{const e=Se.slice();e.push({recipients:"",options:K}),Ce(e),xe(e.length===K.length?"hidden":"disabled")}})))))};T(B,"useCommonConf{conf}\nuseState{[disableSave, setDisableSave](true)}\nuseState{[currentAlert, setCurrentAlert]}\nuseState{[isHidden, setIsHidden](true)}\nuseState{[contentType, setContentType]('dashboard')}\nuseState{[reportFormat, setReportFormat](DEFAULT_NOTIFICATION_FORMAT)}\nuseState{[forceScreenshot, setForceScreenshot](false)}\nuseState{[conditionNotNull, setConditionNotNull](false)}\nuseState{[sourceOptions, setSourceOptions]([])}\nuseState{[dashboardOptions, setDashboardOptions]([])}\nuseState{[chartOptions, setChartOptions]([])}\nuseState{[chartVizType, setChartVizType]('')}\nuseState{[notificationAddState, setNotificationAddState]('active')}\nuseState{[notificationSettings, setNotificationSettings]([])}\nuseSingleViewResource{{ state: { loading, resource, error: fetchError }, fetchResource, createResource, updateResource, clearError, }}\nuseMemo{loadOwnerOptions}\nuseCallback{getSourceData}\nuseMemo{loadSourceOptions}\nuseEffect{}\nuseMemo{loadDashboardOptions}\nuseCallback{getChartData}\nuseEffect{}\nuseMemo{loadChartOptions}\nuseEffect{}\nuseEffect{}\nuseEffect{}",(()=>[S.c,u.LE]));const V=(0,y.Z)(B),W=V;var K,Y;(K="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.default:void 0)&&(K.register(1,"TIMEOUT_MIN","/Users/chenming/superset/superset-frontend/src/views/CRUD/alert/AlertReportModal.tsx"),K.register(N,"TEXT_BASED_VISUALIZATION_TYPES","/Users/chenming/superset/superset-frontend/src/views/CRUD/alert/AlertReportModal.tsx"),K.register(_,"DEFAULT_NOTIFICATION_METHODS","/Users/chenming/superset/superset-frontend/src/views/CRUD/alert/AlertReportModal.tsx"),K.register(R,"DEFAULT_NOTIFICATION_FORMAT","/Users/chenming/superset/superset-frontend/src/views/CRUD/alert/AlertReportModal.tsx"),K.register(A,"CONDITIONS","/Users/chenming/superset/superset-frontend/src/views/CRUD/alert/AlertReportModal.tsx"),K.register(w,"RETENTION_OPTIONS","/Users/chenming/superset/superset-frontend/src/views/CRUD/alert/AlertReportModal.tsx"),K.register(90,"DEFAULT_RETENTION","/Users/chenming/superset/superset-frontend/src/views/CRUD/alert/AlertReportModal.tsx"),K.register(3600,"DEFAULT_WORKING_TIMEOUT","/Users/chenming/superset/superset-frontend/src/views/CRUD/alert/AlertReportModal.tsx"),K.register(H,"DEFAULT_CRON_VALUE","/Users/chenming/superset/superset-frontend/src/views/CRUD/alert/AlertReportModal.tsx"),K.register(G,"DEFAULT_ALERT","/Users/chenming/superset/superset-frontend/src/views/CRUD/alert/AlertReportModal.tsx"),K.register(E,"StyledModal","/Users/chenming/superset/superset-frontend/src/views/CRUD/alert/AlertReportModal.tsx"),K.register(M,"StyledIcon","/Users/chenming/superset/superset-frontend/src/views/CRUD/alert/AlertReportModal.tsx"),K.register(k,"StyledSectionContainer","/Users/chenming/superset/superset-frontend/src/views/CRUD/alert/AlertReportModal.tsx"),K.register(D,"StyledSectionTitle","/Users/chenming/superset/superset-frontend/src/views/CRUD/alert/AlertReportModal.tsx"),K.register(O,"StyledSwitchContainer","/Users/chenming/superset/superset-frontend/src/views/CRUD/alert/AlertReportModal.tsx"),K.register($,"StyledInputContainer","/Users/chenming/superset/superset-frontend/src/views/CRUD/alert/AlertReportModal.tsx"),K.register(z,"StyledRadio","/Users/chenming/superset/superset-frontend/src/views/CRUD/alert/AlertReportModal.tsx"),K.register(I,"StyledRadioGroup","/Users/chenming/superset/superset-frontend/src/views/CRUD/alert/AlertReportModal.tsx"),K.register(P,"StyledCheckbox","/Users/chenming/superset/superset-frontend/src/views/CRUD/alert/AlertReportModal.tsx"),K.register(j,"StyledNotificationAddButton","/Users/chenming/superset/superset-frontend/src/views/CRUD/alert/AlertReportModal.tsx"),K.register(F,"timezoneHeaderStyle","/Users/chenming/superset/superset-frontend/src/views/CRUD/alert/AlertReportModal.tsx"),K.register(q,"NotificationMethodAdd","/Users/chenming/superset/superset-frontend/src/views/CRUD/alert/AlertReportModal.tsx"),K.register(B,"AlertReportModal","/Users/chenming/superset/superset-frontend/src/views/CRUD/alert/AlertReportModal.tsx"),K.register(V,"default","/Users/chenming/superset/superset-frontend/src/views/CRUD/alert/AlertReportModal.tsx")),(Y="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.leaveModule:void 0)&&Y(e)},856400:(e,t,r)=>{r.d(t,{C:()=>m});var a,o=r(667294),n=r(751995),s=r(455867),l=r(9875),i=r(287183),d=r(215428),c=r(590584),u=r(211965);e=r.hmd(e),(a="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.enterModule:void 0)&&a(e);var p="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.default.signature:function(e){return e};const m=({value:e,onChange:t})=>{const r=(0,n.Fg)(),a=(0,o.useRef)(null),[p,m]=(0,o.useState)("picker"),h=(0,o.useCallback)((e=>{var r;t(e),null==(r=a.current)||r.setValue(e)}),[a,t]),[g,f]=(0,o.useState)();return(0,u.tZ)(o.Fragment,null,(0,u.tZ)(i.Y.Group,{onChange:e=>m(e.target.value),value:p},(0,u.tZ)("div",{className:"inline-container add-margin"},(0,u.tZ)(i.Y,{value:"picker"}),(0,u.tZ)(d.CronPicker,{clearButton:!1,value:e,setValue:h,disabled:"picker"!==p,displayError:"picker"===p,onError:f})),(0,u.tZ)("div",{className:"inline-container add-margin"},(0,u.tZ)(i.Y,{value:"input"}),(0,u.tZ)("span",{className:"input-label"},"CRON Schedule"),(0,u.tZ)(c.j,{className:"styled-input"},(0,u.tZ)("div",{className:"input-container"},(0,u.tZ)(l.II,{type:"text",name:"crontab",ref:a,style:g?{borderColor:r.colors.error.base}:{},placeholder:(0,s.t)("CRON expression"),disabled:"input"!==p,onBlur:e=>{t(e.target.value)},onPressEnter:()=>{var e;t((null==(e=a.current)?void 0:e.input.value)||"")}}))))))};var h,g;p(m,"useTheme{theme}\nuseRef{inputRef}\nuseState{[scheduleFormat, setScheduleFormat]('picker')}\nuseCallback{customSetValue}\nuseState{[error, onError]}",(()=>[n.Fg])),(h="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.default:void 0)&&h.register(m,"AlertReportCronScheduler","/Users/chenming/superset/superset-frontend/src/views/CRUD/alert/components/AlertReportCronScheduler.tsx"),(g="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.leaveModule:void 0)&&g(e)},246714:(e,t,r)=>{r.d(t,{Z:()=>m});var a,o,n,s=r(751995),l=r(455867),i=(r(667294),r(358593)),d=r(87693),c=r(802849),u=r(211965);function p(e,t,r){switch(e){case c.Z.Working:return r.colors.primary.base;case c.Z.Error:return r.colors.error.base;case c.Z.Success:return t?r.colors.success.base:r.colors.alert.base;case c.Z.Noop:return r.colors.success.base;case c.Z.Grace:return r.colors.alert.base;default:return r.colors.grayscale.base}}function m({state:e,isReportEnabled:t=!1}){const r=(0,s.Fg)(),a={icon:d.Z.Check,label:"",status:""};switch(e){case c.Z.Success:a.icon=t?d.Z.Check:d.Z.AlertSolidSmall,a.label=t?(0,l.t)("Report sent"):(0,l.t)("Alert triggered, notification sent"),a.status=c.Z.Success;break;case c.Z.Working:a.icon=d.Z.Running,a.label=t?(0,l.t)("Report sending"):(0,l.t)("Alert running"),a.status=c.Z.Working;break;case c.Z.Error:a.icon=d.Z.XSmall,a.label=t?(0,l.t)("Report failed"):(0,l.t)("Alert failed"),a.status=c.Z.Error;break;case c.Z.Noop:a.icon=d.Z.Check,a.label=(0,l.t)("Nothing triggered"),a.status=c.Z.Noop;break;case c.Z.Grace:a.icon=d.Z.AlertSolidSmall,a.label=(0,l.t)("Alert Triggered, In Grace Period"),a.status=c.Z.Grace;break;default:a.icon=d.Z.Check,a.label=(0,l.t)("Nothing triggered"),a.status=c.Z.Noop}const o=a.icon;return(0,u.tZ)(i.u,{title:a.label,placement:"bottomLeft"},(0,u.tZ)(o,{iconColor:p(a.status,t,r)}))}e=r.hmd(e),(a="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.enterModule:void 0)&&a(e),("undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.default.signature:function(e){return e})(m,"useTheme{theme}",(()=>[s.Fg])),(o="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.default:void 0)&&(o.register(p,"getStatusColor","/Users/chenming/superset/superset-frontend/src/views/CRUD/alert/components/AlertStatusIcon.tsx"),o.register(m,"AlertStatusIcon","/Users/chenming/superset/superset-frontend/src/views/CRUD/alert/components/AlertStatusIcon.tsx")),(n="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.leaveModule:void 0)&&n(e)},62557:(e,t,r)=>{r.d(t,{K:()=>m});var a,o=r(667294),n=r(751995),s=r(455867),l=r(104715),i=r(87693),d=r(590584),c=r(211965);e=r.hmd(e),(a="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.enterModule:void 0)&&a(e);var u="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.default.signature:function(e){return e};const p=n.iK.div`
  margin-bottom: 10px;

  .input-container {
    textarea {
      height: auto;
    }
  }

  .inline-container {
    margin-bottom: 10px;

    .input-container {
      margin-left: 10px;
    }

    > div {
      margin: 0;
    }

    .delete-button {
      margin-left: 10px;
      padding-top: 3px;
    }
  }
`,m=({setting:e=null,index:t,onUpdate:r,onRemove:a})=>{const{method:u,recipients:m,options:h}=e||{},[g,f]=(0,o.useState)(m||""),v=(0,n.Fg)();return e?(m&&g!==m&&f(m),(0,c.tZ)(p,null,(0,c.tZ)("div",{className:"inline-container"},(0,c.tZ)(d.j,null,(0,c.tZ)("div",{className:"input-container"},(0,c.tZ)(l.Ph,{ariaLabel:(0,s.t)("Delivery method"),"data-test":"select-delivery-method",onChange:a=>{if(f(""),r){const o={...e,method:a,recipients:""};r(t,o)}},placeholder:(0,s.t)("Select Delivery Method"),options:(h||[]).map((e=>({label:e,value:e}))),value:u}))),void 0!==u&&a?(0,c.tZ)("span",{role:"button",tabIndex:0,className:"delete-button",onClick:()=>a(t)},(0,c.tZ)(i.Z.Trash,{iconColor:v.colors.grayscale.base})):null),void 0!==u?(0,c.tZ)(d.j,null,(0,c.tZ)("div",{className:"control-label"},(0,s.t)(u)),(0,c.tZ)("div",{className:"input-container"},(0,c.tZ)("textarea",{name:"recipients",value:g,onChange:a=>{const{target:o}=a;if(f(o.value),r){const a={...e,recipients:o.value};r(t,a)}}})),(0,c.tZ)("div",{className:"helper"},(0,s.t)('Recipients are separated by "," or ";"'))):null)):null};var h,g;u(m,"useState{[recipientValue, setRecipientValue](recipients || '')}\nuseTheme{theme}",(()=>[n.Fg])),(h="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.default:void 0)&&(h.register(p,"StyledNotificationMethod","/Users/chenming/superset/superset-frontend/src/views/CRUD/alert/components/NotificationMethod.tsx"),h.register(m,"NotificationMethod","/Users/chenming/superset/superset-frontend/src/views/CRUD/alert/components/NotificationMethod.tsx")),(g="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.leaveModule:void 0)&&g(e)},528853:(e,t,r)=>{r.d(t,{Z:()=>d});var a,o=r(211965),n=(r(667294),r(358593)),s=r(87693),l=r(802849);e=r.hmd(e),(a="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.enterModule:void 0)&&a(e),"undefined"!=typeof reactHotLoaderGlobal&&reactHotLoaderGlobal.default.signature;const i=e=>o.iv`
  color: ${e.colors.grayscale.light1};
  margin-right: ${2*e.gridUnit}px;
`;function d({type:e}){const t={icon:null,label:""};switch(e){case l.u.Email:t.icon=(0,o.tZ)(s.Z.Email,{css:i}),t.label=l.u.Email;break;case l.u.Slack:t.icon=(0,o.tZ)(s.Z.Slack,{css:i}),t.label=l.u.Slack;break;default:t.icon=null,t.label=""}return t.icon?(0,o.tZ)(n.u,{title:t.label,placement:"bottom"},t.icon):null}var c,u;(c="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.default:void 0)&&(c.register(i,"StyledIcon","/Users/chenming/superset/superset-frontend/src/views/CRUD/alert/components/RecipientIcon.tsx"),c.register(d,"RecipientIcon","/Users/chenming/superset/superset-frontend/src/views/CRUD/alert/components/RecipientIcon.tsx")),(u="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.leaveModule:void 0)&&u(e)},802849:(e,t,r)=>{var a,o,n,s,l;r.d(t,{Z:()=>o,u:()=>n}),e=r.hmd(e),(a="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.enterModule:void 0)&&a(e),"undefined"!=typeof reactHotLoaderGlobal&&reactHotLoaderGlobal.default.signature,function(e){e.Success="Success",e.Working="Working",e.Error="Error",e.Noop="Not triggered",e.Grace="On Grace"}(o||(o={})),function(e){e.Email="Email",e.Slack="Slack"}(n||(n={})),(s="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.default:void 0)&&(s.register(o,"AlertState","/Users/chenming/superset/superset-frontend/src/views/CRUD/alert/types.ts"),s.register(n,"RecipientIconName","/Users/chenming/superset/superset-frontend/src/views/CRUD/alert/types.ts")),(l="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.leaveModule:void 0)&&l(e)}}]);
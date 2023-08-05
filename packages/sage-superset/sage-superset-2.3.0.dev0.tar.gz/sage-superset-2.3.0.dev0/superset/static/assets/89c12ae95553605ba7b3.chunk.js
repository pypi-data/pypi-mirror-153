"use strict";(globalThis.webpackChunksuperset=globalThis.webpackChunksuperset||[]).push([[9483],{89483:(e,t,r)=>{r.r(t),r.d(t,{default:()=>f});var o,a=r(751995),s=r(667294),n=r(101090),l=r(269856),i=r(174448),d=r(211965);e=r.hmd(e),(o="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.enterModule:void 0)&&o(e);var u="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.default.signature:function(e){return e};const c=(0,a.iK)(i.un)`
  overflow-x: auto;
`,p=a.iK.div`
  padding: 2px;
  & > span,
  & > span:hover {
    border: 2px solid transparent;
    display: inline-block;
    border: ${({theme:e,validateStatus:t})=>{var r;return t&&`2px solid ${null==(r=e.colors[t])?void 0:r.base}`}};
  }
  &:focus {
    & > span {
      border: 2px solid
        ${({theme:e,validateStatus:t})=>{var r;return t?null==(r=e.colors[t])?void 0:r.base:e.colors.primary.base}};
      outline: 0;
      box-shadow: 0 0 0 2px
        ${({validateStatus:e})=>e?"rgba(224, 67, 85, 12%)":"rgba(32, 167, 201, 0.2)"};
    }
  }
`;function f(e){var t;const{setDataMask:r,setFocusedFilter:o,unsetFocusedFilter:a,setFilterActive:i,width:u,height:f,filterState:m,inputRef:v}=e,g=(0,s.useCallback)((e=>{const t=e&&e!==l.vM;r({extraFormData:t?{time_range:e}:{},filterState:{value:t?e:void 0}})}),[r]);return(0,s.useEffect)((()=>{g(m.value)}),[m.value]),null!=(t=e.formData)&&t.inView?(0,d.tZ)(c,{width:u,height:f},(0,d.tZ)(p,{tabIndex:-1,ref:v,validateStatus:m.validateStatus,onFocus:o,onBlur:a,onMouseEnter:o,onMouseLeave:a},(0,d.tZ)(n.Z,{value:m.value||l.vM,name:"time_range",onChange:g,type:m.validateStatus,onOpenPopover:()=>i(!0),onClosePopover:()=>i(!1)}))):null}var m,v;u(f,"useCallback{handleTimeRangeChange}\nuseEffect{}"),(m="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.default:void 0)&&(m.register(c,"TimeFilterStyles","/Users/chenming/superset/superset-frontend/src/filters/components/Time/TimeFilterPlugin.tsx"),m.register(p,"ControlContainer","/Users/chenming/superset/superset-frontend/src/filters/components/Time/TimeFilterPlugin.tsx"),m.register(f,"TimeFilterPlugin","/Users/chenming/superset/superset-frontend/src/filters/components/Time/TimeFilterPlugin.tsx")),(v="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.leaveModule:void 0)&&v(e)},174448:(e,t,r)=>{r.d(t,{un:()=>n,jp:()=>l,Am:()=>i});var o,a=r(751995),s=r(804591);e=r.hmd(e),(o="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.enterModule:void 0)&&o(e),"undefined"!=typeof reactHotLoaderGlobal&&reactHotLoaderGlobal.default.signature;const n=a.iK.div`
  min-height: ${({height:e})=>e}px;
  width: ${({width:e})=>e}px;
`,l=(0,a.iK)(s.Z)`
  &.ant-row.ant-form-item {
    margin: 0;
  }
`,i=a.iK.div`
  color: ${({theme:e,status:t="error"})=>{var r;return null==(r=e.colors[t])?void 0:r.base}};
`;var d,u;(d="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.default:void 0)&&(d.register(n,"FilterPluginStyle","/Users/chenming/superset/superset-frontend/src/filters/components/common.ts"),d.register(l,"StyledFormItem","/Users/chenming/superset/superset-frontend/src/filters/components/common.ts"),d.register(i,"StatusMessage","/Users/chenming/superset/superset-frontend/src/filters/components/common.ts")),(u="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.leaveModule:void 0)&&u(e)}}]);
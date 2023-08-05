"use strict";(globalThis.webpackChunksuperset=globalThis.webpackChunksuperset||[]).push([[6962],{739883:(e,t,o)=>{o.d(t,{m:()=>d}),o(667294);var a,r,n,l=o(294184),i=o.n(l),s=o(211965);function d({disabled:e,onClick:t}){return(0,s.tZ)("li",{className:i()({disabled:e})},(0,s.tZ)("span",{role:"button",tabIndex:e?-1:0,onClick:o=>{o.preventDefault(),e||t(o)}},"…"))}e=o.hmd(e),(a="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.enterModule:void 0)&&a(e),"undefined"!=typeof reactHotLoaderGlobal&&reactHotLoaderGlobal.default.signature,(r="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.default:void 0)&&r.register(d,"Ellipsis","/Users/chenming/superset/superset-frontend/src/components/Pagination/Ellipsis.tsx"),(n="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.leaveModule:void 0)&&n(e)},676638:(e,t,o)=>{o.d(t,{c:()=>d}),o(667294);var a,r,n,l=o(294184),i=o.n(l),s=o(211965);function d({active:e,children:t,onClick:o}){return(0,s.tZ)("li",{className:i()({active:e})},(0,s.tZ)("span",{role:"button",tabIndex:e?-1:0,onClick:t=>{t.preventDefault(),e||o(t)}},t))}e=o.hmd(e),(a="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.enterModule:void 0)&&a(e),"undefined"!=typeof reactHotLoaderGlobal&&reactHotLoaderGlobal.default.signature,(r="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.default:void 0)&&r.register(d,"Item","/Users/chenming/superset/superset-frontend/src/components/Pagination/Item.tsx"),(n="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.leaveModule:void 0)&&n(e)},639292:(e,t,o)=>{o.d(t,{o:()=>d}),o(667294);var a,r,n,l=o(294184),i=o.n(l),s=o(211965);function d({disabled:e,onClick:t}){return(0,s.tZ)("li",{className:i()({disabled:e})},(0,s.tZ)("span",{role:"button",tabIndex:e?-1:0,onClick:o=>{o.preventDefault(),e||t(o)}},"»"))}e=o.hmd(e),(a="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.enterModule:void 0)&&a(e),"undefined"!=typeof reactHotLoaderGlobal&&reactHotLoaderGlobal.default.signature,(r="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.default:void 0)&&r.register(d,"Next","/Users/chenming/superset/superset-frontend/src/components/Pagination/Next.tsx"),(n="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.leaveModule:void 0)&&n(e)},400535:(e,t,o)=>{o.d(t,{O:()=>d}),o(667294);var a,r,n,l=o(294184),i=o.n(l),s=o(211965);function d({disabled:e,onClick:t}){return(0,s.tZ)("li",{className:i()({disabled:e})},(0,s.tZ)("span",{role:"button",tabIndex:e?-1:0,onClick:o=>{o.preventDefault(),e||t(o)}},"«"))}e=o.hmd(e),(a="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.enterModule:void 0)&&a(e),"undefined"!=typeof reactHotLoaderGlobal&&reactHotLoaderGlobal.default.signature,(r="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.default:void 0)&&r.register(d,"Prev","/Users/chenming/superset/superset-frontend/src/components/Pagination/Prev.tsx"),(n="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.leaveModule:void 0)&&n(e)},329623:(e,t,o)=>{o.d(t,{Z:()=>g}),o(667294);var a,r=o(751995),n=o(639292),l=o(400535),i=o(676638),s=o(739883),d=o(211965);e=o.hmd(e),(a="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.enterModule:void 0)&&a(e),"undefined"!=typeof reactHotLoaderGlobal&&reactHotLoaderGlobal.default.signature;const c=r.iK.ul`
  display: inline-block;
  margin: 16px 0;
  padding: 0;

  li {
    display: inline;
    margin: 0 4px;

    span {
      padding: 8px 12px;
      text-decoration: none;
      background-color: ${({theme:e})=>e.colors.grayscale.light5};
      border-radius: ${({theme:e})=>e.borderRadius}px;

      &:hover,
      &:focus {
        z-index: 2;
        color: ${({theme:e})=>e.colors.grayscale.dark1};
        background-color: ${({theme:e})=>e.colors.grayscale.light3};
      }
    }

    &.disabled {
      span {
        background-color: transparent;
        cursor: default;

        &:focus {
          outline: none;
        }
      }
    }
    &.active {
      span {
        z-index: 3;
        color: ${({theme:e})=>e.colors.grayscale.light5};
        cursor: default;
        background-color: ${({theme:e})=>e.colors.primary.base};

        &:focus {
          outline: none;
        }
      }
    }
  }
`;function p({children:e}){return(0,d.tZ)(c,{role:"navigation"},e)}p.Next=n.o,p.Prev=l.O,p.Item=i.c,p.Ellipsis=s.m;const u=p,g=u;var b,m;(b="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.default:void 0)&&(b.register(c,"PaginationList","/Users/chenming/superset/superset-frontend/src/components/Pagination/Wrapper.tsx"),b.register(p,"Pagination","/Users/chenming/superset/superset-frontend/src/components/Pagination/Wrapper.tsx"),b.register(u,"default","/Users/chenming/superset/superset-frontend/src/components/Pagination/Wrapper.tsx")),(m="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.leaveModule:void 0)&&m(e)},212591:(e,t,o)=>{o.d(t,{Z:()=>d}),o(667294);var a,r=o(329623),n=o(452630),l=o(211965);e=o.hmd(e),(a="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.enterModule:void 0)&&a(e),"undefined"!=typeof reactHotLoaderGlobal&&reactHotLoaderGlobal.default.signature;const i=(0,n.YM)({WrapperComponent:r.Z,itemTypeToComponent:{[n.iB.PAGE]:({value:e,isActive:t,onClick:o})=>(0,l.tZ)(r.Z.Item,{active:t,onClick:o},e),[n.iB.ELLIPSIS]:({isActive:e,onClick:t})=>(0,l.tZ)(r.Z.Ellipsis,{disabled:e,onClick:t}),[n.iB.PREVIOUS_PAGE_LINK]:({isActive:e,onClick:t})=>(0,l.tZ)(r.Z.Prev,{disabled:e,onClick:t}),[n.iB.NEXT_PAGE_LINK]:({isActive:e,onClick:t})=>(0,l.tZ)(r.Z.Next,{disabled:e,onClick:t}),[n.iB.FIRST_PAGE_LINK]:()=>null,[n.iB.LAST_PAGE_LINK]:()=>null}}),s=i,d=s;var c,p;(c="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.default:void 0)&&(c.register(i,"ListViewPagination","/Users/chenming/superset/superset-frontend/src/components/Pagination/index.tsx"),c.register(s,"default","/Users/chenming/superset/superset-frontend/src/components/Pagination/index.tsx")),(p="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.leaveModule:void 0)&&p(e)},397754:(e,t,o)=>{o.d(t,{Z:()=>b});var a,r=o(205872),n=o.n(r),l=o(667294),i=o(294184),s=o.n(i),d=o(751995),c=o(87693),p=o(211965);e=o.hmd(e),(a="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.enterModule:void 0)&&a(e),"undefined"!=typeof reactHotLoaderGlobal&&reactHotLoaderGlobal.default.signature;const u=d.iK.table`
  background-color: ${({theme:e})=>e.colors.grayscale.light5};
  border-collapse: separate;
  border-radius: ${({theme:e})=>e.borderRadius}px;

  thead > tr > th {
    border: 0;
  }

  tbody {
    tr:first-of-type > td {
      border-top: 0;
    }
  }
  th {
    background: ${({theme:e})=>e.colors.grayscale.light5};
    position: sticky;
    top: 0;

    &:first-of-type {
      padding-left: ${({theme:e})=>4*e.gridUnit}px;
    }

    &.xs {
      min-width: 25px;
    }
    &.sm {
      min-width: 50px;
    }
    &.md {
      min-width: 75px;
    }
    &.lg {
      min-width: 100px;
    }
    &.xl {
      min-width: 150px;
    }
    &.xxl {
      min-width: 200px;
    }

    span {
      white-space: nowrap;
      display: flex;
      align-items: center;
      line-height: 2;
    }

    svg {
      display: inline-block;
      position: relative;
    }
  }

  td {
    &.xs {
      width: 25px;
    }
    &.sm {
      width: 50px;
    }
    &.md {
      width: 75px;
    }
    &.lg {
      width: 100px;
    }
    &.xl {
      width: 150px;
    }
    &.xxl {
      width: 200px;
    }
  }

  .table-cell-loader {
    position: relative;

    .loading-bar {
      background-color: ${({theme:e})=>e.colors.secondary.light4};
      border-radius: 7px;

      span {
        visibility: hidden;
      }
    }

    .empty-loading-bar {
      display: inline-block;
      width: 100%;
      height: 1.2em;
    }

    &:after {
      position: absolute;
      transform: translateY(-50%);
      top: 50%;
      left: 0;
      content: '';
      display: block;
      width: 100%;
      height: 48px;
      background-image: linear-gradient(
        100deg,
        rgba(255, 255, 255, 0),
        rgba(255, 255, 255, 0.5) 60%,
        rgba(255, 255, 255, 0) 80%
      );
      background-size: 200px 48px;
      background-position: -100px 0;
      background-repeat: no-repeat;
      animation: loading-shimmer 1s infinite;
    }
  }

  .actions {
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
  }

  .table-row {
    .actions {
      opacity: 0;
      font-size: ${({theme:e})=>e.typography.sizes.xl}px;
    }

    &:hover {
      background-color: ${({theme:e})=>e.colors.secondary.light5};

      .actions {
        opacity: 1;
        transition: opacity ease-in ${({theme:e})=>e.transitionTiming}s;
      }
    }
  }

  .table-row-selected {
    background-color: ${({theme:e})=>e.colors.secondary.light4};

    &:hover {
      background-color: ${({theme:e})=>e.colors.secondary.light4};
    }
  }

  .table-cell {
    text-overflow: ellipsis;
    overflow: hidden;
    max-width: 320px;
    line-height: 1;
    vertical-align: middle;
    &:first-of-type {
      padding-left: ${({theme:e})=>4*e.gridUnit}px;
    }
    &__wrap {
      white-space: normal;
    }
    &__nowrap {
      white-space: nowrap;
    }
  }

  @keyframes loading-shimmer {
    40% {
      background-position: 100% 0;
    }

    100% {
      background-position: 100% 0;
    }
  }
`;u.displayName="table";const g=l.memo((({getTableProps:e,getTableBodyProps:t,prepareRow:o,headerGroups:a,columns:r,rows:l,loading:i,highlightRowId:d,columnsForWrapText:g})=>(0,p.tZ)(u,n()({},e(),{className:"table table-hover","data-test":"listview-table"}),(0,p.tZ)("thead",null,a.map((e=>(0,p.tZ)("tr",e.getHeaderGroupProps(),e.headers.map((e=>{let t=(0,p.tZ)(c.Z.Sort,null);return e.isSorted&&e.isSortedDesc?t=(0,p.tZ)(c.Z.SortDesc,null):e.isSorted&&!e.isSortedDesc&&(t=(0,p.tZ)(c.Z.SortAsc,null)),e.hidden?null:(0,p.tZ)("th",n()({},e.getHeaderProps(e.canSort?e.getSortByToggleProps():{}),{"data-test":"sort-header",className:s()({[e.size||""]:e.size})}),(0,p.tZ)("span",null,e.render("Header"),e.canSort&&t))})))))),(0,p.tZ)("tbody",t(),i&&0===l.length&&[...new Array(12)].map(((e,t)=>(0,p.tZ)("tr",{key:t},r.map(((e,t)=>e.hidden?null:(0,p.tZ)("td",{key:t,className:s()("table-cell",{"table-cell-loader":i})},(0,p.tZ)("span",{className:"loading-bar empty-loading-bar",role:"progressbar","aria-label":"loading"}))))))),l.length>0&&l.map((e=>{o(e);const t=e.original.id;return(0,p.tZ)("tr",n()({"data-test":"table-row"},e.getRowProps(),{className:s()("table-row",{"table-row-selected":e.isSelected||void 0!==t&&t===d})}),e.cells.map((e=>{if(e.column.hidden)return null;const t=e.column.cellProps||{},o=g&&g.includes(e.column.Header);return(0,p.tZ)("td",n()({"data-test":"table-row-cell",className:s()("table-cell table-cell__"+(o?"wrap":"nowrap"),{"table-cell-loader":i,[e.column.size||""]:e.column.size})},e.getCellProps(),t),(0,p.tZ)("span",{className:s()({"loading-bar":i}),role:i?"progressbar":void 0},(0,p.tZ)("span",{"data-test":"cell-text"},e.render("Cell"))))})))})))))),b=g;var m,f;(m="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.default:void 0)&&(m.register(u,"Table","/Users/chenming/superset/superset-frontend/src/components/TableCollection/index.tsx"),m.register(g,"default","/Users/chenming/superset/superset-frontend/src/components/TableCollection/index.tsx")),(f="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.leaveModule:void 0)&&f(e)},946977:(e,t,o)=>{o.d(t,{u:()=>b,Z:()=>L});var a,r=o(667294),n=o(618446),l=o.n(n),i=o(751995),s=o(455867),d=o(379521),c=o(104715),p=o(212591),u=o(397754),g=o(211965);e=o.hmd(e),(a="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.enterModule:void 0)&&a(e);var b,m="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.default.signature:function(e){return e};!function(e){e.Default="Default",e.Small="Small"}(b||(b={}));const f=i.iK.div`
  margin: ${({theme:e})=>40*e.gridUnit}px 0;
`,h=i.iK.div`
  ${({scrollTable:e,theme:t})=>e&&`\n    flex: 1 1 auto;\n    margin-bottom: ${4*t.gridUnit}px;\n    overflow: auto;\n  `}

  .table-row {
    ${({theme:e,small:t})=>!t&&`height: ${11*e.gridUnit-1}px;`}

    .table-cell {
      ${({theme:e,small:t})=>t&&`\n        padding-top: ${e.gridUnit+1}px;\n        padding-bottom: ${e.gridUnit+1}px;\n        line-height: 1.45;\n      `}
    }
  }

  th[role='columnheader'] {
    z-index: 1;
    border-bottom: ${({theme:e})=>`${e.gridUnit-2}px solid ${e.colors.grayscale.light2}`};
    ${({small:e})=>e&&"padding-bottom: 0;"}
  }
`,y=i.iK.div`
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background-color: ${({theme:e})=>e.colors.grayscale.light5};

  ${({isPaginationSticky:e})=>e&&"\n        position: sticky;\n        bottom: 0;\n        left: 0;\n    "};

  .row-count-container {
    margin-top: ${({theme:e})=>2*e.gridUnit}px;
    color: ${({theme:e})=>e.colors.grayscale.base};
  }
`,x=({columns:e,data:t,pageSize:o,totalCount:a=t.length,initialPageIndex:n,initialSortBy:i=[],loading:m=!1,withPagination:x=!0,emptyWrapperType:v=b.Default,noDataText:L,showRowCount:G=!0,serverPagination:w=!1,columnsForWrapText:H,onServerPagination:P=(()=>{}),...Z})=>{const k={pageSize:null!=o?o:10,pageIndex:null!=n?n:0,sortBy:i},{getTableProps:T,getTableBodyProps:S,headerGroups:$,page:E,rows:C,prepareRow:I,pageCount:U,gotoPage:N,state:{pageIndex:M,pageSize:_,sortBy:B}}=(0,d.useTable)({columns:e,data:t,initialState:k,manualPagination:w,manualSortBy:w,pageCount:Math.ceil(a/k.pageSize)},d.useFilters,d.useSortBy,d.usePagination);(0,r.useEffect)((()=>{w&&M!==k.pageIndex&&P({pageIndex:M})}),[M]),(0,r.useEffect)((()=>{w&&!l()(B,k.sortBy)&&P({pageIndex:0,sortBy:B})}),[B]);const V=x?E:C;let A;switch(v){case b.Small:A=({children:e})=>(0,g.tZ)(r.Fragment,null,e);break;case b.Default:default:A=({children:e})=>(0,g.tZ)(f,null,e)}const z=!m&&0===V.length,D=U>1&&x;return(0,g.tZ)(r.Fragment,null,(0,g.tZ)(h,Z,(0,g.tZ)(u.Z,{getTableProps:T,getTableBodyProps:S,prepareRow:I,headerGroups:$,rows:V,columns:e,loading:m,columnsForWrapText:H}),z&&(0,g.tZ)(A,null,L?(0,g.tZ)(c.HY,{image:c.HY.PRESENTED_IMAGE_SIMPLE,description:L}):(0,g.tZ)(c.HY,{image:c.HY.PRESENTED_IMAGE_SIMPLE}))),D&&(0,g.tZ)(y,{className:"pagination-container",isPaginationSticky:Z.isPaginationSticky},(0,g.tZ)(p.Z,{totalPages:U||0,currentPage:U?M+1:0,onChange:e=>N(e-1),hideFirstAndLastPageLinks:!0}),G&&(0,g.tZ)("div",{className:"row-count-container"},!m&&(0,s.t)("%s-%s of %s",_*M+(E.length&&1),_*M+E.length,a))))};m(x,"useTable{{ getTableProps, getTableBodyProps, headerGroups, page, rows, prepareRow, pageCount, gotoPage, state: { pageIndex, pageSize, sortBy }, }}\nuseEffect{}\nuseEffect{}",(()=>[d.useTable]));const v=r.memo(x),L=v;var G,w;(G="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.default:void 0)&&(G.register(10,"DEFAULT_PAGE_SIZE","/Users/chenming/superset/superset-frontend/src/components/TableView/TableView.tsx"),G.register(b,"EmptyWrapperType","/Users/chenming/superset/superset-frontend/src/components/TableView/TableView.tsx"),G.register(f,"EmptyWrapper","/Users/chenming/superset/superset-frontend/src/components/TableView/TableView.tsx"),G.register(h,"TableViewStyles","/Users/chenming/superset/superset-frontend/src/components/TableView/TableView.tsx"),G.register(y,"PaginationStyles","/Users/chenming/superset/superset-frontend/src/components/TableView/TableView.tsx"),G.register(x,"TableView","/Users/chenming/superset/superset-frontend/src/components/TableView/TableView.tsx"),G.register(v,"default","/Users/chenming/superset/superset-frontend/src/components/TableView/TableView.tsx")),(w="undefined"!=typeof reactHotLoaderGlobal?reactHotLoaderGlobal.leaveModule:void 0)&&w(e)},676962:(e,t,o)=>{o.d(t,{u:()=>a.u,Z:()=>a.Z});var a=o(946977);"undefined"!=typeof reactHotLoaderGlobal&&reactHotLoaderGlobal.default.signature}}]);
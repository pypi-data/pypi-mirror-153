/*! For license information please see dagDependencies.cf2378fbd03d4e8cb622.js.LICENSE.txt */
!function(e,t){"object"==typeof exports&&"object"==typeof module?module.exports=t():"function"==typeof define&&define.amd?define([],t):"object"==typeof exports?exports.dagDependencies=t():(e.Airflow=e.Airflow||{},e.Airflow.dagDependencies=t())}(window,(function(){return function(e){var t={};function n(l){if(t[l])return t[l].exports;var r=t[l]={i:l,l:!1,exports:{}};return e[l].call(r.exports,r,r.exports,n),r.l=!0,r.exports}return n.m=e,n.c=t,n.d=function(e,t,l){n.o(e,t)||Object.defineProperty(e,t,{enumerable:!0,get:l})},n.r=function(e){"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},n.t=function(e,t){if(1&t&&(e=n(e)),8&t)return e;if(4&t&&"object"==typeof e&&e&&e.__esModule)return e;var l=Object.create(null);if(n.r(l),Object.defineProperty(l,"default",{enumerable:!0,value:e}),2&t&&"string"!=typeof e)for(var r in e)n.d(l,r,function(t){return e[t]}.bind(null,r));return l},n.n=function(e){var t=e&&e.__esModule?function(){return e.default}:function(){return e};return n.d(t,"a",t),t},n.o=function(e,t){return Object.prototype.hasOwnProperty.call(e,t)},n.p="",n(n.s=101)}({101:function(e,t){const n="3px",l="5px",r=500;let s=dagNodes;const o=s,c=s.filter((e=>edges.some((t=>t.u===e.id||t.v===e.id))));let a=(new dagreD3.graphlib.Graph).setGraph({nodesep:15,ranksep:15,rankdir:arrange}).setDefaultEdgeLabel((()=>({lineInterpolate:"basis"})));const d=dagreD3.render(),i=d3.select("#graph-svg"),u=d3.select("#graph-svg g");function f(e,t,n){e.forEach((e=>{const l=a.node(e).elem;d3.select(l).selectAll("rect,circle").style("stroke",t).style("stroke-width",n)}))}let p=null;d3.select("#searchbox").on("keyup",(()=>{!function(e){let t=null;if(d3.selectAll("g.nodes g.node").filter((function(s){var o;return""===e?(d3.select("g.edgePaths").transition().duration(r).style("opacity",1),d3.select(this).transition().duration(r).style("opacity",1).selectAll("rect").style("stroke-width",n)):(d3.select("g.edgePaths").transition().duration(r).style("opacity",.2),o=e,s.indexOf(o)>-1?(t||(t=this),d3.select(this).transition().duration(r).style("opacity",1).selectAll("rect").style("stroke-width",l)):d3.select(this).transition().style("opacity",.2).duration(r).selectAll("rect").style("stroke-width",n)),null})),t){const e=d3.transform(d3.select(t).attr("transform")),n=i.node().getBoundingClientRect();e.translate=[n.width/2-e.translate[0],n.height/2-e.translate[1]],e.scale=[1,1],null!==p&&(p.translate(e.translate),p.scale(1),p.event(u))}}(document.getElementById("searchbox").value)}));const g=()=>{a=(new dagreD3.graphlib.Graph).setGraph({nodesep:15,ranksep:15,rankdir:arrange}).setDefaultEdgeLabel((()=>({lineInterpolate:"basis"}))),s.forEach((e=>{a.setNode(e.id,e.value)})),edges.forEach((e=>{a.setEdge(e.u,e.v,{curve:d3.curveBasis,arrowheadClass:"arrowhead"})})),u.call(d,a),function(e=null){d3.selectAll("g.node").on("mouseover",(function(e){d3.select(this).selectAll("rect").style("stroke","#000000"),f(a.predecessors(e),"#2020A0",l),f(a.successors(e),"#0000FF",l);const t=[e,...a.predecessors(e),...a.successors(e)];d3.selectAll("g.nodes g.node").filter((e=>!t.includes(e))).style("opacity",.2);const n=a.nodeEdges(e);d3.selectAll("g.edgePath")[0].filter((e=>!n.includes(e.__data__))).forEach((e=>{d3.select(e).style("opacity",.2)}))})),d3.selectAll("g.node").on("mouseout",(function(t){d3.select(this).selectAll("rect,circle").style("stroke",null),f(a.predecessors(t),null,n),f(a.successors(t),null,n),d3.selectAll("g.node").style("opacity",1),d3.selectAll("g.node rect").style("stroke-width",n),d3.selectAll("g.edgePath").style("opacity",1),e&&localStorage.removeItem(e)}))}(),function(){p=d3.behavior.zoom().on("zoom",(()=>{u.attr("transform",`translate(${d3.event.translate})scale(${d3.event.scale})`)})),i.call(p);const e=a.graph().width,t=a.graph().height,n=i.node().getBoundingClientRect(),l=n.width-40,r=n.height-20,s=Math.min(Math.min(l/e,r/t),1.5);p.translate([l/2-e*s/2+20,20]),p.scale(s),p.event(u)}()};document.getElementById("deps-filter").addEventListener("change",(function(){document.getElementById("searchbox").value="",s=this.checked?c:o,g()})),document.getElementById("deps-filter").checked&&(s=c),g()}})}));
(this["webpackJsonptime-table"]=this["webpackJsonptime-table"]||[]).push([[0],{144:function(e,a,t){e.exports=t(296)},149:function(e,a,t){},150:function(e,a,t){e.exports=t.p+"static/media/logo.5d5d9eef.svg"},151:function(e,a,t){},152:function(e,a,t){},296:function(e,a,t){"use strict";t.r(a);var n=t(0),r=t.n(n),l=t(8),s=t.n(l),c=(t(149),t(150),t(151),t(60)),o=t(61),i=t(69),m=t(63),u=t(70),d=(t(152),function(e){return r.a.createElement(r.a.Fragment,null,Object.keys(e.cname).map((function(a,t){return r.a.createElement("td",{className:e.main_json.times[t]},e.cname[e.main_json.times[t]].subject)})))}),p=function(e){return void 0==e.main_json?r.a.createElement("div",null):r.a.createElement("div",null,Object.keys(e.main_json.time_table).map((function(a){return r.a.createElement("table",{className:a},r.a.createElement("tr",null,r.a.createElement("td",null,a),e.main_json.times.map((function(e){return r.a.createElement("td",null,e)}))),e.main_json.days.map((function(t){return r.a.createElement("tr",null,r.a.createElement("td",null,t),r.a.createElement(d,{main_json:e.main_json,cname:e.main_json.time_table[a][t]}))})))})))},E=function(e){function a(){return Object(c.a)(this,a),Object(i.a)(this,Object(m.a)(a).apply(this,arguments))}return Object(u.a)(a,e),Object(o.a)(a,[{key:"super",value:function(e){this.props=e}},{key:"render",value:function(){return r.a.createElement("div",{style:{left:"20%",position:"relative"}},r.a.createElement(p,{main_json:this.props.main_json}),r.a.createElement("br",null))}}]),a}(r.a.Component),y=t(48),h=t(62),f=t(304),b=t(305),j=t(306),v=t(124),g=(t(153),t(302)),_=t(301),O=t(303),S=t(95),C=t(299),w=t(300),k=g.a.Option,T={labelCol:{span:8},wrapperCol:{span:8}},I={labelCol:{xs:{span:8},sm:{span:8}},wrapperCol:{xs:{span:8},sm:{span:8}}},D=["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"],x={wrapperCol:{xs:{span:8,offset:8},sm:{span:8,offset:8}}},N=function(){return r.a.createElement(_.a.List,{name:"names"},(function(e,a){var t=a.add,n=a.remove;return r.a.createElement("div",null,e.map((function(a,t){return r.a.createElement(_.a.Item,Object.assign({},0===t?I:x,{label:0===t?"Subject":"",required:!1,key:a.key}),r.a.createElement(_.a.Item,Object.assign({},a,{validateTrigger:["onChange","onBlur"],rules:[{required:!0,whitespace:!0,message:"Enter the Subjects"}],noStyle:!0}),r.a.createElement(O.a,{name:"subject",placeholder:"subject",style:{width:"60%"}})),e.length>1?r.a.createElement(b.a,{className:"dynamic-delete-button",style:{margin:"0 8px"},onClick:function(){n(a.name)}}):null)})),r.a.createElement(_.a.Item,x,r.a.createElement(S.a,{type:"dashed",onClick:function(){t()}},r.a.createElement(j.a,null)," Add Subjects")))}))},F=function(e){function a(e){var t;return Object(c.a)(this,a),(t=Object(i.a)(this,Object(m.a)(a).call(this,e))).state={main_json:void 0,no_sections:0,no_subjects:0,percentage:0},t.sendData=t.sendData.bind(Object(h.a)(t)),t}return Object(u.a)(a,e),Object(o.a)(a,[{key:"sendData",value:function(e){var a=this,t={method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(e)},n=0,r=setInterval((function(){a.setState({percentage:n}),n+=2}),1e3);fetch("/generate",t).then((function(e){return console.log(e),clearInterval(r),a.setState({percentage:100}),e.json()})).then((function(e){return a.setState({main_json:e,percentage:100})}))}},{key:"render",value:function(){var e=this;return r.a.createElement("div",null,r.a.createElement(_.a,Object.assign({},T,{name:"basic",initialValues:{remember:!0},onFinish:function(a){for(var t=[],n=1;n<=a.noClass;n++)t.push(n);for(var r=[],l=[],s=0;s<a.noSec;s++){var c,o={};console.log(a["Teachers"+s]),(c=r).push.apply(c,Object(y.a)(a["Teachers"+s].split(","))),a["Teachers"+s].split(",").forEach((function(e,t){o[a.names[t]]=e})),o.enpty="-",l.push(o)}r=Object(y.a)(new Set(r));var i=Object(y.a)(Array(a.noSec).keys());var m={no_classes:a.noClass,no_days:a.noDays,days_list:function(e,a){for(var t=[],n=0,r=e;n<a;n++,r++)r<7?t.push(D[r]):t.push(D[r-7]);return t}(D.indexOf(a.startClass),a.noDays),rooms:i,time_list:t,subject_list:a.names,teacher_list:r,student_groups:l};console.log(m),e.sendData(m)}}),r.a.createElement(C.a,{justify:"center"},r.a.createElement(w.a,{span:6},r.a.createElement(_.a.Item,{name:"noDays",label:"No of Days"},r.a.createElement(f.a,null))),r.a.createElement(w.a,{span:6},r.a.createElement(_.a.Item,{name:"startClass",label:"Start Day",rules:[{required:!0}]},r.a.createElement(g.a,{style:{width:"100%"},placeholder:"Select a Day",allowClear:!0},r.a.createElement(k,{value:"Sunday"},"Sunday"),r.a.createElement(k,{value:"Monday"},"Monday"),r.a.createElement(k,{value:"Tuesday"},"Tuesday"),r.a.createElement(k,{value:"Wednesday"},"Wednesday"),r.a.createElement(k,{value:"Thursday"},"Thursday"),r.a.createElement(k,{value:"Friday"},"Friday"),r.a.createElement(k,{value:"Saturday"},"Saturday"))))),r.a.createElement(C.a,{justify:"center"},r.a.createElement(w.a,{span:6},r.a.createElement(_.a.Item,{name:"noSec",label:"No of Sections"},r.a.createElement(f.a,{onChange:function(a){e.setState({no_sections:a})}}))),r.a.createElement(w.a,{span:6},r.a.createElement(_.a.Item,{name:"noClass",label:"No of Classes/week:"},r.a.createElement(f.a,null)))),r.a.createElement(C.a,null,r.a.createElement(w.a,{offset:8,span:8},r.a.createElement(N,null))),Object(y.a)(Array(this.state.no_sections)).map((function(e,a){return r.a.createElement(C.a,{key:a,justify:"center"},r.a.createElement(w.a,null,r.a.createElement(_.a.Item,{name:"Teachers"+a,label:"Enter the names of teachers of "+a+" section seprated by comma(,)"},r.a.createElement(O.a,{placeholder:"The names should be in the same order as the subjects entered"}))))})),r.a.createElement(C.a,{justify:"center"},r.a.createElement(w.a,{span:1},r.a.createElement(_.a.Item,null,r.a.createElement(S.a,{type:"primary",htmlType:"submit"},"Submit"))))),r.a.createElement("div",{style:{width:"5%",margin:"auto"}},r.a.createElement(v.a,{value:this.state.percentage,text:"".concat(this.state.percentage,"%")})),r.a.createElement("br",null),r.a.createElement(E,{main_json:this.state.main_json}))}}]),a}(r.a.Component);var W=function(){return r.a.createElement("div",{className:"App"},r.a.createElement("br",null),r.a.createElement(F,null))};Boolean("localhost"===window.location.hostname||"[::1]"===window.location.hostname||window.location.hostname.match(/^127(?:\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}$/));s.a.render(r.a.createElement(W,null),document.getElementById("root")),"serviceWorker"in navigator&&navigator.serviceWorker.ready.then((function(e){e.unregister()})).catch((function(e){console.error(e.message)}))}},[[144,1,2]]]);
//# sourceMappingURL=main.7dc43f15.chunk.js.map
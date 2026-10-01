const demoData={events:[{id:"ev-1",title:"Illustrative event",lat:0,lon:0,status:"confirmed",source:"demo"}],entities:[{id:"ent-1",name:"Illustrative entity",type:"organization"}],changes:[{id:"ch-1",subject:"ent-1",type:"modified",significance:0.7}],signals:[{id:"sig-1",severity:"medium",explanation:"Illustrative signal; production data comes from the Intelligence API."}],evidence:{status:"No evidence selected"},provenance:{status:"Select an intelligence object to inspect its provenance."}};
let data={events:[],entities:[],changes:[],signals:[],evidence:{status:"No evidence selected"},provenance:{status:"No provenance selected"}};
const state={view:"map",search:"",severity:"",selected:null,live:false};
const views=[...document.querySelectorAll(".view")];
function show(view){state.view=view;views.forEach(v=>v.classList.toggle("active",v.id===view));document.querySelectorAll("[data-view]").forEach(b=>b.setAttribute("aria-current",b.dataset.view===view?"page":"false"))}
document.querySelectorAll("button[data-view]").forEach(b=>b.addEventListener("click",()=>show(b.dataset.view)));
function matches(row){const text=JSON.stringify(row).toLowerCase();return (!state.search||text.includes(state.search.toLowerCase()))&&(!state.severity||row.severity===state.severity)}
function inspect(row){state.selected=row;const target=document.getElementById("inspector");target.replaceChildren();const h=document.createElement("h2");h.textContent="Inspector";const pre=document.createElement("pre");pre.textContent=JSON.stringify(row,null,2);target.append(h,pre)}
function renderList(id,rows){const target=document.getElementById(id);target.replaceChildren();rows.filter(matches).forEach(row=>{const article=document.createElement("article");article.className="card";const button=document.createElement("button");button.textContent=String(row.title||row.name||row.id);button.addEventListener("click",()=>inspect(row));const pre=document.createElement("pre");pre.textContent=JSON.stringify(row,null,2);article.append(button,pre);target.append(article)})}
function render(){
 renderList("event-list",data.events);renderList("entity-list",data.entities);renderList("change-list",data.changes);renderList("signal-list",data.signals);
 document.getElementById("evidence-view").textContent=JSON.stringify(data.evidence,null,2);document.getElementById("provenance-view").textContent=JSON.stringify(data.provenance,null,2);
 document.getElementById("source-health").textContent=state.live?"Intelligence API: connected · canonical data":"No live Intelligence API configured · demo mode is explicit via ?demo=1";
 const markers=document.getElementById("markers");markers.replaceChildren();
 data.events.filter(matches).forEach(e=>{const circle=document.createElementNS("http://www.w3.org/2000/svg","circle");circle.setAttribute("cx",((e.lon+180)/360*1000).toFixed(2));circle.setAttribute("cy",((90-e.lat)/180*500).toFixed(2));circle.setAttribute("r","6");circle.setAttribute("aria-label",e.title);circle.addEventListener("click",()=>inspect(e));markers.append(circle)})
}
async function loadLiveData(){
 const config=window.WORLD_INTELLIGENCE_CONFIG||{};
 if(!config.apiBase)return false;
 const base=String(config.apiBase).replace(/\/$/,"");
 const headers={Accept:"application/json"};
 if(config.authorization)headers.Authorization=String(config.authorization);
 const resources=["events","entities","changes","signals"];
 const responses=await Promise.all(resources.map(async resource=>{const response=await fetch(base+"/v1/"+resource,{headers});if(!response.ok)throw new Error(resource+" "+response.status);return [resource,await response.json()]}));
 for(const [resource,payload] of responses)data[resource]=Array.isArray(payload.items)?payload.items:[];
 return true;
}
async function bootstrap(){
 const params=new URLSearchParams(location.search);
 if(params.get("demo")==="1"){data=structuredClone(demoData);state.live=false;render();return}
 try{state.live=await loadLiveData()}catch(error){state.live=false;document.getElementById("source-health").textContent="Intelligence API unavailable · no fallback to synthetic intelligence";console.warn("World Intelligence API unavailable",error)}
 render();
}
document.getElementById("search").addEventListener("input",e=>{state.search=e.target.value;render()});
document.getElementById("severity").addEventListener("change",e=>{state.severity=e.target.value;render()});
const saved=localStorage.getItem("twi-investigation");if(saved){try{const parsed=JSON.parse(saved);Object.assign(state,{search:parsed.search||"",severity:parsed.severity||"",view:parsed.view||"map"});document.getElementById("search").value=state.search;document.getElementById("severity").value=state.severity;show(state.view)}catch{}}
document.getElementById("save-investigation").addEventListener("click",()=>localStorage.setItem("twi-investigation",JSON.stringify({search:state.search,severity:state.severity,view:state.view})));
document.getElementById("clear-investigation").addEventListener("click",()=>{localStorage.removeItem("twi-investigation");state.search="";state.severity="";state.view="map";document.getElementById("search").value="";document.getElementById("severity").value="";show("map");render()});
document.getElementById("timeline-range").addEventListener("input",e=>document.getElementById("timeline-output").value=e.target.value+"%");
bootstrap();

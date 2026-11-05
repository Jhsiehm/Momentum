import {createLearningFlow} from './learning-flow.js';
import {createFirmFlow} from './firm-flow.js';
import {createIntelligenceFlow} from './intelligence-flow.js';
import {createResearchLab} from './research-lab.js';
import {mountBillContext} from './bill-context.js';
import {createConsumerFlow} from './consumer-flow.js';
import {createSampling} from './sampling-flow.js';
import {createAutoResearch} from './autoresearch-flow.js';
import {icon,mountIcons} from './icons.js';
import {createExplorer} from './explore.js';
import {createResearchFlow} from './research-flow.js';
import {workingMarkup,activityMarkup,mountWorkingVisuals,clearWorkingVisuals} from './work-visual.js';
const $=id=>document.getElementById(id);
const esc=value=>String(value??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const prose=value=>esc(value).replace(/^#{1,6}\s+(.+)$/gm,'<strong>$1</strong>').replace(/\*\*([^*\n]+)\*\*/g,'<strong>$1</strong>');
const pct=value=>value==null?'—':`${Math.round(value*100)}%`;
const stamp=value=>value?new Date(value).toLocaleString(undefined,{month:'short',day:'numeric',hour:'numeric',minute:'2-digit'}):'—';
const arrow=icon('arrowRight');
const mark=icon('workspace');
const state={page:'chat',chatId:null,chat:null,chats:[],dataset:'demo',sourceDataset:'official',runId:null,generation:0,chatGeneration:0,pendingSend:false,loadingChat:false,drafts:{},researchContext:null,contextDrafts:{},poll:null};
const explorer=createExplorer({api,$,esc,state,switchPage,navigate,error,toast,askContext:stageResearchContext,startResearch:collectionId=>flow.sessions({collection_id:collectionId})});
const samplingFlow=createSampling({api,$,esc,state,switchPage,navigate,error,toast});
const consumerFlow=createConsumerFlow({api,$,esc,state,switchPage,navigate,buttonPending,toast,error,structuredReport});
const learningFlow=createLearningFlow({api,$,esc,state,switchPage,navigate});
const autoResearch=createAutoResearch({api,$,esc,state,switchPage,buttonPending,error,toast,navigate,structuredReport});
const flow=createResearchFlow({api,$,esc,stamp,pct,state,switchPage,buttonPending,error,toast,navigate,structuredReport,showExperiment,showSources});
const researchLab=createResearchLab({api,$,esc,state,switchPage,navigate,buttonPending,toast,error,structuredReport});
const firmFlow=createFirmFlow({api,$,esc,state,switchPage,navigate});
const intelligenceFlow=createIntelligenceFlow({api,$,esc,state,switchPage,navigate});
let connection={configured:false,model:'OpenRouter'},toastTimer;
function error(text=''){$('global-error').textContent=text;$('global-error').hidden=!text;}
function toast(text){$('toast').textContent=text;$('toast').hidden=false;clearTimeout(toastTimer);toastTimer=setTimeout(()=>$('toast').hidden=true,4000);}
async function api(path,body){let response;try{response=await fetch('/api/'+path,body===undefined?{}:{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)});}catch{throw new Error('The local app is not responding. Open Start Workspace.command in the project folder, then try again.');}const value=await response.json();if(!response.ok)throw new Error(value.error||'Request failed. Try again.');return value;}
function buttonPending(button,pending,label){button.disabled=pending;if(label)button.textContent=label;}
function syncConnection(){ $('connection-dot').classList.toggle('connected',connection.configured);$('model-shortcut').textContent=connection.model.split('/').pop();$('model-shortcut').title=connection.model;}
function renderSidebar(){
  $('chat-list').innerHTML=state.chats.length?state.chats.map(chat=>`<button class="chat-item ${state.chatId===chat.id&&state.page==='chat'?'active':''}" data-chat="${esc(chat.id)}" title="${esc(chat.title)}">${esc(chat.title)}</button>`).join(''):'<p class="empty-chats">Your research starts here.</p>';
  document.querySelectorAll('[data-chat]').forEach(b=>b.onclick=()=>openChat(b.dataset.chat));
  const group=state.page==='firm'?'priorities':state.page==='intelligence'?'campaigns':['bill','explore','collections','sources'].includes(state.page)?'bills':['session','sessions','experiments','sample','data','autoresearch','rigor'].includes(state.page)?'campaigns':state.page;
  document.querySelectorAll('[data-page]').forEach(b=>{const active=b.dataset.page===group;b.classList.toggle('active',active);if(active)b.setAttribute('aria-current','page');else b.removeAttribute('aria-current');});
}
async function refreshChats(){state.chats=await api('chats');renderSidebar();}
function saveDraft(){state.drafts[state.chatId||'new']=$('prompt').value;if(state.page==='chat')state.contextDrafts[state.chatId||'new']=state.researchContext;}
function switchPage(page,title){clearWorkingVisuals();saveDraft();state.page=page;document.body.dataset.page=page;$('content-page').dataset.surface=page;state.generation++;error();clearTimeout(state.poll);$('chat-page').hidden=page!=='chat';$('content-page').hidden=['chat','replay','monitor'].includes(page);$('frame-page').hidden=!['replay','monitor'].includes(page);$('breadcrumb').textContent=title;document.body.classList.remove('sidebar-open');syncSidebar();renderSidebar();}
function pending(){return state.pendingSend||state.loadingChat||Boolean(state.chat?.messages.some(m=>m.status==='running'));}
function composerState(){const busy=pending();$('send').disabled=busy;$('prompt').disabled=busy;$('chat-dataset').disabled=busy||Boolean(state.researchContext);$('prompt').placeholder=busy?'Working on your request…':'Ask about your data, or run an experiment…';}
function welcome(){return `<div class="welcome"><div class="welcome-mark">${mark}</div><h1>What would you like to explore?</h1><p>Bring in a source, ask a question, or put an idea to the test. Your research stays connected.</p><div class="suggestions"><button data-suggestion="Show me the sources we have and explain what data is missing.">${arrow}Explore the source collection</button><button data-suggestion="Run a demo experiment for the 118th Congress at 180 days and show me the results.">${arrow}Run a historical forecasting experiment</button><button data-suggestion="Import H.R. 22 from the 119th Congress and show me its source record.">${arrow}Bring in an official bill</button><button data-start-sample>${icon('sample')}Create an audited sample</button></div></div>`;}
function artifactHtml(a){
  if(a.type==='experiment'){
    const bins=a.metrics?.reliability||[];
    return `<button class="artifact" data-artifact="${esc(JSON.stringify(a))}"><span class="artifact-head"><span>Experiment report</span>${arrow}</span><span class="artifact-meta">${esc(a.config?.dataset==='demo'?'Synthetic demo':'Official subset')} · Congress ${esc(a.config?.congress)} · ${esc(a.config?.age_days)}-day checkpoint<br>${esc(a.status)} · ${a.available??0}/${a.attempted??0} forecasts available${a.metrics?` · Brier ${a.metrics.brier.toFixed(3)}`:''}</span>${bins.length?`<span class="mini-bars" aria-label="Mean predicted probability by nonempty reliability bin">${bins.map(b=>`<i style="height:${Math.max(2,b.predicted*40)}px" title="Predicted ${pct(b.predicted)}; ${b.n} bills"></i>`).join('')}</span><span class="artifact-meta">Predicted probability by bin · Open for observed outcomes</span>`:''}</button>`;
  }
  return `<button class="artifact" data-artifact="${esc(JSON.stringify(a))}"><span class="artifact-head"><span>${esc(a.label)}</span>${arrow}</span></button>`;
}
function bindArtifacts(root){root.querySelectorAll('[data-artifact]').forEach(b=>b.onclick=()=>{const a=JSON.parse(b.dataset.artifact);if(a.type==='experiment')showExperiment(a.id);else if(a.type==='research_report')showResearchReport(a.id);else navigate(a.view,a);});}
function renderMessages(scroll=false){
  const target=$('messages');const nearBottom=target.scrollHeight-target.scrollTop-target.clientHeight<100;
  const messages=state.chat?.messages||[];
  target.innerHTML=messages.length?messages.map((m,index)=>`<article class="message ${esc(m.role)} ${esc(m.status)}">${m.role==='assistant'?`<div class="assistant-body"><div class="message-author">${mark}Research assistant</div>`:''}${m.role==='assistant'&&m.status==='running'?workingMarkup(m):`<div class="message-text">${m.role==='assistant'?prose(m.content):esc(m.content)}</div>`}${m.role==='assistant'?`${activityMarkup(m)}${m.artifacts.map(artifactHtml).join('')}${m.status==='failed'?`<button class="retry" data-retry="${index}">Retry this request</button>`:''}<div class="message-time">${stamp(m.created_at)}</div></div>`:''}</article>`).join(''):welcome();
  target.querySelectorAll('[data-suggestion]').forEach(b=>b.onclick=()=>{$('prompt').value=b.dataset.suggestion;$('prompt').focus();});
  target.querySelectorAll('[data-start-sample]').forEach(b=>b.onclick=()=>navigate('sample'));
  target.querySelectorAll('[data-retry]').forEach(b=>b.onclick=()=>{const index=Number(b.dataset.retry);const user=messages.slice(0,index).reverse().find(m=>m.role==='user');if(user){$('prompt').value=user.content;send();}});
  mountWorkingVisuals(target);bindArtifacts(target);composerState();if(scroll||nearBottom)target.scrollTop=target.scrollHeight;
}
async function openChat(id){
  saveDraft();const generation=++state.chatGeneration;switchPage('chat','Loading chat…');state.chatId=id;state.chat=null;state.researchContext=null;renderResearchContext();state.loadingChat=true;composerState();$('messages').innerHTML='<p class="page-empty">Loading your conversation…</p>';$('prompt').value=state.drafts[id]||'';
  try{const chat=await api('chat?id='+encodeURIComponent(id));if(generation!==state.chatGeneration||state.page!=='chat')return;state.chat=chat;state.researchContext=Object.prototype.hasOwnProperty.call(state.contextDrafts,id)?state.contextDrafts[id]:[...chat.messages].reverse().find(m=>m.role==='user')?.research_context||null;renderResearchContext();$('breadcrumb').textContent=chat.title;localStorage.setItem('research-last-chat',id);renderMessages(true);renderSidebar();scheduleChatPoll();}catch(e){if(generation===state.chatGeneration){error(e.message);$('messages').innerHTML='<p class="page-empty">Chat could not be loaded. Select it again to retry.</p>';}}finally{if(generation===state.chatGeneration){state.loadingChat=false;composerState();}}
}
async function createChat(){
  try{const chat=await api('chats',{});await refreshChats();await openChat(chat.id);$('prompt').focus();}catch(e){error(e.message);}
}
function scheduleChatPoll(){clearTimeout(state.poll);if(state.page==='chat'&&state.chat?.messages.some(m=>m.status==='running'))state.poll=setTimeout(pollChat,1200);}
async function pollChat(){const id=state.chatId,generation=state.chatGeneration;try{const chat=await api('chat?id='+encodeURIComponent(id));if(id!==state.chatId||generation!==state.chatGeneration||state.page!=='chat')return;const changed=JSON.stringify(chat.messages)!==JSON.stringify(state.chat?.messages);state.chat=chat;if(changed)renderMessages();scheduleChatPoll();}catch(e){if(id===state.chatId&&state.page==='chat'){error(e.message);state.poll=setTimeout(pollChat,4000);}}}
async function send(){
  const text=$('prompt').value.trim();if(!text||pending())return;error();state.pendingSend=true;composerState();
  const generation=++state.chatGeneration, originalId=state.chatId;
  let id=originalId;
  try{
    if(!id){const chat=await api('chats',{});id=chat.id;if(generation===state.chatGeneration&&state.page==='chat'&&state.chatId===originalId){state.chatId=id;state.chat=chat;localStorage.setItem('research-last-chat',id);}}
    const result=await api('chat/send',{chat_id:id,message:text,dataset:$('chat-dataset').value,request_id:crypto.randomUUID(),research_context:state.researchContext});
    if(state.drafts[id]===text)state.drafts[id]='';if(!originalId&&state.drafts.new===text)state.drafts.new='';
    if(generation===state.chatGeneration&&state.chatId===id&&state.page==='chat'){state.chat=result;$('prompt').value='';$('breadcrumb').textContent=result.title;renderMessages(true);scheduleChatPoll();}
    await refreshChats();
  }catch(e){error(e.message);}finally{state.pendingSend=false;composerState();}
}
async function navigate(page,options={},restoring=false){
  if(page==='bill'&&!options.returnTo)options={...options,returnTo:options.return_view?{page:options.return_view,options:options.return_options||{}}:state.route||{page:'bills',options:{}}};
  const route={page,options};
  if(!restoring&&JSON.stringify(route)!==JSON.stringify(state.route))history.pushState({route},'', '#'+page);
  state.route=route;
  if(page==='firm')return firmFlow.show(options);
  if(page==='intelligence')return intelligenceFlow.show(options);
  if(page==='experiment')return showExperiment(options.id);
  if(page==='campaigns')return researchLab.show(options);
  if(page==='bills')return consumerFlow.bills(options);
  if(page==='chat'){if(state.chatId)return openChat(state.chatId);switchPage('chat','New chat');renderMessages();return;}
  if(page==='data')return samplingFlow.show(options);
  if(page==='sample')return samplingFlow.sample(options);
  if(page==='explore')return explorer.show(options);
  if(page==='collections')return flow.collections(options);
  if(page==='watching')return flow.watching();
  if(page==='session')return flow.session(options.id);
  if(['priorities','activity','coverage'].includes(page))return consumerFlow[page](options);
  if(page==='learning')return learningFlow.show(options);
  if(page==='autoresearch')return autoResearch.show();
  if(page==='sessions')return flow.sessions(options);
  if(page==='bill')return showBill(options);
  if(page==='rigor')return showRigor();
  if(page==='sources')return showSources(options.dataset);
  if(page==='experiments')return showExperiments();
  if(page==='settings')return showSettings();
  if(page==='replay'||page==='monitor'){
    switchPage(page,page==='replay'?'Historical replay':'Bill monitor');
    const params=new URLSearchParams({embed:'1',mode:page,dataset:options.dataset||'demo'});
    for(const key of ['bill_id','cutoff'])if(options[key])params.set(key,options[key]);
    if(options.bill_id){const match=options.bill_id.match(/(?:demo-)?(\d+)-/);if(match)params.set('congress',match[1]);}
    const url='/workspace.html?'+params.toString();if($('research-frame').getAttribute('src')!==url)$('research-frame').src=url;
  }
}
async function showSources(dataset){
  if(dataset)state.sourceDataset=dataset;switchPage('sources','Sources');const generation=state.generation;$('content-page').innerHTML='<p class="page-empty">Reading source collection…</p>';
  try{const result=await api('sources?dataset='+state.sourceDataset);if(generation!==state.generation)return;
    $('content-page').innerHTML=`<div class="content-header"><div><h1>Source collection</h1><p>Import official records, inspect their coverage, and take them into your research.</p></div><button class="primary" data-icon="import" id="show-source-import">Import a bill</button></div><form id="source-import" class="inline-form" hidden><label>Congress<input name="congress" type="number" min="93" max="200" value="119" required></label><label>Type<select name="type"><option value="hr">H.R.</option><option value="s">S.</option></select></label><label>Bill number<input name="number" type="number" min="1" value="22" required></label><button class="primary">Import / refresh</button><span class="form-status">Retrieved from GovInfo. Source snapshots are preserved.</span></form><div class="source-toolbar"><input id="source-search" type="search" placeholder="Search bills, topics or identifiers" aria-label="Search sources"><select id="source-dataset" aria-label="Source collection"><option value="official">Official sources</option><option value="demo">Synthetic demo</option></select></div><form class="source-save-form" id="source-save-form"><label>Save filtered results as a collection<input name="name" maxlength="100" required placeholder="Collection name"></label><button class="secondary" id="source-save">Save collection</button><span class="form-status" role="status"></span></form><p class="source-count" id="source-count"></p><div id="source-table" class="table-wrap"></div>`;
    $('source-dataset').value=state.sourceDataset;
    let filteredBills=[];
    const render=()=>{const q=$('source-search').value.toLowerCase();const rows=result.bills.filter(b=>`${b.bill_id} ${b.title} ${b.topic}`.toLowerCase().includes(q));filteredBills=rows.map(b=>b.bill_id);$('source-save').disabled=!rows.length||rows.length>100;$('source-count').textContent=`${rows.length} of ${result.count} records · ${result.note}`;$('source-table').innerHTML=rows.length?`<table><thead><tr><th>Bill</th><th>Source timing</th><th>Events</th><th>Actions</th></tr></thead><tbody>${rows.map(b=>`<tr><td><small>${esc(b.bill_id)} · ${esc(b.topic)}</small><strong>${esc(b.title)}</strong></td><td>${stamp(b.observed_at)}<br><small>${b.archive_asserted?'Archive availability asserted':'Historical availability unverified'}</small></td><td>${b.events}</td><td><button class="table-action" data-source-open="${esc(b.bill_id)}">Open record</button>${state.sourceDataset==='official'?`<br><button class="table-action" data-refresh="${esc(b.bill_id)}">Refresh</button>`:''}</td></tr>`).join('')}</tbody></table>`:'<div class="page-empty"><h2>No matching sources</h2><p>Clear your search or import a bill to begin.</p></div>';
      document.querySelectorAll('[data-source-open]').forEach(b=>b.onclick=()=>navigate('bill',{dataset:state.sourceDataset,bill_id:b.dataset.sourceOpen,cutoff:state.sourceDataset==='demo'?'2023-07-01':undefined}));
      document.querySelectorAll('[data-refresh]').forEach(b=>b.onclick=async()=>{const match=b.dataset.refresh.match(/^(\d+)-(hr|s)(\d+)$/);if(!match)return;buttonPending(b,true,'Refreshing…');try{await api('import',{congress:Number(match[1]),type:match[2],number:Number(match[3])});toast('Official source refreshed');if(state.page==='sources'&&state.generation===generation)await showSources('official');}catch(e){error(e.message);buttonPending(b,false,'Refresh');}});
    };
    $('source-search').oninput=render;$('source-dataset').onchange=()=>showSources($('source-dataset').value);render();
    $('source-save-form').onsubmit=async event=>{event.preventDefault();const form=event.currentTarget,b=$('source-save'),status=form.querySelector('.form-status');buttonPending(b,true,'Saving…');try{const c=await api('collections',{name:form.elements.name.value,dataset:state.sourceDataset,bill_ids:filteredBills});if(generation===state.generation)await flow.collections({id:c.id});}catch(e){if(generation===state.generation)status.textContent=e.message;}finally{buttonPending(b,false,'Save collection');}};
    $('show-source-import').onclick=()=>{$('source-import').hidden=!$('source-import').hidden;};
    $('source-import').onsubmit=async event=>{event.preventDefault();const form=event.currentTarget,button=form.querySelector('button'),status=form.querySelector('.form-status'),data=new FormData(form);buttonPending(button,true,'Importing…');try{const r=await api('import',{congress:Number(data.get('congress')),type:data.get('type'),number:Number(data.get('number'))});toast(r.bill_id+' imported');if(state.page==='sources'&&state.generation===generation)await showSources('official');}catch(e){status.textContent=e.message;buttonPending(button,false,'Import / refresh');}};
  }catch(e){if(generation===state.generation){error(e.message);$('content-page').innerHTML='<p class="page-empty">Could not load sources. Select Sources to retry.</p>';}}
}
function experimentForm(){return `<form id="run-form" class="inline-form"><label>Collection<select name="dataset"><option value="demo">Synthetic demo</option><option value="official">Official sources</option></select></label><label>Test Congress<input name="congress" type="number" value="118" min="93" max="200" required></label><label>Checkpoint age (days)<input name="age_days" type="number" value="180" min="1" max="700" required></label><button class="primary">Run experiment</button><span class="form-status">Prior-Congress training. One checkpoint per bill.</span></form>`;}
async function showExperiments(){
  switchPage('experiments','Experiments');state.runId=null;const generation=state.generation;$('content-page').innerHTML='<p class="page-empty">Loading experiment history…</p>';
  try{const runs=await api('experiments');if(generation!==state.generation)return;
    $('content-page').innerHTML=`<div class="content-header"><div><h1>Experiments</h1><p>Plan a research session, test an idea, and compare it with earlier evidence.</p></div><button class="primary" id="research-sessions">Research sessions</button></div><div id="session-entry" class="flow-callout"><strong>From question to reproducible result</strong><p>Choose a saved collection, review the exact experiment and its data checks, then run and compare.</p><button class="table-action" id="start-session">Plan a research session</button></div><details class="flow-details"><summary>Quick exploratory run</summary>${experimentForm()}</details><h2 class="section-heading">All experiment reports</h2><div class="table-wrap">${runs.length?`<table><thead><tr><th>Run</th><th>Collection / checkpoint</th><th>Status</th><th>Brier</th><th></th></tr></thead><tbody>${runs.map(r=>`<tr><td><strong>${esc(r.id.slice(0,8))}${r.parent_id?' · rerun':''}</strong><small>${stamp(r.created_at)}</small></td><td>${esc(r.title||(r.config.dataset==='demo'?'Synthetic demo':'Official subset'))}<br><small>Congress ${r.config.congress} · ${r.config.age_days} days</small></td><td><span class="run-status ${esc(r.status)}">${esc(r.status)}</span></td><td>${r.metrics?r.metrics.brier.toFixed(3):'—'}</td><td><button class="table-action" data-open-run="${esc(r.id)}">Open report</button></td></tr>`).join('')}</tbody></table>`:'<div class="page-empty"><h2>Your first experiment starts here</h2><p>Choose a collection and checkpoint above, or ask the assistant to run one.</p></div>'}</div>`;
    $('research-sessions').onclick=()=>flow.sessions();$('start-session').onclick=()=>flow.sessions();
    document.querySelectorAll('[data-open-run]').forEach(b=>b.onclick=()=>showExperiment(b.dataset.openRun));
    $('run-form').onsubmit=async event=>{event.preventDefault();const form=event.currentTarget,data=new FormData(form),button=form.querySelector('button');buttonPending(button,true,'Starting…');try{const run=await api('experiments',{dataset:data.get('dataset'),congress:Number(data.get('congress')),age_days:Number(data.get('age_days'))});if(state.page==='experiments'&&state.generation===generation)await showExperiment(run.id);}catch(e){error(e.message);buttonPending(button,false,'Run experiment');}};
  }catch(e){if(generation===state.generation)error(e.message);}
}
async function showExperiment(id){switchPage('experiments','Experiment report');state.runId=id;$('content-page').innerHTML='<p class="page-empty">Reading experiment report…</p>';await refreshExperiment();}
async function refreshExperiment(){
  const id=state.runId,generation=state.generation;
  try{const run=await api('experiment?id='+encodeURIComponent(id));if(state.runId!==id||generation!==state.generation||state.page!=='experiments')return;renderExperiment(run);if(run.status==='running')state.poll=setTimeout(refreshExperiment,1200);}catch(e){if(generation===state.generation)error(e.message);}
}
function renderExperiment(run){
  const renderGeneration=state.generation;
  const m=run.metrics,bins=m?.reliability||[];
  $('content-page').innerHTML=`<div class="content-header"><div><h1>${esc(run.title||'Experiment report')}</h1><p>${esc(run.note)} ${esc(typeof run.protocol==='string'?run.protocol:run.protocol?.split||'')}</p></div><button class="secondary" id="all-runs">All experiments</button></div><div class="run-header"><div><h2>Congress ${run.config.congress} · ${run.config.age_days}-day checkpoint</h2><span class="run-status ${esc(run.status)}">${esc(run.status)}</span> <span class="run-note">${stamp(run.created_at)} · ${esc(run.id.slice(0,8))}</span></div><button class="primary" id="rerun" ${run.status==='running'?'disabled':''}>Rerun experiment</button></div><p class="run-note">${esc(run.design_status||'Exploratory development')} · Preflight: ${esc(run.preflight?.status||'Legacy run; no recorded preflight')} ${run.protocol_id?'· Protocol '+esc(run.protocol_id.slice(0,8)):''}</p>${run.parent_id?`<p class="run-note">Rerun of <button class="table-action" id="parent-run">${esc(run.parent_id.slice(0,8))}</button>. The earlier report is preserved.</p>`:''}${run.status==='running'?'<p class="page-empty"><span class="working-dot"></span>Building snapshots and evaluating eligible forecasts…</p>':['failed','blocked'].includes(run.status)?`<div class="global-error">${esc(run.error || run.preflight?.blockers?.join(' ') || run.conclusion || 'Evidence checks did not pass.')}</div>${run.kind==='sample_publication_study'?publicationStudyDetails(run):''}`:`<div class="run-metrics"><div><strong>${run.available}/${run.attempted}</strong><span>Forecasts available</span></div><div><strong>${m?.n??0}</strong><span>Resolved cases scored</span></div><div><strong>${m?m.brier.toFixed(3):'—'}</strong><span>Model Brier · lower is better</span></div><div><strong>${run.baseline?run.baseline.brier.toFixed(3):'—'}</strong><span>Historical-rate Brier</span></div></div><div class="result-columns"><section><h3>Predictions and observed outcomes</h3><p>Each row is a nonempty probability bin. Bars use the same 0–100% scale.</p><div class="chart-legend"><span><i></i>Predicted</span><span><i class="observed"></i>Observed</span></div><div class="reliability-chart">${bins.length?bins.map(b=>`<div class="reliability-bin"><span>${Math.round(b.lower*100)}–${Math.round(b.lower*100+10)}%</span><div class="bar-pair"><span style="width:${b.predicted*100}%" title="Predicted ${pct(b.predicted)}"></span><span class="observed" style="width:${b.observed*100}%" title="Observed ${pct(b.observed)}"></span></div><span>n=${b.n}</span></div>`).join(''):'<p>No resolved forecasts to visualize. Inspect coverage and unavailable reasons below.</p>'}</div></section><section><h3>Read this result correctly</h3><p>${esc(run.note)}</p><p>Unavailable estimates are excluded, never treated as zero. Unresolved outcomes are not failures. Sparse reliability bins do not establish calibration.</p><p>${m?`Log loss: ${m.log_loss.toFixed(3)}. Outcome base rate: ${pct(m.base_rate)}.`:'No proper score is available for this run.'}</p><p>${esc(run.rerun_note)}</p></section></div><div class="table-wrap"><table><thead><tr><th>Bill</th><th>Estimate</th><th>Outcome</th><th>Availability</th></tr></thead><tbody>${(run.results||[]).map(r=>`<tr><td><strong>${esc(r.bill_id)}</strong><small>${esc(r.title)}</small></td><td>${pct(r.probability)}</td><td>${r.outcome==null?'Unresolved':r.outcome?'Enacted':'Not enacted'}</td><td>${r.status==='available'?'Saved forecast':run.kind==='macro_pilot'?'Retrospective estimate':esc(r.reason)}</td></tr>`).join('')}</tbody></table></div><p class="run-note">Input fingerprint: ${esc(run.input_hash)}. Model: ${esc(run.candidate||(run.kind==='macro_pilot'?'publication-plus-macro-l2':'structured-l2-v1'))}. Calibration: not established.</p>`}`;
  if(run.kind==='macro_pilot'){
    const evidence=document.createElement('section');evidence.className='sampling-step';
    evidence.innerHTML=`<h2>Did macro context help?</h2><p>Same ${run.available} evaluation bills; ${run.evaluation_positives} enactments. Training: ${run.training_count} bills, ${run.training_positives} enactments.</p><div class="table-wrap"><table><caption>Fixed exploratory comparison; lower Brier is better</caption><thead><tr><th>Method</th><th>Brier</th></tr></thead><tbody><tr><td>Historical-rate baseline</td><td>${run.baseline.brier.toFixed(6)}</td></tr><tr><td>Publication history only</td><td>${run.publication_metrics.brier.toFixed(6)}</td></tr><tr><td>Publication history + unemployment + inflation</td><td>${run.metrics.brier.toFixed(6)}</td></tr></tbody></table></div><p>Macro minus publication-only Brier: ${run.brier_difference_vs_publication.toFixed(6)}. Negative favors adding macro on this sample. No model is promoted.</p><details><summary>Economic sources and research limitations</summary><p>ALFRED releases as of previous month-end; all original bill exclusions retained.</p><ul>${run.limitations.map(x=>`<li>${esc(x)}</li>`).join('')}</ul><p>Reproduce offline: python3 -m engine.macro_pilot --offline</p><p>Fingerprint: ${esc(run.reproducibility_hash)}</p></details>`;
    $('content-page').append(evidence);$('rerun').textContent='Verify offline reproduction';
  }
  if(run.kind==='sample_publication_study_v2'){
    const evidence=document.createElement('section'); evidence.className='sampling-step';
    evidence.innerHTML=`<h2>Version 2 evidence amendment</h2><p>${esc(run.amendment_note)}</p><p>${run.selected} originally selected · ${run.training_count} training cases (${run.training_positives} enacted) · ${run.available} evaluated (${run.evaluation_positives} enacted).</p><p>Candidate minus baseline Brier: ${Number(run.brier_difference).toFixed(5)}. Positive means the candidate performed worse. This model is not promoted.</p><details><summary>Earlier outcome evidence and limitations</summary><ul>${(run.training_label_provenance||[]).map(p=>`<li>Congress ${p.congress}: complete law census available ${esc(p.available_at)}</li>`).join('')}${(run.limitations||[]).map(p=>`<li>${esc(p)}</li>`).join('')}</ul><p class="run-note">Reproduction fingerprint: ${esc(run.reproducibility_hash)}</p></details>`;
    $('content-page').append(evidence);
  }
  $('all-runs').onclick=showExperiments;if($('parent-run'))$('parent-run').onclick=()=>showExperiment(run.parent_id);
  $('rerun').onclick=async()=>{const button=$('rerun');buttonPending(button,true,'Starting rerun…');try{const next=await api('experiments/rerun',{id:run.id});if(state.page==='experiments'&&state.generation===renderGeneration)await showExperiment(next.id);toast(next.reproduced?'Offline reproduction matches the saved report':'New run created; original report preserved');}catch(e){error(e.message);buttonPending(button,false,'Rerun experiment');}};
}
function publicationStudyDetails(run){
  return `<section class="sampling-step"><h2>What the source audit found</h2><p>${run.selected} bills remain in the frozen sample. No forecasts were scored or promoted.</p><p>${run.training_count} potentially eligible training cases; ${run.publication_eligible_count} potentially eligible evaluation cases. These counts do not establish permission to score.</p><ul>${(run.blockers||[]).map(b=>`<li>${esc(b)}</li>`).join('')}</ul><details><summary>Training-label availability</summary><ul>${(run.training_label_provenance||[]).map(p=>`<li>Congress ${p.congress}: complete outcome source available ${esc(p.available_at)}</li>`).join('')}</ul></details><details><summary>Research limitations</summary><ul>${(run.limitations||[]).map(p=>`<li>${esc(p)}</li>`).join('')}</ul></details><p class="run-note">Reproduction fingerprint: ${esc(run.reproducibility_hash)}</p></section>`;
}
async function showSettings(){
  switchPage('settings','Connections');const generation=state.generation;$('content-page').innerHTML='<p class="page-empty">Reading connection settings…</p>';
  try{connection=await api('settings');syncConnection();if(generation!==state.generation)return;
    $('content-page').innerHTML=`<div class="content-header"><div><h1>Connections</h1><p>Official records come from GovInfo. OpenRouter powers the research conversation.</p></div></div><section class="setting-section"><h2>OpenRouter</h2><div class="connection-status"><i></i><span>${connection.configured?'API key configured locally':'No API key configured'}</span></div><form id="settings-form" class="settings-form"><label>Model ID<input id="model-id" name="model" value="${esc(connection.model)}" required autocomplete="off"><span class="field-help">Use a model that supports tool calls, such as openai/gpt-4o-mini.</span></label><label>${connection.configured?'Replace API key':'API key'}<input id="api-key" name="key" type="password" placeholder="${connection.configured?'Leave blank to keep your existing key':'Paste your OpenRouter API key'}" autocomplete="new-password" spellcheck="false"><span class="field-help">Stored in the ignored local .env file. The saved key is never returned to the browser or included in chats.</span></label><div class="setting-actions"><button class="primary" type="submit">Save connection</button><button class="secondary" data-icon="connection" id="test-connection" type="button">Test saved connection</button><span id="settings-status" class="settings-status" role="status"></span></div></form></section><section class="setting-section"><h2>GovInfo official records</h2><p>Bill inventories and source records download directly from the official bulk repository. No API key is needed for this connection.</p><button class="secondary" data-icon="data" id="connection-data">Open data &amp; imports</button><p>Congress.gov API discovery is not connected. The current workflow uses GovInfo and does not require a second credential.</p></section><section class="setting-section"><h2>What chat can do</h2><p>Inspect imported records, retrieve a specific official bill, run a fixed-age experiment, rerun earlier experiments, and open the related workspace tabs.</p><p>Each run preserves its report. The assistant has no shell or arbitrary code execution. Model-generated text does not alter official outcomes or saved probabilities.</p><p>Chat messages and the relevant research records are sent to OpenRouter when you submit a prompt. Testing the connection sends one small test request.</p></section>`;
    $('connection-data').onclick=()=>navigate('data');
    $('settings-form').onsubmit=async event=>{event.preventDefault();const button=event.currentTarget.querySelector('button[type=submit]'),status=$('settings-status'),apiKey=$('api-key');buttonPending(button,true,'Saving…');try{connection=await api('settings',{model:$('model-id').value,key:apiKey.value});apiKey.value='';syncConnection();status.textContent='Connection saved.';}catch(e){status.textContent=e.message;}finally{buttonPending(button,false,'Save connection');}};
    $('test-connection').onclick=async()=>{const button=$('test-connection'),status=$('settings-status');buttonPending(button,true,'Testing…');status.textContent='';try{const r=await api('settings/test',{});status.textContent='Connected · '+r.model;}catch(e){status.textContent=e.message;}finally{buttonPending(button,false,'Test saved connection');}};
  }catch(e){if(generation===state.generation)error(e.message);}
}
document.querySelector('.skip-link').onclick=event=>{event.preventDefault();$('workspace-main').focus();};
$('composer').onsubmit=event=>{event.preventDefault();send();};
$('prompt').onkeydown=event=>{if(event.key==='Enter'&&!event.shiftKey&&!event.isComposing){event.preventDefault();send();}};
$('new-chat').onclick=createChat;$('model-shortcut').onclick=showSettings;
document.querySelectorAll('[data-page]').forEach(button=>button.onclick=()=>navigate(button.dataset.page));
function syncSidebar(){const mobile=matchMedia('(max-width:700px)').matches;const visible=mobile?document.body.classList.contains('sidebar-open'):!document.body.classList.contains('sidebar-collapsed');$('sidebar').inert=!visible;$('sidebar').setAttribute('aria-hidden',String(!visible));$('toggle-sidebar').setAttribute('aria-expanded',String(visible));}
$('toggle-sidebar').onclick=()=>{if(matchMedia('(max-width:700px)').matches){document.body.classList.remove('sidebar-collapsed');document.body.classList.toggle('sidebar-open');}else{document.body.classList.toggle('sidebar-collapsed');}syncSidebar();};
matchMedia('(max-width:700px)').addEventListener('change',syncSidebar);syncSidebar();
document.addEventListener('keydown',event=>{if((event.metaKey||event.ctrlKey)&&event.key==='k'){event.preventDefault();createChat();}if(event.key==='Escape'){document.body.classList.remove('sidebar-open');syncSidebar();}});
try{const values=await Promise.all([api('settings'),api('chats')]);connection=values[0];state.chats=values[1];syncConnection();renderSidebar();renderMessages();const route=location.hash==='#learning'?{page:'learning',options:{}}:history.state?.route||{page:'priorities',options:{}};await navigate(route.page,route.options,true);}catch(e){switchPage('priorities','Home');researchLoadError(e.message,()=>location.reload());}

window.addEventListener('popstate',event=>{const r=event.state?.route||{page:'priorities',options:{}};navigate(r.page,r.options,true);});
flow.startNotifications();

function readable(key){return key.replace(/_/g,' ').replace(/^./,c=>c.toUpperCase());}
function researchLoadError(message,retry){
  $('content-page').innerHTML=`<div class="page-empty" role="alert"><p>${esc(message)}</p><button class="secondary" id="retry-research">Try again</button></div>`;
  $('retry-research').onclick=retry;
}
function structuredReport(value,depth=0){
  if(value===null||value===undefined)return '<span class="run-note">Not established</span>';
  if(typeof value!=='object')return `<span>${esc(value)}</span>`;
  if(Array.isArray(value))return value.length?`<ul class="report-list">${value.map(v=>`<li>${structuredReport(v,depth+1)}</li>`).join('')}</ul>`:'<span class="run-note">None recorded</span>';
  return `<dl class="report-fields">${Object.entries(value).filter(([key])=>!['id','kind','contract_version'].includes(key)).map(([key,val])=>`<div><dt>${esc(readable(key))}</dt><dd>${structuredReport(val,depth+1)}</dd></div>`).join('')}</dl>`;
}
async function showResearchReport(id){
  switchPage('rigor','Research report');const generation=state.generation;$('content-page').innerHTML='<p class="page-empty">Reading audit record…</p>';
  try{const report=await api('research-report?id='+encodeURIComponent(id));if(generation!==state.generation)return;
    $('content-page').innerHTML=`<div class="content-header"><div><h1>${esc(report.title||'Research report')}</h1><p>Saved ${stamp(report.created_at)} · ${esc(report.contract_version)} · ${esc(report.status||'Recorded')}</p></div><button class="secondary" id="back-rigor">Research protocol</button></div><div class="research-report">${structuredReport(report)}</div>`;
    $('back-rigor').onclick=showRigor;
  }catch(e){if(generation===state.generation)researchLoadError(e.message,()=>showResearchReport(id));}
}
async function showRigor(){
  switchPage('rigor','Research protocol');const generation=state.generation;$('content-page').innerHTML='<p class="page-empty">Checking the research contract…</p>';
  try{const info=await api('rigor?dataset='+$('chat-dataset').value);if(generation!==state.generation)return;
    const r=info.readiness;
    $('content-page').innerHTML=`<div class="content-header"><div><h1>Research protocol</h1><p>The full plan, the current implementation, and the evidence needed to move forward.</p></div></div><section class="setting-section"><h2>Release gate: not passed</h2><ul class="report-list">${r.release_blockers.map(b=>`<li>${esc(b)}</li>`).join('')}</ul><p>${esc(r.next_step)}</p></section><h2 class="section-heading">What chat can oversee</h2><div class="table-wrap"><table><thead><tr><th>Plan area</th><th>Status</th><th>Current scope</th></tr></thead><tbody>${r.capabilities.map(c=>`<tr><td>${esc(c.name)}</td><td><span class="run-status">${esc(c.status.replaceAll('_',' '))}</span></td><td>${esc(c.scope)}</td></tr>`).join('')}</tbody></table></div><h2 class="section-heading">Saved protocols</h2>${info.protocols.length?`<div class="table-wrap"><table><thead><tr><th>Hypothesis / design</th><th>Status</th><th>Registration</th></tr></thead><tbody>${info.protocols.map(p=>`<tr><td><strong>${esc(p.title)}</strong><small>${esc(p.hypothesis)}</small><br><small>${esc(p.id)}</small></td><td>${esc(p.status)}<br><small>${esc(p.unsupported.join(' '))}</small></td><td>${esc(p.registration_note)}</td></tr>`).join('')}</tbody></table></div>`:'<p class="run-note">No saved protocols. Ask chat to register a hypothesis, collection, test Congress and checkpoint. Unsupported designs remain explicitly blocked.</p>'}<h2 class="section-heading">Plan and architecture</h2><div class="source-toolbar"><select id="contract-document" aria-label="Research document">${Object.keys(info.documents).map(k=>`<option value="${k}">${esc(readable(k))}</option>`).join('')}</select><select id="contract-section" aria-label="Research document section"></select><button class="secondary" id="read-contract">Read section</button></div><pre id="contract-content" class="contract-content">Select a section to read the original specification.</pre>`;
    let readRequest=0;
    const invalidate=()=>{readRequest++;$('contract-content').textContent='Select Read section to load this selection.';};
    const sections=()=>{$('contract-section').innerHTML=info.documents[$('contract-document').value].sections.map(s=>`<option>${esc(s.heading)}</option>`).join('');invalidate();};
    sections();$('contract-document').onchange=sections;$('contract-section').onchange=invalidate;
    $('read-contract').onclick=async()=>{
      const request=++readRequest,document=$('contract-document').value,section=$('contract-section').value,target=$('contract-content');
      target.textContent='Loading section…';
      try{const result=await api('research-document?'+new URLSearchParams({document,section}));if(generation!==state.generation||request!==readRequest)return;target.textContent=result.content+'\n\nDocument fingerprint: '+result.hash;}
      catch(e){if(generation===state.generation&&request===readRequest)target.textContent=e.message+' Select Read section to retry.';}
    };
  }catch(e){if(generation===state.generation)researchLoadError(e.message,showRigor);}
}

function billDate(value){return value?new Date(value).toLocaleDateString(undefined,{year:'numeric',month:'short',day:'numeric',timeZone:'UTC'}):'Not recorded';}
function billSource(url,label='View official source'){
  try{const parsed=new URL(url);if(parsed.protocol==='https:'&&['govinfo.gov','www.govinfo.gov','congress.gov','www.congress.gov'].includes(parsed.hostname))return `<a href="${esc(parsed.href)}" target="_blank" rel="noopener noreferrer">${esc(label)} ${icon('arrowRight')}</a>`;}catch{}
  return '';
}
function plainBillStatus(status,id){if(status==='Passed origin')return id.includes('-hr')?'Passed the House':'Passed the Senate';if(status==='Bicameral')return 'Passed both chambers';if(status==='Committee')return 'In committee';return status;}
async function showBill(options){
  const {dataset='official',bill_id,cutoff}=options;
  switchPage('bill','Bill overview');const generation=state.generation;
  $('content-page').innerHTML='<p class="page-empty">Reading the bill’s evidence…</p>';
  const params=new URLSearchParams({dataset,bill_id});if(cutoff)params.set('cutoff',cutoff);
  try{
    const r=await api('bill-detail?'+params);if(generation!==state.generation)return;
    const back=`<button class="table-action" data-icon="arrowLeft" id="bill-sources">${options.sample_id?'Back to sample review':options.returnTo?.page==='explore'?'Back to map':options.returnTo?.page==='priorities'?'Back to Home':options.returnTo?.page==='firm'?'Back to organization':options.returnTo?.page==='intelligence'?'Back to evidence report':'Back to Bills'}</button>`;
    if(!r.available){$('content-page').innerHTML=`${back}<div class="page-empty"><h1>Evidence unavailable at this date</h1><p>${esc(r.reason)}</p><button class="secondary" id="bill-latest">Open latest imported record</button></div>`;$('bill-sources').onclick=()=>options.sample_id?navigate('sample',{id:options.sample_id}):navigate(options.returnTo?.page||'bills',options.returnTo?.options||{});$('bill-latest').onclick=()=>showBill({dataset,bill_id});return;}
    const b=r.bill,f=r.forecast;
    const uniqueEvents=[...new Map(r.events.map(e=>[[e.effective_at,e.text].join('|'),e])).values()];
    const events=uniqueEvents.map(e=>`<li><time datetime="${esc(e.effective_at)}">${billDate(e.effective_at)}</time><div><p>${esc(e.text||e.stage_name||'Recorded legislative action')}</p>${billSource(e.source_url,'Source record')}</div></li>`);
    $('content-page').innerHTML=`<article class="bill-page">${back}<header class="bill-heading"><p class="bill-eyebrow">${esc(bill_id)} · ${dataset==='demo'?'Synthetic demonstration':'Official source record'}</p><h1>${esc(b.title)}</h1><span class="run-status">${esc(plainBillStatus(r.status,bill_id))}</span><p class="run-note">Evidence as of ${billDate(r.as_of)} · Source retrieved ${billDate(b.observed_at)}. This page reflects the imported record.</p><div class="bill-actions"><button class="secondary" data-icon="watch" id="bill-watch" aria-pressed="${r.watched}">${r.watched?'Following':'Follow bill'}</button><button class="secondary" data-icon="chat" id="bill-ask">Ask about this bill</button><button class="table-action" data-icon="settings" id="bill-watching">Following settings</button><button class="table-action" data-icon="clock" id="bill-replay">Past evidence</button></div><p class="run-note" id="bill-watch-note" role="status">Following saves this bill here. Automatic checks run only while this local app is running.</p></header><div class="bill-columns"><section><h2>What this bill does</h2><p class="bill-eyebrow">${esc(r.overview.label)}</p><div class="bill-overview">${esc(r.overview.text)}</div><p class="run-note">${esc(r.overview.note)} ${r.overview.version?esc(r.overview.version):''}</p>${billSource(r.overview.source_url)}</section><aside class="bill-estimate"><h2>Forecast</h2>${f.status==='available'?`<strong class="bill-probability">${pct(f.probability)}</strong><p class="run-note">${esc(f.track)} · Calculated ${esc(f.issued_at)}</p><p>Experimental estimate of this bill becoming public law by the end of Congress.</p><p class="run-note">${esc(r.forecast_note)}</p><p class="run-note">Historical-rate baseline: ${pct(f.baseline_probability)} · ${f.training_count} training cases.</p>`:`<h3>No estimate available</h3><p>There is not enough eligible historical evidence for an estimate.</p><details><summary>Why is an estimate unavailable?</summary><p>${esc(f.reason||'The evidence is not eligible for a forecast.')}</p></details>`}<p class="run-note">Research has not established predictive improvement over the baseline.</p></aside></div><section class="bill-timeline"><h2>Recorded timeline</h2><p class="run-note">Dates below are action dates, not proof that this information was available then. ${uniqueEvents.length} distinct actions from ${r.events.length} source records.</p><ol>${events.slice(0,8).join('')}</ol>${events.length>8?`<details><summary>Show ${events.length-8} earlier actions</summary><ol>${events.slice(8).join('')}</ol></details>`:''}${events.length?'':'<p>No eligible actions at this evidence date.</p>'}</section><details class="bill-audit"><summary>Research record <span>Sources, timing, coverage and model limits</span></summary>${structuredReport(r.research)}</details></article>`;
    $('bill-sources').onclick=()=>options.sample_id?navigate('sample',{id:options.sample_id}):navigate(options.returnTo?.page||'bills',options.returnTo?.options||{});
    $('bill-replay').onclick=()=>navigate('replay',{dataset,bill_id,cutoff:r.as_of});
    $('bill-watching').onclick=()=>navigate('watching');
    $('bill-ask').onclick=async()=>{await createChat();if(state.page==='chat'){$('chat-dataset').value=dataset;$('prompt').value=`Explain ${bill_id} using its imported official evidence. Summarize its purpose, latest recorded stage and important limitations. Do not infer influence or invent a forecast.`;$('prompt').focus();}};
    let watched=r.watched;
    mountBillContext($('content-page').querySelector('.bill-page'),r,{api,esc,navigate,dataset,bill_id});
    $('bill-watch').onclick=async()=>{const button=$('bill-watch');buttonPending(button,true,'Saving…');try{const saved=await api('watchlist?dataset='+dataset,{bill_id,enabled:!watched});if(generation!==state.generation)return;watched=saved.watchlist.includes(bill_id);button.setAttribute('aria-pressed',String(watched));$('bill-watch-note').textContent=watched?'Saved to your local watchlist. Open Watch settings and changes to configure scheduled checks.':'Removed from your local watchlist.';}catch(e){if(generation===state.generation)error(e.message);}finally{buttonPending(button,false,watched?'Following':'Follow bill');}};
  }catch(e){if(generation===state.generation)researchLoadError(e.message,()=>showBill(options));}
}

function contextOptions(c){return {...c,collection_id:c.collection_id,collection_version:c.collection_version,cutoff:c.cutoff,bill_id:c.bill_id};}
function renderResearchContext(){
  const box=$('chat-research-context'),c=state.researchContext;box.hidden=!c;
  if(!c){box.innerHTML='';return;}
  $('chat-dataset').value=c.dataset;
  box.innerHTML=`<div><strong>${esc(c.collection_name)}</strong><span>Version ${c.collection_version} · ${c.visible_bill_ids.length} bills in view${c.bill_id?' · '+esc(c.bill_id):''}<br>Evidence as of ${esc(c.cutoff)} · ${c.window_days}-day comparison</span></div><div class="context-actions"><button type="button" id="context-return">Return to Explore</button><button type="button" id="context-clear">Clear context</button></div>`;
  $('context-return').onclick=()=>navigate('explore',contextOptions(c));
  $('context-clear').onclick=()=>{state.researchContext=null;state.contextDrafts[state.chatId||'new']=null;renderResearchContext();composerState();};
}
async function stageResearchContext(context){
  try{
    const chat=await api('chats',{});await refreshChats();await openChat(chat.id);
    if(state.chatId!==chat.id||state.page!=='chat')return;
    state.researchContext=context;state.contextDrafts[chat.id]=context;renderResearchContext();composerState();
    $('prompt').value=context.bill_id?'Explain what was known about this bill at the selected date, and what evidence changed in this window.':'Summarize the evidence changes in this collection at the selected date.';
    $('prompt').focus();
  }catch(e){error(e.message);}
}

// Render explicitly named SVG marks after each page or asynchronous result update.
let iconsQueued=false;
new MutationObserver(()=>{if(iconsQueued)return;iconsQueued=true;queueMicrotask(()=>{iconsQueued=false;mountIcons();});}).observe(document.body,{childList:true,subtree:true});
mountIcons();

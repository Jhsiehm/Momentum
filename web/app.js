const $ = id => document.getElementById(id);
const esc = value => String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const pct = value => value == null ? '—' : `${Math.round(value * 100)}%`;
const shortDate = value => value ? new Date(value).toLocaleDateString('en-US', {month:'short',day:'numeric',year:'numeric',timeZone:'UTC'}) : 'Unknown';
const identifier = id => id.replace('demo-', '').replace(/^(\d+)-(hr|s)(\d+)$/, (_, c, t, n) => `${t === 'hr' ? 'H.R.' : 'S.'} ${n}`);
const safeLink = (url, label) => /^https:\/\/(www\.)?(congress\.gov|govinfo\.gov)\//.test(url || '') ? `<a href="${esc(url)}" target="_blank" rel="noopener noreferrer">${esc(label)}</a>` : esc(label);
const state = {dataset:'demo',mode:'replay',view:'landscape',bills:[],watchlist:[],selected:null,cutoff:'2023-07-01',congress:118,tab:'evidence',request:0,detailRequest:0,researchRequest:0};
let currentDetail = null;
let toastTimer;
function toast(message) {$('toast').textContent=message;$('toast').hidden=false;clearTimeout(toastTimer);toastTimer=setTimeout(()=>$('toast').hidden=true,4000);}
function error(message) {$('error').textContent=message;$('error').hidden=!message;}
function query(extra={}) {return new URLSearchParams({dataset:state.dataset,cutoff:state.cutoff,congress:state.congress,...extra});}
async function api(path, options={}) {
  const response = await fetch(`/api/${path}`,options);
  const result = await response.json();
  if (!response.ok) throw new Error(result.error || 'Request failed. Try again.');
  return result;
}
async function post(path, body) {return api(path,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)});}
function filtered() {
  const text=$('search').value.toLowerCase();
  return state.bills.filter(b=>(!text || `${b.title} ${identifier(b.bill_id)} ${b.topic}`.toLowerCase().includes(text)) && (!$('topic').value || b.topic === $('topic').value) && (!$('watch-only').checked || state.watchlist.includes(b.bill_id)));
}
function renderBills() {
  const bills=filtered();
  $('count').textContent=`${bills.length} of ${state.bills.length} bills · ${state.watchlist.filter(id=>state.bills.some(b=>b.bill_id===id)).length} watched`;
  const selected=state.bills.find(b=>b.bill_id===state.selected);
  $('selected-label').textContent=selected ? `${identifier(selected.bill_id)} selected${bills.some(b=>b.bill_id===state.selected)?'':' · outside filter'}` : 'Select a bill to inspect';
  document.querySelectorAll('[data-view]').forEach(b=>{b.classList.toggle('active',b.dataset.view===state.view);b.setAttribute('aria-pressed',b.dataset.view===state.view);});
  if (!bills.length) {
    $('bill-view').innerHTML='<div class="empty"><h2>No bills in this view</h2><p>Clear your filters, select another Congress, or import an official bill.</p></div>';
    return;
  }
  if (state.view==='landscape') {
    const topics=[...new Set(bills.map(b=>b.topic || 'Unknown'))];
    const available=bills.filter(b=>b.probability!=null);
    const missing=bills.filter(b=>b.probability==null);
    if (available.length) {
      $('bill-view').innerHTML=`<div class="landscape" style="--columns:${topics.length}"><div class="axis">${[0,25,50,75,100].map(p=>`<span style="bottom:${p}%">${p}%</span>`).join('')}</div>${topics.map(topic=>{
        const group=available.filter(b=>b.topic===topic);
        return `<div class="topic-column"><span class="topic-name">${esc(topic)}</span>${group.map((bill,i)=>`<button class="bill-marker ${bill.bill_id===state.selected?'selected':''}" style="--p:${bill.probability*100};--x:${22+(i%3)*28}%" data-bill="${esc(bill.bill_id)}" aria-label="${esc(identifier(bill.bill_id)+': '+bill.title+', '+pct(bill.probability))}" aria-pressed="${bill.bill_id===state.selected}" title="${esc(identifier(bill.bill_id)+': '+bill.title+' · '+pct(bill.probability))}"><span></span></button>`).join('')}</div>`;
      }).join('')}</div>${missing.length?`<div class="unavailable-list">No estimate: ${missing.map(b=>`<button class="secondary" data-bill="${esc(b.bill_id)}">${esc(identifier(b.bill_id))}</button>`).join('')}</div>`:''}`;
    } else {
      $('bill-view').innerHTML='<div class="empty"><h2>Evidence first. Estimates when supported.</h2><p>No eligible forecasts at this cutoff. Open a bill to inspect its source records and the reason an estimate is unavailable.</p></div><div class="unavailable-list">'+missing.map(b=>`<button class="secondary" data-bill="${esc(b.bill_id)}">${esc(identifier(b.bill_id))}</button>`).join('')+'</div>';
    }
    $('chart-caption').textContent='Height = estimated probability · Columns = topic · Horizontal spacing separates bills';
  } else if(state.view==='flat') {
    $('bill-view').innerHTML=`<div class="flat-list">${bills.map(b=>`<button class="flat-bill ${b.bill_id===state.selected?'selected':''}" data-bill="${esc(b.bill_id)}" aria-pressed="${b.bill_id===state.selected}"><span><small>${esc(identifier(b.bill_id))} · ${esc(b.topic)}</small><strong>${esc(b.title)}</strong></span><span class="bar-track"><span class="bar-fill" style="display:block;width:${b.probability==null?0:b.probability*100}%"></span></span><span class="number">${pct(b.probability)}</span></button>`).join('')}</div>`;
    $('chart-caption').textContent='Bar length = estimated enactment probability · — = unavailable';
  } else {
    $('bill-view').innerHTML=`<table><thead><tr><th>Bill / title</th><th>Policy</th><th>Stage</th><th>Estimate</th></tr></thead><tbody>${bills.map(b=>`<tr class="${b.bill_id===state.selected?'selected':''}"><td><button data-bill="${esc(b.bill_id)}">${esc(identifier(b.bill_id))}<br>${esc(b.title)}</button></td><td>${esc(b.topic)}</td><td>${esc(b.stage)}</td><td>${pct(b.probability)}</td></tr>`).join('')}</tbody></table>`;
    $('chart-caption').textContent='Enactment by Congress end · — = no eligible estimate';
  }
  $('bill-view').querySelectorAll('[data-bill]').forEach(button=>button.addEventListener('click',()=>selectBill(button.dataset.bill)));
}
function timeline() {
  const year=1787+state.congress*2;
  const start=new Date(`${year}-01-03T00:00:00Z`), end=new Date(`${year+2}-01-02T00:00:00Z`);
  $('timeline').max=Math.max(0,Math.round((Math.min(end.getTime(),new Date(config.today+'T00:00:00Z').getTime())-start)/86400000));
  $('timeline').value=Math.max(0,Math.round((new Date(state.cutoff)-start)/86400000));
  $('start-date').textContent=`Jan ${year}`;$('end-date').textContent=`Jan ${year+2}`;
  $('cutoff-label').textContent=shortDate(state.cutoff);
  $('cutoff').value=state.cutoff.slice(0,10);
  $('timeline').disabled=state.mode==='monitor';
  $('replay-note').textContent=state.mode==='monitor'?'Imported subset, refreshed on demand. Source observation times determine what is available.':'Move through time. Only evidence available by the cutoff enters a forecast.';
}
async function load() {
  const generation=++state.request;
  state.detailRequest++;
  currentDetail=null; $('inspector').innerHTML='<div class="empty"><h2>Loading dated evidence…</h2><p>Preparing the selected bill and cutoff.</p></div>';
  error('');$('bill-view').classList.add('loading');$('count').textContent='Building dated snapshots…';
  try {
    const result=await api(`bills?${query()}`);
    if(generation!==state.request)return;
    state.bills=result.bills;state.watchlist=result.watchlist;state.cutoff=result.cutoff;
    const topic=$('topic').value;
    $('topic').innerHTML='<option value="">All policy topics</option>'+[...new Set(result.bills.map(b=>b.topic))].sort().map(t=>`<option>${esc(t)}</option>`).join('');
    if([...$('topic').options].some(o=>o.value===topic))$('topic').value=topic;
    if(!state.bills.some(b=>b.bill_id===state.selected)) state.selected=state.bills.find(b=>state.watchlist.includes(b.bill_id))?.bill_id || state.bills[0]?.bill_id;
    $('freshness').textContent=state.dataset==='demo'?'Synthetic collection · Not a live feed':`Latest source retrieval: ${result.coverage.latest_retrieval?new Date(result.coverage.latest_retrieval).toLocaleString():'No records imported'}`;
    $('export-ledger').href=`/api/ledger?dataset=${state.dataset}`;
    timeline();renderBills();
    if(state.selected)await loadDetail();else $('inspector').innerHTML='<div class="empty"><h2>Build your evidence collection</h2><p>Use “Import official bill” to retrieve a bill from GovInfo, then select it here.</p></div>';
  } catch(e) {if(generation===state.request){error(e.message);$('count').textContent='Collection could not be loaded';$('inspector').innerHTML='<div class="empty"><h2>Collection unavailable</h2><p>Change the collection or cutoff to retry.</p></div>';}}
  finally {if(generation===state.request)$('bill-view').classList.remove('loading');}
}
async function selectBill(id) {state.selected=id;renderBills();await loadDetail();}
async function loadDetail() {
  const generation=++state.detailRequest;
  currentDetail=null; $('inspector').innerHTML='<div class="empty"><h2>Loading dated evidence…</h2></div>';
  $('inspector').setAttribute('aria-busy','true');
  try {
    const result=await api(`snapshot?${query({bill_id:state.selected})}`);
    if(generation!==state.detailRequest)return;
    currentDetail=result;renderDetail();
  }catch(e){if(generation===state.detailRequest){error(e.message);$('inspector').innerHTML='<div class="empty"><h2>Evidence could not be loaded</h2><p>Select the bill again to retry.</p></div>';}}
  finally {if(generation===state.detailRequest)$('inspector').removeAttribute('aria-busy');}
}
function renderDetail() {
  const {snapshot:snap,forecast:f,previous}=currentDetail;
  const fallback=state.bills.find(b=>b.bill_id===state.selected);
  const bill=snap?.bill || fallback;
  const watched=state.watchlist.includes(state.selected);
  const difference=f.probability!=null&&previous ? (f.probability-previous.probability)*100 : null;
  $('inspector').innerHTML=`<div class="dossier-top"><span>${esc(identifier(state.selected))} · ${state.congress}th Congress</span><button class="secondary watch-button" id="watch-bill">${watched?'Watching':'Watch bill'}</button></div><h2>${esc(bill.title)}</h2><span class="stage-tag">${esc(snap?.stage_name || 'No eligible metadata')}</span>${f.status==='available'?`<div class="probability-line"><span class="probability">${pct(f.probability)}</span><p>Estimated enactment<br>by ${shortDate(f.deadline)}</p></div><div class="forecast-label">${esc(f.track)} · Uncalibrated baseline</div>${difference!=null?`<p class="small-note">${difference>=0?'+':''}${difference.toFixed(1)} percentage points since saved cutoff ${shortDate(previous.cutoff)}.</p>`:'<p class="small-note">First saved checkpoint for this view. No change estimate yet.</p>'}<dl class="forecast-dates"><dt>As of</dt><dd>${shortDate(f.cutoff)}</dd><dt>Issued</dt><dd>${esc(f.issued_at.replace('T',' '))}</dd><dt>Training</dt><dd>${f.training_count} resolved prior families</dd></dl>`:`<div class="probability-line"><span class="probability">—</span><p>Forecast unavailable</p></div><p class="evidence-summary">${esc(f.reason)}</p>`}<div class="dossier-tabs" aria-label="Dossier detail">${['evidence','analogs','audit'].map(tab=>`<button aria-pressed="${state.tab===tab}" class="${state.tab===tab?'active':''}" data-tab="${tab}">${tab[0].toUpperCase()+tab.slice(1)}</button>`).join('')}</div><div id="dossier-content"></div><button id="reveal" class="reveal">Reveal actual outcome</button><div id="outcome" aria-live="polite"></div>`;
  renderDossierContent();
  $('watch-bill').onclick=async()=>{try{const result=await post(`watchlist?${query()}`,{bill_id:state.selected,enabled:!watched});state.watchlist=result.watchlist;renderDetail();renderBills();}catch(e){error(e.message);}};
  document.querySelectorAll('[data-tab]').forEach(b=>b.onclick=()=>{state.tab=b.dataset.tab;renderDetail();document.querySelector(`[data-tab="${state.tab}"]`).focus();});
  $('reveal').onclick=async()=>{
    const id=state.selected, generation=state.detailRequest;
    try{const result=await api(`outcome?${query({bill_id:id})}`);if(generation!==state.detailRequest)return;
      $('outcome').innerHTML=result.resolution?`<div class="outcome"><strong>${result.resolution.value?'Enacted':'Not enacted by Congress end'}</strong>${shortDate(result.resolution.effective_at)}${result.brier!=null?` · Forecast Brier score ${result.brier.toFixed(3)}`:''}<p class="small-note">${esc(result.note)}</p></div>`:'<div class="outcome">Unresolved or not adjudicated. Missing outcome evidence is not failure.</div>';
      $('reveal').textContent='Outcome revealed';
    }catch(e){error(e.message);}
  };
}
function renderDossierContent() {
  const {snapshot:snap,forecast:f}=currentDetail;
  const content=$('dossier-content');
  if(state.tab==='evidence') {
    const events=[...(snap?.events || [])].reverse();
    content.innerHTML=`<p class="evidence-summary">${events.length} eligible source records at this cutoff.${state.dataset==='demo'?' All records in this collection are fictional.':''}</p>${events.map(e=>`<article class="event"><div class="event-time">${shortDate(e.effective_at)} · ${esc(e.source_name)}</div><p>${esc(e.text)}</p><details><summary>Source and timing</summary><p>Event: ${esc(e.effective_at)}<br>Published: ${esc(e.published_at || 'Unknown')}<br>Retrieved: ${esc(e.observed_at)}<br>Archive proof: ${esc(e.archive_proof || 'Not established')}</p>${safeLink(e.source_url,'Open original record')}</details></article>`).join('') || '<p class="small-note">No eligible events. Change the cutoff or import dated evidence.</p>'}<button id="extract" class="secondary">Extract cited evidence with AI</button><div id="ai-result" aria-live="polite"></div>`;
    $('extract').onclick=async()=>{
      const button=$('extract');button.disabled=true;button.textContent='Checking source spans…';
      const id=state.selected, generation=state.detailRequest;
      try{const result=await post(`extract?${query()}`,{bill_id:id});if(generation!==state.detailRequest||!$('ai-result'))return;
        $('ai-result').innerHTML=result.status==='success'?`${result.claims.map(c=>`<div class="event"><p>${esc(c.claim)}</p><details><summary>Verified source quote</summary><p>${esc(c.quote)}</p></details></div>`).join('') || '<p>No supported claims extracted.</p>'}<p class="small-note">${esc(result.note)} Model: ${esc(result.provider_model || result.model)} · Run ${esc(result.id.slice(0,8))}</p>`:`<p class="small-note">${esc(result.error)} Failure retained in the audit log.</p>`;
      }catch(e){error(e.message);}finally{button.disabled=false;button.textContent='Extract cited evidence with AI';}
    };
  } else if(state.tab==='analogs') {
    if(!f.cohort){content.innerHTML='<p class="evidence-summary">No eligible historical comparison cohort. Import and audit prior-Congress records before estimating a rate.</p>';return;}
    const c=f.cohort;
    content.innerHTML=`<p class="small-note">${esc(c.rule)}. One resolved example per family.</p><p class="analog-summary"><strong>${c.successes} of ${c.resolved}</strong> prior bills enacted (${pct(c.observed_rate)} observed).</p><p class="small-note">Shrinkage estimate: ${pct(f.reference_probability)}. ${esc(c.pending_note)} No validated sampling interval.</p>${c.rows.slice(0,12).map(r=>`<div class="analog-row"><strong>${esc(identifier(r.bill_id))} · ${esc(r.title)}</strong>${r.congress}th Congress · ${r.y?'Enacted':'Not enacted'}<br>Matched cutoff ${shortDate(r.cutoff)} · ${esc(r.topic)}</div>`).join('')}${c.rows.length>12?`<p class="small-note">Showing 12 of ${c.rows.length}. Complete source rows are in the forecast ledger export.</p>`:''}`;
  } else {
    content.innerHTML=`<dl class="audit"><dt>Target</dt><dd>Own-bill enactment by Congress end</dd><dt>Cutoff</dt><dd>${esc(state.cutoff)}</dd><dt>Snapshot</dt><dd>${esc(f.snapshot_hash || snap?.snapshot_hash || 'Unavailable')}</dd><dt>Model</dt><dd>${esc(f.model_version || 'No eligible forecast')}</dd><dt>Calibration</dt><dd>${esc(f.calibration_version || 'Not established')}</dd><dt>Training and missingness</dt><dd>Earlier Congresses only; resolved and observable labels. No-recorded-event does not imply failure.</dd><dt>Uncertainty</dt><dd>${esc(f.uncertainty_note || 'No estimate or interval available.')}</dd><dt>Family links</dt><dd>${esc(snap?.bill.family_status || 'Synthetic family identifiers')}</dd><dt>Forecast ID</dt><dd>${esc(f.id || 'Not saved')}</dd></dl>`;
  }
}
async function research() {
  const generation=++state.researchRequest;
  $('research').innerHTML='<div class="empty"><h2>Loading research record…</h2></div>';
  error('');
  try{
    const [r,c]=await Promise.all([api(`research?${query()}`),api(`coverage?${query()}`)]);
    if(generation!==state.researchRequest || state.mode!=='research')return;
    const m=r.metrics;
    $('research').innerHTML=`<div class="research-head"><div><h2>Inspect the forecast record</h2><p>${esc(r.note)}</p></div><a href="/api/ledger?dataset=${state.dataset}" download="forecast-ledger.json">Export ledger</a></div><div class="research-metrics"><div><strong>${r.ledger_count}</strong><span>Locked forecasts</span></div><div><strong>${r.bills}</strong><span>Resolved bills scored</span></div><div><strong>${m?m.brier.toFixed(3):'—'}</strong><span>Brier score · lower is better</span></div><div><strong>${r.baseline?r.baseline.brier.toFixed(3):'—'}</strong><span>Historical-rate Brier</span></div></div><div class="research-columns"><section><h3>Reliability, with denominators</h3><p>Observed outcomes against predicted probabilities. Sparse bins are descriptive and cannot establish calibration.</p>${m?`<table><thead><tr><th>Predicted</th><th>Observed</th><th>Bills</th></tr></thead><tbody>${m.reliability.map(b=>`<tr><td>${pct(b.predicted)}</td><td>${pct(b.observed)}</td><td>${b.n}</td></tr>`).join('')}</tbody></table><p>Log loss: ${m.log_loss.toFixed(3)} · Base rate: ${pct(m.base_rate)} · ${r.families} families</p>`:'<p>No resolved forecasts to score. Explore replay to save checkpoints, then return here.</p>'}<p>${r.pending} unresolved forecast records are excluded from scores. No family-clustered interval has been established.</p></section><section><h3>Source coverage</h3><p>${esc(c.note)}</p><table><thead><tr><th>Congress</th><th>Bills</th><th>Events</th><th>Resolved</th></tr></thead><tbody>${c.rows.map(row=>`<tr><td>${row.congress}</td><td>${row.bills}</td><td>${row.events}</td><td>${row.resolved}</td></tr>`).join('')}</tbody></table><p>Customer-facing validation gate: <strong>not passed</strong>. No untouched holdout, historical breadth or prospective reliability claim.</p></section></div>`;
  }catch(e){if(generation===state.researchRequest){error(e.message);$('research').innerHTML='<p>Research could not be loaded. Select the collection again to retry.</p>';}}
}
function collectionLabel() {
  $('notice').textContent=state.dataset==='demo'?'Demonstration collection · Fictional bills and experimental estimates. No predictive-performance claim.':'Official source collection · Imported subset. Forecasts require audited prior data; missing estimates are shown explicitly.';
  $('notice').classList.toggle('official',state.dataset==='official');
}
async function mode(mode) {
  state.mode=mode;state.researchRequest++;
  $('dataset').disabled=mode==='monitor';$('cutoff').disabled=mode==='monitor';
  document.querySelectorAll('[data-mode]').forEach(b=>b.classList.toggle('active',b.dataset.mode===mode));
  $('workspace').hidden=mode==='research';$('research').hidden=mode!=='research';
  $('page-title').textContent=mode==='replay'?'See the bill. Trace the evidence.':mode==='monitor'?'Follow the legislative record.':'Put every estimate to the test.';
  $('page-description').textContent=mode==='replay'?'Reconstruct a legislative moment, then examine what came next.':mode==='monitor'?'Your imported bills, their evidence, and what has changed.':'Inspect locked forecasts, denominators, source coverage and limitations.';
  if(mode==='monitor'){state.dataset='official';$('dataset').value='official';state.congress=119;$('congress').value='119';state.cutoff=config.today;collectionLabel();}
  if(mode==='replay' && state.dataset==='demo' && state.cutoff.slice(0,4)!=='2023'){state.cutoff='2023-07-01';state.congress=118;$('congress').value='118';}
  if(mode==='research')await research();else await load();
}
let config={today:'2026-10-24'};
document.querySelectorAll('[data-mode]').forEach(b=>b.onclick=()=>mode(b.dataset.mode));
document.querySelectorAll('[data-view]').forEach(b=>b.onclick=()=>{state.view=b.dataset.view;renderBills();});
$('search').oninput=renderBills;$('topic').onchange=renderBills;$('watch-only').onchange=renderBills;
$('dataset').onchange=async()=>{state.dataset=$('dataset').value;state.selected=null;state.cutoff=state.dataset==='demo'?'2023-07-01':config.today;state.congress=state.dataset==='demo'?118:119;$('congress').value=String(state.congress);collectionLabel();if(state.mode==='research')await research();else await load();};
$('congress').onchange=()=>{state.congress=Number($('congress').value);state.cutoff=state.mode==='monitor'?config.today:`${1787+state.congress*2}-07-01`;load();};
$('cutoff').onchange=()=>{if(!$('cutoff').value)return;state.cutoff=$('cutoff').value;load();};
$('timeline').oninput=()=>{const start=new Date(`${1787+state.congress*2}-01-03T00:00:00Z`);start.setUTCDate(start.getUTCDate()+Number($('timeline').value));$('cutoff-label').textContent=shortDate(start.toISOString());};
$('timeline').onchange=()=>{const start=new Date(`${1787+state.congress*2}-01-03T00:00:00Z`);start.setUTCDate(start.getUTCDate()+Number($('timeline').value));state.cutoff=start.toISOString().slice(0,10);load();};
$('open-import').onclick=()=>{$('import-form').hidden=!$('import-form').hidden;};
$('import-form').onsubmit=async event=>{event.preventDefault();const button=event.currentTarget.querySelector('button');button.disabled=true;$('import-status').textContent='Retrieving and preserving official source…';try{const result=await post(`import?${query()}`,{congress:Number($('import-congress').value),type:$('import-type').value,number:Number($('import-number').value)});$('import-status').textContent=`${result.bill_id}: ${result.status}.`;state.dataset='official';$('dataset').value='official';state.congress=Number($('import-congress').value);$('congress').value=String(state.congress);state.cutoff=config.today;state.selected=result.bill_id;collectionLabel();await load();toast('Official record imported. Source timing preserved.');}catch(e){$('import-status').textContent=e.message;}finally{button.disabled=false;}};
try{
  config=await api('config');$('cutoff').max=config.today;
  const initial=new URLSearchParams(location.search);
  if(initial.get('embed')==='1')document.body.classList.add('embedded');
  if(initial.get('mode')==='monitor'){await mode('monitor');}
  else {
    state.dataset=initial.get('dataset')==='official'?'official':'demo';$('dataset').value=state.dataset;
    state.congress=Number(initial.get('congress') || (state.dataset==='demo'?118:119));$('congress').value=String(state.congress);
    state.cutoff=initial.get('cutoff') || (state.dataset==='demo'?'2023-07-01':config.today);
    state.selected=initial.get('bill_id');collectionLabel();await load();
  }
}catch(e){error(e.message);}

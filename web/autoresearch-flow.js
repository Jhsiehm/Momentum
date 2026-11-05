// The background worker owns execution. This view edits its limits and observes receipts.
export function createAutoResearch(ctx){
  const {api,$,esc,state,switchPage,buttonPending,navigate}=ctx;
  const root=()=>$('content-page');
  let poll=null;
  const date=value=>value?new Date(value).toLocaleString():'Not yet';
  const readable=value=>String(value||'pending').replaceAll('_',' ');
  async function show(){
    clearTimeout(poll);switchPage('autoresearch','Background research');
    const g=state.generation,current=()=>g===state.generation;
    root().innerHTML='<p class="page-empty" role="status">Loading the research schedule…</p>';
    try{
      const [initial,samples]=await Promise.all([api('autoresearch'),api('sampling/samples')]);if(!current())return;
      let latest=initial;
      const names=new Map(samples.map(s=>[s.id,s.name||'Historical sample']));
      const settings=initial.settings||{};
      root().innerHTML=`<div class="content-header"><div><h1>Background research</h1><p>Run bounded experiments on saved samples, with automatic learning and a record of every decision.</p></div><button data-icon="sample" class="secondary" id="auto-samples">Manage samples</button></div><section class="flow-section" aria-labelledby="auto-status-title"><h2 id="auto-status-title">Research activity</h2><div id="auto-status"></div><p id="auto-connection" class="form-status" role="status"></p></section><section class="flow-section"><h2>Set the schedule</h2><form id="auto-settings" class="flow-form"><label class="check-label"><input type="checkbox" name="enabled" ${settings.enabled?'checked':''}>Enable background experiments</label><fieldset><legend>Samples to research · choose up to 20</legend>${samples.length?samples.map(s=>`<label class="check-label"><input type="checkbox" name="sample_id" value="${esc(s.id)}" ${(settings.sample_ids||[]).includes(s.id)?'checked':''}>${esc(s.name||'Historical sample')}</label>`).join(''):'<p>No saved samples yet. Create a sample in Data & imports before enabling research.</p>'}</fieldset><div class="flow-form-columns"><label>Minutes between cycles<input name="interval_minutes" type="number" min="15" max="10080" required value="${esc(settings.interval_minutes??30)}"></label><label>Maximum runs per cycle<input name="max_runs_per_cycle" type="number" min="1" max="10" required value="${esc(settings.max_runs_per_cycle??1)}"></label></div><label>Daily run limit<input name="daily_run_limit" type="number" min="1" max="100" required value="${esc(settings.daily_run_limit??10)}"></label><p class="run-note">Each sample is checked at ${(initial.checkpoint_ages||[90,180,365]).map(n=>esc(n)).join(', ')} days after introduction. Evidence checks still apply. Blocked samples need source evidence or human audit; a schedule cannot make them eligible.</p><div class="flow-actions"><button data-icon="save" class="primary">Save schedule</button><span id="auto-save-status" class="form-status" role="status"></span></div><p class="run-note">Uncheck Enable background experiments and save to pause. The local server must remain running. This worker uses saved records and local models; it makes no external source requests or paid language-model calls.</p></form></section><section class="flow-section"><div class="flow-heading"><h2>Experiment queue</h2><button data-icon="refresh" class="table-action" id="auto-refresh">Refresh activity</button></div><p class="run-note">Open a session to inspect its fixed and adaptive results. Repeated evidence does not become new validation.</p><div id="auto-jobs"></div></section>`;
      $('auto-samples').onclick=()=>navigate('data');
      function renderStatus(data){
        latest=data;const active=data.settings?.enabled;
        const jobs=data.jobs||[];
        $('auto-status').innerHTML=`<p><strong>${active?'Schedule enabled':'Schedule paused'}</strong>${data.scheduler_running?' · Worker running':' · Worker not running'}</p><dl class="session-spec"><div><dt>Daily budget</dt><dd>${esc(data.daily_used??0)} used · ${esc(data.daily_remaining??0)} remaining</dd></div><div><dt>Last cycle</dt><dd>${esc(date(data.last_cycle?.finished_at||data.last_cycle?.started_at))}${data.last_cycle?.status?' · '+esc(readable(data.last_cycle.status)):''}</dd></div><div><dt>Next cycle</dt><dd>${active?esc(data.next_due?date(data.next_due):'Waiting for the next worker check'):'Paused'}</dd></div></dl><p class="run-note">${esc(data.runtime_note||'Work continues while the local server is running.')}</p>${data.last_cycle?.message?`<p class="run-note">${esc(data.last_cycle.message)}</p>`:''}`;
        const target=$('auto-jobs'),focus=document.activeElement;
        // Avoid replacing the focused queue action during an automatic refresh.
        if(!target.contains(focus)){
          target.innerHTML=jobs.length?`<div class="flow-list">${jobs.map(j=>`<article class="collection-row"><div><h3>${esc(names.get(j.sample_id)||'Historical sample')} · ${esc(j.age_days)}-day checkpoint</h3><p><strong>${esc(readable(j.status))}</strong> · Created ${esc(date(j.created_at))}</p>${j.message?`<p>${esc(j.message)}</p>`:''}${j.started_at||j.finished_at?`<p>${j.finished_at?'Finished':'Started'} ${esc(date(j.finished_at||j.started_at))}</p>`:''}</div><div class="flow-actions">${j.session_id?`<button data-icon="experiment" class="secondary" data-auto-session="${esc(j.session_id)}">Open session</button>`:''}<button data-icon="audit" class="table-action" data-auto-sample="${esc(j.sample_id)}">Review sample</button></div></article>`).join('')}</div>`:'<p class="page-empty">No experiments queued yet. Choose your samples and enable the schedule to start.</p>';
          target.querySelectorAll('[data-auto-session]').forEach(b=>b.onclick=()=>navigate('session',{id:b.dataset.autoSession}));
          target.querySelectorAll('[data-auto-sample]').forEach(b=>b.onclick=()=>navigate('sample',{id:b.dataset.autoSample}));
        }
      }
      function schedulePoll(){clearTimeout(poll);if(current()&&(latest.settings?.enabled||(latest.jobs||[]).some(j=>['queued','running'].includes(j.status))))poll=setTimeout(refresh,5000);}
      async function refresh(){
        clearTimeout(poll);if(!current())return;
        try{const data=await api('autoresearch');if(!current())return;renderStatus(data);$('auto-connection').textContent='';}
        catch(e){if(!current())return;$('auto-connection').textContent='Could not refresh activity: '+e.message+'. Your form changes are preserved.';}
        schedulePoll();
      }
      renderStatus(initial);schedulePoll();$('auto-refresh').onclick=refresh;
      $('auto-settings').onsubmit=async e=>{
        e.preventDefault();const form=e.currentTarget,button=form.querySelector('button'),status=$('auto-save-status');
        const config={enabled:form.elements.enabled.checked,sample_ids:[...form.querySelectorAll('[name="sample_id"]:checked')].map(input=>input.value),interval_minutes:Number(form.elements.interval_minutes.value),max_runs_per_cycle:Number(form.elements.max_runs_per_cycle.value),daily_run_limit:Number(form.elements.daily_run_limit.value)};
        if(config.enabled&&!config.sample_ids.length){status.textContent='Choose at least one saved sample before enabling research.';return;}
        if(config.sample_ids.length>20){status.textContent='Choose no more than 20 samples per schedule.';return;}
        buttonPending(button,true,'Saving schedule…');status.textContent='';
        try{await api('autoresearch/settings',config);if(!current())return;status.textContent=config.enabled?'Schedule saved. The next cycle time is shown above.':'Schedule paused. Any work already running may finish.';await refresh();}
        catch(e){if(current())status.textContent=e.message;}
        finally{if(current())buttonPending(button,false,'Save schedule');}
      };
    }catch(e){if(!current())return;root().innerHTML=`<div class="page-empty" role="alert"><h2>Could not load background research</h2><p>${esc(e.message)}</p><button data-icon="retry" id="auto-retry" class="secondary">Try again</button></div>`;$('auto-retry').onclick=show;}
  }
  return {show};
}

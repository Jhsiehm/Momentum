export function createLearningFlow({api,$,esc,state,switchPage,navigate}){
  const number=n=>n==null?'Unavailable':Number(n).toFixed(5);
  const percent=n=>n==null?'Unavailable':`${(n*100).toFixed(1)}%`;
  const readable=s=>String(s||'Not trained').replaceAll('_',' ');
  async function show({dataset='official'}={}){
    switchPage('learning','Model learning');const generation=state.generation;
    const current=()=>state.page==='learning'&&state.generation===generation;
    const root=$('content-page');root.innerHTML='<p class="page-empty" role="status">Loading saved learning runs…</p>';
    try{
      const data=await api('learning?dataset='+encodeURIComponent(dataset));if(!current())return;
      root.innerHTML=`<div class="research-page"><div class="consumer-heading"><div><h1>Model learning</h1><p>Train forecasting weights on earlier outcomes. Check the result before trusting an update.</p></div></div>
      <section class="consumer-section"><label>Evidence type <select id="learning-dataset"><option value="official" ${dataset==='official'?'selected':''}>Official bill evidence</option><option value="demo" ${dataset==='demo'?'selected':''}>Synthetic demonstration</option></select></label>
      <p class="run-note">${dataset==='demo'?'Fictional evidence tests the workflow. These scores do not measure real-world prediction skill.':'Official data must pass historical availability and audit checks before training.'}</p>
      <div class="consumer-actions"><button id="learning-new" class="primary">Prepare training session</button><button id="learning-schedule" class="secondary">Automatic learning settings</button></div>
      <p class="run-note">New eligible research sessions refit local forecasting weights. The chat provider’s model is unchanged. Saved predictions remain locked; experimental updates do not replace live forecasts.</p></section>
      <section id="learning-detail" class="consumer-section" aria-live="polite"></section><section class="consumer-section"><h2>Training history</h2><p>Compare adaptive and fixed weights on the same cases. Lower Brier loss is better. A lower development score alone does not establish improvement.</p><p class="run-note">${esc(data.note)}</p>
      <div>${data.sessions.length?data.sessions.map(s=>`<article class="research-result"><div><h3>${esc(s.title)}</h3><p>${esc(new Date(s.created_at).toLocaleString())}</p><p>${esc(readable(s.learning_status||s.status))} · ${esc(s.trained_cases)} fitted cases · ${esc(s.adjusted_cases)} changed configurations${s.reused?' · Reused evidence':''}</p><p>Adaptive ${number(s.metrics?.brier)} · Fixed ${number(s.fixed_metrics?.brier)}</p>${s.blockers.length?`<p>${esc(s.blockers.join(' '))}</p>`:''}</div><button class="secondary" data-learning-id="${esc(s.id)}">Inspect training</button></article>`).join(''):'<p class="page-empty">No research sessions in this view. Prepare a session from a saved collection, or use a synthetic demonstration to explore the workflow.</p>'}</div></section>
      </div>`;
      $('learning-dataset').onchange=e=>show({dataset:e.target.value});
      $('learning-new').onclick=()=>navigate('sessions');$('learning-schedule').onclick=()=>navigate('autoresearch');
      let selection=0;
      root.querySelectorAll('[data-learning-id]').forEach(b=>b.onclick=()=>inspect(b.dataset.learningId));
      async function inspect(id){
        const request=++selection;const target=$('learning-detail');target.innerHTML='<p role="status">Loading weights and evidence…</p>';
        try{const detail=await api('learning/detail?id='+encodeURIComponent(id));if(!current()||request!==selection)return;render(detail);target.querySelector('h2').focus({preventScroll:true});target.scrollIntoView({block:'start'});}
        catch(e){if(current()&&request===selection)target.innerHTML=`<p role="alert">${esc(e.message)}</p>`;}
      }
      function render(d){
        const target=$('learning-detail');
        target.innerHTML=`<h2 tabindex="-1">${esc(d.title)}</h2><p>Experimental ${d.dataset==='demo'?'synthetic':'official-evidence'} model · Target: this bill becomes law by the end of its Congress.</p><p>${esc(d.note||'This frozen session has not produced an adaptive model yet.')}</p>
        <div class="consumer-actions"><button id="learning-run" class="primary" ${d.blockers.length||d.learning_status?'disabled':''}>${d.learning_status?'Training saved':'Train and evaluate'}</button><button id="learning-session" class="secondary">Open research session</button><a class="table-action" href="/api/session/export?id=${encodeURIComponent(d.id)}" download="learning-bundle.json">Export evidence and models</a></div><p id="learning-run-status" role="status"></p>
        ${d.blockers.length?`<ul>${d.blockers.map(b=>`<li>${esc(b)}</li>`).join('')}</ul>`:''}
        ${d.cases.length?`<label>Bill checkpoint <select id="learning-case">${d.cases.map((c,i)=>`<option value="${i}">${esc(c.bill_id)} · ${esc(c.cutoff||'Unknown cutoff')}</option>`).join('')}</select></label><div id="learning-weights"></div>`:'<p>No weight snapshots are available. Complete an eligible research session to fit and compare models.</p>'}`;
        $('learning-session').onclick=()=>navigate('session',{id:d.id});
        $('learning-run').onclick=async()=>{
          const b=$('learning-run'),status=$('learning-run-status');b.disabled=true;status.textContent='Training on frozen evidence…';
          try{const updated=await api('learning/train',{id:d.id});if(!current()||!target.contains(b))return;render(updated);target.querySelector('h2').focus({preventScroll:true});$('learning-run-status').textContent='Saved. Refresh training history to see the latest scores.';}
          catch(e){if(current()&&target.contains(b)){status.textContent=e.message;b.disabled=false;}}
        };
        function draw(index){
          const c=d.cases[index];
          $('learning-weights').innerHTML=`<p><strong>${esc(readable(c.status))}</strong> · ${esc(c.reason||'')}</p><p>Evidence cutoff: ${esc(c.cutoff||'Unavailable')}.</p><p>Fixed prediction ${percent(c.fixed_probability)} · Adaptive prediction ${percent(c.probability)} · Outcome ${c.outcome==null?'Unknown':c.outcome===1?'Enacted':'Not enacted'}</p>
          ${c.weights.length?`<p>Feature policy: ${esc(c.feature_policy)} · Regularization: ${esc(c.l2)}</p><p class="run-note">Coefficients act on standardized inputs and log-odds. Positive values raise the estimate with other inputs held fixed; these are associations, not causal effects. Hash bins may combine unrelated words. Fixed and adaptive scales can differ, so coefficient differences are not an importance score.</p>
          <div class="learning-table" tabindex="0" role="region" aria-label="Model coefficient table"><table><thead><tr><th scope="col">Feature</th><th scope="col">Fixed coefficient</th><th scope="col">Adaptive coefficient</th></tr></thead><tbody>${c.weights.map(w=>`<tr><th scope="row">${esc(w.feature)}</th><td>${number(c.fixed_weights.find(f=>f.feature===w.feature)?.coefficient)}</td><td>${number(w.coefficient)}</td></tr>`).join('')}</tbody></table></div>`:'<p>No adaptive weights fitted for this checkpoint. The original prediction is retained.</p>'}
          ${c.inner_validation?`<details><summary>Training and validation evidence</summary><p>${esc(c.inner_validation.train_ids.length)} training families · ${esc(c.inner_validation.validation_ids.length)} validation bills · Validation Congress ${esc(c.inner_validation.validation_congress)}</p><p>Training labels available by ${esc(c.inner_validation.label_availability_cutoff)}.</p><p>Target outcomes are used only for scoring, never to choose weights for that target.</p></details>`:''}`;
        }
        if(d.cases.length){$('learning-case').onchange=e=>draw(Number(e.target.value));draw(0);}
      }
    }catch(e){if(current()){root.innerHTML=`<p role="alert">Could not load model learning: ${esc(e.message)}</p><button id="learning-retry">Try again</button>`;$('learning-retry').onclick=()=>show({dataset});}}
  }
  return {show};
}

import {workingMarkup,mountWorkingVisuals,clearWorkingVisuals,activityMarkup} from './work-visual.js';
const labels={read:'Read dated bill publications',audit:'Check source timestamps and provenance',experiment:'Reproduce the frozen cohort',respond:'Prepare the research summary'};
const message={id:'motion-preview',created_at:new Date().toISOString(),status:'running',activity:[]};
function show(phase){
  document.querySelectorAll('[data-phase]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.phase===phase)));
  if(phase==='complete'){message.status='completed';message.activity=message.activity.map(s=>({...s,status:'completed'}));clearWorkingVisuals();document.querySelector('#preview').innerHTML='<p>Preview complete. Real results appear here when the research finishes.</p>'+activityMarkup(message);return;}
  message.status='running';const order=['read','audit','experiment','respond'];message.activity=order.slice(0,order.indexOf(phase)+1).map(p=>({phase:p,label:labels[p],status:p===phase?'running':'completed'}));
  document.querySelector('#preview').innerHTML=workingMarkup(message);mountWorkingVisuals(document.querySelector('#preview'));
}
document.querySelectorAll('[data-phase]').forEach(b=>b.onclick=()=>show(b.dataset.phase));show('audit');

// A decorative point cloud. Only server-recorded activity supplies progress text.
const escapeText=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const phases={read:'Reading sources',audit:'Checking evidence',experiment:'Running experiment',respond:'Preparing response'};
const runtimes=new Map();
let paused=false;
try{paused=localStorage.getItem('research-motion-paused')==='true';}catch{}
const reduced=matchMedia('(prefers-reduced-motion: reduce)');
let frame=0,last=0,timer=0;
const points=Array.from({length:3000},(_,i)=>{
  // Fixed sampling keeps the cloud stable across phase changes and rerenders.
  const u=((i*0.61803398875)%1),v=((i*0.754877666)%1),face=i%6;
  const a=(u-.5)*1.6,b=(v-.5)*1.6;
  const cube=face<2?[face?-.8:.8,a,b]:face<4?[a,face===2?-.8:.8,b]:[a,b,face===4?-.8:.8];
  const sheet=i%3, paper=[a*.82,b,(sheet-1)*.38];
  const column=i%4,h=[.55,1.05,.8,1.5][column], x=(column-1.5)*.46;
  const chart=face<2?[x+(face?.16:-.16),-.8+u*h,b*.33]:face<4?[x+(u-.5)*.32,face===2?-.8:-.8+h,b*.33]:[x+(u-.5)*.32,-.8+v*h,face===4?-.27:.27];
  const ring=[Math.cos(u*Math.PI*2)*(.58+v*.32),Math.sin(u*Math.PI*2)*(.58+v*.32),(i%5-2)*.15];
  return {cube,paper,chart,ring,seed:u};
});
export function workingMarkup(message){
  const steps=message.activity||[],active=steps.filter(s=>s.status==='running').at(-1),phase=active?.phase||'respond';
  const current=active?.label||message.content||'Preparing response…';
  return `<div class="work-panel" data-work-id="${escapeText(message.id)}" data-phase="${escapeText(phase)}" data-started="${escapeText(message.created_at)}"><div class="work-art"><canvas class="work-canvas" aria-hidden="true"></canvas></div><div class="work-copy"><div class="work-heading"><strong>${escapeText(phases[phase]||'Working on your request')}</strong><span class="work-elapsed" aria-hidden="true"></span></div><ol class="work-trail" aria-label="Research activity">${steps.filter(s=>s.status!=='running').slice(-3).map(s=>`<li class="${s.status==='completed'?'done':'issue'}"><span aria-hidden="true">${s.status==='completed'?'✓':'!'}</span>${escapeText(s.label)}${s.status==='failed'?' — failed':s.status==='blocked'?' — blocked':''}</li>`).join('')}</ol><p class="work-current">${escapeText(current)}</p><div class="work-controls"><span>Live activity · elapsed time, not an ETA</span><button type="button" class="work-pause" aria-pressed="${paused}">${paused?'Resume visual':'Pause visual'}</button></div></div></div>`;
}
export function activityMarkup(message){
  if(!message.activity?.length||message.status==='running')return '';
  return `<details class="work-record"><summary>Research activity · ${message.activity.length} steps</summary><ol>${message.activity.map(s=>`<li><span>${escapeText(s.label)}</span><small>${escapeText(s.status==='running'?'Interrupted':s.status)}</small></li>`).join('')}</ol></details>`;
}
function shape(phase){return phase==='read'?'paper':phase==='experiment'?'chart':phase==='audit'?'cube':'ring';}
function paint(r,time){
  const canvas=r.canvas,ctx=canvas.getContext('2d');if(!ctx)return;
  const width=canvas.clientWidth,height=canvas.clientHeight;if(!width||!height)return;
  const dpr=Math.min(devicePixelRatio||1,2);
  if(canvas.width!==Math.round(width*dpr)||canvas.height!==Math.round(height*dpr)){canvas.width=Math.round(width*dpr);canvas.height=Math.round(height*dpr);}
  ctx.setTransform(dpr,0,0,dpr,0,0);ctx.clearRect(0,0,width,height);
  const still=paused||reduced.matches;
  r.visualTime=(r.visualTime||0)+(still?0:Math.min(50,time-(r.lastPaint||time)));r.lastPaint=time;
  const angle=.5+(reduced.matches?0:r.visualTime*.00016),tilt=-.25;
  const blend=still?1:Math.min(1,(time-r.changed)/850),eased=1-Math.pow(1-blend,3),scale=Math.min(width,height)*.34;
  const cloud=[];
  for(let i=0;i<points.length;i++){
    const p=points[i],a=p[r.previous],b=p[r.shape];
    let x=a[0]+(b[0]-a[0])*eased,y=a[1]+(b[1]-a[1])*eased,z=a[2]+(b[2]-a[2])*eased;
    if(i%19===0&&!still){const drift=Math.sin(r.visualTime*.0006+p.seed*20)*.16;x+=drift;z+=drift;}
    const rx=x*Math.cos(angle)+z*Math.sin(angle),rz=-x*Math.sin(angle)+z*Math.cos(angle);
    const ry=y*Math.cos(tilt)-rz*Math.sin(tilt),depth=y*Math.sin(tilt)+rz*Math.cos(tilt),perspective=3.9/(3.9-depth);
    cloud.push([width/2+rx*scale*perspective,height/2-ry*scale*perspective,depth]);
  }
  cloud.sort((a,b)=>a[2]-b[2]);
  for(const [x,y,z] of cloud){ctx.fillStyle=`rgba(57,70,49,${Math.max(.18,Math.min(.94,.65+z*.22))})`;const size=z>.3?1.8:1.4;ctx.fillRect(x,y,size,size);}
}
function loop(time){
  frame=0;
  if(document.hidden)return;
  if(time-last>32){last=time;for(const r of runtimes.values())if(r.visible){if((!paused&&!reduced.matches)||r.dirty){paint(r,time);r.dirty=false;}const seconds=Math.max(0,Math.floor((Date.now()-r.started)/1000));const label=seconds<60?`${seconds}s`:`${Math.floor(seconds/60)}m ${seconds%60}s`;if(r.elapsed.textContent!==label)r.elapsed.textContent=label;}}
  if([...runtimes.values()].some(r=>r.visible)){if(paused||reduced.matches)timer=setTimeout(()=>{timer=0;wake();},1000);else frame=requestAnimationFrame(loop);}
}
function wake(){if(timer){clearTimeout(timer);timer=0;}if(!frame&&!document.hidden&&[...runtimes.values()].some(r=>r.visible))frame=requestAnimationFrame(loop);}
const observer=new IntersectionObserver(entries=>{for(const entry of entries){const r=runtimes.get(entry.target.dataset.workId);if(r)r.visible=entry.isIntersecting;}wake();},{threshold:.05});
export function mountWorkingVisuals(root){
  const panels=[...root.querySelectorAll('[data-work-id]')],ids=new Set(panels.map(p=>p.dataset.workId));
  for(const [id,r] of runtimes)if(!ids.has(id)){observer.unobserve(r.panel);runtimes.delete(id);}
  for(const panel of panels){
    const id=panel.dataset.workId,newShape=shape(panel.dataset.phase);let r=runtimes.get(id);
    if(r){observer.unobserve(r.panel);panel.querySelector('canvas').replaceWith(r.canvas);if(r.shape!==newShape){r.previous=r.shape;r.shape=newShape;r.changed=performance.now();}}
    else{r={canvas:panel.querySelector('canvas'),shape:newShape,previous:newShape,changed:performance.now(),started:Date.parse(panel.dataset.started)||Date.now(),visible:false};runtimes.set(id,r);}
    r.panel=panel;r.elapsed=panel.querySelector('.work-elapsed');observer.observe(panel);
    const button=panel.querySelector('.work-pause');button.disabled=reduced.matches;if(reduced.matches)button.textContent='Reduced motion';
    button.onclick=()=>{paused=!paused;try{localStorage.setItem('research-motion-paused',String(paused));}catch{}for(const runtime of runtimes.values()){runtime.dirty=true;const b=runtime.panel.querySelector('.work-pause');b.textContent=paused?'Resume visual':'Pause visual';b.setAttribute('aria-pressed',String(paused));}wake();};
    paint(r,performance.now());
  }
  if(!runtimes.size&&frame){cancelAnimationFrame(frame);frame=0;}wake();
}
export function clearWorkingVisuals(){for(const r of runtimes.values())observer.unobserve(r.panel);runtimes.clear();if(timer){clearTimeout(timer);timer=0;}if(frame)cancelAnimationFrame(frame);frame=0;}
document.addEventListener('visibilitychange',()=>{if(document.hidden){if(frame)cancelAnimationFrame(frame);frame=0;if(timer)clearTimeout(timer);timer=0;}else wake();});
window.addEventListener('resize',()=>{for(const r of runtimes.values())r.dirty=true;wake();});
reduced.addEventListener('change',()=>{for(const r of runtimes.values()){r.dirty=true;const b=r.panel.querySelector('.work-pause');b.disabled=reduced.matches;b.textContent=reduced.matches?'Reduced motion':paused?'Resume visual':'Pause visual';}wake();});

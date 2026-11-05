import {icon} from './icons.js';
const cameras=new WeakMap();
// A shared isometric survey plane. Every solid corresponds to one evidence row.
export function renderEvidenceMap(host, rows, selected, esc, onSelect){
  const focused=host.contains(document.activeElement)&&document.activeElement.hasAttribute('data-map-bill');
  const topics=[...new Set(rows.map(r=>r.topic||'Unclassified'))];
  const groups=topics.map(topic=>({topic,rows:rows.filter(r=>(r.topic||'Unclassified')===topic)}));
  const columns=Math.min(6,Math.max(3,...groups.map(g=>g.rows.length)));
  let width=columns*88+64,depth=18;
  // Small collections retain their topic strips. Larger collections wrap on
  // both ground axes so Fit map does not shrink a single very long slab.
  const wrap=groups.length>4;
  groups.forEach(g=>{
    g.columns=wrap?Math.min(6,Math.max(3,Math.ceil(Math.sqrt(g.rows.length)))):columns;
    g.width=g.columns*88+64;
    g.depth=Math.ceil(g.rows.length/g.columns)*72+65;
  });
  const rowWidth=wrap?Math.max(...groups.map(g=>g.width),Math.sqrt(groups.reduce((area,g)=>area+(g.width+18)*(g.depth+18),0))):width;
  let left=0,rowDepth=0;
  if(wrap)width=0;
  groups.forEach(g=>{
    if(left&&left+g.width>rowWidth){depth+=rowDepth+18;left=0;rowDepth=0;}
    g.left=left;g.start=depth;
    width=Math.max(width,left+g.width);
    rowDepth=Math.max(rowDepth,g.depth);
    if(wrap)left+=g.width+18;
    else{depth+=g.depth+18;rowDepth=0;}
  });
  if(wrap)depth+=rowDepth+18;
  const project=(x,y,z=0)=>[(x-y)*.86,(x+y)*.45-z];
  const point=(x,y,z=0)=>project(x,y,z).join(',');
  const polygon=(points,cls)=>`<polygon class="${cls}" points="${points.map(p=>point(...p)).join(' ')}"/>`;
  const plane=(x,y,w,d,z=0,cls='map-region')=>polygon([[x,y,z],[x+w,y,z],[x+w,y+d,z],[x,y+d,z]],cls);
  const label=(x,y,text,cls)=>{const p=project(x,y);if(cls==='map-count')p[1]+=11;return `<text x="${p[0]}" y="${p[1]}" class="${cls}">${esc(text)}</text>`;};
  const short=id=>id.replace(/^demo-/, '').replace(/^\d+-hr/, 'H.R. ').replace(/^\d+-s/, 'S. ');
  const unit=30;
  let content=polygon([[0,depth,0],[width,depth,0],[width,depth,-9],[0,depth,-9]],'map-base-front')+polygon([[width,0,0],[width,depth,0],[width,depth,-9],[width,0,-9]],'map-base-side')+plane(0,0,width,depth,0,'map-ground');
  content+=plane(0,0,width,depth,.1,'map-survey');
  groups.forEach(g=>{
    content+=plane(g.left+14,g.start,g.width-28,g.depth,0,'map-region');
    content+=label(g.left+g.width-30,g.start+g.depth-19,g.topic,'map-topic');
    content+=label(g.left+g.width-30,g.start+g.depth+1,`${g.rows.length} ${g.rows.length===1?'bill':'bills'}`,'map-count');
  });
  const marks=[];
  groups.forEach(g=>g.rows.forEach((r,i)=>{
    const x=g.left+40+(i%g.columns)*88,y=g.start+24+Math.floor(i/g.columns)*72;
    marks.push({r,x,y});
  }));
  marks.sort((a,b)=>(a.x+a.y)-(b.x+b.y));
  marks.forEach(({r,x,y})=>{
    const stage=r.available?Math.max(0,Math.min(4,Number(r.stage)||0)):0;
    const height=r.available?14+stage*16:5;
    const chosen=r.bill_id===selected;
    const p=project(x+unit/2,y+unit/2,height+18);
    const name=short(r.bill_id);
    content+=`<g class="map-bill ${chosen?'is-selected':''} ${r.available?'':'is-unavailable'}" role="button" tabindex="0" aria-pressed="${chosen}" aria-label="${esc(r.bill_id+', '+r.title+', '+(r.available?r.stage_name:'Evidence unavailable'))}" data-map-bill="${esc(r.bill_id)}"><title>${esc(r.title)} — ${esc(r.available?r.stage_name:'Evidence unavailable')}</title>`;
    content+=plane(x-6,y-6,unit+12,unit+12,.5,'map-footprint');
    content+=polygon([[x,y+unit,0],[x+unit,y+unit,0],[x+unit,y+unit,height],[x,y+unit,height]],'map-face-front');
    content+=polygon([[x+unit,y,0],[x+unit,y+unit,0],[x+unit,y+unit,height],[x+unit,y,height]],'map-face-side');
    content+=plane(x,y,unit,unit,height,'map-face-top');
    content+=`<path class="map-leader" d="M${p[0]},${p[1]+4}v12"/><rect class="map-bill-label" x="${p[0]-Math.max(34,name.length*3.7)}" y="${p[1]-13}" width="${Math.max(68,name.length*7.4)}" height="20"/><text class="map-bill-name" x="${p[0]}" y="${p[1]+1}">${esc(name)}</text></g>`;
  });
  const bounds={x:-depth*.86-35,y:-100,w:(width+depth)*.86+70,h:(width+depth)*.45+145};
  host.innerHTML=`<div class="evidence-map"><div class="map-toolbar"><span>One block per bill · grouped by topic</span><div><button type="button" data-map-zoom="out" aria-label="Zoom out">${icon('zoomOut')}</button><button type="button" data-map-zoom="fit">${icon('fit')}Fit map</button><button type="button" data-map-zoom="in" aria-label="Zoom in">${icon('zoomIn')}</button></div></div><svg class="map-scene" viewBox="${bounds.x} ${bounds.y} ${bounds.w} ${bounds.h}" role="group" aria-label="Isometric evidence map. Select a bill to inspect it. Use arrow keys to move between bills."><defs><pattern id="map-dots" width="5" height="5" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r=".45" fill="#777d68" opacity=".48"/></pattern></defs>${content}</svg><div class="map-caption"><span><i></i>Recorded stage</span><span><i class="map-selected-key"></i>Selected bill</span><span>Drag to pan · + / − to zoom</span></div></div>`;
  const svg=host.querySelector('svg.map-scene'),cached=cameras.get(host),key=JSON.stringify(bounds);let view=cached?.key===key?{...cached.view}:{...bounds},drag=null,moved=false;
  const update=()=>{svg.setAttribute('viewBox',`${view.x} ${view.y} ${view.w} ${view.h}`);cameras.set(host,{key,view:{...view}});};update();
  const zoom=f=>{const w=Math.max(bounds.w/4,Math.min(bounds.w*1.5,view.w*f)),h=w*bounds.h/bounds.w;view={x:view.x+(view.w-w)/2,y:view.y+(view.h-h)/2,w,h};update();};
  host.querySelectorAll('[data-map-zoom]').forEach(b=>b.onclick=()=>{if(b.dataset.mapZoom==='fit'){view={...bounds};update();}else zoom(b.dataset.mapZoom==='in'?.8:1.25);});
  const buttons=[...host.querySelectorAll('[data-map-bill]')];
  buttons.forEach((b,i)=>{
    b.onclick=()=>{if(!moved)onSelect(b.dataset.mapBill);};
    b.onkeydown=e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();onSelect(b.dataset.mapBill);}else if(['ArrowRight','ArrowDown','ArrowLeft','ArrowUp','Home','End'].includes(e.key)){e.preventDefault();const next=e.key==='Home'?0:e.key==='End'?buttons.length-1:(i+(['ArrowRight','ArrowDown'].includes(e.key)?1:-1)+buttons.length)%buttons.length;buttons[next].focus();}};
  });
  svg.onpointerdown=e=>{if(e.button!==0)return;moved=false;drag={x:e.clientX,y:e.clientY,view:{...view}};};
  svg.onpointermove=e=>{if(!drag)return;const dx=e.clientX-drag.x,dy=e.clientY-drag.y;if(Math.abs(dx)+Math.abs(dy)<5&&!moved)return;moved=true;svg.setPointerCapture(e.pointerId);const scale=1/svg.getScreenCTM().a;view={...drag.view,x:drag.view.x-dx*scale,y:drag.view.y-dy*scale};update();};
  svg.onpointerup=()=>{drag=null;};svg.onpointercancel=()=>{drag=null;};
  if(focused)buttons.find(b=>b.dataset.mapBill===selected)?.focus({preventScroll:true});
}

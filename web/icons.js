/* Workspace marks drawn on one 24-unit grid. Labels belong to the host control. */
const shapes = Object.freeze({
  workspace:'<path d="M3 20V10h5v10M8 20V4h7v16M15 20v-7h6v7M2 20h20"/>',
  chat:'<path d="M4 4h16v12H9l-5 4V4Z"/><path d="M8 8h8M8 12h5"/>',
  collection:'<path d="M4 7h13v13H4zM8 4h12v13M8 11h5M8 15h5"/>',
  explore:'<path d="m3 10 6-4 6 3 6-4v13l-6 3-6-3-6 3V10ZM9 6v12M15 9v12M5 13l2-1M17 12l2-1"/>',
  experiment:'<path d="M3 20h18M5 17v-5h5v5M14 17V6h5v11M5 8l4-4 7 1"/>',
  compare:'<path d="M12 3v18M3 8h6M3 16h6M15 6h6M15 18h6M7 6l2 2-2 2M17 16l-2 2 2 2"/>',
  watch:'<path d="M2 12h4l3-6 5 12 3-6h5"/><circle cx="18" cy="5" r="2"/>',
  data:'<path d="M4 4h16v16H4zM4 10h16M10 4v16M10 15h10"/>',
  sample:'<path d="M4 4h5v5H4zM15 4h5v5h-5zM4 15h5v5H4zM15 15h5v5h-5zM11 6h2M6 11v2M18 11v2M11 18h2"/><path d="m16 17 1 1 2-2"/>',
  import:'<path d="M4 14v6h16v-6M12 3v12M7 10l5 5 5-5"/>',
  download:'<path d="M5 20h14M12 3v12M7 10l5 5 5-5"/>',
  audit:'<path d="M5 3h10l4 4v14H5V3ZM14 3v5h5M8 13l2 2 5-5M8 18h7"/>',
  source:'<path d="M5 3h10l4 4v14H5V3ZM14 3v5h5M8 12h8M8 16h6"/>',
  settings:'<path d="M4 6h16M4 12h16M4 18h16"/><path d="M8 3v6M16 9v6M10 15v6"/>',
  connection:'<path d="m8 4 4 4-4 4-4-4 4-4ZM16 12l4 4-4 4-4-4 4-4ZM10 10l4 4M3 3l3 3M18 18l3 3"/>',
  chevron:'<path d="m9 5 7 7-7 7"/>',
  plus:'<path d="M12 5v14M5 12h14"/>', close:'<path d="m6 6 12 12M6 18 18 6"/>',
  send:'<path d="M12 20V4M6 10l6-6 6 6"/>',
  sidebar:'<rect x="3" y="4" width="18" height="16" rx="1"/><path d="M9 4v16M5 8h2M5 12h2"/>',
  arrowRight:'<path d="M4 12h16M14 6l6 6-6 6"/>', arrowLeft:'<path d="M20 12H4M10 6l-6 6 6 6"/>',
  check:'<path d="m5 12 4 4L19 6"/>', warning:'<path d="m12 3 10 18H2L12 3ZM12 9v5M12 17v.1"/>',
  retry:'<path d="M4 10a8 8 0 1 1 1 8M4 4v6h6"/>', refresh:'<path d="M4 9a8 8 0 0 1 14-4l2 3M20 3v5h-5M20 15a8 8 0 0 1-14 4l-2-3M4 21v-5h5"/>',
  search:'<circle cx="10" cy="10" r="6"/><path d="m15 15 6 6"/>',
  filter:'<path d="M3 5h18l-7 8v6l-4 2v-8L3 5Z"/>',
  save:'<path d="M4 3h13l3 3v15H4V3ZM8 3v6h8V3M8 21v-7h8v7"/>',
  clock:'<circle cx="12" cy="12" r="9"/><path d="M12 6v6l4 2"/>',
  map:'<path d="m3 10 6-4 6 3 6-4v13l-6 3-6-3-6 3V10ZM9 6v12M15 9v12"/>',
  table:'<rect x="3" y="4" width="18" height="16" rx="1"/><path d="M3 10h18M3 15h18M9 4v16"/>',
  flat:'<path d="M4 5h16M4 12h16M4 19h16M4 5v2M4 12v2M4 19v2"/>',
  zoomIn:'<circle cx="10" cy="10" r="6"/><path d="m15 15 6 6M7 10h6M10 7v6"/>',
  zoomOut:'<circle cx="10" cy="10" r="6"/><path d="m15 15 6 6M7 10h6"/>',
  fit:'<path d="M8 3H3v5M16 3h5v5M21 16v5h-5M8 21H3v-5M8 8h8v8H8z"/>'
});
export const iconNames=Object.freeze(Object.keys(shapes));
export function icon(name,{className='',size=20}={}) {
  if(!Object.hasOwn(shapes,name))throw new Error(`Unknown workspace icon: ${name}`);
  const cls=String(className).replace(/[^a-zA-Z0-9_ -]/g,'');
  const px=Number.isFinite(Number(size))?Math.max(12,Math.min(96,Number(size))):20;
  return `<svg class="workspace-icon ${cls}" width="${px}" height="${px}" viewBox="0 0 24 24" aria-hidden="true" focusable="false">${shapes[name]}</svg>`;
}
export function mountIcons(root=document){
  root.querySelectorAll('summary').forEach(el=>{if(!el.dataset.icon)el.dataset.icon='chevron';});
  root.querySelectorAll('[data-icon]').forEach(el=>{
    if(el.querySelector('.workspace-icon'))return;
    if(Object.hasOwn(shapes,el.dataset.icon))el.insertAdjacentHTML('afterbegin',icon(el.dataset.icon));
  });
}
if(typeof document!=='undefined')mountIcons();

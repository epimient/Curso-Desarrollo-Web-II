// ─── STATE ───
let navStack = [];
let sidebarVisible = window.innerWidth > 768;

// ─── BUILD LANDING ───
function buildLanding(){
  const root = document.getElementById('landing-view');
  root.innerHTML = `
    <div class="hero-section">
      <div class="badge">Curso 2026</div>
      <h1>Desarrollo Web&nbsp;II&nbsp;<span>FastAPI</span></h1>
      <p class="sub">De cero a producci&oacute;n en 13 semanas &middot; 4 unidades &middot; APIs REST profesionales</p>
      <div class="meta">
        <span><span class="lab">Docente:</span> Ing. Eduardo Pimienta</span>
        <span><span class="lab">Nivel:</span> Intermedio</span>
        <span><span class="lab">Stack:</span> FastAPI + SQLAlchemy + Render</span>
      </div>
      <div class="hero-stats">
        <div class="hero-stat"><span class="num">13</span><span class="lab">Clases</span></div>
        <div class="hero-stat"><span class="num">4</span><span class="lab">Unidades</span></div>
        <div class="hero-stat"><span class="num">41+</span><span class="lab">Tests</span></div>
        <div class="hero-stat"><span class="num">96%</span><span class="lab">Coverage</span></div>
      </div>
    </div>
  `;
  UNITS.forEach(u => {
    const sec = document.createElement('section');
    sec.className = 'unit-section u'+u.id;
    const gridClass = u.classes.length>4 ? 'c5' : (u.classes.length<3 ? 'c2' : '');
    sec.innerHTML = `
      <div class="unit-header">
        <span class="tag">Unidad ${u.id} &mdash; ${u.name}</span>
        <div class="line"></div>
      </div>
      <div class="cards-grid ${gridClass}">
        ${u.classes.map(c => `
          <div class="card" data-unit="${u.id}" data-class="${c.n}">
            <div class="card-num">${String(c.n).padStart(2,'0')}</div>
            <h3>${c.title}</h3>
            <p class="desc">${c.desc}</p>
            <div class="tags">${c.tags.map(t => `<span>${t}</span>`).join('')}</div>
          </div>
        `).join('')}
      </div>
    `;
    root.appendChild(sec);
    sec.querySelectorAll('.card').forEach(el => {
      el.addEventListener('click', () => {
        const cn = parseInt(el.dataset.class);
        const cls = findClass(cn);
        if(cls) openSlides(cls);
      });
    });
  });

  const resSec = document.createElement('section');
  resSec.className = 'resources-section';
  resSec.innerHTML = `<h2>Recursos bibliogr&aacute;ficos</h2><div class="res-grid">` +
    RESOURCES.map(r => `
      <div class="res-card"><h4>${r.cat}</h4><ul>${r.links.map(l => `<li><a href="${l.u}" target="_blank" rel="noopener">${l.l}</a></li>`).join('')}</ul></div>
    `).join('') +
    `</div>`;
  root.appendChild(resSec);
}

// ─── BUILD SIDEBAR ───
function buildSidebar(){
  const tree = document.getElementById('sidebarTree');
  let html = '';
  UNITS.forEach(u => {
    html += `<div class="tree-group">`;
    html += `<div class="tree-unit">Unidad ${u.id} &mdash; ${u.name}</div>`;
    u.classes.forEach(c => {
      const unitClass = 'u'+u.id;
      html += `<details class="tree-item ${unitClass}" data-class="${c.n}">
        <summary><span class="folder-icon">&#128193;</span><span class="num">${String(c.n).padStart(2,'0')}</span><span class="name">${c.title}</span><span class="arrow">&#9654;</span></summary>
        <div class="tree-subs">
          <a href="#" data-action="slides" data-class="${c.n}"><span class="icon">&#9654;</span> Slides</a>
          <a href="#" data-action="doc" data-class="${c.n}"><span class="icon">&#128196;</span> Documento</a>
          <a href="#" data-action="example" data-class="${c.n}"><span class="icon">&#128736;</span> Ejemplo guiado</a>
          <a href="#" data-action="exercises" data-class="${c.n}"><span class="icon">&#128221;</span> Ejercicios</a>
          <a href="#" data-action="faq" data-class="${c.n}"><span class="icon">&#10067;</span> FAQ</a>
        </div>
      </details>`;
    });
    html += `</div>`;
  });
  html += `<div class="tree-resources"><details>
    <summary>&#128218; Recursos bibliogr&aacute;ficos</summary>
    <div class="subs">
      ${RESOURCES.map(r => `<a href="${r.links[0].u}" target="_blank" rel="noopener"><span class="icon">&#128279;</span> ${r.cat}</a>`).join('')}
    </div>
  </details></div>`;
  tree.innerHTML = html;

  tree.querySelectorAll('.tree-subs a').forEach(a => {
    a.addEventListener('click', e => {
      e.preventDefault();
      const cls = parseInt(a.dataset.class);
      const action = a.dataset.action;
      const c = findClass(cls);
      if(!c) return;
      const dir = './'+c.dir;
      const paths = {
        slides:dir+'/'+c.slides,
        doc:dir+'/'+c.doc,
        example:dir+'/'+c.example,
        exercises:dir+'/'+c.ex,
        faq:dir+'/'+c.faq,
      };
      const url = paths[action]||paths.slides;
      const label = action==='slides'
        ? `${c.n}. ${c.title} &mdash; Slides`
        : `${c.n}. ${c.title} &mdash; ${action.charAt(0).toUpperCase()+action.slice(1)}`;
      if(action==='slides') loadContent(url,label);
      else loadContent(url,label);
      tree.querySelectorAll('.tree-subs a').forEach(x => x.classList.remove('active'));
      a.classList.add('active');
    });
  });

  tree.querySelectorAll('.tree-item > summary').forEach(s => {
    s.addEventListener('click', e => {
      const details = s.closest('details');
      setTimeout(() => {
        const cls = parseInt(details.dataset.class);
        const c = findClass(cls);
        if(c) openSlides(c);
      }, 50);
    });
  });
}

// ─── HELPERS ───
function findClass(n){
  for(const u of UNITS) for(const c of u.classes) if(c.n===n) return c;
  return null;
}

function openSlides(c){
  const url = './'+c.dir+'/'+c.slides;
  loadContent(url,`${c.n}. ${c.title} &mdash; Slides`);
  document.querySelectorAll('.tree-subs a').forEach(x => x.classList.remove('active'));
  const link = document.querySelector(`.tree-subs a[data-class="${c.n}"][data-action="slides"]`);
  if(link) link.classList.add('active');
  const details = document.querySelector(`.tree-item[data-class="${c.n}"]`);
  if(details) details.open = true;
  if(!sidebarVisible) toggleSidebar();
}

function loadContent(url,label){
  const isMd = url.match(/\.md($|\?)/);
  if(isMd) loadMarkdown(url,label);
  else loadIframe(url,label);
}

function loadIframe(url,label){
  const frame = document.getElementById('contentFrame');
  const iframeView = document.getElementById('iframe-view');
  const mdView = document.getElementById('markdown-view');
  const landing = document.getElementById('landing-view');
  mdView.classList.remove('show');
  frame.src = url;
  document.getElementById('iframeLabel').innerHTML = label;
  document.getElementById('topbarPath').textContent = url;
  landing.style.display = 'none';
  iframeView.classList.add('show');
  navStack.push({url,label,type:'html'});
  updateBackBtn();
}

async function loadMarkdown(url,label){
  const mdView = document.getElementById('markdown-view');
  const iframeView = document.getElementById('iframe-view');
  const landing = document.getElementById('landing-view');
  iframeView.classList.remove('show');
  landing.style.display = 'none';
  mdView.classList.add('show');
  document.getElementById('mdLabel').innerHTML = label;
  document.getElementById('topbarPath').textContent = url;
  navStack.push({url,label,type:'md'});
  updateBackBtn();
  document.getElementById('md-content').innerHTML = '<p style="color:var(--text-muted)">Cargando...</p>';
  try{
    const res = await fetch(url);
    if(!res.ok) throw new Error('HTTP '+res.status);
    const md = await res.text();
    const processed = md
      .replace(/:::(\w+)\s*\n([\s\S]*?):::/g,'<div class="callout callout--$1">$2</div>')
      .replace(/\[!(\w+)\]\s*\n([\s\S]*?)(?=\n\n|$)/g,'<div class="callout callout--$1">$2</div>');
    let html = marked.parse(processed,{breaks:true,gfm:true});
    document.getElementById('md-content').innerHTML = html;
    if(typeof hljs!=='undefined'){
      document.querySelectorAll('#md-content pre code').forEach(b => hljs.highlightElement(b));
    }
  }catch(e){
    document.getElementById('md-content').innerHTML =
      '<div class="callout callout--error"><strong>Error al cargar</strong><br>'+e.message+'</div>';
  }
}

function showLanding(){
  const iframeView = document.getElementById('iframe-view');
  const mdView = document.getElementById('markdown-view');
  const landing = document.getElementById('landing-view');
  iframeView.classList.remove('show');
  mdView.classList.remove('show');
  landing.style.display = 'block';
  document.getElementById('topbarPath').textContent = '';
  navStack = [];
  updateBackBtn();
  document.getElementById('contentFrame').src = '';
}

function goBack(){
  if(navStack.length<=1){ showLanding(); return; }
  navStack.pop();
  const prev = navStack[navStack.length-1];
  if(prev){
    const frame = document.getElementById('contentFrame');
    frame.src = prev.url;
    document.getElementById('iframeLabel').innerHTML = prev.label;
    document.getElementById('topbarPath').textContent = prev.url;
  }
  updateBackBtn();
}

function updateBackBtn(){
  document.getElementById('homeBtn').disabled = navStack.length===0;
}

function toggleSidebar(){
  sidebarVisible = !sidebarVisible;
  document.getElementById('sidebar').classList.toggle('hidden');
}

// ─── INIT ───
buildLanding();
buildSidebar();
if(!sidebarVisible) document.getElementById('sidebar').classList.add('hidden');
updateBackBtn();

// ─── EVENT BINDINGS ───
document.getElementById('sidebarToggle').addEventListener('click',toggleSidebar);
document.getElementById('homeBtn').addEventListener('click',showLanding);
document.getElementById('iframeBack').addEventListener('click',goBack);
document.getElementById('mdBack').addEventListener('click',goBack);

document.addEventListener('keydown', e => {
  if(e.key==='Escape') goBack();
});

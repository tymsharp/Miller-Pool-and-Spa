#!/usr/bin/env python3
"""Build the Miller Pool and Spa static site.

Usage: python3 build.py <site_dir> <preview_file> <logo_png>

Writes:
  <site_dir>/index.html and <site_dir>/<slug>/index.html   one real page per folder
  <site_dir>/assets/site.css, site.js, miller-logo.png
  <preview_file>   every page in one file with a hash router, for the Artifact preview
"""
import base64, html, json, os, sys

SITE_DIR, PREVIEW_FILE, LOGO_PNG = sys.argv[1], sys.argv[2], sys.argv[3]
BASE = "https://www.millerpoolandspausa.com"
PHONE = "(805) 492-6991"
TEL = "tel:+18054926991"
EMAIL = "info@millerpoolandspausa.com"
MODE = "site"  # or "preview"

# ---------------------------------------------------------------- helpers

def href(slug, anchor=None):
    """Link to a page. slug '' is the home page."""
    if MODE == "preview":
        return "#" + (slug or "home")
    return ("/" if not slug else f"/{slug}/") + (f"#{anchor}" if anchor else "")

def aid(slug, name):
    """Element id that stays unique when every page shares one file."""
    return f"{name}-{(slug or 'home').replace('/', '-')}"

def logo_src():
    if MODE == "preview":
        return "data:image/png;base64," + LOGO_B64
    return "/assets/miller-logo.png"

LOGO_B64 = base64.b64encode(open(LOGO_PNG, "rb").read()).decode()

# ---------------------------------------------------------------- css

CSS = r"""
/* Miller Pool and Spa. Light, left-aligned, one type family, photo slots where photos go. */
:root{
  --blue:#3f88aa; --blue-dark:#275877; --sky:#eaf6fc; --sky-line:#cfe8f4;
  --yellow:#f8f08c; --yellow-dark:#f0e35a;
  --ink:#222826; --muted:#59676f; --line:#dde4e9; --bg:#ffffff;
  --font:"Lato","Helvetica Neue",Arial,sans-serif;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
[hidden]{display:none!important}
body{margin:0;background:var(--bg);color:var(--ink);font:400 17px/1.65 var(--font);padding-bottom:64px}
h1,h2,h3{font-weight:900;line-height:1.15;margin:0;text-wrap:balance}
h1{font-size:clamp(32px,4.6vw,46px)}
h2{font-size:clamp(26px,3.4vw,32px)}
h3{font-size:19px;font-weight:700}
p{margin:0}
ul,ol{margin:0;padding-left:20px}
a{color:var(--blue)}
img{max-width:100%}
.wrap{max-width:1100px;margin:0 auto;padding-inline:16px}
section{padding-block:60px}
.sky{background:var(--sky)}
.lede{font-size:19px;color:var(--muted)}
.max{max-width:62ch}
.mt{margin-top:12px}
.btn{display:inline-block;font:700 17px/1 var(--font);padding:15px 22px;border-radius:4px;text-decoration:none;border:0;cursor:pointer;text-align:center}
.btn-call{background:var(--yellow);color:var(--ink)}
.btn-call:hover{background:var(--yellow-dark)}
.btn-blue{background:var(--blue);color:#fff}
.btn-blue:hover{background:var(--blue-dark)}
.btn-outline{background:#fff;color:var(--blue);border:2px solid var(--blue);padding:13px 20px}
.btn:focus-visible,input:focus-visible,select:focus-visible,textarea:focus-visible,a:focus-visible,button:focus-visible{outline:3px solid var(--blue);outline-offset:2px}

/* photo slots */
.photo{margin:0;background:#d6e7f0;border-radius:4px;aspect-ratio:4/3;max-width:100%;display:flex;align-items:flex-end;padding:12px 14px;color:#56687a;font-size:13px;line-height:1.4}
.photo.wide{aspect-ratio:16/9}
.photo.tall{aspect-ratio:3/4}
.photo.top{align-items:flex-start}
.photo span{background:rgba(255,255,255,.75);padding:4px 8px;border-radius:3px}

/* header */
.topbar{background:var(--blue-dark);color:#dbeaf3;font-size:14px}
.topbar .wrap{display:flex;justify-content:space-between;gap:12px;padding-block:7px;flex-wrap:wrap}
.topbar a{color:#fff;font-weight:700;text-decoration:none}
header.site{background:#fff;border-bottom:1px solid var(--line);position:sticky;top:env(safe-area-inset-top,0px);z-index:30}
header.site .wrap{display:flex;align-items:center;gap:22px;padding-block:10px;position:relative}
.logo{display:block;line-height:0}
.logo img{height:64px;width:64px;display:block}
nav.main{display:flex;gap:20px;margin-left:auto;font-weight:700;font-size:15px;align-items:center}
nav.main a{color:var(--ink);text-decoration:none}
nav.main a:hover{color:var(--blue)}
.has-sub{position:relative}
.has-sub>a::after{content:"";display:inline-block;margin-left:6px;width:6px;height:6px;border-right:2px solid currentColor;border-bottom:2px solid currentColor;transform:translateY(-3px) rotate(45deg)}
.sub{display:none;position:absolute;top:100%;left:-14px;padding-top:10px;z-index:40}
.sub div{background:#fff;border:1px solid var(--line);box-shadow:0 8px 24px rgba(20,40,60,.14);min-width:250px;padding:8px 0}
.sub a{display:block;padding:9px 16px;font-weight:400;font-size:15px}
.sub a:hover{background:var(--sky)}
.has-sub:hover .sub,.has-sub:focus-within .sub{display:block}
.hdr-call{text-align:right;line-height:1.2;white-space:nowrap}
.hdr-call small{display:block;font-size:12px;color:var(--muted);font-weight:700}
.hdr-call a{font-weight:900;font-size:20px;color:var(--blue-dark);text-decoration:none}
.hdr-btn{padding:12px 16px;font-size:15px}
.burger{display:none;width:44px;height:40px;border:1px solid var(--line);border-radius:4px;background:#fff;position:relative;cursor:pointer;flex:none}
.burger i{position:absolute;left:11px;right:11px;height:2px;background:var(--ink);top:12px}
.burger i:nth-child(2){top:19px}
.burger i:nth-child(3){top:26px}

/* hero */
.hero{padding-block:48px 56px}
.hero .wrap{display:grid;grid-template-columns:1.1fr .9fr;gap:40px;align-items:center}
.hero-text{display:grid;gap:20px}
.hero-cta{display:flex;flex-wrap:wrap;gap:12px;align-items:center}
.hero-note{font-size:15px;color:var(--muted)}
.hero-photo{position:relative}
.rating{position:absolute;left:16px;bottom:-18px;background:#fff;border:1px solid var(--line);border-radius:4px;padding:10px 14px;box-shadow:0 4px 14px rgba(20,40,60,.12);font-size:14px;line-height:1.3}
.rating b{font-size:18px}
.stars{color:#f5a623;letter-spacing:1px}

/* trust band */
.band{background:var(--sky);border-top:1px solid var(--sky-line);border-bottom:1px solid var(--sky-line);padding-block:16px}
.band ul{list-style:none;padding:0;display:flex;flex-wrap:wrap;gap:8px 0;font-weight:700;font-size:15px}
.band li{padding-inline:22px;border-left:1px solid var(--sky-line)}
.band li:first-child{padding-left:0;border-left:0}

/* home: three services */
.svc{display:grid;grid-template-columns:repeat(3,1fr);gap:32px;margin-top:32px}
.svc>div{display:grid;gap:10px;min-width:0;align-content:start}
.svc p{color:var(--muted);font-size:16px}
.svc a.more{font-weight:700}

/* repairs list */
.repairs{display:grid;grid-template-columns:1fr 1fr;gap:0 48px;margin-top:32px}
.repairs>div{padding-block:20px;border-top:1px solid var(--line);display:grid;gap:6px;min-width:0}
.repairs p{color:var(--muted);font-size:16px}
.repairs h3 a{color:var(--ink);text-decoration:none}
.repairs h3 a:hover{color:var(--blue)}
.brand-line{margin-top:28px;font-size:15px;color:var(--muted)}

/* symptom lists on service pages */
.problems{display:grid;grid-template-columns:1fr 1fr;gap:18px 48px;margin:28px 0 0}
.problems>div{padding-top:14px;border-top:1px solid var(--line);min-width:0}
.problems dt{font-weight:700}
.problems dd{margin:4px 0 0;color:var(--muted);font-size:16px}

/* alternating rows */
.row{display:grid;grid-template-columns:1fr 1fr;gap:48px;align-items:center}
.row+.row{margin-top:56px}
.row.flip .photo{order:2}
.row .text{display:grid;gap:16px}
.row h3{font-size:22px;font-weight:900}
.row p{color:var(--muted)}
.row ul{color:var(--muted)}

/* city grid */
.cities{display:grid;grid-template-columns:repeat(3,1fr);gap:16px 32px;margin-top:28px}
.cities>div{padding-top:14px;border-top:1px solid var(--line);min-width:0}
.cities h3{font-size:18px}
.cities p{color:var(--muted);font-size:15px;margin-top:4px}

/* form + contact */
.contact{display:grid;grid-template-columns:1fr 1.1fr;gap:48px;align-items:start}
.contact-info{display:grid;gap:18px}
.contact-info .big{font-weight:900;font-size:30px;color:var(--blue-dark);text-decoration:none}
.contact-info dl{display:grid;grid-template-columns:auto 1fr;gap:6px 16px;margin:0}
.contact-info dt{font-weight:700}
.contact-info dd{margin:0;color:var(--muted)}
form.req{background:#fff;border:1px solid var(--line);border-radius:4px;padding:24px;display:grid;gap:14px}
form.req h3{font-size:22px;font-weight:900}
.f2{display:grid;grid-template-columns:1fr 1fr;gap:14px}
label{display:grid;gap:5px;font-weight:700;font-size:15px}
input,select,textarea{font:inherit;font-size:16px;padding:11px 12px;border:1px solid #b9c6d0;border-radius:4px;background:#fff;color:var(--ink);width:100%}
textarea{min-height:90px;resize:vertical}
.fine{font-size:14px;color:var(--muted)}
.done{background:var(--sky);border-radius:4px;padding:12px 14px;font-weight:700}

/* reviews */
.reviews{display:grid;grid-template-columns:1fr 1fr;gap:28px 48px;margin-top:32px}
.review{margin:0;display:grid;gap:10px;min-width:0}
.review .stars{font-size:15px}
.review blockquote{margin:0;font-size:17px}
.review figcaption{font-size:15px;color:var(--muted)}
.review figcaption b{color:var(--ink)}

/* areas */
.areas{display:grid;grid-template-columns:1fr 1fr;gap:40px;margin-top:28px;align-items:start}
table.zips{border-collapse:collapse;width:100%;font-size:16px}
table.zips th,table.zips td{text-align:left;padding:10px 12px 10px 0;border-bottom:1px solid var(--line);vertical-align:top}
table.zips th{font-size:13px;text-transform:uppercase;letter-spacing:.08em;color:var(--muted)}
table.zips td:first-child{font-weight:900;font-variant-numeric:tabular-nums;white-space:nowrap;color:var(--blue-dark)}
.nearby{list-style:none;padding:0;display:grid;grid-template-columns:1fr 1fr;gap:8px 16px}
.nearby a{font-weight:700}

/* faq */
.faq{display:grid;gap:22px;margin-top:28px;max-width:70ch}
.faq p{color:var(--muted);margin-top:4px}

/* plain text page */
.prose{max-width:68ch;display:grid;gap:16px}
.prose p{color:var(--muted)}
.prose h3{margin-top:12px}

/* blog */
.posts{max-width:70ch;margin-top:28px}
.posts article{padding-block:22px;border-top:1px solid var(--line)}
.posts h2{font-size:22px;margin-top:4px}
.posts h2 a{color:var(--ink);text-decoration:none}
.posts h2 a:hover{color:var(--blue)}
.posts p{color:var(--muted);margin-top:6px}
.post-meta{font-size:13px;color:var(--muted);text-transform:uppercase;letter-spacing:.08em}
.post-meta a{color:var(--muted)}
.post{max-width:70ch;display:grid;gap:16px}
.post h2{font-size:24px;margin-top:14px}
.post ul,.post ol{display:grid;gap:6px}
.post table{border-collapse:collapse;width:100%;font-size:16px}
.post th,.post td{text-align:left;padding:10px 12px 10px 0;border-bottom:1px solid var(--line);vertical-align:top}
.post th{font-size:13px;text-transform:uppercase;letter-spacing:.08em;color:var(--muted)}
.post td:first-child{font-weight:700}
.post td:last-child{white-space:nowrap;font-variant-numeric:tabular-nums}
.post-related{padding:16px 18px;background:var(--sky);border-radius:4px;margin-top:8px}

/* footer */
footer{background:var(--blue-dark);color:#c9dde9;padding-block:36px;font-size:15px}
footer .wrap{display:grid;grid-template-columns:1.4fr 1fr 1fr 1fr;gap:32px}
footer h4{color:#fff;margin:0 0 10px;font-size:15px;text-transform:uppercase;letter-spacing:.08em}
footer .flogo{height:88px;width:88px;display:block;margin-bottom:14px}
footer a{color:#fff;text-decoration:none}
footer a:hover{text-decoration:underline}
footer ul{list-style:none;padding:0;display:grid;gap:6px}
footer .legal{grid-column:1/-1;border-top:1px solid rgba(255,255,255,.15);padding-top:16px;font-size:13px;display:flex;flex-wrap:wrap;gap:8px 24px;justify-content:space-between}

/* mobile call bar */
.mbar{position:fixed;left:0;right:0;bottom:0;z-index:20;background:#fff;border-top:1px solid var(--line);padding:10px 16px calc(10px + env(safe-area-inset-bottom,0px));display:none;gap:10px}
.mbar .btn{flex:1;padding:13px 10px;font-size:16px}

@media (max-width:1100px){.hdr-btn{display:none}}
@media (max-width:900px){
  .burger{display:block;margin-left:auto}
  .hdr-call{margin-left:auto}
  .burger{margin-left:0}
  nav.main{display:none;position:absolute;left:0;right:0;top:100%;background:#fff;border-bottom:1px solid var(--line);flex-direction:column;align-items:stretch;gap:0;padding:4px 16px 16px;margin:0;box-shadow:0 12px 24px rgba(20,40,60,.12)}
  header.site.nav-open nav.main{display:flex}
  nav.main>a,.has-sub>a{display:block;padding:12px 0;border-bottom:1px solid var(--line)}
  .has-sub>a::after{display:none}
  .sub{display:block;position:static;padding:0}
  .sub div{border:0;box-shadow:none;padding:4px 0 8px 14px;min-width:0}
  .sub a{padding:8px 0}
  .hero .wrap,.row,.contact,.areas,.reviews{grid-template-columns:1fr}
  .row.flip .photo{order:0}
  .repairs,.problems{grid-template-columns:1fr;gap:0}
  .problems>div{padding-block:14px}
  .svc,.cities{grid-template-columns:1fr 1fr}
  footer .wrap{grid-template-columns:1fr 1fr}
}
@media (max-width:600px){
  body{font-size:16px}
  section{padding-block:44px}
  .hero{padding-block:32px 48px}
  .f2{grid-template-columns:1fr}
  .topbar .where{display:none}
  .hdr-call small{display:none}
  .hdr-call a{font-size:17px}
  header.site .wrap{gap:12px}
  .logo img{height:48px;width:48px}
  .band li{border-left:0;padding-inline:0 18px}
  .nearby,.svc,.cities{grid-template-columns:1fr}
  footer .wrap{grid-template-columns:1fr}
  .mbar{display:flex}
  .post td:nth-child(2),.post th:nth-child(2){display:none}
}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
"""

JS_COMMON = r"""
(function(){
  var hdr=document.querySelector('header.site');
  var burger=document.querySelector('.burger');
  if(burger){burger.addEventListener('click',function(){
    var open=hdr.classList.toggle('nav-open');
    burger.setAttribute('aria-expanded',open?'true':'false');
  });}
  var forms=document.querySelectorAll('form.req');
  for(var i=0;i<forms.length;i++){forms[i].addEventListener('submit',function(e){
    e.preventDefault();
    var d=e.target.querySelector('.done'); if(d) d.hidden=false;
  });}
})();
"""

JS_ROUTER = r"""
(function(){
  var pages=document.querySelectorAll('.page');
  var hdr=document.querySelector('header.site');
  function show(slug){
    var p=document.getElementById('pg-'+slug); if(!p) return false;
    for(var i=0;i<pages.length;i++){pages[i].hidden=true;}
    p.hidden=false;
    document.title=p.getAttribute('data-title')||document.title;
    hdr.classList.remove('nav-open');
    window.scrollTo(0,0);
    return true;
  }
  function route(){
    var h=(location.hash||'#home').slice(1);
    if(show(h)) return;
    var el=document.getElementById(h);
    if(el){el.scrollIntoView();} else {show('home');}
  }
  document.addEventListener('click',function(e){
    var a=e.target.closest('a[href^="#"]'); if(!a) return;
    var h=a.getAttribute('href').slice(1);
    if(document.getElementById('pg-'+h)){
      e.preventDefault(); show(h);
      try{history.pushState(null,'','#'+h);}catch(x){try{location.hash='#'+h;}catch(y){}}
    } else {
      var el=document.getElementById(h);
      if(el){e.preventDefault(); el.scrollIntoView({behavior:'smooth'});}
    }
  });
  window.addEventListener('hashchange',route);
  window.addEventListener('popstate',route);
  route();
})();
"""

# ---------------------------------------------------------------- data

SERVICES = [
    ("pool-pump-repair", "Pump repair"),
    ("pool-heater-repair", "Heater repair"),
    ("pool-leak-detection", "Leak detection"),
    ("pool-filter-repair", "Filter &amp; equipment"),
    ("salt-system-repair", "Salt systems"),
    ("green-pool-cleanup", "Green pool cleanup"),
]

CITY_LINKS = [
    ("pool-repair-thousand-oaks", "Thousand Oaks &amp; Newbury Park", "Home base. Most calls are minutes away."),
    ("pool-repair-simi-valley", "Simi Valley", "Pumps and filters, mostly. Up the 23 from the shop."),
    ("pool-repair-camarillo", "Camarillo", "Repairs, plus weekly service routes."),
    ("pool-repair-westlake-village", "Westlake Village &amp; Oak Park", "Heaters, automation, salt and leaks on bigger pools."),
    ("pool-repair-calabasas", "Calabasas &amp; Hidden Hills", "Estate pools. Pentair, Jandy and Hayward systems."),
    ("pool-repair-agoura-hills", "Agoura Hills", "Leak detection on hillside lots, and everything else."),
]

REVIEWS = {
    "andreas": ("I used Miller Pool for their leak detection service. Jon and Jarett arrived with big smiles which is always a good start. They had the right gear and very quickly located my leak. These guys are clearly experienced at what they do. If I was to recommend someone for leak detection I would most certainly recommend Miller Pool.", "Andreas Tompros"),
    "michael": ("Professional. Honest. Timely. Good communication. Left backyard clean. Explained the operation of the new heater. Will contact Miller Pool for all of our future pool needs.", "Michael Roy"),
    "jeannie": ("We have been so happy with this pool service! They always show up regularly. Communication has been really good. At one point our full pool sweeper broke and the very next day they were able to get us a new pool sweeper. Thank you!", "Jeannie Nickerson"),
    "jayne": ("They show up same day and time. I love that I can pay online. Their prices are not the cheapest, but you're paying for a licensed and professional company with great communication skills.", "Jayne Miller"),
}

REPAIR_ITEMS = {
    "pump": ("pool-pump-repair", "Pumps and motors", "Pumps that hum and won't start, trip the breaker, leak at the shaft seal or keep losing prime. We rebuild or replace, and we'll tell you when a variable-speed pump makes more sense than another repair on an old single-speed."),
    "heater": ("pool-heater-repair", "Heaters", "Gas heaters and heat pumps from Raypak, Pentair, Hayward and Jandy. Ignition failures, pressure switches, bad sensors, and heat exchangers scaled up by our hard water."),
    "filter": ("pool-filter-repair", "Filters", "Cartridge, DE and sand filters. Cracked tanks, worn multiport valves, and pressure that climbs faster than it should between cleanings."),
    "leak": ("pool-leak-detection", "Leak detection and repair", "If the pool loses more than about a quarter inch a day, it's not evaporation. We pressure-test the plumbing and dye-test the shell, lights and fittings, then fix what we find."),
    "salt": ("salt-system-repair", "Salt systems", "Hayward AquaRite, Pentair IntelliChlor and Jandy AquaPure. Cells that read low after you've added salt, flow sensors, and control boards."),
    "auto": (None, "Automation and pool lights", "Control panels that drop their schedules, apps that lose the pool, and pool or spa lights that won't come on. We repair LED and incandescent fixtures and the wiring behind them."),
    "green": ("green-pool-cleanup", "Green pool cleanup", "Neglected or storm-hit pools brought back to clear water. We check the equipment while we're at it, since a green pool usually means something stopped running."),
    "install": (None, "Equipment installs", "New pumps, heaters, filters and salt systems, sized for the pool. We install what we repair, so there's one company to call afterward."),
}

BUSINESS_LD = {
    "@type": "HomeAndConstructionBusiness",
    "@id": BASE + "/#business",
    "name": "Miller Pool and Spa",
    "url": BASE + "/",
    "telephone": "+1-805-492-6991",
    "email": EMAIL,
    "address": {"@type": "PostalAddress", "addressLocality": "Newbury Park", "addressRegion": "CA", "addressCountry": "US"},
    "areaServed": [{"@type": "City", "name": c} for c in ["Thousand Oaks", "Newbury Park", "Simi Valley", "Camarillo", "Westlake Village", "Oak Park", "Agoura Hills", "Calabasas", "Hidden Hills", "Moorpark"]],
}

# ---------------------------------------------------------------- components

def topbar():
    return f"""
<div class="topbar">
  <div class="wrap">
    <span class="where">Pool repair and weekly service in Thousand Oaks and the Conejo Valley</span>
    <span>Licensed &amp; insured &nbsp;·&nbsp; <a href="{TEL}">{PHONE}</a></span>
  </div>
</div>"""

def header():
    sub = "".join(f'<a href="{href(s)}">{n}</a>' for s, n in SERVICES)
    return f"""
<header class="site">
  <div class="wrap">
    <a class="logo" href="{href('')}"><img src="{logo_src()}" alt="Miller Pool and Spa" width="64" height="64"></a>
    <nav class="main" aria-label="Main">
      <div class="has-sub">
        <a href="{href('pool-repair')}">Repairs</a>
        <div class="sub"><div><a href="{href('pool-repair')}">All pool repair</a>{sub}</div></div>
      </div>
      <a href="{href('pool-service-thousand-oaks')}">Weekly Service</a>
      <a href="{href('service-areas')}">Service Area</a>
      <a href="{href('reviews')}">Reviews</a>
      <a href="{href('about')}">About</a>
      <a href="{href('blog')}">Blog</a>
      <a href="{href('contact')}">Contact</a>
    </nav>
    <div class="hdr-call">
      <small>Call or text</small>
      <a href="{TEL}">{PHONE}</a>
    </div>
    <a class="btn btn-call hdr-btn" href="{href('contact')}">Request service</a>
    <button class="burger" type="button" aria-label="Menu" aria-expanded="false"><i></i><i></i><i></i></button>
  </div>
</header>"""

def footer():
    cities = "".join(f'<li><a href="{href(s)}">{n}</a></li>' for s, n, _ in CITY_LINKS)
    svcs = "".join(f'<li><a href="{href(s)}">{n}</a></li>' for s, n in SERVICES)
    return f"""
<footer>
  <div class="wrap">
    <div>
      <img class="flogo" src="{logo_src()}" alt="" width="88" height="88">
      <h4>Miller Pool and Spa</h4>
      <p>Newbury Park, CA<br><a href="{TEL}">{PHONE}</a><br>{EMAIL}</p>
      <p style="margin-top:12px">CSLB License # (to be added)</p>
    </div>
    <div>
      <h4>Repairs</h4>
      <ul><li><a href="{href('pool-repair')}">All pool repair</a></li>{svcs}</ul>
    </div>
    <div>
      <h4>Service area</h4>
      <ul>{cities}<li><a href="{href('service-areas')}">All cities</a></li></ul>
    </div>
    <div>
      <h4>Company</h4>
      <ul>
        <li><a href="{href('pool-service-thousand-oaks')}">Weekly pool service</a></li>
        <li><a href="{href('about')}">About</a></li>
        <li><a href="{href('reviews')}">Reviews</a></li>
        <li><a href="{href('blog')}">Blog</a></li>
        <li><a href="{href('contact')}">Contact</a></li>
      </ul>
    </div>
    <div class="legal">
      <span>© 2026 Miller Pool and Spa. All rights reserved.</span>
      <span><a href="{href('privacy-policy')}">Privacy policy</a></span>
    </div>
  </div>
</footer>
<div class="mbar">
  <a class="btn btn-call" href="{TEL}">Call now</a>
  <a class="btn btn-outline" href="{href('contact')}">Request service</a>
</div>"""

def photo(caption, cls=""):
    return f'<figure class="photo {cls}"><span>Photo: {caption}</span></figure>'

def hero(slug, h1, lede, note, caption, secondary=None, rating=True):
    sec = ""
    if secondary:
        label, target = secondary
        sec = f'<a class="btn btn-outline" href="{target}">{label}</a>'
    badge = '<div class="rating"><b>5.0</b> <span class="stars">★★★★★</span><br>Rated on Google</div>' if rating else ""
    return f"""
<section class="hero">
  <div class="wrap">
    <div class="hero-text">
      <h1>{h1}</h1>
      <p class="lede max">{lede}</p>
      <div class="hero-cta">
        <a class="btn btn-call" href="{TEL}">Call {PHONE}</a>
        {sec}
      </div>
      <p class="hero-note">{note}</p>
    </div>
    <div class="hero-photo">
      {photo(caption, 'top')}
      {badge}
    </div>
  </div>
</section>"""

def band(items=None):
    items = items or ["Licensed &amp; insured", "Based in Newbury Park", "Repair techs on staff", "Price quoted before work starts"]
    return '<div class="band"><div class="wrap"><ul>' + "".join(f"<li>{i}</li>" for i in items) + "</ul></div></div>"

def section(inner, cls="", sid=None):
    idattr = f' id="{sid}"' if sid else ""
    return f'<section class="{cls}"{idattr}><div class="wrap">{inner}</div></section>'

def row(caption, h3, paras, flip=False, cls="", bullets=None):
    ps = "".join(f"<p>{p}</p>" for p in paras)
    if bullets:
        ps += "<ul>" + "".join(f"<li>{b}</li>" for b in bullets) + "</ul>"
    return f"""
<div class="row {'flip' if flip else ''}">
  {photo(caption, cls)}
  <div class="text"><h3>{h3}</h3>{ps}</div>
</div>"""

def repairs_list(order):
    out = []
    for key in order:
        s, h, p = REPAIR_ITEMS[key]
        title = f'<a href="{href(s)}">{h}</a>' if s else h
        out.append(f"<div><h3>{title}</h3><p>{p}</p></div>")
    return '<div class="repairs">' + "".join(out) + "</div>"

def problems(items):
    return '<dl class="problems">' + "".join(f"<div><dt>{a}</dt><dd>{b}</dd></div>" for a, b in items) + "</dl>"

def review_fig(key):
    text, name = REVIEWS[key]
    return f"""
<figure class="review">
  <span class="stars" aria-label="5 stars">★★★★★</span>
  <blockquote>"{text}"</blockquote>
  <figcaption><b>{name}</b> · Google review</figcaption>
</figure>"""

def reviews_section(keys, heading="What customers say", more=True):
    link = f'<p class="mt"><a href="{href("reviews")}">Read all reviews</a></p>' if more else ""
    return section(f"<h2>{heading}</h2>" + '<div class="reviews">' + "".join(review_fig(k) for k in keys) + "</div>" + link, "sky")

def faq_section(items, heading="Common questions"):
    body = "".join(f"<div><h3>{q}</h3><p>{a}</p></div>" for q, a in items)
    return section(f'<h2>{heading}</h2><div class="faq">{body}</div>')

def faq_ld(items):
    return {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": html.unescape(q), "acceptedAnswer": {"@type": "Answer", "text": html.unescape(a)}} for q, a in items]}

ISSUES = ["Pump or motor", "Heater", "Losing water / leak", "Filter", "Salt system", "Automation or lights", "Green pool", "Weekly service quote", "Something else"]

def request_section(slug, heading="Request a repair", lede="Call, text or send the form. We call back to schedule a visit.", cities="Thousand Oaks, Newbury Park, Westlake Village, Agoura Hills, Simi Valley, Camarillo, Calabasas", default_issue=None, cls=""):
    opts = "".join(f'<option{" selected" if o == default_issue else ""}>{o}</option>' for o in ISSUES)
    u = lambda n: aid(slug, n)
    return f"""
<section class="{cls}" id="{aid(slug, 'request')}">
  <div class="wrap contact">
    <div class="contact-info">
      <h2>{heading}</h2>
      <p class="lede">{lede}</p>
      <a class="big" href="{TEL}">{PHONE}</a>
      <dl>
        <dt>Email</dt><dd>{EMAIL}</dd>
        <dt>Office</dt><dd>Newbury Park, CA</dd>
        <dt>Service area</dt><dd>{cities}</dd>
      </dl>
      <p class="fine">Already a weekly customer? Call the office and we'll send your tech.</p>
    </div>
    <form class="req" id="{u('form')}">
      <h3>Tell us what's going on</h3>
      <div class="f2">
        <label for="{u('name')}">Name<input id="{u('name')}" name="name" autocomplete="name" required></label>
        <label for="{u('phone')}">Phone<input id="{u('phone')}" name="phone" type="tel" autocomplete="tel" required></label>
      </div>
      <div class="f2">
        <label for="{u('zip')}">Address or ZIP<input id="{u('zip')}" name="zip" autocomplete="postal-code" placeholder="91362"></label>
        <label for="{u('issue')}">What do you need?<select id="{u('issue')}" name="issue">{opts}</select></label>
      </div>
      <label for="{u('notes')}">Details<textarea id="{u('notes')}" name="notes" placeholder="Pump hums for a few seconds then shuts off. Pentair, about 8 years old."></textarea></label>
      <button class="btn btn-blue" type="submit">Send request</button>
      <p class="fine">No spam, no newsletter. We only use this to call you back.</p>
      <p class="done" hidden>Got it. This preview isn't connected to the office yet. On the live site this goes straight to scheduling.</p>
    </form>
  </div>
</section>"""

def city_grid(intro=None):
    cards = "".join(f'<div><h3><a href="{href(s)}">{n}</a></h3><p>{d}</p></div>' for s, n, d in CITY_LINKS)
    intro_html = f'<p class="lede max mt">{intro}</p>' if intro else ""
    return section(f'<h2>Repair service by city</h2>{intro_html}<div class="cities">{cards}</div><p class="mt" style="margin-top:24px"><a href="{href("service-areas")}">Full service area</a></p>', "sky")

def zips_section(h2, drive, rows, nearby):
    trs = "".join(f"<tr><td>{z}</td><td>{n}</td></tr>" for z, n in rows)
    lis = "".join(f'<li><a href="{href(s)}">{n}</a></li>' for s, n in nearby)
    return section(f"""
<h2>{h2}</h2>
<p class="lede max mt">{drive}</p>
<div class="areas">
  <table class="zips"><thead><tr><th>ZIP</th><th>Neighborhoods</th></tr></thead><tbody>{trs}</tbody></table>
  <div><h3>Nearby cities</h3><ul class="nearby mt">{lis}</ul></div>
</div>""", "sky")

def service_ld(name, slug, offers=None):
    d = {"@type": "Service", "name": name, "serviceType": name, "provider": {"@id": BASE + "/#business"}, "url": f"{BASE}/{slug}/", "areaServed": {"@type": "Place", "name": "Conejo Valley, CA"}}
    if offers:
        d["hasOfferCatalog"] = {"@type": "OfferCatalog", "name": name, "itemListElement": [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": o}} for o in offers]}
    return d

# ---------------------------------------------------------------- pages

PAGES = []  # (slug, title, description, body_html, ld_blocks)

def add(slug, title, desc, body, ld=None):
    PAGES.append((slug, title, desc, body, ld or []))

GENERAL_FAQ = [
    ("Do you repair pools you don't service weekly?", "Yes. Repair calls are open to any pool owner in our service area. Plenty of our repair customers have a different weekly service company or clean the pool themselves."),
    ("How soon can someone come out?", "Call and we'll give you a real date. Pumps and green pools go first in summer, because the water turns fast. Tell us if the pool is already turning."),
    ("Do you charge for the diagnosis?", "There's a service call fee for the visit and the diagnosis. If you go ahead with the repair, we tell you up front how that applies. You'll have the full price before any work starts."),
]

def build_pages():
    # ---------- Home
    body = hero("", "Pool service and repair in Thousand Oaks and the Conejo Valley",
        "Miller Pool and Spa cleans and repairs pools across Ventura and Los Angeles County. Weekly service routes, and repair techs on staff for pumps, heaters, filters, salt systems and leaks.",
        "Based in Newbury Park. Repair calls welcome from any pool owner in our service area, weekly customer or not.",
        "clear backyard pool in Thousand Oaks, Miller truck in the driveway",
        secondary=("Request service", "#" + aid("", "request")))
    body += band()
    body += section(f"""
<h2>What we do</h2>
<div class="svc">
  <div>{photo('tech replacing a pump motor at an equipment pad')}<h3>Pool repair</h3><p>Pumps, heaters, filters, salt systems, automation and lights. Diagnosed on site and priced before the work starts.</p><a class="more" href="{href('pool-repair')}">Pool repair services</a></div>
  <div>{photo('tech brushing a pool, net and test kit on the deck')}<h3>Weekly pool service</h3><p>Same tech, same day every week. Water balanced, pool brushed and skimmed, equipment checked, and you pay online.</p><a class="more" href="{href('pool-service-thousand-oaks')}">Weekly service</a></div>
  <div>{photo('pressure-testing rig hooked to a skimmer line')}<h3>Leak detection</h3><p>Pressure testing and dye testing to find the leak before anything gets dug up. Most leaks are at the equipment, the skimmer or the light.</p><a class="more" href="{href('pool-leak-detection')}">Leak detection</a></div>
</div>
<p class="brand-line">Also <a href="{href('green-pool-cleanup')}">green pool cleanups</a>, new equipment installs, and most major brands: Pentair, Hayward, Jandy and Raypak.</p>""")
    body += city_grid("We're based in Newbury Park and cover the Conejo Valley, Simi Valley and Camarillo.")
    body += reviews_section(["andreas", "michael"])
    body += request_section("", "Get in touch", "Call, text or send the form. We call back to schedule.")
    add("", "Pool Service and Repair in Thousand Oaks | Miller Pool and Spa",
        "Pool repair and weekly pool service in Thousand Oaks, Newbury Park and the Conejo Valley. Pumps, heaters, filters, salt systems and leak detection. Call (805) 492-6991.", body)

    # ---------- Pool repair hub
    body = hero("pool-repair", "Pool repair in the Conejo Valley",
        "One call for whatever stopped working on the equipment pad. Our techs diagnose on site, quote before the work, and know the Pentair, Hayward, Jandy and Raypak equipment on most pools around here.",
        "Serving Thousand Oaks, Newbury Park, Westlake Village, Agoura Hills, Simi Valley, Camarillo and Calabasas.",
        "equipment pad with pump, filter and heater, tech kneeling at the pump",
        secondary=("Request a repair", "#" + aid("pool-repair", "request")))
    body += band()
    body += section(f"""<h2>What we repair</h2><p class="lede max mt">Most calls fall into one of these. If yours doesn't, call anyway. If we can't fix it, we'll tell you who can.</p>{repairs_list(['pump','heater','filter','leak','salt','auto','green','install'])}""", sid="repairs")
    body += section(
        row("tech testing a pool heater, gauges visible", "The price comes before the work",
            ["The tech diagnoses first and quotes second. You approve the number, then we start. If something else turns up once we're in there, we stop and call you.",
             "We also tell you when a repair isn't worth it. A twelve-year-old single-speed pump with a bad motor is usually a replacement, not a rebuild, and we'll say so."]) +
        row("salt cell with scale buildup", "We know Conejo Valley water",
            ["Water here is hard. That scale shows up on salt cells, heater exchangers and tile long before it shows up on your bill. Our techs work on it every day, so repairs account for it and last longer.",
             f'If you want someone to keep an eye on the pool after it\'s fixed, we run <a href="{href("pool-service-thousand-oaks")}">weekly service</a> routes through Thousand Oaks and Newbury Park too.'], flip=True), "sky")
    body += city_grid()
    body += faq_section(GENERAL_FAQ)
    body += request_section("pool-repair")
    add("pool-repair", "Pool Repair in the Conejo Valley | Miller Pool and Spa",
        "Pool equipment repair in Thousand Oaks and the Conejo Valley. Pumps, heaters, filters, leaks, salt systems and automation. Price quoted before work starts. (805) 492-6991.",
        body, [service_ld("Pool repair", "pool-repair", ["Pool pump repair", "Pool heater repair", "Pool filter repair", "Pool leak detection", "Salt system repair", "Pool light repair", "Green pool cleanup"]), faq_ld(GENERAL_FAQ)])

    # ---------- Service pages
    svc_pages = [
        dict(slug="pool-pump-repair", name="Pool pump repair", h1="Pool pump repair",
             lede="The pump is the one piece of equipment that has to work for everything else to. When it stops, the water goes green within days in summer. We repair and replace pool pumps across Thousand Oaks, Simi Valley, Camarillo and the rest of the Conejo Valley.",
             note="Motors, capacitors, seals and most wet-end parts are common, so a lot of pump calls are fixed in one visit.",
             caption="tech pulling a pump motor, wet end still on the pad",
             problems=[("Hums but won't start", "Usually the start capacitor. Sometimes seized bearings."),
                       ("Runs a while, then shuts off", "Motor overheating, a thermal overload, or low voltage at the pad."),
                       ("Trips the breaker", "Shorted windings, water in the motor, or a wiring fault."),
                       ("Leaks at the pump", "Shaft seal, housing o-ring, or a cracked volute."),
                       ("Loses prime or sucks air", "Lid o-ring, a suction-side leak, or the water level is too low."),
                       ("Grinding or screeching", "Bearings. Fix it now or the motor fails and takes the seal with it.")],
             rows=[("multimeter on a pump motor", "What we do on site",
                    ["We test voltage, amp draw, the capacitor, the seal and the plumbing around the pump. Most motor problems are a motor swap, not a whole new pump. If the wet end is in good shape, that's usually the cheaper fix.",
                     "If the pump is an old single-speed, we price a variable-speed replacement next to the repair so you can compare. Variable-speed pumps run at low speed most of the day and often cut the pump's electricity use by more than half."]),
                   ("new variable-speed pump on a pad", "Pumps we work on",
                    ["Pentair IntelliFlo, SuperFlo and WhisperFlo. Hayward TriStar, Super Pump and MaxFlo. Jandy FloPro, Stealth and the VS series. Booster pumps for pressure-side cleaners too.",
                     "We install what we repair, so if it comes to a replacement there's one company to call afterward."])],
             faq=[("How long does a pump repair take?", "Most are done in the first visit when the part is common. Motors, capacitors and seals are common. A cracked housing on an older pump can mean a return trip."),
                  ("Should I switch to a variable-speed pump?", "If your single-speed motor has failed and the pump is more than a few years old, usually yes. The power savings pay for the difference, and most replacement pumps sold in California are variable-speed now anyway."),
                  ("How long should the pump run each day?", "Long enough to turn the water over once. For a variable-speed pump at low speed that's often most of the day in summer and less in winter. We set the schedule when we install or repair.")],
             default_issue="Pump or motor",
             desc="Pool pump repair in Thousand Oaks and the Conejo Valley. Motors, capacitors, seals and variable-speed replacements for Pentair, Hayward and Jandy pumps. (805) 492-6991."),

        dict(slug="pool-heater-repair", name="Pool heater repair", h1="Pool and spa heater repair",
             lede="Gas heaters and heat pumps for pools and spas. We repair Raypak, Pentair MasterTemp, Hayward and Jandy units across the Conejo Valley, and we'll tell you when a heater is past fixing.",
             note="Bring the error code if the display shows one. It shortens the diagnosis.",
             caption="tech with the front panel off a Raypak heater",
             problems=[("Won't ignite", "Ignitor, gas supply, or a pressure switch that isn't seeing enough flow."),
                       ("Lights, then shuts down", "Flame sensor or gas valve. Sometimes a venting problem."),
                       ("Shows an error code", "A sensor or the control board. We read the code and test the part, not just swap it."),
                       ("Low flow or pressure error", "A dirty filter, a closed valve, or a bad pressure switch. Often not the heater at all."),
                       ("Soot, rust or a burning smell", "Exchanger corrosion or scale from hard water. Needs a look before you run it again."),
                       ("Heats slowly", "Scale in the exchanger, a bypass stuck open, or the heater is undersized for the spa.")],
             rows=[("heater control board and wiring", "What we do on site",
                    ["We start with the code and a flow check, because a lot of heater calls are a filter or valve problem showing up as a heater fault. Then we test the part the code points to. Ignitors, sensors, switches and boards are the usual fixes.",
                     "On older heaters we check the exchanger. Conejo Valley water is hard, and scale builds up inside the tubes until the heater can't move heat into the water."]),
                   ("spa spillover running with steam coming off", "What a heater repair costs",
                    ["It depends on the part. An ignitor, a sensor or a pressure switch is a small job. A gas valve or control board is a mid-size one. A heat exchanger is the big one, and on a heater more than ten or twelve years old it's usually close to the cost of a new heater. We'll say so.",
                     "You get the number before we touch anything. If replacement makes more sense, we quote that beside the repair."])],
             faq=[("Why does the heater work for the spa but not the pool?", "Usually flow. The pool side runs through more plumbing and the filter, so a dirty filter or a stuck valve can drop the flow below what the pressure switch wants. We check that before we blame the heater."),
                  ("Do you repair heat pumps?", "Yes. Heat pumps have the same sensors, boards and flow switches as gas heaters, plus a fan and a compressor side. We'll tell you if a problem is in the sealed system."),
                  ("How long does a pool heater last?", "Ten to fifteen years with balanced water. Hard water and low pH shorten that. Regular service is mostly about keeping the exchanger clean.")],
             default_issue="Heater",
             desc="Pool heater repair in Thousand Oaks and the Conejo Valley. Raypak, Pentair, Hayward and Jandy gas heaters and heat pumps. Diagnosed first, priced before work. (805) 492-6991."),

        dict(slug="pool-leak-detection", name="Pool leak detection", h1="Pool leak detection and repair",
             lede="Losing water faster than evaporation? We find the leak before we fix anything. Pressure testing on the lines, dye testing on the shell, lights and fittings, and a clear answer on what it will take to repair. Serving Thousand Oaks, Westlake Village, Agoura Hills, Calabasas and the Conejo Valley.",
             note="Most leaks are at the equipment pad, the skimmer or the light. Very few need the deck cut.",
             caption="tech dye-testing a pool light niche",
             problems=[("More than a quarter inch a day", "Evaporation in our climate is usually less than that, even in summer wind."),
                       ("The autofill never stops", "It's keeping up with a leak. Turn it off for a day and watch the level."),
                       ("Wet or soggy ground", "Near the equipment or along the deck edge. Follow the water."),
                       ("Air in the pump or bubbles at the returns", "A suction-side leak pulling air in, often the same spot that leaks water when the pump is off."),
                       ("Chemicals won't hold", "Fresh fill water every day dilutes everything you add."),
                       ("Level drops faster with the pump on", "Pressure-side plumbing. Faster with it off points to the suction side or the shell.")],
             rows=[("pressure-testing rig on a return line", "How we find it",
                    ["We start with the equipment pad, because that's where most leaks are. Then we pressure-test each line to see which one holds. Dye tests around the lights, skimmers, returns and any cracks show leaks in the shell. For underground lines we locate the spot before anyone digs.",
                     "You get a report of what we found and a price for the repair. If the leak is at the pad or the skimmer, the repair is often the same visit."]),
                   ("skimmer throat repair with epoxy", "Repairs we do",
                    ["Skimmer and light niche repairs. Fitting and return replacements. Plumbing repairs with as little deck cut as we can manage. Shell crack repair. Equipment leaks at the pump, filter, heater and valves.",
                     "Hillside lots in Agoura Hills, Oak Park and Westlake Village put extra stress on long plumbing runs. We see a lot of those."])],
             faq=[("Will my deck get torn up?", "Rarely. Most leaks are at the equipment, the skimmer or the light, and those are repaired without touching the deck. When an underground line is leaking, we locate the spot first so the cut is small."),
                  ("Can I keep using the pool?", "Yes, as long as you keep the water above the skimmer. Keep filling it until we're out. A pool that drops below the skimmer can run the pump dry."),
                  ("Do you do spas and water features?", "Attached spas, yes. Spillovers and waterfalls are common leak points and we test them with the rest of the pool.")],
             default_issue="Losing water / leak",
             desc="Pool leak detection in Thousand Oaks, Agoura Hills, Westlake Village and the Conejo Valley. Pressure testing, dye testing and repair. Call (805) 492-6991."),

        dict(slug="pool-filter-repair", name="Pool filter repair", h1="Pool filter and equipment repair",
             lede="Cartridge, DE and sand filters, plus the valves, cleaners, timers and plumbing that sit on the equipment pad. If the water's cloudy or the pressure gauge keeps climbing, this is the page.",
             note="A filter problem often looks like a heater or chlorinator problem, because low flow trips both. We check the filter first.",
             caption="tech lifting a cartridge out of a filter tank",
             problems=[("Pressure climbs fast between cleanings", "Scale on the cartridges, a torn cartridge letting debris through, or the filter is too small for the pump."),
                       ("Cloudy water with a clean filter", "A torn cartridge, a broken DE grid or a cracked manifold letting water bypass."),
                       ("DE powder blowing back into the pool", "A torn grid or a bad manifold. Easy to confirm, quick to fix."),
                       ("Leaking from the tank or the clamp", "A worn tank o-ring, a cracked tank, or a clamp band that's stretched."),
                       ("Water out the backwash line", "The multiport or push-pull valve. Usually the spider gasket."),
                       ("Cleaner won't move", "Booster pump, hoses, or the drive gears in the cleaner itself.")],
             rows=[("multiport valve open on the bench", "What we do on site",
                    ["We open the filter and look. Cartridges get inspected for tears and scale. DE grids and manifolds get checked for cracks. Valves get rebuilt or replaced. Tanks that are cracked get replaced, because a patched tank under pressure isn't worth the risk.",
                     "If the filter is undersized for the pump, which happens a lot after a pump upgrade, we'll tell you. A bigger filter means longer between cleanings and easier on the pump."]),
                   ("new cartridge filter next to an old one", "Cartridges, grids and scale",
                    ["In our hard water, cartridges scale up and lose capacity even when they look clean. Acid washing helps once or twice. After that they need replacing, usually every two to three years with weekly cleaning.",
                     "We service Pentair Clean &amp; Clear, Hayward SwimClear and StarClear, Jandy CL and CV, and the common DE and sand filters."])],
             faq=[("How often should the filter be cleaned?", "Cartridge filters every three to six months in normal use, or when the pressure rises about ten psi over clean. More often in a windy yard or after a green pool."),
                  ("Why is the pressure high right after a cleaning?", "Scale. The cartridges are plugged with calcium that a hose can't remove. An acid wash or new cartridges fixes it."),
                  ("Cartridge or DE?", "Cartridge is simpler and uses no backwash water, which matters here. DE filters finer. For most residential pools in the Conejo Valley we lean cartridge.")],
             default_issue="Filter",
             desc="Pool filter repair in Thousand Oaks and the Conejo Valley. Cartridge, DE and sand filters, valves, cleaners and equipment pad plumbing. (805) 492-6991."),

        dict(slug="salt-system-repair", name="Salt system repair", h1="Salt system repair",
             lede="Hayward AquaRite, Pentair IntelliChlor, Jandy AquaPure and TruClear. Cells, flow switches, control boards, and the scale problems hard water causes in Westlake Village, Calabasas and Thousand Oaks.",
             note="A salt cell is a wear part. Three to five years in our water is typical, and cleaning it every few months stretches that.",
             caption="salt cell with scale on the plates, held up to the light",
             problems=[("Low salt light, but you just added salt", "The cell is near the end of its life, or the water is cold. Cells read low under about 60 degrees."),
                       ("Check cell or inspect cell", "Scale on the plates. Needs an acid clean, or replacement if the plates are worn."),
                       ("No flow", "The flow switch, a dirty filter, or air in the line. Often not the salt system at all."),
                       ("No chlorine in the water", "A dead cell, a board fault, the output turned down, or stabilizer so high the chlorine can't work."),
                       ("Corrosion on the pad", "Salt splash on metal, or a bonding problem. Worth fixing before it eats a heater."),
                       ("Panel shows nothing", "Power, a fuse, or the board.")],
             rows=[("tech reading volts and amps on a salt panel", "What we do on site",
                    ["We test what the cell is actually producing in volts and amps, check the flow switch, and read the board. A cell that's scaled gets cleaned. A cell that's worn gets replaced. Boards and flow switches are stocked for the common systems.",
                     "We also check salt, stabilizer and calcium levels, because a salt system on badly balanced water will scale up again in months."]),
                   ("new salt cell installed on a pad", "Systems we repair and install",
                    ["Hayward AquaRite and AquaRite Pro. Pentair IntelliChlor and iChlor. Jandy AquaPure and TruClear. We also convert tablet-chlorine pools to salt, and we'll tell you what that does to your plaster, stone and equipment before you decide."])],
             faq=[("Is salt water hard on my equipment or stone?", "A salt pool is still a chlorine pool, just a mild one. The salt level is about a tenth of seawater. Natural stone and some metals need rinsing and a sealed surface, and we'll point out anything on your pad that's at risk."),
                  ("Why is my pool green if the salt system is on?", "The cell may be dead or scaled, the output may be turned down, or stabilizer is so high the chlorine is tied up. A test tells us which in a few minutes."),
                  ("How often should the cell be cleaned?", "Every three months is a good habit here. In very hard water, more often. Scale left on the plates shortens the cell's life.")],
             default_issue="Salt system",
             desc="Salt system repair in Thousand Oaks, Westlake Village and Calabasas. Hayward AquaRite, Pentair IntelliChlor and Jandy AquaPure cells, boards and flow switches. (805) 492-6991."),

        dict(slug="green-pool-cleanup", name="Green pool cleanup", h1="Green pool cleanup",
             lede="Pool went green while you were away, or came with the house that way? We bring it back to clear, fix the equipment that let it happen, and set it up so it doesn't come back. Available anywhere in our service area.",
             note="The sooner you call, the cheaper it is. Light green is a few days of work. Black and swampy can mean a drain.",
             caption="before and after of a green pool, same angle",
             problems=[("The pump or filter stopped", "The most common cause. A pool with no circulation turns in days in summer."),
                       ("Chlorinator ran empty", "Or the salt cell died quietly. The water looks fine for a week, then it isn't."),
                       ("A heat wave", "Hot water burns through chlorine. A pool that was borderline tips over."),
                       ("Vacant or just purchased", "Nobody was watching it. We see a lot of these from realtors and new owners."),
                       ("Storm debris", "Leaves and dirt eat chlorine and feed algae. Wind events do it too."),
                       ("Stabilizer too high", "Years of tablets build up cyanuric acid until chlorine can't work. A partial drain is the only fix.")],
             rows=[("tech vacuuming a cloudy pool to waste", "How we bring it back",
                    ["First a test, because the chemistry decides the plan. If stabilizer and phosphates are reasonable, we treat it: shock, algaecide, brush, filter around the clock, vacuum to waste, and clean the filter as it loads up. Most pools clear in three to seven days.",
                     "If stabilizer is very high or the algae is black, a drain and acid wash can be cheaper and faster than fighting it. We'll say which."]),
                   ("clean pool with the equipment pad in the background", "After it's clear",
                    ["We check why it happened. A pump that quit, a filter that's torn, a cell that's dead. That gets fixed or it'll be green again next month.",
                     f'If you\'d like someone watching it from here on, our <a href="{href("pool-service-thousand-oaks")}">weekly service</a> routes cover most of the Conejo Valley.'])],
             faq=[("How long does it take?", "Three to seven days for most green pools, depending on how far gone it is and how well the filter keeps up. A drain and refill is faster but uses a lot of water."),
                  ("Is it safe to swim after?", "Once the water is clear, balanced and the chlorine is back in the normal range. We'll tell you when."),
                  ("What does it cost?", "It depends on the chemistry and whether the filter and pump are working. We quote after the first test. A light green pool with working equipment is a small job.")],
             default_issue="Green pool",
             desc="Green pool cleanup in Thousand Oaks, Simi Valley, Camarillo and the Conejo Valley. Back to clear in days, with the equipment that caused it fixed. (805) 492-6991."),
    ]
    for s in svc_pages:
        slug = s["slug"]
        body = hero(slug, s["h1"], s["lede"], s["note"], s["caption"], secondary=("Request a repair", "#" + aid(slug, "request")))
        body += band()
        body += section(f"<h2>Common problems</h2>{problems(s['problems'])}")
        rows_html = "".join(row(c, h, ps, flip=(i % 2 == 1)) for i, (c, h, ps) in enumerate(s["rows"]))
        body += section(rows_html, "sky")
        body += faq_section(s["faq"])
        body += request_section(slug, default_issue=s["default_issue"], cls="sky")
        add(slug, f"{s['name'].replace('Pool ', 'Pool ')} in Thousand Oaks | Miller Pool and Spa", s["desc"], body,
            [service_ld(s["name"], slug), faq_ld(s["faq"])])

    # ---------- City pages
    cities = [
        dict(slug="pool-repair-thousand-oaks", city="Thousand Oaks", h1="Pool repair in Thousand Oaks and Newbury Park",
             lede="Pump won't turn on? Heater throwing a code? Water level dropping every day? Miller Pool and Spa repairs pool equipment across the Conejo Valley. A tech comes out, finds the problem, and gives you a price before any work starts.",
             caption="Miller tech at an equipment pad in Thousand Oaks (pump, filter, heater in frame)",
             order=["pump", "heater", "filter", "leak", "salt", "auto", "green", "install"],
             row2=("salt cell with scale buildup", "We know Conejo Valley water",
                   ["Water here is hard. That scale shows up on salt cells, heater exchangers and tile long before it shows up on your bill. Our techs work on it every day, so repairs account for it and last longer.",
                    "If you want someone to keep an eye on the pool after it's fixed, we run weekly service routes through Thousand Oaks and Newbury Park too."]),
             drive="We're based in Newbury Park, so most Thousand Oaks repair calls are a short drive for us.",
             zips=[("91362", "North Ranch, Lang Ranch, Sunset Hills, east Thousand Oaks"), ("91360", "Central Thousand Oaks, Wildwood, Lynn Ranch, Conejo Oaks"), ("91320", "Newbury Park, Dos Vientos, Rancho Conejo, Casa Conejo"), ("91361", "South Thousand Oaks, Westlake side of Thousand Oaks")],
             nearby=[("pool-repair-westlake-village", "Westlake Village &amp; Oak Park"), ("pool-repair-agoura-hills", "Agoura Hills"), ("pool-repair-simi-valley", "Simi Valley"), ("pool-repair-camarillo", "Camarillo"), ("pool-repair-calabasas", "Calabasas &amp; Hidden Hills"), ("service-areas", "Moorpark")],
             faq_city="Thousand Oaks and Newbury Park", ld_city=["Thousand Oaks", "Newbury Park"],
             desc="Pool pump, heater, filter, salt system and leak repair in Thousand Oaks and Newbury Park. Licensed techs based in Newbury Park. Call (805) 492-6991."),
        dict(slug="pool-repair-simi-valley", city="Simi Valley", h1="Pool repair in Simi Valley",
             lede="Pump quit, filter pressure through the roof, pool starting to turn? Miller Pool and Spa sends repair techs to Simi Valley from our shop in Newbury Park, a short run up the 23. Pumps, filters, heaters, salt systems, leaks and green pool cleanups.",
             caption="tech swapping a pump motor in a Simi Valley backyard",
             order=["pump", "filter", "heater", "leak", "salt", "auto", "green", "install"],
             row2=("variable-speed pump freshly installed", "Pumps and filters are most of our Simi Valley calls",
                   ["Simi pools run hard through the summer heat, and the pump and filter take the beating. Motors, capacitors, seals and cartridges are common parts, so many of these calls are fixed on the first visit.",
                    "If the pump is an older single-speed, we quote a variable-speed replacement beside the repair. With pumps running long hours all summer, the power savings usually decide it."]),
             drive="Simi Valley is about twenty-five minutes from our shop in Newbury Park. We're in Simi most days.",
             zips=[("93065", "West Simi Valley, Wood Ranch, Big Sky"), ("93063", "East Simi Valley, Bridle Path, Santa Susana Knolls"), ("93021", "Moorpark")],
             nearby=[("pool-repair-thousand-oaks", "Thousand Oaks &amp; Newbury Park"), ("service-areas", "Moorpark"), ("pool-repair-camarillo", "Camarillo"), ("pool-repair-westlake-village", "Westlake Village"), ("pool-repair-agoura-hills", "Agoura Hills"), ("pool-repair-calabasas", "Calabasas")],
             faq_city="Simi Valley", ld_city=["Simi Valley"],
             desc="Pool repair in Simi Valley. Pump, filter, heater and salt system repair, leak detection and green pool cleanup. Price quoted before work starts. (805) 492-6991."),
        dict(slug="pool-repair-camarillo", city="Camarillo", h1="Pool repair in Camarillo",
             lede="Coastal air, hard water and long pump hours are tough on pool equipment. Miller Pool and Spa repairs pumps, heaters, filters, salt systems and leaks across Camarillo, and runs weekly service routes there too.",
             caption="tech at an equipment pad in Camarillo, filter tank open",
             order=["pump", "filter", "heater", "salt", "leak", "auto", "green", "install"],
             row2=("tech brushing a pool with the test kit on the deck", "Repair now, weekly service if you want it",
                   ["A lot of Camarillo customers found us through a repair and stayed for weekly service. Having repair techs on the same team means the person cleaning your pool notices a pump seal starting to weep before it fails.",
                    "If you already have a service company, that's fine. We'll fix the problem and hand it back."]),
             drive="Camarillo is about twenty minutes from Newbury Park down the 101. We run routes there, so repair calls fit around them.",
             zips=[("93010", "Central Camarillo, Camarillo Heights, Spanish Hills, Sterling Hills"), ("93012", "Mission Oaks, Leisure Village, Santa Rosa Valley"), ("93066", "Somis")],
             nearby=[("pool-repair-thousand-oaks", "Thousand Oaks &amp; Newbury Park"), ("pool-repair-simi-valley", "Simi Valley"), ("service-areas", "Moorpark"), ("pool-repair-westlake-village", "Westlake Village"), ("pool-repair-agoura-hills", "Agoura Hills"), ("pool-repair-calabasas", "Calabasas")],
             faq_city="Camarillo", ld_city=["Camarillo"],
             desc="Pool repair in Camarillo. Pumps, filters, heaters, salt systems and leak detection, plus weekly pool service. Based in Newbury Park. (805) 492-6991."),
        dict(slug="pool-repair-westlake-village", city="Westlake Village", h1="Pool repair in Westlake Village and Oak Park",
             lede="Big pools, attached spas, gas heaters, automation and salt. Westlake Village equipment pads have more on them than most, and more that can go wrong. Miller Pool and Spa repairs all of it from our shop in Newbury Park, ten minutes down the 101.",
             caption="large equipment pad with two heaters and an automation panel",
             order=["heater", "auto", "leak", "salt", "pump", "filter", "green", "install"],
             row2=("tech at a Pentair automation panel", "Heaters, automation and leaks",
                   ["Most Westlake calls are a heater that won't fire, an automation panel that lost its schedule, or a pool losing water. We carry the diagnostic gear for all three and we know the Pentair, Jandy and Hayward control systems that run most of these pools.",
                    "North Ranch, Westlake Island and Lake Sherwood pools often run two heaters and a spa spillover. We size parts for the system, not just the pool."]),
             drive="Westlake Village is ten minutes from Newbury Park. Oak Park is a few minutes more.",
             zips=[("91361", "Westlake Village, Westlake Island, First Neighborhood, Three Springs, Lake Sherwood"), ("91362", "North Ranch, Westlake north of the 101"), ("91377", "Oak Park")],
             nearby=[("pool-repair-thousand-oaks", "Thousand Oaks &amp; Newbury Park"), ("pool-repair-agoura-hills", "Agoura Hills"), ("pool-repair-calabasas", "Calabasas &amp; Hidden Hills"), ("pool-repair-simi-valley", "Simi Valley"), ("pool-repair-camarillo", "Camarillo"), ("service-areas", "Moorpark")],
             faq_city="Westlake Village and Oak Park", ld_city=["Westlake Village", "Oak Park"],
             desc="Pool repair in Westlake Village and Oak Park. Heaters, automation, salt systems, leak detection and pumps. Pentair, Jandy and Hayward systems. (805) 492-6991."),
        dict(slug="pool-repair-calabasas", city="Calabasas", h1="Pool repair in Calabasas and Hidden Hills",
             lede="Estate pools with Pentair, Jandy or Hayward systems, often with a spa, a waterfall and a second pump or two. Miller Pool and Spa repairs the equipment, finds the leaks, and keeps the automation talking. Serving Calabasas, Hidden Hills and the surrounding hills.",
             caption="estate pool with spa spillover and waterfall, equipment pad behind a hedge",
             order=["leak", "heater", "auto", "salt", "pump", "filter", "install", "green"],
             row2=("Jandy iAquaLink panel with the cover open", "Brand-specific repair on bigger systems",
                   ["Pentair IntelliCenter and EasyTouch, Jandy iAquaLink, Hayward OmniLogic. The automation on a Calabasas pool usually runs the heater, the valves, the lights and the salt cell, so a fault in one shows up everywhere. We trace it to the actual part.",
                    "Leaks on a large pool get expensive fast. A quarter inch a day on a 30,000-gallon pool is a lot of water and a lot of chemicals. We pressure-test and dye-test before anyone cuts anything."]),
             drive="Calabasas is about twenty-five minutes from Newbury Park on the 101. Hidden Hills is the same trip.",
             zips=[("91302", "Calabasas, Hidden Hills, The Oaks, Calabasas Park, Mulwood, Mountain View Estates"), ("91301", "Agoura Hills"), ("91307", "West Hills")],
             nearby=[("pool-repair-agoura-hills", "Agoura Hills"), ("pool-repair-westlake-village", "Westlake Village &amp; Oak Park"), ("pool-repair-thousand-oaks", "Thousand Oaks"), ("service-areas", "Woodland Hills"), ("pool-repair-simi-valley", "Simi Valley"), ("pool-repair-camarillo", "Camarillo")],
             faq_city="Calabasas and Hidden Hills", ld_city=["Calabasas", "Hidden Hills"],
             desc="Pool repair in Calabasas and Hidden Hills. Leak detection, heaters, automation and salt systems on Pentair, Jandy and Hayward equipment. (805) 492-6991."),
        dict(slug="pool-repair-agoura-hills", city="Agoura Hills", h1="Pool repair and leak detection in Agoura Hills",
             lede="Agoura Hills pools sit on hillside lots with long plumbing runs, and a lot of them are thirty years old. That makes leaks and pump problems the two calls we get most. Miller Pool and Spa handles both, along with heaters, filters, salt systems and automation.",
             caption="hillside backyard pool in Agoura Hills, tech at the skimmer",
             order=["leak", "pump", "heater", "filter", "salt", "auto", "green", "install"],
             row2=("pressure-testing rig on a skimmer line", "Leak detection in Agoura Hills",
                   ["Hillside plumbing runs shift with the ground, and older pools in Old Agoura and Fountainwood were plumbed before flexible fittings were common. We pressure-test each line, dye-test the shell and lights, and locate underground leaks to a spot before we dig.",
                    "If the leak turns out to be at the equipment pad, which it often is, the repair is usually quick."]),
             drive="Agoura Hills is fifteen minutes from Newbury Park on the 101.",
             zips=[("91301", "Agoura Hills, Old Agoura, Morrison Ranch, Liberty Canyon, Fountainwood, Malibou Lake"), ("91377", "Oak Park"), ("91302", "Calabasas")],
             nearby=[("pool-repair-westlake-village", "Westlake Village &amp; Oak Park"), ("pool-repair-calabasas", "Calabasas &amp; Hidden Hills"), ("pool-repair-thousand-oaks", "Thousand Oaks &amp; Newbury Park"), ("pool-repair-simi-valley", "Simi Valley"), ("pool-repair-camarillo", "Camarillo"), ("service-areas", "Moorpark")],
             faq_city="Agoura Hills", ld_city=["Agoura Hills"],
             desc="Pool repair and leak detection in Agoura Hills. Pumps, heaters, filters, salt systems and automation. Based in Newbury Park. (805) 492-6991."),
    ]
    for c in cities:
        slug = c["slug"]
        faq = [
            ("Do you repair pools you don't service weekly?", f"Yes. Repair calls are open to any pool owner in {c['faq_city']}. Plenty of our repair customers have a different weekly service company or clean the pool themselves."),
            ("What does a pool heater repair cost?", "It depends on the part. An ignitor or a pressure switch is a small job. A heat exchanger is a big one, and on an older heater it can be close to the cost of a new unit. We diagnose first and give you the number before touching anything."),
            ("How do I know if my pool is actually leaking?", "Fill a bucket, set it on the top step, and mark the water level inside and outside the bucket. Check after 24 hours with the pump off. If the pool dropped more than the bucket did, call us for leak detection."),
            ("Should I fix my pump or replace it?", "If it's a newer variable-speed pump, usually fix it. If it's an old single-speed with a failing motor, a variable-speed replacement often pays for itself in electricity within a couple of years. We'll show you both numbers."),
        ]
        body = hero(slug, c["h1"], c["lede"], "You don't need to be a weekly customer. We take repair calls from any pool owner in our service area.", c["caption"], secondary=("Request a repair", "#" + aid(slug, "request")))
        body += band()
        body += section(f"<h2>Pool equipment repair in {c['city']}</h2><p class=\"lede max mt\">Most calls fall into one of these. If yours doesn't, call anyway. If we can't fix it, we'll tell you who can.</p>{repairs_list(c['order'])}<p class=\"brand-line\">We work on Pentair, Hayward, Jandy and Raypak equipment, plus most other major brands.</p>")
        cap2, h2_, ps2 = c["row2"]
        body += section(
            row("tech testing a pool heater, gauges visible", "The price comes before the work",
                ["The tech diagnoses first and quotes second. You approve the number, then we start. If something else turns up once we're in there, we stop and call you.",
                 "We also tell you when a repair isn't worth it. A twelve-year-old single-speed pump with a bad motor is usually a replacement, not a rebuild, and we'll say so."]) +
            row(cap2, h2_, ps2, flip=True), "sky")
        body += request_section(slug, cities=", ".join(n for n in [c["city"]] + [html.unescape(n.split(" &amp; ")[0]) for _, n in c["nearby"]][:4]))
        body += reviews_section(["andreas", "michael", "jeannie", "jayne"], more=False)
        body += zips_section(f"Where we work in {c['city']}", c["drive"], c["zips"], c["nearby"])
        body += faq_section(faq, "Pool repair questions")
        ld = [{"@type": "Service", "name": f"Pool Repair in {c['city']}", "serviceType": "Pool equipment repair", "provider": {"@id": BASE + "/#business"},
               "areaServed": [{"@type": "City", "name": n} for n in c["ld_city"]] + [{"@type": "PostalCodeSpecification", "postalCode": z} for z, _ in c["zips"]],
               "url": f"{BASE}/{slug}/"}, faq_ld(faq)]
        add(slug, f"Pool Repair {c['city']} | Miller Pool and Spa", c["desc"], body, ld)

    # ---------- Weekly service
    slug = "pool-service-thousand-oaks"
    body = hero(slug, "Weekly pool service in Thousand Oaks",
        "Same tech, same day every week. Water tested and balanced, pool brushed and skimmed, baskets emptied, equipment checked. Our routes run across the Conejo Valley, and you can pay online.",
        "Routes run through Thousand Oaks, Newbury Park, Westlake Village, Oak Park, Agoura Hills, Moorpark, Simi Valley and Camarillo.",
        "tech skimming a pool, Miller truck visible through the side gate",
        secondary=("Get a service quote", "#" + aid(slug, "request")))
    body += band(["Same day, same tech each week", "Pay online", "Repair techs on the same team", "Chemicals included"])
    body += section(f"""
<h2>What a visit includes</h2>
<div class="row" style="margin-top:28px">
  <div class="text">
    <ul>
      <li>Test the water and balance chlorine, pH, alkalinity, calcium and stabilizer</li>
      <li>Skim the surface and brush the walls, steps and tile line</li>
      <li>Empty the skimmer and pump baskets, and the cleaner bag</li>
      <li>Check the pump, filter pressure, chlorinator or salt cell, and the heater</li>
      <li>Note anything wearing out before it fails, with a price if it needs attention</li>
      <li>Vacuum when the pool needs it</li>
    </ul>
    <p>Filter cleanings are scheduled on top of the weekly visit, every few months depending on the pool. We'll tell you when one is due.</p>
  </div>
  {photo('tech writing up a service note, test kit open')}
</div>""")
    body += section(
        row("pump seal starting to drip at an equipment pad", "Why repair techs on the route matter",
            ["The person cleaning your pool each week is the one who notices the pump seal weeping, the filter pressure creeping up, or the heater taking longer than it used to. On our routes that's reported back the same day and a repair tech handles it.",
             "That's the difference between a small part now and a motor, or a green pool, later."]) +
        row("phone showing an online payment screen", "Simple to deal with",
            ["Service is billed monthly and you can pay online. If something comes up you can call or text the office. Reviews mention the same thing over and over: we show up when we say we will.",
             "Chemical-only service is available if you'd rather do the brushing yourself. Ask when you call."], flip=True), "sky")
    body += reviews_section(["jeannie", "jayne"], "What weekly customers say")
    svc_faq = [
        ("What does weekly service cost?", "It depends on the pool size, the equipment and whether there's a spa. We'll quote after a look at the pool. Chemicals are included."),
        ("Do I need to be home?", "No. We need gate access and a clear path to the pool and the equipment. Dogs are fine if we know about them."),
        ("What if my pool turns green?", "If it happens on our watch, we fix it. If you're starting with a green pool, we clean it up first and then put it on the route."),
        ("Which areas do you cover?", "Thousand Oaks, Newbury Park, Westlake Village, Oak Park, Agoura Hills, Moorpark, Simi Valley and Camarillo. Calabasas and Hidden Hills by request."),
    ]
    body += faq_section(svc_faq, "Weekly service questions")
    body += request_section(slug, "Get a service quote", "Call, text or send the form with your address and we'll come take a look.", default_issue="Weekly service quote", cls="sky")
    add(slug, "Weekly Pool Service in Thousand Oaks | Miller Pool and Spa",
        "Weekly pool service in Thousand Oaks and Newbury Park. Same tech every week, water balanced, equipment checked, pay online. (805) 492-6991.",
        body, [service_ld("Weekly pool service", slug), faq_ld(svc_faq)])

    # ---------- About
    slug = "about"
    body = section(f"""
<div class="row">
  <div class="prose">
    <h1>A Newbury Park pool company</h1>
    <p>Mason Miller learned pool work from his father and started this company on his own, cleaning and repairing pools around Newbury Park. It grew by referral into a crew serving homeowners across Ventura and Los Angeles County.</p>
    <p>The job is the same as it was on day one: show up when we say we will, fix it right, and charge what we quoted. Weekly service routes and repair techs run through the Conejo Valley, Simi Valley and Camarillo.</p>
  </div>
  {photo('the crew with a truck in the Newbury Park yard', 'tall')}
</div>""", "", None)
    body += section(
        row("tech handing a written quote to a homeowner", "How we work",
            ["The price comes before the work. The tech diagnoses first, quotes second, and you approve the number before anything is replaced.",
             "We show up when we say we will. On weekly routes that means the same day and roughly the same time each week. On repairs it means a real date, not a window that slides.",
             "We fix what we install. If we put in the pump, we're the ones who come back if it ever gives you trouble."]) +
        row("two techs with the leak detection kit", "The people you'll meet",
            ["Customers mention our techs by name in reviews, which is the best kind of review. Jon and Jarett run a lot of the leak detection work. The office answers the phone during the day and calls back if you leave a message.",
             f'<a href="{href("reviews")}">Read the reviews</a> or <a href="{href("contact")}">get in touch</a>.'], flip=True), "sky")
    body += request_section(slug, "Get in touch", "Call, text or send the form. We call back to schedule.")
    add(slug, "About Us | Miller Pool and Spa, Newbury Park, CA",
        "Miller Pool and Spa was founded by Mason Miller in Newbury Park. Pool repair and weekly pool service across the Conejo Valley, Simi Valley and Camarillo.", body)

    # ---------- Contact
    slug = "contact"
    body = section(f"""
<h1>Contact Miller Pool and Spa</h1>
<p class="lede max mt">Call or text during the day and you'll usually get a person. Leave a message or send the form and we call back.</p>""")
    body += request_section(slug, "Reach the office", "Repairs, weekly service quotes, and questions about a pool you just bought.", cls="sky")
    body += section(f"""
<h2>Before you call</h2>
<div class="prose mt">
  <p>Not required, but it speeds things up:</p>
  <ul style="color:var(--muted)">
    <li>The brand of the equipment that's acting up, or a photo of the equipment pad</li>
    <li>What you're seeing: a noise, a code on the display, water dropping, cloudy water</li>
    <li>Whether the pool is already turning green. Those go first in summer.</li>
    <li>Gate code or dog situation if nobody will be home</li>
  </ul>
  <h3>Service area</h3>
  <p>Thousand Oaks, Newbury Park, Westlake Village, Oak Park, Agoura Hills, Simi Valley, Moorpark, Camarillo, Calabasas and Hidden Hills. <a href="{href('service-areas')}">Full list</a>.</p>
</div>""")
    add(slug, "Contact | Miller Pool and Spa", "Call or text Miller Pool and Spa at (805) 492-6991 for pool repair or weekly service in Thousand Oaks and the Conejo Valley. Or send the form and we call back.", body)

    # ---------- Reviews
    slug = "reviews"
    body = section(f"""
<h1>Reviews</h1>
<p class="lede max mt">From Google. We don't edit them. The same things come up: communication, showing up, and getting the problem fixed.</p>
<div class="reviews">{''.join(review_fig(k) for k in ['andreas','michael','jeannie','jayne'])}</div>
<p style="margin-top:28px"><a href="https://www.google.com/search?q=Miller+Pool+and+Spa+Newbury+Park+reviews" rel="noopener">Read more on Google</a></p>""")
    body += request_section(slug, "Get in touch", "Call, text or send the form. We call back to schedule.", cls="sky")
    add(slug, "Reviews | Miller Pool and Spa", "Google reviews for Miller Pool and Spa, pool repair and weekly pool service in Thousand Oaks and the Conejo Valley.", body)

    # ---------- Service areas
    slug = "service-areas"
    cards = "".join(f'<div><h3><a href="{href(s)}">{n}</a></h3><p>{d}</p></div>' for s, n, d in CITY_LINKS)
    body = section(f"""
<h1>Where we work</h1>
<p class="lede max mt">We're based in Newbury Park. Repairs and weekly service run through the Conejo Valley, Simi Valley and Camarillo. Pick your city for the repair page.</p>
<div class="cities">{cards}</div>""")
    body += section(f"""
<h2>Also covered</h2>
<div class="prose mt">
  <p><b>Weekly service and repairs:</b> Moorpark, Somis, Santa Rosa Valley, Lake Sherwood.</p>
  <p><b>Repairs by request:</b> Woodland Hills, West Hills, Malibu, Porter Ranch. Call and we'll tell you honestly whether we can get there quickly enough to be worth it.</p>
  <p>If your city isn't listed, call anyway. The map changes as the routes grow.</p>
</div>""", "sky")
    body += request_section(slug, "Get in touch", "Call, text or send the form. We call back to schedule.")
    add(slug, "Service Area | Miller Pool and Spa", "Miller Pool and Spa serves Thousand Oaks, Newbury Park, Westlake Village, Oak Park, Agoura Hills, Simi Valley, Camarillo, Calabasas and Hidden Hills. Based in Newbury Park.", body)

    # ---------- Blog
    posts = [
        dict(slug="pool-heater-repair-cost", title="What a pool heater repair costs in the Conejo Valley",
             summary="Most heater calls end with a sensor or a switch. A few end with the exchanger. Here is what each one typically runs, and when a new heater is the better buy.",
             related=("pool-heater-repair", "Pool heater repair"), issue="Heater",
             body=f"""
<p>Most heater calls end with a small part. A few end with a conversation about a new heater. The difference is usually the age of the unit and what the error code points to, so here is how the price breaks down before anyone takes the panel off.</p>
<h2>The diagnosis comes first</h2>
<p>A service call covers the visit and the test. If the display shows a code, write it down or take a photo. It shortens the diagnosis. Before blaming the heater, a tech checks flow. A dirty filter, a closed valve or a pump running too slow will trip the pressure switch and shut the heater down, and that is a filter cleaning or a valve, not a heater repair.</p>
<h2>Small, medium and large</h2>
<p>These are typical ranges for parts and labor on residential gas heaters in our area. Your quote depends on the brand, the model and what the tech finds once the panel is off.</p>
<table>
<thead><tr><th>Repair</th><th>What it fixes</th><th>Typical range</th></tr></thead>
<tbody>
<tr><td>Ignitor, flame sensor or thermistor</td><td>Won't light, lights then quits, wrong temperature reading</td><td>$150 to $400</td></tr>
<tr><td>Pressure switch or flow switch</td><td>Low flow or pressure errors when the filter is clean</td><td>$150 to $350</td></tr>
<tr><td>Gas valve</td><td>No gas to the burners, or the flame drops out</td><td>$300 to $600</td></tr>
<tr><td>Control board or display</td><td>Dead panel, random codes, buttons that do nothing</td><td>$400 to $900</td></tr>
<tr><td>Heat exchanger</td><td>Leaks, soot, rust, or a heater that takes forever</td><td>$1,200 to $2,500</td></tr>
<tr><td>New gas heater, installed</td><td>Replacement for a unit that isn't worth fixing</td><td>$3,500 to $6,000 and up</td></tr>
</tbody></table>
<p>The first two rows cover most calls. Boards and gas valves are the middle. The heat exchanger is the one to think about, because on a heater more than ten or twelve years old it costs close to what a new heater does.</p>
<h2>When replacement wins</h2>
<p>Three things push the answer toward a new heater: the unit is past ten years, the failed part is the exchanger or the board, and the heater was undersized for the spa to begin with. A new 400,000 BTU heater from Raypak, Pentair, Hayward or Jandy heats faster, burns less gas and comes with a warranty. If the gas line or the vent needs work to meet code, that adds to the install, and the quote will say so.</p>
<p>If the heater is under ten years old and the repair is a board or a valve, fix it. Those heaters have a lot of life left.</p>
<h2>Why heaters fail early here</h2>
<p>Conejo Valley water is hard. Calcium drops out inside the exchanger tubes and builds a layer that slows heat transfer, so the heater runs longer and hotter to do the same job. Low pH does the opposite damage and eats the copper. Keeping calcium and pH balanced is the cheapest way to make a heater last. A clean filter is next, because a heater that sees proper flow doesn't cycle on its pressure switch all day.</p>
<p>Run the heater now and then in the off-season too. Spiders and corrosion get into burners that sit for months.</p>"""),

        dict(slug="hayward-aquarite-lights", title="Reading the lights on a Hayward AquaRite salt system",
             summary="The AquaRite's panel tells you most of what's wrong. Here is what each light means, and what to check before you buy salt or a new cell.",
             related=("salt-system-repair", "Salt system repair"), issue="Salt system",
             body=f"""
<p>The Hayward AquaRite is the salt system on more Conejo Valley pools than any other, and its front panel tells you most of what's wrong if you know how to read it. Here is what each light means and what to do before you buy anything.</p>
<h2>Check salt, or low salt</h2>
<p>The AquaRite doesn't measure salt directly. It measures how well the water conducts electricity through the cell and reads that as salt. Two things fool it. Cold water conducts less, so from about November to March the panel reads low even when the salt is fine. And a worn or scaled cell conducts less, which also looks like low salt.</p>
<p>So before adding salt, test the water. A salt test strip or a sample at a pool store gives you the real number. The AquaRite wants 2,700 to 3,400 ppm, with 3,200 as the target. If the test says the salt is fine and the panel says it isn't, the problem is the cell or the water temperature, and bags of salt won't help. They'll just leave you with a salty pool.</p>
<h2>Inspect cell</h2>
<p>This one isn't a fault. The system turns it on every 500 hours of operation as a reminder. Pull the cell and look through it. White crust on the plates is calcium scale, which is normal in our hard water and comes off with a diluted muriatic acid soak. Pour acid into water, never the other way, soak until the foaming stops, rinse and reinstall. If the plates are clean, put it back. Hold the diagnostic button for about three seconds to clear the light.</p>
<p>Scale left on the plates makes the cell work harder and shortens its life, so cleaning every three months is a good habit here.</p>
<h2>No flow</h2>
<p>The cell only makes chlorine when the flow switch confirms water is moving. If the light is on with the pump running, check the filter pressure first. A dirty filter, a closed valve or air in the line drops flow below what the switch wants. If flow is fine, the switch paddle may be stuck or the switch has failed. Either way, no chlorine is being made until it's fixed, and the pool will show it within a week in summer.</p>
<h2>High salt</h2>
<p>Usually the result of adding salt for a low salt light that was really a cold-water or worn-cell reading. The only fix is to drain some water and refill. Test first, add later.</p>
<h2>The cell itself</h2>
<p>A T-Cell-15 is rated for about 10,000 hours, which works out to three to five years at normal run times, less when scale is left on the plates. The diagnostic display shows the cell's voltage and amperage, and a cell drawing low current with the salt at the right level is a cell that's wearing out. A tech can tell from those numbers whether you need a new cell or just a cleaning.</p>
<h2>One more thing: stabilizer</h2>
<p>A salt pool with no chlorine reading and a healthy cell often has a stabilizer problem. Hayward recommends cyanuric acid between 60 and 80 ppm for salt pools. Too little and the sun burns off chlorine as fast as the cell makes it. Years of tablets before the salt conversion can push it well past 100, where the chlorine is there but tied up. A partial drain is the only fix for that.</p>"""),

        dict(slug="how-to-clear-a-green-pool", title="How to clear a green pool, and when to stop and call",
             summary="Something stopped before the pool turned. Fix that first, then brush, shock and filter in the right order. And know when a drain is the cheaper answer.",
             related=("green-pool-cleanup", "Green pool cleanup"), issue="Green pool",
             body=f"""
<p>A pool goes green for one reason: chlorine stopped keeping up. Something behind that stopped first, usually the pump, the filter or the chlorinator, and if you don't fix that part the pool will be green again in a month. Here is the order of operations, and the point where it's cheaper to call.</p>
<h2>1. Find out what stopped</h2>
<p>Is the pump running? Is the filter pressure normal, or pinned high? Is the chlorinator empty, or the salt cell showing a fault? Fix the equipment first. Shocking a pool with no circulation wastes the chlorine.</p>
<h2>2. Test before you treat</h2>
<p>Free chlorine, pH and stabilizer (cyanuric acid). Stabilizer decides the plan. If it's over about 100 ppm, chlorine can't work no matter how much you add, and the fix is a partial drain and refill. Years of tablets do this. If stabilizer is reasonable, you can treat the pool where it stands.</p>
<h2>3. Brush, then shock</h2>
<p>Brush the walls, steps and corners so the algae is in the water where chlorine can reach it. Then add liquid chlorine, not tablets. A rough starting dose for a light green pool is a gallon of 12.5 percent liquid chlorine per 10,000 gallons, added in the evening with the pump running. Test the next morning. If the chlorine is gone, the algae ate it, so dose again. You're done shocking when the water holds chlorine overnight.</p>
<h2>4. Run the pump around the clock and clean the filter</h2>
<p>Dead algae clogs the filter fast. Watch the pressure gauge and clean the cartridge or backwash whenever it climbs eight to ten psi over clean, which may be daily for a few days. If you have a multiport valve, vacuum the dead algae to waste so it never hits the filter at all. Gray, cloudy water after the green is gone is a filtration problem, not a chemical one. Keep filtering.</p>
<h2>5. Expect a few days</h2>
<p>Light green with working equipment clears in three to five days. Dark green takes a week or more. Black algae rooted in the plaster is a different problem that needs scrubbing and spot treatment, and a pool that sat swampy for months is often cheaper to drain and acid wash than to fight.</p>
<h2>When to call</h2>
<ul>
<li>The pump, filter or chlorinator isn't working. That's a repair before it's a cleanup.</li>
<li>Stabilizer is over 100 ppm. Draining a pool safely takes more than a hose, especially with old plaster or a high water table.</li>
<li>You can't see the bottom. That's a safety problem as much as a water problem.</li>
<li>You've shocked twice and it's still green. Phosphates or stabilizer are probably why, and a test will say which.</li>
<li>The algae is black, or the pool was green for months.</li>
</ul>
<p>Once the water is clear, get the cause fixed, or you'll be reading this again next summer.</p>"""),

        dict(slug="pool-leak-bucket-test", title="The bucket test: is your pool leaking or just evaporating?",
             summary="A bucket, a marker and 24 hours tell you whether the pool is leaking. Here is how to run the test and what the result means.",
             related=("pool-leak-detection", "Leak detection"), issue="Losing water / leak",
             body=f"""
<p>Every pool loses water. In Conejo Valley summer heat with a little wind, a quarter inch a day is normal evaporation, and a heated spa or a Santa Ana week can double that. The bucket test tells you in a day whether what you're seeing is weather or a leak, and it costs nothing.</p>
<h2>The test</h2>
<ol>
<li>Fill the pool to its normal level and turn off the autofill if you have one.</li>
<li>Set a bucket on the second step and fill it so the water inside matches the pool level outside. Weigh it down with a brick if it floats.</li>
<li>Mark the water level inside the bucket and on the outside of the bucket with tape or a marker.</li>
<li>Turn the pump off and wait 24 hours. No swimming.</li>
<li>Compare the two marks. Evaporation lowers both the same. If the pool dropped more than the bucket did, you have a leak.</li>
<li>Repeat with the pump running for 24 hours.</li>
</ol>
<h2>Reading the result</h2>
<p>If the pool loses more with the pump off than on, the leak is on the suction side or in the shell: a skimmer throat, the light niche, a return fitting or a crack. If it loses more with the pump running, the leak is on the pressure side, in the plumbing between the pump and the returns, which is often underground. The same loss either way points to the shell. Those three answers are what a leak tech wants to know on the phone.</p>
<h2>Where leaks usually are</h2>
<p>The equipment pad first: a weeping pump seal, a filter drain plug, a heater that drips when it's running. Then the skimmer, where the plastic throat meets the concrete. Then the light niche and the conduit behind it. Returns and spa spillovers after that. Cracks in the shell and underground plumbing are last on the list, which is why most leak repairs never touch the deck.</p>
<h2>Other signs</h2>
<ul>
<li>The autofill runs all the time.</li>
<li>Air bubbles at the returns, or air under the pump lid, with the water level fine. A suction leak pulls air in when the pump is on and lets water out when it's off.</li>
<li>Wet or soft ground near the pad or along the deck edge.</li>
<li>Chemistry that won't hold, because fresh fill water keeps diluting it.</li>
</ul>
<h2>What to do next</h2>
<p>Keep the water above the skimmer so the pump doesn't run dry, and keep filling until it's fixed. Leak detection is pressure testing on each line and dye testing around the fittings, and when the leak is at the pad or the skimmer, which it usually is, the repair is often the same visit.</p>"""),
    ]
    POST_DATE, POST_DATE_TEXT = "2026-10-12", "October 2026"
    for p in posts:
        pslug = f"blog/{p['slug']}"
        rel_s, rel_n = p["related"]
        body = section(f"""
<article class="post">
  <p class="post-meta"><a href="{href('blog')}">Blog</a> &nbsp;·&nbsp; {POST_DATE_TEXT}</p>
  <h1>{p['title']}</h1>
  <p class="lede">{p['summary']}</p>
  {p['body']}
  <p class="post-related">Related: <a href="{href(rel_s)}">{rel_n}</a> in Thousand Oaks and the Conejo Valley. Questions about your pool? <a href="{href('contact')}">Send us the details</a>.</p>
</article>""")
        body += request_section(pslug, "Want a tech to look at it?", "Call, text or send the form. We call back to schedule a visit.", default_issue=p["issue"], cls="sky")
        ld = [{"@type": "BlogPosting", "headline": p["title"], "description": p["summary"], "datePublished": POST_DATE, "dateModified": POST_DATE,
               "author": {"@type": "Organization", "name": "Miller Pool and Spa"}, "publisher": {"@id": BASE + "/#business"},
               "mainEntityOfPage": f"{BASE}/{pslug}/", "url": f"{BASE}/{pslug}/"}]
        add(pslug, f"{p['title']} | Miller Pool and Spa", p["summary"], body, ld)

    items = "".join(f"""<article><p class="post-meta">{POST_DATE_TEXT}</p><h2><a href="{href('blog/' + p['slug'])}">{p['title']}</a></h2><p>{p['summary']}</p></article>""" for p in posts)
    body = section(f"""
<h1>Blog</h1>
<p class="lede max mt">Practical notes from our techs on pumps, heaters, salt systems, leaks and green pools, written for pool owners in the Conejo Valley.</p>
<div class="posts">{items}</div>""")
    body += request_section("blog", "Have a question we haven't covered?", "Call, text or send the form. If it's one we hear a lot, it'll end up here.", cls="sky")
    add("blog", "Blog | Miller Pool and Spa", "Practical notes on pool pumps, heaters, salt systems, leak detection and green pools from Miller Pool and Spa in Newbury Park.", body,
        [{"@type": "Blog", "name": "Miller Pool and Spa blog", "url": f"{BASE}/blog/", "publisher": {"@id": BASE + "/#business"},
          "blogPost": [{"@type": "BlogPosting", "headline": p["title"], "url": f"{BASE}/blog/{p['slug']}/", "datePublished": POST_DATE} for p in posts]}])

    # ---------- Privacy (short placeholder, real sites have one)
    slug = "privacy-policy"
    body = section("""
<h1>Privacy policy</h1>
<div class="prose mt">
  <p>Miller Pool and Spa uses the information you send through this site (name, phone, address, what's wrong with the pool) to call you back and schedule service. We don't sell it or add you to a mailing list.</p>
  <p>Call tracking numbers on this site may record calls for quality and training. If you'd rather not be recorded, say so at the start of the call.</p>
  <p>This page will be replaced with the full policy before launch.</p>
</div>""")
    add(slug, "Privacy Policy | Miller Pool and Spa", "Privacy policy for Miller Pool and Spa.", body)

# ---------------------------------------------------------------- render

def ld_script(blocks):
    return '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@graph": [BUSINESS_LD] + blocks}, ensure_ascii=False) + "</script>"

FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Lato:wght@400;700;900&display=swap">'

def render_site():
    global MODE, PAGES
    MODE = "site"; PAGES = []
    build_pages()
    os.makedirs(os.path.join(SITE_DIR, "assets"), exist_ok=True)
    open(os.path.join(SITE_DIR, "assets", "site.css"), "w").write(CSS.strip() + "\n")
    open(os.path.join(SITE_DIR, "assets", "site.js"), "w").write(JS_COMMON.strip() + "\n")
    import shutil; shutil.copy(LOGO_PNG, os.path.join(SITE_DIR, "assets", "miller-logo.png"))
    hdr, ftr, top = header(), footer(), topbar()
    index = []
    for slug, title, desc, body, ld in PAGES:
        path = "/" if not slug else f"/{slug}/"
        doc = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{html.escape(desc, quote=True)}">
<link rel="canonical" href="{BASE}{path}">
{FONTS}
<link rel="stylesheet" href="/assets/site.css">
</head>
<body>
{top}
{hdr}
<main>
{body}
</main>
{ftr}
{ld_script(ld)}
<script src="/assets/site.js"></script>
</body>
</html>
"""
        d = os.path.join(SITE_DIR, slug) if slug else SITE_DIR
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(doc)
        index.append((path, title))
    return index

def render_preview():
    global MODE, PAGES
    MODE = "preview"; PAGES = []
    build_pages()
    pages_html = []
    for slug, title, desc, body, ld in PAGES:
        pid = "pg-" + (slug or "home")
        hidden = "" if not slug else " hidden"
        pages_html.append(f'<div class="page" id="{pid}" data-title="{html.escape(title, quote=True)}"{hidden}>{body}{ld_script(ld)}</div>')
    doc = f"""<title>Miller Pool and Spa</title>
{FONTS}
<style>{CSS}</style>
{topbar()}
{header()}
<main>
{''.join(pages_html)}
</main>
{footer()}
<script>{JS_COMMON}{JS_ROUTER}</script>
"""
    open(PREVIEW_FILE, "w", encoding="utf-8").write(doc)
    return len(doc)

if __name__ == "__main__":
    idx = render_site()
    n = render_preview()
    print(f"site: {len(idx)} pages -> {SITE_DIR}")
    for p, t in idx:
        print(f"  {p:34s} {t}")
    print(f"preview: {n:,} bytes -> {PREVIEW_FILE}")

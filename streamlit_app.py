import streamlit as st
import time
import threading
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

st.set_page_config(
    page_title="YKTI RAWAT",
    page_icon="🦂",
    layout="wide",
    initial_sidebar_state="collapsed"
)

custom_css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Share+Tech+Mono&display=swap');

    * { box-sizing: border-box; margin: 0; padding: 0; }

    /* ── BACKGROUND WALLPAPER ── */
    .stApp {
        min-height: 100vh;
        background:
            linear-gradient(rgba(0,0,0,0.72), rgba(0,0,0,0.78)),
            url('https://images.unsplash.com/photo-1518770660439-4636190af475?w=1920&q=80') center/cover no-repeat fixed;
    }

    /* animated grid overlay */
    .stApp::before {
        content: '';
        position: fixed; top:0; left:0; right:0; bottom:0;
        background-image:
            linear-gradient(rgba(120,0,255,0.06) 1px, transparent 1px),
            linear-gradient(90deg, rgba(120,0,255,0.06) 1px, transparent 1px);
        background-size: 48px 48px;
        z-index: 0; pointer-events: none;
        animation: gridDrift 25s linear infinite;
    }
    @keyframes gridDrift { 0%{transform:translateY(0)} 100%{transform:translateY(48px)} }

    /* ── MAIN CONTAINER ── */
    .main .block-container {
        background: rgba(4,0,18,0.82);
        backdrop-filter: blur(18px);
        -webkit-backdrop-filter: blur(18px);
        border-radius: 20px;
        padding: 1.6rem 2.2rem 2.5rem;
        border: 1px solid rgba(130,0,255,0.30);
        box-shadow:
            0 0 80px rgba(100,0,255,0.18),
            0 0 200px rgba(255,0,100,0.06),
            inset 0 1px 0 rgba(255,255,255,0.04);
        margin-top: 0.6rem;
        position: relative; z-index: 1;
    }

    /* ── HEADER ── */
    .hdr { text-align:center; padding:1.2rem 1rem 0.5rem; }
    .hdr::after {
        content:''; display:block; height:2px; margin-top:1.1rem;
        background:linear-gradient(90deg,transparent,#7b00ff,#ff0080,#00c8ff,transparent);
        animation:lineGlow 3s ease-in-out infinite;
    }
    @keyframes lineGlow { 0%,100%{opacity:.55} 50%{opacity:1;box-shadow:0 0 18px rgba(255,0,128,.7)} }

    .hdr-title {
        font-family:'Orbitron',sans-serif; font-weight:900; font-size:2.5rem;
        letter-spacing:5px; text-transform:uppercase;
        background:linear-gradient(135deg,#b400ff,#ff0080,#00c8ff);
        -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text;
        filter:drop-shadow(0 0 18px rgba(180,0,255,.55));
        animation:hdrPulse 4s ease-in-out infinite;
    }
    @keyframes hdrPulse {
        0%,100%{filter:drop-shadow(0 0 14px rgba(180,0,255,.5))}
        50%{filter:drop-shadow(0 0 28px rgba(255,0,128,.8))}
    }
    .hdr-sub {
        font-family:'Share Tech Mono',monospace; font-size:0.78rem;
        color:rgba(170,0,255,.75); letter-spacing:3px; text-transform:uppercase; margin-top:0.35rem;
    }

    /* ── STATUS METRICS ── */
    .metrics { display:flex; gap:10px; margin:1.1rem 0; flex-wrap:wrap; }
    .mbox {
        flex:1; min-width:100px;
        background:rgba(8,0,25,0.75); border:1px solid rgba(110,0,255,0.38);
        border-radius:12px; padding:0.8rem 0.5rem; text-align:center;
    }
    .mval {
        font-family:'Orbitron',sans-serif; font-size:1.3rem; font-weight:900;
        background:linear-gradient(135deg,#b400ff,#ff0080);
        -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text;
        display:block; line-height:1.2;
    }
    .mlbl {
        font-family:'Share Tech Mono',monospace; font-size:0.56rem;
        color:rgba(160,90,255,.55); letter-spacing:2px; text-transform:uppercase; margin-top:4px; display:block;
    }
    .run { color:#00ff88!important; -webkit-text-fill-color:#00ff88!important; background:none!important;
           text-shadow:0 0 10px rgba(0,255,136,.55); animation:blink 1.6s ease-in-out infinite; }
    .stp { color:#ff4444!important; -webkit-text-fill-color:#ff4444!important; background:none!important; }
    @keyframes blink { 0%,100%{opacity:1} 50%{opacity:.5} }

    /* ── BUTTONS ── */
    .stButton > button {
        background:linear-gradient(135deg,rgba(110,0,255,.28),rgba(255,0,110,.22)) !important;
        color:#fff !important; border:1px solid rgba(110,0,255,.55) !important;
        border-radius:10px !important; padding:0.65rem 1rem !important;
        font-family:'Orbitron',sans-serif !important; font-weight:700 !important;
        font-size:0.68rem !important; letter-spacing:2px !important;
        text-transform:uppercase !important; width:100% !important;
        transition:all .28s ease !important;
    }
    .stButton > button:hover {
        background:linear-gradient(135deg,rgba(110,0,255,.6),rgba(255,0,110,.55)) !important;
        border-color:#ff0080 !important; box-shadow:0 0 18px rgba(255,0,128,.4) !important;
        transform:translateY(-1px) !important;
    }
    .stButton > button:disabled { opacity:.28 !important; transform:none !important; }

    /* ── INPUTS ── */
    .stTextInput>div>div>input,
    .stNumberInput>div>div>input {
        background:rgba(8,0,25,.9) !important; border:1px solid rgba(110,0,255,.48) !important;
        border-radius:9px !important; color:#ddb8ff !important;
        padding:.65rem .95rem !important;
        font-family:'Share Tech Mono',monospace !important; font-size:.86rem !important;
    }
    .stTextInput>div>div>input:focus,
    .stNumberInput>div>div>input:focus {
        border-color:#ff0080 !important; box-shadow:0 0 0 2px rgba(255,0,128,.18) !important; outline:none !important;
    }
    .stTextArea>div>div>textarea {
        background:rgba(8,0,25,.9) !important; border:1px solid rgba(110,0,255,.48) !important;
        border-radius:9px !important; color:#ddb8ff !important;
        font-family:'Share Tech Mono',monospace !important; font-size:.82rem !important;
    }
    .stTextArea>div>div>textarea:focus {
        border-color:#ff0080 !important; box-shadow:0 0 0 2px rgba(255,0,128,.18) !important;
    }

    /* ── LABELS ── */
    label, .stTextInput label, .stTextArea label, .stNumberInput label,
    [data-testid="stFileUploader"] label {
        color:rgba(190,90,255,.9) !important;
        font-family:'Orbitron',sans-serif !important;
        font-size:.63rem !important; font-weight:700 !important;
        letter-spacing:1.8px !important; text-transform:uppercase !important;
    }

    /* ── RADIO ── */
    .stRadio>div {
        background:rgba(8,0,25,.55) !important; border-radius:9px !important;
        padding:.6rem .9rem !important; border:1px solid rgba(110,0,255,.28) !important;
    }
    .stRadio label {
        color:rgba(190,90,255,.88) !important; font-family:'Share Tech Mono',monospace !important;
        font-size:.85rem !important; letter-spacing:.5px !important; text-transform:none !important;
    }

    /* ── FILE UPLOADER ── */
    [data-testid="stFileUploader"] {
        background:rgba(8,0,25,.65) !important;
        border:1.5px dashed rgba(110,0,255,.45) !important;
        border-radius:10px !important;
    }
    [data-testid="stFileUploader"]:hover {
        border-color:rgba(255,0,128,.6) !important;
        box-shadow:0 0 14px rgba(255,0,128,.12) !important;
    }

    /* ── EXPANDERS ── */
    .streamlit-expanderHeader {
        background:rgba(8,0,25,.82) !important; border:1px solid rgba(110,0,255,.38) !important;
        border-radius:11px !important; color:#bb55ff !important;
        font-family:'Orbitron',sans-serif !important; font-size:.68rem !important;
        letter-spacing:1.8px !important; padding:.75rem 1.1rem !important;
    }
    .streamlit-expanderHeader:hover {
        border-color:rgba(255,0,128,.55) !important; box-shadow:0 0 14px rgba(110,0,255,.2) !important;
    }
    .streamlit-expanderContent {
        background:rgba(4,0,14,.68) !important; border:1px solid rgba(110,0,255,.22) !important;
        border-top:none !important; border-radius:0 0 11px 11px !important; padding:1.1rem !important;
    }

    /* ── CONSOLE ── */
    .console-wrap {
        background:#000; border:1px solid rgba(0,255,136,.28);
        border-radius:12px; overflow:hidden; margin-top:.4rem;
    }
    .console-bar {
        background:rgba(0,28,14,.92); border-bottom:1px solid rgba(0,255,136,.18);
        padding:.45rem .9rem; display:flex; align-items:center; gap:7px;
        font-family:'Share Tech Mono',monospace; font-size:.68rem;
        color:rgba(0,255,136,.65); letter-spacing:1px;
    }
    .cd { width:9px; height:9px; border-radius:50%; display:inline-block; }
    .cr{background:#ff5f57} .cy{background:#febc2e} .cg{background:#28c840}
    .console-out {
        background:#000; font-family:'Share Tech Mono',monospace;
        font-size:.74rem; color:#00ff88; line-height:1.85;
        max-height:360px; overflow-y:auto; padding:.75rem;
        scrollbar-width:thin; scrollbar-color:rgba(110,0,255,.45) transparent;
    }
    .console-out::-webkit-scrollbar{width:4px}
    .console-out::-webkit-scrollbar-thumb{background:rgba(110,0,255,.5);border-radius:2px}
    .lg{padding:2px 0;border-bottom:1px solid rgba(0,255,136,.04);word-break:break-all;}
    .lg::before{content:'» ';color:rgba(170,0,255,.65);font-weight:bold;}
    .ls{color:#00ff88}.le{color:#ff4444}.lw{color:#ffaa00}.li{color:#00c8ff}

    /* ── BADGE / PILL ── */
    .pill {
        display:inline-block; margin:2px;
        background:rgba(8,0,25,.75); border:1px solid rgba(110,0,255,.35);
        border-radius:7px; padding:3px 11px;
        font-family:'Share Tech Mono',monospace; font-size:.65rem;
        color:rgba(170,95,255,.8); letter-spacing:.8px;
    }

    /* ── DIVIDER ── */
    hr { border:none!important; height:1px!important;
         background:linear-gradient(90deg,transparent,rgba(110,0,255,.38),rgba(255,0,110,.35),transparent)!important;
         margin:.9rem 0!important; }

    /* ── ALERTS ── */
    .stSuccess,[data-testid="stNotification"]{background:rgba(0,45,22,.8)!important;border:1px solid rgba(0,200,90,.38)!important;border-radius:9px!important;color:#00ff88!important;}
    .stWarning{background:rgba(45,28,0,.8)!important;border:1px solid rgba(255,170,0,.35)!important;border-radius:9px!important;}
    .stError{background:rgba(45,0,0,.8)!important;border:1px solid rgba(255,45,45,.35)!important;border-radius:9px!important;}

    /* ── SIDEBAR HIDE ── */
    [data-testid="stSidebar"]{display:none!important;}

    /* ── FOOTER ── */
    .ftr{
        text-align:center; padding:.9rem; margin-top:1.4rem;
        font-family:'Share Tech Mono',monospace; font-size:.65rem;
        color:rgba(110,0,255,.4); letter-spacing:2px; text-transform:uppercase;
        border-top:1px solid rgba(110,0,255,.18);
    }

    /* ── SCROLLBAR ── */
    ::-webkit-scrollbar{width:5px;height:5px}
    ::-webkit-scrollbar-track{background:rgba(8,0,25,.5)}
    ::-webkit-scrollbar-thumb{background:linear-gradient(#7b00ff,#ff0080);border-radius:3px}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ══════════════════════════════════════════════
#  SESSION STATE
# ══════════════════════════════════════════════
class AutomationState:
    def __init__(self):
        self.running = False
        self.message_count = 0
        self.logs = []
        self.rot_idx = 0

if 'astate'        not in st.session_state: st.session_state.astate        = AutomationState()
if 'cookie_mode'   not in st.session_state: st.session_state.cookie_mode   = 'single'
if 'multi_cookies' not in st.session_state: st.session_state.multi_cookies = []
if 'single_cookie' not in st.session_state: st.session_state.single_cookie = ''
if 'msg_list'      not in st.session_state: st.session_state.msg_list      = []
if 'cfg' not in st.session_state:
    st.session_state.cfg = {'chat_id':'','name_prefix':'','delay':30,'cookies':'','messages':''}

astate = st.session_state.astate
cfg    = st.session_state.cfg

# ══════════════════════════════════════════════
#  HELPERS
# ══════════════════════════════════════════════
def lg(msg, s=None):
    ts  = time.strftime("%H:%M:%S")
    fmt = f"[{ts}] {msg}"
    (s if s else st.session_state.astate).logs.append(fmt)

def log_cls(log):
    lo = log.lower()
    if '✅' in log or 'sent' in lo or 'success' in lo: return 'ls'
    if '❌' in lo  or 'error' in lo or 'fail' in lo or 'fatal' in lo: return 'le'
    if '⚠'  in log or 'warn' in lo or 'not found' in lo: return 'lw'
    return 'li'

def find_input(driver, pid, s=None):
    lg(f'{pid}: Searching message input…', s); time.sleep(10)
    try:
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight);"); time.sleep(2)
        driver.execute_script("window.scrollTo(0,0);"); time.sleep(2)
    except: pass
    try: lg(f'{pid}: {driver.title} | {driver.current_url}', s)
    except: pass
    sels = [
        'div[contenteditable="true"][role="textbox"]',
        'div[contenteditable="true"][data-lexical-editor="true"]',
        'div[aria-label*="message" i][contenteditable="true"]',
        'div[contenteditable="true"][spellcheck="true"]',
        '[role="textbox"][contenteditable="true"]',
        'textarea[placeholder*="message" i]',
        '[contenteditable="true"]',
        'textarea',
        'input[type="text"]',
    ]
    for idx, sel in enumerate(sels):
        try:
            els = driver.find_elements(By.CSS_SELECTOR, sel)
            lg(f'{pid}: sel {idx+1} → {len(els)} el', s)
            for el in els:
                try:
                    ok = driver.execute_script(
                        "return arguments[0].contentEditable==='true'||arguments[0].tagName==='TEXTAREA'||arguments[0].tagName==='INPUT';", el)
                    if ok:
                        try: el.click(); time.sleep(.4)
                        except: pass
                        txt = driver.execute_script(
                            "return arguments[0].placeholder||arguments[0].getAttribute('aria-label')||arguments[0].getAttribute('aria-placeholder')||'';", el).lower()
                        kws = ['message','write','type','send','chat','msg','reply','text','aa']
                        if any(k in txt for k in kws) or idx < 8:
                            lg(f'{pid}: ✅ Input found (sel {idx+1})', s); return el
                except: continue
        except: continue
    return None

def make_browser(s=None):
    lg('Setting up browser…', s)
    opts = Options()
    for a in ['--headless=new','--no-sandbox','--disable-setuid-sandbox',
              '--disable-dev-shm-usage','--disable-gpu','--disable-extensions','--window-size=1920,1080']:
        opts.add_argument(a)
    opts.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36')
    for p in ['/usr/bin/chromium','/usr/bin/chromium-browser','/usr/bin/google-chrome']:
        if Path(p).exists(): opts.binary_location=p; lg(f'Chromium: {p}', s); break
    dp = next((p for p in ['/usr/bin/chromedriver','/usr/local/bin/chromedriver'] if Path(p).exists()), None)
    from selenium.webdriver.chrome.service import Service
    svc = Service(executable_path=dp) if dp else None
    driver = webdriver.Chrome(service=svc, options=opts) if svc else webdriver.Chrome(options=opts)
    driver.set_window_size(1920,1080); lg('✅ Browser ready!', s); return driver

def add_cookies(driver, raw, s, pid):
    if not raw or not raw.strip(): return
    n = 0
    for c in raw.split(';'):
        c = c.strip()
        if c:
            i = c.find('=')
            if i > 0:
                try: driver.add_cookie({'name':c[:i].strip(),'value':c[i+1:].strip(),'domain':'.facebook.com','path':'/'}); n+=1
                except: pass
    lg(f'{pid}: ✅ Applied {n} cookies', s)

def next_msg(msgs, s=None):
    if not msgs: return 'Hello!'
    if s: m = msgs[s.rot_idx % len(msgs)]; s.rot_idx+=1; return m
    return msgs[0]

def send_loop(config, s, pid='AUTO-1'):
    driver = None
    try:
        lg(f'{pid}: Starting…', s)
        driver = make_browser(s)
        driver.get('https://www.facebook.com/'); time.sleep(8)
        add_cookies(driver, config['cookies'], s, pid)
        cid = config['chat_id'].strip()
        lg(f'{pid}: Opening conversation {cid}…', s)
        driver.get(f'https://www.facebook.com/messages/t/{cid}' if cid else 'https://www.facebook.com/messages')
        time.sleep(15)
        inp = find_input(driver, pid, s)
        if not inp:
            lg(f'{pid}: ❌ Message input not found!', s); s.running=False; return 0
        delay = int(config['delay'])
        msgs  = [m.strip() for m in config['messages'].split('\n') if m.strip()] or ['Hello!']
        sent  = 0
        while s.running:
            base = next_msg(msgs, s)
            full = f"{config['name_prefix']} {base}" if config['name_prefix'] else base
            try:
                driver.execute_script("""
                    const el=arguments[0],msg=arguments[1];
                    el.scrollIntoView({behavior:'smooth',block:'center'});
                    el.focus();el.click();
                    if(el.tagName==='DIV'){el.textContent=msg;el.innerHTML=msg;}else{el.value=msg;}
                    el.dispatchEvent(new Event('input',{bubbles:true}));
                    el.dispatchEvent(new Event('change',{bubbles:true}));
                    el.dispatchEvent(new InputEvent('input',{bubbles:true,data:msg}));
                """, inp, full)
                time.sleep(1)
                res = driver.execute_script("""
                    const bs=document.querySelectorAll('[aria-label*="Send" i]:not([aria-label*="like" i]),[data-testid="send-button"]');
                    for(let b of bs){if(b.offsetParent!==null){b.click();return 'ok';}} return 'enter';
                """)
                if res=='enter':
                    driver.execute_script("""
                        const el=arguments[0];el.focus();
                        ['keydown','keypress','keyup'].forEach(t=>el.dispatchEvent(
                            new KeyboardEvent(t,{key:'Enter',code:'Enter',keyCode:13,which:13,bubbles:true})));
                    """, inp)
                sent+=1; s.message_count=sent
                lg(f'{pid}: ✅ #{sent} sent — "{full[:45]}"  | wait {delay}s', s)
                time.sleep(delay)
            except Exception as e:
                lg(f'{pid}: send error: {str(e)[:80]}', s); time.sleep(5)
        lg(f'{pid}: ⚠️ Stopped. Total: {sent}', s); return sent
    except Exception as e:
        lg(f'{pid}: ❌ Fatal: {str(e)}', s); s.running=False; return 0
    finally:
        if driver:
            try: driver.quit(); lg(f'{pid}: Browser closed', s)
            except: pass

def run_multi(cfgs, s):
    ts = [threading.Thread(target=send_loop, args=(c, s, f'COOKIE-{i+1}'), daemon=True) for i,c in enumerate(cfgs)]
    for t in ts: t.start()
    for t in ts: t.join()

def start_auto(config):
    s = st.session_state.astate
    if s.running: return
    s.running=True; s.message_count=0; s.logs=[]; s.rot_idx=0
    lg('🚀 Automation starting…', s)
    if st.session_state.cookie_mode=='multiple' and st.session_state.multi_cookies:
        cfgs = [{**config,'cookies':ck} for ck in st.session_state.multi_cookies]
        t = threading.Thread(target=run_multi, args=(cfgs,s), daemon=True)
    else:
        t = threading.Thread(target=send_loop, args=(config,s), daemon=True)
    t.start()

def stop_auto():
    st.session_state.astate.running = False
    lg('⚠️ Stop requested.', st.session_state.astate)

# ══════════════════════════════════════════════
#  HEADER
# ══════════════════════════════════════════════
st.markdown("""
<div class="hdr">
    <div class="hdr-title">YKTI RAWAT</div>
    <div class="hdr-sub">PREMIUM E2EE OFFLINE CONVO SYSTEM</div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════
#  STATUS BAR
# ══════════════════════════════════════════════
is_run   = astate.running
scls     = 'run' if is_run else 'stp'
stxt     = 'RUNNING' if is_run else 'STOPPED'
cid_disp = (cfg['chat_id'][:10]+'…') if cfg['chat_id'] and len(cfg['chat_id'])>10 else (cfg['chat_id'] or 'NOT SET')
ck_disp  = f"{len(st.session_state.multi_cookies)} COOKIES" if st.session_state.cookie_mode=='multiple' else ("SET" if st.session_state.single_cookie.strip() else "NONE")
mc_cnt   = len([m for m in cfg['messages'].split('\n') if m.strip()]) if cfg['messages'] else 0

st.markdown(f"""
<div class="metrics">
    <div class="mbox"><span class="mval">{astate.message_count}</span><span class="mlbl">SENT</span></div>
    <div class="mbox"><span class="mval {scls}">{stxt}</span><span class="mlbl">STATUS</span></div>
    <div class="mbox"><span class="mval" style="font-size:.88rem;">{cid_disp}</span><span class="mlbl">CHAT ID</span></div>
    <div class="mbox"><span class="mval" style="font-size:.88rem;">{ck_disp}</span><span class="mlbl">COOKIE</span></div>
    <div class="mbox"><span class="mval" style="font-size:.88rem;">{mc_cnt}</span><span class="mlbl">MESSAGES</span></div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════
#  START / STOP / REFRESH BUTTONS
# ══════════════════════════════════════════════
b1, b2, b3 = st.columns([2,2,1], gap="small")
with b1:
    if st.button("START AUTOMATION", key="start_btn", disabled=is_run or not cfg['chat_id'], use_container_width=True):
        start_auto(cfg)
        st.success("Automation started!")
        st.rerun()
with b2:
    if st.button("STOP AUTOMATION", key="stop_btn", disabled=not is_run, use_container_width=True):
        stop_auto()
        st.warning("Stop signal sent!")
        st.rerun()
with b3:
    if st.button("REFRESH", key="ref_btn", use_container_width=True):
        st.rerun()

st.markdown("<hr>", unsafe_allow_html=True)

# ══════════════════════════════════════════════
#  PANEL 1 — TARGET SETTINGS
# ══════════════════════════════════════════════
with st.expander("TARGET SETTINGS", expanded=True):
    c1, c2, c3 = st.columns([2,2,1], gap="medium")
    with c1:
        v_chatid = st.text_input("CHAT / E2EE ID", value=cfg['chat_id'], placeholder="1362400298935018")
    with c2:
        v_prefix = st.text_input("NAME PREFIX", value=cfg['name_prefix'], placeholder="[YKTI RAWAT]")
    with c3:
        v_delay  = st.number_input("DELAY (SEC)", min_value=1, max_value=300, value=cfg['delay'])
    # auto-save on change
    st.session_state.cfg['chat_id']     = v_chatid
    st.session_state.cfg['name_prefix'] = v_prefix
    st.session_state.cfg['delay']       = int(v_delay)

# ══════════════════════════════════════════════
#  PANEL 2 — COOKIE CONFIG
# ══════════════════════════════════════════════
with st.expander("COOKIE CONFIG", expanded=False):
    ck_mode = st.radio("COOKIE MODE",
                       ["Single Cookie", "Multiple Cookies (Upload TXT)"],
                       index=0 if st.session_state.cookie_mode=='single' else 1,
                       horizontal=True)
    st.session_state.cookie_mode = 'single' if ck_mode=="Single Cookie" else 'multiple'

    if st.session_state.cookie_mode == 'single':
        sc = st.text_area("PASTE YOUR FACEBOOK COOKIE", value=st.session_state.single_cookie,
                          placeholder="c_user=xxxx; xs=xxxx; datr=xxxx; ...", height=100)
        st.session_state.single_cookie = sc
        st.session_state.cfg['cookies'] = sc
    else:
        ck_f = st.file_uploader("UPLOAD cookie.txt (one cookie per line)", type=['txt'], key="ck_up")
        if ck_f:
            lines = [l.strip() for l in ck_f.read().decode('utf-8','ignore').split('\n') if l.strip()]
            st.session_state.multi_cookies = lines
            if lines: st.session_state.cfg['cookies'] = lines[0]
            st.success(f"Loaded {len(lines)} cookies")
        for i,c in enumerate(st.session_state.multi_cookies):
            p = c[:52]+'…' if len(c)>52 else c
            st.markdown(f'<span class="pill">Cookie {i+1}: {p}</span>', unsafe_allow_html=True)

# ══════════════════════════════════════════════
#  PANEL 3 — MESSAGE FILE UPLOAD
# ══════════════════════════════════════════════
with st.expander("MESSAGE CONFIG", expanded=False):
    msg_f = st.file_uploader("UPLOAD messages.txt  —  one message per line", type=['txt'], key="msg_up")
    if msg_f:
        lines = [l.strip() for l in msg_f.read().decode('utf-8','ignore').split('\n') if l.strip()]
        st.session_state.msg_list = lines
        st.session_state.cfg['messages'] = '\n'.join(lines)
        st.success(f"Loaded {len(lines)} messages")
    if st.session_state.msg_list:
        for i,m in enumerate(st.session_state.msg_list[:6]):
            p = m[:58]+'…' if len(m)>58 else m
            st.markdown(f'<span class="pill">Line {i+1}: {p}</span>', unsafe_allow_html=True)
        if len(st.session_state.msg_list) > 6:
            st.markdown(f'<span class="pill">+{len(st.session_state.msg_list)-6} more messages…</span>', unsafe_allow_html=True)
    elif not st.session_state.msg_list:
        st.markdown('<span class="pill">No messages loaded yet — upload a TXT file above</span>', unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# ══════════════════════════════════════════════
#  LIVE LOGS
# ══════════════════════════════════════════════
total_l   = len(astate.logs)
success_l = sum(1 for l in astate.logs if '✅' in l or 'sent' in l.lower())
error_l   = sum(1 for l in astate.logs if '❌' in l.lower() or 'error' in l.lower())

with st.expander(f"LIVE LOGS  —  {total_l} lines  |  {success_l} ok  |  {error_l} err", expanded=is_run):
    _, clr_col = st.columns([5,1])
    with clr_col:
        if st.button("CLEAR", use_container_width=True, key="clr_logs"):
            st.session_state.astate.logs = []
            st.rerun()

    if astate.logs:
        html = '<div class="console-wrap"><div class="console-bar"><span class="cd cr"></span><span class="cd cy"></span><span class="cd cg"></span>&nbsp;&nbsp;YKTI RAWAT // CONSOLE</div><div class="console-out" id="co">'
        for log in astate.logs[-100:]:
            esc = log.replace('<','&lt;').replace('>','&gt;')
            html += f'<div class="lg {log_cls(log)}">{esc}</div>'
        html += '</div></div><script>var c=document.getElementById("co");if(c)c.scrollTop=c.scrollHeight;</script>'
        st.markdown(html, unsafe_allow_html=True)
    else:
        st.markdown('<div class="console-wrap"><div class="console-bar"><span class="cd cr"></span><span class="cd cy"></span><span class="cd cg"></span>&nbsp;&nbsp;YKTI RAWAT // CONSOLE</div><div class="console-out" style="text-align:center;color:rgba(0,255,136,.2);padding:2rem 1rem;">// NO LOGS YET — START AUTOMATION TO SEE OUTPUT</div></div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════
#  AUTO-REFRESH
# ══════════════════════════════════════════════
if is_run:
    st.markdown('<div style="text-align:center;margin:.6rem 0"><span class="pill" style="border-color:rgba(0,255,136,.45);color:#00ff88;">AUTOMATION RUNNING — auto refresh every 3s</span></div>', unsafe_allow_html=True)
    time.sleep(3)
    st.rerun()

st.markdown('<div class="ftr">MADE WITH ❤ BY YKTI RAWAT &nbsp;|&nbsp; 2026 &nbsp;|&nbsp; PREMIUM E2EE SYSTEM</div>', unsafe_allow_html=True)

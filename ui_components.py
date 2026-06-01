import streamlit as st

def apply_custom_css():
    st.markdown("""
    <style>
      /* Menggunakan font Nunito yang sangat soft, membulat, dan aesthetic */
      @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&family=JetBrains+Mono:wght@400;700&display=swap');
      
      :root {
        --bg-primary:   #E0F2FE; /* Biru langit sangat muda (Sky Blue 100) */
        --bg-card:      rgba(255, 255, 255, 0.65); /* Kaca putih transparan */
        --accent-blue:  #0EA5E9; /* Biru cerah utama (Sky Blue 500) */
        --accent-light: #BAE6FD; /* Biru pastel (Sky Blue 200) */
        --accent-dark:  #0369A1; /* Biru dongker/tegas (Sky Blue 700) */
        --text-main:    #082F49; /* Biru paling gelap untuk teks (Sky Blue 900) */
        --text-muted:   #0284C7; /* Biru medium untuk teks tambahan */
        --border-color: #7DD3FC; /* Garis batas biru awan */
      }

      html, body, [class*="css"] {
        font-family: 'Nunito', sans-serif;
        background-color: var(--bg-primary);
        color: var(--text-main);
      }

      /* Background Aesthetic Awan/Langit */
      .main { 
        background-color: var(--bg-primary);
        background-image: 
          radial-gradient(circle at 15% 50%, rgba(255, 255, 255, 0.4), transparent 25%),
          radial-gradient(circle at 85% 30%, rgba(255, 255, 255, 0.4), transparent 25%);
      }

      h1, h2, h3 {
        font-family: 'Nunito', sans-serif;
        color: var(--accent-dark);
        font-weight: 800;
        letter-spacing: 0.5px;
      }

      /* Sidebar Soft Blue */
      section[data-testid="stSidebar"] {
        background: rgba(240, 249, 255, 0.85); /* Frosty blue */
        border-right: 2px solid #FFFFFF;
        backdrop-filter: blur(10px);
      }
      
      /* Cards & Soft Glassmorphism */
      .stTabs [data-baseweb="tab-panel"], .ds-card {
        background: var(--bg-card) !important;
        border: 2px solid #FFFFFF !important;
        box-shadow: 0 8px 32px rgba(14, 165, 233, 0.1) !important;
        border-radius: 20px !important;
        backdrop-filter: blur(12px);
      }
      
      .stTabs [data-baseweb="tab"] {
        font-family: 'Nunito', sans-serif !important;
        color: var(--text-muted) !important;
        font-weight: 700 !important;
        background: transparent !important;
      }
      .stTabs [aria-selected="true"] {
        color: var(--accent-dark) !important;
        border-bottom: 3px solid var(--accent-blue) !important;
        background: rgba(255, 255, 255, 0.5) !important;
        border-radius: 10px 10px 0 0 !important;
      }

      /* Cute Aesthetic Buttons */
      .stButton > button {
        background: linear-gradient(135deg, #7DD3FC 0%, #38BDF8 100%) !important;
        color: #FFFFFF !important;
        font-family: 'Nunito', sans-serif !important;
        font-weight: 800 !important;
        font-size: 1.05rem !important;
        border: 2px solid #FFFFFF !important;
        border-radius: 16px !important;
        box-shadow: 0 6px 15px rgba(14, 165, 233, 0.25) !important;
        letter-spacing: 1px;
        transition: all 0.3s ease !important;
      }
      .stButton > button:hover {
        transform: translateY(-4px) !important;
        box-shadow: 0 10px 20px rgba(14, 165, 233, 0.4) !important;
        background: linear-gradient(135deg, #38BDF8 0%, #0EA5E9 100%) !important;
      }

      /* Input Fields */
      .stTextArea textarea, .stTextInput input {
        background: #FFFFFF !important;
        border: 2px solid var(--accent-light) !important;
        color: var(--text-main) !important;
        border-radius: 16px !important;
        font-family: 'JetBrains Mono', monospace !important;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.02) !important;
      }
      .stTextArea textarea:focus, .stTextInput input:focus {
        border-color: var(--accent-blue) !important;
        box-shadow: 0 0 0 4px rgba(14, 165, 233, 0.15) !important;
      }

      /* Data / Mono Values */
      .mono-val {
        color: var(--accent-dark);
        background: #FFFFFF;
        border: 1px solid var(--accent-light);
        border-radius: 10px;
        padding: 0.3rem 0.8rem;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.85rem;
        font-weight: 700;
        word-break: break-all;
        display: inline-block;
        box-shadow: 0 2px 5px rgba(14, 165, 233, 0.05);
      }

      /* Cute Badges */
      .step-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.6rem;
        background: #FFFFFF;
        border: 2px solid var(--accent-light);
        color: var(--accent-dark);
        padding: 0.5rem 1.2rem;
        border-radius: 99px;
        font-family: 'Nunito', sans-serif;
        font-size: 0.95rem;
        font-weight: 800;
        margin-bottom: 1.2rem;
        box-shadow: 0 4px 10px rgba(14, 165, 233, 0.08);
      }

      /* Equations */
      .eq-row {
        padding: 0.6rem 0;
        border-bottom: 2px dotted var(--accent-light);
        font-size: 0.9rem;
        font-family: 'JetBrains Mono', monospace;
        display: flex;
        align-items: center;
        gap: 0.6rem;
      }
      .eq-label { color: var(--text-muted); min-width: 140px; font-weight: 700; font-family: 'Nunito', sans-serif; }
      .eq-op { color: var(--accent-light); font-weight: bold; }
      .eq-val { color: var(--accent-blue); }
      .eq-result { color: var(--accent-dark); font-weight: 800; }

      /* Metrics (Dashboard Numbers) */
      [data-testid="stMetricValue"] {
        color: var(--accent-blue) !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 1.3rem !important;
        font-weight: 800 !important;
      }
      [data-testid="stMetricLabel"] {
        color: var(--text-muted) !important;
        font-family: 'Nunito', sans-serif !important;
        font-weight: 700 !important;
        letter-spacing: 0.5px;
      }

      /* FULL BLUE Banners (Valid/Invalid) */
      .banner-valid {
        background: linear-gradient(to right, #F0F9FF, #E0F2FE);
        border: 2px solid #38BDF8;
        border-radius: 16px;
        box-shadow: 0 6px 15px rgba(56, 189, 248, 0.2);
        padding: 1.2rem;
        text-align: center;
        color: #0284C7;
        font-family: 'Nunito', sans-serif;
        font-weight: 800;
        font-size: 1.1rem;
        margin-top: 1rem;
      }
      .banner-invalid {
        background: linear-gradient(to right, #E0F2FE, #BAE6FD);
        border: 2px solid #0284C7;
        border-radius: 16px;
        box-shadow: 0 6px 15px rgba(2, 132, 199, 0.2);
        padding: 1.2rem;
        text-align: center;
        color: #082F49;
        font-family: 'Nunito', sans-serif;
        font-weight: 800;
        font-size: 1.1rem;
        margin-top: 1rem;
      }
    </style>
    """, unsafe_allow_html=True)

def truncate_display(n, max_len: int = 40) -> str:
    s = str(n)
    if len(s) > max_len:
        return s[:18] + " … " + s[-10:]
    return s

def step_badge(number: int, label: str):
    icons = ["☁️", "💧", "🦋"]
    st.markdown(f'<div class="step-badge">{icons[number-1]} &nbsp; {label}</div>', unsafe_allow_html=True)

def mono(val, label: str = ""):
    if label:
        st.markdown(f'<div class="eq-row"><span class="eq-label">{label}</span><span class="mono-val">{truncate_display(val) if isinstance(val, int) else val}</span></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<span class="mono-val">{truncate_display(val) if isinstance(val, int) else val}</span>', unsafe_allow_html=True)

def eq_row(label: str, formula: str, result):
    result_str = truncate_display(result) if isinstance(result, int) else str(result)
    st.markdown(
        f'<div class="eq-row">'
        f'  <span class="eq-label">{label}</span><span class="eq-op">✨</span>'
        f'  <span class="eq-val">{formula}</span><span class="eq-op">➜</span>'
        f'  <span class="eq-result">{result_str}</span>'
        f'</div>', unsafe_allow_html=True)

def show_valid(valid: bool): 
    if valid:
        st.markdown('<div class="banner-valid">🦋 Tanda Tangan VALID 🦋</div>', unsafe_allow_html=True)
        st.info("Sistem memverifikasi integritas data. Pesan aman dan tidak diubah.", icon="☁️")
    else:
        st.markdown('<div class="banner-invalid">🧊 Tanda Tangan INVALID 🧊</div>', unsafe_allow_html=True)
        st.warning("Terdeteksi anomali. Tanda tangan digital tidak cocok dengan pesan.", icon="💧")

# ── FUNGSI GLOBAL PEMBUAT TABEL EEA ──
def get_eea_html(m_val, a_val, label_m="φ(n)", label_a="d"):
    q_list, r_list, t_list = [label_m, label_a], [m_val, a_val], [0, 1]
    while True:
        quot, rem = r_list[-2] // r_list[-1], r_list[-2] % r_list[-1]
        q_list.append(str(quot)); r_list.append(rem)
        if rem == 0:
            t_list.append(""); break
        t_list.append(t_list[-2] - quot * t_list[-1])
        
    last_t = t_list[-2] 
    html = '<div style="overflow-x: auto; margin-top: 1rem; margin-bottom: 1.5rem;"><table style="width: 100%; border-collapse: collapse; text-align: center; font-family: \'JetBrains Mono\', monospace; font-size: 0.85rem; border: 2px solid #BAE6FD; background-color: #FFFFFF;">'
    html += '<tr style="background-color: #F0F9FF;"><th style="padding: 0.6rem; border: 1px solid #BAE6FD; color: #0284C7;">q</th>' + "".join([f'<td style="padding: 0.6rem; border: 1px solid #BAE6FD; color: #082F49;">{q}</td>' for q in q_list]) + '</tr>'
    html += '<tr><th style="padding: 0.6rem; border: 1px solid #BAE6FD; color: #0284C7;">r</th>' + "".join([f'<td style="padding: 0.6rem; border: 1px solid #BAE6FD; color: #0EA5E9; font-weight: bold;">{r}</td>' for r in r_list]) + '</tr>'
    html += '<tr style="background-color: #F0F9FF;"><th style="padding: 0.6rem; border: 1px solid #BAE6FD; color: #0284C7;">t</th>' + "".join([f'<td style="padding: 0.6rem; border: 1px solid #BAE6FD; color: #082F49;">{t}</td>' for t in t_list]) + '</tr></table></div>'
    return html, last_t
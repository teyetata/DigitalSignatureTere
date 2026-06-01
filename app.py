import streamlit as st
import time

# Import modul yang sudah kita pisahkan
from crypto_core import *
from ui_components import *

st.set_page_config(page_title="Digital Signature", page_icon="🔐", layout="wide")
apply_custom_css()

# ==========================================
# FUNGSI RENDER TAMPILAN ALGORITMA
# ==========================================
def render_rsa(message: str, mode: str, p_val: int, q_val: int, d_val: int, hash_algo: str):
    # ── FITUR BARU: GENERATOR TABEL EEA & PENANGKAP NILAI T ──
    def get_eea_html(phi, d):
        q_list = ["φ(n)", "d"]
        r_list = [phi, d]
        t_list = [0, 1]

        # Looping perhitungan EEA
        while True:
            quot = r_list[-2] // r_list[-1]
            rem = r_list[-2] % r_list[-1]
            
            q_list.append(str(quot))
            r_list.append(rem)
            
            if rem == 0:
                t_list.append("") # Kosongkan nilai t jika r sudah 0
                break
            
            t_val = t_list[-2] - quot * t_list[-1]
            t_list.append(t_val)
            
        # Ambil nilai t terakhir sebelum r menjadi 0
        last_t = t_list[-2] 
            
        # Merakit HTML agar matching dengan tema biru
        html = '<div style="overflow-x: auto; margin-top: 1rem; margin-bottom: 1.5rem;">'
        html += '<table style="width: 100%; border-collapse: collapse; text-align: center; font-family: \'JetBrains Mono\', monospace; font-size: 0.85rem; border: 2px solid #BAE6FD; background-color: #FFFFFF;">'
        
        # Baris Q (Quotient)
        html += '<tr style="background-color: #F0F9FF;"><th style="padding: 0.6rem; border: 1px solid #BAE6FD; color: #0284C7;">q</th>'
        for q in q_list:
            html += f'<td style="padding: 0.6rem; border: 1px solid #BAE6FD; color: #082F49;">{q}</td>'
        html += '</tr>'
        
        # Baris R (Remainder)
        html += '<tr><th style="padding: 0.6rem; border: 1px solid #BAE6FD; color: #0284C7;">r</th>'
        for r in r_list:
            html += f'<td style="padding: 0.6rem; border: 1px solid #BAE6FD; color: #0EA5E9; font-weight: bold;">{r}</td>'
        html += '</tr>'
        
        # Baris T (Nilai Invers Sementara)
        html += '<tr style="background-color: #F0F9FF;"><th style="padding: 0.6rem; border: 1px solid #BAE6FD; color: #0284C7;">t</th>'
        for t in t_list:
            html += f'<td style="padding: 0.6rem; border: 1px solid #BAE6FD; color: #082F49;">{t}</td>'
        html += '</tr>'
        
        html += '</table></div>'
        
        # Kembalikan tabel HTML dan nilai t terakhir
        return html, last_t

    keys = {}
    if mode == "✨ Generate Otomatis":
        with st.spinner("⚙️  Membangkitkan kunci RSA…"): 
            keys = rsa_keygen()
    else:
        # Validasi Prima Gabungan
        p_is_prime = is_prime_miller_rabin(p_val)
        q_is_prime = is_prime_miller_rabin(q_val)
        
        if not p_is_prime and not q_is_prime:
            st.error(f"❌ Oops! Nilai p ({p_val}) dan q ({q_val}) BUKAN bilangan prima. Silakan ganti dengan angka prima.", icon="❌")
            st.stop()
        elif not p_is_prime:
            st.error(f"❌ Oops! Nilai p ({p_val}) BUKAN bilangan prima. Silakan ganti dengan angka prima.", icon="❌")
            st.stop()
        elif not q_is_prime:
            st.error(f"❌ Oops! Nilai q ({q_val}) BUKAN bilangan prima. Silakan ganti dengan angka prima.", icon="❌")
            st.stop()
            
        if p_val == q_val:
            st.error("❌ Oops! Nilai p dan q tidak boleh sama agar RSA aman.", icon="❌")
            st.stop()

        n = p_val * q_val
        phi = (p_val - 1) * (q_val - 1)

        if gcd(d_val, phi) != 1:
            st.error(f"❌ Oops! Nilai d ({d_val}) TIDAK relatif prima dengan φ(n) = {phi}. FPB-nya adalah {gcd(d_val, phi)}, seharusnya 1.", icon="❌")
            st.stop()

        try:
            e_val = mod_inverse(d_val, phi)
            keys = {"p": p_val, "q": q_val, "n": n, "phi": phi, "d": d_val, "e": e_val}
        except Exception as exc:
            st.error(f"❌ Terjadi kesalahan perhitungan: {exc}", icon="❌")
            st.stop()

    with st.spinner(f"✍️  Menandatangani pesan dengan {hash_algo}…"): sig = rsa_sign(message, keys, hash_algo)
    with st.spinner("🔍  Memverifikasi tanda tangan…"): ver = rsa_verify(message, sig, keys, hash_algo)

    tab1, tab2, tab3 = st.tabs(["🔑  KEY GENERATION", "✍️  SIGNING", "🔍  VERIFICATION"])
    
    with tab1:
        step_badge(1, "KEY GENERATION RSA")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### Parameter Prima")
            st.metric("p (prima 1)", f"{keys['p']:,}")
            st.metric("q (prima 2)", f"{keys['q']:,}")
            st.metric("n = p × q", f"{keys['n']:,}")
        with col2:
            st.markdown("#### Kunci")
            st.metric("φ(n) = (p-1)(q-1)", truncate_display(keys['phi']))
            st.metric("d — Kunci Privat", truncate_display(keys['d']))
            st.metric("e — Kunci Publik", truncate_display(keys['e']))
            
        st.divider()
        st.markdown("#### Proses Perhitungan Kunci")
        eq_row("n", "p × q", keys['n'])
        eq_row("φ(n)", "(p−1) × (q−1)", keys['phi'])
        eq_row("d", "input user / acak", keys['d'])
        eq_row("e", "d⁻¹ mod φ(n)", keys['e'])
        
        # ── TABEL EEA & DETAIL PERHITUNGAN E DITAMPILKAN DI SINI ──
        st.markdown("#### Detail Pencarian e (Extended Euclidean Algorithm)")
        eea_html, last_t = get_eea_html(keys['phi'], keys['d'])
        st.markdown(eea_html, unsafe_allow_html=True)
        
        # Tambahan Detail Penjabaran Perhitungan e dari t
        if last_t < 0:
            eq_row("e", "t + φ(n)", f"{last_t} + {keys['phi']}")
            eq_row("e", "Hasil Akhir", keys['e'])
        else:
            eq_row("e", "t mod φ(n)", f"{last_t} mod {keys['phi']}")
            eq_row("e", "Hasil Akhir", keys['e'])
            
        st.write("") # Spasi tambahan agar rapi
        st.info("💡 Nilai **e** diambil dari nilai **t** terakhir sebelum sisa bagi (r) menjadi 0. Jika nilai t negatif, maka e = t + φ(n).")

    with tab2:
        step_badge(2, "SIGNING RSA")
        st.markdown(f"#### Hash Pesan ({hash_algo})")
        # ── FITUR BARU: HASH HEX & DEC ──
        mono(sig['hash_hex'], f"{hash_algo}(M) hex")
        mono(int(sig['hash_hex'], 16), f"{hash_algo}(M) dec")
        st.divider()
        eq_row("H(M) mod n", "hash mod n", sig['hash_mod'])
        eq_row("S", "H(M)ᵈ mod n", sig['S'])
        col1, col2 = st.columns(2)
        with col1: st.metric("Kunci Privat d", truncate_display(keys['d']))
        with col2: st.metric("Tanda Tangan S", truncate_display(sig['S']))

    with tab3:
        step_badge(3, "VERIFICATION RSA")
        eq_row("H₁(M)", f"{hash_algo}(M) mod n", sig['hash_mod'])
        eq_row("H₂", "Sᵉ mod n", ver['h2'])
        st.divider()
        show_valid(ver['valid'])

# ── RENDER EL GAMAL ──
def render_elgamal(message: str, mode: str, p_val: int, g_val: int, x_val: int, k_val: int, hash_algo: str):
    keys = {}
    if mode == "✨ Generate Otomatis":
        with st.spinner("⚙️  Membangkitkan kunci El Gamal…"): 
            keys = elgamal_keygen()
    else:
        if not is_prime_miller_rabin(p_val):
            st.error(f"❌ Oops! Nilai p ({p_val}) BUKAN bilangan prima.", icon="❌")
            st.stop()
        if not (1 < g_val < p_val):
            st.error(f"❌ Oops! Nilai g ({g_val}) tidak valid.", icon="❌")
            st.stop()
        if not (1 < x_val < p_val - 1):
            st.error(f"❌ Oops! Nilai x ({x_val}) tidak valid.", icon="❌")
            st.stop()
        try:
            keys = {"p": p_val, "g": g_val, "x": x_val, "y": pow(g_val, x_val, p_val)}
        except Exception as exc:
            st.error(f"❌ Terjadi kesalahan: {exc}", icon="❌")
            st.stop()

    k_final = None
    if mode == "✍️ Input Manual (p, g, x, k)":
        p1 = keys['p'] - 1
        if not (1 < k_val < p1):
            st.error(f"❌ Oops! Nilai k ({k_val}) tidak valid.", icon="❌")
            st.stop()
        if gcd(k_val, p1) != 1:
            st.error(f"❌ Oops! Nilai k ({k_val}) TIDAK relatif prima dengan p-1 ({p1}).", icon="❌")
            st.stop()
        k_final = k_val

    with st.spinner(f"✍️  Menandatangani pesan dengan {hash_algo}…"): sig = elgamal_sign(message, keys, hash_algo, k_val=k_final)
    with st.spinner("🔍  Memverifikasi tanda tangan…"): ver = elgamal_verify(message, sig, keys, hash_algo)

    tab1, tab2, tab3 = st.tabs(["🔑  KEY GENERATION", "✍️  SIGNING", "🔍  VERIFICATION"])
    with tab1:
        step_badge(1, "KEY GENERATION El Gamal")
        col1, col2, col3 = st.columns(3)
        with col1: st.metric("p (prima)", f"{keys['p']:,}")
        with col2: st.metric("g (generator)", keys['g'])
        with col3: st.metric("x (Kunci Privat)", truncate_display(keys['x']))
        st.divider()
        st.metric("y = gˣ mod p (Kunci Publik)", truncate_display(keys['y']))

    with tab2:
        step_badge(2, "SIGNING El Gamal")
        st.markdown(f"#### Hash Pesan ({hash_algo})")
        mono(sig['hash_hex'], f"{hash_algo}(M) hex")
        mono(int(sig['hash_hex'], 16), f"{hash_algo}(M) dec")
        
        st.divider()
        st.markdown("#### Detail Pencarian Nilai b")
        
        # Penjabaran Langkah-langkah penyelesaian b seperti gambar
        p1 = keys['p'] - 1
        xa = keys['x'] * sig['a']
        xa_mod = xa % p1
        diff = (sig['M'] - xa_mod) % p1
        
        st.markdown("Selesaikan persamaan `M = x·a + k·b (mod p-1)` untuk menghitung nilai b:")
        st.markdown(f"**`{sig['M']} = ({keys['x']} * {sig['a']}) + ({sig['k']} * b) mod ({keys['p']}-1)`**")
        st.markdown(f"**`{sig['M']} = {xa_mod} + {sig['k']}b mod {p1}`**")
        st.markdown(f"**`{sig['k']}b = {sig['M']} - {xa_mod} mod {p1}`**")
        st.markdown(f"**`{sig['k']}b = {diff} mod {p1}`**")
        st.markdown(f"**`b = {diff} * {sig['k']}⁻¹ mod {p1}`**")
        st.markdown(f"**`b = {diff} * {sig['k_inv']} mod {p1}`**")
        st.markdown(f"**`b = {sig['b']}`**")
        
        st.divider()
        st.markdown(f"#### Perhitungan Invers {sig['k']}⁻¹ atau invers {sig['k']} mod {p1} (EEA)")
        # ── Memanggil tabel EEA untuk El Gamal ──
        eea_html, last_t = get_eea_html(p1, sig['k'], "p-1", "k")
        st.markdown(eea_html, unsafe_allow_html=True)
        
        if last_t < 0:
            eq_row(f"{sig['k']}⁻¹", f"t + (p-1)", f"{last_t} + {p1}")
            eq_row(f"{sig['k']}⁻¹", "Hasil Akhir", sig['k_inv'])
        else:
            eq_row(f"{sig['k']}⁻¹", f"t mod (p-1)", f"{last_t} mod {p1}")
            eq_row(f"{sig['k']}⁻¹", "Hasil Akhir", sig['k_inv'])
            
        st.info(f"💡 Dengan EEA didapat nilai **{sig['k']}⁻¹ = {sig['k_inv']}**")

    with tab3:
        step_badge(3, "VERIFICATION El Gamal")
        eq_row("LHS", "g^M mod p", ver['lhs'])
        eq_row("RHS", "yᵃ × aᵇ mod p", ver['rhs'])
        st.divider()
        show_valid(ver['valid'])

# ── RENDER SCHNORR ──
def render_schnorr(message: str, mode: str, p_val: int, q_val: int, g_val: int, x_val: int, k_val: int, hash_algo: str):
    keys = {}
    if mode == "✨ Generate Otomatis":
        with st.spinner("⚙️  Membangkitkan kunci Schnorr…"): keys = schnorr_keygen()
    else:
        if not is_prime_miller_rabin(p_val): st.error(f"❌ Oops! Nilai p ({p_val}) BUKAN bilangan prima.", icon="❌"); st.stop()
        if not is_prime_miller_rabin(q_val): st.error(f"❌ Oops! Nilai q ({q_val}) BUKAN bilangan prima.", icon="❌"); st.stop()
        if (p_val - 1) % q_val != 0: st.error(f"❌ Oops! Nilai q ({q_val}) bukan merupakan faktor pembagi dari p-1.", icon="❌"); st.stop()
        if pow(g_val, q_val, p_val) != 1: st.error(f"❌ Oops! Syarat g^q mod p = 1 tidak terpenuhi untuk g={g_val}.", icon="❌"); st.stop()
        if not (0 < x_val < q_val): st.error(f"❌ Oops! Nilai x harus berada di rentang 0 < x < q.", icon="❌"); st.stop()
        try:
            g_inv = mod_inverse(g_val, p_val)
            keys = {"p": p_val, "q": q_val, "g": g_val, "x": x_val, "y": pow(g_inv, x_val, p_val), "g_inv": g_inv}
        except Exception as exc: st.error(f"❌ Error Perhitungan: {exc}", icon="❌"); st.stop()

    k_final = None
    if mode == "✍️ Input Manual (p, q, g, x, k)":
        if not (0 < k_val < keys['q']): st.error(f"❌ Oops! Nilai k ({k_val}) harus berada di rentang 0 < k < q.", icon="❌"); st.stop()
        k_final = k_val

    with st.spinner(f"✍️  Menandatangani pesan dengan {hash_algo}…"): sig = schnorr_sign(message, keys, hash_algo, k_val=k_final)
    with st.spinner("🔍  Memverifikasi tanda tangan…"): ver = schnorr_verify(message, sig, keys, hash_algo)

    tab1, tab2, tab3 = st.tabs(["🔑  KEY GENERATION", "✍️  SIGNING", "🔍  VERIFICATION"])
    with tab1:
        step_badge(1, "KEY GENERATION Schnorr")
        col1, col2, col3 = st.columns(3)
        with col1: st.metric("p (prima besar)", f"{keys['p']:,}")
        with col2: st.metric("q (prima kecil)", f"{keys['q']:,}")
        with col3: st.metric("g (generator)", keys['g'])
        st.divider()
        col4, col5 = st.columns(2)
        with col4: st.metric("x (Kunci Privat)", truncate_display(keys['x']))
        with col5: st.metric("y (Kunci Publik)", truncate_display(keys['y']))
        
        # ── TABEL EEA UNTUK PENCARIAN INVERS G ──
        st.divider()
        st.markdown("#### Proses Perhitungan Kunci y = g⁻ˣ mod p")
        st.markdown(f"Selesaikan perhitungan invers dari g mod p terlebih dahulu, lalu pangkatkan dengan x.")
        st.markdown(f"**1. Perhitungan g⁻¹ atau invers {keys['g']} mod {keys['p']} (EEA)**")
        eea_html, last_t = get_eea_html(keys['p'], keys['g'], "p", "g")
        st.markdown(eea_html, unsafe_allow_html=True)
        
        if last_t < 0: eq_row("g⁻¹", "t + p", f"{last_t} + {keys['p']}"); eq_row("g⁻¹", "Hasil Akhir", keys['g_inv'])
        else: eq_row("g⁻¹", "t mod p", f"{last_t} mod {keys['p']}"); eq_row("g⁻¹", "Hasil Akhir", keys['g_inv'])
        
        st.markdown(f"<br>**2. Perhitungan y = (g⁻¹)ˣ mod p**", unsafe_allow_html=True)
        st.markdown(f"**`y = {keys['g_inv']}^{keys['x']} mod {keys['p']}`**")
        eq_row(" y", "Hasil Akhir Kunci Publik", keys['y'])

    with tab2:
        step_badge(2, "SIGNING Schnorr")
        st.markdown("#### 1. Pembentukan Nilai r (Nilai Acak)")
        eq_row("k", "input user / acak", sig['k'])
        eq_row("r", "gᵏ mod p", sig['r'])
        st.divider()
        st.markdown(f"#### 2. Hash Pesan yang Digabung ({hash_algo})")
        mono(f"{message}{sig['r']}", "Pesan digabung r (M ‖ r)")
        mono(sig['hash_hex'], f"{hash_algo}(M ‖ r) hex")
        mono(int(sig['hash_hex'], 16), f"{hash_algo}(M ‖ r) dec")
        st.divider()
        st.markdown("#### 3. Perhitungan Tanda Tangan (e, s)")
        eq_row("e", f"H(M ‖ r) mod q", sig['e'])
        eq_row("s", "(k + x·e) mod q", sig['s'])

    with tab3:
        step_badge(3, "VERIFICATION Schnorr")
        eq_row("rᵥ", "(gˢ × yᵉ) mod p", ver['rv'])
        eq_row("eᵥ", f"H(M ‖ rᵥ) mod q", ver['ev'])
        st.divider()
        show_valid(ver['valid'])

# ── RENDER DSA (Menerima Input Manual) ──
def render_dsa(message: str, mode: str, p_val: int, q_val: int, g_val: int, x_val: int, k_val: int, hash_algo: str):
    keys = {}
    if mode == "✨ Generate Otomatis":
        with st.spinner("⚙️  Membangkitkan kunci DSA…"): keys = dsa_keygen()
    else:
        if not is_prime_miller_rabin(p_val): st.error(f"❌ Oops! Nilai p ({p_val}) BUKAN bilangan prima.", icon="❌"); st.stop()
        if not is_prime_miller_rabin(q_val): st.error(f"❌ Oops! Nilai q ({q_val}) BUKAN bilangan prima.", icon="❌"); st.stop()
        if (p_val - 1) % q_val != 0: st.error(f"❌ Oops! Nilai q ({q_val}) bukan merupakan faktor pembagi dari p-1.", icon="❌"); st.stop()
        if pow(g_val, q_val, p_val) != 1: st.error(f"❌ Oops! Syarat g^q mod p = 1 tidak terpenuhi untuk g={g_val}.", icon="❌"); st.stop()
        if not (0 < x_val < q_val): st.error(f"❌ Oops! Nilai x harus berada di rentang 0 < x < q.", icon="❌"); st.stop()
        try:
            keys = {"p": p_val, "q": q_val, "g": g_val, "x": x_val, "y": pow(g_val, x_val, p_val)}
        except Exception as exc: st.error(f"❌ Error Perhitungan: {exc}", icon="❌"); st.stop()

    k_final = None
    if mode == "✍️ Input Manual (p, q, g, x, k)":
        if not (0 < k_val < keys['q']): st.error(f"❌ Oops! Nilai k ({k_val}) harus berada di rentang 0 < k < q.", icon="❌"); st.stop()
        k_final = k_val

    with st.spinner(f"✍️  Menandatangani pesan dengan {hash_algo}…"): 
        try:
            sig = dsa_sign(message, keys, hash_algo, k_val=k_final)
        except Exception as exc:
            st.error(f"❌ Terjadi kesalahan saat menandatangani: {exc}", icon="❌")
            st.stop()
            
    with st.spinner("🔍  Memverifikasi tanda tangan…"): 
        ver = dsa_verify(message, sig, keys, hash_algo)

    tab1, tab2, tab3 = st.tabs(["🔑  KEY GENERATION", "✍️  SIGNING", "🔍  VERIFICATION"])
    with tab1:
        step_badge(1, "KEY GENERATION DSA")
        col1, col2, col3 = st.columns(3)
        with col1: st.metric("p (prima besar)", f"{keys['p']:,}")
        with col2: st.metric("q (prima kecil)", f"{keys['q']:,}")
        with col3: st.metric("g (generator)", keys['g'])
        st.divider()
        col4, col5 = st.columns(2)
        with col4: st.metric("x (Kunci Privat)", truncate_display(keys['x']))
        with col5: st.metric("y (Kunci Publik)", truncate_display(keys['y']))
        st.markdown("#### Proses Perhitungan Kunci")
        eq_row("y", "gˣ mod p", keys['y'])

    with tab2:
        step_badge(2, "SIGNING DSA")
        st.markdown(f"#### 1. Hash Pesan ({hash_algo})")
        mono(sig['hash_hex'], f"{hash_algo}(M) hex")
        mono(int(sig['hash_hex'], 16), f"{hash_algo}(M) dec")
        eq_row("H_M", f"Hash mod q", sig['H_M'])
        st.divider()
        
        st.markdown("#### 2. Pembentukan Nilai r")
        eq_row("k", "input user / acak", sig['k'])
        eq_row("r", "(gᵏ mod p) mod q", sig['r'])
        st.divider()
        
        st.markdown("#### 3. Detail Pencarian Nilai s")
        xr = (keys['x'] * sig['r'])
        xr_mod = xr % keys['q']
        h_plus_xr = (sig['H_M'] + xr_mod) % keys['q']
        
        st.markdown("Selesaikan persamaan `s = k⁻¹ * (H(M) + x·r) mod q`:")
        st.markdown(f"**`s = k⁻¹ * ({sig['H_M']} + ({keys['x']} * {sig['r']})) mod {keys['q']}`**")
        st.markdown(f"**`s = k⁻¹ * ({sig['H_M']} + {xr_mod}) mod {keys['q']}`**")
        st.markdown(f"**`s = {sig['k_inv']} * {h_plus_xr} mod {keys['q']}`**")
        st.markdown(f"**`s = {sig['s']}`**")
        
        st.divider()
        st.markdown(f"#### Perhitungan Invers k⁻¹ atau invers {sig['k']} mod {keys['q']} (EEA)")
        eea_html, last_t = get_eea_html(keys['q'], sig['k'], "q", "k")
        st.markdown(eea_html, unsafe_allow_html=True)
        
        if last_t < 0: eq_row("k⁻¹", f"t + q", f"{last_t} + {keys['q']}"); eq_row("k⁻¹", "Hasil Akhir", sig['k_inv'])
        else: eq_row("k⁻¹", f"t mod q", f"{last_t} mod {keys['q']}"); eq_row("k⁻¹", "Hasil Akhir", sig['k_inv'])

    with tab3:
        step_badge(3, "VERIFICATION DSA")
        st.markdown("#### Perhitungan Sisi Penerima")
        
        # ── PENAMBAHAN TABEL EEA UNTUK NILAI w ──
        st.markdown(f"#### 1. Perhitungan w = s⁻¹ atau invers {sig['s']} mod {keys['q']} (EEA)")
        eea_html_w, last_t_w = get_eea_html(keys['q'], sig['s'], "q", "s")
        st.markdown(eea_html_w, unsafe_allow_html=True)
        
        if last_t_w < 0: 
            eq_row("w", f"t + q", f"{last_t_w} + {keys['q']}")
            eq_row("w", "Hasil Akhir", ver['w'])
        else: 
            eq_row("w", f"t mod q", f"{last_t_w} mod {keys['q']}")
            eq_row("w", "Hasil Akhir", ver['w'])
            
        st.divider()
        st.markdown("#### 2. Perhitungan u1, u2, dan v")
        eq_row("u1", "(H_M × w) mod q", ver['u1'])
        eq_row("u2", "(r × w) mod q", ver['u2'])
        eq_row("v", "((g^u1 × y^u2) mod p) mod q", ver['v'])
        st.divider()
        show_valid(ver['valid'])

# ==========================================
# PENGATURAN HALAMAN & SIDEBAR
# ==========================================
ALGO_INFO = {
    "🔐 RSA": {"desc": "Rivest–Shamir–Adleman", "params": "p, q prima 6–7 digit", "sign": "S = H(M)ᵈ mod n", "verify": "H(M) == Sᵉ mod n"},
    "🔒 El Gamal": {"desc": "El Gamal Signature", "params": "p prima 6–7 digit", "sign": "(a, b)", "verify": "gᴹ ≡ yᵃaᵇ (mod p)"},
    "🛡️ Schnorr": {"desc": "Schnorr (32-bit)", "params": "p 32-bit", "sign": "(e, s)", "verify": "eᵥ == e"},
    "🏛️ DSA": {"desc": "Digital Signature Algorithm", "params": "p, q prima, g", "sign": "(r, s)", "verify": "v == r"},
}

with st.sidebar:
    st.markdown("## 🔐 Digital Signature Tugas 2")
    st.markdown('<p style="color:#64748b;font-size:0.72rem;">IFB · Teresia Hana Agatha Siburian</p>', unsafe_allow_html=True)
    algo = st.radio("", list(ALGO_INFO.keys()), label_visibility="collapsed")
    
    info = ALGO_INFO[algo]
    st.markdown(f"""<div class="algo-info">
      <strong>{info['desc']}</strong><br><br>
      <span>📌 Parameter:</span><br>{info['params']}<br><br>
      <span>✍️ TTD:</span> {info['sign']}<br>
      <span>🔍 Verify:</span> {info['verify']}
    </div>""", unsafe_allow_html=True)

algo_name = algo.split(" ", 1)[1]
st.markdown(f"# {algo} Digital Signature")
st.divider()

st.markdown("### 📝 Pesan yang Akan Ditandatangani")
message = st.text_area("Ketik pesan Anda di sini:", height=120, label_visibility="collapsed")

# ── BLOK INPUT MANUAL ──
rsa_mode = "✨ Generate Otomatis"
p_val, q_val, d_val = 1000003, 1000033, 65537

elg_mode = "✨ Generate Otomatis"
p_val_elg, g_val_elg, x_val_elg, k_val_elg = 1000003, 33, 12345, 54321

sch_mode = "✨ Generate Otomatis"
p_val_sch, q_val_sch, g_val_sch, x_val_sch, k_val_sch = 2267, 103, 354, 30, 45

dsa_mode = "✨ Generate Otomatis"
p_val_dsa, q_val_dsa, g_val_dsa, x_val_dsa, k_val_dsa = 2267, 103, 354, 30, 45

if algo_name == "RSA":
    st.markdown("### ⚙️ Pengaturan Kunci RSA")
    rsa_mode = st.radio(
        "Pilih Metode Pembentukan Kunci:", 
        ["✨ Generate Otomatis", "✍️ Input Manual (p, q, d)"], 
        horizontal=True
    )
    if rsa_mode == "✍️ Input Manual (p, q, d)":
        st.info("💡 Pastikan p dan q adalah bilangan prima, dan d relatif prima dengan φ(n).")
        col1, col2, col3 = st.columns(3)
        with col1: p_val = st.number_input("Nilai p (Prima 1)", min_value=2, value=1000003, step=1)
        with col2: q_val = st.number_input("Nilai q (Prima 2)", min_value=2, value=1000033, step=1)
        with col3: d_val = st.number_input("Nilai d (Kunci Privat)", min_value=2, value=65537, step=1)

# elif algo_name == "El Gamal":
#     st.markdown("### ⚙️ Pengaturan Kunci El Gamal")
#     elg_mode = st.radio(
#         "Pilih Metode Pembentukan Kunci:", 
#         ["✨ Generate Otomatis", "✍️ Input Manual (p, x)"], 
#         horizontal=True
#     )
#     if elg_mode == "✍️ Input Manual (p, x)":
#         st.info("💡 Pastikan p adalah bilangan prima, dan 1 < x < p-1.")
#         col1, col2 = st.columns(2)
#         with col1: p_val_elg = st.number_input("Nilai p (Prima)", min_value=2, value=1000003, step=1)
#         with col2: x_val_elg = st.number_input("Nilai x (Kunci Privat)", min_value=2, value=12345, step=1)

# ── BLOK INPUT MANUAL EL GAMAL (Nilai k ditambahkan) ──
elif algo_name == "El Gamal":
    st.markdown("### ⚙️ Pengaturan Kunci El Gamal")
    elg_mode = st.radio("Pilih Metode Pembentukan Kunci:", ["✨ Generate Otomatis", "✍️ Input Manual (p, g, x, k)"], horizontal=True)
    if elg_mode == "✍️ Input Manual (p, g, x, k)":
        st.info("💡 Pastikan p prima, g < p, x < p-1, dan k relatif prima dengan p-1.")
        col1, col2 = st.columns(2)
        with col1: p_val_elg = st.number_input("Nilai p (Prima)", min_value=3, value=2357, step=1)
        with col2: g_val_elg = st.number_input("Nilai g (Generator)", min_value=2, value=33, step=1)
        col3, col4 = st.columns(2)
        with col3: x_val_elg = st.number_input("Nilai x (Kunci Privat)", min_value=2, value=1751, step=1)
        with col4: k_val_elg = st.number_input("Nilai k (Kunci Acak)", min_value=2, value=1520, step=1)

# ── BLOK INPUT MANUAL SCHNORR ──
elif algo_name == "Schnorr":
    st.markdown("### ⚙️ Pengaturan Kunci Schnorr")
    sch_mode = st.radio("Pilih Metode Pembentukan Kunci:", ["✨ Generate Otomatis", "✍️ Input Manual (p, q, g, x, k)"], horizontal=True)
    if sch_mode == "✍️ Input Manual (p, q, g, x, k)":
        st.info("💡 Pastikan p dan q prima, q faktor pembagi p-1, g^q mod p = 1, x < q, dan k < q.")
        col1, col2, col3 = st.columns(3)
        with col1: p_val_sch = st.number_input("Nilai p (Prima Besar)", min_value=3, value=2267, step=1)
        with col2: q_val_sch = st.number_input("Nilai q (Prima Kecil)", min_value=2, value=103, step=1)
        with col3: g_val_sch = st.number_input("Nilai g (Generator)", min_value=2, value=354, step=1)
        col4, col5 = st.columns(2)
        with col4: x_val_sch = st.number_input("Nilai x (Kunci Privat)", min_value=1, value=30, step=1)
        with col5: k_val_sch = st.number_input("Nilai k (Kunci Acak)", min_value=1, value=45, step=1)

# ── BLOK INPUT MANUAL DSA ──
elif algo_name == "DSA":
    st.markdown("### ⚙️ Pengaturan Kunci DSA")
    dsa_mode = st.radio("Pilih Metode Pembentukan Kunci:", ["✨ Generate Otomatis", "✍️ Input Manual (p, q, g, x, k)"], horizontal=True)
    if dsa_mode == "✍️ Input Manual (p, q, g, x, k)":
        st.info("💡 Pastikan p dan q prima, q faktor pembagi p-1, g^q mod p = 1, x < q, dan k < q.")
        col1, col2, col3 = st.columns(3)
        with col1: p_val_dsa = st.number_input("Nilai p (Prima Besar)", min_value=3, value=2267, step=1)
        with col2: q_val_dsa = st.number_input("Nilai q (Prima Kecil)", min_value=2, value=103, step=1)
        with col3: g_val_dsa = st.number_input("Nilai g (Generator)", min_value=2, value=354, step=1)
        col4, col5 = st.columns(2)
        with col4: x_val_dsa = st.number_input("Nilai x (Kunci Privat)", min_value=1, value=30, step=1)
        with col5: k_val_dsa = st.number_input("Nilai k (Kunci Acak)", min_value=1, value=45, step=1)

st.write("") # Memberi sedikit jarak

# ── PENGATURAN HASH (BERLAKU UNTUK SEMUA) ──
st.markdown("### 🧩 Pengaturan Hash")
hash_algo = st.selectbox("Pilih Fungsi Hash untuk Pesan:", ["SHA-1", "SHA-256", "SHA-512", "MD5"], index=1)
st.write("") 

# ── TOMBOL EKSEKUSI ──
if st.button("⚡ GENERATE & VERIFY", use_container_width=True):
    if not message.strip():
        st.error("❌ Pesan tidak boleh kosong. Isi pesan terlebih dahulu.", icon="❌")
        st.stop()
    
    st.divider()
    t_start = time.time()
    
    # Memanggil fungsi sesuai algoritma yang dipilih dan parameter HASH
    if algo_name == "RSA": render_rsa(message, rsa_mode, p_val, q_val, d_val, hash_algo)
    elif algo_name == "El Gamal": render_elgamal(message, elg_mode, p_val_elg, g_val_elg, x_val_elg, k_val_elg, hash_algo)
    elif algo_name == "Schnorr": render_schnorr(message, sch_mode, p_val_sch, q_val_sch, g_val_sch, x_val_sch, k_val_sch, hash_algo)
    elif algo_name == "DSA": render_dsa(message, dsa_mode, p_val_dsa, q_val_dsa, g_val_dsa, x_val_dsa, k_val_dsa, hash_algo)
    
    st.caption(f"⏱️ Selesai dalam {(time.time() - t_start)*1000:.1f} ms")

##
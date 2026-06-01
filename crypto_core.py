import hashlib
import random

# ==========================================
# UTILITY FUNCTIONS — Matematika Dasar
# ==========================================
def gcd(a: int, b: int) -> int:
    while b:
        a, b = b, a % b
    return a

def mod_inverse(a: int, m: int) -> int:
    if gcd(a, m) != 1:
        raise ValueError(f"Modular inverse tidak ada: gcd({a}, {m}) ≠ 1")
    old_r, r = a, m
    old_s, s = 1, 0
    while r != 0:
        q = old_r // r
        old_r, r = r, old_r - q * r
        old_s, s = s, old_s - q * s
    return old_s % m

def is_prime_miller_rabin(n: int, k: int = 20) -> bool:
    if n < 2: return False
    if n in (2, 3): return True
    if n % 2 == 0: return False
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, d, n)
        if x in (1, n - 1): continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1: break
        else:
            return False
    return True

def generate_prime(bits: int = None, low: int = None, high: int = None) -> int:
    if bits is not None:
        low  = 2 ** (bits - 1)
        high = 2 ** bits - 1
    while True:
        candidate = random.randint(low, high)
        if candidate % 2 == 0: candidate += 1
        if is_prime_miller_rabin(candidate):
            return candidate

# ── FITUR BARU: FUNGSI HASH DINAMIS ──
def get_hash_int(message: str, algo: str) -> int:
    algo_clean = algo.lower().replace("-", "")
    return int(hashlib.new(algo_clean, message.encode('utf-8')).hexdigest(), 16)

def get_hash_hex(message: str, algo: str) -> str:
    algo_clean = algo.lower().replace("-", "")
    return hashlib.new(algo_clean, message.encode('utf-8')).hexdigest()

def sha256_int(message: str) -> int:
    return int(hashlib.sha256(message.encode()).hexdigest(), 16)

def sha256_hex(message: str) -> str:
    return hashlib.sha256(message.encode()).hexdigest()

def sha1_int(message: str) -> int:
    return int(hashlib.sha1(message.encode()).hexdigest(), 16)

# ==========================================
# ALGORITMA 1 — RSA
# ==========================================
def rsa_keygen():
    p = generate_prime(low=1_000_003, high=9_999_991)
    q = generate_prime(low=1_000_003, high=9_999_991)
    while q == p: q = generate_prime(low=1_000_003, high=9_999_991)
    n = p * q
    phi = (p - 1) * (q - 1)
    while True:
        d = random.randint(2, phi - 1)
        if gcd(d, phi) == 1: break
    e = mod_inverse(d, phi)
    return {"p": p, "q": q, "n": n, "phi": phi, "d": d, "e": e}

def rsa_sign(message: str, keys: dict, hash_algo: str) -> dict:
    h = get_hash_int(message, hash_algo)
    h_mod = h % keys["n"]
    S = pow(h_mod, keys["d"], keys["n"])
    return {"hash_hex": get_hash_hex(message, hash_algo), "hash_int": h, "hash_mod": h_mod, "S": S}

def rsa_verify(message: str, sig: dict, keys: dict, hash_algo: str) -> dict:
    h1 = get_hash_int(message, hash_algo) % keys["n"]
    h2 = pow(sig["S"], keys["e"], keys["n"])
    return {"h1": h1, "h2": h2, "valid": (h1 == h2)}

# ==========================================
# ALGORITMA 2 — El Gamal
# ==========================================
def elgamal_keygen():
    p = generate_prime(low=1_000_003, high=9_999_991)
    g = random.randint(2, p - 1)
    x = random.randint(2, p - 2)
    y = pow(g, x, p)
    return {"p": p, "g": g, "x": x, "y": y}

def elgamal_sign(message: str, keys: dict, hash_algo: str, k_val: int = None) -> dict:
    p, g, x = keys["p"], keys["g"], keys["x"]
    M = get_hash_int(message, hash_algo) % (p - 1)
    p1 = p - 1
    
    if k_val is not None:
        k = k_val
    else:
        while True:
            k = random.randint(2, p1 - 1)
            if gcd(k, p1) == 1: break
            
    a = pow(g, k, p)
    k_inv = mod_inverse(k, p1)
    b = (k_inv * (M - x * a)) % p1
    # ── MENGIRIM K_INV KE UI ──
    return {"hash_hex": get_hash_hex(message, hash_algo), "M": M, "k": k, "a": a, "b": b, "k_inv": k_inv}

def elgamal_verify(message: str, sig: dict, keys: dict, hash_algo: str) -> dict:
    p, g, y = keys["p"], keys["g"], keys["y"]
    M = get_hash_int(message, hash_algo) % (p - 1)
    a, b = sig["a"], sig["b"]
    lhs = pow(g, M, p)
    rhs = (pow(y, a, p) * pow(a, b, p)) % p
    return {"lhs": lhs, "rhs": rhs, "M": M, "valid": (lhs == rhs)}

# ==========================================
# ALGORITMA 3 — Schnorr
# ==========================================
def schnorr_keygen():
    MAX_ITER = 2000
    for _ in range(MAX_ITER):
        q = generate_prime(bits=17)
        for k in range(2, 50000):
            p = k * q + 1
            if p.bit_length() == 32 and is_prime_miller_rabin(p): break
        else: continue
        for h_try in range(2, 100):
            g = pow(h_try, (p - 1) // q, p)
            if g > 1: break
        else: continue
        x = random.randint(1, q - 1)
        g_inv = mod_inverse(g, p)
        y = pow(g_inv, x, p)
        # ── FITUR BARU: Mengirim g_inv ke UI ──
        return {"p": p, "q": q, "g": g, "x": x, "y": y, "g_inv": g_inv}
    raise RuntimeError("Gagal generate parameter Schnorr, coba lagi.")

def schnorr_sign(message: str, keys: dict, hash_algo: str, k_val: int = None) -> dict:
    p, q, g, x = keys["p"], keys["q"], keys["g"], keys["x"]
    
    if k_val is not None:
        k = k_val
    else:
        k = random.randint(1, q - 1)
        
    r = pow(g, k, p)
    concat = f"{message}{r}"
    h_hex = get_hash_hex(concat, hash_algo)
    h_int = get_hash_int(concat, hash_algo)
    
    e = h_int % q
    if e == 0: e = 1
    s = (k + x * e) % q
    
    return {"hash_hex": h_hex, "hash_int": h_int, "k": k, "r": r, "e": e, "s": s}

def schnorr_verify(message: str, sig: dict, keys: dict, hash_algo: str) -> dict:
    p, q, g, y = keys["p"], keys["q"], keys["g"], keys["y"]
    e, s = sig["e"], sig["s"]
    rv = (pow(g, s, p) * pow(y, e, p)) % p
    ev = get_hash_int(f"{message}{rv}", hash_algo) % q
    if ev == 0: ev = 1
    return {"rv": rv, "ev": ev, "e_original": e, "valid": (ev == e)}

# ==========================================
# ALGORITMA 4 — DSA
# ==========================================
def dsa_keygen():
    MAX_ITER = 2000
    for _ in range(MAX_ITER):
        q = generate_prime(bits=17)
        for k in range(2, 50000):
            p = k * q + 1
            if p.bit_length() == 32 and is_prime_miller_rabin(p): break
        else: continue
        for h_try in range(2, 100):
            g = pow(h_try, (p - 1) // q, p)
            if g > 1: break
        else: continue
        x = random.randint(1, q - 1)
        y = pow(g, x, p)
        return {"p": p, "q": q, "g": g, "x": x, "y": y}
    raise RuntimeError("Gagal generate parameter DSA, coba lagi.")

# ── FITUR BARU: DSA Menerima Input k Manual & Mengembalikan k_inv ──
def dsa_sign(message: str, keys: dict, hash_algo: str, k_val: int = None) -> dict:
    p, q, g, x = keys["p"], keys["q"], keys["g"], keys["x"]
    h_int = get_hash_int(message, hash_algo)
    H_M = h_int % q
    
    if k_val is not None:
        k = k_val
    else:
        while True:
            k = random.randint(1, q - 1)
            if gcd(k, q) == 1: break
            
    r = pow(g, k, p) % q
    # Jika menggunakan mode otomatis dan hasilnya 0, cari k baru
    if r == 0 and k_val is None: return dsa_sign(message, keys, hash_algo)
    
    k_inv = mod_inverse(k, q)
    s = (k_inv * (H_M + x * r)) % q
    
    if s == 0 and k_val is None: return dsa_sign(message, keys, hash_algo)
    
    return {"hash_hex": get_hash_hex(message, hash_algo), "hash_int": h_int, "H_M": H_M, "k": k, "r": r, "s": s, "k_inv": k_inv}

def dsa_verify(message: str, sig: dict, keys: dict, hash_algo: str) -> dict:
    p, q, g, y = keys["p"], keys["q"], keys["g"], keys["y"]
    r, s = sig["r"], sig["s"]
    h_int = get_hash_int(message, hash_algo)
    H_M = h_int % q
    
    w = mod_inverse(s, q)
    u1 = (H_M * w) % q
    u2 = (r * w) % q
    v = (pow(g, u1, p) * pow(y, u2, p)) % p % q
    
    return {"w": w, "u1": u1, "u2": u2, "v": v, "valid": (v == r)}
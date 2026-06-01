# 🔐 Digital Signature Tugas 2

> Implementasi Pembangkitan Kunci, Penandatanganan, dan Verifikasi Pesan Menggunakan Berbagai Algoritma Kriptografi

## 📋 Deskripsi Proyek

Aplikasi antarmuka web interaktif (menggunakan Streamlit) untuk mendemonstrasikan cara kerja algoritma Tanda Tangan Digital (*Digital Signature*) dalam mengamankan keaslian dan integritas sebuah pesan digital secara *real-time*.

**Skema Kriptografi yang Diimplementasikan:**
- **RSA**: Simulasi pembangkitan kunci dan tanda tangan algoritma Rivest-Shamir-Adleman
- **El Gamal**: Implementasi skema tanda tangan diskrit logaritma El Gamal
- **Schnorr**: Simulasi skema keamanan komputasi efisien Schnorr
- **DSA**: Implementasi standar Digital Signature Algorithm

---

## 🗂️ Struktur File
- `app.py`: File utama untuk menjalankan dan menampilkan antarmuka web Streamlit.
- `crypto_core.py`: Berisi logika inti dan rumus matematika untuk perhitungan setiap algoritma kriptografi.
- `ui_components.py`: Berisi komponen tata letak (*layout*) dan elemen visual agar tampilan web lebih rapi.

---

## 🚀 Cara Setup & Menjalankan Aplikasi

### ⚠️ PENTING: Setup Virtual Environment (venv)

**JANGAN skip langkah ini!** Virtual environment diperlukan agar *dependencies* (pustaka tambahan) tidak berbenturan dengan *project* Python Anda yang lain.

#### Windows (Command Prompt / PowerShell)
```cmd
# 1. Clone repository
git clone [https://github.com/teyetata/DigitalSignatureTere.git](https://github.com/teyetata/DigitalSignatureTere.git)
cd DigitalSignatureTere

# 2. Buat virtual environment
python -m venv venv

# 3. Aktifkan virtual environment
# Jika menggunakan Command Prompt (CMD):
venv\Scripts\activate
# Jika menggunakan PowerShell:
.\venv\Scripts\Activate.ps1

# 4. Pastikan venv aktif (akan muncul tulisan (venv) di kiri prompt terminal)

# 5. Install dependencies
# (Pastikan menginstal library yang dibutuhkan, utamanya Streamlit)
pip install streamlit
# Jika ada file requirements.txt, gunakan: pip install -r requirements.txt

# 6. Jalankan aplikasi
streamlit run app.py

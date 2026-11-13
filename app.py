import streamlit as st
import json
import os
import time
import random
from datetime import datetime, timedelta, timezone

# Türkiye Saat Dilimi (UTC+3)
TR_SAATI = timezone(timedelta(hours=3))

def simdi_tr():
    return datetime.now(TR_SAATI).replace(tzinfo=None)

st.set_page_config(
    page_title="Aralıklı Oruç",
    page_icon="⏳",
    layout="centered"
)

VERI_DOSYASI = "oruc_verisi.json"

# --- Hafıza (Veri İşlemleri) ---
def veri_yukle():
    if os.path.exists(VERI_DOSYASI):
        with open(VERI_DOSYASI, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

def veri_kaydet(baslangic_zamani, hedef_saat, su_sayisi=0):
    veri = {
        "baslangic": baslangic_zamani.isoformat(),
        "hedef_saat": hedef_saat,
        "su_sayisi": su_sayisi
    }
    with open(VERI_DOSYASI, "w", encoding="utf-8") as f:
        json.dump(veri, f)

def veri_sil():
    if os.path.exists(VERI_DOSYASI):
        os.remove(VERI_DOSYASI)

# --- Beyin (Biyolojik Hesaplamalar) ---
def vucut_durumu_getir(gecen_saat):
    if gecen_saat < 4:
        st.success(...)
        return "🍽️ **Sindirim Aşaması:** Kan şekeri yükseliyor ve insülin salgılanıyor."
    elif gecen_saat < 12:
        return "📉 **Kan Şekeri Dengeleniyor:** Vücut glikojen depolarını kullanmaya başladı."
    elif gecen_saat < 16:
        return "🔥 **Yağ Yakımı (Ketozis):** Glikojen azaldı! Vücut enerji için yağ yakıyor."
    elif gecen_saat < 24:
        return "🧬 **Derin Yağ Yakımı & Otofaji:** Hücresel yenilenme ve temizlik hızlandı."
    else:
        return "⚡ **Maksimum Otofaji & HGH:** Büyüme hormonu zirvede, derin yenilenme aktif."
    MOTIVASYON_SOZLERI = [
    "🔥 Şu an vücudun kendi kendini onarıyor, harika gidiyorsun!",
    "💧 Bir bardak su iç, açlık hissinin çoğu aslında susuzluktur.",
    "⚡ Disiplin, o an istediğin şey ile en çok istediğin şey arasındaki seçimdir.",
    "🧬 Her geçen saat hücrelerin yenileniyor, hedefe çok az kaldı!"
]
# --- Vitrin (Arayüz) ---
st.title("⏳ Aralıklı Oruç Takip")

veri = veri_yukle()

if veri:
    baslangic = datetime.fromisoformat(veri["baslangic"])
    hedef_saat = veri["hedef_saat"]
    su = veri.get("su_sayisi", 0)
    bitis = baslangic + timedelta(hours=hedef_saat)
    su_an = simdi_tr()

    gecen_saniye = max(0, int((su_an - baslangic).total_seconds()))
    gecen_saat = gecen_saniye / 3600
    yuzde = min(1.0, gecen_saat / hedef_saat)

    saat = gecen_saniye // 3600
    dakika = (gecen_saniye % 3600) // 60
    saniye = gecen_saniye % 60

    # Dijital Sayaç Kartı
    st.markdown(f"""
        <div style="background-color:#1E1E2E; padding:25px; border-radius:15px; text-align:center; margin-bottom:15px;">
            <p style="color:#A6ADC8; margin:0; font-size:14px;">GEÇEN SÜRE ({hedef_saat} SAATLİK PLAN)</p>
            <h1 style="color:#A6E3A1; font-size:48px; margin:10px 0; font-family:monospace;">{saat:02d}:{dakika:02d}:{saniye:02d}</h1>
            <p style="color:#CDD6F4; margin:0; font-size:14px;">Başlangıç: <b>{baslangic.strftime('%d.%m %H:%M')}</b> &nbsp;|&nbsp; Hedef: <b>{bitis.strftime('%d.%m %H:%M')}</b></p>
        </div>
    """, unsafe_allow_html=True)

    st.progress(yuzde)

    # Kalan Süre ve Yüzde Metrikleri
    kalan_saniye = int((bitis - su_an).total_seconds())
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Tamamlanan", f"%{yuzde * 100:.1f}")
    with col2:
        if kalan_saniye > 0:
            k_saat = kalan_saniye // 3600
            k_dakika = (kalan_saniye % 3600) // 60
            st.metric("Kalan Süre", f"{k_saat} sa {k_dakika} dk")
        else:
            st.metric("Durum", "Hedef Tamamlandı! 🎉")

    st.info(vucut_durumu_getir(gecen_saat))
    
    st.divider()

    # Su Takibi Bölümü
    st.subheader(f"💧 İçilen Su: {su} Bardak ({su * 0.25:.2f} L)")
    su_col1, su_col2 = st.columns(2)
    with su_col1:
        if st.button("💧 +1 Bardak Su", use_container_width=True):
            veri_kaydet(baslangic, hedef_saat, su + 1)
            st.rerun()
    with su_col2:
        if st.button("↩️ 1 Bardak Geri Al", use_container_width=True) and su > 0:
            veri_kaydet(baslangic, hedef_saat, su - 1)
            st.rerun()

    st.divider()

    # Orucu Bitir Butonu
    if st.button("⏹ Orucu Bitir / Sıfırla", type="primary", use_container_width=True):
        veri_sil()
        st.rerun()

    time.sleep(1)
    st.rerun()

else:
    st.info("Şu an aktif bir orucun bulunmuyor. Aşağıdan planını seçip hemen başlayabilirsin.")

    hedef = st.selectbox(
        "Oruç Planını Seç (Saat):",
        options=[14, 16, 18, 20, 24],
        index=1
    )

    st.subheader("Ne zaman başladın?")
    
    if st.button("▶ Orucu Şimdi Başlat", type="primary", use_container_width=True):
        veri_kaydet(simdi_tr(), hedef, 0)
        st.rerun()

    st.markdown("<p style='text-align:center; color:gray;'>— veya —</p>", unsafe_allow_html=True)

    secilen_saat = st.time_input("Yemeyi bıraktığın saati seç:", value=simdi_tr().time())
    if st.button("🕒 Seçilen Saatte Başlat", use_container_width=True):
        simdi = simdi_tr()
        baslangic = simdi.replace(hour=secilen_saat.hour, minute=secilen_saat.minute, second=0, microsecond=0)
        if baslangic > simdi:
            baslangic -= timedelta(days=1)
        veri_kaydet(baslangic, hedef, 0)
        st.rerun()

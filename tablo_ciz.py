import json
import matplotlib.pyplot as plt

with open("metrikler.json", "r") as f:
    metrikler = json.load(f)

# Hangi N değerleri var
N_degerleri = sorted(set(m["N"] for m in metrikler))

# Sütunlar (gösterilecek metrikler ve başlıkları)
sutunlar = [
    ("T_p",    "T_p (s)"),
    ("T_comp", "T_comp (s)"),
    ("S",      "Speedup"),
    ("E",      "Efficiency"),
]

# Sayıyı tabloda gösterilebilir hale getir
def bicim(deger, anahtar):
    if anahtar in ("S", "E"):
        return f"{deger:.3f}"
    # Zaman sütunları: küçükse daha fazla basamak göster
    if deger < 0.01:
        return f"{deger:.6f}"
    elif deger < 1:
        return f"{deger:.4f}"
    else:
        return f"{deger:.3f}"

for N in N_degerleri:
    # Bu N için kayıtları topla
    alt_kume = [m for m in metrikler if m["N"] == N]
    # Satır sırası: önce CPU, sonra Dil, sonra P
    alt_kume.sort(key=lambda x: (x["CPU"], x["Dil"], x["P"]))

    # Tablo verisi
    satir_etiketleri = []
    hucre_verisi = []
    for m in alt_kume:
        satir_etiketleri.append(f"{m['CPU']}  |  {m['Dil']}  |  P={m['P']}")
        hucre_verisi.append([bicim(m[anahtar], anahtar) for anahtar, _ in sutunlar])

    sutun_etiketleri = [baslik for _, baslik in sutunlar]

    # Figür boyutunu satır sayısına göre ayarla
    fig, ax = plt.subplots(figsize=(10, 0.45 * len(alt_kume) + 1.5))
    ax.axis("off")
    ax.set_title(f"N = {N}  (Paralel Performans Metrikleri)",
                 fontsize=13, fontweight="bold", pad=15)

    tablo = ax.table(
        cellText=hucre_verisi,
        rowLabels=satir_etiketleri,
        colLabels=sutun_etiketleri,
        cellLoc="center",
        rowLoc="center",
        loc="center",
    )
    tablo.auto_set_font_size(False)
    tablo.set_fontsize(10)
    tablo.scale(1, 1.4)

    # Başlık satır ve sütununu hafifçe vurgula
    for (i, j), hucre in tablo.get_celld().items():
        if i == 0:  # sütun başlığı
            hucre.set_facecolor("#d9e7f5")
            hucre.set_text_props(fontweight="bold")
        elif j == -1:  # satır etiketi
            hucre.set_facecolor("#f0f0f0")
            hucre.set_text_props(fontweight="bold")

    plt.tight_layout()
    cikti = f"tablo_N{N}.png"
    plt.savefig(cikti, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Yazıldı: {cikti}")

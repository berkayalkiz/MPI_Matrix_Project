import json
import matplotlib.pyplot as plt

# Veriyi oku
with open("sonuclar.json", "r") as f:
    data = json.load(f)

# CPU ismindeki büyük/küçük harf farkını gidermek için normalleştir
for d in data:
    d["Dil"] = d["Dil"].strip()

# Boyutlara renk ata
boyut_renkleri = {
    1024: "tab:blue",
    4096: "tab:red",
    8192: "tab:green",
}

# Dillere çizgi stili ata
dil_stilleri = {
    "Python": "-",   # düz çizgi
    "C": "--",       # kesikli çizgi
}

# Veriyi (Dil, N) gruplarına ayır
gruplar = {}
for d in data:
    anahtar = (d["Dil"], d["N"])
    gruplar.setdefault(anahtar, []).append(d)

# Grafik
plt.figure(figsize=(10, 6))

for (dil, N), kayitlar in gruplar.items():
    # P'ye göre sırala
    kayitlar = sorted(kayitlar, key=lambda x: x["P"])
    P_degerleri = [k["P"] for k in kayitlar]
    T_degerleri = [k["T_total"] for k in kayitlar]

    # P=1 referans alınarak speedup hesapla
    T1 = T_degerleri[0]  # P=1 değeri (sıralı olduğu için ilk eleman)
    speedup = [T1 / t for t in T_degerleri]

    plt.plot(
        P_degerleri,
        speedup,
        linestyle=dil_stilleri[dil],
        color=boyut_renkleri[N],
        marker="o",
        linewidth=2,
        label=f"{dil}, N={N}",
    )

plt.xlabel("Çekirdek Sayısı (P)")
plt.ylabel("Speedup (T_1 / T_P)")
plt.title(" i5 10400 Speedup: Python (düz) vs C (kesikli)")
plt.xscale("log", base=2)
plt.xticks([1, 2, 4, 8, 16], ["1", "2", "4", "8", "16"])
plt.grid(True, which="both", linestyle=":", alpha=0.6)
plt.legend()
plt.tight_layout()

plt.savefig("speedup.png", dpi=150)
plt.show()
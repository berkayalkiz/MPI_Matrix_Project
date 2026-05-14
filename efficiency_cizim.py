import json
import matplotlib.pyplot as plt

# Veriyi oku
with open("sonuclar_10400.json", "r") as f:
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

    # P=1 referans alınarak speedup ve efficiency hesapla
    T1 = T_degerleri[0]
    speedup = [T1 / t for t in T_degerleri]
    efficiency = [s / p for s, p in zip(speedup, P_degerleri)]

    plt.plot(
        P_degerleri,
        efficiency,
        linestyle=dil_stilleri[dil],
        color=boyut_renkleri[N],
        marker="o",
        linewidth=2,
        label=f"{dil}, N={N}",
    )

# İdeal efficiency çizgisi (E=1)
#plt.axhline(y=1.0, color="gray", linestyle=":", linewidth=1, alpha=0.7, label="İdeal (E=1)")

plt.xlabel("Çekirdek Sayısı (P)")
plt.ylabel("Efficiency (E = Speedup / P)")
plt.title("i5 10400 Efficiency: Python (düz) vs C (kesikli)")
plt.xscale("log", base=2)
plt.xticks([1, 2, 4, 8, 16], ["1", "2", "4", "8", "16"])
plt.grid(True, which="both", linestyle=":", alpha=0.6)
plt.legend()
plt.tight_layout()

plt.savefig("efficiency.png", dpi=150)
plt.show()
import json

with open("sonuclar_10400.json", "r") as f:
    veri1 = json.load(f)
with open("sonuclar_11400h.json", "r") as f:
    veri2 = json.load(f)

ham_veri = veri1 + veri2

# normalleştirme muhabbeti
for d in ham_veri:
    d["Dil"] = d["Dil"].strip()
    d["CPU"] = d["CPU"].strip()
    # i5-11400f / i5-11400F farkını gider
    if d["CPU"].lower() == "i5-11400f":
        d["CPU"] = "i5-11400F"

# (cpu, dil, N) gruplama muhabbeti, her grupta P=1 değerini referans alıp S ve E hesapla
gruplar = {}
for d in ham_veri:
    anahtar = (d["CPU"], d["Dil"], d["N"])
    gruplar.setdefault(anahtar, []).append(d)

metrikler = []
for anahtar, kayitlar in gruplar.items():
    kayitlar = sorted(kayitlar, key=lambda x: x["P"])

    # P=1 referans değeri (T_p = T_total oluyor aslında)
    T_p_ref = None
    for k in kayitlar:
        if k["P"] == 1:
            T_p_ref = k["T_total"]
            break
    if T_p_ref is None:  # P=1 yoksa en küçük p yi referans al (unutursak diye ekledim ya)
        T_p_ref = kayitlar[0]["T_total"] 

    for k in kayitlar:
        T_p = k["T_total"]
        T_comp = k["T_comp"]
        P = k["P"]
        S = T_p_ref / T_p
        E = S / P
        metrikler.append({
            "CPU": k["CPU"],
            "Dil": k["Dil"],
            "N": k["N"],
            "P": P,
            "T_p": T_p,
            "T_comp": T_comp,
            "S": S,
            "E": E,
        })


metrikler.sort(key=lambda x: (x["CPU"], x["Dil"], x["N"], x["P"]))

with open("metrikler.json", "w") as f:
    json.dump(metrikler, f, indent=2, ensure_ascii=False)

print(f"Toplam {len(metrikler)} kayıt yazıldı -> metrikler.json")
print(f"CPU'lar: {sorted(set(m['CPU'] for m in metrikler))}")
print(f"Diller: {sorted(set(m['Dil'] for m in metrikler))}")
print(f"N değerleri: {sorted(set(m['N'] for m in metrikler))}")

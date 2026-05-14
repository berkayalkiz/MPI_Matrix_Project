import sys
import json
import os

# C'den gelen argümanları al (CPU, Dil, N, P, T_total, T_comp)
cpu_modeli = sys.argv[1]
dil = sys.argv[2]
N = int(sys.argv[3])    
size = int(sys.argv[4])
t_total = float(sys.argv[5])
t_comp = float(sys.argv[6])

dosya_adi = "sonuclar-10400.json"
veriler = []

if os.path.exists(dosya_adi):
    with open(dosya_adi, "r") as f:
        try:
            veriler = json.load(f)
        except json.JSONDecodeError:
            veriler = [] 

kayit_bulundu = False
for kayit in veriler:
    if kayit.get("CPU") == cpu_modeli and kayit.get("Dil") == dil and kayit.get("P") == size and kayit.get("N") == N:
        kayit["T_total"] = t_total
        kayit["T_comp"] = t_comp
        kayit_bulundu = True
        break
        
if not kayit_bulundu:
    veriler.append({
        "CPU": cpu_modeli,
        "Dil": dil,
        "N": N,          
        "P": size,
        "T_total": t_total,
        "T_comp": t_comp
    })

with open(dosya_adi, "w") as f:
    json.dump(veriler, f, indent=4)
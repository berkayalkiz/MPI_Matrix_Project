import os
# numpy ın kendi kendine paralelleşmesini yasaklama muhabbeti
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["VECLIB_MAXIMUM_THREADS"] = "1"
os.environ["NUMEXPR_NUM_THREADS"] = "1"

from mpi4py import MPI
import numpy as np
import json

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

N = 0
A = None
B = None

if rank == 0:
    with open('a.txt', 'r') as f:
        N = int(f.readline().strip())
        A = np.loadtxt(f, dtype=np.float64)
        
    with open('b.txt', 'r') as f:
        f.readline()
        B = np.loadtxt(f, dtype=np.float64)
        
    A = np.ascontiguousarray(A, dtype=np.float64) 
    start_total = MPI.Wtime()
else:
    B = None

N = comm.bcast(N, root=0)
if rank != 0:
    B = np.empty((N, N), dtype=np.float64)
comm.Bcast(B, root=0)

satir_sayisi = N // size
local_A = np.empty((satir_sayisi, N), dtype=np.float64)
comm.Scatter(A, local_A, root=0)

start_comp = MPI.Wtime()
local_C = np.dot(local_A, B) 
end_comp = MPI.Wtime()
t_comp = end_comp - start_comp

if rank == 0:
    C = np.empty((N, N), dtype=np.float64)
else:
    C = None
comm.Gather(local_C, C, root=0)

// json kaydewtme burası
if rank == 0:
    end_total = MPI.Wtime()
    t_total = end_total - start_total
    
    cpu_modeli = "i5-10400" 
    dil = "Python"
    dosya_adi = "sonuclar_10400.json"
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
        yeni_veri = {
            "CPU": cpu_modeli,
            "Dil": dil,
            "N": N,
            "P": size,
            "T_total": t_total,
            "T_comp": t_comp
        }
        veriler.append(yeni_veri)
    
    with open(dosya_adi, "w") as f:
        json.dump(veriler, f, indent=4)
        
    print(f"P={size} test edildi. Toplam Sure: {t_total:.6f} sn | Saf Hesaplama: {t_comp:.6f} sn")
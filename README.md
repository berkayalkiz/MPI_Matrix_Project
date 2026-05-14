# Dağıtık Bellekli Matris Çarpımı (MPI ile C vs Python Analizi)

Bu proje, Çok Çekirdekli İşlemci mimarilerinde **Message Passing Interface (MPI)** kullanılarak dağıtık bellekli paralel programlama performansının ölçülmesi ve analiz edilmesi amacıyla geliştirilmiştir. 

Proje kapsamında kare matris çarpım işlemi (C = A x B), hem düşük seviyeli bir dil olan **C (OpenMPI & OpenBLAS)** hem de yüksek seviyeli bir dil olan **Python (mpi4py & NumPy)** kullanılarak paralelleştirilmiş ve farklı işlemci/çekirdek senaryolarında test edilmiştir.

## Projenin Temel Özellikleri
* **Adil Performans Kıyaslaması:** Python'da NumPy arka planda kullandığı C tabanlı BLAS optimizasyonlarına karşı, C kodunda da `cblas_dgemm` (OpenBLAS) kullanılarak tam anlamıyla "elma ile elma" kıyası yapılmıştır.
* **Dağıtık Bellek Yönetimi:** Master işlemci (Rank 0) verileri okur, `MPI_Bcast` ve `MPI_Scatter` ile işçi işlemcilere dağıtır, hesaplamalar bittikten sonra `MPI_Gather` ile sonuçları birleştirir.
* **Otomatik Raporlama:** Her iki dildeki test sonuçları (Toplam Süre ve Saf Hesaplama Süresi), işlemci sayısı (P) ve matris boyutu (N) baz alınarak otomatik olarak bir `json` dosyasına loglanır.

## Sistem Gereksinimleri
Ubuntu (veya WSL) ortamında kodu derleyip çalıştırabilmek için aşağıdaki paketlerin kurulu olması gerekmektedir:
**C Ortamı İçin:**
```bash
sudo apt update
sudo apt install openmpi-bin libopenmpi-dev
sudo apt install libopenblas-dev

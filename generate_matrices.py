import random

N = 1024   # Matris boyutu


def matris_yaz(dosya_adi, n):
    random.seed(hash(dosya_adi) % (2**32))
    with open(dosya_adi, "w") as f:
        f.write(f"{n}\n")
        for _ in range(n):
            satir = [str(random.randint(1, 9)) for _ in range(n)]
            f.write(" ".join(satir) + "\n")
    print(f"{dosya_adi} olusturuldu ({n}x{n}).")


if __name__ == "__main__":
    matris_yaz("a.txt", N)
    matris_yaz("b.txt", N)

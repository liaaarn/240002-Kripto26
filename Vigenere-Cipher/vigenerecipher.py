# Nama: Aulia Ramdani Nur
# NPM : 140810240002
# Deskripsi: Buatlah kode program untuk Vigenere Cipher! 
# (enkripsi dan dekripsi)(bahasa pemrograman bebas)

while True:
    print("\n==============================")
    print("       VIGENERE CIPHER")
    print("==============================")
    print("1. Enkripsi")
    print("2. Dekripsi")
    print("3. Keluar")

    pilihan = int(input("Pilih menu: "))

    # enkripsi
    if pilihan == 1:
        plaintext = input("\nMasukkan plaintext : ").upper()
        key = input("Masukkan key       : ").upper()

        P = []
        nP = []
        K = []
        nK = []
        hasil_angka = []
        C = []

        key_index = 0

        for huruf in plaintext:
            if huruf.isalpha():
                # Nilai plaintext
                angka_P = ord(huruf) - ord('A')

                # Nilai key
                huruf_K = key[key_index % len(key)]
                angka_K = ord(huruf_K) - ord('A')

                # Enkripsi
                angka_C = (angka_P + angka_K) % 26
                huruf_C = chr(angka_C + ord('A'))

                P.append(huruf)
                nP.append(angka_P)
                K.append(huruf_K)
                nK.append(angka_K)
                hasil_angka.append(angka_C)
                C.append(huruf_C)

                key_index += 1

            else:
                P.append(huruf)
                K.append(" ")
                C.append(huruf)

        print("\n===== PROSES ENKRIPSI =====\n")

        print("P             :", *P)
        print("n(P)          :", *nP)
        print()
        print("K             :", *K)
        print("n(K)          :", *nK)
        print()
        print("(P+K) mod 26  :", *hasil_angka)
        print()
        print("C             :", *C)

        print("\nHasil Enkripsi :", "".join(C))

    # dekripsi
    elif pilihan == 2:
        ciphertext = input("\nMasukkan ciphertext : ").upper()
        key = input("Masukkan key        : ").upper()

        C = []
        nC = []
        K = []
        nK = []
        hasil_angka = []
        P = []

        key_index = 0

        for huruf in ciphertext:
            if huruf.isalpha():
                # Nilai ciphertext
                angka_C = ord(huruf) - ord('A')

                # Nilai key
                huruf_K = key[key_index % len(key)]
                angka_K = ord(huruf_K) - ord('A')

                # Dekripsi
                angka_P = (angka_C - angka_K) % 26
                huruf_P = chr(angka_P + ord('A'))

                C.append(huruf)
                nC.append(angka_C)
                K.append(huruf_K)
                nK.append(angka_K)
                hasil_angka.append(angka_P)
                P.append(huruf_P)

                key_index += 1

            else:
                C.append(huruf)
                K.append(" ")
                P.append(huruf)

        print("\n===== PROSES DEKRIPSI =====\n")

        print("C             :", *C)
        print("n(C)          :", *nC)
        print()
        print("K             :", *K)
        print("n(K)          :", *nK)
        print()
        print("(C-K) mod 26  :", *hasil_angka)
        print()
        print("P             :", *P)

        print("\nHasil Dekripsi :", "".join(P))

    # keluar
    elif pilihan == 3:

        print("\nProgram selesai.")
        break
    else:
        print("\nPilihan tidak tersedia.")
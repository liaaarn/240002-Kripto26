# Nama: Aulia Ramdani Nur
# NPM : 140810240002
# Deskripsi: Buatlah program untuk enkripsi, dekripsi, dan mencari kunci Hill Cipher (bahasa pemrograman bebas)

ALFABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
MOD = 26

# konversi huruf --> angka
def text_to_numbers(text):
    text = text.upper().replace(" ", "")
    return [ALFABET.index(c) for c in text]


def numbers_to_text(numbers):
    return ''.join(ALFABET[n] for n in numbers)

# mencari invers module
def mod_inverse(a, m):
    a = a % m

    for i in range(1, m):
        if (a * i) % m == 1:
            return i

    return None

# determinan matriks
def determinant(matrix):
    n = len(matrix)

    if n == 1:
        return matrix[0][0]

    if n == 2:
        return (
            matrix[0][0] * matrix[1][1]
            - matrix[0][1] * matrix[1][0]
        )

    hasil = 0

    for j in range(n):
        sub_matrix = []
        for i in range(1, n):
            baris = []
            for k in range(n):
                if k != j:
                    baris.append(matrix[i][k])

            sub_matrix.append(baris)

        tanda = (-1) ** j

        hasil += (
            tanda
            * matrix[0][j]
            * determinant(sub_matrix)
        )

    return hasil

# matriks minor
def minor_matrix(matrix, row, col):
    return [
        [
            matrix[i][j]
            for j in range(len(matrix))
            if j != col
        ]
        for i in range(len(matrix))
        if i != row
    ]

# invers matriks modulo 26
def inverse_matrix(matrix):
    n = len(matrix)

    det = determinant(matrix)
    det = det % MOD

    det_inverse = mod_inverse(det, MOD)

    # Jika determinan tidak punya invers modulo 26
    if det_inverse is None:
        return None

    # Matriks 1x1
    if n == 1:
        return [[det_inverse]]

    # Membuat matriks kofaktor
    cofactors = []
    for i in range(n):
        row = []
        for j in range(n):
            minor = minor_matrix(matrix, i, j)
            nilai = determinant(minor)
            nilai = ((-1) ** (i + j)) * nilai
            row.append(nilai % MOD)

        cofactors.append(row)

    # Transpose matriks kofaktor
    inverse = []

    for i in range(n):
        row = []
        for j in range(n):
            nilai = cofactors[j][i]
            nilai = (det_inverse * nilai) % MOD
            row.append(nilai)
        inverse.append(row)

    return inverse

# perkalian matriks dengan vektor
def multiply_matrix_vector(matrix, vector):
    hasil = []

    for i in range(len(matrix)):
        total = 0
        for j in range(len(vector)):
            total += matrix[i][j] * vector[j]
        hasil.append(total % MOD)

    return hasil

# ekripsi
def encrypt(plaintext, key):
    plaintext = plaintext.upper().replace(" ", "")
    n = len(key)

    # Padding X jika jumlah karakter tidak habis dibagi n
    while len(plaintext) % n != 0:
        plaintext += "X"

    numbers = text_to_numbers(plaintext)
    ciphertext = ""

    for i in range(0, len(numbers), n):
        blok = numbers[i:i + n]
        hasil = multiply_matrix_vector(key, blok)
        ciphertext += numbers_to_text(hasil)

    return ciphertext

# dekripsi
def decrypt(ciphertext, key):
    ciphertext = ciphertext.upper().replace(" ", "")
    n = len(key)

    # Ciphertext harus habis dibagi ukuran blok
    if len(ciphertext) % n != 0:
        return None

    inverse_key = inverse_matrix(key)

    # Jika kunci tidak mempunyai invers
    if inverse_key is None:
        return None

    numbers = text_to_numbers(ciphertext)
    plaintext = ""

    for i in range(0, len(numbers), n):
        blok = numbers[i:i + n]
        hasil = multiply_matrix_vector(
            inverse_key,
            blok
        )
        plaintext += numbers_to_text(hasil)

    return plaintext

# cek apakah kunci valid
def is_valid_key(key):
    inverse = inverse_matrix(key)
    return inverse is not None

# bandingkan 2 baris
def row_less(row1, row2):
    for i in range(len(row1)):
        if row1[i] < row2[i]:
            return True
        
        if row1[i] > row2[i]:
            return False

    return False

# cari 1 baris kunci
def find_key_row(blocks, targets, n):
    # coba semua kemungkinan:
    # [0,0], [0,1], ..., [25,25] untuk n = 2
    # Setiap kandidat diuji terhadap semua blok plaintext.
    row = [0] * n
    best_row = None

    def search(position):
        nonlocal best_row

        # Semua elemen baris sudah diisi
        if position == n:
            # Periksa kandidat terhadap semua blok
            for i in range(len(blocks)):
                total = 0
                for j in range(n):
                    total += row[j] * blocks[i][j]

                if total % MOD != targets[i]:
                    return

            # Kandidat cocok
            kandidat = row.copy()

            if best_row is None:
                best_row = kandidat
            elif row_less(kandidat, best_row):
                best_row = kandidat

            return

        # Coba nilai 0 sampai 25
        for nilai in range(MOD):
            row[position] = nilai
            search(position + 1)

    search(0)

    return best_row

# cari kunci
def find_key(plaintext, ciphertext, n):
    plaintext = plaintext.upper().replace(" ", "")
    ciphertext = ciphertext.upper().replace(" ", "")

    # validasi panjang
    if len(plaintext) != len(ciphertext):
        return None

    # minimal diperlukan n blok
    # n blok × n karakter = n*n karakter
    if len(plaintext) < n * n:
        return None

    # jumlah karakter harus habis dibagi n
    if len(plaintext) % n != 0:
        return None

    p_numbers = text_to_numbers(plaintext)
    c_numbers = text_to_numbers(ciphertext)

    # membentuk blok plaintext dan ciphertext
    blocks = []
    cipher_blocks = []

    for i in range(0, len(p_numbers), n):
        blok_p = p_numbers[i:i + n]
        blok_c = c_numbers[i:i + n]

        blocks.append(blok_p)
        cipher_blocks.append(blok_c)

    # Mencari setiap baris matriks K
    # Misalnya:
    # K = [ a b ]
    #     [ c d ]
    # Baris pertama dicari dari target ciphertext
    # huruf pertama setiap blok.
    # Baris kedua dicari dari target ciphertext
    # huruf kedua setiap blok.

    K = []

    for row_index in range(n):
        targets = []
        for blok in cipher_blocks:
            targets.append(blok[row_index])
        row = find_key_row(
            blocks,
            targets,
            n
        )

        # jika tidak ditemukan
        if row is None:
            return None

        K.append(row)

    # kunci hill cipher harus modulo 26
    if not is_valid_key(K):
        return None

    # verifikasi
    hasil_ciphertext = encrypt(
        plaintext,
        K
    )

    if hasil_ciphertext != ciphertext:
        return None

    return K

# input matriks
def input_matrix(n):
    matrix = []
    print("\nMasukkan matriks kunci:")

    for i in range(n):
        row = []
        for j in range(n):
            nilai = int(
                input(
                    f"Baris {i + 1}, Kolom {j + 1}: "
                )
            )
            row.append(nilai % MOD)
        matrix.append(row)
    return matrix

# menampilkan matriks
def print_matrix(matrix):
    for row in matrix:
        print(
            " ".join(
                f"{nilai:3}"
                for nilai in row
            )
        )

# main
while True:

    print("\n==============================")
    print("         HILL CIPHER")
    print("==============================")
    print("1. Enkripsi")
    print("2. Dekripsi")
    print("3. Mencari Kunci")
    print("4. Keluar")
    print("==============================")

    pilihan = input("Pilih menu: ")

    # enkripsi 
    if pilihan == "1":
        print("\n--- ENKRIPSI ---")
        n = int(input("Ukuran matriks kunci: "))

        if n < 1:
            print("\nUkuran matriks tidak valid.")
            continue

        key = input_matrix(n)

        plaintext = input("Masukkan plaintext: ")
        ciphertext = encrypt(plaintext, key)

        print("\nMatriks Kunci:")
        print_matrix(key)

        print("\nPlaintext :", plaintext.upper().replace(" ", ""))
        print("Ciphertext:", ciphertext)

    # dekripsi 
    elif pilihan == "2":
        print("\n--- DEKRIPSI ---")
        n = int(input("Ukuran matriks kunci: "))

        if n < 1:
            print("\nUkuran matriks tidak valid.")
            continue

        key = input_matrix(n)

        ciphertext = input("Masukkan ciphertext: ")
        plaintext = decrypt(ciphertext, key)

        print("\nMatriks Kunci:")
        print_matrix(key)

        if plaintext is None:
            print("\nKunci tidak dapat digunakan.")
            print("Pastikan determinan matriks "
                "mempunyai invers modulo 26."
            )
        else:
            print("\nCiphertext:", ciphertext.upper().replace(" ", ""))
            print("Plaintext :", plaintext)

    # cari kunci
    elif pilihan == "3":
        print("\n--- MENCARI KUNCI ---")
        n = int(input("Ukuran matriks kunci: "))

        if n < 1:
            print("\nUkuran matriks tidak valid.")
            continue

        plaintext = input("Masukkan plaintext : ")
        ciphertext = input("Masukkan ciphertext: ")

        key = find_key(plaintext, ciphertext, n)

        if key is None:
            print("\nKunci tidak dapat ditemukan.")
            print("Pastikan:")
            print(f"- Minimal terdapat {n * n} karakter.")
            print("- Panjang plaintext dan ciphertext sama.")
            print("- Matriks kunci yang dicari memiliki invers modulo 26.")
        else:
            print("\nKunci ditemukan!")
            print("\nMatriks Kunci:")
            print_matrix(key)
            print("\nVerifikasi:")
            print(
                plaintext.upper().replace(" ", ""),
                "->",
                encrypt(
                    plaintext,
                    key
                )
            )

    # keluar
    elif pilihan == "4":
        print("\nProgram selesai.")
        break
    else:
        print("\nPilihan tidak valid.")
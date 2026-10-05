# Nama: Aulia Ramdani Nur
# NPM : 140810240002
# Deskripsi: Buat program encode dan decode steganography yang dapat menyembunyikan sebuah pesan atau file gambar 
# (Bahasa Pemrograman Bebas).

from PIL import Image
import os
import sys

# konstanta
MAGIC = b"STEG"
HEADER_SIZE = 8  # 4 byte MAGIC + 4 byte panjang pesan

# folder tempat file lsb_steg.py berada
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# fungsi konversi
def bytes_to_bits(data):
    """
    Mengubah data bytes menjadi kumpulan bit 0 dan 1.
    """
    bits = []

    for byte in data:
        for i in range(7, -1, -1):
            bits.append((byte >> i) & 1)

    return bits

def bits_to_bytes(bits):
    """
    Mengubah kumpulan bit kembali menjadi bytes.
    """
    result = bytearray()

    for i in range(0, len(bits), 8):
        byte = 0

        for bit in bits[i:i + 8]:
            byte = (byte << 1) | bit

        result.append(byte)

    return bytes(result)

# fungsi encode
def encode_image(input_image, output_image, message):
    """
    Menyisipkan pesan ke dalam gambar menggunakan metode LSB.
    """

    try:
        image = Image.open(input_image).convert("RGB")
    except Exception as e:
        print(f"\n[ERROR] Gagal membuka gambar: {e}")
        return False

    pixels = list(image.getdata())

    # pesan diubah menjadi UTF-8
    message_bytes = message.encode("utf-8")

    # header:
    # 4 byte = MAGIC
    # 4 byte = panjang pesan
    header = MAGIC + len(message_bytes).to_bytes(
        4,
        byteorder="big"
    )

    # gabungkan header + pesan
    data = header + message_bytes

    # ubah menjadi bit
    bits = bytes_to_bits(data)

    # kapasitas maksimum gambar
    capacity = len(pixels) * 3

    if len(bits) > capacity:
        max_bytes = (capacity - HEADER_SIZE * 8) // 8
        print("\n[ERROR] Pesan terlalu panjang!")
        print(f"Maksimal sekitar {max_bytes} byte.")

        return False

    # Pproses penyisipan lsb
    new_pixels = []
    bit_index = 0

    for pixel in pixels:
        r, g, b = pixel
        channels = [r, g, b]

        for i in range(3):
            if bit_index < len(bits):
                # hapus bit terakhir
                # kemudian masukkan bit pesan
                channels[i] = (
                    channels[i] & 0xFE
                ) | bits[bit_index]

                bit_index += 1

        new_pixels.append(tuple(channels))

    # membuat gambar baru
    stego_image = Image.new(
        "RGB",
        image.size
    )

    stego_image.putdata(new_pixels)

    # simpan gambar
    try:
        stego_image.save(output_image)

    except Exception as e:
        print(f"\n[ERROR] Gagal menyimpan gambar: {e}")

        return False

    # informasi hasil
    print("\n========================================")
    print("       ENCODE BERHASIL")
    print("========================================")
    print(f"Input gambar : {input_image}")
    print(f"Output gambar: {output_image}")
    print(f"Pesan        : {message}")
    print(f"Panjang pesan: {len(message_bytes)} byte")
    print("========================================")

    return True

# fungsi decode
def decode_image(input_image):
    """
    Mengambil pesan tersembunyi dari gambar.
    """

    try:
        image = Image.open(input_image).convert("RGB")

    except Exception as e:
        print(f"\n[ERROR] Gagal membuka gambar: {e}")

        return None

    pixels = list(image.getdata())

    # mengambil seluruh bit lsb
    bits = []

    for pixel in pixels:
        r, g, b = pixel

        bits.append(r & 1)
        bits.append(g & 1)
        bits.append(b & 1)

    # cek header
    if len(bits) < HEADER_SIZE * 8:
        print(
            "\n[ERROR] Gambar terlalu kecil "
            "atau tidak memiliki data steganografi."
        )

        return None

    # ambil header
    header_bits = bits[:HEADER_SIZE * 8]

    header = bits_to_bytes(header_bits)

    # periksa magic
    magic = header[:4]

    if magic != MAGIC:
        print("\n[ERROR] Tidak ditemukan pesan steganografi.")
        print("Gambar kemungkinan bukan hasil encode program ini.")

        return None

    # ambil panjang pesan
    message_length = int.from_bytes(
        header[4:8],
        byteorder="big"
    )

    # hitung jumlah bit pesan
    message_bits_length = message_length * 8

    start = HEADER_SIZE * 8

    end = start + message_bits_length

    # pastikan data cukup
    if end > len(bits):
        print("\n[ERROR] Data pesan tidak lengkap.")

        return None

    # ambil bit pesan
    message_bits = bits[start:end]

    # ubah kembali menjadi bytes
    message_bytes = bits_to_bytes(message_bits)

    # decode utf-8
    try:
        message = message_bytes.decode("utf-8")

    except UnicodeDecodeError:
        print("\n[ERROR] Pesan tidak dapat dibaca.")

        return None

    # tampilkan hasil
    print("\n========================================")
    print("       DECODE BERHASIL")
    print("========================================")
    print(f"Gambar       : {input_image}")
    print(f"Panjang pesan: {message_length} byte")
    print(f"Pesan        : {message}")
    print("========================================")

    return message


# fungsi untuk menemukan path file
def get_file_path(filename):
    """
    Menentukan lokasi file.

    Jika user memasukkan path absolut,
    gunakan path tersebut.

    Jika user hanya memasukkan nama file,
    cari file di folder tempat lsb_steg.py berada.
    """

    filename = filename.strip()

    # jika path absolut
    if os.path.isabs(filename):

        return filename

    # jika path relatif
    return os.path.join(BASE_DIR, filename)

# fugsi input encode
def menu_encode():
    print("\n========================================")
    print("              ENCODE PESAN")
    print("========================================")

    input_image = input(
        "Masukkan nama gambar asli : "
    ).strip()

    # tentukan lokasi gambar
    input_path = get_file_path(input_image)

    # cek apakah file benar-benar ada
    if not os.path.isfile(input_path):

        print("\n[ERROR] File gambar tidak ditemukan!")
        print(f"Dicari di: {input_path}")

        return

    # input pesan
    message = input(
        "Masukkan pesan rahasia    : "
    )

    if message == "":
        print("\n[ERROR] Pesan tidak boleh kosong!")

        return

    # input nama output
    output_image = input(
        "Nama gambar hasil (contoh: stego.png): "
    ).strip()

    if output_image == "":
        output_image = "stego.png"

    # tentukan lokasi output
    output_path = get_file_path(output_image)

    # encode
    encode_image(
        input_path,
        output_path,
        message
    )

# fungsi input encode
def menu_decode():
    print("\n========================================")
    print("              DECODE PESAN")
    print("========================================")

    input_image = input(
        "Masukkan nama gambar stego : "
    ).strip()

    # tentukan lokasi gambar
    input_path = get_file_path(input_image)

    # cek apakah file ada
    if not os.path.isfile(input_path):
        print("\n[ERROR] File gambar tidak ditemukan!")
        print(f"Dicari di: {input_path}")

        return

    # decode
    decode_image(input_path)

# Mmenu utama
def main_menu():
    while True:
        print("\n")
        print("========================================")
        print("       STEGANOGRAFI LSB IMAGE")
        print("========================================")
        print("  1. Encode / Sembunyikan Pesan")
        print("  2. Decode / Ambil Pesan")
        print("  3. Keluar")
        print("========================================")

        choice = input(
            "Pilih menu [1-3]: "
        ).strip()

        # menu 1 - encode
        if choice == "1":
            menu_encode()

        # menu 2 - decode
        elif choice == "2":
            menu_decode()

        # menu 3 - keluar
        elif choice == "3":
            print("\n========================================")
            print("Program selesai.")
            print("Terima kasih!")
            print("========================================")

            sys.exit()

        # input salah
        else:
            print("\n[ERROR] Pilihan tidak valid!")
            print("Silakan pilih menu 1, 2, atau 3.")

# program utama
if __name__ == "__main__":

    main_menu()
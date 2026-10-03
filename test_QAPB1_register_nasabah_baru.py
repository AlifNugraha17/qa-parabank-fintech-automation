"""
TIKET JIRA: QAPB-1
Summary: [Customer Onboarding] Verify successful new customer registration with complete personal profile
"""

import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


def test_QAPB1_register_nasabah_baru():
    print("\n=======================================================")
    print("🚀 MENJALANKAN TEST TIKET QAPB-1: Registrasi Nasabah Baru")
    print("=======================================================")

    opsi = Options()
    opsi.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=opsi)
    driver.implicitly_wait(5)

    try:
        driver.get("https://parabank.parasoft.com/parabank/register.htm")
        time.sleep(1.5)

        # Buat username unik otomatis agar tidak pernah ditolak karena username duplikat
        angka_acak = random.randint(1000, 9999)
        username_baru = f"alif_qa_{angka_acak}"
        password_baru = "RahasiaBank123!"

        print(f"👤 Mendaftarkan nasabah baru dengan Username: {username_baru}")

        # 1. Isi Formulir Pendaftaran Nasabah
        driver.find_element(By.ID, "customer.firstName").send_keys("Alif")
        driver.find_element(By.ID, "customer.lastName").send_keys("Nugraha")
        driver.find_element(By.ID, "customer.address.street").send_keys("Jl. Engku Putri No. 1")
        driver.find_element(By.ID, "customer.address.city").send_keys("Batam")
        driver.find_element(By.ID, "customer.address.state").send_keys("Kepulauan Riau")
        driver.find_element(By.ID, "customer.address.zipCode").send_keys("29461")
        driver.find_element(By.ID, "customer.phoneNumber").send_keys("081234567890")
        driver.find_element(By.ID, "customer.ssn").send_keys("987-65-4321")

        # 2. Isi Akun Login
        driver.find_element(By.ID, "customer.username").send_keys(username_baru)
        driver.find_element(By.ID, "customer.password").send_keys(password_baru)
        driver.find_element(By.ID, "repeatedPassword").send_keys(password_baru)
        time.sleep(1.5)

        # 3. Klik tombol Register
        driver.find_element(By.CSS_SELECTOR, "input[value='Register']").click()
        time.sleep(2)

        # 4. Validasi pesan sukses pembuatan akun bank
        pesan_sukses = driver.find_element(By.CSS_SELECTOR, "#rightPanel p").text
        assert "Your account was created successfully" in pesan_sukses
        print(f"\n✅ TEST PASSED: {pesan_sukses}")
        print(f"🎉 Nasabah '{username_baru}' berhasil terdaftar di ParaBank!")

        # Simpan username terakhir ke file teks agar bisa dipakai otomatis oleh test login berikutnya!
        with open("akun_nasabah_aktif.txt", "w", encoding="utf-8") as f:
            f.write(f"{username_baru},{password_baru}")

        time.sleep(4)  # Jeda 4 detik agar Anda leluasa melihat halaman dan mengambil screenshot sendiri!

    finally:
        driver.quit()


if __name__ == "__main__":
    test_QAPB1_register_nasabah_baru()

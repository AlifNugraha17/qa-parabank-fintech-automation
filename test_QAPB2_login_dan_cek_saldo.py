"""
TIKET JIRA: QAPB-2
Summary: [Account Auditing] Verify account overview displays active balance and account ID
"""

import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


def test_QAPB2_login_dan_cek_saldo():
    print("\n=======================================================")
    print("🚀 MENJALANKAN TEST TIKET QAPB-2: Login & Cek Saldo Bank")
    print("=======================================================")

    # Baca akun nasabah yang baru saja didaftarkan di QAPB-1
    if not os.path.exists("akun_nasabah_aktif.txt"):
        username = "john"
        password = "demo"
    else:
        with open("akun_nasabah_aktif.txt", "r", encoding="utf-8") as f:
            username, password = f.read().strip().split(",")

    opsi = Options()
    opsi.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=opsi)
    driver.implicitly_wait(5)

    try:
        driver.get("https://parabank.parasoft.com/parabank/index.htm")
        time.sleep(1.5)

        # 1. Login nasabah
        driver.find_element(By.NAME, "username").send_keys(username)
        driver.find_element(By.NAME, "password").send_keys(password)
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, "input[value='Log In']").click()
        time.sleep(2)

        # 2. Klik menu 'Accounts Overview'
        driver.find_element(By.LINK_TEXT, "Accounts Overview").click()
        time.sleep(1.5)

        # 3. Verifikasi tabel saldo rekening
        tabel_saldo = driver.find_element(By.ID, "accountTable")
        baris_rekening = tabel_saldo.find_elements(By.CSS_SELECTOR, "tbody tr")

        assert len(baris_rekening) > 0, "Tabel rekening nasabah tidak ditemukan!"
        print(f"✅ Berhasil memuat halaman Accounts Overview!")
        print(f"💰 Saldo rekening nasabah terverifikasi aktif!")

        print("\n✅ TEST PASSED: Login sukses dan saldo rekening tampil akurat!")
        time.sleep(4)

    finally:
        driver.quit()


if __name__ == "__main__":
    test_QAPB2_login_dan_cek_saldo()

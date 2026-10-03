"""
TIKET JIRA: QAPB-4
Summary: [Funds Transfer] Verify real-time fund transfer between customer accounts and balance debiting
"""

import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


def test_QAPB4_transfer_dana_berhasil():
    print("\n=======================================================")
    print("🚀 MENJALANKAN TEST TIKET QAPB-4: Transfer Dana Antar Rekening")
    print("=======================================================")

    if not os.path.exists("akun_nasabah_aktif.txt"):
        username, password = "john", "demo"
    else:
        with open("akun_nasabah_aktif.txt", "r", encoding="utf-8") as f:
            username, password = f.read().strip().split(",")

    opsi = Options()
    opsi.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=opsi)
    driver.implicitly_wait(5)

    try:
        driver.get("https://parabank.parasoft.com/parabank/index.htm")
        driver.find_element(By.NAME, "username").send_keys(username)
        driver.find_element(By.NAME, "password").send_keys(password)
        driver.find_element(By.CSS_SELECTOR, "input[value='Log In']").click()
        time.sleep(1.5)

        # 1. Klik menu 'Transfer Funds'
        driver.find_element(By.LINK_TEXT, "Transfer Funds").click()
        time.sleep(1.5)

        # 2. Masukkan nominal transfer: $50
        nominal = "50"
        driver.find_element(By.ID, "amount").send_keys(nominal)
        time.sleep(1)

        # 3. Klik tombol 'Transfer'
        driver.find_element(By.CSS_SELECTOR, "input[value='Transfer']").click()
        time.sleep(2)

        # 4. Validasi judul 'Transfer Complete!'
        judul_sukses = driver.find_element(By.CSS_SELECTOR, "#showResult h1").text
        assert "Transfer Complete!" in judul_sukses
        print(f"\n✅ TEST PASSED: {judul_sukses}")
        print(f"💸 Sukses mentransfer dana sebesar ${nominal} ke rekening tujuan!")

        time.sleep(4)

    finally:
        driver.quit()


if __name__ == "__main__":
    test_QAPB4_transfer_dana_berhasil()

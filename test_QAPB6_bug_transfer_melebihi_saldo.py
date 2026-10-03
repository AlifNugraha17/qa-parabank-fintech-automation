"""
TIKET JIRA: QAPB-6 (BUG DEFECT)
Summary: [Transaction Boundary Bug] System permits negative / zero fund transfer amount without error validation
"""

import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


def test_QAPB6_bug_transfer_negatif():
    print("\n=======================================================")
    print("🚀 MENJALANKAN TEST TIKET QAPB-6: Bug Transfer Nominal Negatif")
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

        # 1. Buka menu Transfer Funds
        driver.find_element(By.LINK_TEXT, "Transfer Funds").click()
        time.sleep(1.5)

        # 2. Coba transfer nominal tidak masuk akal: -$500 atau 0
        driver.find_element(By.ID, "amount").send_keys("-500")
        time.sleep(1)

        # 3. Klik Transfer
        driver.find_element(By.CSS_SELECTOR, "input[value='Transfer']").click()
        time.sleep(2)

        # Sistem perbankan yang aman SEHARUSNYA menolak angka minus (harus ada error validation)!
        # Tapi di ParaBank, transfer ini malah berhasil diproses!
        judul_hasil = driver.find_element(By.CSS_SELECTOR, "#showResult h1").text

        assert "Transfer Complete!" not in judul_hasil, (
            "[BUG FINTECH TERDETEKSI OTOMATIS OLEH PYTHON!] "
            "Sistem perbankan berhasil meloloskan transfer nominal negatif (-$500)! "
            "Seharusnya sistem memvalidasi dan menolak transaksi!"
        )

    finally:
        time.sleep(4)
        driver.quit()


if __name__ == "__main__":
    test_QAPB6_bug_transfer_negatif()

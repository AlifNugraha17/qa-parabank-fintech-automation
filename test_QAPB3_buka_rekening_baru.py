"""
TIKET JIRA: QAPB-3
Summary: [Open Account] Verify opening a new secondary Savings account funded from existing balance
"""

import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select


def test_QAPB3_buka_rekening_baru():
    print("\n=======================================================")
    print("🚀 MENJALANKAN TEST TIKET QAPB-3: Buka Rekening Tabungan Baru")
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

        # 1. Klik menu 'Open New Account'
        driver.find_element(By.LINK_TEXT, "Open New Account").click()
        time.sleep(1.5)

        # 2. Pilih tipe rekening: SAVINGS
        tipe_rekening = Select(driver.find_element(By.ID, "type"))
        tipe_rekening.select_by_visible_text("SAVINGS")
        time.sleep(1)

        # 3. Klik tombol 'Open New Account'
        driver.find_element(By.CSS_SELECTOR, "input[value='Open New Account']").click()
        time.sleep(2)

        # 4. Validasi pesan sukses & nomor rekening baru
        pesan_sukses = driver.find_element(By.CSS_SELECTOR, "#openAccountResult p").text
        nomor_rekening_baru = driver.find_element(By.ID, "newAccountId").text

        assert "Congratulations, your account is now open" in pesan_sukses
        print(f"\n✅ TEST PASSED: {pesan_sukses}")
        print(f"🏦 Nomor Rekening Tabungan Baru yang Terbit: {nomor_rekening_baru}")

        time.sleep(4)

    finally:
        driver.quit()


if __name__ == "__main__":
    test_QAPB3_buka_rekening_baru()

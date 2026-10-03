"""
TIKET JIRA: QAPB-8 (BUG DEFECT)
Summary: [KYC Profile Integrity] Update Profile service accepts empty/blank mandatory fields without validation
"""

import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


def test_QAPB8_bug_update_profile_blank():
    print("\n=======================================================")
    print("🚀 MENJALANKAN TEST TIKET QAPB-8: Bug Update Profile Kosong")
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

        # 1. Buka menu Update Contact Info
        driver.find_element(By.LINK_TEXT, "Update Contact Info").click()
        time.sleep(1.5)

        # 2. Kosongkan field wajib Nama Depan dan Nomor HP (menghilangkan identitas nasabah)
        first_name_input = driver.find_element(By.ID, "customer.firstName")
        phone_input = driver.find_element(By.ID, "customer.phoneNumber")

        first_name_input.clear()
        phone_input.clear()
        time.sleep(1)

        # 3. Klik tombol Update Profile
        driver.find_element(By.CSS_SELECTOR, "input[value='Update Profile']").click()
        time.sleep(2)

        # 4. Validasi respon sistem
        # Aturan KYC Perbankan: Nama nasabah WAJIB ada (tidak boleh kosong)!
        # Jika sistem meloloskan nama kosong dan menampilkan "Profile Updated", maka ini BUG!
        teks_hasil = driver.find_element(By.CSS_SELECTOR, "#updateProfileResult").text

        assert "Profile Updated" not in teks_hasil, (
            "[BUG KYC INTEGRITY DITEMUKAN!] "
            "Sistem perbankan mengizinkan nasabah mengupdate profil dengan nama kosong/blank! "
            "Menyebabkan data nasabah di core banking hilang / terkorupsi."
        )

    finally:
        time.sleep(4)
        driver.quit()


if __name__ == "__main__":
    test_QAPB8_bug_update_profile_blank()

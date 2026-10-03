"""
TIKET JIRA: QAPB-5
Summary: [Loan Underwriting] Verify loan application submission and automated credit approval
"""

import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


def test_QAPB5_pengajuan_pinjaman_loan():
    print("\n=======================================================")
    print("🚀 MENJALANKAN TEST TIKET QAPB-5: Pengajuan Pinjaman Bank (Loan)")
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

        # 1. Klik menu 'Request Loan'
        driver.find_element(By.LINK_TEXT, "Request Loan").click()
        time.sleep(1.5)

        # 2. Masukkan jumlah pinjaman yang wajar ($1000) dan uang muka DP ($200)
        driver.find_element(By.ID, "amount").send_keys("1000")
        driver.find_element(By.ID, "downPayment").send_keys("200")
        time.sleep(1)

        # 3. Klik tombol 'Apply Now'
        driver.find_element(By.CSS_SELECTOR, "input[value='Apply Now']").click()
        time.sleep(2)

        # 4. Validasi status pinjaman: 'Approved'
        status_pinjaman = driver.find_element(By.ID, "loanStatus").text
        assert status_pinjaman == "Approved"
        print(f"\n✅ TEST PASSED: Status Pengajuan Pinjaman: {status_pinjaman}")
        print("🎉 Bank ParaBank menyetujui pinjaman nasabah (Credit Score Lolos)!")

        time.sleep(4)

    finally:
        driver.quit()


if __name__ == "__main__":
    test_QAPB5_pengajuan_pinjaman_loan()

"""
TIKET JIRA: QAPB-9 (BUG DEFECT)
Summary: [Bill Pay Payment Integrity] System allows bill payment with $0.00 and negative amount values
"""

import os
import sys
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


def test_QAPB9_bug_billpay_nominal_negatif():
    print("\n=======================================================")
    print("🚀 MENJALANKAN TEST TIKET QAPB-9: Bug Bill Pay Nominal Negatif")
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

        # Fallback login jika akun custom sesi sebelumnya telah kedaluwarsa di server demo
        if len(driver.find_elements(By.LINK_TEXT, "Bill Pay")) == 0:
            driver.get("https://parabank.parasoft.com/parabank/index.htm")
            driver.find_element(By.NAME, "username").send_keys("john")
            driver.find_element(By.NAME, "password").send_keys("demo")
            driver.find_element(By.CSS_SELECTOR, "input[value='Log In']").click()
            time.sleep(1.5)

        # 1. Buka menu Bill Pay
        driver.find_element(By.LINK_TEXT, "Bill Pay").click()
        time.sleep(1.5)

        # 2. Isi data tagihan (Payee Information)
        driver.find_element(By.NAME, "payee.name").send_keys("PLN Electricity")
        driver.find_element(By.NAME, "payee.address.street").send_keys("Jl. Sudirman No. 10")
        driver.find_element(By.NAME, "payee.address.city").send_keys("Batam")
        driver.find_element(By.NAME, "payee.address.state").send_keys("Kepri")
        driver.find_element(By.NAME, "payee.address.zipCode").send_keys("29400")
        driver.find_element(By.NAME, "payee.phoneNumber").send_keys("08123456789")
        driver.find_element(By.NAME, "payee.accountNumber").send_keys("888999")
        driver.find_element(By.NAME, "verifyAccount").send_keys("888999")

        # 3. Masukkan nominal tagihan minus (-$75.00)
        nominal_bug = "-75"
        driver.find_element(By.NAME, "amount").send_keys(nominal_bug)
        time.sleep(1)

        # 4. Klik tombol Send Payment
        driver.find_element(By.CSS_SELECTOR, "input[value='Send Payment']").click()
        time.sleep(2)

        # 5. Cek apakah transaksi tagihan minus berhasil diproses
        hasil_pembayaran = driver.find_element(By.ID, "billpayResult").text
        print("\n🔍 HASIL YANG DITAMPILKAN DI LAYAR:")
        print(hasil_pembayaran)

        assert "Bill Payment Complete" not in hasil_pembayaran, (
            "[CRITICAL FINANCIAL BUG DITEMUKAN!] "
            "Sistem Bill Pay meloloskan pembayaran tagihan dengan nominal negatif (-$75)! "
            "Seharusnya sistem memvalidasi dan memblokir nominal <= 0."
        )

    finally:
        time.sleep(4)
        driver.quit()


if __name__ == "__main__":
    test_QAPB9_bug_billpay_nominal_negatif()

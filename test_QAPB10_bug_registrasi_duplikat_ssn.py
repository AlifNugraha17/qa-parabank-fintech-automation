"""
TIKET JIRA: QAPB-10 (BUG DEFECT)
Summary: [Identity Theft / AML Risk] System accepts duplicate Social Security Number (SSN) during onboarding
"""

import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


def test_QAPB10_bug_registrasi_duplikat_ssn():
    print("\n=======================================================")
    print("🚀 MENJALANKAN TEST TIKET QAPB-10: Bug Duplikasi SSN Nasabah")
    print("=======================================================")

    opsi = Options()
    opsi.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=opsi)
    driver.implicitly_wait(5)

    try:
        driver.get("https://parabank.parasoft.com/parabank/register.htm")
        time.sleep(1.5)

        # Buat username acak baru
        angka_acak = random.randint(1000, 9999)
        username_baru = f"nasabah_kloning_{angka_acak}"
        # Gunakan nomor identitas SSN yang sama persis (SSN duplikat)
        ssn_duplikat = "987-65-4321"

        print(f"👤 Mendaftarkan nasabah baru dengan SSN yang sudah ada: {ssn_duplikat}")

        # 1. Isi Formulir Pendaftaran dengan SSN duplikat
        driver.find_element(By.ID, "customer.firstName").send_keys("Budi")
        driver.find_element(By.ID, "customer.lastName").send_keys("Santoso")
        driver.find_element(By.ID, "customer.address.street").send_keys("Jl. Kloning No. 99")
        driver.find_element(By.ID, "customer.address.city").send_keys("Jakarta")
        driver.find_element(By.ID, "customer.address.state").send_keys("DKI Jakarta")
        driver.find_element(By.ID, "customer.address.zipCode").send_keys("10110")
        driver.find_element(By.ID, "customer.phoneNumber").send_keys("089988776655")
        driver.find_element(By.ID, "customer.ssn").send_keys(ssn_duplikat)

        driver.find_element(By.ID, "customer.username").send_keys(username_baru)
        driver.find_element(By.ID, "customer.password").send_keys("PasswordKloning123!")
        driver.find_element(By.ID, "repeatedPassword").send_keys("PasswordKloning123!")
        time.sleep(1)

        # 2. Klik tombol Register
        driver.find_element(By.CSS_SELECTOR, "input[value='Register']").click()
        time.sleep(2)

        # 3. Validasi respon sistem
        # Regulasi AML & Perbankan: 1 nomor KTP/SSN hanya boleh memiliki 1 CIF (Customer Identification File).
        # Sistem perbankan harus menolak jika SSN sudah terdaftar di sistem.
        pesan_respon = driver.find_element(By.ID, "rightPanel").text

        assert "Your account was created successfully" not in pesan_respon, (
            "[CRITICAL REGULATORY BUG DITEMUKAN!] "
            f"Sistem perbankan meloloskan registrasi nasabah dengan nomor SSN duplikat ({ssn_duplikat})! "
            "Rentan terhadap Identity Theft dan pencucian uang (Anti-Money Laundering non-compliance)."
        )

    finally:
        time.sleep(4)
        driver.quit()


if __name__ == "__main__":
    test_QAPB10_bug_registrasi_duplikat_ssn()

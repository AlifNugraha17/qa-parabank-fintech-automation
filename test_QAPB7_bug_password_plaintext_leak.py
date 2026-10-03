"""
TIKET JIRA: QAPB-7 (BUG DEFECT)
Summary: [Security / Data Leak] Plaintext password exposure in Customer Lookup recovery module
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


def test_QAPB7_bug_password_plaintext_leak():
    print("\n=======================================================")
    print("🚀 MENJALANKAN TEST TIKET QAPB-7: Bug Plaintext Password Leak")
    print("=======================================================")

    opsi = Options()
    opsi.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=opsi)
    driver.implicitly_wait(5)

    try:
        driver.get("https://parabank.parasoft.com/parabank/lookup.htm")
        time.sleep(1.5)

        # 1. Isi form Forgot Login Info dengan identitas nasabah
        driver.find_element(By.ID, "firstName").send_keys("Alif")
        driver.find_element(By.ID, "lastName").send_keys("Nugraha")
        driver.find_element(By.ID, "address.street").send_keys("Jl. Engku Putri No. 1")
        driver.find_element(By.ID, "address.city").send_keys("Batam")
        driver.find_element(By.ID, "address.state").send_keys("Kepulauan Riau")
        driver.find_element(By.ID, "address.zipCode").send_keys("29461")
        driver.find_element(By.ID, "ssn").send_keys("987-65-4321")
        time.sleep(1)

        # 2. Klik tombol "Find My Login Info"
        driver.find_element(By.CSS_SELECTOR, "input[value='Find My Login Info']").click()
        time.sleep(2)

        # 3. Cek hasil yang ditampilkan di layar
        teks_hasil = driver.find_element(By.ID, "rightPanel").text

        # STANDAR KEAMANAN PERBANKAN INTERNASIONAL (PCI-DSS & OWASP):
        # Password TIDAK BOLEH PERNAH ditampilkan dalam bentuk plaintext langsung di layar publik!
        # Harus melalui reset token link via Email/SMS OTP.
        assert "Password:" not in teks_hasil, (
            "[CRITICAL SECURITY BUG DITEMUKAN!] "
            "Sistem perbankan menampilkan plaintext password langsung di layar hasil pencarian! "
            "Melanggar standar keamanan PCI-DSS & OWASP Sensitive Data Exposure!"
        )

    finally:
        time.sleep(4)
        driver.quit()


if __name__ == "__main__":
    test_QAPB7_bug_password_plaintext_leak()

"""
TIKET JIRA: QAPB-8 (BUG DEFECT)
Summary: [KYC Profile Integrity] Update Profile service accepts empty/blank mandatory fields without validation
"""

import sys
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


def test_QAPB8_bug_update_profile_blank():
    print("\n=======================================================")
    print("🚀 MENJALANKAN TEST TIKET QAPB-8: Bug Update Profil Nomor HP Kosong")
    print("=======================================================")

    opsi = Options()
    opsi.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=opsi)
    driver.implicitly_wait(5)

    try:
        # 1. Daftarkan nasabah baru agar data profil bersih (tidak terpengaruh akun demo bersama)
        driver.get("https://parabank.parasoft.com/parabank/register.htm")
        username_baru = f"alif_kyc_{random.randint(10000, 99999)}"
        driver.find_element(By.ID, "customer.firstName").send_keys("Alif")
        driver.find_element(By.ID, "customer.lastName").send_keys("Nugraha")
        driver.find_element(By.ID, "customer.address.street").send_keys("Jl. Engku Putri No. 1")
        driver.find_element(By.ID, "customer.address.city").send_keys("Batam")
        driver.find_element(By.ID, "customer.address.state").send_keys("Kepulauan Riau")
        driver.find_element(By.ID, "customer.address.zipCode").send_keys("29461")
        driver.find_element(By.ID, "customer.phoneNumber").send_keys("081234567890")
        driver.find_element(By.ID, "customer.ssn").send_keys("987654321")
        driver.find_element(By.ID, "customer.username").send_keys(username_baru)
        driver.find_element(By.ID, "customer.password").send_keys("RahasiaBank123!")
        driver.find_element(By.ID, "repeatedPassword").send_keys("RahasiaBank123!")
        driver.find_element(By.CSS_SELECTOR, "input[value='Register']").click()
        time.sleep(2)
        print(f"👤 Nasabah baru terdaftar & login: {username_baru}")

        # 2. Buka menu Update Contact Info
        driver.find_element(By.LINK_TEXT, "Update Contact Info").click()

        # 3. Tunggu sampai data profil nasabah selesai dimuat (form diisi via AJAX)
        WebDriverWait(driver, 10).until(
            lambda d: d.find_element(By.ID, "customer.phoneNumber").get_attribute("value") != ""
        )
        time.sleep(1.5)

        # 4. Kosongkan field wajib Phone # (nomor HP nasabah)
        phone_input = driver.find_element(By.ID, "customer.phoneNumber")
        print(f"📞 Nomor HP sebelum dihapus: {phone_input.get_attribute('value')}")
        phone_input.clear()
        time.sleep(1.5)

        # 5. Klik tombol Update Profile
        driver.find_element(By.CSS_SELECTOR, "input[value='Update Profile']").click()
        time.sleep(3)

        # 6. Validasi respon sistem
        teks_hasil = driver.find_element(By.ID, "rightPanel").text
        print("\n🔍 HASIL YANG DITAMPILKAN DI LAYAR:")
        print(teks_hasil)

        # Aturan KYC Perbankan: Nomor HP nasabah WAJIB diisi.
        # Sistem SEHARUSNYA menolak dengan pesan "Phone number is required."
        assert "Profile Updated" not in teks_hasil, (
            "[BUG KYC INTEGRITY DITEMUKAN!] "
            "Sistem perbankan menerima update profil dengan nomor HP KOSONG dan menampilkan 'Profile Updated'! "
            "Data kontak nasabah di core banking terhapus tanpa validasi."
        )
        assert "An internal error has occurred" not in teks_hasil, (
            "[BUG BACKEND DITEMUKAN!] "
            "Server crash (internal error) saat nomor HP dikosongkan, bukan menampilkan validasi form."
        )

    finally:
        time.sleep(4)
        driver.quit()


if __name__ == "__main__":
    test_QAPB8_bug_update_profile_blank()

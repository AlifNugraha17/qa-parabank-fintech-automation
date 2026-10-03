# 🏦 ParaBank - Full-Cycle Fintech & Banking QA Automation Suite

![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python)
![Selenium](https://img.shields.io/badge/Selenium-WebDriver-green?logo=selenium)
![Pytest](https://img.shields.io/badge/Pytest-Test_Framework-yellow?logo=pytest)
![Jira](https://img.shields.io/badge/Jira-Atlassian-0052CC?logo=jira)
![Fintech](https://img.shields.io/badge/Domain-Fintech_Banking-00A86B?logo=bank)

An automated web testing and quality assurance suite targeting **[ParaBank (Parasoft)](https://parabank.parasoft.com/parabank/index.htm)**—the world's premier online banking and financial services simulation platform designed for QA Engineers.

---

## 📌 Jira Requirements Traceability Matrix (RTM)

| Jira ID | Banking Module | Test Scenario & Summary | Issue Type | Test Script |
| :--- | :--- | :--- | :--- | :--- |
| **QAPB-1** | Customer Onboarding | Verify successful new customer registration with complete personal profile | `Task` | `test_QAPB1_register_nasabah_baru.py` |
| **QAPB-2** | Account Auditing | Verify account overview displays active balance and account ID | `Task` | `test_QAPB2_login_dan_cek_saldo.py` |
| **QAPB-3** | Open Account | Verify opening a new secondary Savings account funded from existing balance | `Task` | `test_QAPB3_buka_rekening_baru.py` |
| **QAPB-4** | Funds Transfer | Verify real-time fund transfer between customer accounts and balance debiting | `Task` | `test_QAPB4_transfer_dana_berhasil.py` |
| **QAPB-5** | Loan Underwriting | Verify loan application submission and automated credit approval | `Task` | `test_QAPB5_pengajuan_pinjaman_loan.py` |
| **QAPB-6** | Transaction Security | System permits negative / zero fund transfer amount without error validation | `Bug` 🔴 | `test_QAPB6_bug_transfer_melebihi_saldo.py` |
| **QAPB-7** | Security / Auth | Plaintext password exposure in Customer Lookup recovery module | `Bug` 🔴 | `test_QAPB7_bug_password_plaintext_leak.py` |
| **QAPB-8** | KYC Compliance | Update Profile service accepts empty/blank mandatory fields without validation | `Bug` 🔴 | `test_QAPB8_bug_update_profile_blank_fields.py` |
| **QAPB-9** | Payment Integrity | System allows bill payment with $0.00 and negative amount values | `Bug` 🔴 | `test_QAPB9_bug_billpay_nominal_negatif.py` |
| **QAPB-10** | Anti-Money Laundering | System accepts duplicate Social Security Number (SSN) during onboarding | `Bug` 🔴 | `test_QAPB10_bug_registrasi_duplikat_ssn.py` |

---


## 🚀 How to Run the Tests

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Individual Ticket Tests
```bash
# Example: Customer Registration
python test_QAPB1_register_nasabah_baru.py

# Example: Account Overview & Balance Check
python test_QAPB2_login_dan_cek_saldo.py

# Example: Fund Transfer
python test_QAPB4_transfer_dana_berhasil.py
```

### 3. Run Entire Suite via Pytest
```bash
pytest test_*.py -v
```

---

## 👤 Author
- **Alif Nugraha**
- GitHub: [@AlifNugraha17](https://github.com/AlifNugraha17)
- Quality Assurance | Test Automation | Python | Selenium WebDriver | Jira Software | Fintech Banking

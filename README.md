# Automated API Security & DevSecOps Pipeline

This project was built to demonstrate practical Application Security, Security Automation, and DevSecOps skills, specifically aligning with the requirements for Information Security engineering roles.

## 🎯 Project Overview
This repository contains a complete DevSecOps ecosystem:
1. **The Target:** A mock financial/lending REST API built in Python (FastAPI) containing intentional vulnerabilities.
2. **Custom Detections:** Custom-written Semgrep (SAST) rules and Nuclei (DAST) templates designed to catch the specific vulnerabilities in the API.
3. **Security Automation:** A Python script (`sec_scanner.py`) that orchestrates the execution of these security tools and parses their outputs.
4. **CI/CD Pipeline:** A GitHub Actions workflow that automatically runs Dependency Scanning (SCA), SAST, and DAST on every code push.

## 🚨 Included Vulnerabilities (OWASP Top 10)
- **Broken Object Level Authorization (BOLA/IDOR):** An authenticated user can fetch loan details of other users by manipulating the `user_id` parameter.
- **Hardcoded Secrets:** The JWT signing key is hardcoded directly into the source code.
- **Vulnerable Dependencies:** The project intentionally uses an outdated, vulnerable version of `PyJWT`.

## ⚙️ How the DevSecOps Pipeline Works
You do not need to run this project locally to see it work! The security checks are completely automated via GitHub Actions.

If you check the **[Actions tab](../../actions)** in this repository, you will see the automated pipeline:
1. **SCA:** `safety check` scans `requirements.txt` and flags the outdated `PyJWT` library.
2. **SAST:** `semgrep` runs the custom rule (`rules/semgrep/fastapi-hardcoded-secret.yaml`) against the codebase and flags the hardcoded JWT secret.
3. **DAST:** The pipeline spins up the API in a staging environment and runs `nuclei` with a custom template (`rules/nuclei/api-bola-test.yaml`) to actively exploit the BOLA vulnerability.

## 🛠️ Testing it Locally (Optional)
If you wish to run the automation tool locally:
```bash
# 1. Install dependencies
pip install -r app/requirements.txt
pip install -r requirements.txt
pip install semgrep
brew install nuclei # (Mac) or standard Go install

# 2. Start the API in the background
cd app && uvicorn main:app --port 8000 &

# 3. Run the automated scanner
cd ..
./sec_scanner.py
```

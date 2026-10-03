# Moneyview Info-Sec Project: Automated API Security & DevSecOps

This project is built to demonstrate the skills required for the Information Security Intern role at Moneyview.

## Project Structure

- `app/`: A vulnerable FastAPI application representing a lending platform backend.
- `rules/semgrep/`: Custom SAST rules to find vulnerabilities in the source code (e.g., hardcoded secrets).
- `rules/nuclei/`: Custom DAST templates to find runtime vulnerabilities (e.g., BOLA).
- `.github/workflows/`: A simulated DevSecOps pipeline using GitHub Actions.
- `sec_scanner.py`: A Python automation script that orchestrates the security scans.

## How to run locally

1. **Install dependencies**:
   ```bash
   pip install -r app/requirements.txt
   pip install -r requirements.txt
   ```

2. **Start the Vulnerable API**:
   ```bash
   cd app
   uvicorn main:app --reload --port 8000
   ```
   *The API will be available at http://127.0.0.1:8000. You can view the swagger docs at http://127.0.0.1:8000/docs.*

3. **Run the Security Automation Scanner**:
   Open a new terminal window in the root of the project and ensure you have `semgrep` and `nuclei` installed:
   ```bash
   pip install semgrep
   # For nuclei, see: https://docs.projectdiscovery.io/tools/nuclei/install
   ```

   Run the scanner:
   ```bash
   ./sec_scanner.py
   ```

   The scanner will automatically run Semgrep against the `app/` code, and then run Nuclei against the running API.

## Pushing to GitHub

If you initialize this as a git repository and push it to GitHub, the `.github/workflows/devsecops.yml` will automatically trigger, demonstrating a DevSecOps CI/CD pipeline!

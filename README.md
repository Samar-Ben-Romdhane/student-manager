
---

## 🔒 Sécurité — CVE détectées et corrigées

| CVE | Package | Avant | Après | Détecté par |
|-----|---------|-------|-------|-------------|
| CVE-2024-6221  | Flask-Cors | 4.0.1 | 4.0.2  | Trivy (CI/CD) |
| CVE-2026-32597 | PyJWT      | 2.9.0 | 2.13.0 | Trivy (CI/CD) |
| CVE-2026-48526 | PyJWT      | 2.9.0 | 2.13.0 | Trivy (CI/CD) |

> CVE détectées automatiquement par Trivy dans le pipeline GitHub Actions et corrigées
> par mise à jour des dépendances. Les CVE système Alpine (OS-level) sont documentées
> dans `.trivyignore` en attente de patches upstream.

## 🚀 CI/CD Pipeline

![CI/CD](https://github.com/Samar-Ben-Romdhane/student-manager/actions/workflows/ci-cd.yml/badge.svg)

| Étape | Outil | Rôle |
|-------|-------|------|
| Lint | flake8 | Qualité du code Python |
| Tests | pytest | 7 tests unitaires/API |
| SAST | Bandit | Analyse statique sécurité |
| Scan images | Trivy | Détection CVE dans les images Docker |
| Registry | DockerHub | Push automatique des images |

---

## 🔒 Sécurité — CVE détectées et corrigées

| CVE | Package | Avant | Après | Détecté par |
|-----|---------|-------|-------|-------------|
| CVE-2024-6221  | Flask-Cors | 4.0.1 | 4.0.2  | Trivy (CI/CD) |
| CVE-2026-32597 | PyJWT      | 2.9.0 | 2.13.0 | Trivy (CI/CD) |
| CVE-2026-48526 | PyJWT      | 2.9.0 | 2.13.0 | Trivy (CI/CD) |

> CVE détectées automatiquement par Trivy dans le pipeline GitHub Actions et corrigées
> par mise à jour des dépendances. Les CVE système Alpine (OS-level) sont documentées
> dans `.trivyignore` en attente de patches upstream.

## 🚀 CI/CD Pipeline

![CI/CD](https://github.com/Samar-Ben-Romdhane/student-manager/actions/workflows/ci-cd.yml/badge.svg)

| Étape | Outil | Rôle |
|-------|-------|------|
| Lint | flake8 | Qualité du code Python |
| Tests | pytest | 7 tests unitaires/API |
| SAST | Bandit | Analyse statique sécurité |
| Scan images | Trivy | Détection CVE dans les images Docker |
| Registry | DockerHub | Push automatique des images |

#!/bin/bash
# ── Script d'initialisation Git Flow ─────────────────────────────────────────
# Usage : chmod +x git-init.sh && ./git-init.sh

set -e

echo "🌿 Initialisation du dépôt Git..."
git init
git add .
git commit -m "chore: initial project structure — 3-tier student manager"

echo "🌿 Création de la branche develop..."
git checkout -b develop
git commit --allow-empty -m "chore: initialize develop branch"

echo "🌿 Simulation feature/add-student-crud..."
git checkout -b feature/add-student-crud
git commit --allow-empty -m "feat(backend): add student model and CRUD endpoints"
git commit --allow-empty -m "feat(frontend): add student form and table UI"
git checkout develop
git merge --no-ff feature/add-student-crud -m "merge: feature/add-student-crud → develop"
git branch -d feature/add-student-crud

echo "🌿 Simulation feature/add-stats..."
git checkout -b feature/add-stats
git commit --allow-empty -m "feat(backend): add stats endpoint (total, filiere, niveau)"
git commit --allow-empty -m "feat(frontend): display stats cards and level breakdown"
git checkout develop
git merge --no-ff feature/add-stats -m "merge: feature/add-stats → develop"
git branch -d feature/add-stats

echo "🌿 Merge develop → main (release v1.0.0)..."
git checkout main
git merge --no-ff develop -m "release: v1.0.0 — initial release"
git tag -a v1.0.0 -m "Version 1.0.0 — Student Manager"

echo ""
echo "✅ Git Flow initialisé avec succès !"
echo ""
git log --oneline --graph --all
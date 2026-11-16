#!/usr/bin/env bash
# Regenera el sitio y lo publica en la rama gh-pages.
# Uso:
#   ./deploy.sh            # publica indexable (dominio .eu ya activo)
#   ./deploy.sh --preview  # publica con noindex (vista previa en github.io)
set -euo pipefail
cd "$(dirname "$0")"

if [[ "${1:-}" == "--preview" ]]; then
  NOINDEX=1 BASE_PATH=/observatorio-ia python3 build.py
else
  python3 build.py
fi

BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [[ "$BRANCH" != "master" ]]; then
  echo "Cambia a master antes de publicar (estás en $BRANCH)"; exit 1
fi

git add -A && git commit -qm "build: $(date -u +%Y-%m-%dT%H:%MZ)" || true
git checkout -q --orphan gh-pages-deploy
git rm -rf . -q
cp -r site/. .
rm -rf site
touch .nojekyll
git add -A
git commit -qm "Deploy $(date -u +%Y-%m-%dT%H:%MZ)"
git branch -f gh-pages HEAD
git push -q -f origin gh-pages
git checkout -q master
git branch -qD gh-pages-deploy
echo "Publicado en https://caseroclaw.github.io/observatorio-ia/"

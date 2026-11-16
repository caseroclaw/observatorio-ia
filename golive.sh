#!/usr/bin/env bash
# Puesta en marcha del subdominio del directorio. Idempotente.
#
# Arquitectura elegida: el ápice plataformaia.eu sigue haciendo 308 → plataformaia.com
# (no se toca nada del .com ni del servidor). El directorio vive en
# observatorio.plataformaia.eu.
#
# Requisito previo (solo el dueño, 1 registro en dondominio):
#   CNAME  observatorio  →  caseroclaw.github.io
#
# Uso: ./golive.sh            publica y verifica
#      ./golive.sh --check    solo comprueba DNS, no publica
set -euo pipefail
cd "$(dirname "$0")"
DOMAIN="observatorio.plataformaia.eu"
APEX="plataformaia.eu"
REPO="caseroclaw/observatorio-ia"
TARGET="caseroclaw.github.io"

echo "== 1. DNS del subdominio =="
cname=$(dig +short "$DOMAIN" CNAME | tr -d ' ' | sed 's/\.$//')
ips=$(dig +short "$DOMAIN" A | tr '\n' ' ')
echo "CNAME: ${cname:-<ninguno>}  |  A: ${ips:-<ninguno>}"
if [[ "$cname" != "$TARGET" ]]; then
  echo "BLOQUEADO: falta el CNAME observatorio → $TARGET en la zona de $APEX."
  echo "En dondominio: Campo 'observatorio' · Tipo CNAME · Valor '$TARGET'. Luego repite."
  exit 1
fi

echo "== 2. El ápice sigue redirigiendo (informativo, no se toca) =="
echo "https://$APEX → HTTP $(curl -s -o /dev/null -w '%{http_code}' --max-time 15 "https://$APEX" || echo 000)"

if [[ "${1:-}" == "--check" ]]; then echo "Comprobación OK. Nada publicado."; exit 0; fi

echo "== 3. Build indexable (sin noindex, sin BASE_PATH) =="
python3 build.py
printf '%s\n' "$DOMAIN" > site/CNAME

echo "== 4. Publicar gh-pages =="
git add -A && git commit -qm "Go-live: $DOMAIN" || true
git checkout -q --orphan gh-pages-golive
git rm -rf . -q
cp -r site/. .
rm -rf site
touch .nojekyll
printf '%s\n' "$DOMAIN" > CNAME
git add -A
git commit -qm "Go-live $(date -u +%Y-%m-%dT%H:%MZ)"
git branch -f gh-pages HEAD
git push -q -f origin gh-pages
git checkout -q master
git branch -qD gh-pages-golive

echo "== 5. Dominio en GitHub Pages + HTTPS =="
gh api -X PUT "repos/$REPO/pages" -f "cname=$DOMAIN" >/dev/null
gh api -X PUT "repos/$REPO/pages" -F "https_enforced=true" >/dev/null || true

echo "== 6. Verificación =="
for i in 1 2 3 4 5 6; do
  sleep 20
  st=$(gh api "repos/$REPO/pages" --jq '.status' 2>/dev/null || echo "?")
  echo "estado pages: $st"
  [[ "$st" == "built" ]] && break
done
for u in "/" "/agencias-ia-madrid/" "/precios-agencias-ia/"; do
  printf '%s  ' "$(curl -s -o /dev/null -w '%{http_code}' --max-time 20 "https://$DOMAIN$u")"
  echo "https://$DOMAIN$u"
done
echo "-- robots.txt --"; curl -s --max-time 15 "https://$DOMAIN/robots.txt"
echo "-- meta robots (no debe aparecer) --"
curl -s --max-time 15 "https://$DOMAIN/" | grep -o '<meta name="robots"[^>]*>' || echo "ok: sin noindex"
echo "-- http → https --"; curl -s -o /dev/null -w "%{http_code}\n" --max-time 15 "http://$DOMAIN/"
echo
echo "Siguiente: Search Console → propiedad de dominio '$APEX' (TXT en DNS, cubre subdominios)"
echo "o prefijo de URL https://$DOMAIN/ , y enviar el sitemap."

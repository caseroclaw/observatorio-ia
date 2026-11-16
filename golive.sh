#!/usr/bin/env bash
# Puesta en marcha del dominio propio. Idempotente: se puede repetir.
# Requisitos previos (solo el dueño):
#   1. plataformaia.eu ya no responde 308 al .com
#   2. DNS de plataformaia.eu apuntando a GitHub Pages (4 A + CNAME www)
#
# Uso: ./golive.sh            ejecuta y verifica
#      ./golive.sh --check    solo comprueba DNS/redirect, no publica
set -euo pipefail
cd "$(dirname "$0")"
DOMAIN="plataformaia.eu"
REPO="caseroclaw/observatorio-ia"
PAGES_IPS="185.199.108.153 185.199.109.153 185.199.110.153 185.199.111.153"

echo "== 1. Redirect del .eu =="
code=$(curl -s -o /dev/null -w "%{http_code}" --max-time 15 "https://$DOMAIN" || echo "000")
if [[ "$code" == "301" || "$code" == "308" ]]; then
  echo "BLOQUEADO: $DOMAIN sigue redirigiendo ($code). Quita la regla en el servidor del .com."; exit 1
fi
echo "ok ($code)"

echo "== 2. DNS =="
resolved=$(dig +short "$DOMAIN" A | sort | tr '\n' ' ')
echo "A: $resolved"
missing=0
for ip in $PAGES_IPS; do
  grep -qw "$ip" <<<"$resolved" || { echo "falta A $ip"; missing=1; }
done
www=$(dig +short "www.$DOMAIN" CNAME | tr -d ' ')
echo "www CNAME: ${www:-<ninguno>}"
[[ -n "$www" ]] || { echo "falta CNAME de www"; missing=1; }
if [[ $missing -eq 1 ]]; then
  echo "BLOQUEADO: la zona DNS todavía no apunta a GitHub Pages."; exit 1
fi

if [[ "${1:-}" == "--check" ]]; then echo "Comprobación OK. Nada publicado."; exit 0; fi

echo "== 3. CNAME en el repo y build indexable =="
printf '%s\n' "$DOMAIN" > site/CNAME 2>/dev/null || true
NOINDEX= python3 build.py
printf '%s\n' "$DOMAIN" > site/CNAME
mkdir -p site
echo "build sin noindex hecho"

echo "== 4. Publicar gh-pages =="
git add -A && git commit -qm "Go-live: dominio $DOMAIN" || true
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
gh api -X PUT "repos/$REPO/pages" -f "cname=$DOMAIN" -F "source[branch]=gh-pages" -F "source[path]=/" >/dev/null || \
  gh api -X PUT "repos/$REPO/pages" -f "cname=$DOMAIN" >/dev/null
gh api -X PUT "repos/$REPO/pages" -F "https_enforced=true" >/dev/null || true

echo "== 6. Verificación =="
for i in 1 2 3 4 5 6; do
  sleep 20
  st=$(gh api "repos/$REPO/pages" --jq '.status' 2>/dev/null || echo "?")
  echo "estado pages: $st"
  [[ "$st" == "built" ]] && break
done
echo "-- servido en el dominio --"
for u in "/" "/agencias-ia-madrid/" "/precios-agencias-ia/"; do
  printf '%s  ' "$(curl -s -o /dev/null -w '%{http_code}' --max-time 20 "https://$DOMAIN$u")"
  echo "https://$DOMAIN$u"
done
echo "-- robots y robots meta --"
curl -s --max-time 15 "https://$DOMAIN/robots.txt"
curl -s --max-time 15 "https://$DOMAIN/" | grep -o '<meta name="robots"[^>]*>' || echo "sin meta robots (correcto)"
echo "-- http -> https --"
curl -s -o /dev/null -w "%{http_code}\n" --max-time 15 "http://$DOMAIN/"
echo
echo "Siguiente: Search Console → añadir propiedad de dominio $DOMAIN (TXT DNS) o prefijo URL"
echo "y enviar https://$DOMAIN/sitemap.xml"

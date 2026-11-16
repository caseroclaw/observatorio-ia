# Puesta en marcha del directorio en `observatorio.plataformaia.eu`

**Arquitectura decidida:** el ápice `plataformaia.eu` **no se toca** (sigue haciendo
`308 → plataformaia.com`). El directorio vive en un **subdominio**:

- `observatorio.plataformaia.eu` → GitHub Pages (repo `caseroclaw/observatorio-ia`)
- `plataformaia.eu` → 308 → `plataformaia.com` (sin cambios)

Ventaja: un único registro DNS, cero riesgo para el `.com` y no hay que tocar el servidor.

Estado ahora: sitio construido (34 páginas, 27 fichas) y publicado con `noindex` en la vista previa
**https://caseroclaw.github.io/observatorio-ia/**.

---

## 1. El único paso que falta: un registro CNAME (dondominio)

En la zona DNS de `plataformaia.eu`:

- Campo: `observatorio`
- Tipo: `CNAME`
- Valor: `caseroclaw.github.io`

Nada más. No se borra el A del ápice, no se toca `www`, no se toca el servidor del `.com`.

Propagación habitual: 5-30 minutos con los TTL por defecto.

## 2. Avisar: activo dominio e indexado (lo ejecuto yo, 1 comando)

Cuando el CNAME resuelva:

```bash
./golive.sh --check   # comprueba el DNS sin publicar
./golive.sh           # build sin noindex + CNAME + dominio en Pages + HTTPS + verificación
```

Ese script:

1. Comprueba que `dig observatorio.plataformaia.eu CNAME` devuelve `caseroclaw.github.io`.
2. Regenera el sitio **sin** `noindex` y con `robots.txt` en `Allow: /` + sitemap.
3. Publica `gh-pages` con el fichero `CNAME`.
4. Declara el dominio en GitHub Pages y fuerza HTTPS (certificado Let's Encrypt automático).
5. Verifica 200 en `/`, `/agencias-ia-madrid/`, `/precios-agencias-ia/`, ausencia de `noindex`
   y redirección http → https.

## 3. Search Console (5 minutos, en paralelo)

Dos opciones:

- **Propiedad de dominio `plataformaia.eu`** → requiere un TXT en la zona DNS de dondominio.
  Cubre el ápice y todos los subdominios: es la que recomiendo.
- **Prefijo de URL `https://observatorio.plataformaia.eu/`** → verificación por meta etiqueta
  (me la pasas y la incrusto) o por fichero HTML.

Después: enviar `https://observatorio.plataformaia.eu/sitemap.xml`.

## 4. Qué acelera el indexado

Un subdominio nuevo tarda semanas en aparecer, y este arranca sin enlaces. Por orden de impacto:

1. **Un enlace desde `plataformaia.com`** (footer o página de recursos). El `.com` está indexado y
   pasa autoridad; es el enlace más valioso y no cuesta nada.
2. **LinkedIn de empresa** y perfiles propios.
3. **Que las agencias listadas reclamen su ficha** y la compartan: enlace entrante legítimo y
   temáticamente exacto.
4. Sitemap enviado y URL inspeccionada a mano en GSC las primeras semanas.

Nota técnica: Google trata un subdominio como un sitio distinto del ápice, así que no hereda
autoridad del `.com`. Aquí es irrelevante porque el `.com` no tiene autoridad que heredar: el
directorio arranca igual en `plataformaia.eu/` que en `observatorio.plataformaia.eu/`.

---

## Qué hay publicado ahora mismo

- `/` — directorio de 27 fichas, ~2.000 palabras, con criterios de elección y FAQ.
- `/agencias-ia-madrid/` (5 fichas) y `/agencias-ia-barcelona/` (7) — solo se generan con 3+.
- `/precios-agencias-ia/` — modelos de cobro, sin tarifas inventadas.
- `/metodologia/` y `/como-nos-financiamos/` — transparencia y relación con Plataforma IA.
- `/agencia/{slug}/` × 27 — sede comprobada, especialidad declarada, fuente enlazada, fecha.
- `sitemap.xml`, `robots.txt`, `llms.txt`, 404 y JSON-LD (Organization, ItemList, CollectionPage,
  FAQPage, BreadcrumbList, Organization por ficha).

## Reglas editoriales fijadas en el código

- Orden alfabético; no existe campo de posición ni de pago.
- Ciudad solo si está publicada en la web de la agencia (contacto/aviso legal con código postal).
- La ficha de Plataforma IA lleva etiqueta visible y queda fuera de la selección editorial.
- Página de ciudad solo con 3+ fichas verificadas.

## Siguiente fase (cuando el subdominio esté indexado)

1. Subir a 40 fichas → Valencia y Sevilla abren página propia.
2. Formulario «publica o corrige tu ficha» → cada alta es una agencia que comparte el enlace.
3. Comparador A vs B (el incumbent tiene 113 páginas de ese tipo; es la long tail más rentable).
4. Versión LatAm (México, Perú, Colombia): el autocomplete ya las pide y el incumbent solo tiene inglés.

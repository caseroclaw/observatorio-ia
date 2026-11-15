# Puesta en marcha de plataformaia.eu (lo que solo puede hacer el dueño)

Estado hoy: sitio construido y publicado en vista previa con `noindex`:
**https://caseroclaw.github.io/observatorio-ia/** — 34 páginas, 27 fichas verificadas.

El sitio ya está listo. Para que empiece a competir con el dominio propio hay que hacer tres cosas,
en este orden. Ninguna requiere tocar código.

---

## 1. Quitar el redirect 308 del .eu (servidor del .com)

Hoy `https://plataformaia.eu` responde `308 → https://plataformaia.com/`. Mientras exista, el dominio
no puede servir el directorio.

- Es el servidor `116.203.251.187` (el del `.com`, Next.js detrás de un proxy).
- Hay que eliminar la regla que redirige el host `plataformaia.eu` al `.com` (en nginx/caddy/traefik
  o en la configuración de dominios de la plataforma). El dominio deja de apuntar ahí en el paso 2,
  así que en la práctica basta con **no volver a añadir la regla**.

Comprobación: `curl -sI https://plataformaia.eu | head -1` deja de devolver 308.

## 2. Apuntar el DNS del dominio a GitHub Pages (dondominio)

En el panel de dondominio, zona DNS de `plataformaia.eu`:

- **4 registros A para el ápice** (`plataformaia.eu`):
  - `185.199.108.153`
  - `185.199.109.153`
  - `185.199.110.153`
  - `185.199.111.153`
- **1 CNAME** para `www` → `caseroclaw.github.io`
- Quitar el A actual que apunta a `116.203.251.187`.
- Opcional (recomendado): registro `AAAA` con las IPv6 de Pages
  (`2606:50c0:8000::153`, `2606:50c0:8001::153`, `2606:50c0:8002::153`, `2606:50c0:8003::153`).

Propagación habitual: 10-60 minutos con los TTL por defecto de dondominio.

## 3. Avisar para activar el dominio y el indexado

Cuando el DNS ya resuelva, hay que:

1. Declarar el dominio en el repo (fichero `CNAME` con `plataformaia.eu`).
2. Configurar el dominio en GitHub Pages y forzar HTTPS.
3. Reconstruir el sitio **sin** `noindex` y sustituir `robots.txt` (`Allow: /` + sitemap).
4. Enviar el sitemap a Search Console y verificar la propiedad.

Los puntos 1-3 los ejecuto yo en cuanto avises de que el DNS está listo (`./deploy.sh` sin `--preview`).

## 4. Search Console (5 minutos, en paralelo)

Alta de la propiedad `plataformaia.eu` en Search Console. Es el único dato que no puedo medir desde
fuera: impresiones, consultas y páginas «rastreadas sin indexar». Sin eso vamos a ciegas, igual que
pasa hoy con el `.com`.

---

## Qué hay publicado ahora mismo

- `/` — directorio de 27 fichas, 2.027 palabras, con metodología, criterios de elección y FAQ.
- `/agencias-ia-madrid/` y `/agencias-ia-barcelona/` — solo se generan con 3+ fichas verificadas.
- `/precios-agencias-ia/` — modelos de cobro (sin tarifas inventadas).
- `/metodologia/` y `/como-nos-financiamos/` — transparencia y declaración de la agencia que opera el sitio.
- `/agencia/{slug}/` × 27 — sede comprobada, especialidad declarada, fuente enlazada, fecha de revisión.
- `sitemap.xml`, `robots.txt`, `llms.txt`, 404, JSON-LD (Organization, ItemList, CollectionPage,
  FAQPage, BreadcrumbList, Organization por ficha).

## Reglas editoriales que quedan fijadas en el código

- Orden alfabético; no existe campo de posición ni de pago.
- Ciudad solo si está publicada en la web de la agencia (contacto/aviso legal con código postal).
- La ficha de Plataforma IA lleva etiqueta visible y queda fuera de la selección editorial.
- Página de ciudad solo con 3+ fichas verificadas.

## Siguiente fase (cuando el dominio esté activo)

1. Subir el directorio a 40 fichas (Valencia y Sevilla llegan a 3 y tendrían página propia).
2. Formulario «publica o corrige tu ficha» → cada alta es una agencia que comparte el enlace.
3. Comparador A vs B (el incumbent tiene 113 páginas de este tipo; es la long tail más rentable).
4. Versión LatAm (México, Perú, Colombia): el autocomplete de Google ya las pide y el incumbent
   solo tiene inglés.

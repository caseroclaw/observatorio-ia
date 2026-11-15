# plataformaia.eu — ¿directorio "mejores agencias de IA" o puerta al .com?

Estudio de viabilidad · 15 nov 2026 · datos medidos hoy (DNS/HTTP, SERP, competidores abiertos, BOE, doc. de Google)

---

## 1. Estado técnico real del dominio

- `plataformaia.eu` → **308 permanente** a `https://plataformaia.eu/*` … concretamente a `https://plataformaia.com/` (cabecera `location` + `refresh`), mismo IP que el .com (`116.203.251.187`, Hetzner), aplicación Next.js (`x-middleware-rewrite: /es`).
- DNS en **dondominio** (`ns1/ns2.dondominio.com`), A → mismo servidor.
- No sirve contenido propio: **mientras exista el 308 no puede posicionar nada**. Y hoy no hay histórico que perder (no hay páginas propias que redirigir de forma individual).

**Implicación:** cualquier plan con el .eu empieza por quitar el redirect y servir un sitio distinto en ese host (misma máquina u otro hosting con CNAME/A en dondominio).

## 2. Mercado: quién ocupa ya esa consulta (medido hoy)

- **aiagencies.eu** — el competidor directo exacto: **1.148 URLs** en sitemap, **333 agencias**, **48 ciudades**, **113 páginas "A vs B"**, índice de tarifas (`/rates`), perfiles de agencia, `submit`/`claim`, metodología pública y autor con nombre. **100 % inglés** y solo **13 páginas de España (28 agencias de 333)**. Aparece en todas las consultas en inglés ("best AI agencies Spain / Europe").
- **mejores-agencias.com** — EMD, 107 URLs, titular "Jenofonte" en aviso legal, top-10 con #1 *Pixelclip* y notas tipo "5 (48 opiniones)"; sin metodología visible. Es el modelo "yo primero" en su versión más frágil.
- **roihacking.ai** — agencia que se coloca **#1 en su propio "Top 10 agencias IA España 2026"** (25 URLs). Prueba de que el patrón funciona… sobre una web que ya tenía autoridad.
- **6+ blogs de agencias** cubriendo la misma consulta (galadrim, cyberclick, hiberusbooster, auttomai, kiwop, isocialweb). Head **saturado**.
- **plataformaia.com no aparece** en ninguna de las variantes probadas de estas consultas.

## 3. Demanda

- Autocomplete ES: *"agencias de inteligencia artificial en españa / en méxico / en perú"*, *"mejores agencias de inteligencia artificial (en perú)"*, *"agencia seo para ia madrid"*, *"agencia inteligencia artificial barcelona"*.
- **"mejores agencias de ia" no expande** en ES → el head tiene volumen bajo; el negocio está en **ciudad × servicio × país** y en LatAm (México, Perú ya aparecen como sugerencia).
- Volumen exacto **sin medir**: no hay GSC ni Keyword Planner a mano. Es lo primero a sacar (10 min) antes de dimensionar el proyecto.

## 4. Riesgos

**Política de Google (texto literal, spam policies):**
- *Doorway abuse*: "Having multiple websites with slight variations to the URL and home page to maximize their reach for any specific query" y "Having multiple domain names or pages targeted at specific regions or cities that funnel users to one page". El plan "serie de páginas en .eu que empujan a .com" **es literalmente ese patrón**.
- *Scaled content abuse* si las fichas son plantillas sin datos propios.
- *Policy circumvention*: crear un dominio nuevo para seguir haciendo lo mismo se penaliza explícitamente.

**Legal (España, verificado hoy en BOE):**
- LCD 3/1991 **art. 5** (actos de engaño): información veraz presentada de forma que induzca a error.
- LCD 3/1991 **art. 26** (prácticas comerciales encubiertas): promoción pagada no identificada como tal. Aplica directo a posiciones "destacadas" de pago.
- Un ranking propio sin criterio verificable + posición #1 del dueño = el supuesto de manual de ambos artículos.

**Huella:** mismo titular, mismo IP, misma cuenta de GSC y enlaces cruzados masivos = lo que convierte "dos webs" en "red de dominios".

## 5. El dato que decide (del ledger SEO del .com)

- 151 URLs en sitemap, todas 200, 72 posts, y **3 de 3 títulos exactos sin aparecer**; `/es/blog` sirve snapshots viejos; **sin GSC** y **sin un solo enlace de un dominio real**.
- Traducción: el cuello de botella del .com es **autoridad e indexación**, no contenido. Un dominio nuevo **hereda 0** de eso y compite contra un incumbent con 1.148 URLs.

## 6. Veredicto

**Como puerta (mi ranking conmigo #1 → .com): no.** Técnicamente posible, mal negocio: head saturado y de volumen bajo, riesgo de política + legal, y no resuelve el problema real (autoridad). Techo: tráfico residual de long tail y una marca de ranking que nadie cita ni enlaza.

**Como directorio real (sub-marca independiente, datos propios, listado propio declarado, ES + LatAm): sí.** Es de los pocos activos que generan enlaces legítimos por diseño (cada agencia listada enlaza su ficha), construye la autoridad que el .com no tiene y es citable por LLMs si va con datos estructurados. Plazo realista: **9-12 meses**, no 9 semanas.

**Ventaja competitiva concreta:** aiagencies.eu es inglés y tiene 28 agencias españolas de 333. El hueco es **español + LatAm + datos locales verificados (tarifas, tamaño, casos)**, no "otro top 10 más".

## 7. Plan 30/60/90

**Semana 1-3 — MVP (8-40 URLs, estático pre-renderizado, 0 €):**
- Marca propia, **no** "Plataforma IA" (un ranking de agencias firmado por una de las agencias listadas no se cita).
- `/es/mejores-agencias-ia-espana` (hub, edición 2027)
- `/es/mejores-agencias-ia-{madrid,barcelona,valencia,sevilla,malaga,bilbao}`
- `/es/precios-agencias-ia-espana` — índice de tarifas: el activo más citable y el que nadie tiene en español.
- `/es/metodologia`, `/es/como-nos-financiamos` (transparencia = el escudo legal y de confianza)
- `/es/agencia/{slug}` × 40 fichas con datos verificados (sede, año, tamaño, servicios, caso público, tarifa si la publican)
- JSON-LD `ItemList` + `Organization` + `FAQPage`; HTML estático (no JS) para crawlers e IA.

**Mes 2-3:** alta y "reclama tu ficha" (cada alta = una agencia que comparte el enlace), comparador `A vs B` (las 113 páginas del incumbent prueban el patrón), LatAm (MX, CO, CL, PE, AR).

**Mes 4-12:** posiciones destacadas **declaradas**, lead-gen hacia .com con disclosure, medición en GSC, enlace de cada agencia a su ficha como motor de autoridad.

## 8. Decisiones que solo puede tomar el dueño

1. **Nombre/sub-marca** del directorio (3 candidatos: *Observatorio IA*, *AgenciasIA.eu*, *IA Directory ES*).
2. **Listado propio:** declarado ("operado por Plataforma IA") o #1 silencioso. Recomiendo declarado; el silencioso no lo ejecuto.
3. **Accesos:** quitar el 308 en el servidor del .com + DNS en dondominio (o Netlify con el .eu apuntando por A/CNAME).
4. **GSC del .com** (5 min): sin impresiones ni cobertura no hay forma de medir si el proyecto funciona.

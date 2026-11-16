#!/usr/bin/env python3
"""Generador estático del Observatorio IA (plataformaia.eu).

Sin dependencias. Lee data/agencias.json y escribe site/ con HTML pre-renderizado,
JSON-LD, sitemap, robots y llms.txt.
"""
import json
import html
import os
import re
import shutil
from datetime import date

BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(BASE, "data", "agencias.json")
OUT = os.path.join(BASE, "site")
DOMAIN = "https://observatorio.plataformaia.eu"
BRAND = "Observatorio IA"
TODAY = "2026-11-15"

CITY_META = {
    "madrid": {
        "nombre": "Madrid",
        "titulo": "Agencias de IA en Madrid",
        "intro": (
            "Madrid concentra la mayor oferta de consultoría tecnológica del país, y eso se nota en cómo se "
            "vende la IA: casi cualquier consultora de sistemas tiene ya una línea de IA. La contrapartida es "
            "que el comprador madrileño se encuentra propuestas muy distintas bajo la misma etiqueta, desde "
            "equipos de datos de gran cuenta hasta agencias de automatización de tres personas."
        ),
        "mercado": (
            "En la práctica, el mercado madrileño se divide en tres capas. La primera son las consultoras de "
            "sistemas y datos que atienden a gran empresa y administración, con equipos de más de cien personas "
            "y ciclos de venta largos. La segunda son los equipos técnicos medianos que construyen producto y "
            "plataformas de datos. La tercera, la que más ha crecido, son agencias pequeñas de automatización "
            "que implantan agentes, RAG y flujos sobre herramientas ya contratadas (CRM, ERP, Helpdesk). "
            "Para una pyme o un despacho, la tercera capa suele ser la única que responde en semanas y con "
            "presupuesto cerrado; para un proyecto con datos regulados, la primera es la que aguanta auditoría."
        ),
        "elegir": (
            "Dos comprobaciones separan rápido a un proveedor serio en Madrid: que enseñe una dirección física "
            "en la comunidad (no un coworking de alquiler por horas sin equipo detrás) y que el nombre de la "
            "persona que va a dirigir el proyecto aparezca antes de la firma, no después. Si la propuesta llega "
            "con un equipo de preventa y el equipo de entrega es anónimo, el riesgo de traspaso es alto."
        ),
    },
    "barcelona": {
        "nombre": "Barcelona",
        "titulo": "Agencias de IA en Barcelona",
        "intro": (
            "Barcelona tiene un perfil distinto al de Madrid: menos gran cuenta institucional y más producto "
            "digital, marketing y datos aplicados a negocio. Muchas de las agencias que aquí se anuncian como "
            "«de IA» vienen del mundo del marketing y del diseño, y han añadido la capa de automatización en "
            "los últimos dos años."
        ),
        "mercado": (
            "Esa herencia se nota en el tipo de proyecto: es la ciudad donde más fácil es encontrar un equipo "
            "que combine captación, analítica y modelos de lenguaje en un mismo encargo, y donde el SEO con "
            "visibilidad en asistentes (GEO) se ha convertido en servicio propio. Lo que escasea es la "
            "consultoría de datos pura con equipo grande: para eso, la oferta local suele ser buena en "
            "proyectos de analítica y gobierno del dato, y corta en integraciones de sistemas heredados."
        ),
        "elegir": (
            "En Barcelona conviene preguntar por la frontera entre agencia y tecnología: varias de las fichas "
            "de este directorio venden también su propia plataforma, y eso cambia la conversación de precios. "
            "Pide el desglose de horas de estrategia frente a horas de implantación; si el 60 % del presupuesto "
            "es estrategia, estás comprando un plan, no un sistema funcionando."
        ),
    },
}

CSS = """
:root{--bg:#0b0d10;--panel:#12161b;--line:#232a32;--txt:#e7ecf2;--mut:#9aa7b4;--acc:#4ea1ff;--ok:#38d39f}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--txt);font:16px/1.65 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
a{color:var(--acc);text-decoration:none}
a:hover{text-decoration:underline}
.wrap{max-width:960px;margin:0 auto;padding:0 20px}
header.site{border-bottom:1px solid var(--line);background:#0e1116;position:sticky;top:0;z-index:9}
header.site .wrap{display:flex;align-items:center;gap:18px;height:60px;flex-wrap:wrap}
.brand{font-weight:700;letter-spacing:.2px;color:var(--txt)}
.brand span{color:var(--acc)}
nav.top{display:flex;gap:16px;flex-wrap:wrap;font-size:14px}
nav.top a{color:var(--mut)}
nav.top a:hover{color:var(--txt);text-decoration:none}
main{padding:38px 0 10px}
h1{font-size:clamp(26px,4vw,40px);line-height:1.15;margin:.2em 0 .4em;letter-spacing:-.5px}
h2{font-size:clamp(20px,3vw,26px);margin:2em 0 .5em;letter-spacing:-.3px}
h3{font-size:18px;margin:1.6em 0 .4em}
p{margin:.7em 0}
.lead{font-size:18px;color:#cbd6e2}
.mut{color:var(--mut)}
ul,ol{padding-left:1.2em}
li{margin:.35em 0}
.card{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:18px 20px;margin:14px 0}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:14px;margin:18px 0}
.grid .card{margin:0}
.card h3{margin:.1em 0 .3em;font-size:17px}
.tag{display:inline-block;font-size:12px;color:var(--mut);border:1px solid var(--line);border-radius:999px;padding:2px 9px;margin:3px 5px 3px 0}
.badge{display:inline-block;font-size:12px;border-radius:6px;padding:2px 8px;background:rgba(78,161,255,.12);color:var(--acc);border:1px solid rgba(78,161,255,.35)}
.badge.own{background:rgba(56,211,159,.12);color:var(--ok);border-color:rgba(56,211,159,.35)}
.note{font-size:14px;color:var(--mut)}
.note a{color:var(--acc)}
.crumbs{font-size:13px;color:var(--mut);margin-bottom:8px}
table{width:100%;border-collapse:collapse;margin:16px 0;font-size:15px}
th,td{text-align:left;padding:9px 10px;border-bottom:1px solid var(--line);vertical-align:top}
th{color:var(--mut);font-weight:600;font-size:13px;text-transform:uppercase;letter-spacing:.4px}
details{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:12px 16px;margin:10px 0}
summary{cursor:pointer;font-weight:600}
footer.site{border-top:1px solid var(--line);margin-top:50px;padding:26px 0 50px;color:var(--mut);font-size:14px}
footer.site a{color:var(--acc)}
.hl{border-left:3px solid var(--acc);padding-left:14px;color:#cbd6e2}
.cta{display:inline-block;background:var(--acc);color:#08111c;font-weight:700;padding:10px 18px;border-radius:8px;margin:10px 0}
.cta:hover{text-decoration:none;filter:brightness(1.08)}
"""


def esc(s):
    return html.escape(s, quote=True)


def load():
    with open(DATA, encoding="utf-8") as f:
        return json.load(f)


def page(path, title, desc, body, jsonld=None, updated=TODAY):
    """Escribe una página con layout común. path sin barra final salvo la home."""
    url = DOMAIN + ("/" if path == "" else "/" + path + "/")
    noindex = bool(os.environ.get("NOINDEX"))
    robots_meta = '\n<meta name="robots" content="noindex, follow">' if noindex else ""
    ld = ""
    if jsonld:
        for block in (jsonld if isinstance(jsonld, list) else [jsonld]):
            ld += '\n<script type="application/ld+json">%s</script>' % json.dumps(block, ensure_ascii=False)
    doc = f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{url}">{robots_meta}
<meta property="og:type" content="website">
<meta property="og:site_name" content="{BRAND}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:locale" content="es_ES">
<meta name="twitter:card" content="summary">
<link rel="stylesheet" href="/assets/style.css">
<link rel="alternate" type="application/xml" title="Sitemap" href="/sitemap.xml">
</head>
<body>
<header class="site"><div class="wrap">
<a class="brand" href="/">{BRAND.replace(' ', '&nbsp;').replace('IA','<span>IA</span>')}</a>
<nav class="top">
<a href="/">Directorio</a>
<a href="/agencias-ia-madrid/">Madrid</a>
<a href="/agencias-ia-barcelona/">Barcelona</a>
<a href="/precios-agencias-ia/">Precios</a>
<a href="/metodologia/">Metodología</a>
</nav>
</div></header>
<main><div class="wrap">
{body}
</div></main>
<footer class="site"><div class="wrap">
<p><strong>{BRAND}</strong> es un directorio de agencias de inteligencia artificial en España, operado por
<a href="https://plataformaia.com" rel="noopener">Plataforma IA</a>. No vendemos posiciones: el orden del listado es
alfabético dentro de cada nivel de verificación y ninguna ficha se paga. Nuestra propia agencia aparece en el
directorio con esa condición declarada y fuera de cualquier selección editorial.</p>
<p>Fichas revisadas por última vez el {updated}. Datos obtenidos de la web pública de cada agencia; cada ficha enlaza
su fuente. ¿Detectas un error o quieres corregir tu ficha? <a href="https://plataformaia.com/es/contacto" rel="noopener">Escríbenos</a>.</p>
<p class="mut">© 2027 {BRAND} · <a href="/metodologia/">Metodología</a> · <a href="/como-nos-financiamos/">Cómo nos financiamos</a></p>
</div></footer>
{ld}
</body>
</html>"""
    if path == "":
        dest = os.path.join(OUT, "index.html")
    else:
        d = os.path.join(OUT, path)
        os.makedirs(d, exist_ok=True)
        dest = os.path.join(d, "index.html")
    with open(dest, "w", encoding="utf-8") as f:
        f.write(doc)
    return dest


def org_jsonld():
    return {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": BRAND,
        "url": DOMAIN,
        "description": "Directorio verificado de agencias y consultoras de inteligencia artificial en España.",
        "parentOrganization": {"@type": "Organization", "name": "Plataforma IA", "url": "https://plataformaia.com"},
        "areaServed": "ES",
    }


def breadcrumbs(items):
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n, "item": DOMAIN + u} for i, (n, u) in enumerate(items)
        ],
    }


def faq_jsonld(pairs):
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in pairs
        ],
    }


def card(a):
    tags = "".join('<span class="tag">%s</span>' % esc(t) for t in a["tags"])
    own = ' <span class="badge own">opera este directorio</span>' if a["propio"] else ""
    return f"""<article class="card">
<h3><a href="/agencia/{a['slug']}/">{esc(a['nombre'])}</a>{own}</h3>
<p class="mut" style="font-size:14px;margin:.1em 0 .5em">{esc(a['ciudad'])} · {esc(a['tipo_label'])}</p>
<p>{esc(a['nota'].split('. ')[0])}.</p>
<div>{tags}</div>
</article>"""


FAQ_HUB = [
    ("¿Cuáles son las mejores agencias de IA en España?",
     "No hay una respuesta única y desconfía de quien la dé sin explicar el criterio. Para una pyme que necesita "
     "automatizar captación o backoffice, «mejor» suele significar un equipo pequeño que entregue en semanas con "
     "precio cerrado; para una empresa con datos regulados, significa un proveedor con equipo de datos, "
     "trazabilidad y capacidad de auditoría. Este directorio no publica un ranking competitivo: publica fichas "
     "comparables, con la fuente de cada dato, para que el criterio lo pongas tú."),
    ("¿Cómo se ordenan las agencias de este directorio?",
     "Alfabéticamente dentro de cada nivel de verificación. No hay posiciones pagadas ni orden por comisión. "
     "La ficha de Plataforma IA —la empresa que opera el directorio— aparece con esa condición visible y queda "
     "excluida de la selección editorial."),
    ("¿Qué significa «ficha verificada»?",
     "Que el 15 de noviembre de 2026 abrimos la web de la agencia, comprobamos que sigue activa y que publica una "
     "dirección o una descripción de servicio coherente con lo que figura en la ficha, y guardamos la URL exacta "
     "de la fuente. No verificamos resultados de clientes, facturación ni certificaciones: si un dato no está en "
     "la web de la agencia, no aparece aquí."),
    ("¿Cobráis por aparecer o por destacar una agencia?",
     "No. Ni alta, ni posición, ni etiqueta de «destacada». El modelo de ingresos está publicado en la página de "
     "financiación: servicios de captación de leads para quien los quiera contratar, siempre identificados como "
     "tales, y nunca condicionando la presencia ni el orden en el directorio."),
    ("¿Puedo corregir o reclamar mi ficha?",
     "Sí. Cualquier agencia puede pedir corrección o baja escribiendo al contacto. Las correcciones se publican con "
     "la fecha de revisión actualizada, y las bajas se ejecutan sin pedir nada a cambio."),
]


def apply_base_path():
    """Reescribe los enlaces raíz cuando el sitio se publica en un subdirectorio
    (vista previa en usuario.github.io/repo). En producción BASE_PATH va vacío."""
    base = os.environ.get("BASE_PATH", "").rstrip("/")
    if not base:
        return 0
    n = 0
    for dp, _, fs in os.walk(OUT):
        for f in fs:
            if not f.endswith(".html"):
                continue
            p = os.path.join(dp, f)
            s = open(p, encoding="utf-8").read()
            new = re.sub(r'(href|src)="/(?!/)', lambda m: '%s="%s/' % (m.group(1), base), s)
            if new != s:
                with open(p, "w", encoding="utf-8") as fh:
                    fh.write(new)
                n += 1
    return n


def build():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(os.path.join(OUT, "assets"))
    with open(os.path.join(OUT, "assets", "style.css"), "w", encoding="utf-8") as f:
        f.write(CSS)

    d = load()
    ags = d["agencias"]
    verif = d["actualizado"]
    propios = [a for a in ags if a["propio"]]
    terceros = [a for a in ags if not a["propio"]]

    # ---------- HOME ----------
    by_city = {}
    for a in ags:
        if a["ciudad_slug"]:
            by_city.setdefault(a["ciudad_slug"], []).append(a)

    cards = "\n".join(card(a) for a in sorted(ags, key=lambda x: x["nombre"].lower()))
    TIPOS_ORDER = [("consultora", "Consultoría tecnológica"),
                   ("automatizacion", "Agencia de automatización e IA aplicada"),
                   ("marketing", "Agencia de marketing y captación"),
                   ("producto", "Estudio de producto digital")]
    TIPO_INTRO = {
        "consultora": "Equipos de sistemas y datos que venden IA dentro de proyectos de plataforma. Encajan cuando "
                      "hay que construir o integrar infraestructura y cuando el comprador necesita capacidad de auditoría.",
        "automatizacion": "Equipos centrados en implantar agentes, RAG y flujos sobre herramientas ya contratadas. "
                          "Es el perfil que responde en semanas y con alcance cerrado, y el que más ha crecido en el sector.",
        "marketing": "Agencias que llegan a la IA desde la captación: SEO, publicidad, contenidos y ahora visibilidad "
                     "en asistentes. Útiles para demanda; conviene separar qué parte es IA y qué parte es gestión de canales.",
        "producto": "Estudios que diseñan y construyen producto digital. Entran cuando la IA es una capa de un producto "
                    "que hay que definir antes de desarrollar.",
    }
    tipos_html = ("<h2>Por tipo de proveedor</h2>\n<p>No todas las agencias que dicen «IA» hacen lo mismo. Esta es la "
                  "clasificación que usamos en las fichas y el criterio de cuándo encaja cada perfil.</p>\n")
    for tslug, tlabel in TIPOS_ORDER:
        group = sorted([a for a in ags if a["tipo"] == tslug], key=lambda x: x["nombre"].lower())
        if not group:
            continue
        tipos_html += ('<h3>%s (%d)</h3>\n<p>%s</p>\n<p class="note">%s</p>\n'
                       % (esc(tlabel), len(group), esc(TIPO_INTRO[tslug]),
                          " · ".join('<a href="/agencia/%s/">%s</a>' % (a["slug"], esc(a["nombre"])) for a in group)))
    faq_html = "\n".join(
        "<details><summary>%s</summary><p>%s</p></details>" % (esc(q), esc(a)) for q, a in FAQ_HUB
    )
    item_list = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": "Agencias de IA en España",
        "itemListOrder": "https://schema.org/ItemListOrderAscending",
        "numberOfItems": len(ags),
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": a["nombre"],
             "url": "%s/agencia/%s/" % (DOMAIN, a["slug"])}
            for i, a in enumerate(sorted(ags, key=lambda x: x["nombre"].lower()))
        ],
    }
    home_body = f"""
<p class="crumbs">Directorio · España</p>
<h1>Agencias de IA en España: {len(ags)} fichas verificadas (edición 2027)</h1>
<p class="lead">Un directorio de consultoras y agencias de inteligencia artificial que enseña <strong>qué hace
cada una, dónde está y de dónde sale el dato</strong>. Sin ranking inventado, sin notas de valoración sin
respaldo y sin posiciones a la venta.</p>

<div class="card hl">
<p><strong>Qué vas a encontrar aquí:</strong> {len(ags)} fichas de agencias y consultoras con actividad de IA
en España, cada una con su sede comprobada, su especialidad declarada y un enlace a la fuente exacta.
El listado está ordenado alfabéticamente y revisado por última vez el {verif}.</p>
<p style="margin-bottom:0"><strong>Qué no vas a encontrar:</strong> un «top 10» con estrellas que nadie puede
auditar, valoraciones de clientes que no existen y una agencia del dueño del sitio en el número uno.</p>
</div>

<h2>¿Buscas «las mejores agencias de IA de España»? Lee el criterio antes que la lista</h2>
<p>La consulta «mejores agencias de inteligencia artificial» devuelve hoy decenas de listas, y casi todas
comparten el mismo defecto: el orden no responde a nada comprobable. Unas colocan primero a la agencia que
escribe el artículo. Otras cobran por posición. Las más honestas ordenan por tamaño, que es una forma rápida
de dejar fuera a los equipos pequeños que sí resuelven problemas de pyme.</p>
<p>Nuestro criterio es más aburrido y más útil: <strong>fichas comparables</strong>. En cada una verás la sede,
la especialidad tal como la declara la agencia, para qué tipo de proyecto encaja y para cuál no, y el enlace
a la página de la que sale el dato. Si necesitas un proveedor para un proyecto concreto, compara tres fichas
de tu sector y haz las cuatro preguntas de la sección siguiente. Eso decide más que cualquier ranking.</p>
<p><a class="cta" href="/metodologia/">Cómo verificamos cada ficha</a></p>

<h2>Las cuatro preguntas que descartan a la mitad de los proveedores</h2>
<ol>
<li><strong>¿Quién firma la entrega?</strong> Nombre y rol de la persona que dirige el proyecto, antes de firmar.
Si solo hay un equipo comercial, el proyecto se traspasa en la segunda semana.</li>
<li><strong>¿Qué parte es IA y qué parte es configuración?</strong> Pide el desglose: modelo, datos usados,
integraciones y quién mantiene el sistema cuando el modelo cambie de versión.</li>
<li><strong>¿Cómo se mide?</strong> Un proyecto serio define una métrica antes de empezar (horas ahorradas,
tickets resueltos, tiempo de respuesta) y acepta revisarla al mes. Sin métrica, no hay proyecto: hay demo.</li>
<li><strong>¿Qué pasa con los datos?</strong> Dónde se alojan, qué proveedor de modelo se usa, si hay cesión a
terceros y cómo se ejerce el derecho de supresión. En proyectos con datos personales, esta respuesta debería
estar por escrito en la propuesta.</li>
</ol>

<h2>Directorio completo</h2>
<p class="note">Orden alfabético. Nivel de verificación único: web activa y datos comprobados el {verif}.
Ciudades con al menos tres fichas verificadas tienen página propia: <a href="/agencias-ia-madrid/">Madrid</a> ·
<a href="/agencias-ia-barcelona/">Barcelona</a>.</p>
<div class="grid">
{cards}
</div>

{tipos_html}

<h2>Qué significa cada ficha</h2>
<p>No puntuamos «calidad»: no tenemos forma de auditar los resultados de una agencia sin acceso a sus clientes.
Lo que sí hacemos es separar hechos comprobables de marketing. La nota de cada ficha está escrita para que
sirva de filtro: dice para qué tipo de encargo encaja el equipo y en qué casos es mejor buscar otro perfil.
Cuando una agencia publica su propio ranking y se coloca primera, lo decimos en su ficha, porque es
información que el lector necesita para leer ese ranking.</p>
<p>La ficha de <strong>Plataforma IA</strong> —la consultora que opera este directorio— está en el listado con
la etiqueta visible y queda excluida de la selección editorial. Nos parece la única forma defendible de
aparecer en un directorio propio: declarado, no escondido en el puesto uno.</p>

<h2>Preguntas frecuentes</h2>
{faq_html}

<p class="note">Última revisión del directorio: {verif}. ¿Falta una agencia o hay un dato desactualizado?
<a href="https://plataformaia.com/es/contacto" rel="noopener">Avísanos</a> y lo corregimos con fecha.</p>
"""
    page("", "Agencias de IA en España: directorio verificado (2027) | " + BRAND,
         "Directorio verificado de agencias y consultoras de inteligencia artificial en España: %d fichas con sede, "
         "especialidad y fuente comprobada. Sin posiciones pagadas ni rankings inventados." % len(ags),
         home_body, [org_jsonld(), item_list, faq_jsonld(FAQ_HUB),
                     breadcrumbs([("Directorio", "/")])])

    # ---------- CITY PAGES ----------
    for cslug, meta in CITY_META.items():
        items = sorted(by_city.get(cslug, []), key=lambda x: x["nombre"].lower())
        if len(items) < 3:
            continue
        cc = "\n".join(card(a) for a in items)
        other = "madrid" if cslug == "barcelona" else "barcelona"
        other_name = CITY_META[other]["nombre"]
        body = f"""
<p class="crumbs"><a href="/">Directorio</a> · {meta['nombre']}</p>
<h1>{meta['titulo']}: {len(items)} fichas verificadas</h1>
<p class="lead">{meta['intro']}</p>
<p>{meta['mercado']}</p>

<h2>Fichas verificadas en {meta['nombre']}</h2>
<p class="note">Orden alfabético. Datos comprobados el {verif}; cada ficha enlaza su fuente.</p>
<div class="grid">
{cc}
</div>

<h2>Cómo se elige un proveedor en {meta['nombre']}</h2>
<p>{meta['elegir']}</p>
<p>Un criterio adicional que vale para cualquier ciudad: pide el mismo caso de uso a dos proveedores y compara
la propuesta, no la presentación. La diferencia entre una agencia que ha hecho el trabajo antes y otra que
improvisa aparece en la tercera pregunta, cuando entra en detalle sobre datos e integraciones.</p>

<h2>Antes de contratar</h2>
<p>Lee la <a href="/metodologia/">metodología</a> para saber exactamente qué hemos comprobado en cada ficha y
qué no. Si tu decisión depende del precio, la guía de <a href="/precios-agencias-ia/">modelos de cobro</a>
explica qué se paga en cada formato y qué pedir en el presupuesto. Y si tu proyecto no es de {meta['nombre']},
mira las agencias de <a href="/agencias-ia-{other}/">{other_name}</a> o el <a href="/">directorio completo</a>.</p>
"""
        page("agencias-ia-" + cslug, meta["titulo"] + " (2027) | " + BRAND,
             "%d agencias y consultoras de IA con sede verificada en %s: qué hace cada una, para qué proyecto "
             "encaja y enlace a la fuente de cada dato." % (len(items), meta["nombre"]),
             body,
             [org_jsonld(),
              {"@context": "https://schema.org", "@type": "CollectionPage",
               "name": meta["titulo"], "url": DOMAIN + "/agencias-ia-" + cslug + "/",
               "about": {"@type": "Thing", "name": "Agencias de inteligencia artificial en " + meta["nombre"]}},
              breadcrumbs([("Directorio", "/"), (meta["nombre"], "/agencias-ia-" + cslug + "/")])])

    # ---------- PRECIOS ----------
    precios_pairs = [
        ("¿Cuánto cuesta contratar una agencia de IA en España?",
         "Depende del formato, no del tamaño de la agencia. Un proyecto cerrado con alcance definido suele "
         "presupuestarse por entregables; un acompañamiento continuo, por bolsa de horas o cuota mensual; y una "
         "automatización puntual, por horas. Esta página no publica una tabla de tarifas porque no hay ninguna "
         "fuente pública que la respalde: pedimos presupuesto a las agencias del directorio y publicaremos rangos "
         "con fuente cuando las tengamos, no antes."),
        ("¿Es más caro un proyecto cerrado o por horas?",
         "El proyecto cerrado tiene precio más alto por hora trabajada, porque el proveedor cobra el riesgo de "
         "equivocarse en la estimación. La bolsa de horas sale más barata si el alcance cambia mucho, y más cara "
         "si no cambia nunca. Para una primera automatización con alcance claro, el cerrado suele proteger al "
         "comprador; para un sistema que va a evolucionar, la bolsa con límite mensual es más honesta que un "
         "cerrado que se queda corto en la semana tres."),
        ("¿Qué debe incluir un presupuesto de IA para ser comparable?",
         "Cinco líneas: alcance (qué procesos entran y cuáles no), entregables, modelo y proveedor de IA usado, "
         "quién mantiene el sistema y con qué coste mensual de infraestructura, y criterio de aceptación. Si dos "
         "presupuestos no comparten esas cinco líneas, no son comparables aunque el número final se parezca."),
        ("¿Por qué las agencias no publican precios?",
         "Porque el coste depende del sistema que ya tienes: integrar con un CRM antiguo puede costar más que el "
         "propio modelo. Aun así, la opacidad total es una señal de alarma: una agencia que no puede dar un rango "
         "orientativo tras una llamada de treinta minutos no ha hecho proyectos parecidos, o no quiere competir "
         "por precio."),
    ]
    pfaq = "\n".join("<details><summary>%s</summary><p>%s</p></details>" % (esc(q), esc(a)) for q, a in precios_pairs)
    precios_body = f"""
<p class="crumbs"><a href="/">Directorio</a> · Precios</p>
<h1>Cuánto cuesta una agencia de IA en España: los tres modelos de cobro</h1>
<p class="lead">No hay una tarifa de mercado, hay tres formas de cobrar y cada una reparte el riesgo de forma
distinta. Esto es lo que cambia en cada modelo, qué pedir en el presupuesto y qué respuestas deben hacerte
descartar a un proveedor.</p>

<h2>1. Proyecto cerrado</h2>
<p>El proveedor fija precio y fecha para un alcance definido por escrito. Es el formato habitual en
automatizaciones concretas: un agente de atención, un flujo de presupuestos, una integración con el ERP.
Protege al comprador frente a desviaciones y penaliza al proveedor que estima mal. Lo que debes exigir:
criterio de aceptación explícito y qué ocurre si el alcance cambia a mitad.</p>

<h2>2. Bolsa de horas o cuota mensual</h2>
<p>Se paga tiempo, no resultado. Tiene sentido cuando el sistema va a evolucionar mes a mes o cuando el
proveedor hace mantenimiento de modelos y flujos. Lo que debes exigir: límite mensual, informe de horas por
tarea y cláusula de devolución o traspaso de las horas no consumidas. Sin esas tres cosas, la bolsa se
convierte en una cuota que no termina nunca.</p>

<h2>3. Éxito o comisión sobre ahorro</h2>
<p>Poco frecuente fuera del mundo comercial, donde se cobra por lead o por venta. En automatización interna
aparece a veces como porcentaje del ahorro estimado. Es un formato que suena atractivo y suele acabar en
discusión: el ahorro se mide con datos del cliente, y quien vende tiene incentivo a inflar la línea base.
Si te lo proponen, exige que la fórmula de medición esté firmada antes de empezar.</p>

<h2>Qué pedir en cualquier presupuesto</h2>
<table>
<tr><th>Línea</th><th>Qué comprobar</th></tr>
<tr><td>Alcance</td><td>Qué procesos entran y, sobre todo, cuáles quedan fuera</td></tr>
<tr><td>Entregables</td><td>Sistema funcionando, documentación y traspaso, no «un informe»</td></tr>
<tr><td>Modelo y proveedor</td><td>Qué modelo se usa y qué pasa si cambia de precio o de versión</td></tr>
<tr><td>Mantenimiento</td><td>Coste mensual de infraestructura y quién lo asume</td></tr>
<tr><td>Aceptación</td><td>Métrica y plazo para dar el proyecto por terminado</td></tr>
</table>

<h2>La pregunta que ahorra más dinero</h2>
<p>«¿Cuánto de este presupuesto es integración con mis sistemas y cuánto es el modelo de IA?». En proyectos
pequeños, el modelo suele ser la parte barata; lo caro es conectar con el CRM, el ERP, el correo y la
telefonía. Un proveedor que responde con porcentajes concretos ha hecho el trabajo antes.</p>

<h2>Preguntas frecuentes</h2>
{pfaq}
<p class="note">Esta página no contiene tarifas de terceros porque no tenemos una fuente pública que las
respalde. Cuando una agencia del directorio publique precios, se replicarán aquí con enlace a su web.</p>
"""
    page("precios-agencias-ia", "Precios de agencias de IA en España: modelos de cobro | " + BRAND,
         "Proyecto cerrado, bolsa de horas o pago por éxito: qué implica cada modelo de cobro de una agencia de IA, "
         "qué pedir en el presupuesto y qué respuestas deben hacerte descartar al proveedor.",
         precios_body, [org_jsonld(), faq_jsonld(precios_pairs),
                        breadcrumbs([("Directorio", "/"), ("Precios", "/precios-agencias-ia/")])])

    # ---------- METODOLOGIA ----------
    metodo_body = f"""
<p class="crumbs"><a href="/">Directorio</a> · Metodología</p>
<h1>Metodología: qué comprobamos y qué no</h1>
<p class="lead">Un directorio vale lo que vale su letra pequeña. Esta página explica cómo se construye cada
ficha, qué datos están verificados, qué queda fuera y cómo se corrige un error.</p>

<h2>Qué comprobamos el {verif}</h2>
<ul>
<li><strong>Web activa.</strong> Abrimos la web de la agencia y comprobamos que responde y que el contenido
corresponde a la actividad que declara.</li>
<li><strong>Sede.</strong> Solo publicamos ciudad cuando la dirección aparece en la web de la agencia (página
de contacto o aviso legal, con código postal) o cuando la propia agencia se describe con esa ciudad en su
portada. Si no hay forma de comprobarlo, la ficha dice «España» y no entra en las páginas de ciudad.</li>
<li><strong>Especialidad.</strong> Tomada de cómo la agencia describe su propio servicio, no de una
clasificación nuestra.</li>
<li><strong>Fuente.</strong> Cada ficha enlaza la URL exacta de la que salen los datos, con fecha de revisión.</li>
</ul>

<h2>Qué no comprobamos</h2>
<ul>
<li><strong>Resultados de clientes.</strong> No tenemos acceso a sus cuentas. Cualquier cifra de ROI que
publique una agencia es suya, no nuestra.</li>
<li><strong>Valoraciones.</strong> No publicamos estrellas ni notas de usuarios que no podamos verificar. Un
«5 (48 opiniones)» sin enlace a las opiniones es decoración.</li>
<li><strong>Certificaciones y tamaño de equipo.</strong> Salvo que la agencia las publique en su web, no
aparecen. Los «más de X empleados» sin fuente se quedan fuera.</li>
</ul>

<h2>Cómo se ordena el directorio</h2>
<p>Alfabéticamente, dentro de un único nivel de verificación: web activa y datos comprobados en la fecha de
revisión. No hay orden por comisión, ni por tráfico enviado, ni por relación comercial. Cuando el directorio
incorpore niveles adicionales de verificación (por ejemplo, casos de uso documentados por el cliente), se
publicarán con su criterio exacto y su fecha de entrada en vigor.</p>

<h2>La agencia que opera el directorio</h2>
<p>Plataforma IA es la consultora que mantiene este sitio y aparece como una ficha más, con la etiqueta
visible y fuera de la selección editorial. No se autoselecciona, no se pone primera y no recibe tratamiento
distinto en el listado. Si en algún momento eso cambia, se anunciará aquí antes de aplicarlo.</p>

<h2>Correcciones y bajas</h2>
<p>Cualquier agencia puede pedir corrección o retirada escribiendo al <a href="https://plataformaia.com/es/contacto" rel="noopener">contacto</a>.
Las correcciones se publican con la fecha de revisión actualizada. Las bajas se ejecutan sin condiciones y sin
coste: el directorio no cobra por estar ni por dejar de estar.</p>

<h2>Frecuencia de revisión</h2>
<p>Revisión completa manual con cada ampliación del directorio; comprobación automática de que las webs siguen
activas, semanal. Una ficha cuya web desaparezca se marca y se retira en la siguiente revisión manual.</p>
"""
    page("metodologia", "Metodología del directorio: qué verificamos | " + BRAND,
         "Cómo se construye cada ficha del directorio: web activa, sede comprobada con código postal, "
         "especialidad declarada por la agencia y fuente enlazada. Qué no verificamos y cómo se corrige.",
         metodo_body, [org_jsonld(), breadcrumbs([("Directorio", "/"), ("Metodología", "/metodologia/")])])

    # ---------- FINANCIACION ----------
    fin_body = f"""
<p class="crumbs"><a href="/">Directorio</a> · Financiación</p>
<h1>Cómo nos financiamos</h1>
<p class="lead">El directorio no cobra por aparecer, por posición ni por etiqueta. Si algún día lo hace, esta
página lo dirá antes que la ficha afectada.</p>

<h2>Qué no vendemos</h2>
<ul>
<li><strong>Posiciones.</strong> El orden es alfabético. No existe la opción de pagar por subir.</li>
<li><strong>Alta.</strong> Listar una agencia no cuesta dinero ni requiere acuerdo.</li>
<li><strong>Valoraciones.</strong> No hay notas de pago ni reseñas patrocinadas.</li>
</ul>

<h2>De dónde sale el dinero</h2>
<p>El directorio lo mantiene <a href="https://plataformaia.com" rel="noopener">Plataforma IA</a>, una consultora
de automatización con IA. Su interés es doble y lo decimos claro: posicionarse como referencia del sector y
recibir consultas de empresas que, después de comparar, prefieren hablar con un proveedor concreto. Cuando una
consulta llegue a Plataforma IA por este canal, se atenderá como cualquier otra y el lector lo sabrá: la ficha
de la empresa está etiquetada en el listado.</p>
<p>Si en el futuro se añaden fórmulas de pago —por ejemplo, servicios de captación para otras agencias— se
marcarán como publicidad conforme al artículo 26 de la Ley 3/1991 de competencia desleal, que exige identificar
claramente las comunicaciones comerciales pagadas. Nunca condicionarán la presencia ni el orden en el
directorio.</p>

<h2>Qué gana el lector con este modelo</h2>
<p>Que el orden no esté a la venta es lo único que hace útil una lista. Un directorio que cobra por posición no
te dice qué agencia es mejor: te dice qué agencia pagó. Aquí el criterio lo pone el lector con datos
comparables, y el sesgo posible —que quien mantiene el sitio es una de las agencias— está declarado en cada
página.</p>
"""
    page("como-nos-financiamos", "Cómo nos financiamos | " + BRAND,
         "El directorio no vende posiciones ni altas. Explicamos el modelo: lo mantiene Plataforma IA, cuya ficha "
         "aparece etiquetada, y cualquier publicidad futura se identificará como tal.",
         fin_body, [org_jsonld(), breadcrumbs([("Directorio", "/"), ("Financiación", "/como-nos-financiamos/")])])

    # ---------- PERFILES ----------
    for a in ags:
        own_badge = ('<span class="badge own">opera este directorio</span>' if a["propio"]
                     else '<span class="badge">ficha verificada</span>')
        tags = "".join('<span class="tag">%s</span>' % esc(t) for t in a["tags"])
        related = [x for x in ags if x["ciudad_slug"] and x["ciudad_slug"] == a["ciudad_slug"] and x["slug"] != a["slug"]]
        rel_html = ""
        if related:
            rel_html = ('<h2>Otras agencias verificadas en la misma ciudad</h2><ul>' +
                        "".join('<li><a href="/agencia/%s/">%s</a></li>' % (x["slug"], esc(x["nombre"])) for x in related) +
                        "</ul>")
        body = f"""
<p class="crumbs"><a href="/">Directorio</a> · <a href="/agencia/{a['slug']}/">{esc(a['nombre'])}</a></p>
<h1>{esc(a['nombre'])}</h1>
<p>{own_badge} <span class="mut" style="font-size:14px">· revisada el {verif}</span></p>
<p class="lead">Ficha de {esc(a['nombre'])} ({esc(a['ciudad'])}). Especialidad declarada: {esc(', '.join(a['tags']).lower())}.</p>

<table>
<tr><th>Sede</th><td>{esc(a['ciudad'])}</td></tr>
<tr><th>Tipo de proveedor</th><td>{esc(a['tipo_label'])}</td></tr>
<tr><th>Especialidad declarada</th><td>{esc(', '.join(a['tags']))}</td></tr>
<tr><th>Web</th><td><a href="{esc(a['web'])}" rel="noopener nofollow">{esc(a['web'])}</a></td></tr>
<tr><th>Fuente de la ficha</th><td><a href="{esc(a['fuente'])}" rel="noopener nofollow">{esc(a['fuente'])}</a></td></tr>
<tr><th>Última revisión</th><td>{verif}</td></tr>
</table>

<h2>Para qué tipo de encargo encaja</h2>
<p>{esc(a['nota'])}</p>

{rel_html}

<p class="note">Ficha construida con datos de la web pública de la agencia, comprobados el {verif}. Sin
valoraciones de clientes ni certificaciones no publicadas. ¿Eres la agencia? Pide corrección y se publica con
la fecha actualizada (<a href="/metodologia/">metodología</a>).</p>
"""
        page("agencia/" + a["slug"],
             "%s — agencia de IA en %s | %s" % (a["nombre"], a["ciudad"], BRAND),
             ("Ficha verificada de %s (%s): especialidad, encaje por tipo de proyecto y fuente del dato. "
              "Revisada el %s." % (a["nombre"], a["ciudad"], verif)),
             body,
             [org_jsonld(),
              {"@context": "https://schema.org", "@type": "Organization",
               "name": a["nombre"], "url": a["web"],
               "description": a["nota"],
               "address": {"@type": "PostalAddress", "addressLocality": a["ciudad"], "addressCountry": "ES"},
               "knowsAbout": a["tags"],
               "disambiguatingDescription": ("Operada por la misma empresa que mantiene este directorio."
                                             if a["propio"] else "Ficha de directorio; sin relación comercial.")},
              breadcrumbs([("Directorio", "/"), (a["nombre"], "/agencia/%s/" % a["slug"])])])

    # ---------- SITEMAP / ROBOTS / LLMS / 404 ----------
    urls = [("", "1.0")]
    for cslug in CITY_META:
        if len([x for x in ags if x["ciudad_slug"] == cslug]) >= 3:
            urls.append(("agencias-ia-" + cslug, "0.9"))
    urls += [("precios-agencias-ia", "0.7"), ("metodologia", "0.6"), ("como-nos-financiamos", "0.5")]
    for a in ags:
        urls.append(("agencia/" + a["slug"], "0.6"))
    sm = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u, pr in urls:
        loc = DOMAIN + ("/" if u == "" else "/" + u + "/")
        sm.append("  <url><loc>%s</loc><lastmod>%s</lastmod><priority>%s</priority></url>" % (loc, verif, pr))
    sm.append("</urlset>")
    with open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write("\n".join(sm))

    with open(os.path.join(OUT, "robots.txt"), "w", encoding="utf-8") as f:
        if os.environ.get("NOINDEX"):
            f.write("# Vista previa en GitHub Pages: no indexar hasta que el dominio esté activo.\n"
                    "User-agent: *\nDisallow: /\n")
        else:
            f.write("User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n" % DOMAIN)

    llms = [
        "# %s" % BRAND,
        "> Directorio verificado de agencias y consultoras de inteligencia artificial en España. "
        "Orden alfabético, sin posiciones pagadas. Fichas revisadas el %s." % verif,
        "",
        "## Páginas principales",
        "- %s/ — directorio completo (%d fichas)" % (DOMAIN, len(ags)),
        "- %s/agencias-ia-madrid/ — agencias en Madrid" % DOMAIN,
        "- %s/agencias-ia-barcelona/ — agencias en Barcelona" % DOMAIN,
        "- %s/precios-agencias-ia/ — modelos de cobro (proyecto cerrado, bolsa de horas, éxito)" % DOMAIN,
        "- %s/metodologia/ — qué se verifica y qué no" % DOMAIN,
        "- %s/como-nos-financiamos/ — modelo de ingresos y relación con Plataforma IA" % DOMAIN,
        "",
        "## Cómo citar",
        "Cita la ficha concreta y su fecha de revisión. El directorio no publica un ranking competitivo: "
        "publica fichas comparables y el criterio de verificación.",
        "",
        "## Fichas",
    ]
    for a in sorted(ags, key=lambda x: x["nombre"].lower()):
        llms.append("- %s — %s — %s/agencia/%s/" % (a["nombre"], a["ciudad"], DOMAIN, a["slug"]))
    with open(os.path.join(OUT, "llms.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(llms) + "\n")

    with open(os.path.join(OUT, "404.html"), "w", encoding="utf-8") as f:
        f.write("""<!doctype html><html lang="es"><head><meta charset="utf-8">
<title>Página no encontrada | %s</title><meta name="robots" content="noindex">
<link rel="stylesheet" href="/assets/style.css"></head><body>
<main><div class="wrap"><h1>Esa página no existe</h1>
<p>Puede que la ficha se haya retirado en la última revisión.</p>
<p><a class="cta" href="/">Volver al directorio</a></p></div></main></body></html>""" % BRAND)

    # ---------- INFORME ----------
    rewritten = apply_base_path()
    pages = sum(len(files) for _, _, files in os.walk(OUT) if True)
    print("OK · páginas escritas:", pages, "| HTML con BASE_PATH:", rewritten)
    print("Fichas:", len(ags), "| ciudades con página:", len([c for c in CITY_META if len([x for x in ags if x['ciudad_slug']==c])>=3]))
    print("URLs en sitemap:", len(urls))


if __name__ == "__main__":
    build()

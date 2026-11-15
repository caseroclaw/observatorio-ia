# Observatorio IA — directorio de agencias de IA en España

Sitio estático (HTML pre-renderizado, sin JS) del directorio de agencias y consultoras de
inteligencia artificial en España. Dominio previsto: `plataformaia.eu`.

## Estructura

- `data/agencias.json` — fuente de verdad: una ficha por agencia (sede verificada, especialidad
  declarada por la agencia, URL exacta de la fuente y fecha de revisión).
- `build.py` — generador sin dependencias: escribe `site/` completo (HTML, JSON-LD, sitemap,
  `robots.txt`, `llms.txt`, 404).
- `site/` — salida publicada (rama `gh-pages`).

## Reglas editoriales (no negociables)

1. El orden del listado es **alfabético**. No hay posiciones pagadas, ni altas de pago, ni notas
   de valoración sin fuente.
2. Solo se publica ciudad cuando la dirección aparece en la web de la agencia (contacto o aviso
   legal con código postal) o cuando la agencia se describe con esa ciudad en portada. Si no se
   puede comprobar, la ficha dice «España» y no entra en páginas de ciudad.
3. La ficha de Plataforma IA (empresa que opera el directorio) lleva etiqueta visible y queda
   fuera de cualquier selección editorial.
4. Una página de ciudad solo se genera con **3 o más fichas verificadas**; por debajo, es relleno.
5. Cada ficha enlaza su fuente y su fecha de revisión.

## Uso

```bash
python3 build.py          # regenera site/
```

## Publicación

`site/` se publica en GitHub Pages (rama `gh-pages`). Para apuntar el dominio:
`plataformaia.eu` → registros A de GitHub Pages (185.199.108.153, .109.153, .110.153, .111.153)
y `www` → CNAME `caseroclaw.github.io`, además de quitar el redirect 308 actual en el servidor.

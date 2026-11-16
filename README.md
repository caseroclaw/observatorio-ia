# Observatorio IA — directorio de agencias de IA en España

Sitio estático (HTML pre-renderizado, sin JS) del directorio de agencias y consultoras de
inteligencia artificial en España. Dominio previsto: `observatorio.plataformaia.eu`
(el ápice `plataformaia.eu` sigue redirigiendo al `.com`).

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

`site/` se publica en GitHub Pages (rama `gh-pages`) y se sirve en
`observatorio.plataformaia.eu`. Para activarlo basta **un registro CNAME** en dondominio:
`observatorio` → `caseroclaw.github.io`. El ápice `plataformaia.eu` no se toca (sigue redirigiendo
al `.com`). Detalle completo en `GO-LIVE.md`; la activación se hace con `./golive.sh`.

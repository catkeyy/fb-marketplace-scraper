# Funcionamiento

Este script automatiza la obtención de datos públicos en Facebook Marketplace para una búsqueda predefinida y los guarda en un archivo Excel por defecto. La búsqueda por defecto es "ps4" en la zona de Curicó y un radio de 80 km.

## Requerimientos

Asegúrate de tener instalados los siguientes paquetes antes de ejecutar el script:

- [Chromium para Playwright](https://playwright.dev/python/docs/browsers#install-browsers).
- [Playwright](https://playwright.dev/python/) para buscar en el sitio
- [Beautifulsoup4](https://pypi.org/project/beautifulsoup4/) Para obtener el código fuente del sitio
- [unidecode](https://pypi.org/project/Unidecode/) Para formatear bien los strings
- [pandas](https://pypi.org/project/pandas/) Para guardar en excel

## Paso a Paso

### 1. Obtener los enlaces a cada producto

El script `links.py` abre un navegador Chromium y realiza una búsqueda en Marketplace. Por defecto, utiliza la URL: https://www.facebook.com/marketplace/106250626077027/search?daysSinceListed=7&query='ps4'

Donde `106250626077027` es un código interno que define la zona (actualmente Curicó y 80 km alrededor). Para obtener este código para otra zona, puedes hacer una búsqueda manual y copiar el código de la URL.

![Paso 1](gif/1.gif)

### 2. Acceder a cada producto y obtener el HTML

El script accede a cada producto individual, obtiene campos como título, precio, clasificación, días desde la publicación máxima, ubicación, estado del producto, detalles y enlace.

![Paso 2](gif/2.gif)

Para mejorar el rendimiento, se recomienda utilizar `headless=True` al lanzar el navegador:
```python
browser = p.chromium.launch(headless=True)


al final escribirá un archivo productos.xlsx



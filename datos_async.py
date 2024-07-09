# datos_async.py
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
import asyncio
import re
from unidecode import unidecode

async def async_consigue_datos(max_dias_publicacion: int, links: list = None):
    datos = []
    async with async_playwright() as p:
        for link_producto in links:
            try:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()

                await page.set_viewport_size({"width": 1720, "height": 1280})

                await page.goto(link_producto)

                # Esperar un poco para asegurar que la página haya cargado
                await asyncio.sleep(2)

                # Cerrar botón de iniciar sesión si existe
                selector = 'div[aria-label="Cerrar"]'
                element = page.locator(selector).first
                if element:
                    await element.click()
                    print(f"Se hizo clic en el elemento con selector '{selector}'")
                else:
                    print(f"No se encontró ningún elemento con el selector '{selector}'")

                print("Consiguiendo datos...")

                html = await page.content()
                soup = BeautifulSoup(html, 'html.parser')

                meta_tags = soup.find_all('meta')  # Descripciones
                title_tag = soup.find('title')  # Títulos
                script_tags = soup.find_all('script')  # Precios en JSON {"formatted_amount_zeros_stripped":"$150.000"}

                # Título del producto
                titulo_producto = ""
                if title_tag:
                    contenido_titulo = title_tag.text.strip()
                    titulo_producto = contenido_titulo
                else:
                    titulo_producto = None
                    print("TITULO NO ENCONTRADO")

                # Precio, buscar con expresiones regulares
                patron_precio = re.compile(r'formatted_amount_zeros_stripped":"(\$[\d,\.]+)"')

                precio_producto = ""
                for script in script_tags:
                    script_content = script.string
                    if script_content:
                        # Aplicar la búsqueda con regex
                        matches_precio = patron_precio.findall(script_content)

                        # Imprimir los resultados encontrados
                        for match in matches_precio:
                            precio_producto = match

                # Clasificación
                patron_clasificacion = re.compile(r'\{"name":"([^"]+)","seo_info"')

                clasificacion_producto = ""
                for script in script_tags:
                    script_content = script.string
                    if script_content:
                        # Buscar coincidencias del patrón
                        matches_clasificacion = patron_clasificacion.findall(script_content)

                        for match in matches_clasificacion:
                            clasificacion_producto += " " + unidecode(match.encode().decode('unicode_escape'))

                # Fecha aproximada
                fecha_publicacion_aprox_producto = max_dias_publicacion

                # Ubicación
                ubicacion_producto = ""
                patron_ciudad = re.compile(r'\{"reverse_geocode":\{"city":"([^"]+)"\}\}')
                for script in script_tags:
                    script_content = script.string
                    if script_content:
                        # Buscar coincidencias del patrón
                        matches_ciudad = patron_ciudad.findall(script_content)

                        for match in matches_ciudad:
                            ubicacion_producto = unidecode(match.encode().decode('unicode_escape'))

                # Estado del producto
                estado_producto = ""
                patron_estado = re.compile(r'\[{"attribute_name":"[^"]*","value":"[^"]*","label":"([^"]+)"}\]')
                for script in script_tags:
                    script_content = script.string
                    if script_content:
                        # Aplicar la búsqueda con regex
                        matches_estado = patron_estado.findall(script_content)

                        # Imprimir los resultados encontrados
                        for match in matches_estado:
                            estado_producto = match

                # Detalles del producto
                detalles_producto = ""
                for meta in meta_tags:
                    if meta.get('name') == 'description':
                        descripcion_producto = meta.get('content')
                        detalles_producto = descripcion_producto
                        break

                # Guardar los datos del producto en la lista
                datos.append({
                    "titulo": titulo_producto,
                    "precio": precio_producto,
                    "clasificacion": clasificacion_producto,
                    "ubicacion": ubicacion_producto,
                    "estado_producto": estado_producto,
                    "max_dias_publicacion": fecha_publicacion_aprox_producto,
                    "detalles_producto": detalles_producto,
                    "enlace": link_producto
                })

            except Exception as e:
                print(f"Error en {link_producto}: {e}")

            finally:
                await browser.close()

    return datos

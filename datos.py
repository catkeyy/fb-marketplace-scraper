"""
    Este script consigue datos NO CONFIDENCIALES 
    de los links de un producto random de marketplace
    
    Requiere tener el link al producto.
    
    Se almacenan en una lista de diccionarios
    [
        { titulo: "",
          precio: "",
          clasificacion: "",
          max_dias_publicacion: "",
          ubicacion: "",
          estado_producto: "",
          detalles: "",
          link: ""
        },
        ,.... (y más) 
    ]
"""
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import time
import re
from unidecode import unidecode


def consigue_datos(max_dias_publicacion : int, links : list = None):
    #link_producto = 'https://www.facebook.com/marketplace/item/8322096264486870/?ref=search&referral_code=null&referral_story_type=post&__tn__=!%3AD'
    
    datos = []
    total_productos = len(links)
    contador = 0
    for link_producto in links:
        with sync_playwright() as p:
            try:
                browser = p.chromium.launch(headless=False)
                page = browser.new_page()

                page.set_viewport_size({"width": 1720, "height": 1280})

                page.goto(link_producto)

                time.sleep(2)  # Esperar un poco para asegurar que la página haya cargado

                #Cerrar boton de iniciar sesion
                selector = 'div[aria-label="Cerrar"]'
                element = page.locator(selector)
                if element:
                    element.click()
                    #print(f"Se hizo clic en el elemento con selector '{selector}'")
                else:
                    print(f"No se encontró ningún elemento con el selector '{selector}'")    
                
                contador+=1
                print(f"Consiguiendo datos: {contador}/{total_productos}...")
                
                html = page.content()
                soup = BeautifulSoup(html, 'html.parser')
                
                meta_tags = soup.find_all('meta') # Descripciones 
                title_tag = soup.find('title') # Titulos
                script_tags = soup.find_all('script') # precios --> estan en un json {"formatted_amount_zeros_stripped":"$150.000"}
            
                # Titulo del producto
                
                titulo_producto = ""
                if title_tag:
                    contenido_titulo = title_tag.text.strip()
                    titulo_producto = contenido_titulo
                else:
                    titulo_producto = None
                    print("TITULO NO ENCONTRADO")
                
                #print("TITULO PRODUCTO: ", titulo_producto)
                
                # Precio, lo buscamos con expresiones regulares :D
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
                
                #print ("PRECIO: ", precio_producto)
                
                # Clasificacion
                    
                patron_clasificacion = re.compile(r'\{"name":"([^"]+)","seo_info"')

                #Iterar sobre los script_tags
                clasificacion_producto = ""
                for script in script_tags:
                    script_content = script.string
                    if script_content:
                        # Buscar coincidencias del patrón
                        matches_clasificacion = patron_clasificacion.findall(script_content)
                        
                        for match in matches_clasificacion:
                            clasificacion_producto += " " + unidecode(match.encode().decode('unicode_escape'))
                            
                #print("CLASIFICACION: ", clasificacion_producto)
                        
                # Fecha aproximada 
                fecha_publicacion_aprox_producto = max_dias_publicacion
                #print("MAX DIAS PUBLICACION", fecha_publicacion_aprox_producto)
                
                # Ubicacion
                ubicacion_producto = ""
                patron_ciudad = re.compile(r'\{"reverse_geocode":\{"city":"([^"]+)"\}\}')
                for script in script_tags:
                    script_content = script.string
                    if script_content:
                        # Buscar coincidencias del patrón
                        matches_ciudad = patron_ciudad.findall(script_content)
                        
                        for match in matches_ciudad:
                            ubicacion_producto = unidecode(match.encode().decode('unicode_escape'))
                
                #print("UBICACION: ", ubicacion_producto)    
                
                #Estado del producto
                
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
                #print("ESTADO DEL PRODUCTO: ", estado_producto)
                

                # Detalles del producto
                detalles_producto = ""
                for meta in meta_tags:
                    if meta.get('name') == 'description':
                        descripcion_producto = meta.get('content')
                        detalles_producto = descripcion_producto
                        break
                    else:
                        descripcion_producto = None
                
                #print("DETALLES DEL PRODUCTO: \n", detalles_producto)
                # Link

                            

                # añadimos...
                datos.append({
                    "titulo": titulo_producto,
                    "precio": precio_producto,
                    "clasificacion": clasificacion_producto,
                    "ubicacion" : ubicacion_producto,
                    "estado_producto" : estado_producto,
                    "max_dias_publicacion" : fecha_publicacion_aprox_producto,
                    "detalles_producto" : detalles_producto,
                    "enlace" : link_producto 
                })
                
                #print(datos)

            except Exception as e:
                print(f"Error: {e}")

            finally:
                browser.close()
    return datos


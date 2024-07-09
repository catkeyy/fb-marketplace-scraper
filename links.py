import re
import codecs
import random
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import time

# URL de la página web

# https://www.facebook.com/marketplace/106250626077027/search?daysSinceListed=7&query='ps4'

def consigue_links(max_dias_publicacion, consulta, pasos_scroll: int = 100):
    
    # default curico con 7 dias como maximo
    url = f'https://www.facebook.com/marketplace/106250626077027/search?daysSinceListed={max_dias_publicacion}&query={consulta}' 
    
    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()

            page.set_viewport_size({"width": 1720, "height": 1280})
            # Navegar a la URL marketplace
            page.goto(url)

            time.sleep(2)  # Esperar un poco para asegurar que la página haya cargado

            #Cerrar boton de iniciar sesion
            selector = 'div[aria-label="Cerrar"]'
            element = page.locator(selector)
            if element:
                element.click()
                print(f"Se hizo clic en el elemento con selector '{selector}'")
            else:
                print(f"No se encontró ningún elemento con el selector '{selector}'")
            
            time.sleep(2)
            print("haciendo scroll...")
            
            # Scroll hacia abajo
            paso_arbitrario = pasos_scroll
            for _ in range(0, paso_arbitrario):
                page.evaluate("""
                            () => {
                                window.scrollBy(0,100);
                            }
                            """)
                time.sleep(random.randint(0,10)/100)
            
            print("Consiguiendo links...")
            time.sleep(2)

            html = page.content()

            # Crear objeto BeautifulSoup
            soup = BeautifulSoup(html, 'html.parser')
            
            #todos los a que sean links y tengan el rol link
            links_bruto = soup.find_all('a', attrs={'role': 'link', 'href': True})

            links_limpios = []
            for link_sucio in links_bruto:
                links_limpios.append(f"https://www.facebook.com{link_sucio['href']}")
            
            #for link in links_limpios:
            #    print(link)
                
            #Descarta los que no sean de marketplace
            links_validos = [link for link in links_limpios if link.startswith("https://www.facebook.com/marketplace/item/")]
                
            #for link in links_validos:
            #    print(link)
            #print(f"Total de links encontrados: {len(links_validos)}")

        except Exception as e:
            print(f"Error: {e}")

        finally:
            browser.close()
            return links_validos, f"Total de links encontrados: {len(links_validos)}"

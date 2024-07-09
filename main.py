from links import consigue_links
from datos import consigue_datos
from datos_async import async_consigue_datos
import pandas as pd
import asyncio


# TODO: Terminar la versión asincrona
async def async_main(links):
    datos_productos = await async_consigue_datos(max_dias_publicacion, links)
    return datos_productos
    
 
def enlaces(max_dias_publicacion, consulta, pasos_scroll):
    links, cantidad_links = consigue_links(max_dias_publicacion, consulta, pasos_scroll)
    print("\n\nCantidad de links encontrados: ", cantidad_links, "\n\n")
    return links

def main(links):
    datos= consigue_datos(max_dias_publicacion, links)
    escribir_excel(datos)

def escribir_excel(datos_productos):
    df = pd.DataFrame(datos_productos)
    df.to_excel('productos.xlsx', index=False)

    
if __name__ == '__main__':
    
    max_dias_publicacion = 7
    consulta = 'ps4'
    pasos_scroll = 100 # valores altos más productos

    links = enlaces(max_dias_publicacion, consulta, pasos_scroll)
    for link in links:
        print(link)
    main(links)
    print("Listo.")
    
    #datos_async = asyncio.run(async_main(links))
    #escribir_excel(datos_async)


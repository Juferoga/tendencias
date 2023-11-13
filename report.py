from weasyprint import HTML
import os

def generar_html_con_imagenes(directorio_imagenes):
    """ Genera una cadena HTML con imágenes incrustadas desde un directorio dado. """
    imagenes = os.listdir(directorio_imagenes)
    imagenes_html = "".join([f'<img src="{directorio_imagenes}/{img}" style="width:100%"><br><br>' for img in imagenes if img.endswith('.png')])

    html_content = f"""
    <html>
        <head>
            <title>Informe de Análisis</title>
        </head>
        <body>
            <h1>Análisis de Datos</h1>
            {imagenes_html}
        </body>
    </html>
    """
    return html_content

def crear_pdf(html_content, ruta_salida):
    """ Crea un archivo PDF a partir de una cadena HTML. """
    HTML(string=html_content).write_pdf(ruta_salida)

if __name__ == "__main__":
    directorio_imagenes = './reporte/imagenes'
    archivo_pdf = './reporte/informe.pdf'

    # Generar el contenido HTML con las imágenes
    html = generar_html_con_imagenes(directorio_imagenes)

    # Crear el archivo PDF
    crear_pdf(html, archivo_pdf)

    print(f"Informe generado con éxito en {archivo_pdf}")

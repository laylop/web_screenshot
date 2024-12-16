import json
import os
import sys
import time
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image


def extract_domain(url):
    """
    Extrae el nombre de dominio de una URL
    Elimina prefijos como 'www.' y extensiones como '.com'
    """
    parsed_url = urlparse(url)
    domain = parsed_url.netloc

    # Eliminar 'www.' si existe
    if domain.startswith('www.'):
        domain = domain[4:]

    # Eliminar extensión como '.com', '.es', etc.
    domain = domain.split('.')[0]

    return domain


def load_progress(progress_file):
    """Cargar el progreso anterior"""
    if os.path.exists(progress_file):
        with open(progress_file, 'r') as f:
            return int(f.read().strip())
    return 0


def save_progress(progress_file, last_processed_id):
    """Guardar el último ID procesado"""
    with open(progress_file, 'w') as f:
        f.write(str(last_processed_id))


def capture_website_screenshots(json_file, screenshot_dir, batch_size=10):
    # Archivo para rastrear el progreso
    progress_file = os.path.join(os.path.dirname(
        json_file), 'screenshot_progress.txt')

    # Configurar opciones de Chrome/Brave
    chrome_options = ChromeOptions()
    chrome_options.add_argument("--headless")  # Ejecutar en modo sin cabeza

    # Ruta a Brave (ajusta para Windows)
    brave_path = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
    chrome_options.binary_location = brave_path

    # Configurar el servicio del webdriver
    service = Service(ChromeDriverManager().install())

    # Crear directorio para guardar screenshots si no existe
    if not os.path.exists(screenshot_dir):
        os.makedirs(screenshot_dir)

    # Cargar datos del JSON
    with open(json_file, 'r', encoding='utf-8') as file:
        golf_courses = json.load(file)

    # Cargar el último punto de progreso
    last_processed_id = load_progress(progress_file)

    # Filtrar cursos que aún no han sido procesados
    pending_courses = [
        course for course in golf_courses if course['id'] > last_processed_id]

    # Inicializar el navegador
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # Procesar en lotes
        for i in range(0, len(pending_courses), batch_size):
            # Obtener el lote actual
            batch = pending_courses[i:i+batch_size]

            print(f"\n--- Procesando lote {i//batch_size + 1} ---")

            # Procesar cada curso en el lote
            for course in batch:
                # Saltar entradas con web vacía
                if not course['web'] or course['web'].strip() == '':
                    print(f"Saltando {course['name']} - Web vacía")
                    continue

                try:
                    # Navegar a la web del campo de golf
                    driver.get(course['web'])

                    # Esperar un poco para que cargue la página
                    driver.implicitly_wait(10)

                    # Añadir un pequeño retraso para evitar sobrecargar el servidor
                    time.sleep(2)

                    # Generar nombre de archivo con ID y dominio
                    domain = extract_domain(course['web'])
                    screenshot_filename = f"{course['id']}_{domain}.png"
                    screenshot_path = os.path.join(
                        screenshot_dir, screenshot_filename)

                    # Capturar screenshot
                    driver.save_screenshot(screenshot_path)

                    print(f"Screenshot capturado para {
                          course['name']}: {screenshot_filename}")

                    # Guardar el progreso
                    save_progress(progress_file, course['id'])

                except Exception as e:
                    print(f"Error capturando screenshot para {
                          course['name']}: {e}")

            # Pequeña pausa entre lotes para no sobrecargar recursos
            time.sleep(5)

    finally:
        # Cerrar el navegador
        driver.quit()

    print("Proceso de screenshots completado.")


# Rutas configurables
BASE_DIR = r"C:\Users\shala\OneDrive\Documentos\VsApp\_Py\web_screenshot"
JSON_FILE = os.path.join(BASE_DIR, 'items.json')
SCREENSHOT_DIR = os.path.join(BASE_DIR, 'img')

# Uso del script
if __name__ == "__main__":
    capture_website_screenshots(JSON_FILE, SCREENSHOT_DIR)

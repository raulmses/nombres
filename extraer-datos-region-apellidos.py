import requests
import csv
import urllib.parse

# Nombres de los archivos de entrada y salida
primer_apellido_file = r'C:\Users\Raul\Desktop\Infonombres\nombres\URLs\primer-apellido-mapa.txt'
output_file = r'C:\Users\Raul\Desktop\Infonombres\nombres\Outputs\output-mapa-apellidos.csv'

# Función para extraer la información de las URLs
def fetch_data_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Verificar errores HTTP
        json_data = response.json()  # Parsear el JSON

        # Extraer datos de 'regiones'
        regiones = json_data.get('regiones', [])
        if regiones:  # Verificar si hay datos en 'regiones'
            return ", ".join(
                f"{region['id']}:{region['val']}" for region in regiones
            )
        else:
            return 'No hay datos en regiones'
    except Exception as e:
        print(f"Error al procesar la URL {url}: {e}")
        return f"Error: {e}"

# Leer URLs de un archivo
def read_urls_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file.readlines() if line.strip()]

# Generar datos combinados y guardarlos en un CSV
def generate_combined_data(file1, output_path):
    urls_primero = read_urls_from_file(file1)

    combined_data = []
    total_urls = len(urls_primero)  # Número total de URLs
    for index, url1 in enumerate(urls_primero, start=1):
        print(f"Procesando URL {index}/{total_urls} para el primer apellido...")
        # Decodificar la URL para corregir problemas de codificación
        url1_decoded = urllib.parse.unquote(url1)
        apellido = url1_decoded.split('=')[1].split('&')[0]  # Extraer apellido de la URL
        data1 = fetch_data_from_url(url1_decoded)  # Información del primer apellido

        # Modificar la URL para el segundo apellido
        url2_decoded = url1_decoded.replace("=1", "=2")
        print(f"Procesando URL {index}/{total_urls} para el segundo apellido...")
        data2 = fetch_data_from_url(url2_decoded)  # Información del segundo apellido

        combined_data.append({'apellido': apellido, 'data1': data1, 'data2': data2})

    # Guardar en el archivo CSV
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['apellido', 'data1', 'data2']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(combined_data)

    print(f"Datos guardados en {output_path}")

# Ejecutar el proceso
generate_combined_data(primer_apellido_file, output_file)

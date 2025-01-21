import requests
import csv

# Nombre del archivo con las URLs y nombre del archivo de salida
input_file = r'C:\Users\raulmses\Desktop\Proyecto nombre\nombres\URLs\mapa-urls.txt'
output_file = r'C:\Users\raulmses\Desktop\Proyecto nombre\nombres\Outputs\output-mapa.csv'

# Función para extraer la información
def fetch_data_from_urls(file_path):
    data = []
    with open(file_path, 'r') as file:
        urls = file.readlines()
        total_urls = len(urls)  # Total de URLs
        for i, url in enumerate(urls, start=1):
            url = url.strip()
            if url:  # Asegurarse de que no hay líneas vacías
                try:
                    print(f"Procesando {i}/{total_urls}: {url}")  # Mostrar progreso
                    response = requests.get(url)
                    response.raise_for_status()  # Verificar errores HTTP
                    json_data = response.json()  # Parsear el JSON

                    # Extraer datos de 'regiones'
                    regiones = json_data.get('regiones', [])
                    if regiones:  # Verificar si hay datos en 'regiones'
                        combined_data = ", ".join(
                            f"{region['id']}:{region['val']}" for region in regiones
                        )
                        data.append({'url': url, 'data': combined_data})
                    else:
                        data.append({'url': url, 'data': 'No hay datos en regiones'})
                except Exception as e:
                    print(f"Error al procesar la URL {url}: {e}")
                    data.append({'url': url, 'data': f"Error: {e}"})
    return data

# Guardar los datos en un CSV
def save_to_csv(data, output_path):
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['url', 'data']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

# Ejecutar el proceso
urls_data = fetch_data_from_urls(input_file)
save_to_csv(urls_data, output_file)

print(f"Datos guardados en {output_file}")

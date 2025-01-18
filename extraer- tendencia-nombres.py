import requests
import csv

# Nombre del archivo con las URLs y nombre del archivo de salida
input_file = 'urls.txt'
output_file = 'output.csv'

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

                    # Extraer información
                    values = json_data.get('values', [[]])[0]  # Tomar el primer conjunto de valores
                    series = json_data.get('series', [])
                    label = series[0].get('label') if series else 'Sin etiqueta'
                    ticks = json_data.get('ticks', [])

                    data.append({
                        'url': url,
                        'label': label,
                        'values': values,
                        'ticks': ticks
                    })
                except Exception as e:
                    print(f"Error al procesar la URL {url}: {e}")
                    data.append({'url': url, 'label': 'Error', 'values': f"Error: {e}", 'ticks': []})
    return data

# Guardar los datos en un CSV
def save_to_csv(data, output_path):
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['url', 'label', 'values', 'ticks']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow({
                'url': row['url'],  # Añadir la URL en el CSV
                'label': row['label'],
                'values': ', '.join(map(str, row['values'])),  # Convertir valores a cadena
                'ticks': ', '.join(row['ticks'])  # Convertir ticks a cadena
            })

# Ejecutar el proceso
urls_data = fetch_data_from_urls(input_file)
save_to_csv(urls_data, output_file)

print(f"Datos guardados en {output_file}")

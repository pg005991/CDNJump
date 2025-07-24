import re
from bs4 import BeautifulSoup

def similarity_percentage(text1: str, text2: str) -> int:
    """
    Calcula el porcentaje de similitud entre dos textos basado en las palabras únicas.

    Se consideran las palabras únicas en cada texto y se calcula el porcentaje
    de palabras comunes respecto al total de palabras únicas. Si alguno de los textos
    está vacío, se retorna 0.

    Ejemplo:
      similarity_percentage("gato perro", "gato casa") -> 33
      (La intersección es {"gato"} y la unión es {"gato", "perro", "casa"})

    Parámetros:
      text1 (str): Primer texto a comparar.
      text2 (str): Segundo texto a comparar.

    Retorna:
      int: Porcentaje de similitud redondeado al entero más cercano.
    """
    # Si alguno de los textos es vacío, se retorna 0
    if not text1.strip() or not text2.strip():
        return 0

    # Dividir los textos en palabras y obtener conjuntos de palabras únicas
    words1 = set(text1.split())
    words2 = set(text2.split())

    # Calcular la intersección y la unión de ambos conjuntos
    common_words = words1.intersection(words2)
    total_words = words1.union(words2)

    if not total_words:
        return 0

    similarity = (len(common_words) / len(total_words)) * 100
    return int(round(similarity))


def read_and_normalize_html(file_path: str) -> str:
    """
    Extrae y normaliza el texto de un archivo HTML.

    La función realiza lo siguiente:
      1. Lee el contenido del archivo HTML.
      2. Utiliza BeautifulSoup para extraer todo el texto de las etiquetas HTML.
      3. Convierte el texto a minúsculas.
      4. Normaliza los espacios, eliminando espacios redundantes.

    Parámetros:
      file_path (str): Ruta al archivo HTML.

    Retorna:
      str: Texto extraído y normalizado.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
    except Exception as e:
        raise Exception(f"Error al leer el archivo HTML: {e}")

    # Extraer el texto usando BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    # El parámetro separator=' ' asegura que se inserten espacios entre los textos extraídos
    text = soup.get_text(separator=' ', strip=True)

    # Convertir a minúsculas
    text = text.lower()

    # Normalizar espacios: reemplaza múltiples espacios por uno solo
    text = re.sub(r'\s+', ' ', text)

    return text.strip()

import pytest
from cdnjump.validation import similarity_percentage, read_and_normalize_html

def test_similarity_percentage_identical():
    """
    Prueba que dos textos idénticos tengan una similitud del 100%.
    """
    text = "Esto es una prueba de similitud"
    result = similarity_percentage(text, text)
    assert result == 100, f"Se esperaba 100, se obtuvo {result}"

def test_similarity_percentage_completely_different():
    """
    Prueba que dos textos sin palabras en común tengan una similitud del 0%.
    """
    text1 = "Gato perro"
    text2 = "Manzana naranja"
    result = similarity_percentage(text1, text2)
    assert result == 0, f"Se esperaba 0, se obtuvo {result}"

def test_similarity_percentage_partial():
    """
    Prueba la similitud de dos textos parcialmente similares.
    Por ejemplo:
      Texto1: "El rápido zorro marrón salta sobre el perro perezoso"
      Texto2: "El zorro salta sobre el perro"
    Se espera una similitud alrededor del 62-63%.
    """
    text1 = "El rápido zorro marrón salta sobre el perro perezoso"
    text2 = "El zorro salta sobre el perro"
    result = similarity_percentage(text1, text2)
    assert 65 <= result <= 70, f"Se esperaba una similitud entre 60 y 65, se obtuvo {result}"

def test_similarity_percentage_empty():
    """
    Prueba que si alguno de los textos está vacío se retorne 0.
    """
    assert similarity_percentage("", "algo") == 0
    assert similarity_percentage("algo", "") == 0

def test_read_and_normalize_html(tmp_path):
    """
    Crea un archivo HTML temporal, extrae el texto con read_and_normalize_html y verifica
    que se realice la normalización (por ejemplo, pasando a minúsculas y eliminando espacios extra).
    """
    # Contenido HTML de prueba
    html_content = """
    <html>
      <head><title>Prueba</title></head>
      <body>
        <h1>Hola Mundo</h1>
        <p>Esta es una   prueba de   normalización.</p>
      </body>
    </html>
    """
    # Crear el archivo temporal
    html_file = tmp_path / "test.html"
    html_file.write_text(html_content, encoding="utf-8")
    
    # Ejecutar la función que extrae y normaliza el texto
    result = read_and_normalize_html(str(html_file))
    
    # Verificar que el resultado esté en minúsculas y sin espacios redundantes
    expected_phrases = ["hola mundo", "esta es una prueba de normalización"]
    result_lower = result.lower()
    for phrase in expected_phrases:
        assert phrase in result_lower, f"No se encontró la frase '{phrase}' en el resultado: {result_lower}"

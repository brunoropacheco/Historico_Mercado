from src.utils.ocr_parser import extract_text, parse_text

def process_image(image_path):
    """
    Processa uma única imagem de nota:
      1) OCR → texto
      2) Parsing → dados estruturados
    Retorna dicionário com todos os campos.
    """
    raw_text = extract_text(image_path)
    print(f"Texto extraído: {raw_text}")  # Debug: mostrar o texto extraído
    data = parse_text(raw_text)
    # Aqui você poderia adicionar validações, enriquecimentos, etc.
    return data

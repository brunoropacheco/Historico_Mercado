# ATENÇÃO: Para utilizar o pytesseract, é necessário ter o Tesseract OCR instalado na máquina.
# pytesseract é apenas uma interface para o motor Tesseract.
#
# Instalação do Tesseract OCR e pacote de idioma Português (Exemplo para Debian/Ubuntu):
# 1. Instalar o Tesseract OCR:
#    sudo apt-get update
#    sudo apt-get install tesseract-ocr
#
# 2. Instalar o pacote de idioma para Português:
#    sudo apt-get install tesseract-ocr-por
#
# Para outros sistemas operacionais, consulte a documentação oficial do Tesseract.
# Certifique-se de que o Tesseract está no PATH do sistema após a instalação.

import re
import cv2
from pyzbar.pyzbar import decode
import urllib.parse

def extrair_chave(image_path):
    """
    Extrai a chave de acesso da nota fiscal lendo o QR code presente na imagem.
    QR codes de NFC-e geralmente contêm uma URL que inclui a chave de acesso.
    """
    # Carregar a imagem
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Não foi possível ler a imagem: {image_path}")
    
    # Tentar diferentes pré-processamentos se necessário
    images_to_try = [
        image,  # Imagem original
        cv2.cvtColor(image, cv2.COLOR_BGR2GRAY),  # Versão em escala de cinza
    ]
    
    # Tentar decodificar QR code em cada versão da imagem
    qr_data = None
    for img in images_to_try:
        # Decodificar todos QR codes encontrados na imagem
        decoded_objects = decode(img)
        
        if decoded_objects:
            # Usar o primeiro QR code encontrado
            qr_data = decoded_objects[0].data.decode('utf-8')
            print(f"QR Code detectado com conteúdo: {qr_data}")
            break
    
    if not qr_data:
        raise ValueError("Nenhum QR code encontrado na imagem.")
    
    # Padrões para extração da chave em diferentes formatos de URL de NFC-e
    url_patterns = [
        # Formato padrão: p=CHAVE_ACESSO (44 dígitos)
        r'[?&]p=(\d{44})',
        # Formato alternativo: chNFe=CHAVE_ACESSO
        r'[?&]chNFe=(\d{44})',
        # Formato com URL encoded: p=VALOR_ENCODED
        r'[?&]p=([^&]+)',
    ]
    
    # Tentar extrair a chave da URL
    for pattern in url_patterns:
        match = re.search(pattern, qr_data)
        if match:
            chave_candidata = match.group(1)
            
            # Se for URL encoded, decodificar
            if not chave_candidata.isdigit():
                chave_candidata = urllib.parse.unquote(chave_candidata)
            
            # Limpar caracteres não numéricos
            chave_candidata = re.sub(r'\D', '', chave_candidata)
            
            if len(chave_candidata) == 44:
                # Formato legível para visualização
                chave_formatada = ' '.join([chave_candidata[i:i+4] for i in range(0, len(chave_candidata), 4)])
                #print(f"✅ Chave válida extraída do QR code: {chave_formatada}")
                return chave_candidata
    
    # Se não encontrou pelos padrões, mas o QR code contém uma sequência de 44 dígitos
    digits_match = re.search(r'(\d{44})', qr_data)
    if digits_match:
        chave = digits_match.group(1)
        print(f"✅ Chave encontrada diretamente no QR code: {chave}")
        return chave
    
    raise ValueError(f"Não foi possível extrair a chave de acesso do QR code: {qr_data}")
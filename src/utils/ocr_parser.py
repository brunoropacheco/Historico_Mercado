import pytesseract
from PIL import Image
import re
import datetime

def extract_text(image_path):
    """Retorna o texto bruto extraído da imagem."""
    img = Image.open(image_path)
    return pytesseract.image_to_string(img, lang='por')  # ou 'eng', conforme sua nota

def parse_text(raw_text):
    """
    Converte o texto cru em dados estruturados:
      - data: ISO format
      - estabelecimento, cnpj
      - items: [{descricao, quantidade, unidade, preco_unitario, preco_total}, ...]
    """
    # Exemplo simples de extração de data (formato DD/MM/YYYY)
    data_match = re.search(r'\b(\d{2}/\d{2}/\d{4})\b', raw_text)
    data = None
    if data_match:
        data = datetime.datetime.strptime(data_match.group(1), '%d/%m/%Y').date().isoformat()

    # Estabelecimento (linha antes de CNPJ, por exemplo)
    estab_match = re.search(r'(.+?)\s+CNPJ', raw_text)
    estabelecimento = estab_match.group(1).strip() if estab_match else None

    # CNPJ
    cnpj_match = re.search(r'CNPJ[:\s]*([\d./-]+)', raw_text)
    cnpj = re.sub(r'\D', '', cnpj_match.group(1)) if cnpj_match else None

    # Itens: linha por linha buscando padrões como "1x Produto ... R$ 4,59"
    items = []
    for line in raw_text.splitlines():
        m = re.match(r'(\d+)x\s+(.+?)\s+R\$?\s*([\d.,]+)', line)
        if m:
            qtd = int(m.group(1))
            desc = m.group(2).strip()
            preco = float(m.group(3).replace('.', '').replace(',', '.'))
            items.append({
                'descricao': desc,
                'quantidade': qtd,
                'unidade': None,            # preencher se detectar unidade no desc
                'preco_unitario': preco,
                'preco_total': preco * qtd
            })

    return {
        'data': data,
        'estabelecimento': estabelecimento,
        'cnpj': cnpj,
        'items': items
    }

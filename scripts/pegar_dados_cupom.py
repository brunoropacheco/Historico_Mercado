import requests
from bs4 import BeautifulSoup
import re
import datetime
import os


def extrair_dados_cupom(chave_original):
    """
    Extrai dados de uma nota fiscal a partir da chave de acesso.
    Se a consulta online falhar, tenta usar o arquivo HTML existente.
    Retorna os dados extraídos ou None em caso de erro completo.
    """
    # Caminho do arquivo HTML de saída
    html_path = "resposta_consulta.html"
    
    try:
        # URL da consulta
        url = 'https://consultadfe.fazenda.rj.gov.br/consultaDFe/paginas/consultaChaveAcesso.faces'

        # Formatar a chave com + a cada 4 dígitos
        chave_formatada = ""
        for i in range(0, len(chave_original), 4):
            if i > 0:
                chave_formatada += "+"
            chave_formatada += chave_original[i:i+4]

        #print(f"Chave formatada: {chave_formatada}")

        # Configurar um User-Agent válido
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Sec-Ch-Ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
        }

        # Criar uma sessão para manter cookies entre requisições
        session = requests.Session()
        session.headers.update(headers)

        # Passo 1: Fazer o GET inicial para obter cookies e ViewState
        print("Fazendo requisição GET para obter cookies e ViewState...")
        response_get = session.get(url)
        
        if response_get.status_code != 200:
            print(f"AVISO: GET initial falhou com status code {response_get.status_code}")
            print(response_get.text[:1000])
            # Em vez de exit(1), retornamos para usar o arquivo existente
            raise Exception(f"GET falhou: {response_get.status_code}")
        
        # Extrair o ViewState com BeautifulSoup
        soup = BeautifulSoup(response_get.text, 'html.parser')
        view_state_element = soup.find('input', {'name': 'javax.faces.ViewState'})
        
        if not view_state_element or 'value' not in view_state_element.attrs:
            print("AVISO: Não foi possível encontrar o javax.faces.ViewState na página")
            # Em vez de exit(1), retornamos para usar o arquivo existente
            raise Exception("ViewState não encontrado")
        
        view_state = view_state_element['value']
        #print(f"ViewState capturado: {view_state}")
        
        # Mostrar cookies capturados
        #print("Cookies capturados:")
        #for cookie in session.cookies:
        #    print(f"  {cookie.name}: {cookie.value}")
        
        # Passo 2: Preparar o payload do POST
        payload = (
            f"formulario=formulario"
            f"&chaveAcesso={chave_formatada}"
            f"&j_idt37=1"
            f"&consultar="
            f"&javax.faces.ViewState={view_state}"
        )
        
        print("\nFazendo requisição POST...")
        
        # Passo 3: Fazer o POST com os cookies e ViewState capturados
        post_headers = headers.copy()
        post_headers['Content-Type'] = 'application/x-www-form-urlencoded'
        post_headers['Referer'] = url
        
        response_post = session.post(url, data=payload, headers=post_headers)
        
        print(f"Status Code da resposta da requisicao POST: {response_post.status_code}")
        print(response_post.text[:500])  # Exibir os primeiros 500 caracteres da resposta
        # Passo 4: Verificar se a resposta contém resultado ou foi bloqueada
        bloqueio_strings = [
            "solicitação foi bloqueada",
            "acesso bloqueado",
            "bloqueado por questões de segurança",
            "bloqueio temporário",
            "bloqueio permanente",
            "bloqueio de acesso"
        ]
        if any(b in response_post.text.lower() for b in bloqueio_strings):
            print("AVISO: A solicitação foi bloqueada. Nenhum arquivo será salvo.")
            raise Exception("Solicitação bloqueada")

        # Salvar a resposta em um arquivo
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(response_post.text)

        #print("\nPrimeiros 500 caracteres da resposta:")
        #print(response_post.text[:500])
        print("\nResposta completa salva em 'resposta_consulta.html'")
        
        # Extrair dados do HTML recém-baixado
        return extrair_dados_html(html_path)
    except Exception as e:
        print(f"Erro ao fazer a requisição: {e}")
        return e

def extrair_dados_html(path_html):
    with open(path_html, encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    # Nome da empresa
    empresa = soup.find('div', class_='txtTopo')
    nome_empresa = empresa.get_text(strip=True) if empresa else ''

    # CNPJ
    cnpj_div = soup.find('div', class_='text', string=lambda t: t and 'CNPJ:' in t)
    if not cnpj_div:
        cnpj_div = empresa.find_next('div', class_='text') if empresa else None
    cnpj = cnpj_div.get_text(strip=True).replace('CNPJ:', '').strip() if cnpj_div else ''

    # Endereço
    endereco_div = cnpj_div.find_next('div', class_='text') if cnpj_div else None
    if endereco_div:
        # Pegar o texto completo e normalizar os espaços
        endereco_raw = endereco_div.get_text()
        # Substituir quebras de linha, tabs e múltiplos espaços por um espaço único
        endereco = re.sub(r'\s+', ' ', endereco_raw).strip()
    else:
        endereco = ''

    # Itens detalhados da compra
    itens = []
    tabela = soup.find('table', id='tabResult')
    if tabela:
        for tr in tabela.find_all('tr'):
            tds = tr.find_all('td')
            if len(tds) == 2:
                # Texto do produto
                texto = tds[0].find('span', class_='txtTit')
                texto = texto.get_text(strip=True) if texto else ''
                # Código
                cod_span = tds[0].find('span', class_='RCod')
                codigo = ''
                if cod_span:
                    cod_text = cod_span.get_text()
                    match = re.search(r'Código:\s*(\d+)', cod_text)
                    if match:
                        codigo = match.group(1)
                # Quantidade
                qtd_span = tds[0].find('span', class_='Rqtd')
                quantidade = ''
                if qtd_span:
                    qtd_text = qtd_span.get_text()
                    match = re.search(r'Qtde\.:\s*(\d+[.,]?\d*)', qtd_text)
                    if match:
                        quantidade = match.group(1)
                # Unidade
                un_span = tds[0].find('span', class_='RUN')
                unidade = ''
                if un_span:
                    un_text = un_span.get_text()
                    match = re.search(r'UN:\s*(\w+)', un_text)
                    if match:
                        unidade = match.group(1)
                # Valor unitário
                vlu_span = tds[0].find('span', class_='RvlUnit')
                valor_unitario = ''
                if vlu_span:
                    vlu_text = vlu_span.get_text()
                    match = re.search(r'Vl\. Unit\.\:\s*([\d\.,]+)', vlu_text)
                    if match:
                        valor_unitario = match.group(1).replace('\xa0', '').replace(' ', '')
                # Valor total
                valor = tds[1].find('span', class_='valor')
                valor = valor.get_text(strip=True) if valor else ''
                itens.append({
                    'descricao': texto,
                    'codigo': codigo,
                    'quantidade': quantidade,
                    'unidade': unidade,
                    'valor_unitario': valor_unitario,
                    'valor_total': valor
                })

    # Data da compra
    data_compra = ''
    data_div = soup.find('span', class_='txtTopo', string=re.compile(r'\d{2}/\d{2}/\d{4}'))
    if data_div:
        match = re.search(r'(\d{2}/\d{2}/\d{4})', data_div.get_text())
        if match:
            data_compra = match.group(1)
    else:
        # Tenta encontrar a data em outros lugares
        possiveis_datas = soup.find_all(string=re.compile(r'\d{2}/\d{2}/\d{4}'))
        for d in possiveis_datas:
            match = re.search(r'(\d{2}/\d{2}/\d{4})', d)
            if match:
                data_compra = match.group(1)
                break
    # Converter data_compra para datetime.date
    data_compra_date = None
    if data_compra:
        try:
            data_compra = datetime.datetime.strptime(data_compra, "%d/%m/%Y").date()
        except ValueError:
            data_compra = None
    
    # Valor total da compra (NOVO CÓDIGO)
    total_compra = None
    
    # Método 0: Procurar pelo elemento específico com classe totalNumb txtMax
    total_element = soup.find('span', class_='totalNumb txtMax')
    if total_element:
        valor_texto = total_element.get_text(strip=True)
        # Remover R$ se existir e trocar vírgula por ponto
        valor_limpo = valor_texto.replace('R$', '').replace(' ', '').replace('.', '').replace(',', '.')
        try:
            total_compra = valor_limpo
            print(f"Total encontrado pelo elemento totalNumb: {total_compra}")
        except ValueError:
            pass
    
    # Método 1: Procurar por elementos com texto específico
    if not total_compra:
        total_spans = soup.find_all(['span', 'div', 'td'], 
                                string=re.compile(r'(valor\s+total|total\s+r\$|valor\s+a\s+pagar)', re.I))
        
        for span in total_spans:
            # Tenta extrair valor do próprio elemento
            valor_match = re.search(r'R?\$?\s*(\d+[,.]\d+)', span.get_text())
            if valor_match:
                total_compra = valor_match.group(1).replace('.', '').replace(',', '.')
                break
            
            # Se não encontrou no elemento, procura no próximo irmão ou pai
            next_el = span.find_next(['span', 'div'])
            if next_el:
                valor_match = re.search(r'R?\$?\s*(\d+[,.]\d+)', next_el.get_text())
                if valor_match:
                    total_compra = valor_match.group(1).replace('.', '').replace(',', '.')
                    break
    
    # Método 2: Última linha da tabela de itens (geralmente contém o total)
    if not total_compra and tabela:
        ultima_linha = tabela.find_all('tr')[-1]
        if ultima_linha:
            valor_match = re.search(r'R?\$?\s*(\d+[,.]\d+)', ultima_linha.get_text())
            if valor_match:
                total_compra = valor_match.group(1).replace('.', '').replace(',', '.')
    
    # Método 3: Somar os valores individuais dos itens
    if not total_compra and itens:
        # Tenta somar os valores individuais
        soma = 0
        for item in itens:
            if item['valor']:
                try:
                    valor_limpo = item['valor'].replace('R$', '').replace(' ', '').replace('.', '').replace(',', '.')
                    soma += float(valor_limpo)
                except ValueError:
                    continue
        if soma > 0:
            total_compra = str(soma)
    
    # Converter para float se encontrou um valor
    total_compra_float = None
    if total_compra:
        try:
            total_compra_float = float(total_compra)
            print(f'Total da compra: R$ {total_compra_float:.2f}')
        except ValueError:
            print(f'Total da compra (não convertido): {total_compra}')
    else:
        print('Total da compra não encontrado')

    return {
        'nome_empresa': nome_empresa,
        'cnpj': cnpj,
        'endereco': endereco,
        'data': data_compra,
        'total': total_compra_float,  # Adiciona o total ao retorno
        'itens_compra': itens
    }
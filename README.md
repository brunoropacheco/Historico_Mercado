# Historico_Mercado

Este projeto automatiza o processo de extração e análise de dados de notas fiscais para montar histórico de preços de produtos de supermercado.

## Visão Geral

O sistema é composto por dois principais módulos:
- **Batch Diário:** Responsável por monitorar uma pasta no Google Drive, detectar novas imagens de notas fiscais, processar as imagens, extrair chave do QR code do cupom, consultar SEFAZ e atualizar o banco de dados.
- **Web App:** Permite ao usuário consultar o histórico de preços de produtos a partir dos dados extraídos.

## Status do Projeto (Versão 0.1.0 - Em Desenvolvimento)

Atualmente, o projeto encontra-se em fase de desenvolvimento com as seguintes funcionalidades implementadas:

*   **Monitoramento de Pasta no Google Drive:** O script `scripts/process_daily.py` monitora pastas especificadas no Google Drive em busca de novas imagens.
*   **Download e Processamento de Imagens:** Novas imagens são baixadas, processadas e depois excluídas do servidor local.
*   **Extração de Chave de Acesso via QR Code:** O sistema identifica e extrai a chave de acesso NFC-e a partir do QR code presente nas imagens.
*   **Consulta Automatizada à SEFAZ:** Utilizando a chave obtida, o sistema consulta o portal da Secretaria da Fazenda para extrair dados do cupom fiscal.
*   **Persistência de Dados:** Os dados extraídos são salvos em um banco de dados SQLite para consultas posteriores.
*   **Interface Web Básica:** Uma interface web implementada com Flask permite a consulta de produtos e visualização de compras.

**Funcionalidades Ainda Pendentes:**

*   Implantação em ambiente produtivo fora do github codespaces

## Casos de Uso

- **UC01:** Adicionar nova imagem na pasta (Implementado)
- **UC02:** Monitorar diariamente a pasta (Implementado)
- **UC03:** Processar novas imagens detectadas (Implementado)
- **UC04:** Atualizar banco de dados com dados das imagens (Implementado)
- **UC05:** Consultar histórico de preços (Implementado)
- **UC06:** Visualizar detalhes de uma compra específica (Implementado)

## Fluxo de Processamento

O sistema funciona com o seguinte fluxo:

1. Busca imagens na pasta do Google Drive definida pela variável de ambiente `GOOGLE_DRIVE_FOLDER_NOVASNOTAS_ID`
2. Processa cada imagem:
   - Executa melhorias na imagem
   - Extrai a chave do QR code
   - Consulta os dados da nota fiscal via SEFAZ
   - Salva os dados no banco SQLite
3. Move a imagem processada para a pasta `GOOGLE_DRIVE_FOLDER_NOTASTRATADAS_ID` 
4. Exclui a imagem temporária do servidor local
5. Obtem os dados do cupom via site da SEFAZ
6. Salva os dados no bnnco de dados
7. Cliente acessa via interface web para buscar por termo

### Tolerância a Falhas

O sistema foi implementado para lidar com erros sem interromper o processamento:
- Se não conseguir ler o QR code de uma imagem, passa para a próxima
- Qualquer erro durante o processamento é registrado no log e o sistema continua
- As imagens com erro também são movidas para a pasta de tratados

## Boas Práticas para Captura de Imagens

Para melhor eficiência do sistema:

- Tire foto apenas do QR code da nota fiscal
- Certifique-se de que o QR code esteja bem visível e não deformado
- Evite reflexos, sombras ou obstruções no QR code
- Mantenha a câmera estável ao fotografar

## Tecnologias Utilizadas

- **Python** (OpenCV, pyzbar, Flask)
- **SQLite** (banco de dados local)
- **Google Drive API** (monitoramento de imagens)
- **HTML/CSS** (interface web)
- **PlantUML** (documentação dos fluxos)
- **Flask** (servidor WEB)

## Diagramas

Os diagramas de casos de uso e fluxograma do sistema estão disponíveis na pasta `docs/`:
- `docs/casos_de_uso.plantuml`
- `docs/fluxograma.plantuml`
- `docs/diagrama_mvc.plantuml` (Representa a arquitetura do Web App)

## Como Contribuir

1.  Faça um fork do repositório.
2.  Crie uma branch para sua feature ou correção.
3.  Envie um pull request.

## Configuração do Ambiente

### Dependências do Sistema (Linux)

Antes de instalar as dependências Python, instale as bibliotecas do sistema necessárias:

```sh
sudo apt-get update
sudo apt-get install libgl1 libzbar0
```

Essas bibliotecas são necessárias para o funcionamento do OpenCV (`cv2`) e do `pyzbar`.

### Inicialização do Banco de Dados

Antes de executar o sistema pela primeira vez, crie o banco de dados SQLite:

```sh
python scripts/init_db.py
```

### Configuração do Google Drive API

Para utilizar a funcionalidade de monitoramento de notas fiscais no Google Drive:

1.  **Criar projeto no Google Cloud Platform**
    1.  Acesse o [Console do Google Cloud](https://console.cloud.google.com/)
    2.  Crie um novo projeto ou selecione um existente
    3.  Anote o ID do projeto para uso posterior

2.  **Ativar a API do Google Drive**
    1.  No menu lateral, vá para "APIs e Serviços" > "Biblioteca"
    2.  Pesquise por "Google Drive API"
    3.  Clique no resultado e selecione "Ativar"

3.  **Criar uma conta de serviço**
    1.  No menu lateral, vá para "APIs e Serviços" > "Credenciais"
    2.  Clique em "Criar credenciais" > "Conta de serviço"
    3.  Preencha o nome, ID e descrição da conta de serviço
    4.  Conceda o papel/role "Editor do Drive" (Drive File Editor) - necessário para mover arquivos
    5.  Conclua a criação da conta de serviço
    6.  Anote o email da conta de serviço (formato: `nome-servico@projeto-id.iam.gserviceaccount.com`)

4.  **Gerar chave JSON para a conta de serviço**
    1.  Na lista de contas de serviço, clique na conta recém-criada
    2.  Vá para a aba "Chaves"
    3.  Clique em "Adicionar chave" > "Criar nova chave"
    4.  Selecione o formato JSON e clique em "Criar"
    5.  O arquivo de credenciais será baixado automaticamente para seu computador
    6.  **IMPORTANTE**: Mantenha este arquivo seguro e nunca o adicione ao controle de versão

5.  **Compartilhar pastas do Google Drive com a conta de serviço**
    1.  Acesse seu [Google Drive](https://drive.google.com/)
    2.  Crie duas pastas: uma para novas notas e outra para notas tratadas
    3.  Compartilhe ambas as pastas com o email da conta de serviço com permissão "Editor"
    4.  Obtenha os IDs das pastas a partir das URLs

6.  **Configurar variáveis de ambiente**
    Configure as seguintes variáveis:

    **Linux/macOS:**
    ```bash
    export GOOGLE_DRIVE_CREDENTIALS='{"type":"service_account","project_id":"seu-projeto",...}'
    export GOOGLE_DRIVE_FOLDER_NOVASNOTAS_ID='id-da-pasta-de-novas-notas'
    export GOOGLE_DRIVE_FOLDER_NOTASTRATADAS_ID='id-da-pasta-de-notas-tratadas'
    ```

    **Windows:**
    ```cmd
    set GOOGLE_DRIVE_CREDENTIALS={"type":"service_account","project_id":"seu-projeto",...}
    set GOOGLE_DRIVE_FOLDER_NOVASNOTAS_ID=id-da-pasta-de-novas-notas
    set GOOGLE_DRIVE_FOLDER_NOTASTRATADAS_ID=id-da-pasta-de-notas-tratadas
    ```

    Para desenvolvimento, crie um arquivo `.env` na raiz do projeto com estas variáveis.

## Interface Gráfica Web

Uma interface web foi implementada para facilitar a consulta aos dados das notas fiscais:

* **Página inicial com busca**: Interface para pesquisar produtos pelo nome/descrição
* **Listagem de resultados**: Exibição dos produtos encontrados com detalhes como preço e estabelecimento
* **Visualização de compra**: Página detalhada de uma compra específica com todos os itens

### Estrutura de Arquivos

```
src/
├── views/
│   ├── templates/           # Arquivos HTML
│   │   ├── base.html        # Template base com estrutura comum
│   │   ├── index.html       # Página inicial com busca
│   │   ├── resultados.html  # Listagem de resultados da busca
│   │   └── detalhes_compra.html  # Visualização detalhada de uma compra
│   └── static/              # Arquivos estáticos
│       └── css/
│           └── style.css    # Estilos da aplicação
app.py                      # Aplicação Flask com rotas definidas
```

### Execução da Aplicação Web

Para executar a aplicação web localmente:

```sh
python app.py
```

A aplicação estará disponível em http://localhost:5000

## Próximos Passos

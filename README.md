# Historico_Mercado

Este projeto automatiza o processo de extração e análise de dados de notas fiscais para montar histórico de preços de produtos de supermercado.

## Visão Geral

O sistema é composto por dois principais módulos:
- **Batch Diário:** Responsável por monitorar uma pasta no Google Drive, detectar novas imagens de notas fiscais, processar as imagens com OCR, extrair os dados relevantes e atualizar o banco de dados.
- **Web App:** Permite ao usuário consultar o histórico de preços de produtos a partir dos dados extraídos.

## Status do Projeto (Versão 0.1.0 - Em Desenvolvimento)

Atualmente, o projeto encontra-se em fase inicial de desenvolvimento. As seguintes funcionalidades foram implementadas:

*   **Monitoramento de Pasta no Google Drive:** O script `scripts/process_daily.py` consegue monitorar uma pasta especificada no Google Drive em busca de novas imagens.
*   **Download de Imagens:** Novas imagens detectadas são baixadas para a pasta local `data/images`.
*   **Extração de Chave de Acesso via QR Code:** O sistema identifica e extrai a chave de acesso NFC-e a partir do QR code presente nas imagens de notas fiscais.
*   **Consulta Automatizada à SEFAZ:** Utilizando a chave obtida, o sistema consulta o portal da Secretaria da Fazenda para extrair dados detalhados do cupom fiscal.
*   **Persistência de Dados:** Os dados extraídos das notas fiscais (estabelecimento, valor total, itens) são salvos em um banco de dados SQLite local para consultas posteriores.
*   **Exibição de Dados Extraídos:** Os dados estruturados da nota fiscal e informações básicas da imagem são exibidos no console.

**Funcionalidades Ainda Não Implementadas / Em Desenvolvimento:**

*   Refinamento do parser para extração de dados mais complexos (descrições padronizadas, categorização de produtos).
*   Otimização do acesso à SEFAZ para lidar com restrições de acesso.
*   Desenvolvimento do Web App para consulta dos dados.
*   Automação completa do processo batch (agendamento, tratamento de erros robusto).

O objetivo é evoluir para um sistema completamente automatizado e com uma interface web funcional.

## Casos de Uso (Planejados)

- **UC01:** Adicionar nova imagem na pasta (Administrador)
- **UC02:** Monitorar diariamente a pasta (Script de Monitoramento)
- **UC03:** Processar novas imagens detectadas (Script de Monitoramento)
- **UC04:** Atualizar banco de dados com dados das imagens (Script de Monitoramento)
- **UC05:** Consultar histórico de preços (Administrador)

## Fluxo Batch Diário (Implementação Parcial)

1.  Detectar novas imagens no Google Drive (Implementado).
2.  Se existirem novas imagens:
    *   Baixar a imagem (Implementado).
    *   Extrair chave de acesso via QR code (Implementado).
    *   Consultar site da SEFAZ usando a chave extraída (Implementado).
    *   Fazer parse dos dados retornados (Implementado parcialmente).
    *   Salvar dados estruturados no banco SQLite (Implementado parcialmente).
3.  Se não existirem novas imagens:
    *   Aguardar próximo ciclo e voltar a detectar novas imagens (Lógica básica implementada).

## Fluxo Web App (Não Implementado)

1.  Usuário acessa o site.
2.  Insere termo de pesquisa.
3.  Consulta o banco de dados.
4.  Exibe o histórico de preços.

## Diagramas

Os diagramas de casos de uso e fluxograma do sistema estão disponíveis na pasta `docs/`:
- `docs/casos_de_uso.plantuml`
- `docs/fluxograma.plantuml`
- `docs/diagrama_mvc.plantuml` (Representa a arquitetura planejada para o Web App)

Para visualizar os diagramas, utilize a extensão PlantUML no VS Code ou gere as imagens via terminal:

```sh
sudo apt-get install plantuml graphviz
plantuml docs/casos_de_uso.plantuml
plantuml docs/fluxograma.plantuml
plantuml docs/diagrama_mvc.plantuml
```

## Tecnologias Utilizadas (e Planejadas)

- **Python** (pytesseract para OCR, Flask/Django para Web App - planejado)
- **SQLite** (banco de dados local para armazenamento e testes)
- **PlantUML** (documentação dos fluxos)
- **Google Drive API** (monitoramento de imagens)
- **Tesseract OCR** (motor de reconhecimento óptico de caracteres)
- **Banco de Dados** (SQLite, PostgreSQL, ou outro - a definir)
- **Regex/BeautifulSoup** (parser de HTML para extração de dados)
- *Flask/Django* (Web App - planejado)

## Como Contribuir

1.  Faça um fork do repositório.
2.  Crie uma branch para sua feature ou correção.
3.  Envie um pull request.

## Configuração do Ambiente

### Configuração do Google Drive API

Para utilizar a funcionalidade de monitoramento de notas fiscais no Google Drive, é necessário configurar o acesso à API do Google. Siga os passos abaixo:

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
    4.  Conceda o papel/role "Leitor do Drive" (Drive File Reader)
    5.  Conclua a criação da conta de serviço
    6.  Anote o email da conta de serviço (formato: `nome-servico@projeto-id.iam.gserviceaccount.com`)

4.  **Gerar chave JSON para a conta de serviço**
    1.  Na lista de contas de serviço, clique na conta recém-criada
    2.  Vá para a aba "Chaves"
    3.  Clique em "Adicionar chave" > "Criar nova chave"
    4.  Selecione o formato JSON e clique em "Criar"
    5.  O arquivo de credenciais será baixado automaticamente para seu computador
    6.  **IMPORTANTE**: Mantenha este arquivo seguro e nunca o adicione ao controle de versão

5.  **Compartilhar pasta do Google Drive com a conta de serviço**
    1.  Acesse seu [Google Drive](https://drive.google.com/)
    2.  Crie uma pasta para armazenar as imagens das notas fiscais
    3.  Clique com o botão direito na pasta > "Compartilhar"
    4.  No campo de email, insira o email da conta de serviço
    5.  Defina a permissão como "Leitor"
    6.  Desmarque a opção de notificação e clique em "Compartilhar"
    7.  Obtenha o ID da pasta da URL (formato: `https://drive.google.com/drive/folders/SEU_FOLDER_ID_AQUI`)

6.  **Configurar variáveis de ambiente para o Google Drive**
    Para proteger suas credenciais, use variáveis de ambiente em vez de incluir diretamente no código:

    1.  Converta o conteúdo do arquivo JSON das credenciais para uma string única (removendo quebras de linha).
    2.  Configure as seguintes variáveis de ambiente:

    **Linux/macOS:**
    ```bash
    export GOOGLE_DRIVE_CREDENTIALS='{"type":"service_account","project_id":"seu-projeto",...}'
    export GOOGLE_DRIVE_FOLDER_ID='seu-folder-id'
    ```

    **Windows:**
    ```cmd
    set GOOGLE_DRIVE_CREDENTIALS={"type":"service_account","project_id":"seu-projeto",...}
    set GOOGLE_DRIVE_FOLDER_ID=seu-folder-id
    ```

    Para desenvolvimento, crie um arquivo `.env` na raiz do projeto com estas variáveis (não esqueça de adicionar `.env` ao `.gitignore`).

### Configuração do Tesseract OCR

Para a extração de texto de imagens (OCR), este projeto utiliza a biblioteca `pytesseract`, que é uma interface para o motor Tesseract OCR. É necessário instalar o Tesseract OCR no seu sistema operacional, bem como os pacotes de idioma desejados.

1.  **Instalar a biblioteca Python `pytesseract`**:
    ```bash
    pip install pytesseract
    ```

2.  **Instalar o motor Tesseract OCR**:
    *   **Linux (Debian/Ubuntu):**
        ```bash
        sudo apt-get update
        sudo apt-get install tesseract-ocr
        ```
    *   **Linux (Fedora):**
        ```bash
        sudo dnf install tesseract
        ```
    *   **macOS (usando Homebrew):**
        ```bash
        brew install tesseract
        ```
    *   **Windows:**
        Baixe o instalador na [página de downloads do Tesseract no GitHub](https://github.com/UB-Mannheim/tesseract/wiki). Durante a instalação, adicione o Tesseract ao PATH do sistema e selecione os pacotes de idioma.

3.  **Instalar Pacotes de Idioma para Tesseract (Exemplo: Português)**:
    O projeto está configurado para usar o idioma português (`por`).
    *   **Linux (Debian/Ubuntu):**
        ```bash
        sudo apt-get install tesseract-ocr-por
        ```
    *   **Outros Sistemas:** Consulte a documentação do Tesseract ou as opções do instalador para adicionar pacotes de idioma. O arquivo de dados para português é geralmente `por.traineddata`.

4.  **Verificação**:
    Após a instalação, abra um terminal e digite `tesseract --version`. Se o comando for reconhecido, o Tesseract está instalado e no PATH do sistema.

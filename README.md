# Historico_Mercado

Este projeto automatiza o processo de extração e análise de dados de notas fiscais para montar histórico de preços de produtos de supermercado.

## Visão Geral

O sistema é composto por dois principais módulos:
- **Batch Diário:** Responsável por monitorar uma pasta no Google Drive, detectar novas imagens de notas fiscais, processar as imagens com OCR, extrair os dados relevantes e atualizar o banco de dados.
- **Web App:** Permite ao usuário consultar o histórico de preços de produtos a partir dos dados extraídos.

## Casos de Uso

- **UC01:** Adicionar nova imagem na pasta (Administrador)
- **UC02:** Monitorar diariamente a pasta (Script de Monitoramento)
- **UC03:** Processar novas imagens detectadas (Script de Monitoramento)
- **UC04:** Atualizar banco de dados com dados das imagens (Script de Monitoramento)
- **UC05:** Consultar histórico de preços (Administrador)

## Fluxo Batch Diário

1. Detectar novas imagens no Google Drive.
2. Se existirem novas imagens:
    - Executar OCR via pytesseract.
    - Realizar parser de texto (regex/heurísticas).
    - Atualizar banco de dados.
3. Se não existirem novas imagens:
    - Aguardar próximo ciclo e voltar a detectar novas imagens.

## Fluxo Web App

1. Usuário acessa o site.
2. Insere termo de pesquisa.
3. Consulta o banco de dados.
4. Exibe o histórico de preços.

## Diagramas

Os diagramas de casos de uso e fluxograma do sistema estão disponíveis na pasta `docs/`:
- `docs/casos_de_uso.plantuml`
- `docs/fluxograma.plantuml`

Para visualizar os diagramas, utilize a extensão PlantUML no VS Code ou gere as imagens via terminal:

```sh
sudo apt-get install plantuml graphviz
plantuml docs/casos_de_uso.plantuml
plantuml docs/fluxograma.plantuml
```

## Tecnologias Utilizadas

- **Python** (pytesseract para OCR)
- **PlantUML** (documentação dos fluxos)
- **Google Drive API** (monitoramento de imagens)
- **Banco de Dados** (armazenamento do histórico de preços)
- **Regex/Heurísticas** (parser de texto)

## Como Contribuir

1. Faça um fork do repositório.
2. Crie uma branch para sua feature ou correção.
3. Envie um pull request.

---

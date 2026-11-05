# JP Slides Didáticos

Skill para criar ou revisar apresentações educativas a partir de resumos próprios de obras, com fontes rastreáveis, notas de estudo e identidade visual JP Wealth.

**Versão do pacote:** 1.5.1.

## O que a skill faz

- Organiza o conteúdo em uma sequência de explicações, exemplos, relações e limites.
- Adapta a apresentação ao objetivo, ao público e ao tempo disponível.
- Separa o apoio visual da apresentação oral do aprofundamento nas notas.
- Orienta a pesquisa e a atribuição de fontes, explicitando divergências e lacunas.
- Planeja imagens e diagramas que ajudem a explicar os conceitos.
- Prevê revisão acadêmica e didática por auditores distintos do autor.
- Inclui um verificador estrutural de arquivos PPTX.

O padrão visual usa preto e branco e uma logo pequena JP Wealth em todos os slides. As metas de uso de imagens são editoriais e podem ser ajustadas ao tema com justificativa.

## Como usar

Disponibilize o pacote em um ambiente compatível com skills e execução local. A definição principal está em [SKILL.md](skills/jp-slides-didaticos/SKILL.md); os manifestos do plugin estão na raiz e em `.codex-plugin/`.

Para uso como skill avulsa, utilize a pasta completa `skills/jp-slides-didaticos/`, preservando `references/`, `assets/`, `agents/` e `scripts/`. O procedimento de instalação depende do aplicativo usado.

Invoque a skill explicitamente e forneça seu resumo:

> Use $jp-slides-didaticos para transformar meu resumo em slides educativos com notas de estudo e identidade JP Wealth.

Inclua, quando disponíveis:

- Obra, autor, edição e localizadores das passagens utilizadas.
- Resumo ou material de origem.
- Público, objetivo e duração da apresentação.
- Formatos desejados e restrições relevantes.

Exemplo de pedido:

> Use $jp-slides-didaticos para criar uma apresentação de 20 minutos a partir do resumo abaixo. O público inclui iniciantes e pessoas familiarizadas com o tema. Quero PPTX editável com notas e PDF dos slides. Obra e edição: […]. Resumo: […].

A skill também pode revisar uma apresentação ou desenvolver apenas um roteiro, conforme o pedido.

## Fluxo de trabalho

1. Delimitar o escopo e verificar as ferramentas disponíveis.
2. Mapear conceitos, pré-requisitos, fontes e afirmações que precisam de pesquisa.
3. Construir a progressão didática, o roteiro e as notas.
4. Planejar e produzir os visuais explicativos.
5. Verificar a estrutura, renderizar, inspecionar os slides e reabrir os arquivos.
6. Submeter a mesma versão às auditorias acadêmica e didática independentes.
7. Corrigir os achados materiais e entregar os arquivos com o relato das verificações e pendências.

## Entregas

Na produção completa, conforme as capacidades verificadas do ambiente:

- PPTX editável com notas.
- PDF dos slides.
- Material de estudo com notas relacionadas aos slides.
- Relato de fontes, revisões, validações e pendências.

## Estrutura do repositório

```text
.
├── README.md
├── plugin.json
├── .codex-plugin/
│   └── plugin.json
├── assets/
│   └── icon.svg
└── skills/
    └── jp-slides-didaticos/
        ├── SKILL.md
        ├── agents/
        │   └── openai.yaml
        ├── assets/
        │   ├── icon.svg
        │   └── jp-wealth-logo.png
        ├── references/
        └── scripts/
            └── verify_deck.py
```

As referências detalham fontes, pesquisa científica, progressão didática, direção de arte, identidade visual, rubricas e auditoria do resultado.

## Requisitos e validação

O pacote requer execução local e não instala um runtime. A geração, a renderização e a reabertura de PPTX e PDF dependem das ferramentas disponíveis no ambiente. Pesquisa e produção de imagens também dependem dos recursos acessíveis.

O verificador `verify_deck.py` usa Python 3 e apenas a biblioteca padrão. Para consultar seus argumentos, execute a partir da raiz do repositório:

```bash
python3 skills/jp-slides-didaticos/scripts/verify_deck.py --help
```

O script realiza controles estruturais de OOXML. Ele não substitui a inspeção visual, a revisão das fontes, a avaliação da qualidade das notas ou a análise pedagógica. Os hashes vinculam as verificações aos bytes dos arquivos; o recibo não é uma assinatura digital.

A execução da skill não garante aprendizagem ou adequação ao público. Essas conclusões exigem avaliação com aprendizes. Quando faltarem ferramentas, acesso às fontes ou auditores independentes, as limitações devem ser registradas na entrega.

## Autoria

João Paulo Vinagre Alves Cirqueira — JP Wealth.

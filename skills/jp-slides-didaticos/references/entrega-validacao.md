# Entrega e validação

## Prepare uma entrega verificável

Confirme as capacidades do host antes de prometer formatos. Use as ferramentas disponíveis de apresentações, documentos e PDF para gerar, renderizar e reabrir os arquivos. Antes de uma produção completa, confirme uma rota disponível para leitura da entrada, geração, renderização e reabertura dos formatos pedidos. Em ambiente ainda não exercitado, faça uma pequena exportação/reabertura com texto, nota, logo e imagem descrita antes de gerar o lote. Reutilize uma prova recente válida para o mesmo ambiente; não repita esse preparo por slide. O pacote não inclui um editor, renderizador ou servidor próprio. A opção `requires_local_executor` declara a dependência; não instala runtime ou ferramentas e não comprova disponibilidade em outro host.

Para uso oral e estudo, produza, quando suportado:

- PPTX editável com notas correspondentes aos slides.
- PDF dos slides.
- Material de estudo que mostre as notas junto aos slides ou as relacione por número/título inequívoco.
- Registro compacto de fontes, divergências e verificação.

Guarde entradas preservadas e resultados no espaço da tarefa, fora da pasta do plugin. Reutilize a organização existente; `work/` para intermediários e `outputs/` para entregas é uma opção simples.

## Execute o controle estrutural

O script usa Python 3 e inspeciona o PPTX; rode-o a partir do diretório do skill ou ajuste os caminhos:

```sh
python3 scripts/verify_deck.py DECK.pptx --logo assets/jp-wealth-logo.png --receipt RECEIPT.json
python3 scripts/verify_deck.py --check-receipt RECEIPT.json
```

Quando o número esperado de slides tiver sido definido, acrescente `--expect-slides N` ao primeiro comando. O recibo v2 exige `p:cNvPr/@descr` não vazio em cada objeto explícito de imagem, inclusive a marca. Nome ou título do objeto, descrição apenas nas notas e campo informado à API de autoria não bastam: confira o PPTX exportado. Use descrição pertinente ao conteúdo, sem inventar metadados ou inserir preenchimento para passar. A presença é automatizada; utilidade e ordem de leitura continuam na revisão. Recibos v1 devem ser regenerados, pois não contêm esse controle.

Use caminhos dos arquivos efetivos, colocando entre aspas os que contiverem espaços. Examine o resultado e as falhas registradas; a existência de um recibo, sozinha, não representa aprovação. O modo de conferência do recibo ajuda a conferir a versão a que os controles se referem. Qualquer alteração nos arquivos examinados exige nova verificação pertinente.

Esse controle é estrutural e limitado às verificações que o script relata. Ele não renderiza slides, interpreta evidência acadêmica nem mede aprendizagem. Presença técnica de uma imagem também não garante que esteja visível, legível e bem posicionada. Uma saída favorável não substitui a inspeção abaixo.

## Examine a versão entregue

Renderize e inspecione **todos** os slides, em tamanho suficiente para conferir conteúdo, cortes, sobreposição, substituição de fontes e marca. Reabra o arquivo final em ferramenta compatível e confirme slides, notas, editabilidade e recursos de acesso que forem pertinentes. Confira que o PDF e o material de estudo correspondem à mesma versão. Após correções, reveja os controles afetados. Se a exportação perder um atributo, corrija-o no candidato com ferramenta compatível ou edição delimitada do pacote, preservando conteúdo/mídia; reabra e valide novamente. Não altere silenciosamente o original nem declare acessibilidade completa sem teste no destino.

Na revisão de conteúdo, confira números, unidades, períodos, fontes, citações, nomes de capítulos e a distinção entre evidência e interpretação. Relações qualitativas devem ser reconhecíveis sem precisão numérica inventada. Se houver acesso parcial à obra, limite o alcance da validação. Confira também chamadas científicas legíveis nos slides e referências completas vinculadas nas notas/estudo, com DOI ou endereço estável, resultado e localizador consultados; examine correspondências e limites das comparações conforme [pesquisa crítica](pesquisa-cientifica.md). O verificador estrutural não executa essa avaliação.

## Passe pelas revisões de conteúdo e arte

Depois do controle estrutural, renderização e reabertura já executados, congele os arquivos e execute a [auditoria acadêmica e didática](auditoria-resultado.md) com a [rubrica de conteúdo e arte](qa-rubrica.md), registrando evidências por núcleo e slide. Não repita os mesmos controles como uma terceira revisão. Congele os arquivos examinados, resolva achados materiais e confira a versão corrigida pelos auditores pertinentes. Registre os pareceres acadêmico e didático, suficiência, arte e estrutura separadamente; limitações de acesso ou independência ficam explícitas. Cada achado visual deve trazer arquivo/identidade, tela, elemento, região e evidência observada. Uma ausência percebida requer reexame da região legível antes de exigir mudança. Estrutura e recortes auxiliam o confronto, sem substituir a visibilidade renderizada. A presença de notas ou imagens detectadas no arquivo não comprova explicação suficiente. Sem arte prevista produzida, registre pendência; não aprove visualmente o deck provisório.

## Relate o estado com precisão

Informe o que existe e o que foi efetivamente examinado: criação do arquivo, verificação estrutural, inspeção visual, reabertura, revisão de conteúdo e avaliação com participantes são estados distintos. Apresente os dois pareceres e os achados corrigidos ou pendentes, com o efeito deles na entrega. Sem os controles aplicáveis concluídos, não declare o resultado academicamente aprovado, claro para o público ou de alta qualidade final. Mantenha o processo técnico fora do conteúdo educativo, salvo quando o próprio tema o exigir.

A aprovação do artefato não demonstra aprendizagem. Quando houver teste humano, registre perfis, modo oral ou estudo autônomo, conhecimentos prévios, tempo e rubrica. Avalie compreensão, retenção posterior e aplicação a caso novo; satisfação pode ser registrada separadamente. Sem participantes, declare avaliação pedagógica humana pendente. Uma amostra pequena não sustenta superioridade universal, certificação ou promessa de economia.

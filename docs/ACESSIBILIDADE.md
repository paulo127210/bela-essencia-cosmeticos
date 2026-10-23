# Documentação de acessibilidade

Este documento descreve como a loja Bela Essência atende pessoas cegas, com baixa visão e com daltonismo, e quais critérios da WCAG 2.2 são cumpridos.

## Normas seguidas

- WCAG 2.2, nível AA, buscando o nível AAA em contraste de texto.
- eMAG 3.1, Modelo de Acessibilidade em Governo Eletrônico.
- Lei 13.146/2015, Lei Brasileira de Inclusão.
- Lei 13.709/2018, LGPD, nos formulários.

## Estrutura da página

Todas as páginas têm a mesma ordem, para que a pessoa aprenda o caminho uma vez só:

1. Barra superior com os atalhos visíveis e os botões rápidos de acessibilidade.
2. Painel de recursos de acessibilidade, fechado por padrão.
3. Cabeçalho com a marca, a busca e o carrinho.
4. Menu principal.
5. Trilha de navegação ("Você está aqui"), nas páginas internas.
6. Conteúdo principal (`main`), sempre com um único `h1`.
7. Rodapé.

Regiões usadas: `header`, `nav` (atalhos, menu principal, trilha e links do rodapé, cada uma com nome próprio), `main`, `aside` (resumo do pedido) e `footer`. Os títulos seguem a ordem h1, h2 e h3 sem pular níveis.

O título da aba (`title`) muda em cada página e também quando a pessoa filtra o catálogo ou abre um produto.

## Atalhos de teclado

| Atalho | Destino |
| --- | --- |
| Alt + 1 | Conteúdo principal |
| Alt + 2 | Menu principal |
| Alt + 3 | Campo de busca |
| Alt + 4 | Rodapé |
| Esc | Fecha o painel de recursos e devolve o foco ao botão que o abriu |

Os atalhos são tratados por JavaScript usando o código físico da tecla, então funcionam em qualquer layout de teclado. Os mesmos destinos estão nos links visíveis do topo da página.

## Barra de acessibilidade

| Recurso | Como funciona |
| --- | --- |
| Tamanho da letra | Cinco níveis: 100%, 125%, 150%, 175% e 200%. Todo o layout usa `rem`, então nada se sobrepõe. |
| Alto contraste | Fundo preto, texto branco, links e botões amarelos, foco ciano. Imagens ficam em tons de cinza. |
| Modo escuro | Paleta escura com contraste AA ou superior. |
| Cores para daltonismo | Troca a paleta para combinações seguras: azul e laranja para protanopia e deuteranopia, vinho e verde-azulado para tritanopia. Existe versão clara e escura. |
| Espaçamento ampliado | Altura de linha 2, espaço entre letras 0,12 em e entre palavras 0,16 em, conforme o critério 1.4.12. |
| Fonte facilitada | Troca para a fonte Lexend, de leitura mais fácil para pessoas com dislexia. |
| Ouvir a página | Usa a Web Speech API em português do Brasil. Lê o texto selecionado ou o conteúdo principal, com pausar, continuar, parar e quatro velocidades. |
| Ler ao passar o mouse | Desligado por padrão. Quando ligado, lê em voz alta o item sob o mouse (após 0,35 segundo parado) e o item que recebe o foco pelo Tab. Diz o tipo do elemento ("Link", "Botão", "Título", "Imagem", "Campo") e marca o item lido com contorno tracejado. Indicado para baixa visão. |
| Restaurar | Volta tudo ao padrão. |

As escolhas ficam no `localStorage` do navegador, com tratamento de erro para navegação privada. O arquivo `js/preferencias.js` aplica as escolhas antes de a página aparecer, sem piscar. Se a pessoa nunca escolheu um tema, o site segue o sistema: `prefers-contrast: more` ativa o alto contraste e `prefers-color-scheme: dark` ativa o modo escuro. O modo de cores forçadas do Windows também é respeitado.

## Por que a leitura ao passar o mouse fica desligada

Pessoas cegas não usam o mouse. Elas navegam pelo teclado ou pelo toque com um leitor de tela (NVDA, JAWS, VoiceOver, TalkBack), que já fala todo o conteúdo do site. Se a leitura ao passar o mouse ficasse sempre ligada, a voz do site e a voz do leitor de tela falariam ao mesmo tempo. Por isso ela é uma opção, com botão no topo de todas as páginas, voltada para quem tem baixa visão e usa o mouse.

## Leitores de tela

- Avisos dinâmicos usam duas regiões: `role="status"` (educada) para confirmações, como produto adicionado, e `role="alert"` (urgente) para falhas, como CEP não encontrado.
- Os botões de adicionar ao carrinho repetem o nome do produto em texto oculto: "Adicionar ao carrinho: Batom Cremoso Rosé". Assim, a lista de botões do leitor de tela não fica com dezesseis botões iguais.
- Preços com desconto são lidos como "Preço anterior: R$ 49,90. Preço atual: R$ 39,90".
- Botões de mais e menos têm nomes completos, como "Aumentar quantidade de Sérum Vitamina C 10%".
- Botões de alternância usam `aria-pressed`. O botão do painel usa `aria-expanded` e `aria-controls`.
- O item atual do menu e da trilha usa `aria-current="page"`.
- Ícones decorativos têm `aria-hidden="true"` e `focusable="false"`.

## Imagens

Cada produto tem uma foto real e um texto alternativo que descreve o que a foto mostra, como "Frasco âmbar de sérum com conta-gotas preto, sobre fundo laranja". Se a foto não carregar, o site troca sozinho pela ilustração local do produto, mantendo o mesmo texto alternativo. No carrinho, a miniatura tem `alt=""`, porque o nome do produto já está ao lado. A ilustração da página inicial é decorativa.

Além do texto alternativo, cada produto tem o campo "Como reconhecer a embalagem pelo toque", que é o diferencial da loja para quem não enxerga.

## Cores e texto

- Texto principal #2B1626 sobre #FFF7FA, contraste de 16:1.
- Botão principal: branco sobre #6B1F57, contraste de 10,7:1.
- Nenhuma informação depende só de cor. Erros têm símbolo de alerta e texto, o item atual do menu tem um marcador e o selo de Braille tem borda mais grossa e negrito.
- Letra base de 18 pixels, com a fonte Atkinson Hyperlegible, criada pelo Braille Institute para pessoas com baixa visão.
- Alvos de toque de no mínimo 44 por 44 pixels.
- Foco sempre visível, com anel de 4 pixels e contorno externo, que aparece em qualquer fundo.
- Animações respeitam `prefers-reduced-motion`. Não há nada piscando nem som ou vídeo automático.

## Formulários

- Todo campo tem `label` visível ligado ao campo. Nenhuma instrução fica só no `placeholder`.
- Instruções e exemplos ficam antes do campo e são ligados por `aria-describedby`.
- Campos obrigatórios têm asterisco visual e `aria-required="true"`, e a regra é explicada no topo do formulário.
- Os campos usam `autocomplete` correto (nome, e-mail, telefone, CEP, endereço), o que atende ao critério 1.3.5.
- Ao enviar com problemas, aparece um resumo com a quantidade de erros e um link para cada campo. O foco vai para esse resumo. Cada campo com erro recebe `aria-invalid="true"` e a mensagem é ligada a ele.
- A formatação de CEP e telefone só acontece quando a pessoa sai do campo, para não atrapalhar quem digita com leitor de tela.
- Não há CAPTCHA.
- Ao concluir, o foco vai para o título da confirmação.

## Checklist WCAG 2.2 nível AA

| Critério | Situação | Onde |
| --- | --- | --- |
| 1.1.1 Conteúdo não textual | Atende | Texto alternativo em todas as imagens informativas |
| 1.3.1 Informações e relações | Atende | HTML semântico, `fieldset`, `legend`, tabelas com `th` e `caption` |
| 1.3.2 Sequência com significado | Atende | Ordem do código igual à ordem visual |
| 1.3.3 Características sensoriais | Atende | Instruções não dependem de forma ou posição |
| 1.3.4 Orientação | Atende | Funciona na vertical e na horizontal |
| 1.3.5 Identificar o propósito da entrada | Atende | Atributos `autocomplete` |
| 1.4.1 Uso de cor | Atende | Texto e símbolos junto com a cor |
| 1.4.3 Contraste mínimo | Atende | Verificado pelo axe em sete combinações de tema |
| 1.4.4 Redimensionar texto | Atende | Até 200% pela barra e pelo zoom do navegador |
| 1.4.5 Imagens de texto | Atende | Não há texto dentro de imagens |
| 1.4.10 Refluxo | Atende | Sem rolagem horizontal a 320 pixels |
| 1.4.11 Contraste não textual | Atende | Bordas de campos e botões com 3:1 ou mais |
| 1.4.12 Espaçamento de texto | Atende | Opção de espaçamento ampliado sem perda de conteúdo |
| 1.4.13 Conteúdo em foco ou passar o mouse | Atende | Não há conteúdo que aparece ao passar o mouse |
| 2.1.1 Teclado | Atende | Tudo funciona pelo teclado |
| 2.1.2 Sem bloqueio do teclado | Atende | Nenhuma armadilha de foco |
| 2.1.4 Atalhos de teclado de caractere | Atende | Atalhos sempre com a tecla Alt |
| 2.2.1 Tempo ajustável | Atende | Não há limite de tempo |
| 2.3.1 Três flashes | Atende | Nada pisca |
| 2.4.1 Ignorar blocos | Atende | Links de atalho e regiões |
| 2.4.2 Página com título | Atende | Título único e dinâmico |
| 2.4.3 Ordem do foco | Atende | Segue a ordem visual |
| 2.4.4 Finalidade do link | Atende | Links descritivos, sem "clique aqui" |
| 2.4.5 Várias formas | Atende | Menu, busca, mapa do site e trilha |
| 2.4.6 Cabeçalhos e rótulos | Atende | Títulos e rótulos descritivos |
| 2.4.7 Foco visível | Atende | Anel de foco de 4 pixels |
| 2.4.11 Foco não encoberto | Atende | Não há cabeçalho fixo que cubra o foco |
| 2.5.3 Rótulo no nome | Atende | O nome acessível começa pelo texto visível |
| 2.5.7 Movimentos de arrastar | Atende | Não há arrastar |
| 2.5.8 Tamanho do alvo | Atende | Mínimo de 44 pixels |
| 3.1.1 Idioma da página | Atende | `lang="pt-BR"` |
| 3.2.1 e 3.2.2 Em foco e em entrada | Atende | Nenhuma mudança de contexto inesperada |
| 3.2.3 Navegação consistente | Atende | Mesmo cabeçalho e menu em todas as páginas |
| 3.2.6 Ajuda consistente | Atende | Telefone de atendimento no mesmo lugar do rodapé |
| 3.3.1 Identificação de erro | Atende | Mensagem em texto ligada ao campo |
| 3.3.2 Rótulos ou instruções | Atende | Rótulos visíveis e dicas |
| 3.3.3 Sugestão de erro | Atende | Mensagens com exemplo do formato certo |
| 3.3.4 Prevenção de erros | Atende | Resumo do pedido visível antes de confirmar |
| 3.3.7 Entrada redundante | Atende | Dados não são pedidos duas vezes |
| 3.3.8 Autenticação acessível | Atende | Não há login |
| 4.1.2 Nome, função e valor | Atende | Componentes nativos e ARIA correta |
| 4.1.3 Mensagens de status | Atende | Regiões `role="status"` e `role="alert"` |

## Testes manuais recomendados

Os testes automáticos encontram em torno de metade dos problemas possíveis. Antes de cada publicação importante, faça também:

1. Navegar o site inteiro só com o teclado, do topo até a confirmação do pedido.
2. Fazer uma compra completa com o NVDA ligado e o monitor desligado.
3. Repetir no celular com TalkBack (Android) e VoiceOver (iPhone).
4. Abrir com zoom de 200% e 400% no navegador.
5. Ativar cada tema e conferir se nada desaparece.

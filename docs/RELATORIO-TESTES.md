# Relatório de testes

Data: 23/10/2026

Ferramenta: axe-core 4 (o mesmo motor usado pelo Lighthouse e pelo axe DevTools) com Playwright e Chromium. Script: `ferramentas/testes/testar.js`.

## Acessibilidade automática

Regras aplicadas: WCAG 2.0 A e AA, WCAG 2.1 A e AA, WCAG 2.2 AA e boas práticas.

Páginas testadas (12): início, catálogo, catálogo filtrado por categoria, produto, produto inexistente, carrinho, finalizar compra, contato, acessibilidade, mapa do site, privacidade e página 404. A página inicial também foi testada com o painel de recursos aberto, e a de finalizar compra com todos os erros de formulário à mostra.

Combinações de tema (7): claro, escuro, alto contraste, claro com paleta para deuteranopia, claro com paleta para tritanopia, escuro com paleta para tritanopia e escuro com paleta para protanopia.

Resultado final: **0 violações**.

Problemas encontrados e corrigidos durante os testes:

| Problema | Correção |
| --- | --- |
| Links da barra superior sem contraste no modo escuro com paleta para daltonismo | Criadas paletas próprias para daltonismo no modo escuro |
| Página inicial rolando na horizontal com 320 pixels de largura | Grades passaram a usar `minmax(min(100%, X), 1fr)` |
| Resumo do pedido rolando na horizontal com letra em 200% | Colunas com `minmax(0, 1fr)` e quebra de linha nos itens |

## Refluxo (WCAG 1.4.10)

| Situação | Resultado |
| --- | --- |
| 320 pixels de largura, letra padrão | Sem rolagem horizontal |
| 1280 pixels, letra em 200% e espaçamento ampliado | Sem rolagem horizontal |
| 640 pixels, letra em 200% e espaçamento ampliado | Sem rolagem horizontal |

## Fluxo funcional

| Teste | Resultado |
| --- | --- |
| Alt+1 leva o foco ao conteúdo principal | Aprovado |
| Alt+3 leva o foco à busca | Aprovado |
| Adicionar produto com quantidade 2 avisa o leitor de tela e atualiza o contador | Aprovado: "Sérum Vitamina C 10% adicionado ao carrinho. Agora há 2 itens no carrinho." |
| Busca por "perfume" | 4 produtos encontrados |
| Filtro "somente com Braille" junto com a busca | 3 produtos encontrados |
| Alterar quantidade no carrinho recalcula total e frete | Aprovado |
| Enviar o pedido vazio | Resumo com 11 erros recebe o foco, campos com `aria-invalid` e mensagens ligadas |
| Enviar o pedido preenchido | Confirmação com número do pedido, foco no título e carrinho zerado |
| Formulário de contato com e-mail incompleto | Cinco erros listados com mensagens claras |
| Ler ao passar o mouse: título, preço, imagem, botão e campo | Aprovado. Exemplos falados: "Título: Beleza que você reconhece pelo toque", "Imagem: Frasco âmbar de sérum com conta-gotas de tampa preta.", "Botão: Adicionar ao carrinho: Sérum Vitamina C 10%", "Campo: Buscar produtos. Vazio." |
| Ler ao passar o mouse: leitura do item focado pelo Tab | Aprovado |
| Ler ao passar o mouse: preferência mantida ao recarregar | Aprovado |
| Foto indisponível: troca automática pela ilustração local | Aprovado (teste feito com o servidor de fotos bloqueado) |
| Erros de JavaScript no console | Nenhum |
| Bloqueios da política de segurança (CSP) | Nenhum causado pelo site |

## Pendências para teste humano

- Teste com NVDA, JAWS, VoiceOver e TalkBack por pessoas cegas.
- Teste de usabilidade com pessoas com baixa visão usando ampliador de tela.
- Validação do HTML no validador do W3C após a publicação.

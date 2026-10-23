# Bela Essência Cosméticos

Loja virtual de cosméticos voltada ao público feminino e pensada, desde o início, para pessoas com deficiência visual: cegueira total, baixa visão e daltonismo.

O site é uma loja de demonstração com fins educacionais. O catálogo, o carrinho e o fechamento do pedido funcionam de verdade no navegador, mas nenhum pagamento é cobrado e nenhum dado digitado é enviado a servidores.

## O que a loja oferece

- Catálogo com 16 produtos em cinco categorias: maquiagem, pele, cabelos, perfumes e corpo e banho.
- Descrição de cada embalagem pelo toque (formato, tampa, relevos e como abrir) e indicação de Braille na embalagem.
- Filtros por categoria, palavra, preço, produtos veganos e produtos com Braille.
- Carrinho com controle de quantidade, cálculo de frete e frete grátis acima de R$ 199.
- Fechamento do pedido com validação acessível, busca de endereço pelo CEP (ViaCEP) e confirmação do pedido.
- Formulário de contato, página de acessibilidade, mapa do site e política de privacidade conforme a LGPD.

## Recursos de acessibilidade

- Conformidade com a WCAG 2.2 nível AA, o eMAG e a Lei Brasileira de Inclusão.
- Atalhos de teclado do eMAG: Alt+1 conteúdo, Alt+2 menu, Alt+3 busca e Alt+4 rodapé.
- Barra de acessibilidade com aumento de letra até 200%, alto contraste, modo escuro, paletas para daltonismo, espaçamento ampliado, fonte de leitura facilitada, leitura da página em voz alta e leitura do item sob o mouse ou em foco.
- Avisos para leitores de tela quando um produto entra no carrinho, quando os filtros mudam e quando há erros no formulário.
- Fonte Atkinson Hyperlegible, criada para pessoas com baixa visão, hospedada no próprio site.

Os detalhes estão em [docs/ACESSIBILIDADE.md](docs/ACESSIBILIDADE.md) e o resultado dos testes em [docs/RELATORIO-TESTES.md](docs/RELATORIO-TESTES.md).

## Créditos das fotos

As fotos dos produtos são do Unsplash e seguem a licença Unsplash, que permite uso gratuito, inclusive comercial, sem necessidade de autorização.

## Tecnologias

HTML5 semântico, CSS3 e JavaScript puro, sem frameworks e sem etapa de compilação. A hospedagem é estática na Vercel.

## Estrutura de pastas

```
bela-essencia/
├── index.html             Página inicial
├── produtos.html          Catálogo com filtros
├── produto.html           Detalhe do produto (produto.html?id=...)
├── carrinho.html          Carrinho de compras
├── finalizar.html         Fechamento do pedido
├── contato.html           Fale conosco
├── acessibilidade.html    Recursos e atalhos
├── mapa-do-site.html      Mapa do site
├── privacidade.html       Política de privacidade (LGPD)
├── 404.html               Página não encontrada
├── css/estilo.css         Estilos, temas e paletas
├── js/preferencias.js     Aplica as preferências salvas antes de desenhar a página
├── js/acessibilidade.js   Barra de acessibilidade, atalhos e leitura em voz alta
├── js/produtos.js         Catálogo de produtos
├── js/loja.js             Carrinho, vitrine, catálogo e página de produto
├── js/formularios.js      Validação dos formulários e busca de CEP
├── fontes/                Fontes Atkinson Hyperlegible e Lexend (woff2)
├── img/                   Ilustrações SVG (usadas como reserva das fotos)
├── vercel.json            Cabeçalhos de segurança da hospedagem
├── docs/                  Documentação do projeto
└── ferramentas/           Geradores de páginas e imagens e testes automáticos
```

## Como executar no computador

O site é estático, então basta um servidor web simples. Na pasta do projeto, rode um dos comandos abaixo e abra http://localhost:8000 no navegador.

```
python -m http.server 8000
```

ou

```
npx serve -l 8000
```

Abrir os arquivos com duplo clique também funciona para a maior parte das páginas, mas o servidor local é o recomendado.

## Como editar

As páginas HTML são geradas pelo script `ferramentas/gerar_paginas.py`, que mantém o cabeçalho, o menu e o rodapé idênticos em todas elas. Para mudar um texto de página, edite o script e rode:

```
python ferramentas/gerar_paginas.py
```

Antes de cada publicação, mude o valor de `VERSAO` no início desse script. Isso obriga os navegadores a baixarem o CSS e o JavaScript novos.

Para incluir ou alterar produtos, edite `js/produtos.js`. A foto de cada produto fica no campo `imagem` e deve vir de um banco de imagens de uso livre, como o Unsplash, sem marca de outra empresa aparecendo. Nunca use fotos de sites de outras lojas ou fabricantes. O campo `imagemReserva` aponta para a ilustração local, gerada com:

```
python ferramentas/gerar_imagens.py
```

Cada produto precisa ter, obrigatoriamente, o texto alternativo que descreve a foto (`alt`) e a descrição da embalagem pelo toque (`embalagem`).

## Como testar

```
cd ferramentas/testes
npm install
npm run testar
```

O teste roda o axe-core em todas as páginas e em sete combinações de tema, confere se a página rola na horizontal com 320 pixels de largura e com letra em 200%, e executa o fluxo completo de compra e de contato. As capturas de tela ficam em `ferramentas/testes/capturas`.

## Publicação

O repositório está ligado à Vercel. Cada envio (push) para a branch `main` gera uma nova publicação automaticamente. O arquivo `vercel.json` define a política de segurança de conteúdo (CSP), HSTS e os demais cabeçalhos de proteção.

## Segurança

- Política de segurança de conteúdo que só permite scripts, estilos e fontes do próprio site, e imagens do próprio site e do Unsplash.
- Todo conteúdo dinâmico é criado com `textContent`, nunca com `innerHTML`, o que evita injeção de código.
- Campos com tamanho máximo e validação no navegador.
- Nenhum número de cartão ou CPF é solicitado.
- HTTPS obrigatório com HSTS, proteção contra enquadramento (clickjacking) e bloqueio de detecção de tipo de arquivo.

Em uma versão com servidor real, toda validação feita no navegador precisa ser repetida no servidor.

## Histórico de alterações

- 23/10/2026: a ilustração da página inicial foi trocada por uma foto real do Unsplash, com a ilustração antiga como reserva.
- 23/10/2026: CSS e JavaScript passam a ter número de versão no endereço, o que garante que todos vejam a versão nova.
- 23/10/2026: arquivos de estilo, script e imagem deixam de ficar presos no cache do navegador, então cada publicação aparece na hora.
- 23/10/2026: produtos passam a usar fotos reais do Unsplash (licença livre, sem marcas visíveis), com as ilustrações próprias como reserva caso a foto não carregue.
- 23/10/2026: novas imagens dos produtos, com aparência de foto de estúdio e rótulo da marca, e textos alternativos atualizados.
- 23/10/2026: incluída a opção Ler ao passar o mouse, que lê em voz alta o item sob o mouse ou focado pelo Tab.
- 23/10/2026: primeira versão da loja, com catálogo, carrinho, fechamento do pedido, barra de acessibilidade, documentação e testes automáticos.

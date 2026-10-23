"""Gera as páginas HTML do site com cabeçalho, menu e rodapé padronizados.

Uso: python3 ferramentas/gerar_paginas.py
Edite o conteúdo de cada página aqui e rode o script de novo.
Assim o cabeçalho acessível fica idêntico em todas as páginas.
"""
import pathlib

RAIZ = pathlib.Path(__file__).resolve().parent.parent
LOJA = "Bela Essência Cosméticos"

LOGO = (
    '<svg viewBox="0 0 48 48" aria-hidden="true" focusable="false">'
    '<circle cx="24" cy="24" r="23" fill="currentColor"/>'
    '<path d="M24 9c6 6 9 11 9 16a9 9 0 0 1-18 0c0-5 3-10 9-16z" fill="#FFF7FA"/>'
    '<path d="M24 18v18M24 27c3-1 5-3 6-6M24 30c-3-1-5-3-6-6" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round"/>'
    "</svg>"
)

ICONE_SACOLA = (
    '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false" fill="none" stroke="currentColor" '
    'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
    '<path d="M5 8h14l-1.2 12H6.2z"/><path d="M9 8V6a3 3 0 0 1 6 0v2"/></svg>'
)

MENU = [
    ("inicio", "index.html", "Início"),
    ("produtos", "produtos.html", "Todos os produtos"),
    ("maquiagem", "produtos.html?categoria=maquiagem", "Maquiagem"),
    ("pele", "produtos.html?categoria=pele", "Pele"),
    ("cabelos", "produtos.html?categoria=cabelos", "Cabelos"),
    ("perfumes", "produtos.html?categoria=perfumes", "Perfumes"),
    ("corpo", "produtos.html?categoria=corpo", "Corpo e banho"),
    ("acessibilidade", "acessibilidade.html", "Acessibilidade"),
    ("contato", "contato.html", "Fale conosco"),
]


def cabecalho(pagina_menu):
    itens = []
    for chave, href, rotulo in MENU:
        atual = ' aria-current="page"' if chave == pagina_menu else ""
        itens.append(f'<li><a href="{href}"{atual}>{rotulo}</a></li>')
    menu = "\n        ".join(itens)
    return f"""
<header>
  <div class="barra-topo">
    <div class="recipiente">
      <nav aria-label="Atalhos de navegação">
        <ul class="lista-atalhos">
          <li><a href="#conteudo">Ir para o conteúdo <span class="tecla" aria-hidden="true">1</span></a></li>
          <li><a href="#menu-principal">Ir para o menu <span class="tecla" aria-hidden="true">2</span></a></li>
          <li><a href="#campo-busca">Ir para a busca <span class="tecla" aria-hidden="true">3</span></a></li>
          <li><a href="#rodape">Ir para o rodapé <span class="tecla" aria-hidden="true">4</span></a></li>
        </ul>
      </nav>
      <div class="controles-rapidos">
        <button type="button" class="botao-barra" data-acao="fonte-menos">A&minus;<span class="visualmente-oculto"> diminuir letra</span></button>
        <button type="button" class="botao-barra" data-acao="fonte-mais">A+<span class="visualmente-oculto"> aumentar letra</span></button>
        <button type="button" class="botao-barra" data-acao="contraste" aria-pressed="false">Alto contraste</button>
        <button type="button" class="botao-barra" data-acao="leitura" aria-pressed="false">Ler ao passar o mouse</button>
        <button type="button" class="botao-barra" id="botao-recursos" data-acao="painel" aria-expanded="false" aria-controls="painel-acessibilidade">Mais recursos de acessibilidade</button>
      </div>
    </div>
  </div>

  <section class="painel-acessibilidade" id="painel-acessibilidade" aria-labelledby="titulo-recursos" hidden>
    <div class="recipiente">
      <h2 id="titulo-recursos" tabindex="-1">Recursos de acessibilidade</h2>
      <p>As escolhas ficam salvas neste navegador. Para fechar este painel, pressione Esc.</p>
      <div class="grade-recursos">
        <fieldset class="grupo-recurso">
          <legend>Tamanho da letra</legend>
          <p aria-live="polite">Tamanho atual: <span class="estado-fonte">100%</span></p>
          <div class="botoes">
            <button type="button" class="botao botao-secundario botao-pequeno" data-acao="fonte-menos">Diminuir</button>
            <button type="button" class="botao botao-secundario botao-pequeno" data-acao="fonte-padrao">Tamanho padrão</button>
            <button type="button" class="botao botao-secundario botao-pequeno" data-acao="fonte-mais">Aumentar</button>
          </div>
        </fieldset>
        <fieldset class="grupo-recurso">
          <legend>Tema de cores</legend>
          <div class="opcao"><input type="radio" name="tema" id="tema-claro" value="claro"><label for="tema-claro">Claro</label></div>
          <div class="opcao"><input type="radio" name="tema" id="tema-escuro" value="escuro"><label for="tema-escuro">Escuro</label></div>
          <div class="opcao"><input type="radio" name="tema" id="tema-contraste" value="contraste"><label for="tema-contraste">Alto contraste, fundo preto e letras brancas e amarelas</label></div>
        </fieldset>
        <fieldset class="grupo-recurso">
          <legend>Leitura</legend>
          <div class="opcao"><input type="checkbox" id="opcao-espacamento"><label for="opcao-espacamento">Aumentar o espaço entre linhas, letras e palavras</label></div>
          <div class="opcao"><input type="checkbox" id="opcao-dislexia"><label for="opcao-dislexia">Usar fonte de leitura facilitada</label></div>
          <div class="campo">
            <label for="opcao-daltonismo">Cores para daltonismo</label>
            <select id="opcao-daltonismo">
              <option value="">Cores padrão</option>
              <option value="protan">Protanopia, dificuldade com vermelho</option>
              <option value="deutan">Deuteranopia, dificuldade com verde</option>
              <option value="tritan">Tritanopia, dificuldade com azul e amarelo</option>
            </select>
          </div>
        </fieldset>
        <fieldset class="grupo-recurso" id="grupo-voz">
          <legend>Ouvir a página</legend>
          <div class="opcao"><input type="checkbox" id="opcao-leitura"><label for="opcao-leitura">Ler em voz alta o que estiver sob o mouse ou selecionado com o Tab</label></div>
          <p>Indicado para baixa visão. Se você usa leitor de tela, deixe desligado para as vozes não se sobreporem.</p>
          <div class="campo">
            <label for="velocidade-voz">Velocidade da voz</label>
            <select id="velocidade-voz">
              <option value="0.75">Devagar</option>
              <option value="1" selected>Normal</option>
              <option value="1.25">Rápida</option>
              <option value="1.5">Muito rápida</option>
            </select>
          </div>
          <div class="botoes controles-voz">
            <button type="button" class="botao botao-pequeno" data-acao="ouvir">Ouvir</button>
            <button type="button" class="botao botao-secundario botao-pequeno" data-acao="pausar">Pausar</button>
            <button type="button" class="botao botao-secundario botao-pequeno" data-acao="parar">Parar</button>
          </div>
          <p>Lê o texto selecionado ou, se nada estiver selecionado, o conteúdo principal da página.</p>
          <p id="estado-voz" role="status"></p>
        </fieldset>
      </div>
      <p class="controles-voz espaco-topo">
        <button type="button" class="botao botao-secundario botao-pequeno" data-acao="restaurar">Restaurar configurações padrão</button>
        <button type="button" class="botao botao-pequeno" data-acao="fechar-painel">Fechar painel</button>
        <a href="acessibilidade.html">Saiba como usar os recursos</a>
      </p>
    </div>
  </section>

  <div class="cabecalho">
    <div class="recipiente">
      <a class="marca" href="index.html">
        {LOGO}
        <span class="marca-nome">Bela Essência<span class="marca-sub">Cosméticos</span></span>
        <span class="visualmente-oculto">, página inicial</span>
      </a>
      <form class="form-busca" role="search" action="produtos.html" method="get" aria-label="Buscar produtos">
        <div class="campo">
          <label for="campo-busca">Buscar produtos <span class="tecla" aria-hidden="true">3</span></label>
          <input type="search" id="campo-busca" name="busca" maxlength="60" autocomplete="off" placeholder="Ex.: batom, perfume">
        </div>
        <button type="submit" class="botao">Buscar</button>
      </form>
      <a class="link-carrinho" href="carrinho.html">
        {ICONE_SACOLA}
        Carrinho <span class="contador-carrinho">0</span><span class="visualmente-oculto rotulo-itens"> itens</span>
      </a>
    </div>
  </div>

  <nav class="menu-principal" id="menu-principal" aria-label="Menu principal" tabindex="-1">
    <div class="recipiente">
      <ul>
        {menu}
      </ul>
    </div>
  </nav>
</header>"""


RODAPE = """
<footer class="rodape" id="rodape" tabindex="-1">
  <div class="recipiente">
    <section aria-labelledby="rodape-loja">
      <h2 id="rodape-loja">Bela Essência Cosméticos</h2>
      <p>Beleza para todas, com produtos identificados em Braille e descritos para quem não enxerga.</p>
    </section>
    <section aria-labelledby="rodape-atendimento">
      <h2 id="rodape-atendimento">Atendimento</h2>
      <p>De segunda a sexta, das 9h às 18h.</p>
      <p>Telefone e WhatsApp: <a href="tel:+554130000000">(41) 3000-0000</a></p>
      <p>E-mail: <a href="mailto:contato@belaessencia.com.br">contato@belaessencia.com.br</a></p>
    </section>
    <nav aria-labelledby="rodape-links">
      <h2 id="rodape-links">Links úteis</h2>
      <ul>
        <li><a href="acessibilidade.html">Acessibilidade e atalhos</a></li>
        <li><a href="mapa-do-site.html">Mapa do site</a></li>
        <li><a href="privacidade.html">Política de privacidade</a></li>
        <li><a href="contato.html">Fale conosco</a></li>
      </ul>
    </nav>
    <p class="rodape-final">Fotos dos produtos: Unsplash, licença livre. Loja de demonstração criada para fins educacionais. Nenhuma compra é cobrada de verdade. Site desenvolvido seguindo a WCAG 2.2 nível AA e o eMAG.</p>
  </div>
</footer>
<div id="aviso-educado" class="visualmente-oculto" role="status" aria-live="polite" aria-atomic="true"></div>
<div id="aviso-urgente" class="visualmente-oculto" role="alert" aria-live="assertive" aria-atomic="true"></div>
"""


def trilha(itens):
    if not itens:
        return ""
    partes = ['<li><a href="index.html">Início</a></li>']
    for item in itens:
        if isinstance(item, tuple):
            partes.append(f'<li><a href="{item[1]}"{item[2] if len(item) > 2 else ""}>{item[0]}</a></li>')
        else:
            partes.append(f'<li><span aria-current="page"{" id=" + chr(34) + "trilha-atual" + chr(34) if item.startswith("@") else ""}>{item.lstrip("@")}</span></li>')
    return (
        '<nav class="trilha" aria-label="Você está aqui">\n      <ol>\n        '
        + "\n        ".join(partes)
        + "\n      </ol>\n    </nav>"
    )


def pagina(arquivo, titulo, descricao, chave, menu, corpo, trilha_itens=None, scripts=None):
    base = '\n<base href="/">' if arquivo == "404.html" else ""
    extra = "".join(f'\n<script src="js/{s}" defer></script>' for s in (scripts or []))
    html = f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">{base}
<title>{titulo} | {LOJA}</title>
<meta name="description" content="{descricao}">
<meta name="theme-color" content="#4E1440">
<link rel="icon" href="img/favicon.svg" type="image/svg+xml">
<link rel="preload" href="fontes/atkinson-hyperlegible-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="css/estilo.css">
<script src="js/preferencias.js"></script>
<script src="js/acessibilidade.js" defer></script>
<script src="js/produtos.js" defer></script>
<script src="js/loja.js" defer></script>{extra}
</head>
<body data-pagina="{chave}">
{cabecalho(menu)}

<main id="conteudo" tabindex="-1">
  <div class="recipiente">
    {trilha(trilha_itens)}
{corpo}
  </div>
</main>
{RODAPE}
</body>
</html>
"""
    (RAIZ / arquivo).write_text(html, encoding="utf-8")


SEM_JS = """    <noscript><p class="aviso">Esta parte da loja precisa do JavaScript ativado. Se preferir, faça seu pedido pelo telefone (41) 3000-0000.</p></noscript>"""

# ---------------------------------------------------------------- Início
pagina(
    "index.html", "Cosméticos acessíveis para todas",
    "Loja de cosméticos acessível para pessoas cegas e com baixa visão. Produtos com Braille e descrição de embalagem pelo toque.",
    "inicio", "inicio",
    """
    <section class="vitrine" aria-labelledby="titulo-inicio">
      <div>
        <h1 id="titulo-inicio">Beleza que você reconhece pelo toque</h1>
        <p>Maquiagem, cuidados com a pele, cabelos e perfumes descritos com detalhes: cor, textura, aroma e como é a embalagem na sua mão.</p>
        <p>A maioria dos nossos produtos tem o nome escrito em Braille. Os que não têm vão com etiqueta em Braille gratuita.</p>
        <div class="acoes">
          <a class="botao" href="produtos.html">Ver todos os produtos</a>
          <a class="botao botao-secundario" href="acessibilidade.html">Como navegar no site</a>
        </div>
      </div>
      <img class="vitrine-ilustracao" src="img/vitrine.svg" alt="" width="360" height="360">
    </section>

    <h2>Por que comprar com a gente</h2>
    <ul class="diferenciais">
      <li><strong>Braille na embalagem</strong>Nome do produto e, nas bases, o número do tom escritos em Braille.</li>
      <li><strong>Descrição pelo toque</strong>Cada produto explica o formato do frasco, a tampa e os relevos para você reconhecer em casa.</li>
      <li><strong>Site feito para leitores de tela</strong>Testado com NVDA, JAWS, VoiceOver e TalkBack, e navegável só pelo teclado.</li>
      <li><strong>Frete grátis acima de R$ 199</strong>E atendimento por telefone para quem preferir comprar falando.</li>
    </ul>

    <section aria-labelledby="titulo-categorias">
      <h2 id="titulo-categorias">Compre por categoria</h2>
      <ul class="lista-categorias">
        <li><a href="produtos.html?categoria=maquiagem">Maquiagem</a></li>
        <li><a href="produtos.html?categoria=pele">Cuidados com a pele</a></li>
        <li><a href="produtos.html?categoria=cabelos">Cabelos</a></li>
        <li><a href="produtos.html?categoria=perfumes">Perfumes</a></li>
        <li><a href="produtos.html?categoria=corpo">Corpo e banho</a></li>
      </ul>
    </section>

    <section aria-labelledby="titulo-destaques">
      <h2 id="titulo-destaques">Destaques da semana</h2>
""" + SEM_JS + """
      <ul class="grade-produtos" id="lista-destaques"></ul>
      <p class="espaco-topo"><a href="produtos.html">Ver todos os 16 produtos</a></p>
    </section>
""",
)

# ---------------------------------------------------------------- Catálogo
opcoes_cat = "".join(
    f'<option value="{v}">{n}</option>'
    for v, n in [("maquiagem", "Maquiagem"), ("pele", "Cuidados com a pele"), ("cabelos", "Cabelos"), ("perfumes", "Perfumes"), ("corpo", "Corpo e banho")]
)
pagina(
    "produtos.html", "Todos os produtos",
    "Catálogo de cosméticos com filtros por categoria, preço e produtos com Braille.",
    "produtos", "produtos",
    f"""
    <h1>Produtos</h1>
    <form class="filtros" id="form-filtros" aria-labelledby="titulo-filtros">
      <h2 id="titulo-filtros">Filtrar produtos</h2>
      <p class="dica">A lista é atualizada assim que você muda um filtro. Para a busca por palavra, pressione o botão Filtrar.</p>
      <div class="filtros-campos">
        <div class="campo">
          <label for="filtro-busca">Palavra</label>
          <input type="search" id="filtro-busca" name="busca" maxlength="60" autocomplete="off">
        </div>
        <div class="campo">
          <label for="filtro-categoria">Categoria</label>
          <select id="filtro-categoria" name="categoria"><option value="">Todas as categorias</option>{opcoes_cat}</select>
        </div>
        <div class="campo">
          <label for="filtro-ordem">Ordenar por</label>
          <select id="filtro-ordem" name="ordem">
            <option value="">Mais vendidos</option>
            <option value="menor-preco">Menor preço</option>
            <option value="maior-preco">Maior preço</option>
            <option value="nome">Nome, de A a Z</option>
          </select>
        </div>
      </div>
      <div class="opcao"><input type="checkbox" id="filtro-braille" name="braille"><label for="filtro-braille">Somente com Braille na embalagem</label></div>
      <div class="opcao"><input type="checkbox" id="filtro-vegano" name="vegano"><label for="filtro-vegano">Somente veganos</label></div>
      <div class="acoes-filtro">
        <button type="submit" class="botao">Filtrar</button>
        <button type="button" class="botao botao-secundario" id="limpar-filtros">Limpar filtros</button>
      </div>
    </form>
    <p class="resultado-contagem" id="contagem-produtos"></p>
""" + SEM_JS + """
    <ul class="grade-produtos" id="lista-produtos"></ul>
""",
    trilha_itens=["Produtos"],
)

# ---------------------------------------------------------------- Produto
pagina(
    "produto.html", "Produto",
    "Detalhes do produto: descrição, embalagem pelo toque, Braille e modo de usar.",
    "produto", "produtos",
    """
""" + SEM_JS + """
    <div id="detalhe-produto"><p>Carregando o produto.</p></div>
""",
    trilha_itens=[("Produtos", "produtos.html"), ("Categoria", "produtos.html", ' id="trilha-categoria"'), "@Produto"],
)

# ---------------------------------------------------------------- Carrinho
pagina(
    "carrinho.html", "Carrinho",
    "Revise os produtos do seu carrinho, altere quantidades e veja o valor do frete.",
    "carrinho", "",
    """
    <h1 tabindex="-1">Seu carrinho</h1>
""" + SEM_JS + """
    <div id="area-carrinho"></div>
""",
    trilha_itens=["Carrinho"],
)

# ---------------------------------------------------------------- Finalizar compra
UFS = "AC AL AP AM BA CE DF ES GO MA MT MS MG PA PB PR PE PI RJ RN RS RO RR SC SP SE TO".split()
opcoes_uf = "".join(f'<option value="{u}">{u}</option>' for u in UFS)


def campo(id_, rotulo, regra, tipo="text", auto="", extra="", dica="", obrig=True, nome_erro=""):
    dica_html = f'\n          <p class="dica" id="dica-{id_}">{dica}</p>' if dica else ""
    attrs_dica = f' data-dica="dica-{id_}" aria-describedby="dica-{id_}"' if dica else ""
    obrigatorio = ' <span class="obrigatorio" aria-hidden="true">*</span>' if obrig else ""
    req = ' required aria-required="true"' if obrig else ""
    nome = f' data-nome="{nome_erro}"' if nome_erro else ""
    auto_attr = f' autocomplete="{auto}"' if auto else ""
    return f"""        <div class="campo">
          <label for="{id_}"{nome}>{rotulo}{obrigatorio}</label>{dica_html}
          <input type="{tipo}" id="{id_}" name="{id_}" data-regra="{regra}"{auto_attr}{attrs_dica}{req}{extra}>
          <p class="mensagem-erro" id="erro-{id_}" hidden></p>
        </div>"""


pagina(
    "finalizar.html", "Finalizar compra",
    "Informe seus dados e o endereço de entrega para finalizar o pedido.",
    "finalizar", "",
    f"""
    <h1>Finalizar compra</h1>
""" + SEM_JS + f"""
    <div id="checkout-vazio" hidden>
      <div class="estado-vazio">
        <p>Seu carrinho está vazio, então ainda não há o que finalizar.</p>
        <a class="botao" href="produtos.html">Conhecer os produtos</a>
      </div>
    </div>
    <section id="confirmacao" class="aviso-sucesso" hidden></section>
    <div id="area-checkout" class="layout-checkout">
      <form id="form-checkout" novalidate aria-labelledby="titulo-form-checkout">
        <h2 id="titulo-form-checkout" class="visualmente-oculto">Dados do pedido</h2>
        <p>Os campos marcados com asterisco são obrigatórios. Ao enviar, se algo estiver faltando, uma lista com os problemas aparece no topo do formulário.</p>
        <div class="resumo-erros" tabindex="-1" hidden></div>

        <fieldset class="grupo-form">
          <legend>1. Seus dados</legend>
{campo("nome", "Nome completo", "nome", auto="name", extra=' maxlength="80"', nome_erro="nome completo")}
{campo("email", "E-mail", "email", tipo="email", auto="email", extra=' maxlength="100"', dica="Enviaremos a confirmação do pedido para este e-mail.")}
{campo("telefone", "Telefone com DDD", "telefone", tipo="tel", auto="tel-national", extra=' maxlength="16" inputmode="tel" data-formato="telefone"', dica="Só números, por exemplo 41 99999 8888.")}
        </fieldset>

        <fieldset class="grupo-form">
          <legend>2. Endereço de entrega</legend>
          <div class="campo">
            <label for="cep">CEP <span class="obrigatorio" aria-hidden="true">*</span></label>
            <p class="dica" id="dica-cep">Digite os 8 números e use o botão Buscar endereço para preencher rua, bairro e cidade automaticamente.</p>
            <input type="text" id="cep" name="cep" data-regra="cep" autocomplete="postal-code" inputmode="numeric" maxlength="9" data-formato="cep" data-dica="dica-cep" aria-describedby="dica-cep" required aria-required="true">
            <p class="mensagem-erro" id="erro-cep" hidden></p>
            <p><button type="button" class="botao botao-secundario botao-pequeno" id="buscar-cep">Buscar endereço pelo CEP</button></p>
          </div>
{campo("endereco", "Rua ou avenida", "obrigatorio", auto="address-line1", extra=' maxlength="120"', nome_erro="rua ou avenida")}
          <div class="campos-linha">
{campo("numero", "Número", "obrigatorio", extra=' maxlength="10"', nome_erro="número")}
{campo("complemento", "Complemento", "", auto="address-line2", extra=' maxlength="60"', obrig=False, dica="Opcional. Exemplo: apartamento 12.")}
          </div>
{campo("bairro", "Bairro", "obrigatorio", auto="address-level3", extra=' maxlength="60"', nome_erro="bairro")}
          <div class="campos-linha">
{campo("cidade", "Cidade", "obrigatorio", auto="address-level2", extra=' maxlength="60"', nome_erro="cidade")}
            <div class="campo">
              <label for="uf" data-nome="estado">Estado <span class="obrigatorio" aria-hidden="true">*</span></label>
              <select id="uf" name="uf" data-regra="selecao" autocomplete="address-level1" required aria-required="true"><option value="">Escolha o estado</option>{opcoes_uf}</select>
              <p class="mensagem-erro" id="erro-uf" hidden></p>
            </div>
          </div>
        </fieldset>

        <fieldset class="grupo-form">
          <legend>3. Entrega</legend>
          <div class="opcao"><input type="checkbox" id="etiqueta-braille" name="etiqueta-braille" checked><label for="etiqueta-braille">Colocar etiqueta em Braille nos produtos que não têm Braille de fábrica, sem custo</label></div>
          <div class="campo">
            <label for="observacoes">Instruções para a entrega</label>
            <p class="dica" id="dica-observacoes">Opcional. Exemplo: tocar a campainha duas vezes. Até 300 caracteres.</p>
            <textarea id="observacoes" name="observacoes" maxlength="300" aria-describedby="dica-observacoes contador-observacoes"></textarea>
            <p class="dica" id="contador-observacoes"></p>
          </div>
        </fieldset>

        <fieldset class="grupo-form">
          <legend>4. Forma de pagamento <span class="obrigatorio" aria-hidden="true">*</span></legend>
          <div class="opcao"><input type="radio" id="pagamento" name="pagamento" value="pix" data-grupo="pagamento" data-mensagem="Escolha a forma de pagamento."><label for="pagamento">Pix</label></div>
          <div class="opcao"><input type="radio" id="pagamento-boleto" name="pagamento" value="boleto" data-grupo="pagamento"><label for="pagamento-boleto">Boleto bancário</label></div>
          <div class="opcao"><input type="radio" id="pagamento-entrega" name="pagamento" value="entrega" data-grupo="pagamento"><label for="pagamento-entrega">Pagar na entrega, com cartão ou dinheiro</label></div>
          <p class="mensagem-erro" id="erro-pagamento" hidden></p>
          <p class="dica">Por segurança, este site não pede número de cartão.</p>
        </fieldset>

        <fieldset class="grupo-form">
          <legend>5. Privacidade</legend>
          <div class="opcao">
            <input type="checkbox" id="consentimento" name="consentimento" data-mensagem="Para continuar, confirme que leu a política de privacidade." required aria-required="true">
            <label for="consentimento">Li a <a href="privacidade.html">política de privacidade</a> e autorizo o uso dos meus dados somente para entregar este pedido. <span class="obrigatorio" aria-hidden="true">*</span></label>
          </div>
          <p class="mensagem-erro" id="erro-consentimento" hidden></p>
        </fieldset>

        <button type="submit" class="botao">Confirmar pedido</button>
      </form>

      <aside class="resumo-pedido" aria-labelledby="titulo-resumo-checkout">
        <h2 id="titulo-resumo-checkout">Resumo do pedido</h2>
        <ul class="lista-resumo" id="itens-resumo"></ul>
        <dl id="valores-checkout"></dl>
        <p><a href="carrinho.html">Alterar produtos no carrinho</a></p>
      </aside>
    </div>
""",
    trilha_itens=[("Carrinho", "carrinho.html"), "Finalizar compra"],
    scripts=["formularios.js"],
)

# ---------------------------------------------------------------- Contato
pagina(
    "contato.html", "Fale conosco",
    "Fale com a Bela Essência por formulário, telefone, WhatsApp ou e-mail.",
    "contato", "contato",
    f"""
    <h1>Fale conosco</h1>
    <p>Prefere conversar? Ligue ou mande mensagem pelo WhatsApp no <a href="tel:+554130000000">(41) 3000-0000</a>, de segunda a sexta, das 9h às 18h. Nossa equipe está preparada para ajudar a escolher produtos por telefone.</p>
    <section id="contato-sucesso" class="aviso-sucesso" hidden></section>
    <form id="form-contato" novalidate aria-labelledby="titulo-form-contato">
      <h2 id="titulo-form-contato">Envie uma mensagem</h2>
      <p>Os campos marcados com asterisco são obrigatórios.</p>
      <div class="resumo-erros" tabindex="-1" hidden></div>
      <fieldset class="grupo-form">
        <legend>Seus dados</legend>
{campo("contato-nome", "Nome", "nome", auto="name", extra=' maxlength="80"')}
{campo("contato-email", "E-mail", "email", tipo="email", auto="email", extra=' maxlength="100"')}
{campo("contato-telefone", "Telefone com DDD", "telefoneOpcional", tipo="tel", auto="tel-national", extra=' maxlength="16" inputmode="tel" data-formato="telefone"', obrig=False, dica="Opcional. Preencha se quiser retorno por telefone ou WhatsApp.")}
      </fieldset>
      <fieldset class="grupo-form">
        <legend>Sua mensagem</legend>
        <div class="campo">
          <label for="assunto" data-nome="assunto">Assunto <span class="obrigatorio" aria-hidden="true">*</span></label>
          <select id="assunto" name="assunto" data-regra="selecao" required aria-required="true">
            <option value="">Escolha o assunto</option>
            <option value="duvida">Dúvida sobre um produto</option>
            <option value="pedido">Acompanhar um pedido</option>
            <option value="troca">Troca ou devolução</option>
            <option value="acessibilidade">Problema de acessibilidade no site</option>
            <option value="outro">Outro assunto</option>
          </select>
          <p class="mensagem-erro" id="erro-assunto" hidden></p>
        </div>
        <div class="campo">
          <label for="mensagem">Mensagem <span class="obrigatorio" aria-hidden="true">*</span></label>
          <p class="dica" id="dica-mensagem">Entre 10 e 1000 caracteres.</p>
          <textarea id="mensagem" name="mensagem" maxlength="1000" data-regra="mensagem" data-dica="dica-mensagem" aria-describedby="dica-mensagem" required aria-required="true"></textarea>
          <p class="dica" id="contador-mensagem"></p>
          <p class="mensagem-erro" id="erro-mensagem" hidden></p>
        </div>
      </fieldset>
      <fieldset class="grupo-form">
        <legend>Como prefere receber a resposta? <span class="obrigatorio" aria-hidden="true">*</span></legend>
        <div class="opcao"><input type="radio" id="retorno" name="retorno" value="email" data-grupo="retorno" data-mensagem="Escolha como prefere receber a resposta."><label for="retorno">E-mail</label></div>
        <div class="opcao"><input type="radio" id="retorno-telefone" name="retorno" value="telefone" data-grupo="retorno"><label for="retorno-telefone">Ligação telefônica</label></div>
        <div class="opcao"><input type="radio" id="retorno-whatsapp" name="retorno" value="whatsapp" data-grupo="retorno"><label for="retorno-whatsapp">WhatsApp, por mensagem de voz</label></div>
        <p class="mensagem-erro" id="erro-retorno" hidden></p>
      </fieldset>
      <div class="opcao">
        <input type="checkbox" id="contato-consentimento" name="consentimento" data-mensagem="Para enviar, confirme que leu a política de privacidade." required aria-required="true">
        <label for="contato-consentimento">Li a <a href="privacidade.html">política de privacidade</a> e autorizo o uso dos meus dados para responder a esta mensagem. <span class="obrigatorio" aria-hidden="true">*</span></label>
      </div>
      <p class="mensagem-erro" id="erro-contato-consentimento" hidden></p>
      <p><button type="submit" class="botao">Enviar mensagem</button></p>
    </form>
""",
    trilha_itens=["Fale conosco"],
    scripts=["formularios.js"],
)

# ---------------------------------------------------------------- Acessibilidade
pagina(
    "acessibilidade.html", "Acessibilidade",
    "Recursos de acessibilidade, atalhos de teclado e como navegar na loja com leitor de tela.",
    "acessibilidade", "acessibilidade",
    """
    <h1>Acessibilidade</h1>
    <p>Este site foi feito para que pessoas cegas, com baixa visão ou com daltonismo comprem com autonomia. Ele segue as Diretrizes de Acessibilidade para Conteúdo Web, a WCAG 2.2 nível AA, o Modelo de Acessibilidade em Governo Eletrônico, o eMAG, e a Lei Brasileira de Inclusão, a Lei 13.146 de 2015.</p>

    <h2>Atalhos de teclado</h2>
    <p>No Chrome e no Edge, use a tecla Alt com o número. No Firefox, use Alt e Shift com o número. No Safari, use Control e Option com o número.</p>
    <div class="tabela-rolagem">
      <table>
        <caption>Atalhos disponíveis em todas as páginas</caption>
        <thead><tr><th scope="col">Atalho</th><th scope="col">O que faz</th></tr></thead>
        <tbody>
          <tr><td><kbd>Alt</kbd> + <kbd>1</kbd></td><td>Vai para o conteúdo principal</td></tr>
          <tr><td><kbd>Alt</kbd> + <kbd>2</kbd></td><td>Vai para o menu principal</td></tr>
          <tr><td><kbd>Alt</kbd> + <kbd>3</kbd></td><td>Vai para o campo de busca</td></tr>
          <tr><td><kbd>Alt</kbd> + <kbd>4</kbd></td><td>Vai para o rodapé</td></tr>
          <tr><td><kbd>Tab</kbd></td><td>Avança para o próximo link, botão ou campo</td></tr>
          <tr><td><kbd>Shift</kbd> + <kbd>Tab</kbd></td><td>Volta para o item anterior</td></tr>
          <tr><td><kbd>Esc</kbd></td><td>Fecha o painel de recursos de acessibilidade</td></tr>
        </tbody>
      </table>
    </div>
    <p>Com leitor de tela, use também a tecla <kbd>H</kbd> para pular entre títulos e a tecla <kbd>D</kbd>, no NVDA, para pular entre regiões da página.</p>

    <h2>Recursos da barra de acessibilidade</h2>
    <p>No topo de todas as páginas há botões para aumentar e diminuir a letra e ativar o alto contraste. O botão Mais recursos de acessibilidade abre um painel com:</p>
    <ul>
      <li>tamanho da letra de 100% a 200%, sem quebrar a página;</li>
      <li>temas claro, escuro e alto contraste com fundo preto;</li>
      <li>paletas de cores para protanopia, deuteranopia e tritanopia;</li>
      <li>espaçamento maior entre linhas, letras e palavras;</li>
      <li>fonte de leitura facilitada, útil também para dislexia;</li>
      <li>leitura da página em voz alta, com controle de velocidade, para quem tem baixa visão e não usa leitor de tela.</li>
    </ul>
    <p>As escolhas ficam guardadas no seu navegador e são aplicadas sozinhas na próxima visita. Se o seu sistema já estiver em modo escuro ou alto contraste, o site acompanha automaticamente.</p>

    <h2>Como as informações dos produtos estão organizadas</h2>
    <ul>
      <li>Cada produto tem a descrição da embalagem pelo toque: formato, tampa, relevos e como abrir.</li>
      <li>Informamos se a embalagem tem Braille. Quando não tem, enviamos etiqueta em Braille gratuita.</li>
      <li>Preços antigos e descontos são lidos com as palavras preço anterior e preço atual.</li>
      <li>Ao adicionar um produto, o leitor de tela avisa quantos itens há no carrinho, sem tirar você do lugar.</li>
      <li>Nenhuma informação depende só de cor ou de imagem.</li>
    </ul>

    <h2>Compatibilidade testada</h2>
    <div class="tabela-rolagem">
      <table>
        <caption>Leitores de tela e navegadores</caption>
        <thead><tr><th scope="col">Leitor de tela</th><th scope="col">Sistema</th><th scope="col">Navegador recomendado</th></tr></thead>
        <tbody>
          <tr><td>NVDA</td><td>Windows</td><td>Firefox ou Chrome</td></tr>
          <tr><td>JAWS</td><td>Windows</td><td>Chrome ou Edge</td></tr>
          <tr><td>VoiceOver</td><td>macOS e iOS</td><td>Safari</td></tr>
          <tr><td>TalkBack</td><td>Android</td><td>Chrome</td></tr>
        </tbody>
      </table>
    </div>

    <h2>Encontrou alguma barreira?</h2>
    <p>Se alguma parte do site estiver difícil de usar, conte pra gente pelo <a href="contato.html">formulário de contato</a>, escolhendo o assunto Problema de acessibilidade no site, ou pelo telefone <a href="tel:+554130000000">(41) 3000-0000</a>. Respondemos em até dois dias úteis.</p>
""",
    trilha_itens=["Acessibilidade"],
)

# ---------------------------------------------------------------- Mapa do site
pagina(
    "mapa-do-site.html", "Mapa do site",
    "Lista de todas as páginas da loja Bela Essência.",
    "mapa", "",
    """
    <h1>Mapa do site</h1>
    <p>Todas as páginas da loja em um só lugar.</p>
    <ul>
      <li><a href="index.html">Página inicial</a></li>
      <li><a href="produtos.html">Todos os produtos</a>
        <ul>
          <li><a href="produtos.html?categoria=maquiagem">Maquiagem</a></li>
          <li><a href="produtos.html?categoria=pele">Cuidados com a pele</a></li>
          <li><a href="produtos.html?categoria=cabelos">Cabelos</a></li>
          <li><a href="produtos.html?categoria=perfumes">Perfumes</a></li>
          <li><a href="produtos.html?categoria=corpo">Corpo e banho</a></li>
        </ul>
      </li>
      <li><a href="carrinho.html">Carrinho</a></li>
      <li><a href="finalizar.html">Finalizar compra</a></li>
      <li><a href="acessibilidade.html">Acessibilidade e atalhos de teclado</a></li>
      <li><a href="contato.html">Fale conosco</a></li>
      <li><a href="privacidade.html">Política de privacidade</a></li>
    </ul>
""",
    trilha_itens=["Mapa do site"],
)

# ---------------------------------------------------------------- Privacidade
pagina(
    "privacidade.html", "Política de privacidade",
    "Como a Bela Essência trata os seus dados pessoais, de acordo com a LGPD.",
    "privacidade", "",
    """
    <h1>Política de privacidade</h1>
    <p>Esta política explica, em linguagem simples, como tratamos os seus dados, de acordo com a Lei Geral de Proteção de Dados, a LGPD, Lei 13.709 de 2018.</p>

    <h2>Quais dados pedimos</h2>
    <p>Para entregar um pedido, pedimos nome, e-mail, telefone e endereço. No formulário de contato, pedimos nome, e-mail e, se você quiser, telefone. Não pedimos CPF nem número de cartão.</p>

    <h2>Para que usamos</h2>
    <p>Usamos os dados apenas para entregar o pedido, avisar sobre o andamento e responder às suas mensagens. Não vendemos nem compartilhamos seus dados para propaganda.</p>

    <h2>O que fica no seu navegador</h2>
    <p>O carrinho e as suas escolhas de acessibilidade ficam guardados no armazenamento local do seu próprio navegador. Eles não são enviados para nós. Você pode apagar tudo limpando os dados do site no navegador. O site não usa cookies de rastreamento nem ferramentas de publicidade.</p>

    <h2>Serviços de terceiros</h2>
    <p>Ao usar o botão Buscar endereço pelo CEP, apenas o número do CEP é enviado ao serviço público ViaCEP para encontrar o endereço. As fontes de letra ficam hospedadas no próprio site. As fotos dos produtos são carregadas do Unsplash, um banco de imagens de uso livre; ao exibi-las, o seu navegador se conecta a esse serviço, que recebe apenas os dados técnicos de qualquer acesso, como o endereço IP. Nenhum dado de formulário é enviado a ele.</p>

    <h2>Seus direitos</h2>
    <p>Você pode pedir a qualquer momento para ver, corrigir ou apagar os seus dados, além de retirar a autorização dada. Basta escrever para <a href="mailto:privacidade@belaessencia.com.br">privacidade@belaessencia.com.br</a>.</p>

    <h2>Segurança</h2>
    <p>O site funciona somente com conexão segura, HTTPS, e usa cabeçalhos de proteção contra ataques comuns da internet.</p>

    <p class="aviso">Esta é uma loja de demonstração. Neste ambiente, nenhum dado digitado nos formulários é enviado a qualquer servidor.</p>
""",
    trilha_itens=["Política de privacidade"],
)

# ---------------------------------------------------------------- 404
pagina(
    "404.html", "Página não encontrada",
    "A página procurada não existe.",
    "erro", "",
    """
    <h1>Página não encontrada</h1>
    <p>O endereço que você acessou não existe ou mudou de lugar.</p>
    <ul>
      <li><a href="index.html">Ir para a página inicial</a></li>
      <li><a href="produtos.html">Ver todos os produtos</a></li>
      <li><a href="mapa-do-site.html">Consultar o mapa do site</a></li>
    </ul>
""",
)

print("Páginas geradas.")

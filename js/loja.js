/*
 * Lógica da loja: carrinho, vitrine, catálogo com filtros, página de produto
 * e página do carrinho. Todo conteúdo dinâmico é criado com textContent,
 * nunca com innerHTML, para evitar injeção de código (XSS).
 */
(function () {
  "use strict";

  var BE = (window.BE = window.BE || {});
  var CHAVE_CARRINHO = "be_carrinho";
  var FRETE_GRATIS_A_PARTIR = 199;
  var VALOR_FRETE = 19.9;
  var MAX_POR_ITEM = 10;

  /* ---------- Utilidades ---------- */
  var moeda = new Intl.NumberFormat("pt-BR", { style: "currency", currency: "BRL" });
  BE.formatarPreco = function (valor) { return moeda.format(valor); };

  BE.el = function (tag, atributos, filhos) {
    var no = document.createElement(tag);
    Object.keys(atributos || {}).forEach(function (chave) {
      var valor = atributos[chave];
      if (valor === null || valor === undefined || valor === false) { return; }
      if (chave === "texto") { no.textContent = valor; }
      else if (chave === "classe") { no.className = valor; }
      else { no.setAttribute(chave, valor === true ? "" : valor); }
    });
    [].concat(filhos || []).forEach(function (f) {
      if (f === null || f === undefined) { return; }
      no.appendChild(typeof f === "string" ? document.createTextNode(f) : f);
    });
    return no;
  };
  var el = BE.el;

  function oculto(texto) { return el("span", { classe: "visualmente-oculto", texto: texto }); }

  function semAcento(texto) {
    return String(texto).normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase();
  }

  function plural(n, singular, pluralTexto) { return n + " " + (n === 1 ? singular : pluralTexto); }

  /* ---------- Carrinho (localStorage) ---------- */
  BE.lerCarrinho = function () {
    try {
      var itens = JSON.parse(window.localStorage.getItem(CHAVE_CARRINHO) || "[]");
      if (!Array.isArray(itens)) { return []; }
      return itens.filter(function (i) {
        return i && BE.buscarProduto(i.id) && Number.isInteger(i.qtd) && i.qtd > 0;
      }).map(function (i) { return { id: i.id, qtd: Math.min(i.qtd, MAX_POR_ITEM) }; });
    } catch (e) { return []; }
  };

  BE.salvarCarrinho = function (itens) {
    try { window.localStorage.setItem(CHAVE_CARRINHO, JSON.stringify(itens)); } catch (e) { /* sem armazenamento */ }
    BE.atualizarContador();
  };

  BE.totalItens = function () {
    return BE.lerCarrinho().reduce(function (s, i) { return s + i.qtd; }, 0);
  };

  BE.calcularTotais = function () {
    var subtotal = BE.lerCarrinho().reduce(function (s, i) {
      return s + BE.buscarProduto(i.id).preco * i.qtd;
    }, 0);
    var frete = subtotal === 0 || subtotal >= FRETE_GRATIS_A_PARTIR ? 0 : VALOR_FRETE;
    return { subtotal: subtotal, frete: frete, total: subtotal + frete, faltaFreteGratis: Math.max(0, FRETE_GRATIS_A_PARTIR - subtotal) };
  };

  BE.atualizarContador = function () {
    var n = BE.totalItens();
    document.querySelectorAll(".contador-carrinho").forEach(function (c) { c.textContent = String(n); });
    document.querySelectorAll(".rotulo-itens").forEach(function (c) { c.textContent = n === 1 ? " item" : " itens"; });
  };

  BE.adicionarAoCarrinho = function (id, qtd) {
    var produto = BE.buscarProduto(id);
    if (!produto) { return; }
    qtd = Math.max(1, Math.min(MAX_POR_ITEM, parseInt(qtd, 10) || 1));
    var itens = BE.lerCarrinho();
    var item = itens.find(function (i) { return i.id === id; });
    var limitado = false;
    if (item) {
      var novo = item.qtd + qtd;
      if (novo > MAX_POR_ITEM) { novo = MAX_POR_ITEM; limitado = true; }
      item.qtd = novo;
    } else {
      itens.push({ id: id, qtd: qtd });
    }
    BE.salvarCarrinho(itens);
    var total = BE.totalItens();
    BE.anunciar(
      produto.nome + " adicionado ao carrinho. " +
      (limitado ? "O limite é de " + MAX_POR_ITEM + " unidades por produto. " : "") +
      "Agora há " + plural(total, "item", "itens") + " no carrinho."
    );
  };

  /* ---------- Componentes ---------- */
  function blocoPreco(p) {
    var bloco = el("p", { classe: "preco" });
    if (p.precoAntigo) {
      bloco.appendChild(oculto("Preço anterior: "));
      bloco.appendChild(el("s", { texto: BE.formatarPreco(p.precoAntigo) }));
      bloco.appendChild(oculto(". Preço atual: "));
    } else {
      bloco.appendChild(oculto("Preço: "));
    }
    bloco.appendChild(document.createTextNode(BE.formatarPreco(p.preco)));
    if (p.precoAntigo) {
      var pct = Math.round((1 - p.preco / p.precoAntigo) * 100);
      bloco.appendChild(el("span", { classe: "economia", texto: "Economize " + pct + "%" }));
    }
    return bloco;
  }

  function listaSelos(p) {
    var lista = el("ul", { classe: "selos", "aria-label": "Características" });
    if (p.braille) { lista.appendChild(el("li", { classe: "selo-braille", texto: "Braille na embalagem" })); }
    p.selos.forEach(function (s) { lista.appendChild(el("li", { texto: s })); });
    return lista.children.length ? lista : null;
  }

  BE.cartaoProduto = function (p, nivelTitulo) {
    var idTitulo = "titulo-" + p.id;
    var link = el("a", { href: "produto.html?id=" + encodeURIComponent(p.id), texto: p.nome });
    var titulo = el(nivelTitulo || "h2", { id: idTitulo }, link);
    return el("li", null, el("article", { classe: "cartao-produto", "aria-labelledby": idTitulo }, [
      el("img", { classe: "foto-produto", src: p.imagem, alt: p.alt, width: "400", height: "400", loading: "lazy" }),
      el("div", { classe: "cartao-corpo" }, [
        el("p", { classe: "etiqueta-categoria", texto: BE.categorias[p.categoria] }),
        titulo,
        el("p", { classe: "resumo", texto: p.resumo }),
        listaSelos(p),
        blocoPreco(p),
        el("button", { type: "button", classe: "botao", "data-adicionar": p.id }, [
          "Adicionar ao carrinho", oculto(": " + p.nome)
        ])
      ])
    ]));
  };

  /* Campo de quantidade com botões de menos e mais. */
  BE.controleQuantidade = function (opcoes) {
    var entrada = el("input", {
      type: "number", id: opcoes.id, name: opcoes.id, inputmode: "numeric",
      min: "1", max: String(MAX_POR_ITEM), value: String(opcoes.valor || 1),
      "aria-describedby": opcoes.id + "-dica"
    });
    function aplicar(novo) {
      novo = Math.max(1, Math.min(MAX_POR_ITEM, parseInt(novo, 10) || 1));
      entrada.value = String(novo);
      if (opcoes.aoMudar) { opcoes.aoMudar(novo); }
    }
    var menos = el("button", { type: "button", "aria-label": "Diminuir quantidade de " + opcoes.nome, texto: "−" });
    var mais = el("button", { type: "button", "aria-label": "Aumentar quantidade de " + opcoes.nome, texto: "+" });
    menos.addEventListener("click", function () {
      if (parseInt(entrada.value, 10) <= 1) { BE.anunciar("A quantidade mínima é 1."); return; }
      aplicar(parseInt(entrada.value, 10) - 1);
    });
    mais.addEventListener("click", function () {
      if (parseInt(entrada.value, 10) >= MAX_POR_ITEM) { BE.anunciar("A quantidade máxima é " + MAX_POR_ITEM + "."); return; }
      aplicar(parseInt(entrada.value, 10) + 1);
    });
    entrada.addEventListener("change", function () { aplicar(entrada.value); });
    return el("div", { classe: "quantidade" }, [
      el("label", { for: opcoes.id, classe: "rotulo", texto: opcoes.rotulo || "Quantidade" }),
      el("div", { classe: "quantidade-controles" }, [menos, entrada, mais]),
      el("span", { id: opcoes.id + "-dica", classe: "visualmente-oculto", texto: "De 1 a " + MAX_POR_ITEM + " unidades." })
    ]);
  };

  /* ---------- Página inicial ---------- */
  function iniciarInicio() {
    var lista = document.getElementById("lista-destaques");
    if (!lista) { return; }
    ["serum-vitamina-c", "perfume-flor-de-laranjeira", "batom-cremoso-rose", "shampoo-reconstrucao"].forEach(function (id) {
      lista.appendChild(BE.cartaoProduto(BE.buscarProduto(id), "h3"));
    });
  }

  /* ---------- Catálogo ---------- */
  function iniciarCatalogo() {
    var form = document.getElementById("form-filtros");
    if (!form) { return; }
    var params = new URLSearchParams(window.location.search);
    var campoBusca = document.getElementById("filtro-busca");
    var campoCategoria = document.getElementById("filtro-categoria");
    var campoOrdem = document.getElementById("filtro-ordem");
    var campoVegano = document.getElementById("filtro-vegano");
    var campoBraille = document.getElementById("filtro-braille");
    var lista = document.getElementById("lista-produtos");
    var contagem = document.getElementById("contagem-produtos");

    campoBusca.value = (params.get("busca") || "").slice(0, 60);
    if (BE.categorias[params.get("categoria")]) { campoCategoria.value = params.get("categoria"); }

    function filtrar(anunciar) {
      var termo = semAcento(campoBusca.value.trim());
      var cat = campoCategoria.value;
      var resultado = BE.produtos.filter(function (p) {
        if (cat && p.categoria !== cat) { return false; }
        if (campoVegano.checked && p.selos.indexOf("Vegano") === -1) { return false; }
        if (campoBraille.checked && !p.braille) { return false; }
        if (!termo) { return true; }
        return semAcento([p.nome, p.resumo, p.descricao, BE.categorias[p.categoria]].join(" ")).indexOf(termo) !== -1;
      });
      var ordem = campoOrdem.value;
      resultado.sort(function (a, b) {
        if (ordem === "menor-preco") { return a.preco - b.preco; }
        if (ordem === "maior-preco") { return b.preco - a.preco; }
        if (ordem === "nome") { return a.nome.localeCompare(b.nome, "pt-BR"); }
        return 0;
      });

      lista.textContent = "";
      resultado.forEach(function (p) { lista.appendChild(BE.cartaoProduto(p, "h2")); });

      var texto = resultado.length
        ? plural(resultado.length, "produto encontrado", "produtos encontrados") + "."
        : "Nenhum produto encontrado. Tente outra palavra ou limpe os filtros.";
      contagem.textContent = texto;
      if (anunciar) { BE.anunciar(texto); }

      var titulo = cat ? BE.categorias[cat] : "Todos os produtos";
      document.title = titulo + " | Bela Essência Cosméticos";
      var novosParams = new URLSearchParams();
      if (campoBusca.value.trim()) { novosParams.set("busca", campoBusca.value.trim()); }
      if (cat) { novosParams.set("categoria", cat); }
      var qs = novosParams.toString();
      try { window.history.replaceState(null, "", "produtos.html" + (qs ? "?" + qs : "")); } catch (e) { /* ignora */ }
    }

    form.addEventListener("submit", function (e) { e.preventDefault(); filtrar(true); });
    [campoCategoria, campoOrdem, campoVegano, campoBraille].forEach(function (c) {
      c.addEventListener("change", function () { filtrar(true); });
    });
    document.getElementById("limpar-filtros").addEventListener("click", function () {
      form.reset();
      filtrar(true);
      campoBusca.focus();
    });
    filtrar(Boolean(params.get("busca") || params.get("categoria")));
  }

  /* ---------- Página de produto ---------- */
  function iniciarProduto() {
    var area = document.getElementById("detalhe-produto");
    if (!area) { return; }
    var id = new URLSearchParams(window.location.search).get("id");
    var p = BE.buscarProduto(id);
    var trilhaAtual = document.getElementById("trilha-atual");

    if (!p) {
      document.title = "Produto não encontrado | Bela Essência Cosméticos";
      if (trilhaAtual) { trilhaAtual.textContent = "Produto não encontrado"; }
      area.textContent = "";
      area.appendChild(el("h1", { tabindex: "-1", texto: "Produto não encontrado" }));
      area.appendChild(el("p", { texto: "Não encontramos o produto que você procura. Ele pode ter saído de linha ou o endereço pode estar incorreto." }));
      area.appendChild(el("p", null, el("a", { classe: "botao", href: "produtos.html", texto: "Ver todos os produtos" })));
      return;
    }

    document.title = p.nome + " | Bela Essência Cosméticos";
    var meta = document.querySelector("meta[name='description']");
    if (meta) { meta.setAttribute("content", p.resumo); }
    if (trilhaAtual) { trilhaAtual.textContent = p.nome; }
    var linkCat = document.getElementById("trilha-categoria");
    if (linkCat) {
      linkCat.textContent = BE.categorias[p.categoria];
      linkCat.setAttribute("href", "produtos.html?categoria=" + p.categoria);
    }

    var qtdEscolhida = 1;
    var ficha = el("dl", { classe: "ficha", id: "ficha-produto" }, [
      el("dt", { texto: "Descrição" }), el("dd", { texto: p.descricao }),
      p.cor ? el("dt", { texto: "Cor" }) : null, p.cor ? el("dd", { texto: p.cor }) : null,
      el("dt", { texto: "Conteúdo" }), el("dd", { texto: p.volume }),
      el("dt", { texto: "Como reconhecer a embalagem pelo toque" }), el("dd", { texto: p.embalagem }),
      el("dt", { texto: "Identificação em Braille" }),
      el("dd", { texto: p.braille ? "Sim. O nome do produto está escrito em Braille na embalagem." : "Não. Para identificar, use a descrição de toque acima ou peça a etiqueta em Braille gratuita no fechamento do pedido." }),
      el("dt", { texto: "Como usar" }), el("dd", { texto: p.comoUsar })
    ]);

    area.textContent = "";
    area.appendChild(el("div", { classe: "produto-detalhe" }, [
      el("div", null, el("img", { classe: "foto-produto", src: p.imagem, alt: p.alt, width: "400", height: "400" })),
      el("div", { classe: "produto-info" }, [
        el("p", { classe: "etiqueta-categoria", texto: BE.categorias[p.categoria] }),
        el("h1", { tabindex: "-1", texto: p.nome }),
        el("p", { texto: p.resumo }),
        listaSelos(p),
        blocoPreco(p),
        el("div", { classe: "comprar" }, [
          BE.controleQuantidade({ id: "quantidade-produto", nome: p.nome, valor: 1, aoMudar: function (n) { qtdEscolhida = n; } }),
          (function () {
            var b = el("button", { type: "button", classe: "botao" }, ["Adicionar ao carrinho", oculto(": " + p.nome)]);
            b.addEventListener("click", function () { BE.adicionarAoCarrinho(p.id, qtdEscolhida); });
            return b;
          })()
        ]),
        el("div", { classe: "controles-voz" }, [
          el("button", { type: "button", classe: "botao botao-secundario botao-pequeno", "data-acao": "ouvir-alvo", "data-alvo": "ficha-produto", texto: "Ouvir a descrição do produto" }),
          el("button", { type: "button", classe: "botao botao-secundario botao-pequeno", "data-acao": "parar", texto: "Parar leitura" })
        ]),
        el("h2", { texto: "Detalhes do produto" }),
        ficha
      ])
    ]));

    var relacionados = BE.produtos.filter(function (r) { return r.categoria === p.categoria && r.id !== p.id; }).slice(0, 3);
    if (relacionados.length) {
      var listaRel = el("ul", { classe: "grade-produtos" });
      relacionados.forEach(function (r) { listaRel.appendChild(BE.cartaoProduto(r, "h3")); });
      area.appendChild(el("section", { "aria-labelledby": "titulo-relacionados" }, [
        el("h2", { id: "titulo-relacionados", texto: "Outros produtos de " + BE.categorias[p.categoria].toLowerCase() }),
        listaRel
      ]));
    }
  }

  /* ---------- Página do carrinho ---------- */
  function preencherResumo(destino) {
    var t = BE.calcularTotais();
    destino.textContent = "";
    destino.appendChild(el("dt", { texto: "Subtotal" }));
    destino.appendChild(el("dd", { texto: BE.formatarPreco(t.subtotal) }));
    destino.appendChild(el("dt", { texto: "Frete" }));
    destino.appendChild(el("dd", { texto: t.frete === 0 ? "Grátis" : BE.formatarPreco(t.frete) }));
    destino.appendChild(el("dt", { classe: "total", texto: "Total" }));
    destino.appendChild(el("dd", { classe: "total", texto: BE.formatarPreco(t.total) }));
    return t;
  }
  BE.preencherResumo = preencherResumo;

  function iniciarCarrinho() {
    var area = document.getElementById("area-carrinho");
    if (!area) { return; }
    var titulo = document.querySelector("main h1");

    function desenhar() {
      var itens = BE.lerCarrinho();
      area.textContent = "";
      if (!itens.length) {
        area.appendChild(el("div", { classe: "estado-vazio" }, [
          el("p", { texto: "Seu carrinho está vazio." }),
          el("a", { classe: "botao", href: "produtos.html", texto: "Conhecer os produtos" })
        ]));
        return;
      }
      area.appendChild(el("p", { id: "quantidade-itens", texto: "Você tem " + plural(BE.totalItens(), "item", "itens") + " no carrinho." }));
      var lista = el("ul", { classe: "itens-carrinho" });
      itens.forEach(function (item) {
        var p = BE.buscarProduto(item.id);
        var subtotal = el("p", { texto: "Subtotal: " + BE.formatarPreco(p.preco * item.qtd) });
        var remover = el("button", { type: "button", classe: "botao botao-perigo botao-pequeno" }, ["Remover", oculto(" " + p.nome + " do carrinho")]);
        remover.addEventListener("click", function () {
          BE.salvarCarrinho(BE.lerCarrinho().filter(function (i) { return i.id !== p.id; }));
          desenhar();
          BE.anunciar(p.nome + " removido do carrinho.");
          titulo.focus();
        });
        lista.appendChild(el("li", { classe: "item-carrinho" }, [
          el("img", { src: p.imagem, alt: "", width: "96", height: "96" }),
          el("div", null, [
            el("h2", null, el("a", { href: "produto.html?id=" + encodeURIComponent(p.id), texto: p.nome })),
            el("p", { texto: "Preço unitário: " + BE.formatarPreco(p.preco) }),
            subtotal
          ]),
          el("div", { classe: "acoes-item" }, [
            BE.controleQuantidade({
              id: "qtd-" + p.id, nome: p.nome, valor: item.qtd,
              aoMudar: function (n) {
                var todos = BE.lerCarrinho();
                var alvo = todos.find(function (i) { return i.id === p.id; });
                if (alvo) { alvo.qtd = n; }
                BE.salvarCarrinho(todos);
                subtotal.textContent = "Subtotal: " + BE.formatarPreco(p.preco * n);
                var t = atualizarTotais();
                document.getElementById("quantidade-itens").textContent = "Você tem " + plural(BE.totalItens(), "item", "itens") + " no carrinho.";
                BE.anunciar("Quantidade de " + p.nome + ": " + n + ". Total do pedido: " + BE.formatarPreco(t.total) + ".");
              }
            }),
            remover
          ])
        ]));
      });
      area.appendChild(lista);

      var dl = el("dl", { id: "valores-resumo" });
      var avisoFrete = el("p", { id: "aviso-frete" });
      area.appendChild(el("section", { classe: "resumo-pedido", "aria-labelledby": "titulo-resumo" }, [
        el("h2", { id: "titulo-resumo", texto: "Resumo do pedido" }),
        dl, avisoFrete,
        el("div", { classe: "comprar" }, [
          el("a", { classe: "botao", href: "finalizar.html", texto: "Finalizar compra" }),
          el("a", { classe: "botao botao-secundario", href: "produtos.html", texto: "Continuar comprando" })
        ])
      ]));
      var esvaziar = el("button", { type: "button", classe: "botao botao-perigo botao-pequeno", texto: "Esvaziar carrinho" });
      esvaziar.addEventListener("click", function () {
        if (window.confirm("Deseja mesmo remover todos os produtos do carrinho?")) {
          BE.salvarCarrinho([]);
          desenhar();
          BE.anunciar("Carrinho esvaziado.");
          titulo.focus();
        }
      });
      area.appendChild(el("p", null, esvaziar));
      atualizarTotais();
    }

    function atualizarTotais() {
      var t = preencherResumo(document.getElementById("valores-resumo"));
      document.getElementById("aviso-frete").textContent = t.faltaFreteGratis > 0
        ? "Faltam " + BE.formatarPreco(t.faltaFreteGratis) + " para você ganhar frete grátis."
        : "Parabéns, seu pedido tem frete grátis.";
      return t;
    }

    desenhar();
  }

  /* ---------- Ligações gerais ---------- */
  document.addEventListener("click", function (e) {
    var botao = e.target.closest("[data-adicionar]");
    if (botao) { BE.adicionarAoCarrinho(botao.getAttribute("data-adicionar"), 1); }
  });

  /* Sincroniza o contador se o carrinho mudar em outra aba. */
  window.addEventListener("storage", function (e) { if (e.key === CHAVE_CARRINHO) { BE.atualizarContador(); } });

  document.addEventListener("DOMContentLoaded", function () {
    BE.atualizarContador();
    var pagina = document.body.getAttribute("data-pagina");
    if (pagina === "inicio") { iniciarInicio(); }
    if (pagina === "produtos") { iniciarCatalogo(); }
    if (pagina === "produto") { iniciarProduto(); }
    if (pagina === "carrinho") { iniciarCarrinho(); }
  });
})();

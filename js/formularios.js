/*
 * Formulários acessíveis: validação com mensagens em texto, resumo de erros
 * com links para cada campo, foco levado ao resumo e consulta de CEP.
 * Nenhum dado sai do navegador, exceto o CEP enviado ao ViaCEP.
 */
(function () {
  "use strict";

  var BE = (window.BE = window.BE || {});
  var el = function () { return BE.el.apply(null, arguments); };

  /* ---------- Regras de validação ---------- */
  var REGRAS = {
    obrigatorio: function (v, rotulo) { return v.trim() ? "" : "Preencha o campo " + rotulo + "."; },
    nome: function (v) {
      v = v.trim();
      if (!v) { return "Preencha o seu nome."; }
      if (v.length < 3) { return "O nome precisa ter pelo menos 3 letras."; }
      if (!/^[A-Za-zÀ-ÖØ-öø-ÿ' .-]+$/.test(v)) { return "O nome deve ter apenas letras e espaços."; }
      return "";
    },
    email: function (v) {
      v = v.trim();
      if (!v) { return "Preencha o seu e-mail."; }
      return /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v) ? "" : "O e-mail parece incompleto. Exemplo correto: maria@email.com.";
    },
    telefone: function (v) {
      var d = v.replace(/\D/g, "");
      if (!d) { return "Preencha o telefone com DDD."; }
      return d.length === 10 || d.length === 11 ? "" : "O telefone precisa ter DDD e número, com 10 ou 11 dígitos. Exemplo: 41 99999 8888.";
    },
    telefoneOpcional: function (v) {
      var d = v.replace(/\D/g, "");
      if (!d) { return ""; }
      return d.length === 10 || d.length === 11 ? "" : "O telefone precisa ter DDD e número, com 10 ou 11 dígitos.";
    },
    cep: function (v) {
      var d = v.replace(/\D/g, "");
      if (!d) { return "Preencha o CEP."; }
      return d.length === 8 ? "" : "O CEP precisa ter 8 números. Exemplo: 80010 000.";
    },
    mensagem: function (v) {
      v = v.trim();
      if (!v) { return "Escreva a sua mensagem."; }
      return v.length >= 10 ? "" : "A mensagem precisa ter pelo menos 10 caracteres.";
    },
    selecao: function (v, rotulo) { return v ? "" : "Escolha uma opção em " + rotulo + "."; }
  };

  /* ---------- Funções de apoio ---------- */
  function rotuloDo(campo) {
    var rot = document.querySelector("label[for='" + campo.id + "']");
    if (rot) { return rot.getAttribute("data-nome") || rot.textContent.replace("*", "").replace("(obrigatório)", "").trim().toLowerCase(); }
    return campo.getAttribute("data-nome") || campo.name;
  }

  function definirErro(campo, mensagem) {
    var idErro = "erro-" + (campo.getAttribute("data-grupo") || campo.id);
    var caixa = document.getElementById(idErro);
    var dica = campo.getAttribute("data-dica");
    var descritores = [];
    if (dica) { descritores.push(dica); }
    var alvos = campo.getAttribute("data-grupo")
      ? document.querySelectorAll("input[name='" + campo.name + "']")
      : [campo];
    if (mensagem) {
      caixa.textContent = mensagem;
      caixa.hidden = false;
      descritores.push(idErro);
    } else if (caixa) {
      caixa.textContent = "";
      caixa.hidden = true;
    }
    Array.prototype.forEach.call(alvos, function (a) {
      if (mensagem) { a.setAttribute("aria-invalid", "true"); } else { a.removeAttribute("aria-invalid"); }
      if (descritores.length) { a.setAttribute("aria-describedby", descritores.join(" ")); }
      else { a.removeAttribute("aria-describedby"); }
    });
  }

  function validarCampo(campo) {
    var regra = campo.getAttribute("data-regra");
    var mensagem = "";
    if (campo.type === "checkbox") {
      mensagem = campo.checked ? "" : campo.getAttribute("data-mensagem");
    } else if (campo.type === "radio") {
      var marcado = document.querySelector("input[name='" + campo.name + "']:checked");
      mensagem = marcado ? "" : campo.getAttribute("data-mensagem");
    } else if (regra && REGRAS[regra]) {
      mensagem = REGRAS[regra](campo.value, rotuloDo(campo));
    }
    definirErro(campo, mensagem);
    return mensagem;
  }

  function validarFormulario(form) {
    var erros = [];
    var gruposVistos = {};
    form.querySelectorAll("[data-regra], [data-mensagem]").forEach(function (campo) {
      if (campo.type === "radio") {
        if (gruposVistos[campo.name]) { return; }
        gruposVistos[campo.name] = true;
      }
      var msg = validarCampo(campo);
      if (msg) { erros.push({ campo: campo, mensagem: msg }); }
    });
    mostrarResumo(form, erros);
    return erros.length === 0;
  }

  function mostrarResumo(form, erros) {
    var caixa = form.querySelector(".resumo-erros");
    if (!caixa) { return; }
    caixa.textContent = "";
    if (!erros.length) { caixa.hidden = true; return; }
    var lista = el("ul");
    erros.forEach(function (e) {
      var link = el("a", { href: "#" + e.campo.id, texto: e.mensagem });
      link.addEventListener("click", function (ev) {
        ev.preventDefault();
        e.campo.focus();
      });
      lista.appendChild(el("li", null, link));
    });
    caixa.appendChild(el("h2", { id: form.id + "-titulo-erros", texto: erros.length === 1 ? "Encontramos 1 problema no formulário" : "Encontramos " + erros.length + " problemas no formulário" }));
    caixa.appendChild(el("p", { texto: "Corrija os itens abaixo e envie de novo. Cada item leva você até o campo." }));
    caixa.appendChild(lista);
    caixa.hidden = false;
    caixa.focus();
  }

  /* Revalida enquanto a pessoa corrige, mas só depois da primeira tentativa de envio. */
  function ligarRevalidacao(form) {
    form.addEventListener("change", function (e) {
      if (form.getAttribute("data-tentou") && (e.target.hasAttribute("data-regra") || e.target.hasAttribute("data-mensagem"))) {
        validarCampo(e.target);
      }
    });
    form.addEventListener("blur", function (e) {
      if (form.getAttribute("data-tentou") && e.target.hasAttribute("data-regra")) { validarCampo(e.target); }
    }, true);
  }

  /* Formatação leve, aplicada só ao sair do campo, para não atrapalhar quem digita com leitor de tela. */
  function formatarAoSair(form) {
    form.addEventListener("blur", function (e) {
      var c = e.target;
      var d = (c.value || "").replace(/\D/g, "");
      if (c.getAttribute("data-formato") === "cep" && d.length === 8) { c.value = d.slice(0, 5) + "-" + d.slice(5); }
      if (c.getAttribute("data-formato") === "telefone" && (d.length === 10 || d.length === 11)) {
        c.value = "(" + d.slice(0, 2) + ") " + d.slice(2, d.length - 4) + "-" + d.slice(-4);
      }
    }, true);
  }

  /* ---------- Contador de caracteres ---------- */
  function ligarContador(campo, saida) {
    var limite = parseInt(campo.getAttribute("maxlength"), 10);
    function atualizar() {
      var resta = limite - campo.value.length;
      saida.textContent = resta + " caracteres restantes.";
    }
    campo.addEventListener("input", atualizar);
    atualizar();
  }

  /* ---------- Consulta de CEP (ViaCEP) ---------- */
  function ligarCep() {
    var botao = document.getElementById("buscar-cep");
    if (!botao) { return; }
    botao.addEventListener("click", function () {
      var campo = document.getElementById("cep");
      var cep = campo.value.replace(/\D/g, "");
      if (cep.length !== 8) {
        definirErro(campo, REGRAS.cep(campo.value));
        campo.focus();
        return;
      }
      definirErro(campo, "");
      botao.disabled = true;
      BE.anunciar("Buscando endereço, aguarde.");
      fetch("https://viacep.com.br/ws/" + cep + "/json/", { headers: { Accept: "application/json" } })
        .then(function (r) { if (!r.ok) { throw new Error("falha"); } return r.json(); })
        .then(function (dados) {
          if (dados.erro) { throw new Error("cep inexistente"); }
          var mapa = { logradouro: "endereco", bairro: "bairro", localidade: "cidade", uf: "uf" };
          Object.keys(mapa).forEach(function (k) {
            var alvo = document.getElementById(mapa[k]);
            if (alvo && typeof dados[k] === "string" && dados[k]) { alvo.value = dados[k].slice(0, 120); }
          });
          BE.anunciar("Endereço encontrado: " + [dados.logradouro, dados.bairro, dados.localidade, dados.uf].filter(Boolean).join(", ") + ". Confira os dados e informe o número.");
          document.getElementById("numero").focus();
        })
        .catch(function () {
          BE.anunciar("Não encontramos esse CEP. Confira os números ou preencha o endereço manualmente.", true);
        })
        .finally(function () { botao.disabled = false; });
    });
  }

  /* ---------- Finalizar compra ---------- */
  var FORMAS_PAGAMENTO = {
    pix: "Pix. Na loja real, o código Pix apareceria aqui para copiar com um toque.",
    boleto: "Boleto bancário. Na loja real, o boleto seria enviado para o seu e-mail.",
    entrega: "Pagamento na entrega, com cartão ou dinheiro."
  };

  function iniciarCheckout() {
    var form = document.getElementById("form-checkout");
    if (!form) { return; }
    var areaForm = document.getElementById("area-checkout");
    var vazio = document.getElementById("checkout-vazio");

    function desenharResumo() {
      var lista = document.getElementById("itens-resumo");
      lista.textContent = "";
      BE.lerCarrinho().forEach(function (i) {
        var p = BE.buscarProduto(i.id);
        lista.appendChild(el("li", null, [
          el("span", { texto: i.qtd + " × " + p.nome }),
          el("span", { texto: BE.formatarPreco(p.preco * i.qtd) })
        ]));
      });
      BE.preencherResumo(document.getElementById("valores-checkout"));
    }

    if (!BE.lerCarrinho().length) {
      areaForm.hidden = true;
      vazio.hidden = false;
      return;
    }
    desenharResumo();
    ligarRevalidacao(form);
    formatarAoSair(form);
    ligarCep();
    var obs = document.getElementById("observacoes");
    if (obs) { ligarContador(obs, document.getElementById("contador-observacoes")); }

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      form.setAttribute("data-tentou", "sim");
      if (!validarFormulario(form)) { return; }

      var totais = BE.calcularTotais();
      var numero = "BE" + Date.now().toString().slice(-8);
      var pagamento = form.querySelector("input[name='pagamento']:checked").value;
      var nome = document.getElementById("nome").value.trim().split(" ")[0];
      var braille = document.getElementById("etiqueta-braille").checked;

      var conf = document.getElementById("confirmacao");
      conf.textContent = "";
      conf.appendChild(el("h2", { tabindex: "-1", id: "titulo-confirmacao", texto: "Pedido recebido, " + nome + "!" }));
      conf.appendChild(el("p", { texto: "O número do seu pedido é " + numero + "." }));
      conf.appendChild(el("p", { texto: "Total: " + BE.formatarPreco(totais.total) + ". Forma de pagamento: " + FORMAS_PAGAMENTO[pagamento] }));
      if (braille) { conf.appendChild(el("p", { texto: "Os produtos sem Braille vão com etiqueta em Braille colada na embalagem, sem custo." })); }
      conf.appendChild(el("p", { texto: "Esta é uma loja de demonstração. Nenhum pagamento foi cobrado e nenhum dado foi enviado." }));
      conf.appendChild(el("p", null, el("a", { classe: "botao", href: "index.html", texto: "Voltar para a página inicial" })));

      BE.salvarCarrinho([]);
      areaForm.hidden = true;
      conf.hidden = false;
      document.title = "Pedido recebido | Bela Essência Cosméticos";
      document.getElementById("titulo-confirmacao").focus();
    });
  }

  /* ---------- Contato ---------- */
  function iniciarContato() {
    var form = document.getElementById("form-contato");
    if (!form) { return; }
    ligarRevalidacao(form);
    formatarAoSair(form);
    ligarContador(document.getElementById("mensagem"), document.getElementById("contador-mensagem"));

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      form.setAttribute("data-tentou", "sim");
      if (!validarFormulario(form)) { return; }
      var nome = document.getElementById("contato-nome").value.trim().split(" ")[0];
      var aviso = document.getElementById("contato-sucesso");
      aviso.textContent = "";
      aviso.appendChild(el("h2", { tabindex: "-1", id: "titulo-sucesso", texto: "Mensagem enviada, " + nome + "!" }));
      aviso.appendChild(el("p", { texto: "Obrigada pelo contato. Responderemos em até dois dias úteis pelo meio que você escolheu." }));
      aviso.appendChild(el("p", { texto: "Esta é uma loja de demonstração, então a mensagem não foi realmente enviada." }));
      aviso.hidden = false;
      form.reset();
      form.removeAttribute("data-tentou");
      document.getElementById("contador-mensagem").textContent = "1000 caracteres restantes.";
      document.getElementById("titulo-sucesso").focus();
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    iniciarCheckout();
    iniciarContato();
  });
})();

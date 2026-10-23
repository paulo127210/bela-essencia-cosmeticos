/*
 * Recursos de acessibilidade da Bela Essência:
 *  - avisos para leitores de tela (regiões aria-live)
 *  - painel de recursos (letra, tema, cores, espaçamento, fonte)
 *  - atalhos de teclado no padrão eMAG (Alt+1 a Alt+4)
 *  - leitura em voz alta com a Web Speech API
 */
(function () {
  "use strict";

  var BE = (window.BE = window.BE || {});
  var raiz = document.documentElement;
  var CHAVE = "be_preferencias";
  var TAMANHOS = ["100", "125", "150", "175", "200"];

  /* ---------- Armazenamento seguro ---------- */
  function lerPrefs() {
    try { return JSON.parse(window.localStorage.getItem(CHAVE) || "{}") || {}; }
    catch (e) { return {}; }
  }
  function salvarPrefs(p) {
    try { window.localStorage.setItem(CHAVE, JSON.stringify(p)); } catch (e) { /* navegação privada: segue sem salvar */ }
  }
  function definir(chave, valor) {
    var p = lerPrefs();
    if (valor) { p[chave] = valor; raiz.setAttribute("data-" + chave, valor); }
    else { delete p[chave]; raiz.removeAttribute("data-" + chave); }
    if (chave === "tema") { p.temaEscolhido = true; }
    salvarPrefs(p);
  }

  /* ---------- Avisos para leitores de tela ---------- */
  var limpeza = {};
  BE.anunciar = function (mensagem, urgente) {
    var id = urgente ? "aviso-urgente" : "aviso-educado";
    var regiao = document.getElementById(id);
    if (!regiao) { return; }
    regiao.textContent = "";
    /* Pequeno atraso garante que o leitor perceba a mudança mesmo com texto repetido. */
    window.setTimeout(function () { regiao.textContent = mensagem; }, 60);
    window.clearTimeout(limpeza[id]);
    limpeza[id] = window.setTimeout(function () { regiao.textContent = ""; }, 8000);
  };

  /* ---------- Tamanho da letra ---------- */
  function tamanhoAtual() { return raiz.getAttribute("data-fonte") || "100"; }
  function mudarFonte(passo) {
    var i = TAMANHOS.indexOf(tamanhoAtual()) + passo;
    if (passo === 0) { i = 0; }
    if (i < 0 || i >= TAMANHOS.length) {
      BE.anunciar(i < 0 ? "A letra já está no tamanho mínimo." : "A letra já está no tamanho máximo, 200%.");
      return;
    }
    definir("fonte", TAMANHOS[i] === "100" ? "" : TAMANHOS[i]);
    atualizarEstados();
    BE.anunciar("Tamanho da letra: " + TAMANHOS[i] + "%.");
  }

  /* ---------- Sincroniza botões e campos com o estado atual ---------- */
  function atualizarEstados() {
    var tema = raiz.getAttribute("data-tema") || "claro";
    document.querySelectorAll("[data-acao='contraste']").forEach(function (b) {
      b.setAttribute("aria-pressed", tema === "contraste" ? "true" : "false");
    });
    document.querySelectorAll("input[name='tema']").forEach(function (r) { r.checked = r.value === tema; });
    var espac = document.getElementById("opcao-espacamento");
    if (espac) { espac.checked = raiz.getAttribute("data-espacamento") === "sim"; }
    var disl = document.getElementById("opcao-dislexia");
    if (disl) { disl.checked = raiz.getAttribute("data-dislexia") === "sim"; }
    var dalt = document.getElementById("opcao-daltonismo");
    if (dalt) { dalt.value = raiz.getAttribute("data-daltonismo") || ""; }
    document.querySelectorAll(".estado-fonte").forEach(function (el) { el.textContent = tamanhoAtual() + "%"; });
    var lendo = raiz.getAttribute("data-leitura") === "sim";
    document.querySelectorAll("[data-acao='leitura']").forEach(function (b) { b.setAttribute("aria-pressed", lendo ? "true" : "false"); });
    var opLeitura = document.getElementById("opcao-leitura");
    if (opLeitura) { opLeitura.checked = lendo; }
  }

  /* ---------- Atalhos de teclado (eMAG) ---------- */
  var ALVOS = { Digit1: "conteudo", Digit2: "menu-principal", Digit3: "campo-busca", Digit4: "rodape" };
  function irPara(id) {
    var alvo = document.getElementById(id);
    if (!alvo) { return; }
    if (!alvo.matches("a, button, input, select, textarea") && !alvo.hasAttribute("tabindex")) {
      alvo.setAttribute("tabindex", "-1");
    }
    alvo.focus();
    alvo.scrollIntoView({ block: "start" });
  }

  document.addEventListener("keydown", function (e) {
    if (e.altKey && !e.ctrlKey && !e.metaKey && ALVOS[e.code]) {
      e.preventDefault();
      irPara(ALVOS[e.code]);
    }
    if (e.key === "Escape") {
      var painel = document.getElementById("painel-acessibilidade");
      var botao = document.getElementById("botao-recursos");
      if (painel && !painel.hidden && painel.contains(document.activeElement)) {
        alternarPainel(false);
        botao.focus();
      }
    }
  });

  /* ---------- Painel de recursos ---------- */
  function alternarPainel(abrir) {
    var painel = document.getElementById("painel-acessibilidade");
    var botao = document.getElementById("botao-recursos");
    if (!painel || !botao) { return; }
    if (typeof abrir !== "boolean") { abrir = painel.hidden; }
    painel.hidden = !abrir;
    botao.setAttribute("aria-expanded", abrir ? "true" : "false");
    if (abrir) {
      var titulo = document.getElementById("titulo-recursos");
      if (titulo) { titulo.focus(); }
    }
  }

  /* ---------- Leitura em voz alta ---------- */
  var voz = {
    suportado: "speechSynthesis" in window && "SpeechSynthesisUtterance" in window,
    fila: [],
    velocidade: 1,
    ativo: false
  };

  function vozPortugues() {
    var vozes = window.speechSynthesis.getVoices();
    return vozes.find(function (v) { return /pt[-_]BR/i.test(v.lang); }) ||
      vozes.find(function (v) { return /^pt/i.test(v.lang); }) || null;
  }

  function dividirTexto(texto) {
    var frases = texto.replace(/\s+/g, " ").match(/[^.!?;:]+[.!?;:]*/g) || [];
    var partes = [];
    var atual = "";
    frases.forEach(function (f) {
      if ((atual + f).length > 220) { if (atual) { partes.push(atual); } atual = f; }
      else { atual += f; }
    });
    if (atual.trim()) { partes.push(atual); }
    return partes;
  }

  function estadoVoz(msg) {
    var el = document.getElementById("estado-voz");
    if (el) { el.textContent = msg; }
  }

  BE.lerEmVozAlta = function (texto) {
    if (!voz.suportado) {
      BE.anunciar("Seu navegador não oferece leitura em voz alta.");
      return;
    }
    window.speechSynthesis.cancel();
    voz.fila = dividirTexto(texto);
    voz.ativo = true;
    var v = vozPortugues();
    voz.fila.forEach(function (trecho, indice) {
      var fala = new window.SpeechSynthesisUtterance(trecho);
      fala.lang = "pt-BR";
      fala.rate = voz.velocidade;
      if (v) { fala.voice = v; }
      if (indice === voz.fila.length - 1) {
        fala.onend = function () { voz.ativo = false; estadoVoz("Leitura concluída."); };
      }
      window.speechSynthesis.speak(fala);
    });
    estadoVoz("Lendo em voz alta.");
  };

  function textoParaLer() {
    var selecao = window.getSelection ? String(window.getSelection()) : "";
    if (selecao.trim().length > 2) { return selecao; }
    var principal = document.getElementById("conteudo");
    return principal ? principal.innerText : document.body.innerText;
  }

  function prepararVoz() {
    var grupo = document.getElementById("grupo-voz");
    if (!grupo) { return; }
    if (!voz.suportado) {
      grupo.querySelectorAll("button, select").forEach(function (c) { c.disabled = true; });
      estadoVoz("Seu navegador não oferece leitura em voz alta. Experimente o Chrome, o Edge ou o Safari.");
      return;
    }
    var vel = document.getElementById("velocidade-voz");
    if (vel) {
      vel.addEventListener("change", function () {
        voz.velocidade = parseFloat(vel.value) || 1;
        estadoVoz("Velocidade ajustada. Vale para a próxima leitura.");
      });
    }
    /* Algumas vozes só ficam disponíveis depois deste evento. */
    window.speechSynthesis.onvoiceschanged = function () { /* nada a fazer: a voz é escolhida na hora de ler */ };
  }

  /* ---------- Ligações dos controles ---------- */
  document.addEventListener("click", function (e) {
    var alvo = e.target.closest("[data-acao]");
    if (!alvo) { return; }
    var acao = alvo.getAttribute("data-acao");
    switch (acao) {
      case "fonte-mais": mudarFonte(1); break;
      case "fonte-menos": mudarFonte(-1); break;
      case "fonte-padrao": mudarFonte(0); break;
      case "contraste":
        definir("tema", raiz.getAttribute("data-tema") === "contraste" ? "" : "contraste");
        atualizarEstados();
        BE.anunciar(raiz.getAttribute("data-tema") === "contraste" ? "Alto contraste ativado." : "Alto contraste desativado.");
        break;
      case "painel": alternarPainel(); break;
      case "fechar-painel": alternarPainel(false); document.getElementById("botao-recursos").focus(); break;
      case "ouvir": BE.lerEmVozAlta(textoParaLer()); break;
      case "ouvir-alvo":
        var origem = document.getElementById(alvo.getAttribute("data-alvo"));
        if (origem) { BE.lerEmVozAlta(origem.innerText); }
        break;
      case "pausar":
        if (!voz.suportado) { break; }
        if (window.speechSynthesis.paused) { window.speechSynthesis.resume(); estadoVoz("Leitura retomada."); alvo.textContent = "Pausar"; }
        else if (window.speechSynthesis.speaking) { window.speechSynthesis.pause(); estadoVoz("Leitura pausada."); alvo.textContent = "Continuar"; }
        break;
      case "parar":
        if (voz.suportado) { window.speechSynthesis.cancel(); }
        voz.ativo = false;
        estadoVoz("Leitura interrompida.");
        break;
      case "leitura":
        alternarLeitura(raiz.getAttribute("data-leitura") !== "sim");
        break;
      case "restaurar":
        try { window.localStorage.removeItem(CHAVE); } catch (err) { /* sem armazenamento */ }
        ["tema", "fonte", "espacamento", "dislexia", "daltonismo", "leitura"].forEach(function (c) { raiz.removeAttribute("data-" + c); });
        salvarPrefs({ temaEscolhido: true });
        atualizarEstados();
        BE.anunciar("Configurações de acessibilidade restauradas para o padrão.");
        break;
    }
  });

  document.addEventListener("change", function (e) {
    var t = e.target;
    if (t.name === "tema") {
      definir("tema", t.value === "claro" ? "" : t.value);
      BE.anunciar("Tema " + t.parentNode.textContent.trim() + " aplicado.");
      atualizarEstados();
    } else if (t.id === "opcao-espacamento") {
      definir("espacamento", t.checked ? "sim" : "");
      BE.anunciar(t.checked ? "Espaçamento ampliado ativado." : "Espaçamento ampliado desativado.");
    } else if (t.id === "opcao-dislexia") {
      definir("dislexia", t.checked ? "sim" : "");
      BE.anunciar(t.checked ? "Fonte de leitura facilitada ativada." : "Fonte padrão restaurada.");
    } else if (t.id === "opcao-leitura") {
      alternarLeitura(t.checked);
    } else if (t.id === "opcao-daltonismo") {
      definir("daltonismo", t.value);
      BE.anunciar(t.value ? "Paleta de cores ajustada." : "Paleta de cores padrão.");
    }
  });

  /* ---------- Leitura ao passar o mouse e ao focar com o Tab ----------
   * Pensada para pessoas com baixa visão que usam o mouse. Fica desligada
   * por padrão, porque quem usa leitor de tela já ouve tudo e as duas vozes
   * se sobreporiam. */
  var SELETOR_LEITURA = "a, button, label, input, select, textarea, summary, h1, h2, h3, h4, " +
    "p, li, dt, dd, th, td, legend, img, caption";
  var leitura = { ultimo: null, espera: null, marcado: null };

  /* Texto visível do elemento, sem as partes marcadas como decorativas (aria-hidden). */
  function textoLimpo(no) {
    var copia = no.cloneNode(true);
    copia.querySelectorAll("[aria-hidden='true']").forEach(function (x) { x.remove(); });
    copia.querySelectorAll("*").forEach(function (x) {
      x.insertBefore(document.createTextNode(" "), x.firstChild);
      x.appendChild(document.createTextNode(" "));
    });
    return (copia.textContent || "").replace(/\s+/g, " ").replace(/\s+([:.,;!?])/g, "$1").trim();
  }

  function nomeDoCampo(campo) {
    var rotulo = campo.id ? document.querySelector("label[for='" + campo.id + "']") : null;
    var nome = rotulo ? textoLimpo(rotulo) : (campo.getAttribute("aria-label") || campo.name || "");
    nome = nome.replace("*", "").trim();
    if (campo.type === "checkbox" || campo.type === "radio") {
      return (campo.type === "radio" ? "Opção: " : "Caixa de seleção: ") + nome + (campo.checked ? ", marcada." : ", desmarcada.");
    }
    if (campo.tagName === "SELECT") {
      return "Lista de opções: " + nome + ". Selecionado: " + (campo.options[campo.selectedIndex] || {}).text + ".";
    }
    return "Campo: " + nome + ". " + (campo.value ? "Preenchido com: " + campo.value + "." : "Vazio.");
  }

  function textoDoElemento(alvo) {
    var tag = alvo.tagName;
    if (tag === "IMG") { return alvo.alt ? "Imagem: " + alvo.alt : ""; }
    if (tag === "INPUT" || tag === "SELECT" || tag === "TEXTAREA") { return nomeDoCampo(alvo); }
    if (tag === "LABEL" && alvo.control) { return nomeDoCampo(alvo.control); }
    var texto = alvo.getAttribute("aria-label") || textoLimpo(alvo);
    if (!texto) { return ""; }
    if (texto.length > 400) { texto = texto.slice(0, 400) + "..."; }
    if (tag === "A") { return "Link: " + texto; }
    if (tag === "BUTTON") { return "Botão: " + texto + (alvo.getAttribute("aria-pressed") === "true" ? ", ativado." : ""); }
    if (/^H[1-4]$/.test(tag)) { return "Título: " + texto; }
    return texto;
  }

  function marcar(alvo) {
    if (leitura.marcado) { leitura.marcado.classList.remove("lendo-agora"); }
    leitura.marcado = alvo;
    if (alvo) { alvo.classList.add("lendo-agora"); }
  }

  function falarElemento(alvo) {
    if (!alvo || alvo === leitura.ultimo) { return; }
    var texto = textoDoElemento(alvo);
    if (!texto) { return; }
    leitura.ultimo = alvo;
    marcar(alvo);
    window.speechSynthesis.cancel();
    var fala = new window.SpeechSynthesisUtterance(texto);
    fala.lang = "pt-BR";
    fala.rate = voz.velocidade;
    var v = vozPortugues();
    if (v) { fala.voice = v; }
    window.speechSynthesis.speak(fala);
  }

  function alvoDeLeitura(no) {
    if (!no || !no.closest) { return null; }
    var alvo = no.closest(SELETOR_LEITURA);
    /* Dentro de um link ou botão, lê o link ou o botão inteiro. */
    var interativo = no.closest("a, button, label");
    return interativo || alvo;
  }

  document.addEventListener("mouseover", function (e) {
    if (raiz.getAttribute("data-leitura") !== "sim") { return; }
    var alvo = alvoDeLeitura(e.target);
    window.clearTimeout(leitura.espera);
    /* Pequena espera evita leituras ao apenas atravessar a página com o mouse. */
    leitura.espera = window.setTimeout(function () { falarElemento(alvo); }, 350);
  });

  document.addEventListener("focusin", function (e) {
    if (raiz.getAttribute("data-leitura") !== "sim") { return; }
    window.clearTimeout(leitura.espera);
    leitura.ultimo = null;
    falarElemento(alvoDeLeitura(e.target));
  });

  function alternarLeitura(ligar) {
    if (ligar && !voz.suportado) {
      BE.anunciar("Seu navegador não oferece leitura em voz alta. Experimente o Chrome, o Edge ou o Safari.");
      atualizarEstados();
      return;
    }
    definir("leitura", ligar ? "sim" : "");
    atualizarEstados();
    if (voz.suportado) {
      window.speechSynthesis.cancel();
      var aviso = new window.SpeechSynthesisUtterance(ligar
        ? "Leitura ao passar o mouse ativada. Pare o mouse sobre um texto para ouvir."
        : "Leitura ao passar o mouse desativada.");
      aviso.lang = "pt-BR";
      window.speechSynthesis.speak(aviso);
    }
    if (!ligar) { marcar(null); leitura.ultimo = null; }
  }

  document.addEventListener("DOMContentLoaded", function () {
    atualizarEstados();
    prepararVoz();
    /* Garante que os links de atalho levem o foco de verdade ao destino. */
    document.querySelectorAll(".lista-atalhos a[href^='#']").forEach(function (link) {
      link.addEventListener("click", function (e) {
        e.preventDefault();
        irPara(link.getAttribute("href").slice(1));
      });
    });
  });
})();

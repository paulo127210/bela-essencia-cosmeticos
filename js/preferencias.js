/*
 * Aplica as preferências de acessibilidade salvas ANTES de a página ser
 * desenhada, para não haver "piscada" de tema ou de tamanho de letra.
 * Este arquivo é carregado sem defer, no <head>.
 */
(function () {
  "use strict";
  var prefs = {};
  try {
    prefs = JSON.parse(window.localStorage.getItem("be_preferencias") || "{}") || {};
  } catch (e) {
    prefs = {};
  }
  var raiz = document.documentElement;
  var permitidos = {
    tema: ["escuro", "contraste"],
    fonte: ["125", "150", "175", "200"],
    espacamento: ["sim"],
    dislexia: ["sim"],
    daltonismo: ["protan", "deutan", "tritan"],
    leitura: ["sim"]
  };
  Object.keys(permitidos).forEach(function (chave) {
    var valor = String(prefs[chave] || "");
    if (permitidos[chave].indexOf(valor) !== -1) {
      raiz.setAttribute("data-" + chave, valor);
    }
  });
  /* Se a pessoa nunca escolheu um tema, respeita a preferência do sistema. */
  if (!prefs.tema && !prefs.temaEscolhido && window.matchMedia) {
    if (window.matchMedia("(prefers-contrast: more)").matches) {
      raiz.setAttribute("data-tema", "contraste");
    } else if (window.matchMedia("(prefers-color-scheme: dark)").matches) {
      raiz.setAttribute("data-tema", "escuro");
    }
  }
})();

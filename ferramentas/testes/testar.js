const http = require("http");
const fs = require("fs");
const path = require("path");
const { chromium } = require("playwright");
const axeSrc = fs.readFileSync(require.resolve("axe-core/axe.min.js"), "utf8");

const RAIZ = path.resolve(__dirname, "..", "..");
const cfg = JSON.parse(fs.readFileSync(path.join(RAIZ, "vercel.json"), "utf8"));
const csp = cfg.headers[0].headers.find(h => h.key === "Content-Security-Policy").value.replace("; upgrade-insecure-requests", "");
const tipos = { ".html": "text/html; charset=utf-8", ".css": "text/css", ".js": "text/javascript", ".svg": "image/svg+xml", ".woff2": "font/woff2" };

const servidor = http.createServer((req, res) => {
  let p = decodeURIComponent(req.url.split("?")[0]);
  if (p === "/") p = "/index.html";
  const arq = path.join(RAIZ, p);
  res.setHeader("Content-Security-Policy", csp);
  if (!arq.startsWith(RAIZ) || !fs.existsSync(arq) || fs.statSync(arq).isDirectory()) {
    res.statusCode = 404; res.setHeader("Content-Type", tipos[".html"]);
    return res.end(fs.readFileSync(path.join(RAIZ, "404.html")));
  }
  res.setHeader("Content-Type", tipos[path.extname(arq)] || "application/octet-stream");
  res.end(fs.readFileSync(arq));
}).listen(8765);

const BASE = "http://localhost:8765/";
const paginas = ["index.html", "produtos.html", "produtos.html?categoria=pele", "produto.html?id=serum-vitamina-c", "produto.html?id=inexistente",
  "carrinho.html", "finalizar.html", "contato.html", "acessibilidade.html", "mapa-do-site.html", "privacidade.html", "algo/que/nao/existe"];
const temas = [{}, { tema: "escuro" }, { tema: "contraste" }, { daltonismo: "deutan" }, { daltonismo: "tritan" }, { tema: "escuro", daltonismo: "tritan" }, { tema: "escuro", daltonismo: "protan" }];

(async () => {
  const navegador = await chromium.launch();
  const problemas = [];
  const erros = [];

  async function abrir(ctx, url) {
    const pg = await ctx.newPage();
    pg.on("console", m => { if (m.type() === "error") erros.push(url + " => " + m.text()); });
    pg.on("pageerror", e => erros.push(url + " => " + e.message));
    await pg.goto(BASE + url, { waitUntil: "networkidle" });
    return pg;
  }
  async function axe(pg, rotulo) {
    await pg.addScriptTag({ content: axeSrc }).catch(() => pg.evaluate(axeSrc));
    const r = await pg.evaluate(() => axe.run(document, { runOnly: ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22aa", "best-practice"] }));
    r.violations.forEach(v => problemas.push(`${rotulo}: [${v.impact}] ${v.id} - ${v.help} -> ${v.nodes.slice(0, 3).map(n => n.target.join(" ")).join(" | ")}`));
  }

  // carrinho com itens para as páginas de carrinho e finalizar
  for (const prefs of temas) {
    const ctx = await navegador.newContext();
    await ctx.addInitScript(p => {
      localStorage.setItem("be_preferencias", JSON.stringify(Object.assign({ temaEscolhido: true }, p)));
      localStorage.setItem("be_carrinho", JSON.stringify([{ id: "batom-cremoso-rose", qtd: 2 }, { id: "perfume-noite-de-ambar", qtd: 1 }]));
    }, prefs);
    for (const url of paginas) {
      const pg = await abrir(ctx, url);
      await axe(pg, `${JSON.stringify(prefs)} ${url}`);
      // painel aberto
      if (url === "index.html") {
        await pg.click("#botao-recursos");
        await axe(pg, `${JSON.stringify(prefs)} painel`);
      }
      await pg.close();
    }
    await ctx.close();
  }
  // CSP bypass: axe injection may be blocked by CSP; ensure it ran
  console.log("== Violações axe:", problemas.length);
  [...new Set(problemas)].forEach(p => console.log(p));
  console.log("== Erros de console:", erros.filter(e => !e.includes("axe")).length);
  [...new Set(erros)].forEach(e => console.log(e));

  // ---------- Reflow ----------
  const reflow = [];
  for (const [larg, fonte] of [[320, null], [1280, "200"], [640, "200"]]) {
    const ctx = await navegador.newContext({ viewport: { width: larg, height: 800 } });
    await ctx.addInitScript(f => { if (f) localStorage.setItem("be_preferencias", JSON.stringify({ fonte: f, espacamento: "sim" })); localStorage.setItem("be_carrinho", JSON.stringify([{ id: "serum-vitamina-c", qtd: 1 }])); }, fonte);
    for (const url of paginas.slice(0, 9)) {
      const pg = await abrir(ctx, url);
      const sw = await pg.evaluate(() => document.documentElement.scrollWidth);
      if (sw > larg + 1) reflow.push(`${larg}px fonte ${fonte}: ${url} rola na horizontal (${sw}px)`);
      await pg.close();
    }
    await ctx.close();
  }
  console.log("== Reflow:", reflow.length ? reflow.join("\n") : "ok");

  // ---------- Fluxo de compra e teclado ----------
  const ctx = await navegador.newContext({ viewport: { width: 1280, height: 900 } });
  const log = [];
  let pg = await abrir(ctx, "produto.html?id=serum-vitamina-c");
  await pg.keyboard.press("Alt+1");
  log.push("Alt+1 foca: " + await pg.evaluate(() => document.activeElement.id));
  await pg.keyboard.press("Alt+3");
  log.push("Alt+3 foca: " + await pg.evaluate(() => document.activeElement.id));
  await pg.click("button[aria-label^='Aumentar quantidade']");
  await pg.click(".comprar .botao");
  await pg.waitForTimeout(200);
  log.push("Aviso: " + await pg.textContent("#aviso-educado"));
  log.push("Contador: " + await pg.textContent(".contador-carrinho"));
  await pg.close();

  pg = await abrir(ctx, "produtos.html?busca=perfume");
  log.push("Busca perfume: " + await pg.textContent("#contagem-produtos"));
  await pg.check("#filtro-braille");
  await pg.waitForTimeout(150);
  log.push("Com braille: " + await pg.textContent("#contagem-produtos"));
  await pg.close();

  pg = await abrir(ctx, "carrinho.html");
  await pg.click("button[aria-label^='Aumentar quantidade']");
  await pg.waitForTimeout(150);
  log.push("Carrinho: " + (await pg.textContent("#valores-resumo")).replace(/\s+/g, " ") + " | " + await pg.textContent("#aviso-frete"));
  await pg.screenshot({ path: path.join(__dirname, "capturas", "carrinho.png"), fullPage: true });
  await pg.close();

  pg = await abrir(ctx, "finalizar.html");
  await pg.click("#form-checkout button[type=submit]");
  await pg.waitForTimeout(150);
  log.push("Foco após envio vazio: " + await pg.evaluate(() => document.activeElement.className));
  log.push("Erros listados: " + await pg.$$eval(".resumo-erros li", l => l.length));
  log.push("aria-describedby do email: " + await pg.getAttribute("#email", "aria-describedby"));
  await axe(pg, "finalizar com erros");
  await pg.screenshot({ path: path.join(__dirname, "capturas", "checkout-erros.png"), fullPage: true });
  await pg.fill("#nome", "Maria da Silva");
  await pg.fill("#email", "maria@email.com");
  await pg.fill("#telefone", "41999998888");
  await pg.fill("#cep", "80010000");
  await pg.fill("#endereco", "Rua XV de Novembro");
  await pg.fill("#numero", "100");
  await pg.fill("#bairro", "Centro");
  await pg.fill("#cidade", "Curitiba");
  await pg.selectOption("#uf", "PR");
  await pg.check("#pagamento");
  await pg.check("#consentimento");
  await pg.click("#form-checkout button[type=submit]");
  await pg.waitForTimeout(150);
  log.push("Confirmação: " + (await pg.textContent("#confirmacao")).replace(/\s+/g, " ").slice(0, 160));
  log.push("Foco: " + await pg.evaluate(() => document.activeElement.id));
  log.push("Carrinho após pedido: " + await pg.textContent(".contador-carrinho"));
  await pg.close();

  pg = await abrir(ctx, "contato.html");
  await pg.fill("#contato-nome", "Ana");
  await pg.fill("#contato-email", "ana@");
  await pg.click("#form-contato button[type=submit]");
  log.push("Contato erros: " + await pg.$$eval(".resumo-erros li", l => l.map(x => x.textContent).join(" / ")));
  await pg.close();

  for (const [nome, url, prefs] of [["inicio", "index.html", {}], ["inicio-contraste", "index.html", { tema: "contraste" }], ["produto-escuro", "produto.html?id=perfume-flor-de-laranjeira", { tema: "escuro" }], ["catalogo", "produtos.html", {}], ["inicio-200", "index.html", { fonte: "200" }]]) {
    const c = await navegador.newContext({ viewport: { width: 1280, height: 900 } });
    await c.addInitScript(p => localStorage.setItem("be_preferencias", JSON.stringify(Object.assign({ temaEscolhido: true }, p))), prefs);
    const pp = await c.newPage();
    await pp.goto(BASE + url, { waitUntil: "networkidle" });
    await pp.screenshot({ path: path.join(__dirname, "capturas", nome + ".png") });
    await c.close();
  }
  const cm = await navegador.newContext({ viewport: { width: 390, height: 844 } });
  const pm = await cm.newPage(); await pm.goto(BASE + "index.html", { waitUntil: "networkidle" }); await pm.screenshot({ path: path.join(__dirname, "capturas", "celular.png"), fullPage: true });
  await pm.goto(BASE + "index.html", { waitUntil: "networkidle" }); await pm.click("#botao-recursos"); await pm.screenshot({ path: path.join(__dirname, "capturas", "celular-painel.png") });

  console.log("== Fluxo:\n" + log.join("\n"));
  await navegador.close();
  servidor.close();
})();

"""Gera as fotos ilustradas dos produtos (SVG) a partir de js/produtos.js.

Uso: python3 ferramentas/gerar_imagens.py

Cada imagem simula uma foto de estúdio: fundo com degradê, vidro com
reflexo, tampas metálicas, sombra no chão e rótulo da marca Bela Essência.
As embalagens são criação própria da loja. O texto alternativo de cada
imagem fica em js/produtos.js, no campo "alt".
"""
import pathlib
import re

RAIZ = pathlib.Path(__file__).resolve().parent.parent
DADOS = (RAIZ / "js" / "produtos.js").read_text(encoding="utf-8")
blocos = re.findall(r'id: "([^"]+)".*?forma: "([^"]+)", corImagem: "([^"]+)"', DADOS, re.S)

# Texto impresso no rótulo de cada embalagem: (linha do produto, detalhe)
ROTULOS = {
    "batom-cremoso-rose": ("ROSÉ", "cremoso"),
    "batom-matte-vermelho": ("CLÁSSICO", "matte"),
    "mascara-cilios-volume": ("VOLUME TOTAL", "máscara"),
    "base-liquida-natural": ("BASE", "efeito natural · FPS 20"),
    "serum-vitamina-c": ("VITAMINA C", "sérum 10%"),
    "hidratante-facial-acido-hialuronico": ("HIALURÔNICO", "gel creme facial"),
    "protetor-solar-fps50": ("FPS 50", "protetor facial"),
    "agua-micelar": ("ÁGUA MICELAR", "5 em 1"),
    "shampoo-reconstrucao": ("RECONSTRUÇÃO", "shampoo"),
    "condicionador-reconstrucao": ("RECONSTRUÇÃO", "condicionador"),
    "oleo-capilar-argan": ("ARGAN", "óleo capilar"),
    "perfume-flor-de-laranjeira": ("FLOR DE LARANJEIRA", "eau de parfum"),
    "perfume-noite-de-ambar": ("NOITE DE ÂMBAR", "eau de parfum"),
    "body-splash-frutas-vermelhas": ("FRUTAS VERMELHAS", "body splash"),
    "hidratante-corporal-karite": ("KARITÉ", "loção hidratante"),
    "sabonete-liquido-lavanda": ("LAVANDA", "sabonete líquido"),
}

SERIFA = "Georgia, 'Times New Roman', serif"
SEM_SERIFA = "'Segoe UI', Arial, Helvetica, sans-serif"


def clarear(hexa, f):
    """f > 0 clareia, f < 0 escurece."""
    r, g, b = (int(hexa[i:i + 2], 16) for i in (1, 3, 5))
    if f >= 0:
        r, g, b = (int(c + (255 - c) * f) for c in (r, g, b))
    else:
        r, g, b = (int(c * (1 + f)) for c in (r, g, b))
    return f"#{r:02X}{g:02X}{b:02X}"


def cor_texto(hexa):
    r, g, b = (int(hexa[i:i + 2], 16) for i in (1, 3, 5))
    return "#2B1626" if (0.299 * r + 0.587 * g + 0.114 * b) > 150 else "#FFFFFF"


def defs(cor):
    """Degradês compartilhados: fundo, metal dourado, vidro e corpo colorido."""
    return f"""<defs>
<linearGradient id="fundo" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#FFFFFF"/><stop offset=".62" stop-color="#F9EEF3"/><stop offset="1" stop-color="#EED7E1"/>
</linearGradient>
<radialGradient id="luz" cx="50%" cy="30%" r="60%">
  <stop offset="0" stop-color="#FFFFFF" stop-opacity=".9"/><stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/>
</radialGradient>
<radialGradient id="sombra" cx="50%" cy="50%" r="50%">
  <stop offset="0" stop-color="#4A2238" stop-opacity=".35"/><stop offset="1" stop-color="#4A2238" stop-opacity="0"/>
</radialGradient>
<linearGradient id="ouro" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0" stop-color="#8C6A2F"/><stop offset=".18" stop-color="#E9D29A"/><stop offset=".35" stop-color="#C9A55A"/>
  <stop offset=".6" stop-color="#F6E7B8"/><stop offset=".82" stop-color="#B08840"/><stop offset="1" stop-color="#6E5122"/>
</linearGradient>
<linearGradient id="prata" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0" stop-color="#7D838C"/><stop offset=".2" stop-color="#E9EDF2"/><stop offset=".45" stop-color="#AEB5BF"/>
  <stop offset=".65" stop-color="#F7F9FB"/><stop offset="1" stop-color="#6B717A"/>
</linearGradient>
<linearGradient id="preto" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0" stop-color="#0E0E10"/><stop offset=".25" stop-color="#4A4A52"/><stop offset=".45" stop-color="#1C1C20"/>
  <stop offset=".7" stop-color="#3A3A40"/><stop offset="1" stop-color="#08080A"/>
</linearGradient>
<linearGradient id="corpo" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0" stop-color="{clarear(cor, -.35)}"/><stop offset=".22" stop-color="{clarear(cor, .25)}"/>
  <stop offset=".5" stop-color="{cor}"/><stop offset=".8" stop-color="{clarear(cor, -.15)}"/><stop offset="1" stop-color="{clarear(cor, -.45)}"/>
</linearGradient>
<linearGradient id="liquido" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="{clarear(cor, .15)}" stop-opacity=".85"/><stop offset="1" stop-color="{clarear(cor, -.25)}" stop-opacity=".95"/>
</linearGradient>
<linearGradient id="vidro" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0" stop-color="#FFFFFF" stop-opacity=".55"/><stop offset=".12" stop-color="#FFFFFF" stop-opacity=".08"/>
  <stop offset=".85" stop-color="#FFFFFF" stop-opacity=".05"/><stop offset="1" stop-color="#FFFFFF" stop-opacity=".45"/>
</linearGradient>
<linearGradient id="brilho" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0" stop-color="#FFFFFF" stop-opacity="0"/><stop offset=".5" stop-color="#FFFFFF" stop-opacity=".75"/><stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/>
</linearGradient>
</defs>"""


def cena(conteudo, cor, largura_sombra=150):
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 600" aria-hidden="true">'
        + defs(cor)
        + '<rect width="600" height="600" fill="url(#fundo)"/>'
        + '<ellipse cx="300" cy="230" rx="300" ry="230" fill="url(#luz)"/>'
        + '<rect y="455" width="600" height="145" fill="#EAD0DB" opacity=".35"/>'
        + f'<ellipse cx="300" cy="512" rx="{largura_sombra}" ry="22" fill="url(#sombra)"/>'
        + conteudo
        + "</svg>\n"
    )


def rotulo(cx, y, linha, detalhe, cor_txt, largura, tamanho=22):
    """Rótulo da marca: nome da loja, linha do produto e detalhe."""
    tam = min(tamanho, int(largura / max(len(linha), 6) * 1.55))
    return (
        f'<g text-anchor="middle" fill="{cor_txt}">'
        f'<text x="{cx}" y="{y}" font-family="{SEM_SERIFA}" font-size="10" letter-spacing="2">BELA ESSÊNCIA</text>'
        f'<line x1="{cx - 26}" y1="{y + 10}" x2="{cx + 26}" y2="{y + 10}" stroke="{cor_txt}" stroke-width="1" opacity=".6"/>'
        f'<text x="{cx}" y="{y + 18 + tam}" font-family="{SERIFA}" font-size="{tam}" letter-spacing="1">{linha}</text>'
        f'<text x="{cx}" y="{y + 40 + tam}" font-family="{SERIFA}" font-style="italic" font-size="14" opacity=".85">{detalhe}</text>'
        "</g>"
    )


# ------------------------------------------------------------------ formas
def batom(cor, linha, detalhe):
    return cena(f"""
<g transform="translate(395 360) rotate(-12)">
  <rect x="-38" y="0" width="76" height="140" rx="6" fill="url(#ouro)"/>
  <rect x="-38" y="0" width="76" height="12" fill="#000" opacity=".12"/>
  <rect x="-30" y="40" width="10" height="90" rx="5" fill="#FFF" opacity=".35"/>
</g>
<rect x="215" y="300" width="96" height="190" rx="8" fill="url(#ouro)"/>
<rect x="215" y="300" width="96" height="14" fill="#000" opacity=".15"/>
<rect x="215" y="398" width="96" height="6" fill="#6E5122" opacity=".5"/>
<text x="263" y="460" text-anchor="middle" font-family="{SEM_SERIFA}" font-size="10" letter-spacing="2.4" fill="#4A3613">BELA ESSÊNCIA</text>
<rect x="229" y="232" width="68" height="72" rx="4" fill="url(#ouro)"/>
<path d="M237 236 L237 128 Q237 112 252 102 L289 78 L289 236 Z" fill="url(#corpo)"/>
<path d="M243 230 L243 132 Q243 120 252 113" stroke="#FFF" stroke-width="5" fill="none" opacity=".45" stroke-linecap="round"/>
<path d="M289 78 L289 236" stroke="#000" stroke-width="6" opacity=".12"/>
<rect x="225" y="300" width="14" height="180" rx="7" fill="#FFF" opacity=".35"/>
""", cor, 190)


def rimel(cor, linha, detalhe):
    return cena(f"""
<g transform="translate(360 488) rotate(-8) scale(.85)">
  <rect x="-15" y="-330" width="30" height="210" rx="12" fill="url(#preto)"/>
  <rect x="-22" y="-125" width="44" height="125" rx="10" fill="url(#ouro)"/>
  <rect x="-3" y="-420" width="6" height="95" fill="#8C8C94"/>
  <g stroke="#111" stroke-width="3" stroke-linecap="round">
    {"".join(f'<line x1="{-14 + (i % 2) * 3}" y1="{-480 + i * 6}" x2="{14 - (i % 2) * 3}" y2="{-480 + i * 6}"/>' for i in range(11))}
  </g>
  <ellipse cx="0" cy="-450" rx="12" ry="36" fill="#1A1A1E"/>
</g>
<rect x="190" y="150" width="78" height="340" rx="36" fill="url(#preto)"/>
<rect x="190" y="150" width="78" height="96" rx="36" fill="url(#ouro)"/>
<rect x="190" y="232" width="78" height="14" fill="#000" opacity=".25"/>
<rect x="202" y="260" width="10" height="210" rx="5" fill="#FFF" opacity=".22"/>
<g transform="translate(240 370) rotate(-90)" text-anchor="middle" fill="#E9D29A">
  <text font-family="{SEM_SERIFA}" font-size="11" letter-spacing="3" y="-6">BELA ESSÊNCIA</text>
  <text font-family="{SERIFA}" font-size="20" y="18">{linha}</text>
</g>
""", cor, 140)


def frasco(cor, linha, detalhe):
    return cena(f"""
<rect x="190" y="215" width="220" height="280" rx="28" fill="url(#corpo)" opacity=".18"/>
<rect x="206" y="250" width="188" height="232" rx="16" fill="url(#liquido)"/>
<rect x="190" y="215" width="220" height="280" rx="28" fill="none" stroke="#FFF" stroke-opacity=".9" stroke-width="10"/>
<rect x="190" y="215" width="220" height="280" rx="28" fill="url(#vidro)"/>
<rect x="206" y="232" width="16" height="240" rx="8" fill="#FFF" opacity=".6"/>
<rect x="228" y="300" width="144" height="120" rx="6" fill="#FFFFFF" opacity=".92"/>
{rotulo(300, 330, linha, detalhe, "#5C2A47", 130)}
<rect x="252" y="170" width="96" height="48" rx="8" fill="url(#ouro)"/>
<rect x="286" y="118" width="28" height="54" fill="url(#preto)"/>
<path d="M286 118 L286 100 Q286 92 294 92 L372 92 Q382 92 382 102 L382 112 L314 112 L314 118 Z" fill="url(#preto)"/>
<rect x="252" y="170" width="96" height="8" fill="#FFF" opacity=".35"/>
""", cor, 170)


def frasco_alto(cor, linha, detalhe):
    texto = cor_texto(cor)
    return cena(f"""
<path d="M215 170 Q215 140 245 135 L355 135 Q385 140 385 170 L392 460 Q392 495 357 495 L243 495 Q208 495 208 460 Z" fill="url(#corpo)"/>
<path d="M228 180 Q228 155 248 150" stroke="#FFF" stroke-width="7" fill="none" opacity=".5" stroke-linecap="round"/>
<rect x="226" y="190" width="14" height="270" rx="7" fill="url(#brilho)" opacity=".7"/>
<rect x="245" y="275" width="110" height="130" rx="8" fill="#FFFFFF" opacity="{'.92' if texto == '#FFFFFF' else '.55'}"/>
{rotulo(300, 305, linha, detalhe, "#5C2A47", 100, 18)}
<rect x="250" y="70" width="100" height="70" rx="14" fill="url(#ouro)"/>
<rect x="250" y="70" width="100" height="14" rx="7" fill="#FFF" opacity=".3"/>
<rect x="250" y="128" width="100" height="10" fill="#000" opacity=".15"/>
<line x1="388" y1="300" x2="390" y2="380" stroke="{clarear(cor, -.5)}" stroke-width="3" opacity=".6"/>
""", cor, 150)


def contagotas(cor, linha, detalhe):
    return cena(f"""
<rect x="205" y="250" width="190" height="245" rx="34" fill="url(#corpo)"/>
<rect x="205" y="250" width="190" height="245" rx="34" fill="url(#vidro)"/>
<rect x="220" y="270" width="16" height="200" rx="8" fill="#FFF" opacity=".5"/>
<rect x="236" y="320" width="128" height="120" rx="6" fill="#FFF8F0" opacity=".95"/>
{rotulo(300, 348, linha, detalhe, "#5C2A47", 115)}
<rect x="250" y="205" width="100" height="50" rx="8" fill="url(#ouro)"/>
<rect x="250" y="243" width="100" height="10" fill="#000" opacity=".2"/>
<path d="M262 208 L262 150 Q262 82 300 74 Q338 82 338 150 L338 208 Z" fill="url(#preto)"/>
<path d="M276 196 L276 150 Q276 108 296 96" stroke="#FFF" stroke-width="6" fill="none" opacity=".25" stroke-linecap="round"/>
""", cor, 150)


def pote(cor, linha, detalhe):
    return cena(f"""
<path d="M160 300 L440 300 L432 470 Q430 495 405 495 L195 495 Q170 495 168 470 Z" fill="#FFFFFF"/>
<path d="M160 300 L440 300 L432 470 Q430 495 405 495 L195 495 Q170 495 168 470 Z" fill="url(#vidro)" opacity=".9"/>
<path d="M160 300 L440 300 L432 470 Q430 495 405 495 L195 495 Q170 495 168 470 Z" fill="none" stroke="#E3CBD5" stroke-width="2"/>
<rect x="178" y="315" width="14" height="160" rx="7" fill="#E8DCE2" opacity=".8"/>
<rect x="408" y="315" width="12" height="160" rx="6" fill="#D9C3CE" opacity=".7"/>
{rotulo(300, 365, linha, detalhe, "#5C2A47", 200)}
<rect x="150" y="215" width="300" height="92" rx="18" fill="url(#corpo)"/>
<g stroke="#000" stroke-opacity=".12" stroke-width="3">
  {"".join(f'<line x1="{163 + i * 11}" y1="222" x2="{163 + i * 11}" y2="300"/>' for i in range(26))}
</g>
<rect x="150" y="215" width="300" height="16" rx="8" fill="#FFF" opacity=".35"/>
""", cor, 200)


def bisnaga(cor, linha, detalhe):
    return cena(f"""
<path d="M205 85 L395 85 L372 395 Q370 410 355 410 L245 410 Q230 410 228 395 Z" fill="url(#corpo)"/>
<rect x="200" y="72" width="200" height="22" rx="3" fill="{clarear(cor, -.25)}"/>
<g stroke="#000" stroke-opacity=".15" stroke-width="2">
  {"".join(f'<line x1="{206 + i * 8}" y1="74" x2="{206 + i * 8}" y2="92"/>' for i in range(24))}
</g>
<path d="M222 105 L238 395" stroke="#FFF" stroke-width="10" opacity=".35" stroke-linecap="round"/>
<circle cx="300" cy="185" r="34" fill="#FFF" opacity=".8"/>
<g stroke="#FFF" stroke-width="6" stroke-linecap="round" opacity=".9">
  <line x1="300" y1="132" x2="300" y2="142"/><line x1="300" y1="228" x2="300" y2="238"/>
  <line x1="247" y1="185" x2="257" y2="185"/><line x1="343" y1="185" x2="353" y2="185"/>
</g>
{rotulo(300, 262, linha, detalhe, "#5C2A47", 130, 24)}
<rect x="240" y="405" width="120" height="90" rx="16" fill="#FFFFFF"/>
<rect x="240" y="405" width="120" height="90" rx="16" fill="url(#vidro)"/>
<rect x="240" y="405" width="120" height="10" fill="#000" opacity=".1"/>
<rect x="250" y="420" width="10" height="64" rx="5" fill="#E8DCE2"/>
""", cor, 130)


def perfume(cor, linha, detalhe):
    return cena(f"""
<path d="M165 260 Q165 215 210 212 L390 212 Q435 215 435 260 L435 448 Q435 495 390 495 L210 495 Q165 495 165 448 Z" fill="url(#liquido)"/>
<path d="M165 260 Q165 215 210 212 L390 212 Q435 215 435 260 L435 448 Q435 495 390 495 L210 495 Q165 495 165 448 Z" fill="none" stroke="#FFF" stroke-opacity=".85" stroke-width="14"/>
<path d="M165 260 Q165 215 210 212 L390 212 Q435 215 435 260 L435 448 Q435 495 390 495 L210 495 Q165 495 165 448 Z" fill="url(#vidro)"/>
<path d="M195 250 L195 460" stroke="#FFF" stroke-width="12" opacity=".55" stroke-linecap="round"/>
<path d="M405 260 L405 450" stroke="#FFF" stroke-width="4" opacity=".4" stroke-linecap="round"/>
<polygon points="300,212 435,330 300,495 165,330" fill="#FFF" opacity=".06"/>
{rotulo(300, 330, linha, detalhe, cor_texto(cor) if cor_texto(cor) == "#FFFFFF" else "#3D1A2E", 230, 22)}
<rect x="270" y="180" width="60" height="36" fill="url(#ouro)"/>
<rect x="270" y="180" width="60" height="6" fill="#000" opacity=".2"/>
<rect x="240" y="88" width="120" height="96" rx="10" fill="url(#ouro)"/>
<rect x="240" y="88" width="120" height="16" rx="8" fill="#FFF" opacity=".35"/>
<rect x="252" y="110" width="10" height="64" rx="5" fill="#FFF" opacity=".35"/>
""", cor, 190)


DESENHOS = {
    "batom": batom, "rimel": rimel, "frasco": frasco, "frasco-alto": frasco_alto,
    "contagotas": contagotas, "pote": pote, "bisnaga": bisnaga, "perfume": perfume,
}

destino = RAIZ / "img" / "produtos"
destino.mkdir(parents=True, exist_ok=True)
for ident, forma, cor in blocos:
    linha, detalhe = ROTULOS[ident]
    (destino / f"{ident}.svg").write_text(DESENHOS[forma](cor, linha, detalhe), encoding="utf-8")
print(f"{len(blocos)} imagens geradas em {destino}")

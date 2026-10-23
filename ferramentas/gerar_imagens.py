"""Gera as ilustrações SVG dos produtos a partir de js/produtos.js.

Uso: python3 ferramentas/gerar_imagens.py
As imagens são desenhos simples, leves e sem texto embutido. O texto
alternativo de cada uma fica em js/produtos.js, no campo "alt".
"""
import pathlib
import re

RAIZ = pathlib.Path(__file__).resolve().parent.parent
DADOS = (RAIZ / "js" / "produtos.js").read_text(encoding="utf-8")

blocos = re.findall(r'id: "([^"]+)".*?forma: "([^"]+)", corImagem: "([^"]+)"', DADOS, re.S)

FUNDO = (
    '<defs><radialGradient id="f" cx="50%" cy="40%" r="70%">'
    '<stop offset="0" stop-color="#FFFFFF"/><stop offset="1" stop-color="#F7E4EC"/>'
    '</radialGradient></defs><rect width="400" height="400" fill="url(#f)"/>'
    '<ellipse cx="200" cy="350" rx="110" ry="14" fill="#000" opacity=".08"/>'
)


def batom(c):
    return (
        '<rect x="160" y="210" width="80" height="140" rx="8" fill="#C9CDD3"/>'
        '<rect x="160" y="210" width="80" height="18" fill="#AEB3BA"/>'
        '<rect x="172" y="150" width="56" height="62" rx="4" fill="#E2E5E9"/>'
        f'<path d="M178 152 L178 80 Q200 50 222 70 L222 152 Z" fill="{c}"/>'
        '<path d="M184 150 L184 90" stroke="#fff" stroke-width="5" opacity=".35" stroke-linecap="round"/>'
    )


def rimel(c):
    return (
        f'<rect x="120" y="120" width="44" height="230" rx="20" fill="{c}"/>'
        '<rect x="128" y="130" width="8" height="200" rx="4" fill="#fff" opacity=".2"/>'
        '<rect x="226" y="70" width="14" height="190" rx="6" fill="#B08A57"/>'
        '<rect x="222" y="250" width="22" height="100" rx="10" fill="#3A3A3A"/>'
        '<g stroke="#1A1A1A" stroke-width="3">'
        + "".join(f'<line x1="{220 + (i % 2) * 2}" y1="{75 + i * 9}" x2="{246 - (i % 2) * 2}" y2="{75 + i * 9}"/>' for i in range(10))
        + "</g>"
    )


def frasco(c):
    return (
        f'<rect x="130" y="150" width="140" height="200" rx="18" fill="{c}"/>'
        '<rect x="142" y="165" width="20" height="170" rx="8" fill="#fff" opacity=".3"/>'
        '<rect x="175" y="120" width="50" height="32" rx="6" fill="#4A3440"/>'
        '<rect x="192" y="80" width="16" height="42" fill="#4A3440"/>'
        '<rect x="192" y="74" width="62" height="16" rx="6" fill="#4A3440"/>'
        '<rect x="155" y="230" width="90" height="56" rx="6" fill="#fff" opacity=".75"/>'
    )


def frasco_alto(c):
    return (
        f'<rect x="145" y="110" width="110" height="240" rx="26" fill="{c}"/>'
        '<rect x="157" y="125" width="18" height="210" rx="8" fill="#fff" opacity=".3"/>'
        '<rect x="168" y="70" width="64" height="44" rx="10" fill="#D4AF6A"/>'
        '<rect x="165" y="210" width="70" height="70" rx="8" fill="#fff" opacity=".7"/>'
    )


def contagotas(c):
    return (
        f'<rect x="140" y="170" width="120" height="180" rx="22" fill="{c}"/>'
        '<rect x="152" y="185" width="16" height="150" rx="8" fill="#fff" opacity=".3"/>'
        '<rect x="170" y="140" width="60" height="34" rx="6" fill="#2D2D2D"/>'
        '<path d="M178 142 Q178 70 200 64 Q222 70 222 142 Z" fill="#1F1F1F"/>'
        '<rect x="160" y="240" width="80" height="50" rx="6" fill="#fff" opacity=".7"/>'
    )


def pote(c):
    return (
        '<rect x="110" y="220" width="180" height="120" rx="22" fill="#FFFFFF" stroke="#E3CBD5" stroke-width="3"/>'
        f'<rect x="102" y="180" width="196" height="54" rx="14" fill="{c}"/>'
        '<g stroke="#000" stroke-opacity=".12" stroke-width="3">'
        + "".join(f'<line x1="{112 + i * 12}" y1="186" x2="{112 + i * 12}" y2="228"/>' for i in range(15))
        + "</g>"
        '<rect x="140" y="260" width="120" height="44" rx="6" fill="#F7E4EC"/>'
    )


def bisnaga(c):
    return (
        f'<path d="M130 90 L270 90 L250 300 L150 300 Z" fill="{c}"/>'
        '<rect x="126" y="82" width="148" height="18" rx="4" fill="#E3B23C"/>'
        '<rect x="160" y="300" width="80" height="50" rx="10" fill="#FFFFFF" stroke="#E3CBD5" stroke-width="3"/>'
        '<circle cx="200" cy="180" r="30" fill="#fff" opacity=".7"/>'
        '<g stroke="#fff" stroke-width="5" stroke-linecap="round" opacity=".8">'
        '<line x1="200" y1="132" x2="200" y2="142"/><line x1="200" y1="218" x2="200" y2="228"/>'
        '<line x1="152" y1="180" x2="162" y2="180"/><line x1="238" y1="180" x2="248" y2="180"/></g>'
    )


def perfume(c):
    return (
        f'<path d="M120 210 Q120 160 170 160 L230 160 Q280 160 280 210 L280 300 Q280 350 230 350 L170 350 Q120 350 120 300 Z" fill="{c}" opacity=".9"/>'
        '<path d="M140 200 Q145 175 170 175" stroke="#fff" stroke-width="8" fill="none" opacity=".45" stroke-linecap="round"/>'
        '<rect x="182" y="132" width="36" height="30" fill="#C9A24A"/>'
        '<g fill="#D4AF6A">'
        '<circle cx="200" cy="96" r="18"/><circle cx="178" cy="112" r="16"/><circle cx="222" cy="112" r="16"/>'
        '<circle cx="186" cy="126" r="14"/><circle cx="214" cy="126" r="14"/></g>'
        '<circle cx="200" cy="112" r="10" fill="#F4E2B0"/>'
    )


DESENHOS = {
    "batom": batom, "rimel": rimel, "frasco": frasco, "frasco-alto": frasco_alto,
    "contagotas": contagotas, "pote": pote, "bisnaga": bisnaga, "perfume": perfume,
}

destino = RAIZ / "img" / "produtos"
destino.mkdir(parents=True, exist_ok=True)
for ident, forma, cor in blocos:
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400" aria-hidden="true">'
        + FUNDO + DESENHOS[forma](cor) + "</svg>\n"
    )
    (destino / f"{ident}.svg").write_text(svg, encoding="utf-8")
print(f"{len(blocos)} imagens geradas em {destino}")

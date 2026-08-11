import os
import re
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

load_dotenv()

LOGIN_URL = "https://platform.securityscorecard.io/#/home"
BASE_URL = "https://platform.securityscorecard.io/#/scorecard/{dominio}/issues/OPEN"

# Salva os arquivos na mesma pasta do script
SAIDA = Path(__file__).parent

# XPaths dos campos de login
XPATH_EMAIL = "/html/body/div[2]/div/form/fieldset[1]/div[1]/p[1]/input"
XPATH_SENHA = "/html/body/div[2]/div/form/fieldset[1]/div[1]/p[2]/input"

# XPath da nota de score (apenas o numero)
XPATH_NOTA = "/html/body/div[3]/div/div[1]/div[1]/div[2]/div[1]/div/div/div/div[1]/div[1]/div/div/div"

# Nomes das colunas da tabela de issues (na ordem em que aparecem)
COLUNAS = [
    "Issue", "Factor", "Threat level", "Breach risk",
    "Impact", "Recalibrated impact", "Findings", "Source", "Attestation",
]

def limpar_texto(texto: str) -> str:
    """Remove espacos duplicados e linhas vazias em excesso."""
    linhas = [re.sub(r"\s+", " ", l).strip() for l in texto.splitlines()]
    linhas = [l for l in linhas if l]
    return "\n".join(linhas)

def coletar_texto(page, xpath, timeout=8000):
    """Tenta coletar o texto de um elemento por XPath. Retorna None se nao achar."""
    try:
        locator = page.locator(f"xpath={xpath}")
        locator.wait_for(state="visible", timeout=timeout)
        return locator.inner_text().strip()
    except Exception:
        return None

def extrair_tabela_issues(page):
    """
    Tenta localizar a tabela de issues e extrair cada linha como um bloco.
    Retorna (lista_de_blocos, texto_bruto_fallback).
    """
    blocos = []
    texto_bruto = None

    try:
        # Procura a tabela. A SPA pode usar <table> ou <div role="table">.
        tabela = page.locator("table").first
        tabela.wait_for(state="visible", timeout=15000)

        linhas = tabela.locator("tbody tr").all()
        if not linhas:
            # Tenta pegar todas as <tr> se nao houver tbody
            linhas = tabela.locator("tr").all()

        for linha in linhas:
            celulas = [c.inner_text().strip() for c in linha.locator("td, th").all()]
            celulas = [c for c in celulas if c]  # remove celulas vazias
            if not celulas:
                continue

            # Monta um bloco com os campos rotulados
            bloco = []
            for i, valor in enumerate(celulas):
                nome_coluna = COLUNAS[i] if i < len(COLUNAS) else f"Campo {i + 1}"
                bloco.append(f"{nome_coluna}: {valor}")
            blocos.append("\n".join(bloco))

    except Exception:
        # Fallback: se nao achar a tabela, guarda o texto bruto da pagina
        try:
            texto_bruto = limpar_texto(page.inner_text("body"))
        except Exception:
            texto_bruto = None

    return blocos, texto_bruto

def coletar_cliente(nome, email, senha, dominio):
    print(f"[{nome}] Iniciando coleta de {dominio}...")

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,          # True para rodar sem janela
            channel="msedge"
        )
        context = browser.new_context(
            viewport={"width": 1600, "height": 1000},
            locale="pt-BR",
        )
        page = context.new_page()

        # 1) Abre a tela de login
        page.goto(LOGIN_URL, wait_until="domcontentloaded")
        page.wait_for_timeout(3000)

        # 2) Preenche e-mail e senha
        page.locator(f"xpath={XPATH_EMAIL}").wait_for(state="visible", timeout=20000)
        page.locator(f"xpath={XPATH_EMAIL}").fill(email)
        page.locator(f"xpath={XPATH_SENHA}").fill(senha)

        # 3) Submete o formulario
        enviado = False
        try:
            page.click("form button[type='submit']")
            enviado = True
        except Exception:
            pass
        if not enviado:
            try:
                page.click("form button")
                enviado = True
            except Exception:
                pass
        if not enviado:
            page.keyboard.press("Enter")

        # 4) Aguarda a navegacao pos-login
        page.wait_for_timeout(8000)
        try:
            page.wait_for_selector("text=/scorecard|dashboard|issues/i", timeout=15000)
        except Exception:
            print(f"[{nome}] AVISO: nao confirmou a tela inicial, seguindo mesmo assim.")

        # 5) Navega ate a pagina de issues
        url_issues = BASE_URL.format(dominio=dominio)
        page.goto(url_issues, wait_until="domcontentloaded")

        # Tempo maior de espera para a pagina de issues carregar
        page.wait_for_timeout(12000)
        try:
            page.wait_for_load_state("networkidle", timeout=20000)
        except Exception:
            pass

        # 6) Coleta a nota de score
        nota = coletar_texto(page, XPATH_NOTA)

        # 7) Extrai a tabela de issues (com fallback para texto bruto)
        blocos, texto_bruto = extrair_tabela_issues(page)

        # 8) Monta o chamado formatado
        agora = datetime.now().strftime("%d/%m/%Y %H:%M")
        total_issues = len(blocos)

        chamado = f"""
RELATORIO DE ISSUES - SECURITYSCORECARD

Cliente: {nome}
Dominio: {dominio}
Data/Hora coleta: {agora}
URL: {url_issues}

SCORE: {nota if nota else 'nao encontrado'}
Total de issues abertas: {total_issues}

"""

        if blocos:
            for i, bloco in enumerate(blocos, start=1):
                chamado += f"--- Issue {i} ---\n{bloco}\n\n"
        elif texto_bruto:
            # Fallback: tabela nao encontrada, usa o texto bruto
            chamado += "--- TEXTO BRUTO (tabela nao identificada) ---\n\n"
            chamado += texto_bruto + "\n"

        arquivo_txt = SAIDA / f"chamado_{nome}.txt"
        arquivo_txt.write_text(chamado, encoding="utf-8")

        # 9) Print geral da pagina
        arquivo_png = SAIDA / f"print_{nome}.png"
        page.screenshot(path=str(arquivo_png), full_page=True)

        browser.close()

    print(f"[{nome}] Concluido! Arquivos gerados:")
    print(f"  - {arquivo_txt}")
    print(f"  - {arquivo_png}")

def main():
    clientes = [
        ("CLIENTE_1", "CLIENTE_1_DOMINIO"),
        ("CLIENTE_2", "CLIENTE_2_DOMINIO"),
    ]
    for prefixo, chave_dominio in clientes:
        nome = os.getenv(f"{prefixo}_NOME")
        email = os.getenv(f"{prefixo}_EMAIL")
        senha = os.getenv(f"{prefixo}_SENHA")
        dominio = os.getenv(chave_dominio)
        if not all([nome, email, senha, dominio]):
            print(f"[{prefixo}] Faltando credenciais no .env, pulando.")
            continue
        coletar_cliente(nome, email, senha, dominio)

if __name__ == "__main__":
    main()

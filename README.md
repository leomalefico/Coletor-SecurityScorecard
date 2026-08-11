# Coletor SecurityScorecard

Script em Python que acessa a plataforma **SecurityScorecard**, faz login, navega até a página de **issues abertas** de um domínio e gera:
- Um arquivo `.txt` com o relatório formatado (pronto para colar em um chamado)
- Um print `.png` da página de issues

Suporta a coleta de **dois clientes diferentes** em sequência, com credenciais separadas.

---

## 📋 Pré-requisitos

- Python 3.10 ou superior
- Microsoft Edge instalado (o script usa o Edge para evitar download de navegador)
- Acesso à plataforma SecurityScorecard com credenciais válidas

---

## 🚀 Instalação

1. Clone o repositório e entre na pasta:
```bash
git clone <URL_DO_SEU_REPOSITORIO>
cd <nome_da_pasta>

---

Crie e ative um ambiente virtual (recomendado):
python -m venv venv
Windows: venv\Scripts\activate
Linux/macOS: source venv/bin/activate

---

Instale as dependências:
pip install -r requirements.txt

---

Configure as credenciais:
cp .env.example .env
Edite o .env com os dados dos dois clientes (veja a seção abaixo).

⚙️ Configuração do .envO arquivo .env guarda as credenciais dos dois clientes. Nunca suba este arquivo para o GitHub (ele está no .gitignore).Código1234567891011# ===== Cliente 1 =====
CLIENTE_1_NOME=cliente-a
CLIENTE_1_EMAIL=login@clientea.com.br
CLIENTE_1_SENHA=senha_aqui
CLIENTE_1_DOMINIO=xsite.com.br

# ===== Cliente 2 =====
CLIENTE_2_NOME=cliente-b
CLIENTE_2_EMAIL=login@clienteb.com.br
CLIENTE_2_SENHA=senha_aqui
CLIENTE_2_DOMINIO=outrodominio.com.brCampos





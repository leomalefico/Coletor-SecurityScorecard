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
Crie e ative um ambiente virtual (recomendado):
python -m venv venv
Windows: venv\Scripts\activate
Linux/macOS: source venv/bin/activate

Instale as dependências:
pip install -r requirements.txt
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
























CampoDescriçãoCLIENTE_X_NOMENome do cliente (aparece no cabeçalho do relatório e no nome dos arquivos)CLIENTE_X_EMAILE-mail de login na plataformaCLIENTE_X_SENHASenha de loginCLIENTE_X_DOMINIODomínio do scorecard (ex.: xsite.com.br)
⚠️ Importante: se um cliente não tiver todas as credenciais preenchidas, o script pula ele e segue para o próximo.
▶️ Como executarpython a_issues_scorecard.pyO script roda os dois clientes em sequência. Para cada um, gera na mesma pasta do script:
chamado_<NOME>.txt — relatório formatado com score, total de issues e cada issue em bloco
print_<NOME>.png — captura de tela da página de issues
Modo visível vs. headlessPor padrão, o script abre uma janela do Edge para você acompanhar o login (útil na primeira execução). Para rodar sem janela, altere no script:Código1234browser = p.chromium.launch(
    headless=True,   # True = sem janela
    channel="msedge"
)📁 Estrutura do projetoCódigo.
├── a_issues_scorecard.py   # script principal
├── requirements.txt        # dependências
├── .env.example            # modelo de credenciais (commitável)
├── .env                    # credenciais reais (NÃO commitar)
├── .gitignore              # ignora .env e arquivos gerados
└── README.md               # esta documentação🔧 PersonalizaçãoAlterar os seletores de loginOs XPaths dos campos de login e do score ficam como constantes no topo do script:Código123XPATH_EMAIL = "/html/body/div[2]/div/form/fieldset[1]/div[1]/p[1]/input"
XPATH_SENHA = "/html/body/div[2]/div/form/fieldset[1]/div[1]/p[2]/input"
XPATH_NOTA = "/html/body/div[3]/div/div[1]/div[1]/div[2]/div[1]/div/div/div/div[1]/div[1]/div/div/div"Se o layout da plataforma mudar, atualize esses valores.Adicionar mais clientesPara coletar um terceiro cliente, adicione as variáveis no .env e inclua a tupla em main():Código12345clientes = [
    ("CLIENTE_1", "CLIENTE_1_DOMINIO"),
    ("CLIENTE_2", "CLIENTE_2_DOMINIO"),
    ("CLIENTE_3", "CLIENTE_3_DOMINIO"),  # novo
]🛡️ Segurança
O .env com credenciais reais nunca deve ser versionado.
Use o .env.example como modelo público (sem valores reais).
Considere usar variáveis de ambiente do CI/CD (GitHub Actions, etc.) em vez de arquivos locais em ambientes compartilhados.
📄 Licença[Adicione aqui a licença do seu projeto, se aplicável.]Código
---

## Se também precisar criar o `.env.example` e o `.gitignore` no GitHub

Se esses arquivos ainda não existirem no seu repositório, você pode criá-los pela interface web:

### Criar o `.env.example`

1. Na raiz do repositório, clique em **"Add file"** → **"Create new file"**.
2. No campo de nome, digite: `.env.example`
3. Cole o conteúdo abaixo e clique em **"Commit changes"**:
```env
# ===== Cliente 1 =====
CLIENTE_1_NOME=cliente-a
CLIENTE_1_EMAIL=login@clientea.com.br
CLIENTE_1_SENHA=sua_senha_aqui
CLIENTE_1_DOMINIO=xsite.com.br

# ===== Cliente 2 =====
CLIENTE_2_NOME=cliente-b
CLIENTE_2_EMAIL=login@clienteb.com.br
CLIENTE_2_SENHA=sua_senha_aqui
CLIENTE_2_DOMINIO=outrodominio.com.brCriar o .gitignore
Clique em "Add file" → "Create new file".
No campo de nome, digite: .gitignore
Cole o conteúdo abaixo e clique em "Commit changes":
Código123456789101112# Ambientes virtuais
venv/
.env

# Arquivos gerados pelo script
chamado_*.txt
print_*.png

# Python
__pycache__/
*.py[cod]
*.egg-info/Res

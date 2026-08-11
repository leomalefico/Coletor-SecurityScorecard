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

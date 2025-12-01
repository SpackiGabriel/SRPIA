# 📚 SRPIA - Sistema de Rodízio de Papers de IA

Sistema web para ajudar estudantes e pesquisadores a **organizar e acompanhar a leitura de artigos científicos** da área de Inteligência Artificial.

##  Índice

- [💡 O que é?](#-o-que-é)
- [✨ Principais Funcionalidades](#✨-principais-funcionalidades)
- [🚀 Como Rodar o Sistema](#-como-rodar-o-sistema)
- [💡 Como Usar o Sistema](#-como-usar-o-sistema)
- [❓ Problemas Comuns](#-problemas-comuns)
- [⚡ Resumo Rápido](#-resumo-rápido---instalação-em-5-passos)

---

## 💡 O que é?

O SRPIA é um gerenciador de papers acadêmicos que:

- **Organiza seus artigos** em um só lugar
- **Sugere o que ler** baseado em prioridades e prazos
- **Acompanha seu progresso** de leitura
- **Guarda suas anotações** enquanto estuda
- **Registra tempo de estudo** dedicado a cada artigo
- **Relaciona experimentos** com os papers que você está implementando

É ideal para quem está fazendo TCC, dissertação ou simplesmente quer manter suas leituras acadêmicas organizadas!

## ✨ Principais Funcionalidades

### 📖 Gerenciamento de Papers
- Cadastre papers com título, autores, abstract, ano, DOI e arquivo PDF
- Defina prioridades (Urgente, Alta, Média, Baixa)
- Acompanhe o status (Não Iniciado, Em Leitura, Lido, Revisando)
- Organize com tags temáticas

### 🎯 Sistema de Recomendação
- O sistema sugere qual paper ler a seguir
- Leva em conta suas prioridades e prazos
- Evita recomendar o mesmo paper repetidamente

### 📝 Notas e Anotações
- Faça anotações enquanto lê
- Categorize em: Insights, Críticas, Dúvidas, Citações
- Revise suas notas depois na página do paper

### ⏱️ Controle de Tempo
- Registre sessões de leitura com duração
- Veja quanto tempo dedicou a cada paper
- Acompanhe seu histórico de estudos

### 🧪 Experimentos
- Cadastre experimentos relacionados aos papers
- Gerencie o status (Planejado, Em Execução, Concluído)
- Mantenha descrição dos datasets e resultados

### 📊 Dashboard
- Veja estatísticas dos seus papers
- Confira os próximos papers recomendados
- Acesse rapidamente as funcionalidades principais

## 🚀 Como Rodar o Sistema

### Requisitos

- Python 3.8 ou superior instalado
- Conexão com internet (para baixar dependências)

### Passo 1: Preparar o Ambiente Virtual

O ambiente virtual isola as dependências do projeto. Siga as instruções do seu sistema operacional:

#### 🐧 **Linux / macOS**

```bash
# Navegue até a pasta do projeto
cd caminho/para/trabalho-final-pdsw

# Crie o ambiente virtual
python3 -m venv venv

# Ative o ambiente virtual
source venv/bin/activate

# Você verá (venv) no início da linha do terminal
```

#### 🪟 **Windows**

```bash
# Navegue até a pasta do projeto
cd caminho\para\trabalho-final-pdsw

# Crie o ambiente virtual
python -m venv venv

# Ative o ambiente virtual
venv\Scripts\activate

# Você verá (venv) no início da linha do terminal
```

### Passo 2: Instalar Dependências

Com o ambiente virtual ativo (você verá `(venv)` no terminal):

```bash
pip install django pillow
```

### Passo 3: Configurar o Banco de Dados

```bash
# Entre na pasta do servidor
cd server

# Execute as migrações (cria as tabelas no banco)
python manage.py migrate
```

### Passo 4: Popular com Dados de Demonstração

**⭐ RECOMENDADO:** Execute este comando para criar dados de exemplo e facilitar seus primeiros passos:

```bash
python manage.py populate
```

Isso criará automaticamente:
- ✅ 7 papers importantes de IA (com títulos e abstracts em português)
- ✅ Tags temáticas organizadas
- ✅ Notas e sessões de leitura de exemplo
- ✅ 3 experimentos demonstrativos
- ✅ **Um usuário de demonstração pronto para usar**

**💡 Dica:** Use `--clear` para recriar os dados do zero:
```bash
python manage.py populate --clear
```

### Passo 5: Iniciar o Servidor

```bash
python manage.py runserver
```

Você verá uma mensagem como: `Starting development server at http://127.0.0.1:8000/`

### Passo 6: Acessar o Sistema

Abra seu navegador e acesse:

**🌐 URL:** http://localhost:8000/

**🔐 Credenciais (se você executou o populate):**
```
Usuário: demo
Senha: demo123456
```

> **Nota:** Se não executou o `populate`, você pode criar seu próprio usuário com:
> ```bash
> python manage.py createsuperuser
> ```

---

### 🎮 Comandos Úteis

```bash
# Parar o servidor
Ctrl + C (no terminal onde o servidor está rodando)

# Desativar o ambiente virtual
deactivate

# Reativar o ambiente virtual (Linux/Mac)
source venv/bin/activate

# Reativar o ambiente virtual (Windows)
venv\Scripts\activate

# Criar novo usuário manualmente (se necessário)
python manage.py createsuperuser
```

## 💡 Como Usar o Sistema

Depois de fazer login, você verá o **Dashboard** com suas estatísticas e recomendações.

### Principais Telas:

**📊 Dashboard**
- Veja quantos papers você tem em cada status
- Confira os 5 papers recomendados para ler agora
- Acesse rapidamente as funcionalidades

**📚 Lista de Papers**
- Veja todos os seus papers organizados
- Use a busca para encontrar papers específicos
- Filtre por prioridade, status, tags ou ano

**📄 Detalhes do Paper**
- Veja todas as informações do paper
- Adicione notas enquanto lê
- Registre sessões de leitura
- Acompanhe seu progresso

**🧪 Experimentos**
- Crie experimentos relacionados aos papers
- Descreva datasets e resultados
- Mantenha o código organizado com links para repositórios

## 🎨 Tecnologias

- **Framework:** Django (Python)
- **Interface:** Bootstrap 5
- **Banco de Dados:** SQLite
- **Linguagem:** Português (Brasil)

## ❓ Problemas Comuns

**"Command not found: python"**
- No Windows, tente usar `py` ao invés de `python`
- No Linux/Mac, tente `python3`

**"No module named django"**
- Certifique-se de que o ambiente virtual está ativado (veja `(venv)` no terminal)
- Execute novamente: `pip install django pillow`

**"Port already in use"**
- Outro servidor está rodando na porta 8000
- Use: `python manage.py runserver 8001` (muda para porta 8001)

## 📖 Documentação Adicional

Para mais detalhes técnicos sobre o comando `populate` e suas opções, consulte:
- `server/POPULATE_README.md`

## 🎓 Sobre o Projeto

Sistema desenvolvido para facilitar a organização e leitura de papers acadêmicos, especialmente útil para estudantes de pós-graduação, pesquisadores e alunos desenvolvendo TCC na área de IA.

---

## ⚡ Resumo Rápido - Instalação em 5 Comandos

```bash
# 1. Criar e ativar ambiente virtual
python -m venv venv
source venv/bin/activate          # Linux/Mac
# ou: venv\Scripts\activate       # Windows

# 2. Instalar dependências
pip install django pillow

# 3. Entrar na pasta do servidor e configurar banco
cd server
python manage.py migrate

# 4. (Recomendado) Popular com dados de demonstração
python manage.py populate

# 5. Iniciar o servidor
python manage.py runserver

# 6. Acessar no navegador: http://localhost:8000/
# Se executou o populate, use: demo / demo123456
```

---

**SRPIA** - Sistema de Rodízio de Papers de IA © 2024

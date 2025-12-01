# Popular Banco de Dados - SRPIA

## Comando Django: `populate`

Este comando cria dados de demonstração completos no banco de dados do SRPIA, incluindo:

- ✓ Usuário de demonstração
- ✓ Autores acadêmicos famosos (Yoshua Bengio, Geoffrey Hinton, etc.)
- ✓ Tags temáticas em português (Visão Computacional, Processamento de Linguagem Natural, etc.)
- ✓ 7 Papers importantes de IA com títulos e abstracts traduzidos para português
- ✓ Notas sobre os papers em português
- ✓ Sessões de leitura registradas em português
- ✓ 3 Experimentos em diferentes estágios com descrições em português

**Nota:** Todos os conteúdos foram traduzidos para português para facilitar a compreensão e navegação no sistema.

## Uso Básico

```bash
# Popular com configurações padrão
python manage.py populate

# Popular e limpar dados anteriores
python manage.py populate --clear

# Especificar usuário e senha customizados
python manage.py populate --username meuuser --password minhasenha123
```

## Opções Disponíveis

| Opção | Descrição | Padrão |
|-------|-----------|--------|
| `--username` | Nome do usuário a criar | `demo` |
| `--password` | Senha do usuário | `demo123456` |
| `--clear` | Limpar dados existentes do usuário antes de popular | `False` |

## Exemplos

### 1. Criar dados de demonstração básicos
```bash
python manage.py populate
```

### 2. Recriar dados (limpar e popular novamente)
```bash
python manage.py populate --clear
```

### 3. Criar com credenciais customizadas
```bash
python manage.py populate --username admin --password admin@2024
```

## Credenciais Padrão

Após executar o comando com as configurações padrão:

- **Usuário:** `demo`
- **Senha:** `demo123456`

## O que é Criado

### Papers (7)
1. **Atenção é Tudo que Você Precisa** (2017) - Status: Não Iniciado, Prioridade: Urgente
2. **Aprendizado Residual Profundo para Reconhecimento de Imagens** (2016) - Status: Em Leitura, Prioridade: Alta
3. **Redes Adversariais Generativas** (2014) - Status: Lido, Prioridade: Alta
4. **BERT: Pré-treinamento de Transformers Bidirecionais Profundos para Compreensão de Linguagem** (2019) - Status: Em Leitura, Prioridade: Urgente
5. **Jogando Atari com Aprendizado por Reforço Profundo** (2013) - Status: Não Iniciado, Prioridade: Média
6. **Classificação ImageNet com Redes Neurais Convolucionais Profundas** (2012) - Status: Lido, Prioridade: Média
7. **Dominando o Jogo de Go com Redes Neurais Profundas e Busca em Árvore** (2016) - Status: Não Iniciado, Prioridade: Baixa

### Autores (7)
- Yoshua Bengio
- Geoffrey Hinton
- Yann LeCun
- Andrew Ng
- Ian Goodfellow
- Demis Hassabis
- Fei-Fei Li

### Tags (9)
Deep Learning, Visão Computacional, Processamento de Linguagem Natural, Aprendizado por Reforço, GANs, Transformers, CNN, Mecanismos de Atenção, Transfer Learning

### Notas (6)
Insights, dúvidas e citações sobre os papers lidos

### Sessões de Leitura (6)
Registros de tempo de estudo nos papers

### Experimentos (3)
1. Classificação CIFAR-10 com ResNet (Concluído)
2. Geração de Faces com GAN (Em Execução)
3. Análise de Sentimento com BERT (Planejado)

## Notas Importantes

- ⚠️ O comando usa **transações atômicas** - se algo falhar, nada é criado
- ⚠️ Por padrão, **não sobrescreve** dados existentes
- ⚠️ Use `--clear` com cuidado em produção - remove TODOS os dados do usuário
- ✓ Seguro para executar múltiplas vezes (apenas cria novos itens)
- ✓ Ideal para desenvolvimento, testes e demonstrações

## Desenvolvimento

O comando está localizado em:
```
server/core/management/commands/populate.py
```

Para adicionar mais dados de demonstração, edite este arquivo seguindo o padrão existente.

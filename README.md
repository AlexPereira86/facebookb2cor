# Sistema de Automação Facebook Ads → B2Cor

Este documento fornece instruções detalhadas sobre como instalar e utilizar o sistema de automação para integração entre Facebook Ads e B2Cor.

## Estrutura do Projeto

O projeto está organizado em duas partes principais:

1. **Scripts de Automação** - Localizado na pasta raiz, contém os scripts Python para extração de leads do Facebook Ads e envio para o B2Cor.
2. **Interface Web** - Localizado na pasta `web_interface/`, contém uma aplicação Next.js para gerenciamento visual da integração.

## Requisitos do Sistema

### Para os Scripts de Automação:
- Python 3.8 ou superior
- Bibliotecas Python: requests, json, datetime, schedule, configparser

### Para a Interface Web:
- Node.js 14 ou superior
- NPM ou Yarn

## Instalação

### Scripts de Automação

1. Instale as dependências necessárias:
```bash
pip install requests schedule configparser
```

2. Configure as credenciais no arquivo `config.ini`:
```ini
[facebook]
app_id = SEU_APP_ID
app_secret = SEU_APP_SECRET
form_ids = ID_DO_FORMULARIO_1,ID_DO_FORMULARIO_2
days_back = 30

[b2cor]
api_key = SUA_API_KEY
default_user_id = ID_DO_USUARIO_PADRAO
default_funnel_id = ID_DO_FUNIL_PADRAO
default_stage_id = ID_DO_ESTAGIO_PADRAO
default_origin_id = ID_DA_ORIGEM_PADRAO
```

### Interface Web

1. Navegue até a pasta da interface web:
```bash
cd web_interface
```

2. Instale as dependências:
```bash
npm install
```

3. Execute o servidor de desenvolvimento:
```bash
npm run dev
```

4. Acesse a interface em `http://localhost:3000`

## Uso

### Usando os Scripts de Automação Diretamente

1. **Execução manual**:
```bash
python main.py --process
```

2. **Configuração**:
```bash
python main.py --config
```

3. **Agendamento**:
```bash
python main.py --schedule --run
```

### Usando a Interface Web

1. Acesse a interface web em `http://localhost:3000`
2. Configure as credenciais do Facebook Ads na aba "Configurações"
3. Configure as credenciais do B2Cor na aba "Configurações"
4. Configure o agendamento conforme necessário
5. Use o botão "Executar Agora" para processar leads imediatamente
6. Monitore os resultados no Dashboard

## Funcionalidades

### Scripts de Automação

- **facebook_auth.py**: Gerencia a autenticação com a API do Facebook
- **facebook_leads.py**: Extrai leads dos formulários do Facebook Ads
- **b2cor_auth.py**: Gerencia a autenticação com a API do B2Cor
- **b2cor_leads.py**: Envia leads para o B2Cor
- **main.py**: Script principal que integra todos os componentes

### Interface Web

- **Dashboard**: Visualização de estatísticas e leads recentes
- **Configuração do Facebook Ads**: Gerenciamento de credenciais e formulários
- **Configuração do B2Cor**: Gerenciamento de credenciais e opções de distribuição
- **Agendamento**: Configuração de execuções automáticas

## Solução de Problemas

### Problemas com a API do Facebook

- Verifique se o App ID e App Secret estão corretos
- Confirme que o aplicativo tem as permissões necessárias (ads_management, leads_retrieval)
- Verifique se os IDs dos formulários estão corretos

### Problemas com a API do B2Cor

- Verifique se a chave da API está correta
- Confirme que os IDs de usuário, funil, estágio e origem existem no B2Cor
- Verifique os logs para mensagens de erro específicas

## Personalização

### Personalização dos Scripts

Os scripts podem ser modificados para atender necessidades específicas:

- Altere o mapeamento de campos em `b2cor_leads.py`
- Modifique a lógica de extração em `facebook_leads.py`
- Ajuste as opções de agendamento no arquivo `main.py`

### Personalização da Interface Web

A interface web pode ser personalizada editando os arquivos em `web_interface/src/`:

- Componentes UI em `components/`
- Páginas em `app/`
- Lógica de integração em `lib/`

## Suporte

Para suporte adicional ou dúvidas, entre em contato através dos canais oficiais.

---

© 2025 Sistema de Automação Facebook Ads para B2Cor. Todos os direitos reservados.

# Notas sobre a API do B2Cor para Integração com Facebook Ads

## Informações Gerais

- **URL da API**: https://b2corapi.agencialink.com.br/
- A API do B2Cor permite que outros sistemas possam enviar informações e manipular dados existentes
- Para utilizar a API, é necessário abrir um chamado e solicitar a chave da API

## Autenticação

- Todas as requisições devem incluir o cabeçalho `x-api-key` com o valor da chave da API
- O valor deste cabeçalho é diferente para cada corretora e consiste em uma string de 32 caracteres
- Também deve ser informado o cabeçalho `Content-Type` como `application/json`

## Métodos de Requisição

- Os métodos devem ser chamados através de requisições HTTP (GET ou POST)
- Para requisições POST, os parâmetros devem estar no formato JSON no corpo da requisição
- A confirmação da execução do método é identificada pelo status da requisição HTTP:
  - Status 200: requisição executada com sucesso
  - Status 403: chave informada está errada
  - Status 400: algum valor exigido não foi informado
  - Status 405: método HTTP não aceito
  - Status 500: erro interno (verificar mensagem retornada)

## Endpoints Relevantes para Integração com Facebook Ads

### Manipulação de Leads

1. **Listar leads não exportados**
   - Endpoint: `GET /lead/listAll`
   - Retorna uma lista de leads que ainda não foram exportados

2. **Buscar leads**
   - Endpoint: `POST /lead/find`
   - Permite buscar leads com base em filtros como status, data, usuário, etc.

3. **Alterar dados de um lead existente**
   - Endpoint: `POST /lead/edit/:modelo`
   - Permite alterar dados de um lead existente
   - Modelos permitidos incluem "facebook" e "fbleads"

4. **Adicionar ao funil**
   - Endpoint: `POST /lead/addFunnel`
   - Adiciona leads a funis e estágios específicos

5. **Adicionar histórico**
   - Endpoint: `POST /lead/addHistory/:id`
   - Adiciona entradas ao histórico de um lead

6. **Atualizar lead**
   - Endpoint: `POST /lead/updateLead/:id`
   - Atualiza informações de um lead específico

## Status dos Leads

Na hora de criar um novo lead ou atualizar os status dos leads, utilize a tabela abaixo:
- '' (Vazio - Status Nova)
- Fechada
- Negociacao
- Em Visita
- Em Cotacao
- Nao Quer
- Fora Sp
- Invalida
- Repetida
- fechou_corret
- fechou_segurad
- Ligar
- mail
- renovacao
- recuperacao
- prospeccao
- vendaonline
- repassada
- perdido
- devolvido

## Tipos de Formulários

Para a integração com Facebook Ads, os tipos de formulários mais relevantes são:
- `facebook`: Facebook
- `fbleads`: Facebook Leads

Outros tipos de formulários disponíveis incluem:
- `multi_perfil`: Multi-Perfil
- `saude`: Saúde
- `saude_pme`: Saúde PME
- `saude_pj`: Saúde PJ
- `odonto`: Odonto
- `odonto_pme`: Odonto PME
- E muitos outros tipos específicos para diferentes produtos e canais

## Estrutura de Dados dos Leads

Os leads no B2Cor contêm campos como:
- `id_cliente`: Código do lead
- `data`: Data de cadastro
- `nome`: Nome do lead
- `contato`: Informações de contato
- `email`: Email do lead
- `uf`: Estado
- `cidade`: Cidade
- `fixo_ddd`: DDD do telefone fixo
- `fixo_numero`: Telefone fixo
- `celular_ddd`: DDD do telefone celular
- `celular_numero`: Telefone celular
- E outros campos específicos dependendo do tipo de lead

## Considerações para Integração com Facebook Ads

1. Ao extrair leads do Facebook Ads, será necessário mapear os campos do Facebook para os campos correspondentes no B2Cor
2. Utilizar o tipo de formulário "fbleads" ao enviar leads do Facebook para o B2Cor
3. Implementar autenticação adequada com a chave da API (x-api-key)
4. Tratar possíveis erros e status de resposta da API
5. Considerar a implementação de um mecanismo de verificação para evitar duplicação de leads

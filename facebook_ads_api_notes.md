# Notas sobre a API do Facebook Ads para Extração de Leads

## Métodos de Extração de Leads

Existem dois métodos principais para extrair leads do Facebook Ads:

1. **Webhooks** - Para atualizações em tempo real
2. **Bulk Read** - Para leitura em massa de leads

## Requisitos de Autenticação e Permissões

### Para ler campos específicos de anúncios (ad_id, campaign_id):

- Token de acesso de Página ou Usuário solicitado por uma pessoa que pode anunciar na conta de anúncios e na Página
- Permissão `ads_management`
- Permissão `pages_read_engagement`
- Permissão `pages_show_list`
- Permissão `pages_manage_metadata` (se estiver usando webhooks)

### Para ler todos os dados de leads e dados de nível de anúncio:

- Token de acesso de Página ou Usuário solicitado por uma pessoa que pode anunciar na conta de anúncios e na Página
- Permissão `ads_management`
- Permissão `leads_retrieval`
- Permissão `pages_show_list`
- Permissão `pages_read_engagement`
- Permissão `pages_manage_ads`

## Configuração de Webhooks

1. **Passo 1: Começar**
   - Configurar endpoint e configurar webhook usando o guia "Webhooks Get Started"

2. **Passo 2: Obter um Token de Acesso de Página de Longa Duração**
   - Gerar um token de página de longa duração para buscar dados continuamente sem se preocupar com expiração

3. **Passo 3: Instalar seu Aplicativo na Página**
   - Seguir o guia "Webhooks for Pages" para aprender como instalar o aplicativo em uma Página

4. **Resposta do Webhook**
   - Ao criar um lead, o aplicativo recebe uma resposta webhook com detalhes como leadgen_id, page_id, form_id, adgroup_id, ad_id e created_time
   - O leadgen_id pode ser usado para recuperar dados associados ao lead

## Leitura em Massa (Bulk Read)

- Aplicativos criados após 2 de julho de 2018 são obrigados a usar a permissão `leads_retrieval` para ler leads
- O endpoint `leads` existe em nós de grupo de anúncios e formulários
- Um formulário pode ser reutilizado para muitos anúncios, portanto pode conter muito mais leads do que um único anúncio

### Exemplos de Código para Leitura em Massa:

#### Leitura por anúncio:
```
curl -X GET \
  -d 'access_token=<ACCESS_TOKEN>' \
  https://graph.facebook.com/v22.0/{adgroup-id}/leads
```

#### Leitura por formulário:
```
curl -G \
  -d 'access_token=<ACCESS_TOKEN>' \
  -d 'fields=created_time,id,ad_id,form_id,field_data' \
  https://graph.facebook.com/<API_VERSION>/<FORM_ID>/leads
```

## Filtragem por Data

É possível filtrar leads por intervalo de data usando o endpoint `/ads/lead_gen/export_csv/` com parâmetros como:
```
curl -i -X GET "https://www.facebook.com/ads/lead_gen/export_csv/
  ?id=<FORM_ID>
  &type=form
  &from_date=1482698431
  &to_date=1482784831"
```

## Formato de Resposta

A resposta da API inclui dados como:
- created_time
- id (lead_id)
- ad_id
- form_id
- field_data (contendo os dados do formulário como nome, email, etc.)

## Limitações

- O limite de taxa é 200 multiplicado por 24 multiplicado pelo número de leads criados nos últimos 90 dias para uma Página do Facebook
- Se você fizer mais chamadas do que isso em um período de 24 horas, sua solicitação retornará um erro
- Pings em tempo real ocorrem em eventos com um atraso de até alguns minutos

## Recursos Adicionais

- Muitos CRMs fornecem atualizações em tempo real para migrar dados de leads para os CRMs
- Existe um repositório GitHub com exemplos de implementação
- Há guias de solução de problemas para integrações em tempo real

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Sistema de Automação para Integração entre Facebook Ads e B2Cor
Este script integra a extração de leads do Facebook Ads e o envio para o B2Cor.
"""

import os
import sys
import json
import argparse
import logging
import time
import schedule
from datetime import datetime, timedelta

# Importa os módulos criados
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from scripts.facebook_auth import FacebookAdsAuth
from scripts.facebook_leads import FacebookLeadsExtractor
from scripts.b2cor_auth import B2CorAuth
from scripts.b2cor_leads import B2CorLeadsSender

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("facebook_b2cor_automation.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("facebook_b2cor_automation")

class FacebookB2CorIntegration:
    """
    Classe para integrar a extração de leads do Facebook Ads e o envio para o B2Cor
    """
    
    def __init__(self, config_file=None):
        """
        Inicializa a integração
        
        Args:
            config_file (str): Caminho para o arquivo de configuração (opcional)
        """
        self.config_file = config_file or os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json')
        self.config = self._load_config()
        
        # Inicializa os componentes
        self.facebook_auth = None
        self.facebook_extractor = None
        self.b2cor_auth = None
        self.b2cor_sender = None
        
        # Diretório para armazenar os leads extraídos
        self.leads_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'leads')
        os.makedirs(self.leads_dir, exist_ok=True)
    
    def _load_config(self):
        """
        Carrega a configuração do arquivo ou cria uma configuração padrão
        
        Returns:
            dict: Configuração carregada
        """
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                logger.error(f"Erro ao carregar arquivo de configuração: {self.config_file}")
                return self._create_default_config()
        else:
            return self._create_default_config()
    
    def _create_default_config(self):
        """
        Cria uma configuração padrão
        
        Returns:
            dict: Configuração padrão
        """
        return {
            "facebook": {
                "form_ids": [],
                "ad_ids": [],
                "days_back": 30,
                "schedule": {
                    "enabled": False,
                    "interval": "daily",
                    "time": "00:00"
                }
            },
            "b2cor": {
                "add_to_funnel": True,
                "change_user": True,
                "add_history": True
            },
            "general": {
                "auto_process": True,
                "keep_leads_days": 30
            }
        }
    
    def _save_config(self):
        """
        Salva a configuração atual no arquivo
        """
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=4)
        logger.info(f"Configuração salva em: {self.config_file}")
    
    def setup(self):
        """
        Configura os componentes da integração
        
        Returns:
            bool: True se a configuração foi bem-sucedida
        """
        try:
            # Configura a autenticação do Facebook
            logger.info("Configurando autenticação do Facebook Ads...")
            self.facebook_auth = FacebookAdsAuth()
            
            if not self.facebook_auth.verify_token():
                logger.info("Token do Facebook Ads não encontrado ou inválido. Iniciando processo de autenticação...")
                if not self.facebook_auth.interactive_auth():
                    logger.error("Falha na autenticação do Facebook Ads.")
                    return False
            
            # Configura o extrator de leads do Facebook
            logger.info("Configurando extrator de leads do Facebook Ads...")
            self.facebook_extractor = FacebookLeadsExtractor(self.facebook_auth)
            
            # Configura a autenticação do B2Cor
            logger.info("Configurando autenticação do B2Cor...")
            self.b2cor_auth = B2CorAuth()
            
            if not self.b2cor_auth.verify_api_key():
                logger.info("Chave da API do B2Cor não encontrada ou inválida. Iniciando processo de configuração...")
                if not self.b2cor_auth.interactive_setup():
                    logger.error("Falha na configuração do B2Cor.")
                    return False
            
            # Configura o enviador de leads para o B2Cor
            logger.info("Configurando enviador de leads para o B2Cor...")
            self.b2cor_sender = B2CorLeadsSender(self.b2cor_auth)
            
            logger.info("Configuração concluída com sucesso!")
            return True
        
        except Exception as e:
            logger.error(f"Erro durante a configuração: {str(e)}")
            return False
    
    def extract_leads(self):
        """
        Extrai leads do Facebook Ads
        
        Returns:
            str: Caminho para o arquivo de leads extraídos ou None em caso de erro
        """
        try:
            if not self.facebook_extractor:
                logger.error("Extrator de leads do Facebook não configurado. Execute setup() primeiro.")
                return None
            
            # Define o nome do arquivo de saída
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = os.path.join(self.leads_dir, f"facebook_leads_{timestamp}.json")
            
            # Extrai os leads
            logger.info("Extraindo leads do Facebook Ads...")
            form_ids = self.config.get('facebook', {}).get('form_ids', [])
            ad_ids = self.config.get('facebook', {}).get('ad_ids', [])
            days_back = self.config.get('facebook', {}).get('days_back', 30)
            
            # Se não houver IDs específicos configurados, lista os formulários disponíveis
            if not form_ids and not ad_ids:
                logger.info("Nenhum formulário ou anúncio específico configurado. Listando formulários disponíveis...")
                forms = self.facebook_extractor.get_forms()
                form_ids = [form.get('id') for form in forms]
                logger.info(f"Encontrados {len(form_ids)} formulários para extração.")
            
            # Extrai os leads
            num_leads = self.facebook_extractor.extract_leads_to_json(
                output_file,
                form_ids=form_ids,
                ad_ids=ad_ids,
                days_back=days_back
            )
            
            if num_leads > 0:
                logger.info(f"Extraídos {num_leads} leads para {output_file}")
                return output_file
            else:
                logger.warning("Nenhum lead extraído.")
                return None
        
        except Exception as e:
            logger.error(f"Erro durante a extração de leads: {str(e)}")
            return None
    
    def send_leads(self, leads_file):
        """
        Envia leads para o B2Cor
        
        Args:
            leads_file (str): Caminho para o arquivo de leads
            
        Returns:
            dict: Estatísticas de processamento ou None em caso de erro
        """
        try:
            if not self.b2cor_sender:
                logger.error("Enviador de leads para o B2Cor não configurado. Execute setup() primeiro.")
                return None
            
            if not leads_file or not os.path.exists(leads_file):
                logger.error(f"Arquivo de leads não encontrado: {leads_file}")
                return None
            
            # Envia os leads
            logger.info(f"Enviando leads para o B2Cor a partir de {leads_file}...")
            add_to_funnel = self.config.get('b2cor', {}).get('add_to_funnel', True)
            change_user = self.config.get('b2cor', {}).get('change_user', True)
            add_history = self.config.get('b2cor', {}).get('add_history', True)
            
            stats = self.b2cor_sender.process_facebook_leads(
                leads_file,
                add_to_funnel=add_to_funnel,
                change_user=change_user,
                add_history=add_history
            )
            
            logger.info(f"Envio concluído. Total: {stats.get('total', 0)}, Sucesso: {stats.get('success', 0)}, Falha: {stats.get('failed', 0)}, Pulados: {stats.get('skipped', 0)}")
            return stats
        
        except Exception as e:
            logger.error(f"Erro durante o envio de leads: {str(e)}")
            return None
    
    def process(self):
        """
        Processa a integração completa: extrai leads e envia para o B2Cor
        
        Returns:
            bool: True se o processamento foi bem-sucedido
        """
        try:
            # Verifica se os componentes estão configurados
            if not self.facebook_extractor or not self.b2cor_sender:
                logger.error("Componentes não configurados. Execute setup() primeiro.")
                return False
            
            # Extrai os leads
            leads_file = self.extract_leads()
            
            if not leads_file:
                logger.warning("Nenhum lead extraído ou erro durante a extração.")
                return False
            
            # Envia os leads
            stats = self.send_leads(leads_file)
            
            if not stats:
                logger.error("Erro durante o envio de leads.")
                return False
            
            # Limpa arquivos antigos
            self._cleanup_old_files()
            
            return True
        
        except Exception as e:
            logger.error(f"Erro durante o processamento: {str(e)}")
            return False
    
    def _cleanup_old_files(self):
        """
        Limpa arquivos de leads antigos
        """
        try:
            keep_days = self.config.get('general', {}).get('keep_leads_days', 30)
            cutoff_date = datetime.now() - timedelta(days=keep_days)
            
            for filename in os.listdir(self.leads_dir):
                file_path = os.path.join(self.leads_dir, filename)
                
                # Pula diretórios
                if os.path.isdir(file_path):
                    continue
                
                # Verifica a data de modificação do arquivo
                file_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                
                if file_time < cutoff_date:
                    os.remove(file_path)
                    logger.info(f"Arquivo antigo removido: {file_path}")
        
        except Exception as e:
            logger.error(f"Erro durante a limpeza de arquivos antigos: {str(e)}")
    
    def schedule_job(self):
        """
        Agenda a execução periódica da integração
        
        Returns:
            bool: True se o agendamento foi bem-sucedido
        """
        try:
            schedule_config = self.config.get('facebook', {}).get('schedule', {})
            
            if not schedule_config.get('enabled', False):
                logger.info("Agendamento desativado na configuração.")
                return False
            
            interval = schedule_config.get('interval', 'daily')
            time_str = schedule_config.get('time', '00:00')
            
            if interval == 'daily':
                schedule.every().day.at(time_str).do(self.process)
                logger.info(f"Integração agendada para execução diária às {time_str}")
            elif interval == 'hourly':
                schedule.every().hour.do(self.process)
                logger.info("Integração agendada para execução horária")
            elif interval == 'weekly':
                schedule.every().week.at(time_str).do(self.process)
                logger.info(f"Integração agendada para execução semanal às {time_str}")
            else:
                logger.error(f"Intervalo de agendamento não reconhecido: {interval}")
                return False
            
            return True
        
        except Exception as e:
            logger.error(f"Erro durante o agendamento: {str(e)}")
            return False
    
    def run_scheduled_jobs(self):
        """
        Executa os jobs agendados
        """
        logger.info("Iniciando execução de jobs agendados...")
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Verifica a cada minuto
        except KeyboardInterrupt:
            logger.info("Execução de jobs agendados interrompida pelo usuário.")
        except Exception as e:
            logger.error(f"Erro durante a execução de jobs agendados: {str(e)}")
    
    def interactive_config(self):
        """
        Configuração interativa da integração
        
        Returns:
            bool: True se a configuração foi bem-sucedida
        """
        print("\n=== Configuração da Integração Facebook Ads -> B2Cor ===")
        
        # Configuração do Facebook
        print("\n== Configuração do Facebook Ads ==")
        
        # Formulários
        use_forms = input("Deseja especificar IDs de formulários? (s/n): ").lower() == 's'
        if use_forms:
            form_ids_str = input("IDs dos formulários (separados por vírgula): ")
            form_ids = [form_id.strip() for form_id in form_ids_str.split(',') if form_id.strip()]
            self.config['facebook']['form_ids'] = form_ids
        else:
            self.config['facebook']['form_ids'] = []
        
        # Anúncios
        use_ads = input("Deseja especificar IDs de anúncios? (s/n): ").lower() == 's'
        if use_ads:
            ad_ids_str = input("IDs dos anúncios (separados por vírgula): ")
            ad_ids = [ad_id.strip() for ad_id in ad_ids_str.split(',') if ad_id.strip()]
            self.config['facebook']['ad_ids'] = ad_ids
        else:
            self.config['facebook']['ad_ids'] = []
        
        # Dias para trás
        days_back_str = input("Número de dias para trás para buscar leads (padrão: 30): ")
        if days_back_str.strip() and days_back_str.isdigit():
            self.config['facebook']['days_back'] = int(days_back_str)
        else:
            self.config['facebook']['days_back'] = 30
        
        # Agendamento
        use_schedule = input("Deseja agendar a execução automática? (s/n): ").lower() == 's'
        self.config['facebook']['schedule']['enabled'] = use_schedule
        
        if use_schedule:
            interval = input("Intervalo (daily, hourly, weekly) [daily]: ").lower()
            if interval in ['daily', 'hourly', 'weekly']:
                self.config['facebook']['schedule']['interval'] = interval
            else:
                self.config['facebook']['schedule']['interval'] = 'daily'
            
            if interval != 'hourly':
                time_str = input("Horário (HH:MM) [00:00]: ")
                if time_str.strip():
                    self.config['facebook']['schedule']['time'] = time_str
                else:
                    self.config['facebook']['schedule']['time'] = '00:00'
        
        # Configuração do B2Cor
        print("\n== Configuração do B2Cor ==")
        
        self.config['b2cor']['add_to_funnel'] = input("Adicionar leads ao funil padrão? (s/n) [s]: ").lower() != 'n'
        self.config['b2cor']['change_user'] = input("Alterar responsável para o usuário padrão? (s/n) [s]: ").lower() != 'n'
        self.config['b2cor']['add_history'] = input("Adicionar histórico padrão? (s/n) [s]: ").lower() != 'n'
        
        # Configuração geral
        print("\n== Configuração Geral ==")
        
        self.config['general']['auto_process'] = input("Processar automaticamente após a configuração? (s/n) [s]: ").lower() != 'n'
        
        keep_days_str = input("Número de dias para manter arquivos de leads (padrão: 30): ")
        if keep_days_str.strip() and keep_days_str.isdigit():
            self.config['general']['keep_leads_days'] = int(keep_days_str)
        else:
            self.config['general']['keep_leads_days'] = 30
        
        # Salva a configuração
        self._save_config()
        print("\nConfiguração concluída com sucesso!")
        
        return True

def main():
    """
    Função principal para uso em linha de comando
    """
    parser = argparse.ArgumentParser(description='Integração Facebook Ads -> B2Cor')
    parser.add_argument('--config', action='store_true', help='Configurar a integração interativamente')
    parser.add_argument('--setup', action='store_true', help='Configurar autenticação e componentes')
    parser.add_argument('--extract', action='store_true', help='Extrair leads do Facebook Ads')
    parser.add_argument('--send', metavar='FILE', help='Enviar leads para o B2Cor a partir de um arquivo')
    parser.add_argument('--process', action='store_true', help='Processar a integração completa')
    parser.add_argument('--schedule', action='store_true', help='Agendar a execução periódica')
    parser.add_argument('--run', action='store_true', help='Executar jobs agendados')
    
    args = parser.parse_args()
    
    # Cria a instância da integração
    integration = FacebookB2CorIntegration()
    
    # Configuração interativa
    if args.config:
        integration.interactive_config()
    
    # Configuração de autenticação e componentes
    if args.setup or args.extract or args.process or args.schedule or args.run:
        if not integration.setup():
            logger.error("Falha na configuração. Abortando.")
            return
    
    # Extração de leads
    if args.extract:
        leads_file = integration.extract_leads()
        if leads_file:
            print(f"Leads extraídos para: {leads_file}")
    
    # Envio de leads
    if args.send:
        stats = integration.send_leads(args.send)
        if stats:
            print(f"Envio concluído. Total: {stats.get('total', 0)}, Sucesso: {stats.get('success', 0)}, Falha: {stats.get('failed', 0)}, Pulados: {stats.get('skipped', 0)}")
    
    # Processamento completo
    if args.process:
        if integration.process():
            print("Processamento concluído com sucesso!")
        else:
            print("Erro durante o processamento.")
    
    # Agendamento
    if args.schedule:
        if integration.schedule_job():
            print("Agendamento configurado com sucesso!")
        else:
            print("Erro durante o agendamento.")
    
    # Execução de jobs agendados
    if args.run:
        integration.run_scheduled_jobs()
    
    # Processamento automático após configuração
    if args.config and integration.config.get('general', {}).get('auto_process', True):
        print("\nIniciando processamento automático...")
        if not integration.setup():
            logger.error("Falha na configuração. Abortando processamento automático.")
            return
        
        if integration.process():
            print("Processamento automático concluído com sucesso!")
        else:
            print("Erro durante o processamento automático.")
        
        # Agenda se configurado
        if integration.config.get('facebook', {}).get('schedule', {}).get('enabled', False):
            if integration.schedule_job():
                print("Agendamento configurado com sucesso!")
                print("Pressione Ctrl+C para interromper a execução de jobs agendados.")
                integration.run_scheduled_jobs()

if __name__ == "__main__":
    main()

import os
import re
import subprocess
import time
from pyzabbix import ZabbixMetric, ZabbixSender
from ast import literal_eval
import requests

bot_token = "TELEGRAM BOT TOKEN"
chat_id = "TELEGRAM BOT CHAT ID"

response = subprocess.Popen('/usr/local/bin/speedtest-cli --simple', shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8')

#ping = re.findall('Ping:\s(.*?)\s', response, re.MULTILINE)
download = re.findall('Download:\s(.*?)\s', response, re.MULTILINE)
upload = re.findall('Upload:\s(.*?)\s', response, re.MULTILINE)

#ping = ping[0].replace(',', '.')
download = download[0].replace(',', '.')
upload = upload[0].replace(',', '.')

pacote = [ZabbixMetric('127.0.0.1','nettestd',download),
	  ZabbixMetric('127.0.0.1','nettestu',upload)]

resultado = ZabbixSender(use_config=True).send(pacote)

print(resultado)

teste = literal_eval(str(resultado))
qtdErros = int(teste["failed"])

if qtdErros > 0:
    mensagem = "Ocorreu um erro ao enviar as chaves nettestd e nettestu para o zabbix via zabbix_sender!%0A" +  str(resultado)
    response = requests.get("https://api.telegram.org/bot" + bot_token + "/sendMessage?text=" + mensagem + "&chat_id" + chat+id)

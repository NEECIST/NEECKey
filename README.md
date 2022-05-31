# NEECKey
## Ligar o raspberry
Ao ligar esperar por volta de 45 segundos antes de colocar as chaves para o programa começar a correr e ter tempo de calibrar

## Aceder ao raspberry (caso esteja ligado à internet)
```
ssh pi@raspberrypi.local  
```
password default: 
```
raspberry
```

## Setup do código

Instalar as dependências com 
```
pip3 install -r requirements.txt
```

## Pôr o script a correr quando o raspberry liga
1. Criar um servico systemctl
``` 
sudo systemctl --force --full edit NEECKeys.service
```

2. Editar o ficheiro que aparece com 
``` 
[Unit]
Description=<NEECKeys>
After=network.target

[Service]
User=pi
ExecStart=/usr/bin/python3 /home/pi/Documents/NEECKey/chaves.py

[Install]
WantedBy=multi-user.target
```
Não esquecer de colocar os caminhos certos tanto para o interpretador de python como o script

3. Reiniciar o deamon do systemctl
```
sudo systemctl daemon-reload
```

4. Ativar autostart quando o raspberry liga
```
sudo systemctl enable NEECKeys.service
```


Outros comandos uteis
```
sudo systemctl stop NEECKeys.service #parar
sudo systemctl restart NEECKeys.service #para dar restart do servico
sudo systemctl status NEECKeys.service #para ver o estado
```


## Montagem
![alt text](https://media.discordapp.net/attachments/621808194435547158/935479303162957844/IMG_20220125_100006.jpg?width=819&height=614)  
![alt text](https://media.discordapp.net/attachments/621808194435547158/935479303750164520/IMG_20220125_100000.jpg?width=819&height=614)  
![alt text](https://media.discordapp.net/attachments/621808194435547158/935479304274460753/IMG_20220125_095957.jpg?width=819&height=614)  

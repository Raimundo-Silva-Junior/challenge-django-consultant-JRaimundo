# Challenge Django Consultant
## Iniciar aplicativo
É necessário ter o docker instalado para iniciar o aplicativo. Antes de mais nada, inicie o daemon do docker com o commando:

- sudo service docker start  (wsl)
  
  ou
  
- sudo systemctl start docker

Depois basta aplicar um docker-compose na pasta do projeto

- docker-compose up --build

Será iniciado os servidores django, flet, celery e redis.

## Endereço do aplicativo web
Abaixo estão os endereços do frontend e da API.
- http://localhost:7000  (Fronend)
- http://localhost:8000  (API)

## Credenciais
Para entrar na área de ADM é necessário possuir as credenciais. O projeto foi feito pra iniciar essas credenciais de forma automática.
As credenciais são as seguintes:
- Usuário: admin
- Senha: raimu123

## Detalhes do aplicativo
A API do aplicativo foi feito usando django_restframework. Para gerar os tokens para logar como adm foi usado o rest_framework_simplejwt. Na parte de frontend escolhi um framework
novo em Python chamado Flet. Esse framework é moderno e usa como base Flutter, que atualmente é bastante usado para fazer projetos multiplataforma.

## Observações

a Versão do docker-compose da minha máquina é 2, mas caso dê algum erro, basta alterar para a versão do seu docker-compose ou excluir a versão do arquivo.


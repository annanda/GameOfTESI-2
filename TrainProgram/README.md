# Game of Annotation
Autores: Guilherme Freire e Hugo Gomes

O objetivo desse programa é ajudar na anotação manual de Entidades Nomeadas. 
Como corpus usa-se arquivos retirados da [wiki do Game of Thrones](http://gameofthrones.wikia.com/wiki/Game_of_Thrones_Wiki).
Esses arquivos foram pré-processados e encontram-se no diretório ```DataBase/EpisodesTXT```

## Como rodar o programa
* Crie um virtual env com python 3 
```
python3 -m venv nome_virtual_env
``` 
* Ative o virtual env criado
```
source nome_virtual_env/bin/activate
``` 
* Instale as dependências
```
pip install -r ../requirements.txt
```
* Faça um fork nesse repositório
* Faça um clone do seu fork e baixe o código
* Depois de baixado o código abra o diretório ```TrainProgram``` e rode o arquivo ```main.py```

## Como colaborar
* Mande um email para hugodovs@hotmail.com dizendo que você quer colaborar, ele vai te falar em qual arquivo você vai trabalhar
* Rode o programa clique em "Choose File"
* Clique no arquivo do episódio que você vai marcar, que fica no diretório ```DataBase/EpisodesTXT```
* Vai aparecer uma lista de pedaços do episódio que precisam ser marcadas, escolha uma parte e clique "OK"
* Na coluna à esquerda selecione a Entidade Nomeada
* Na coluna do meio escolha qual o tipo de entidade Nomeada (Person, Location, Organization, Other) 
* Clique em "Add NE"
* Se a Entidade Nomeada tiver mais que um nome, selecione os nomes com CTRL pressionado. 
* Salve o arquivo em formato outputFILE.txt
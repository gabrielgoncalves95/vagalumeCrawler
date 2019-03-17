# Vagalume Crawler

Script para fazer o download de todas as músicas de um determinado gênero musical de um idioma específico do site de músicas <www.vagalume.com.br>. Esse script foi criado para gerar bases de dados para utilização em modelos de Deep Learning para processamento textual. O próprio script já faz uma série de tratamentos na escrita do texto para que ele seja salvo da forma mais limpa possível. 

## Ambiente e Bibliotecas

### Python 3.6+

*  BeautifulSoup 4.6.1

```
    pip install beautifulsoup4==4.6.1
```
* nltk 3.3+
```
    pip install -U nltk
```
* requests 2.18.4
```
    pip install requests==2.18.4
```

## Execução

Abra o terminal (caso esteja usando pyenv ou similar ative o environment) e execute o comando no formato exemplificado a seguir:

```
    python vagalumeCrawler.py www.vagalume.com.br/browse/style/pop.html portuguese
```
Qualquer gênero musical pode ser utilizado, basta trocar a url do exemplo pela url do gênero desejado.

As opções de idioma detectadas pelo script são:

* spanish
* english
* italian
* portuguese
* french

Os arquivos baixados serão colocados dentro de uma pasta "Artistas" contendo um arquivo *.txt com o nome de cada artista do gênero escolhido e com todas as músicas que atendam ao idioma escolhido concatenadas nesse arquivo.

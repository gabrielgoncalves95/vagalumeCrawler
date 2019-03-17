# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
from collections import deque
import nltk
import time
import sys
import os


# 'www.vagalume.com.br/browse/style/pop.html'
url = sys.argv[1]
lang_option = sys.argv[2]

try:
    os.system("mkdir Artistas")
except:
    pass

r  = requests.get("http://" +url)

data = r.text

soup = BeautifulSoup(data)
artistas = deque([])

contador = 0

def detecta_idioma(texto_para_detectar: str):
    languages = ["spanish","english","italian","portuguese","french"]
    tokens = nltk.tokenize.word_tokenize(texto_para_detectar)
    tokens = [t.strip().lower() for t in tokens]
    lang_count = {}

    for lang in languages:
        stop_words = nltk.corpus.stopwords.words(lang)
        lang_count[lang] = 0

        for word in tokens:
            if word in stop_words:
                lang_count[lang] += 1

    return max(lang_count, key=lang_count.get)


def space_replace(texto: str, item :str):
    texto = texto.replace(item, " ")

    return texto

    
#OBTENÇÃO DA LISTA DE ARTISTAS
saved = ""
for link in soup.find_all('a'):
    artistas.append(link.get('href'))

for i in range(0, len(artistas)):
    if (artistas.pop() == '/browse/hotspots/'):
        break

for name in artistas:
    if (name.find('.html') != -1):
        saved = name

for i in range(0, len(artistas)):
    artist = artistas.popleft()
    if (artist.find(saved) != -1):        
        break

flag = 0
for links in artistas:
    if links == "/slow-club/":
        flag = 1
    if flag == 0:
        continue
    print("############ ARTISTA: " + str(links))
    url = 'www.vagalume.com.br'
    a = requests.get("http://" + url + str(links))
    data = a.text
    soup = BeautifulSoup(data)
    songs = deque([])
    file_name = links.replace(".html","")    
    file_name = file_name.replace("-", "")
    file_name = file_name.replace("/", "")
    arquivo = open("Artistas/" + file_name + '.txt', 'w')

    for link in soup.find_all('a'):
        songs.append(link.get('href'))
    for i in range(0, len(songs)):
        song = songs.pop()
        if (song.find(links)!=-1):        
            songs.append(song)
    for i in range(0, len(songs)):
        song = songs.popleft()
        if (song.find(links)!=-1):        
            songs.append(song)

    remove=[]
    for i in range(0, len(songs)):
        song = songs[i]
        if (song.find('#play')!=-1): 
            remove.append(songs[i])
    
    for i in range(0, len(remove)):
        songs.remove(remove[i])
    
    remove.clear()

    for i in range(0, len(songs)):
        song = songs[i]
        if (song.find('traducao')!=-1): 
            remove.append(songs[i])

    for i in range(0, len(remove)):
        songs.remove(remove[i])

    remove.clear()


    for i in range(0, len(songs)):
        song = songs[i]
        if (song.find('cifrada')!=-1): 
            remove.append(songs[i])

    for i in range(0, len(remove)):
        songs.remove(remove[i])

    remove.clear()

    for i in range(0, int(len(songs)/2)):
        song = songs[i]
        if (song.find('/news/')!=-1): 
            remove.append(i)
        if (song.find('/tags/')!=-1): 
            remove.append(i)
        if (song.find('/popularidade/')!=-1): 
            remove.append(i)
        if (song.find('/fotos/')!=-1): 
            remove.append(i)

    try:
        index = max(remove, key=int)
    except:
        index = 0

    for i in range(0, index + 1):
        try:
            del songs[0]
        except:
            continue

    remove.clear()

    for i in range(int(len(songs)/2), int(len(songs))):

        song = songs[i]
        if (song.find('/news/')!=-1): 
            remove.append(i)
        if (song.find('/fotos/')!=-1): 
            remove.append(i)
        if (song.find('/popularidade/')!=-1): 
            remove.append(i)
        if (song.find('/discografia/')!=-1): 
            remove.append(i)

    try:
        index = min(remove, key=int)
    except:
        index = len(songs)

    for i in range(index, len(songs)):
        try:
            del songs[len(songs)-1]

        except:
            continue
    

    for musica in songs:
        print("[x] " + str(musica))
        s = requests.get("http://" + url + str(musica))
        contador = contador + 1
        
        if contador > 200:
            time.sleep(60)
            contador = 0 

        data = s.text
        soup = BeautifulSoup(data)
        letras = deque([])
        letra = soup.find("div", id="lyrics")
        try:
            texto = str(letra.get_text(separator="\n"))
        except:
            continue

        char_list_to_nothing = ["{refrão}", "(2x)", "(3x)", "(1x)", "(4x)", "?", "!", ",", ".", ":", "(2 vezes)", "(1ª vez)", "(2ª vez)", "(", ")", "[", "]", "/", "'", '"', "[cr]",
                     "[repete tudo]", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "--", "_"]
       
        for item in char_list_to_nothing:
            texto = space_replace(texto, item)
        
        '''if texto.find("Ã§")!=-1 or texto.find("Ã£")!=-1 or texto.find("Ã³")!=-1 or texto.find("Ã©")!=-1 or texto.find("Ã´")!=-1 or texto.find("Ã§Ã£")!=-1 or texto.find("Ãª")!=-1 or texto.find("Ã­-")!=-1:
            print(texto)
            continue
        '''
        

        char_list_to_space = ["  ", "   ", "    ", "     ", "      ", " x "]

        for item in char_list_to_space:
            texto = space_replace(texto, item)

        texto = texto.replace("noix", "nós")
        texto = texto.replace("vc", "você")
        texto = texto + '\n'
        idioma = detecta_idioma(texto)
        
        if(idioma != lang_option):
            print("Erro: idioma inválido - letra descartada\n")
            continue
        try:
            arquivo.write(str(texto))
        except:
            print("Encoding problemático - letra descartada\n")

    #print(songs)
    arquivo.close()

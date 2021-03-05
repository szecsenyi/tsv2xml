#!/usr/bin/env python
# coding: utf-8

# # tsv2xml.py
# ver 1.01 05-03-2021  
# (c) Szécsényi Tibor 2020  
# TAB szeparált szövegfájlt XML fájllá alakít

# ## Környezeti változók
# Ezeket lehet módosítani itt, vagy külső paraméterrel

# In[ ]:


inputFileName = 'input.tsv' 
# a feldolgozandó .tsv fájl neve

outputFileName = 'output.xml' 
# a kimeneti .xml fájl neve

rootTag = 'tsv2xml' 
# ez lesz az XML fájl root tagje

sentenceTag = 's' 
# a TSV fájl üres sorait mondatkezdésnek tekinti a program,
# és a mondatok lesznek az XML root leányai, ezzel a címkével

wordTag = 'w'
# a TSV fájl sorai szónak tekinti a program,
# amik a mondat leányai lesznek, ezzel a címkével

dropChar = '_'
# az ilyen értékkel nem történik semmi, hiányzó adat

idPrefix = 's'
# a mondat tagek ID attribútumai ezzel a kifejezéssel kezdődnek,
# majd a mondat sorszámával folytatódnak, pl: s12

sIDStart=1
# az első mondat sorszáma

wSep = 'w'
# ha a szavak is kapnak azonosítót, akkor a mondat azonosítója után
# ez az elválasztó következik, majd a szó mondatbeli azonosítója (sorszáma?)
# pl: s12w7

mtSep = '|'
# ha a TSV fájlban ilyen karaktert tartalmazó kifejezés található,
# akkor a kifejezés ezen elválasztó mentén szétvágható részekre

faSep = '='
# és a szétvágott részek továbbszeletelődnek ezzel két részre
# pl1: 'foo1=bar1|foo2=bar2' -> <w><foo1>bar1</foo1><foo2>bar2</foo2></w>
# pl2: 'foo1=bar1|foo2=bar2' -> <w foo1="bar1" foo2="bar2" />


# ## Használt könyvtárak

# In[ ]:


import sys
from xml.dom import minidom


# ## Parancssori argumentumok
# Ha parancssorból futtatjuk a programot, a környezeti változók 
# paraméterekként is beállíthatók/módosíthatók  
# pl: `python tsv2xml.py input=mlanc01.txt output="mlanc01.xml" idpfx=f01`  
# `python tsv2xml.py -?` paraméterrel leírja a használatot

# In[ ]:


tagsInline = True

for anArg in sys.argv:
    if anArg.find('=') != -1:
        [at,val] = anArg.split('=')
        if at == 'input':
            inputFileName = val.strip('"')
        elif at == 'output':
            outputFileName = val.strip('"')
        elif at == 'root':
            rootTag = val.strip('"')
        elif at == 'stag':
            sentenceTag = val.strip('"')
        elif at == 'idstart':
            sIDStart = int(val.strip('"'))
        elif at == 'wtag':
            wordTag = val.strip('"')
        elif at == 'drop':
            dropChar = val.strip('"')
        elif at == 'idpfx':
            idPrefix = val.strip('"')
        elif at == 'wpfx':
            wSep = val.strip('"')
        elif at == 'split':
            mtSep = val.strip('"')
        elif at == 'attr':
            faSep = val.strip('"')
        elif at == 'tagdef':
            inputFile = open(val.strip('"'), 'r', encoding='utf-8')
            tagLine = inputFile.readline().rstrip()
            tagList = tagLine.split('\t')
            inputFile.close()
            tagsInline = False
    elif anArg in ['help', '-help', '-?', '?']:
        print('tsv2xml 1.0')
        print('Tabszeparált fájlt XML fájllá alakít.')
        print('A tsv fájl egyes sorait szóként (w) értelmezi, az üres sorok új mondatot (s) kezdenek.')
        print('\n')
        print('<tsv2xml>')
        print('  <s>')
        print('    <w>...</w>')
        print('    <w>...</w>')
        print('  </s>')
        print('  ...')
        print('</tsv2xml>')
        print('\n')
        print('A tsv fájl oszlopai a <w> tagek között jelennek meg valamilyen címkével.')
        print('A címkéket a tsv fájl első oszlopából szedi, ami szintén tsv, pl. (magyarlánc depparse):')
        print('\tid:id\tform\tlemma\tpos\tfs:X\tid:idref\tdeprel\n')
        print('A címkék kezdődhetnek utasítással is, a címkétől kettősponttal elválasztva:')
        print('  f:valami    - az adott oszlopban levő érték a szó attribútuma lesz: valami="xxx"')
        print('  fs:X        - az adott oszlopban levő értéket szétvágja "|" mentén több darabra,')
        print('                és a kapott darabokat att=val szerint értelmezve a szó attribútumaiként jeleníti meg.')
        print('  mTag:X      - az adott oszlopban levő értéket szétvágja "|" mentén több darabra,')
        print('                és a kapott darabokat att=val szerint értelmezve a szón belüli <att>val</att> -ként')
        print('                jeleníti meg. Az X nem számít.')
        print('  id:valami   - az adott oszlopban levő értékből a szón "valami" nevű id attribútumot készít.')
        print('                Az attribútum értéke "s1w2" alakú lesz, ahol 1 a mondat sorszáma, 2 pedig az oszlop értéke.')
        print('Ha egy sorban több oszlop van, mint a címkefelsorolásban, akkor <tag> taggel jelenik meg.')
        print('Az oszlopban található "_" érték üresnek számít, nem generál xml-elemet.\n')
        print('A program paraméterezhető param=érték kifejezésekkel:')
        print('  input=filename      - a feldolgozandó tsv fájl neve. Default: ' + inputFileName)
        print('  output=filename     - a a kimeneti xml fájl neve. Default: ' + outputFileName)
        print('  tagdef=filename     - a címkedefiníciók a filename fájlból származnak,')
        print('                        a feldolgozandó fájl ekkor nem tartalmaz címkedefiníciót.')
        print('  root=tagname        - a root tag címkéje. Default: ' + rootTag)
        print('  stag=tagname        - a mondat tag címkéje. Default: ' + sentenceTag)
        print('  wtag=tagname        - a szó tag címkéje. Default: ' + wordTag)
        print('  drop=char           - az üres érték jelölője. Default: ' + dropChar)
        print('  idpfx=string        - az indexek prefixuma. Default: ' + idPrefix)
        print('  idstart=int         - ezzel kezdi a mondatok számozását. Default: ' + str(sIDStart))
        print('  wpfx=string         - az indexekben a mondat és a szó elválasztója. Default: ' + wSep)
        print('  split=char          - a többtagú kifejezések elválasztója. Default: ' + mtSep)
        print('  attr=char           - az attribútumok és értékek elválasztója. Default: ' + faSep + '\n')
        print('A feldolgozhatatlan adatot tartalmazó szavak "error" attribútumot kapnak.')
        print('(c) Szécsényi Tibor 2020')
        sys.exit()


# ## Egy mondat beolvasása a TSV fájlból
# A fájl megnyitása a főprogramban történik

# In[ ]:


def readSentence():
    line = inputFile.readline()
    while line == '' or line[0] == '\n' or line[0] == '#':
        if line == '':
            return
        line = inputFile.readline()
        
    sentence = []
    while line != '' and line[0] != '\n':
        if line[0] != '#':
            sentence.append(line.rstrip().split('\t'))
        line = inputFile.readline()
    
    return sentence
    


# ## A főprogram

# ### A TSV fájl megnyitása és az első sor beolvasása
# Az első sor tartalmazza a TSV fájl oszlopainak az értelmezési utasítását.

# In[ ]:


snum = sIDStart
inputFile = open(inputFileName, 'r', encoding='utf-8-sig')
if tagsInline:
    tagLine = inputFile.readline().rstrip()
    tagList = tagLine.split('\t')


# ### Az XML struktúra létrehozása és az első mondat beolvasása

# In[ ]:


doc = minidom.Document()
root = doc.createElement(rootTag)
doc.appendChild(root)
sentenceData = readSentence()


# ### A mondatok átalakítása XML szerkezetre, és a következő mondat beolvasása

# In[ ]:


while sentenceData:
    if snum % 100 == 0:
        print(str(snum)+'\r')
    sentence = doc.createElement(sentenceTag)
    sentence.setAttribute('id', idPrefix+str(snum))
    root.appendChild(sentence)
    for wordData in sentenceData:
        word = doc.createElement(wordTag)
        for i in range(len(wordData)):
            if wordData[i] != dropChar and wordData[i] != '':
                if i >= len(tagList):
                    newTag = doc.createElement('tag')
                    newTag.appendChild(doc.createTextNode(wordData[i]))
                    word.appendChild(newTag)
                elif tagList[i].startswith('id:'):
                    word.setAttribute(tagList[i][3:], idPrefix+str(snum)+wSep+wordData[i])
                elif tagList[i].startswith('f:'):
                    word.setAttribute(tagList[i][2:], wordData[i])
                elif tagList[i].startswith('fs:'):
                    for av in wordData[i].split(mtSep):
                        if av.find(faSep) == -1:
                            word.setAttribute('error', 'fs')
                            print('error: ' + idPrefix+str(snum)+wSep+wordData[0])
                        else:
                            [at,val] = av.split(faSep)
                            word.setAttribute(at,val)
                elif tagList[i].startswith('mTag:'):
                    for tv in wordData[i].split(mtSep):
                        if tv.find(faSep) == -1:
                            word.setAttribute('error', 'mTag')
                            print('error: ' + idPrefix+str(snum)+wSep+wordData[0])
                        else:
                            [tg,val] = tv.split(faSep)
                            newTag = doc.createElement(tg)
                            newTag.appendChild(doc.createTextNode(val))
                            word.appendChild(newTag)
                else:
                    newTag = doc.createElement(tagList[i])
                    newTag.appendChild(doc.createTextNode(wordData[i]))
                    word.appendChild(newTag)
            sentence.appendChild(word)
    sentenceData = readSentence()
    snum = snum + 1


# ### A TSV fájl bezárása, és az XML fájl létrehozása

# In[ ]:


inputFile.close()
                
with open (outputFileName, "wb") as files :
    files.write(doc.toprettyxml(indent ="\t", encoding="utf-8"))


# In[ ]:





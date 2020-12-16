# tsv2xml.py
ver 1.0  
(c) Szécsényi Tibor 2020  
  
A program tab-szeparált szövegfájlból (.tsv) készít XML fájlt.

## Mi az a TSV, és hogyan értelmezzük?

A TSV fájlokban az egyes sorok egy-egy objektumról szolgálnak információval. 
A `tsv2xml` program az egyes objektumokat szavaknak tekinti. Több szó, vagyis 
több sor mondatot alkot, a mondatokat pedig üres sorok választják el 
egymástól. Az egyes szavakra vonatkozó információk a sorokban tabulátorral 
`\t` vannak elválasztva. A sorokban levő információdarabokra oszlopokként 
fogunk hivatkozni, vagyis egy szóra vonatkozó első információ a sor első 
oszlopában, a második információ a második oszlopban található, stb. 
A szavakra általában ugyanannyi információ vonatkozik, az egyes oszlopokban 
pedig rendre ugyanolyan típusú információ található. A CONLL-U formátumú TSV 
fájlokban például a következő információk sorakoznak a szavakról 
(https://universaldependencies.org/format.html): 

1. ID: Word index, integer starting at 1 for each new sentence; may be a 
range for multiword tokens; may be a decimal number for empty nodes (decimal 
numbers can be lower than 1 but must be greater than 0).
2. FORM: Word form or punctuation symbol.
3. LEMMA: Lemma or stem of word form.
4. UPOS: Universal part-of-speech tag.
5. XPOS: Language-specific part-of-speech tag; underscore if not available.
6. FEATS: List of morphological features from the universal feature inventory 
or from a defined language-specific extension; underscore if not available.
7. HEAD: Head of the current word, which is either a value of ID or zero (0).
8. DEPREL: Universal dependency relation to the HEAD (root iff HEAD = 0) or 
a defined language-specific subtype of one.
9. DEPS: Enhanced dependency graph in the form of a list of head-deprel pairs.
10. MISC: Any other annotation.

Ha egy szó/sor nem jellemezhető valamilyen tulajdonsággal, vagy nem ismert 
valamelyik tulajdonsága, ezt a sor megfelelő helyén a `_` jellel jelölhetjük. 

A TSV fájlban megjegyzések helyezhetők el, a megjegyzéssorok `#` karakterrel 
kezdődnek. A megjegyzéssorokat a `tsv2xml` figyelmen kívül hagyja, mintha 
nem is lennének (még csak üres sornak sem számítanak).

## Mit csinál a `tsv2xml`?

A `tsv2xml` a TSV fájlban található információk alapján létrehoz egy XML fájlt. 
Az XML fájl root tagje alapértelmezés szerint `tsv2xml` (ezt a `root` 
paraméterrel lehet módosítani). A `tsv2xml`-ben `s` tagekkel sorakoznak a 
mondatok (módosítható az `stag` paraméterrel), amiken belül a szavak `w` taggel 
találhatóak (módostható a `wtag` paraméterrel). A mondatok `s` tagje egy `id` 
attribútummal is kiegészül, amellyel a mondatok azonosíthatóak.

A szavak jellemzői, vagyis az egyes szó sorában levő információk, az oszlopok 
tartalma az XML fájlban a `w` tagen belül jelennek meg, jellemzően a `w` 
attribútumaként, vagy `w` alatti elemként. A TSV fájl oszlopainak az 
értelmezését alapértelmezésben a TSV fájl első, szintén tab-szeparált sora 
határozza meg (ez megváltoztatható a `tagdef` paraméterrel). A TSV fájl első 
sorában tabulátorokkal elválasztva adhatjuk meg, hogy az adott oszlopban 
található információ a `w` tag alatt milyen taggel jelenjen meg. Például a 


```
ID	FORM	LEMMA	UPOS	XPOS	FEATS	HEAD	DEPREL	DEPS	MISC
# text = They buy and sell books.
1	They	they	PRON	PRP	Case=Nom|Number=Plur	2	nsubj	2:nsubj|4:nsubj	_
2	buy	buy	VERB	VBP	Number=Plur|Person=3|Tense=Pres	0	root	0:root	_
3	and	and	CONJ	CC	_	4	cc	4:cc	_
4	sell	sell	VERB	VBP	Number=Plur|Person=3|Tense=Pres	2	conj	0:root|2:conj	_
5	books	book	NOUN	NNS	Number=Plur	2	obj	2:obj|4:obj	SpaceAfter=No
6	.	.	PUNCT	.	_	2	punct	2:punct	_
```

TSV fájlból

```
<?xml version="1.0" encoding="utf-8"?>
<tsv2xml>
	<s id="s1">
		<w>
			<ID>1</ID>
			<FORM>They</FORM>
			<LEMMA>they</LEMMA>
			<UPOS>PRON</UPOS>
			<XPOS>PRP</XPOS>
			<FEATS>Case=Nom|Number=Plur</FEATS>
			<HEAD>2</HEAD>
			<DEPREL>nsubj</DEPREL>
			<DEPS>2:nsubj|4:nsubj</DEPS>
		</w>
		<w>
			<ID>2</ID>
			<FORM>buy</FORM>
			<LEMMA>buy</LEMMA>
			<UPOS>VERB</UPOS>
			<XPOS>VBP</XPOS>
			<FEATS>Number=Plur|Person=3|Tense=Pres</FEATS>
			<HEAD>0</HEAD>
			<DEPREL>root</DEPREL>
			<DEPS>0:root</DEPS>
		</w>
		<w>
			<ID>3</ID>
			<FORM>and</FORM>
			<LEMMA>and</LEMMA>
			<UPOS>CONJ</UPOS>
			<XPOS>CC</XPOS>
			<HEAD>4</HEAD>
			<DEPREL>cc</DEPREL>
			<DEPS>4:cc</DEPS>
		</w>
		<w>
			<ID>4</ID>
			<FORM>sell</FORM>
			<LEMMA>sell</LEMMA>
			<UPOS>VERB</UPOS>
			<XPOS>VBP</XPOS>
			<FEATS>Number=Plur|Person=3|Tense=Pres</FEATS>
			<HEAD>2</HEAD>
			<DEPREL>conj</DEPREL>
			<DEPS>0:root|2:conj</DEPS>
		</w>
		<w>
			<ID>5</ID>
			<FORM>books</FORM>
			<LEMMA>book</LEMMA>
			<UPOS>NOUN</UPOS>
			<XPOS>NNS</XPOS>
			<FEATS>Number=Plur</FEATS>
			<HEAD>2</HEAD>
			<DEPREL>obj</DEPREL>
			<DEPS>2:obj|4:obj</DEPS>
			<MISC>SpaceAfter=No</MISC>
		</w>
		<w>
			<ID>6</ID>
			<FORM>.</FORM>
			<LEMMA>.</LEMMA>
			<UPOS>PUNCT</UPOS>
			<XPOS>.</XPOS>
			<HEAD>2</HEAD>
			<DEPREL>punct</DEPREL>
			<DEPS>2:punct</DEPS>
		</w>
	</s>
</tsv2xml>
```

XML fájlt hoz létre. Az átalakítás során az `_` karaktert tartalmazó oszlopok 
nem jelennek meg az XML fájlban (az üres karakter megváltoztatható a `drop` 
paraméterrel).

A TSV fájl egyes oszlopai nem csak `w` alatti tagként értelmezhetőek, hanem

## Oszlopdefiníciós lehetőségek

Amennyiben egy szó valamely információjára nem vonatkozik semmilyen definíció, 
mert kevesebb oszlopból áll a definíciós sor, akkor az az információ `<tag>` 
tag alá keül.

### `f:name`
Ha az oszlopdefiníciós sor (a TSV fájl első sora) egyik oszlopában levő 
kifejezés `f:` kifejezéssel kezdődik, akkor az adott oszlopban található 
információ a `w` tag attribútumaként jelenik meg, az attributum neve pedig az 
oszlopdefiníciós kifejezés kettőspont utáni része lesz. Ha az iménti 
példában kicseréljük az első sorban az `ID` és a `FORM` értékeket 
`f:ID` és `f:FORM` értékre: 

```
f:ID	f:FORM	LEMMA	UPOS	XPOS	FEATS	HEAD	DEPREL	DEPS	MISC
1	They	they	PRON	PRP	Case=Nom|Number=Plur	2	nsubj	2:nsubj|4:nsubj	_
```

akkor a program a következő XML struktúrát hozza létre a szóhoz:

```
<w ID="1" FORM="They">
	<LEMMA>they</LEMMA>
	<UPOS>PRON</UPOS>
	<XPOS>PRP</XPOS>
	<FEATS>Case=Nom|Number=Plur</FEATS>
	<HEAD>2</HEAD>
	<DEPREL>nsubj</DEPREL>
	<DEPS>2:nsubj|4:nsubj</DEPS>
</w>
```

### `fs:X`

Ha az oszlopdefiníciós sor (a TSV fájl első sora) egyik oszlopában levő 
kifejezés `fs:` kifejezéssel kezdődik (a kettőspont utáni rész lényegtelen), 
akkor az adott oszlopban található információ a `w` tag attribútumaként jelenik 
meg. A program feltételezi, hogy az adott oszlopban `|` karakterrel elválasztva 
egy vagy több információ található, mégpedig oly módon, hogy a részinformációk 
`attribute=value` szerkezetűek. (A `|` és az `=` karakterek megváltoztathatóak a
`split` és `attr` paraméterekkel.) Ilyenkor a `w` tagben mindegyik részinformáció 
külön attribútumként jelenik meg, ahol az attribútum neve az `=` előtti rész, 
az értéke pedig az `=` utáni rész lesz. Ha az iménti 
példában kicseréljük az első sorban a `FEATS` értéket `fs:FEATS` értékre: 

```
ID	FORM	LEMMA	UPOS	XPOS	fs:FEATS	HEAD	DEPREL	DEPS	MISC
1	They	they	PRON	PRP	Case=Nom|Number=Plur	2	nsubj	2:nsubj|4:nsubj	_
```

akkor a program a következő XML struktúrát hozza létre a szóhoz:

```
<w Case="Nom" Number="Plur">
	<ID>1</ID>
	<FORM>They</FORM>
	<LEMMA>they</LEMMA>
	<UPOS>PRON</UPOS>
	<XPOS>PRP</XPOS>
	<HEAD>2</HEAD>
	<DEPREL>nsubj</DEPREL>
	<DEPS>2:nsubj|4:nsubj</DEPS>
</w>
```

Ha egy ilyen ilyen módon feldolgozandó (rész)kifejezés nem tartalmaz `=` jelet, 
akkor a `w` tag `error="fs"` attribútumot kap.

### `mTag:X`

Ha az oszlopdefiníciós sor (a TSV fájl első sora) egyik oszlopában levő 
kifejezés `fs:` kifejezéssel kezdődik (a kettőspont utáni rész lényegtelen), 
akkor az adott oszlopban található információ a `w` tag alatti tagként jelenik 
meg. A program feltételezi, hogy az adott oszlopban `|` karakterrel elválasztva 
egy vagy több információ található, mégpedig oly módon, hogy a részinformációk 
`tagname=text` szerkezetűek. (A `|` és az `=` karakterek megváltoztathatóak a
`split` és `attr` paraméterekkel.) Ilyenkor a `w` tag alatt mindegyik 
részinformáció külön tagként jelenik meg, ahol a tag neve az `=` előtti rész, 
az értéke pedig az `=` utáni rész lesz. Ha az iménti 
példában kicseréljük az első sorban a `FEATS` értéket `mTag:FEATS` értékre: 

```
ID	FORM	LEMMA	UPOS	XPOS	mTag:FEATS	HEAD	DEPREL	DEPS	MISC
1	They	they	PRON	PRP	Case=Nom|Number=Plur	2	nsubj	2:nsubj|4:nsubj	_
```

akkor a program a következő XML struktúrát hozza létre a szóhoz:

```
<w>
	<ID>1</ID>
	<FORM>They</FORM>
	<LEMMA>they</LEMMA>
	<UPOS>PRON</UPOS>
	<XPOS>PRP</XPOS>
	<Case>Nom</Case>
	<Number>Plur</Number>
	<HEAD>2</HEAD>
	<DEPREL>nsubj</DEPREL>
	<DEPS>2:nsubj|4:nsubj</DEPS>
</w>
```

Ha egy ilyen ilyen módon feldolgozandó (rész)kifejezés nem tartalmaz `=` jelet, 
akkor a `w` tag `error="mTag"` attribútumot kap.

### `id:name`

Ha az oszlopdefiníciós sor (a TSV fájl első sora) egyik oszlopában levő 
kifejezés `id:` kifejezéssel kezdődik, akkor az adott oszlopban található 
információ a `w` attribútumaként jelenik meg. Az attribútum neve megegyezik 
az oszlopdefinició kettőspont utáni részével, az értéke pedig a `w` fölötti 
`s` tag azonosítójából (`id` attribútum), a `'w'` elválasztó karakterből, 
és a szó adott oszlopában található információból tevődik össze.

A mondatok `id` azonosítója két részből áll: 
1. az `'s'` prefixumból 
2. a mondat sorszámából (hányadik mondat a TSV fájlban)

A szó előállított azonosítója négy részből áll `'s'+num+'w'+val`:

1. `'s'` - a prefixum megváltoztatható az `idpfx` paraméterrel 
2. `num` - a kezdősorszám megváltoztatható az `idstart` paraméterrel
3. `'w'` - az elválasztó karakter megváltoztatható a `wpfx` paraméterrel
4. `val` - a szó megadott oszlopából kiolvasott érték

Ha az iménti példában kicseréljük az első sorban az `ID`, `LEMMA` és `HEAD` 
értéket `id:ID`, `id:LEMMA` és `id:HEAD` értékre: 

```
id:ID	FORM	id:LEMMA	UPOS	XPOS	FEATS	id:HEAD	DEPREL	DEPS	MISC
1	They	they	PRON	PRP	Case=Nom|Number=Plur	2	nsubj	2:nsubj|4:nsubj	_
```

akkor a program a következő XML struktúrát hozza létre a szóhoz:

```
<tsv2xml>
	<s id="s1">
		<w ID="s1w1" LEMMA="s1wthey" HEAD="s1w2">
			<FORM>They</FORM>
			<UPOS>PRON</UPOS>
			<XPOS>PRP</XPOS>
			<FEATS>Case=Nom|Number=Plur</FEATS>
			<DEPREL>nsubj</DEPREL>
			<DEPS>2:nsubj|4:nsubj</DEPS>
		</w>
	...
```


## A program használata

A program feltételezi, hogy a python 3.x telepítve van a számítógépre, és 
a programfájlt tartalmazó könyvtárból elérhető parancssorból. A programot 
parancssorból kell meghívni a `python tsv2xml.py` utasítással. A program 
paraméterek nélkül is futtatható, ekkor az alapértelmezett beállításokkal fut. 
A program paraméterei `parameter=value` alakban változtathatóak meg. 
A paraméterek értéke közvetlenül, vagy idézőjelek között is megadható: a kezdő 
és záró zárójelek nem lesznek figyelembe véve.

A program tipikus paraméteres használata: 
`python tsv2xml.py input=mytsv01.tsv output=myxml01.xml idpfx=f01s`

A használható paraméterek a következők:

### `input`=*filename*
a feldolgozandó tsv fájl neve. Default: `input.tsv`

### `output`=*filename*
a kimeneti xml fájl neve. Default: `output.tsv`

### `tagdef`=*filename*
a címkedefiníciók a filename fájlból származnak a feldolgozandó fájl ekkor nem tartalmaz címkedefiníciót.

### `root`=*tagname*
a root tag címkéje. Default: `tsv2xml`

### `stag`=*tagname*
a mondat tag címkéje. Default: `s`

### `wtag`=*tagname*
a szó tag címkéje. Default: `w`

### `drop`=*char*
az üres érték jelölője. Default: `_`

### `idpfx`=*string*
az indexek prefixuma. Default: `s`

### `idstart`=*int*
ezzel kezdi a mondatok számozását. Default: `1`

### `wpfx`=*string*
az indexekben a mondat és a szó elválasztója. Default: `w`

### `split`=*char*
a többtagú kifejezések elválasztója. Default: `|`

### `attr`=*char*
az attribútumok és értékek elválasztója. Default: `=`



```

```

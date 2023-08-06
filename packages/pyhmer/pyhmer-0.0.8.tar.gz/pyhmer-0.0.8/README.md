[![This is an image](https://img.shields.io/pypi/v/pyhmer.svg?style=flat-square)](https://pypi.python.org/pypi/pyhmer)

# Pyhmer

### About
Use pyhmer to generate a rhyming noun + adjective pair. Useful for giving database objects human readable names. As of right now only animal + adjective pairs can be generated. 

[Package Source](src/pyhmer)    

To see how the data was compiled see the [data_work](data_work/) directory

### Install
```
pip install pyhmer
```
### Usage
```
>>>import pyhmer
>>>animal_rhyme = pyhmer.get_animal_rhyme()
>>>print(animal_rhyme)

'minute newt'

>>>for i in range(10):
>>>    print(pyhmer.get_animal_rhyme())

'allegro buffalo'
'insane crane'
'statuary cassowary'
'starry wallaby'
'preteen wolverine'
'clear deer'
'illusionary cassowary'
'flush thrush'
'maroon baboon'
'skew kangaroo'
```
### Sources
###### Adjectives
[Wordnet Lexical Database](https://wordnet.princeton.edu/download/current-version)

###### Animals 

[Wikipedia List of Animals Names](https://en.wikipedia.org/wiki/List_of_animal_names)

###### Word Rhyming
[Carnegie Mellon University Pronouncing Dictionary](http://www.speech.cs.cmu.edu/cgi-bin/cmudict?in=C+M+U+Dictionary)\
[pronouncingpy python package](https://github.com/aparrish/pronouncingpy)


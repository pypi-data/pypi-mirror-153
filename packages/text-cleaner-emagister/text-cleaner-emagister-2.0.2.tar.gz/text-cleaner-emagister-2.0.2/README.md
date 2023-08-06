# Text Cleaner. Cleaning & Preprocessing Text Data
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
![GitHub release (latest by date)](https://img.shields.io/github/v/release/fdelgados/text-cleaner?style=flat)

text-cleaner is a tool created to perform NLP Text preprocessing. This tool helps to remove noise from text and make it ready to feed to models.

## Table of Contents
* [Dependencies](#dependencies)
* [Installation](#installation)
* [Instructions](#instructions)
* [License](#license)

### Dependencies

text-cleaner requires:

* Python (>=3.8)
* [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) (4.9.3)
* [Unidecode](https://pypi.org/project/Unidecode/) (1.3.2)

### Installation

You can install text-cleaner using `pip`
```
pip install text-cleaner-fdelgados
```
That easy!


### Instructions
You can clean text using the `clean` method of the `TextCleaner` class:

```python
from textcleaner import TextCleaner

text = '<p><i><b>2001: A    Space Odyssey</b></i> \n\nis a 1968 <a href="/wiki/Epic_film" title="Epic ' \
           'film">epic</a> <a href="/wiki/Science_fiction_film" title="Science fiction film">science fiction film</a> ' \
           'produced and directed by\t <a href="/wiki/Stanley_Kubrick" title="Stanley Kubrick">Stanley Kubrick</a>. ' \
           'The screenplay was written by Kubrick and <a href="/wiki/Arthur_C._Clarke" title="Arthur C. ' \
           'Clarke">Arthur C. Clarke</a>, and was inspired by Clarke\'s short story ""<a href="/wiki/The_Sentinel_(' \
           'short_story)" title="The Sentinel (short story)">The Sentinel</a>" and other short stories by Clarke. A ' \
           '<a href="/wiki/2001:_A_Space_Odyssey_(novel)" title="2001: A Space Odyssey (novel)">novelisation of the ' \
           'film</a> released after the film\'s premiere was in part written concurrently with the screenplay. The ' \
           'film, which follows a voyage to <a href="/wiki/Jupiter" title="Jupiter">Jupiter</a> with the <a ' \
           'href="/wiki/Sentience" title="Sentience">sentient</a> computer <a href="/wiki/HAL_9000" title="HAL ' \
           '9000">HAL</a> after the discovery of a <a href="/wiki/Monolith_(Space_Odyssey)" title="Monolith (Space ' \
           'Odyssey)">featureless alien monolith</a> affecting human evolution, deals with themes of <a ' \
           'href="/wiki/Existentialism" title="Existentialism">existentialism</a>, <a href="/wiki/Human_evolution" ' \
           'title="Human evolution">human evolution</a>, technology, <a href="/wiki/Artificial_intelligence" ' \
           'title="Artificial intelligence">artificial intelligence</a>, and the possibility of <a ' \
           'href="/wiki/Extraterrestrial_life" title="Extraterrestrial life">extraterrestrial life</a>.</p> '

cleaner = TextCleaner(text)

print(cleaner.clean())

# output

# 2001: A Space Odyssey is a 1968 epic science fiction film produced and directed by Stanley Kubrick. The screenplay 
# was written by Kubrick and Arthur C. Clarke, and was inspired by Clarke's short story "The Sentinel" and other 
# short stories by Clarke. A novelisation of the film released after the film's premiere was in part written 
# concurrently with the screenplay. The film, which follows a voyage to Jupiter with the sentient computer HAL after 
# the discovery of a featureless alien monolith affecting human evolution, deals with themes of existentialism, 
# human evolution, technology, artificial intelligence, and the possibility of extraterrestrial life.

```
### License

MIT License

Copyright (c) 2021 Cisco Delgado

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

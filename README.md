## Overview

Fast and efficient way to split concatenated Georgian text. 

[*For more details on how the algorithm works visit the [original repository](https://github.com/keredson/wordninja)*]

## Usage
### Example
```
$ python
>>> from wordninja import Wordninja
>>> lm = Wordninja()
>>> lm.split('ვნებისსიმძაფრეშენებაშიადაარააშენებულითტკბობაში')
['ვნების', 'სიმძაფრე', 'შენებაშია', 'და', 'არა', 'აშენებულით', 'ტკბობაში']
>>> lm.split('ესმეუკვემივხვდიროაღარდამზოგავდა')
['ეს', 'მე', 'უკვე', 'მივხვდი', 'რო', 'აღარ', 'დამზოგავდა']
```

### Installation
```
pip install git+https://github.com/jupyterjazz/wordninja
```

### Modifying model's behaviour
Case 1. we don't want to split a specific word
```
>>> lm.split('ემპედოკლე')
['ემპედო', 'კლე'] # we want ['ემპედოკლე']
>>> lm.add_word('ემპედოკლე')
>>> lm.split('ემპედოკლე')
['ემპედოკლე']
```

Case 2. we want to split a word in a certain way
```
>>> lm.split('ჰერაკლე')
['ჰერაკლე'] # we want ['ჰერა', 'კლე']
>>> lm.remove_word('ჰერაკლე')
>>> lm.add_word('ჰერა')
>>> lm.add_word('კლე')
>>> lm.split('ჰერაკლე')
['ჰერა', 'კლე']
```

### Save and reuse models
Don't forget to save the model after you've made some changes.
```
>>> lm.save_model('model_name')
>>> modified_lm = Wordninja('model_name')
```


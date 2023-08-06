# Forseti Language

The system for determining the compliance of the text with the specified rules

## How to install:

PyPi installation guide
```shell
pip install forseti-lang
```

## How to use:

```python
from forseti_lang.execute import execute_condition

condition = "TRUE AND FALSE"
text = ""
execute_condition(condition, text)  # False
```

All regular expressions should be in lowercase.

## Supported logic operators

### English

Below is a table of available logical operators and their description.

| Operator               | Description                                 | Priority |
|------------------------|---------------------------------------------|----------|
| ()                     | The conditions in quotes will be met first  | 0        |
| AND                    | Logical **AND**                             | 1        |
| AND NOT                | Logical **AND NOT**                         | 2        |
| OR                     | Logical **OR**                              | 3        |
| Atoms (TRUE and FALSE) | Minimum logical unit                        | 4        |

### Russian

Forseti was developed for the analysis of texts in Russian.
So, you can use:

| RU  | ENG |
|-----|-----|
| И   | AND |
| ИЛИ | OR  |

#### Note

You can combine ru and eng operators.

## Supported functions

We really lacked a simple syntax (but regular expressions did not allow us to achieve this), so we created our own
functions!

| Function         | In Forseti | Description                                               | Priority |
|------------------|------------|-----------------------------------------------------------|----------|
| f text length    | ll, lg     | Text length in characters check function                  | 5        |
| f words distance | wN, cN, N  | Checks whether the words are in the specified interval    | 6        |
| f words nearby   | nearby     | Checks the words that are next to another word            | 7        |
| f regex search   |            | Checks the occurrence of a regular expression in the text | 8        |

### Explanations

* `|ll` - length less (in characters)
* `|lg` - length great (in characters)
* `|wN` - word in distance `N words`
* `|cN` - word in distance `N characters`
* `|N` - alias of `|wN`
* `|nearby` - the word is nearby to the words `word1 |nearby word2 | word3 | word4`

#### Notes

* All function starts with special character: `|`. That's why we don't support it in regular expressions
* It is also forbidden to use the `-` character, it is used in the distance function
* The function of finding words at a distance will allow you to exclude constructions with a word at a distance,
for example:
```
condition - "hello |w1 -world"
text      - "Hello beautiful world!"
result    - False
```
* You cannot combine two functions in one expression
* Text length and word distance functions don't work with negative values

## Priority table

| Operator                   | Description                                               | Priority |
|----------------------------|-----------------------------------------------------------|----------|
| `()`                       | The conditions in quotes will be met first                | 0        |
| `AND`                      | Logical `AND`                                             | 1        |
| `AND NOT`                  | Logical `AND NOT`                                         | 2        |
| `OR`                       | Logical `OR`                                              | 3        |
| Atoms (`TRUE` and `FALSE`) | Minimum logical unit                                      | 4        |
| f text length              | Text length in characters check function                  | 5        |
| f words distance           | Checks whether the words are in the specified interval    | 6        |
| f words nearby             | Checks the words that are next to another word            | 7        |
| f regex search             | Checks the occurrence of a regular expression in the text | 8        |


## Examples

### Checking the length of the text

```python
from forseti_lang.execute import execute_condition

condition = '|ll5'
execute_condition(condition, "Hello world!")  # False
execute_condition(condition, "Hi")  # True

condition = '|lg5'
execute_condition(condition, "Hello world!")  # True
execute_condition(condition, "Hi")  # False
```

### Checking the words distance

```python
from forseti_lang.execute import execute_condition

condition = 'hello |w1 world'
execute_condition(condition, "Hello world!")  # True
execute_condition(condition, "Hello sunny world!")  # True
execute_condition(condition, "Hello dirty and dark world!")  # False

condition = 'hi\W? |c1 how are you'
execute_condition(condition, "Hi, how are you?")  # True
execute_condition(condition, "Hi, hmm.. how ary you?")  # False

condition = 'hello |1 world'
execute_condition(condition, "Hello world!")  # True
```

### Checking nearby words

```python
from forseti_lang.execute import execute_condition

condition = 'hello |nearby world | people | notalib'
execute_condition(condition, "Hello world!")  # True
execute_condition(condition, "Hello notalib!")  # True
```

### Logic processing

```python
from forseti_lang.execute import execute_condition

execute_condition("TRUE AND FALSE", "") # False
execute_condition("TRUE OR FALSE", "") # True
execute_condition("FALSE OR TRUE AND (TRUE OR FALSE)", "") # True
execute_condition("FALSE OR TRUE AND (FALSE AND TRUE)", "") # False
execute_condition("(TRUE OR FALSE) AND NOT (TRUE AND FALSE)", "") # TRUE
```

### Difficult rules example
* `короб AND NOT короб |2 конфет`
* `минимальн\w,{,2} |1 стоимо`
* `балл AND NOT (сн[ия]\w* балл ИЛИ 10\s?балл ИЛИ десять\sбаллов) AND |lg15`

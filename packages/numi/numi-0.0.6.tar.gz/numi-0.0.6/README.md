

<!-- ![Tests](https://gitlab.com/tiro-is/h10/h10/numi/actions/workflows/tests.yml/badge.svg) -->

## Númi
Númi er pakki sem stafar út tölustafi. Þegar notandinn gefur Núma tölu ásamt streng sem inniheldur upplýsingar um beygingar skilar hann öllum mögulegum leiðum sem þessi tala getur verið stöfðu út.

This package expands Icelandic numbers to their corresponding written form. Given a digit and a string containing the case, gender and inflection the funciton will output a list of strings for all written variants.



## Usage

To get started run 
```
pip install numi
```

The main function in numi is `spell_out`. It takes in two parameters, an number and a string specifying the desired morphology. 

In the following example we want to get the numer `124` in plural, masculine and nominative form.  

```
from numi import spell_out
print(spell_out(124, "ft_kk_nf")

> ["eitt hundrað tuttugu og fjórir", "hundrað tuttugu og fjórir"]
```

All the abrivations for the input string are as follows:

| Abbr. | English    | Icelandic  |
| ----- | ---------- | ---------- |
| et    | singular   | eintala    |
| ft    | plural     | fleirtala  |
|       |            |            |
| kk    | masculine  | karlkyns   |
| kvk   | feminine   | kvenkyns   |
| hvk   | neuter     | hvorugkyns |
|       |            |            |
| nf    | nominative | nefnifall  |
| þf    | accusative | þolfall    |
| þgf   | dative     | þágufall   |
| ef    | genitive   | eignafall  |


## Contributing
This package is a work in progress. We use `pytest` for development test and run `pip install requirements_dev.txt` for development packages.

## License
MIT  

## Project status
* 0.0.5 - Support for numbers between 1-999

Future work
* Adding the first decimal place for all numbers
* Parse user input in a robust way
* Add CLI support 
* Add test script for development
* Document the abbreviations 
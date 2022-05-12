[![Github](https://img.shields.io/badge/sources-github-green.svg)](https://github.com/puttsk/codegen/)
 [![GitHub forks](https://img.shields.io/github/stars/puttsk/codegen.svg?style=social&label=Star)](https://github.com/puttsk/codegen)

# Codegen

Codegen is a simple source-to-source utility for generating a code based on json data. This is useful for embeded data into a code for a small to medium data set. The original goal is used for generating static code for [gocountries](https://github.com/puttsk/gocountries) project.

## Installation

``` bash
go get github.com/puttsk/codegen
```

## Examples

Following is an example of codegen template to generate a function with switch statement in Go language.

Template: 

``` go
func GetCountryFromAlpha3(alpha3 string) (Country) {
    switch alpha3 {
        << for-block begin >>
        case "{{alpha3}}": 
            return Country{
                Alpha2: "{{alpha2}}", 
                Alpha3: "{{alpha3}}", 
                ID: {{id}}, 
                EN:"{{en}}", 
                TH:"{{th}}"}
        << for-block end >>
        default:
            return Country{}
    }
}
```

Input data (from [world_countries](https://github.com/stefangabos/world_countries) dataset):

``` json
[
    {"id":4,"alpha2":"af","alpha3":"afg","en":"Afghanistan","th":"อัฟกานิสถาน"},
    {"id":8,"alpha2":"al","alpha3":"alb","en":"Albania""th":"แอลเบเนีย"},
    ...,
    {"id":894,"alpha2":"zm","alpha3":"zmb","en":"Zambia","th":"แซมเบีย"},
    {"id":716,"alpha2":"zw","alpha3":"zwe","en":"Zimbabwe","th":"ซิมบับเว"}
]
```

Output:

``` go

func GetCountryFromAlpha3(alpha3 string) Country {
    switch alpha3 {
    case "afg":
        return Country{
            Alpha2: "af", 
            Alpha3: "afg", 
            ID: 4, 
            EN: "Afghanistan", 
            TH: "อัฟกานิสถาน"}
    case "alb":
        return Country{
            Alpha2: "al", 
            Alpha3: "alb", 
            ID: 8,
            EN: "Albania", 
            TH: "แอลเบเนีย"}
    ...
    default:
        return Country{}
    }
}
```

## Usage

``` bash
usage: codegen.py [-h] [-d PATH] [-o OUTPUT] [-t TEMPLATE]

Convert input data to an output file based on template

optional arguments:
  -h, --help            show this help message and exit
  -d PATH, --data PATH  path to data file
  -o OUTPUT, --output OUTPUT
                        output file name
  -t TEMPLATE, --template TEMPLATE
                        path to template file
```

## Input Data

Codegen currently support JSON as input. In current version, the input JSON can contain only a list of objects as follows.

``` json
[
    {
        "field1": "", 
        "field2": "", 
    }, 
    {
        "field1": "", 
        "field2": "",
        "field3": "", 
    },
    ...
]
```

## Template

Codegen generates an output based on a template file. Codegen template contains two special sequences: `<<...>>` and `{{...}}`, which indicate control statement and variables, respectively.

**Control statements** determines how codegen will handle the content of the template inside the control block. **A control block** is indicated by two control statement of the same name, where the beginning of the block is indicated by a keyword `begin` and the block ends at the control statement with a keyword `end`.

**Variables** indicates where codegen will put value from input data to the template.

Currently, codegen support only `for` loop as a control statement. For a `for` loop, codegen iterates through objects from the [input data](#input-data) and replaces variables with data from the field, indicated by the variable name, of the object. 

## Contributing

TBD

## Authors

* **Putt Sakdhnagool** - *Initial work*

See also the list of [contributors](https://github.com/puttsk/codegen/graphs/contributors) who participated in this project.

## Issues / Feature request

You can submit bug / issues / feature request using [Tracker](https://github.com/puttsk/codegen/issues).

## License

[MIT License](LICENSE)

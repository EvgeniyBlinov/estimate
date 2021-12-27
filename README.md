[![MIT License][license-image]][license-url]

# Estimate

Small meta-language for the recording estimate and evaluation of the execution time of the project.

##Install

```sh
python3 -m pip install git+https://github.com/EvgeniyBlinov/estimate.git
```

Local

```sh
python3 -m venv .python
source .python/bin/activate
python3 -m pip install git+https://github.com/EvgeniyBlinov/estimate.git
```

## Usage 

```sh
curl -sS https://raw.githubusercontent.com/EvgeniyBlinov/estimate/master/example.txt |estimate
```

Advanced usage

```sh
# set hour rate to 10$
# set exchange rate for 1 USD from cbr.ru
# apply rate to hours file example.txt
cat \
    <(echo "set hour_rate = 10") \
    <(echo "set exchange_rate = `curl -s https://www.cbr-xml-daily.ru/daily_json.js|jq .Valute.USD.Value`") \
    <(curl -sS https://raw.githubusercontent.com/EvgeniyBlinov/estimate/master/tests/example.txt) |
    estimate
```

Result

```sh
set hour_rate = 10
set exchange_rate = 66.9685
Some information may be here (not hours)      === 1
#########################  BEGIN HOURS  ########################################
/*******************             2016-01-26        ****************************/
--- ERA BEGIN main-app
server side settings                          === 2
vagrant(#admin)                               === 1
TOTAL: 3.0
paid $$$ 20
vagrant                                       === 2
--- EPOCH BEGIN require.js
add doctrine migrations(#admin)               === 1
add javascript APP.settings(#js-notwp)        === 1
add js functions & notifications(#js-notwp)   === 1
/*******************             2016-02-03        ****************************/
revision symfony/gulp & rm cache(#js-notwp)   === 2
/*******************             2016-02-04        ****************************/
require.js + datatables bug(#js-notwp)        === 2
/*******************             2016-02-05        ****************************/
require.js + datatables bug(#js-notwp)        === 1.5
require.js routing page(#js-notwp)            === 1
/*******************             2016-02-07        ****************************/
task with time only                           --- 10:00-11:19 === 1.3
task with time only                           --- 11:19-12:00 === 0.7
--- EPOCH END require.js
--- ERA END main-app
______________________________________________________
ERA_main-app: 16.5
EPOCH_require.js: 11.5
TAGS:
    admin: 2.0
    js-notwp: 8.5
TAGS_TOTAL:10
______________________________________________________
TOTAL HOURS: 16.5
TOTAL PAID: 20
TOTAL REST: 145.0
TOTAL MONEY: 145.0
#########################  END HOURS  ##########################################

Some tasks may be here (not hours)     === 1
Or other description   (not hours too) === 1
```

## Example

[./tests/example.txt](./tests/example.txt)

```sh
Some information may be here (not hours)      === 1
#########################  BEGIN HOURS  ########################################
/*******************             2016-01-26        ****************************/
--- ERA BEGIN main-app
server side settings                          === 2
vagrant(#admin)                               === 1
paid $$$ 20
vagrant                                       === 2
--- EPOCH BEGIN require.js
add doctrine migrations(#admin)               === 1
add javascript APP.settings(#js-notwp)        === 1
add js functions & notifications(#js-notwp)   === 1
/*******************             2016-02-03        ****************************/
revision symfony/gulp & rm cache(#js-notwp)   === 2
/*******************             2016-02-04        ****************************/
require.js + datatables bug(#js-notwp)        === 2
/*******************             2016-02-05        ****************************/
require.js + datatables bug(#js-notwp)        === 1.5
require.js routing page(#js-notwp)            === 1
/*******************             2016-02-07        ****************************/
task with time only                           --- 10:00-11:19
task with time only                           --- 11:19-12:00
--- EPOCH END require.js
--- ERA END main-app
#########################  END HOURS  ##########################################

Some tasks may be here (not hours)     === 1
Or other description   (not hours too) === 1
```

Result

```
______________________________________________________
ERA_main-app: 14
EPOCH_require.js: 9
TAGS:
    admin: 2
    js-notwp: 8
TAGS_TOTAL:10
______________________________________________________
TOTAL: 14
TOTAL PAID: 20
TOTAL REST: 120
```

## Tools

[Vim snippets for estimate](https://github.com/EvgeniyBlinov/vim/blob/master/snippets/_.snippets)

### DEBUG

```
python3 -m pip install estimate --no-index --find-links file://${PWD}
```

### @TODO

- add score for every hour_rate

## License

[![MIT License][license-image]][license-url]

## Author

- [Blinov Evgeniy](mailto:evgeniy_blinov@mail.ru) ([http://blinov.in.ua/](http://blinov.in.ua/))

[license-image]: http://img.shields.io/badge/license-MIT-blue.svg?style=flat
[license-url]: LICENSE

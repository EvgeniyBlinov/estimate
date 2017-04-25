[![MIT License][license-image]][license-url]

# Estimate

Small meta-language for the recording estimate and evaluation of the execution time of the project.

##Install

```sh
curl -sS https://raw.githubusercontent.com/EvgeniyBlinov/estimate/master/bin/estimate  > /usr/local/bin/estimate
chmod +x /usr/local/bin/estimate
```

## Usage 

```sh
curl -sS https://raw.githubusercontent.com/EvgeniyBlinov/estimate/master/example.txt |estimate
```

## Example

[example.txt](example.txt)

```sh
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
require.js + datatables bug(#js-notwp)        === 1
require.js routing page(#js-notwp)            === 1
/*******************             2016-02-07        ****************************/
--- EPOCH END require.js
--- ERA END main-app
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

## License

[![MIT License][license-image]][license-url]

## Author

- [Blinov Evgeniy](mailto:evgeniy_blinov@mail.ru) ([http://blinov.in.ua/](http://blinov.in.ua/))

[license-image]: http://img.shields.io/badge/license-MIT-blue.svg?style=flat
[license-url]: LICENSE

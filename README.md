# django-exportjsonmixin
_a mixin for Django models allowing to export the tables as json_

## Installation

This library has been tested with `Python 3.4` and `Python 3.5` and `Django 1.9.2`. Other versions
might work, albeit not Python 2.

## Usage

### Direct

Export the whole table

    class MyModel(models.Model)
        ...
        
    json = json_export(MyModel)
    
Export a subset

    json = json_export( MyModel, MyModel.objects.filter(some_field=100) )

### As mixin

Export the whole table

    class MyModel(ExportJsonMixin, models.Model)
        ...
        
    json = MyModel.json_export()
    
Export a subset

    json = MyModel.json_export( MyModel.objects.filter(some_field=100) )



## Contributions
Contributions welcome. Send us a pull request!

## Change Log
The idea is to use [semantic versioning](http://semver.org/), even though initially we might make some minor
API changes without bumping the major version number. Be warned!

- **v2.0** separate the json export code into a separate function that can be be used without need for a mixin
- **v1.0** initial version 

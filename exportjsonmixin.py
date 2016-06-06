"""
ExportJson - Export (and import) data tables associated to Django models to (and from) JSON

The functionality either exists in form of a function that takes a model as an argument,
or it can be directly implemented into a model as a mixin

Copyright (c) Stefan LOESCH, oditorium 2016. All rights reserved.
Licensed under the Mozilla Public License, v. 2.0 <https://mozilla.org/MPL/2.0/>
"""
__version__="2.1"
__version_dt__="2016-06-06"

from datetime import datetime, date
import json

##############################################################################################
## HELPER FUNCTIONS

# JSON ENCODER
class JsonEncoder(json.JSONEncoder):
    """
    a JSON encoder that can handle datetime objects

    USAGE
        data = ...
        json.dumps(data, cls=_JsonEncoder)
    
    see <http://stackoverflow.com/questions/11875770/how-to-overcome-datetime-datetime-not-json-serializable-in-python>
    """
    def default(self, o):
        if isinstance(o, datetime) or isinstance(o, date):
            return o.isoformat()
        return json.JSONEncoder.default(self, o)

# JSON DUMPS
def json_dumps(data):
    """
    json encodes the data using _JsonEncoder
    """
    return json.dumps(data, cls=JsonEncoder)


##############################################################################################
## DATA EXPORT 
def data_export(model, query_set=None, return_fields=False):
    """
    export the table associated to the model as data

    NOTES
    - if `query_set` is given only those items are exported, otherwise the whole table is
    """
    # https://docs.djangoproject.com/en/1.9/ref/models/fields/#django.db.models.Field
    # https://docs.djangoproject.com/en/1.9/ref/models/fields/#attributes-for-fields
    fields = [(f.name, not f.is_relation) for f in model._meta.get_fields() if f.concrete and not f.hidden]
    #print (fields)
    if query_set == None: query_set = model.objects.all()
    data = [
        { f[0] if f[1] else f[0]+"__id": 
                getattr(r, f[0]) if f[1] else getattr(getattr(r, f[0]), 'id', None) 
                        for f in fields
        } 
        for r in query_set
    ]
        # either get the value, or--for related field--the id
    if return_fields: return fields, data
    return data


##############################################################################################
## JSON EXPORT 
def json_export(model, query_set=None, as_dict=True, as_object=False):
    """
    export the table associated to the model as Json

    NOTES
    - if `query_set` is given only those items are exported, otherwise the whole table is
    - if `as_dict` is false'ish then the export is a list of dicts (one per record); if it
        is true'ish, this list is wrapped in a dict with key being the class name 
    - if `as_object` is true'ish then an object is returned, not JSON (the idea being that
        this allow combining multiple tables into one Json string)
    """
    data = data_export(model, query_set)
    #print (data)
    if as_dict: data = {model.__name__: data}
    if as_object: return data
    return json_dumps(data)



##############################################################################################
## TSV EXPORT 
def tsv_export(model, query_set=None, heading_row=True):
    """
    export the table associated to the model as tsv

    NOTES
    - if `query_set` is given only those items are exported, otherwise the whole table is
    """
    data = data_export(model, query_set)
    if not data: return ""
    fields = data[0].keys()
    tsv = "\n".join([
            "\t".join(['"{}"'.format(row[f]) if isinstance(row[f], str) else str(row[f]) for f in fields])
    for row in data])
    tsv = "\t".join([f for f in fields])+"\n"+tsv
    return tsv


##############################################################################################
## EXPORT JSON MIXIN
class ExportJsonMixin():
    """
    export the data table to Json, and import it

    DEFINES
    - json_export: the export function
    - json_import: the import function
    - json_clear_all: clears the entire table (!!!)
    - json_encoder: a JSONEncoder object that can handle datetime
    
    """

    @classmethod
    def json_export(cls, query_set=None, as_dict=True, as_object=False):
        """
        export the table associated to the model as Json

        (see `json_export` function in this module for details)
        """
        return json_export(cls, query_set, as_dict, as_object)

    @classmethod
    def data_export(cls, query_set=None):
        """
        export the table associated to the model as data

        (see `data_export` function in this module for details)
        """
        return data_export(cls, query_set)

    @classmethod
    def tsv_export(cls, query_set=None):
        """
        export the table associated to the model as tsv

        (see `tsv_export` function in this module for details)
        """
        return tsv_export(cls, query_set)
    
    @classmethod
    def json_import(cls, json, clear_current=False):
        """
        imports the current data table from Json
        
        NOTES
        - if clear_current is true'ish all of the current data is overwritten
        """
        raise NotImplementedError()

    @classmethod
    def json_clear_all(cls):
        """
        clears the current data table (really! there is no way back)
        """
        raise NotImplementedError()

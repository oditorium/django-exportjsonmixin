"""
tests for ExportJsonMixin

Copyright (c) Stefan LOESCH, oditorium 2016. All rights reserved.
Licensed under the Mozilla Public License, v. 2.0 <https://mozilla.org/MPL/2.0/>
"""


from django.test import TestCase, RequestFactory
from django.conf import settings
#from django.core.signing import Signer, BadSignature
#from django.contrib.auth.models import User
#from django.core.urlresolvers import reverse_lazy, reverse
#from Presmo.tools import ignore_failing_tests, ignore_long_tests
#from Presmo.tools import ModelToolsMixin

import json

from .models import *

Model = Issue
RelatedModel = Owner

#from .crudmixin import Token, TokenSignatureError, TokenFormatError, TokenDefinitionError, TokenPermissionError


#########################################################################################
## TOKEN TEST
class ExportJsonMixinTest(TestCase):
    """test the Token helper class"""

    def setUp(s):
        rr = RelatedModel()
        rr.name = 'rmname1'
        rr.save()
        r = Model()
        r.name = "name1"
        r.description = "item1"
        r._owned_by = rr
        r.save()

    def test_export_rm(s):
        """test exporting the (simple!) related model"""
        data_json = RelatedModel.json_export()
        #print (data_json)
        data = json.loads(data_json)
        #print (data)
        di = data['Owner']
        s.assertEqual(len(di), 1)
        s.assertEqual(di[0]['id'], 1)
        s.assertEqual(di[0]['name'], 'rmname1')
        
    def test_export(s):
        """test exporting the (more complex!) main model"""
        data_json = Model.json_export()
        #print (data_json)
        data = json.loads(data_json)
        #print (data)
        #s.assertEqual(data.keys()=["Issue"])
        di = data['Issue']
        s.assertEqual(len(di), 1)
        s.assertEqual(di[0]['id'], 1)
        s.assertEqual(di[0]['description'], 'item1')
        s.assertEqual(di[0]['name'], 'name1')
        s.assertEqual(di[0]['_owned_by__id'], 1)


        


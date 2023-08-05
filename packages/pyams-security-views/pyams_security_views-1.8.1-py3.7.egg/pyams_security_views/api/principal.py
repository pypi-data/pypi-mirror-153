#
# Copyright (c) 2015-2020 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

"""PyAMS_security_views.api.principal module

This module only provides a small Cornice API to search for principals.
"""

import sys

from colander import MappingSchema, SchemaNode, SequenceSchema, String
from cornice import Service
from cornice.validators import colander_querystring_validator
from pyramid.httpexceptions import HTTPOk

from pyams_security.interfaces import ISecurityManager
from pyams_security.interfaces.base import VIEW_SYSTEM_PERMISSION
from pyams_security.rest import check_cors_origin, set_cors_headers
from pyams_security_views.interfaces import REST_PRINCIPALS_SEARCH_ROUTE
from pyams_utils.registry import query_utility


__docformat__ = 'restructuredtext'

from pyams_security_views import _  # pylint: disable=ungrouped-imports


TEST_MODE = sys.argv[-1].endswith('/test')


class PrincipalsSearchQuerySchema(MappingSchema):
    """Principals search schema"""
    term = SchemaNode(String(),
                      description=_("Principals search string"))


class PrincipalResultSchema(MappingSchema):
    """Principal result schema"""
    id = SchemaNode(String(),
                    description=_("Principal ID"))
    text = SchemaNode(String(),
                      description=_("Principal title"))


class PrincipalsSearchResults(SequenceSchema):
    """Principals search results interface"""
    result = PrincipalResultSchema()


class PrincipalsSearchResultsSchema(MappingSchema):
    """Principals search results schema"""
    results = PrincipalsSearchResults(description=_("Results list"))


search_responses = {
    HTTPOk.code: PrincipalsSearchResultsSchema(description=_("Search results")),
}
if TEST_MODE:
    service_params = {}
else:
    service_params = {
        'response_schemas': search_responses
    }


service = Service(name=REST_PRINCIPALS_SEARCH_ROUTE,
                  pyramid_route=REST_PRINCIPALS_SEARCH_ROUTE,
                  description="Principals management")


@service.options(validators=(check_cors_origin, set_cors_headers),
                 **service_params)
def principals_options(request):  # pylint: disable=unused-argument
    """Principals service options"""
    return ''


@service.get(permission=VIEW_SYSTEM_PERMISSION,
             schema=PrincipalsSearchQuerySchema(),
             validators=(check_cors_origin, colander_querystring_validator, set_cors_headers),
             **service_params)
def get_principals(request):
    """Returns list of principals matching given query"""
    if TEST_MODE:
        query = request.params.get('term')
    else:
        query = request.validated.get('term')
    if not query:
        return []
    manager = query_utility(ISecurityManager)
    return {
        'results': [{
            'id': principal.id,
            'text': principal.title
        } for principal in manager.find_principals(query)]
    }

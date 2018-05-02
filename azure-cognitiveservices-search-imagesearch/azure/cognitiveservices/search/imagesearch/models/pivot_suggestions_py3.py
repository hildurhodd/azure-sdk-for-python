# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class PivotSuggestions(Model):
    """Defines the pivot segment.

    All required parameters must be populated in order to send to Azure.

    :param pivot: Required. The segment from the original query to pivot on.
    :type pivot: str
    :param suggestions: Required. A list of suggested queries for the pivot.
    :type suggestions:
     list[~azure.cognitiveservices.search.imagesearch.models.Query]
    """

    _validation = {
        'pivot': {'required': True},
        'suggestions': {'required': True},
    }

    _attribute_map = {
        'pivot': {'key': 'pivot', 'type': 'str'},
        'suggestions': {'key': 'suggestions', 'type': '[Query]'},
    }

    def __init__(self, *, pivot: str, suggestions, **kwargs) -> None:
        super(PivotSuggestions, self).__init__(**kwargs)
        self.pivot = pivot
        self.suggestions = suggestions

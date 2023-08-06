# coding: utf-8

import json

from tapioca import (
    TapiocaAdapter, generate_wrapper_from_adapter, JSONAdapterMixin)


from .resource_mapping import RESOURCE_MAPPING


class TeamCultureClientAdapter(JSONAdapterMixin, TapiocaAdapter):
    resource_mapping = RESOURCE_MAPPING

    def get_api_root(self, api_params, **kwargs):
        
        if kwargs.get('resource_name') in ['user_create', 'group_create']:
            data_url = 'data-import'
        else:
            data_url = 'data'
        
        if api_params.get('dev'):
            return f'https://stage-{data_url}.teamculture.com.br/'
        return f'https://{data_url}.teamculture.com.br/'

    def format_data_to_request(self, data):
        if data:
            return json.dumps(data)

    def get_request_kwargs(self, api_params, *args, **kwargs):
        params = super(TeamCultureClientAdapter, self).get_request_kwargs(
            api_params, *args, **kwargs)

        params.setdefault('params', {}).update(
            {'token': api_params.get('token', '')}
        )

        return params

    def get_iterator_list(self, response_data):

        if 'users' in response_data:
            return response_data.get('users')

        return response_data

    def get_iterator_next_request_kwargs(self, iterator_request_kwargs, response_data, response):

        params = iterator_request_kwargs.get('params', {})

        if 'offset' in params:
            limit = 100
            params = iterator_request_kwargs.get('params',
                                                 {'limit': limit,
                                                  'offset': +limit})
            params['offset'] = params['limit'] + params['offset']

        if 'page' in params:
            params = iterator_request_kwargs.get('params',
                                                 {'page': 1,
                                                  'perPage': 1000})
            params['page'] = params['page'] + 1

        iterator_request_kwargs['params'] = params

        return iterator_request_kwargs


TeamCulture = generate_wrapper_from_adapter(TeamCultureClientAdapter)

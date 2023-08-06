from pydantic import BaseModel


class Base(BaseModel):
    def to_dict(self):
        self_dict = self.dict()
        name = self_dict.pop('Name')
        return {name: self_dict}


class Api:
    swagger = "2.0"
    info = {}
    host = ""
    schemes = ""
    paths = ""
    definitions = ""
    securityDefinitions = ""
    x_amazon_apigateway_request_validators = ""


swagger_template = {'swagger': '2.0',
                    'info': {'title': 'API',
                             'description': 'API description.',
                             'version': '1.0.0'},
                    'host': 'api.example.com',
                    'schemes': ['https'],
                    'paths': {},
                    'definitions': {'Empty': {'type': 'object', 'title': 'Empty Schema'}},
                    'securityDefinitions': {'api_key': {'type': 'apiKey',
                                                        'name': 'x-api-key',
                                                        'in': 'header'}},
                    'x-amazon-apigateway-request-validators': {
                        'Validate query string parameters and headers': {'validateRequestParameters': True,

                                                                         'validateRequestBody': False},
                        'Validate body, query string parameters, and headers': {'validateRequestParameters': True,
                                                                                'validateRequestBody': True},
                        'Validate body': {'validateRequestParameters': False,
                                          'validateRequestBody': True}}}

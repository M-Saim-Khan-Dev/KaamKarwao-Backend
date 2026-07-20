from drf_spectacular.extensions import OpenApiAuthenticationExtension

class GatewayHeaderAuthenticationScheme(OpenApiAuthenticationExtension):
    target_class = 'Earning.authentication.GatewayHeaderAuthentication'
    name = 'bearerAuth'

    def get_security_definition(self, auto_schema):
        return {
            'type': 'http',
            'scheme': 'bearer',
            'bearerFormat': 'JWT',
            'description': 'JWT issued by UserService, sent via the API Gateway',
        }
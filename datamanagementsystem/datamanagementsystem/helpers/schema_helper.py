from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import InvalidToken
from ..models.organization import Organization

def get_tenant_schema(request):
    auth_header = request.META.get('HTTP_AUTHORIZATION')
    if auth_header is None:
        return
    parts = auth_header.split()
    if len(parts) == 2 and parts[0].lower() == 'bearer':
        token = parts[1]
        access_token = AccessToken(token)
        organization_id = access_token['organization_id']
        if organization_id is None:
            raise InvalidToken()
        organization = Organization.objects.get(id=organization_id)
        if organization is None:
            raise InvalidToken()
        return organization.name
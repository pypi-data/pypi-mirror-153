from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated

from drf_temptoken.auth import TempTokenAuthentication

@api_view(http_method_names=('GET',))
@permission_classes((IsAuthenticated,))
@authentication_classes((TempTokenAuthentication,))
def check_auth(request):
    return Response(status=status.HTTP_204_NO_CONTENT)

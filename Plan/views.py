from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import ErrorSerializer, WorkVolumeRequestSerializer
from .services import AccessDenied, FactoryNotFound, save_work_volume

ERROR_FACTORY_NOT_FOUND = 174
ERROR_FIELDS_REQUIRED = 279


class WorkVolumeListView(APIView):
    authentication_classes = []  # авторизации нет
    parser_classes = [JSONParser]

    @extend_schema(
        summary="Сохранить объем работ",
        request=WorkVolumeRequestSerializer,
        responses={
            201: OpenApiResponse(description="Объем работ сохранен"),
            403: OpenApiResponse(description="Пользователь не найден или не в группе"),
            404: OpenApiResponse(ErrorSerializer, description="ЗМК не существует, errorCode=174"),
            406: OpenApiResponse(ErrorSerializer, description="Не заполнены обязательные поля, errorCode=279",),
        },
    )
    def post(self, request):
        serializer = WorkVolumeRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"errorCode": ERROR_FIELDS_REQUIRED},
                status=status.HTTP_406_NOT_ACCEPTABLE,
            )

        data = serializer.validated_data
        try:
            save_work_volume(
                factory_id=data["factory"],
                start=data["start"],
                finish=data["finish"],
                weight=data["weight"],
                author_id=data["author"],
            )
        except FactoryNotFound:
            return Response(
                {"errorCode": ERROR_FACTORY_NOT_FOUND},
                status=status.HTTP_404_NOT_FOUND,
            )
        except AccessDenied:
            return Response(status=status.HTTP_403_FORBIDDEN)

        return Response(status=status.HTTP_201_CREATED)


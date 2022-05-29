from rest_framework.viewsets import ModelViewSet

from elnure_config import models, serializers


class ApplicationWindowViewSet(ModelViewSet):
    """
    Application Window view set

    retrieve: Get an application window by given id
    list: Get all application widows
    create: Create an application window
    update: Update an application window by id
    partial_update: Update only some fields of an application window by id
    delete: Delete an application window by id
    """

    serializer_class = serializers.ApplicationWindowSerializer
    queryset = models.ApplicationWindow.objects
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import viewsets, status
from rest_framework.response import Response
from trips.models import TravelProject, ProjectPlace
from trips.serializers import TravelProjectSerializer, ProjectPlaceSerializer


class TravelProjectViewSet(viewsets.ModelViewSet):
    queryset = TravelProject.objects.prefetch_related("places")
    serializer_class = TravelProjectSerializer

    def destroy(self, request, *args, **kwargs):
        project = self.get_object()

        try:
            project.delete()
        except DjangoValidationError as e:
            return Response(
                {"detail": e.message},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(status=status.HTTP_204_NO_CONTENT)


class ProjectPlaceViewSet(viewsets.ModelViewSet):
    queryset = ProjectPlace.objects.select_related("project")
    serializer_class = ProjectPlaceSerializer

    def perform_update(self, serializer):
        place = serializer.save()
        project = place.project

        if project.places.exists() and not project.places.filter(visited=False).exists():
            project.completed = True
            project.save()
        else:
            project.completed = False
            project.save()

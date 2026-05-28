from rest_framework import serializers
from trips.models import TravelProject, ProjectPlace


class ProjectPlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectPlace
        fields = ("id", "external_id", "name", "notes", "visited")


class TravelProjectSerializer(serializers.ModelSerializer):
    places = ProjectPlaceSerializer(many=True, required=False)

    class Meta:
        model = TravelProject
        fields = ("id", "name", "description", "start_date", "completed", "places")

    def create(self, validated_data):
        places_data = validated_data.pop("places", [])
        project = TravelProject.objects.create(**validated_data)

        for place_data in places_data:
            ProjectPlace.objects.create(project=project, **place_data)

        return project

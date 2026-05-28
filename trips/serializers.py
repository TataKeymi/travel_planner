import requests
from rest_framework import serializers
from trips.models import TravelProject, ProjectPlace


class NestedProjectPlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectPlace
        fields = ("id", "external_id", "name", "notes", "visited")

    def validate_external_id(self, external_id):
        url = f"https://api.artic.edu/api/v1/artworks/{external_id}"
        response = requests.get(url)

        if response.status_code != 200:
            raise serializers.ValidationError(
                "Place with this external_id does not exist."
            )

        return external_id


class ProjectPlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectPlace
        fields = ("id", "project", "external_id", "name", "notes", "visited")

    def validate_external_id(self, external_id):
        url = f"https://api.artic.edu/api/v1/artworks/{external_id}"
        response = requests.get(url)

        if response.status_code != 200:
            raise serializers.ValidationError(
                "Place with this external_id does not exist."
            )

        return external_id


class TravelProjectSerializer(serializers.ModelSerializer):
    places = NestedProjectPlaceSerializer(many=True, required=False)

    class Meta:
        model = TravelProject
        fields = ("id", "name", "description", "start_date", "completed", "places")

    def validate_places(self, places):
        if len(places) > 10:
            raise serializers.ValidationError(
                "Project cannot contain more than 10 places."
            )
        return places

    def create(self, validated_data):
        places_data = validated_data.pop("places", [])
        project = TravelProject.objects.create(**validated_data)

        for place_data in places_data:
            ProjectPlace.objects.create(project=project, **place_data)

        return project

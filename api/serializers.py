from rest_framework import serializers
from projects.models import Project, Tag, Review
from users.models import Profile

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

# modelserializer konvertiert das Project model in ein json-objekt
class ProjectSerializer(serializers.ModelSerializer):
    owner = ProfileSerializer(many=False) # returned ein object im feld owner
    tags = TagSerializer(many=True)

    # brauchen wir um eine Methode zu erstelen, methode ist unten und muss imme rmit get anfangen
    reviews = serializers.SerializerMethodField()


    class Meta:
        model = Project
        fields = '__all__'

    # self ist die Klasse ProjectSerializer, obj ist das model Project
    # wird ann auch zum JSON hinzugefügt
    def get_reviews(self, obj):
        reviews = obj.review_set.all()
        serializer = ReviewSerializer(reviews, many=True)

        return serializer.data


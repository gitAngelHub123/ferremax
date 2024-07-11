from rest_framework.serializers import ModelSerializer
from app.models import Post

class PostSerializer(ModelSerializer):
    
    class Meta:
        model = Post
        fields = '__all__'  # Incluye todos los campos del modelo en el serializador
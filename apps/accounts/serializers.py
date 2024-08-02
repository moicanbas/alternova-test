from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'identification', 'first_name', 'last_name', 'email', 'groups', 'user_permissions', 'is_teacher', 'is_student', 'cellphone', 'password']
        read_only_fields = ['id']
        extra_kwargs = {'password': {'write_only': True}}

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['identification'] = instance.get_encrypted_field(instance.identification)
        representation['id'] = instance.get_encrypted_field(str(instance.id))
        representation['username'] = instance.get_encrypted_field(instance.username)
        representation['cellphone'] = instance.get_encrypted_field(instance.cellphone)
        return representation

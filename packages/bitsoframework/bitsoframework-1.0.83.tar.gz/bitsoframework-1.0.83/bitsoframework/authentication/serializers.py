from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework import serializers, fields


class UpdatePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True, max_length=128)
    new_password = serializers.CharField(required=True, max_length=128)

    def validate_current_password(self, current_password):
        user = self.context.get("request").user

        if not user.check_password(current_password):
            self.fail("invalid")

        return current_password

    def update_password(self):
        user = self.context.get("request").user
        user.set_password(self.validated_data.get("new_password"))
        user.save(update_fields=["password"])


class AbstractForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def get_token(self, user):
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        token_base64 = urlsafe_base64_encode(force_bytes("%s:%s" % (uid, token)))
        return token_base64


class ResetPasswordSerializer(serializers.ModelSerializer):
    password = fields.CharField(required=True)
    token = fields.CharField(required=True)

    class Meta:
        model = get_user_model()
        fields = ('password', 'token')

    def validate_token(self, base64_token):

        try:
            tokens = urlsafe_base64_decode(base64_token).decode().split(":")

            pk = urlsafe_base64_decode(tokens[0]).decode()
            token = tokens[1]

            user = get_user_model().objects.filter(pk=pk).get()

            if not default_token_generator.check_token(user, token):
                self.fail("invalid")

            return user

        except Exception as e:
            self.fail("invalid")

    def reset_password(self):

        user = self.validated_data.get("token")
        password = self.validated_data.get("password")

        user.set_password(raw_password=password)
        user.save(update_fields=['password'])

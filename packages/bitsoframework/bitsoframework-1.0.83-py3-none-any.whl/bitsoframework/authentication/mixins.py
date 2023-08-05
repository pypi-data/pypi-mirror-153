from django.contrib.auth import logout
from rest_framework.decorators import action
from rest_framework.response import Response


class LogoutViewMixin(object):

    @action(methods=["post"], detail=False, permission_classes=[])
    def logout(self, request):
        logout(request)

        return Response("OK")


class UpdatePasswordViewMixin(object):
    @action(methods=["post"], detail=False)
    def update_password(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.update_password()

        return Response("OK")


class ForgotPasswordViewMixin(object):
    @action(methods=["post"], detail=False, permission_classes=[])
    def forgot_password(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.forgot_password()

        return Response("OK")


class ResetPasswordViewMixin(object):
    @action(methods=["post"], detail=False, permission_classes=[])
    def reset_password(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.reset_password()

        return Response("OK")

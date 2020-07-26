from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token


class ManageTokensView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/manage-tokens.html'


class CreateTokenView(APIView):
    def post(self, request):
        with transaction.atomic():
            try:
                auth_token = request.user.auth_token
                auth_token.delete()
            except Token.DoesNotExist:
                pass

            auth_token = Token.objects.create(user=request.user)

        return Response({ 'token': auth_token.key })

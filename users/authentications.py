
from rest_framework import status
from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import authentication_classes, permission_classes
from drf_yasg.utils import swagger_auto_schema
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.tokens import default_token_generator

from . import serializers
from .requests_permissions import RequestsPermissions

from utils.user.user_type_util import UserType
from utils.endpoints_util import EndpointsUtils
from utils.user.authentication import create_token_response, create_valid_token_response, generate_link_to_reset_password
from utils.email.send_email import send_email_reset_password, send_email_first_access_password

from users.models import CustomUser

class Authentication(ObtainAuthToken):

    @swagger_auto_schema(responses={200: serializers.AuthenticationTokenSerializerForDocs()})
    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data,
                                            context={'request': request})

            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user']
            token, _ = Token.objects.get_or_create(user=user)
        except Exception as error:
            return Response({'detail': f'Unable to log in with provided credentials: {str(error)}'}, status.HTTP_401_UNAUTHORIZED)

        try:
            UserType.is_valid_user_type(user.type)
            response = Authentication._create_and_update_login_response(token.key, user.id, user.email, user.first_name, user.last_name, user.type)

            return Response(response)
        except Exception as error:
            return Response({'authentication error': f'{str(error)}'}, status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(query_serializer=serializers.AuthenticationGetTokenParamsSerializer,
                        responses={200: serializers.AuthenticationGetTokenSerializerForDocs()})
    def get(self, request, *args, **kwargs):
        params_serializer = serializers.AuthenticationGetTokenParamsSerializer(data=request.data)
        if not params_serializer.is_valid():
            return Response(params_serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        try:
            Token.objects.get(pk=request.data['token'])

            is_valid_token = True
        except ObjectDoesNotExist:
            is_valid_token = False

        response = create_valid_token_response(is_valid_token)

        return Response(response)

    def _create_and_update_login_response(token, user_id, user_email, user_first_name, user_last_name, user_type):
        response = create_token_response(token, user_id, user_email, user_first_name, user_last_name, user_type)

        if user_type in RequestsPermissions.university_user_permissions:
            user = RequestsPermissions.get_university_user_object(user_id)
            university_id = user.university.id

            response = Authentication._update_university_user_response(response, university_id)

        return response

    def _update_super_user_response(response):
        return response

    def _update_university_user_response(response, university_id):
        response = Authentication._insert_university_id_on_response(response, university_id)
        
        return response

    def _insert_university_id_on_response(response, university_id):
        response['user']['universityId'] = university_id

        return response


class Password():
    def generate_password_token(user):
        user = Password._invalid_all_generated_tokens(user)
        
        return default_token_generator.make_token(user = user)

    def generate_link_to_reset_password(user: str, token: str or None):
        if not token:
            raise Exception('Is necessary a password token')

        if not Password.check_password_token_is_valid(user, token):
            raise Exception('Password token is not valid')

        return generate_link_to_reset_password(token, user.email)

    def check_password_token_is_valid(user, token):
        return default_token_generator.check_token(user, token)

    def change_user_password(user_email, user_new_password, token):
        try:
            user = CustomUser.search_user_by_email(email = user_email)

            user.change_user_password_by_reset_password_token(user_new_password, token)

            Password._invalid_all_generated_tokens(user)
        except Exception as error:
            raise Exception('Change user password: ' + str(error))

    def _invalid_all_generated_tokens(user):
        return user.change_user_last_login_time()

    def send_email_reset_password(email):
        try:
            user = CustomUser.search_user_by_email(email = email)
            token = Password.generate_password_token(user)
            link = Password.generate_link_to_reset_password(user, token)
            
            send_email_reset_password(user.first_name, user.email, link)
        except Exception as error:
            raise Exception('Send email reset password: ' + str(error))

    def send_email_first_access_password(user):
        try:
            token = Password.generate_password_token(user)
            link = Password.generate_link_to_reset_password(user, token)
            
            send_email_first_access_password(user.first_name, user.email, link)
        except Exception as error:
            raise Exception('Send email first access password: ' + str(error))


@authentication_classes([])
@permission_classes([])
class ResetPassword(generics.GenericAPIView):
    @swagger_auto_schema(query_serializer=serializers.ResetPasswordParamsSerializer,
                         responses={200: serializers.ResetPasswordParamsForDocs})
    def post(self, request, *args, **kwargs):
        try:
            request_user_email = request.GET.get('email')

            Password.send_email_reset_password(request_user_email)

            response = EndpointsUtils.create_message_endpoint_response(
                        status = EndpointsUtils.status_success, 
                        message = "Email was sent for user with reset password link")

            return Response(response, status.HTTP_200_OK)
        except Exception as error:
            response = EndpointsUtils.create_message_endpoint_response(
                        status = EndpointsUtils.status_error,
                        message = str(error))

            return Response(response, status.HTTP_400_BAD_REQUEST)


@authentication_classes([])
@permission_classes([])
class ConfirmResetPassword(generics.GenericAPIView):
    @swagger_auto_schema(request_body=serializers.ConfirmPasswordBodySerializer,
                         responses={200: serializers.ResetPasswordParamsForDocs})
    def post(self, request, *args, **kwargs):
        try:
            request_user_email = request.data['user_email']
            request_user_new_password = request.data['user_new_password']
            request_user_reset_password_token = request.data['user_reset_password_token']

            Password.change_user_password(request_user_email, request_user_new_password, request_user_reset_password_token)

            response = EndpointsUtils.create_message_endpoint_response(
                        status = EndpointsUtils.status_success, 
                        message = "User password has been changed")

            return Response(response, status.HTTP_200_OK)
        except Exception as error:
            response = EndpointsUtils.create_message_endpoint_response(
                        status = EndpointsUtils.status_error,
                        message = str(error))

            return Response(response, status.HTTP_400_BAD_REQUEST)

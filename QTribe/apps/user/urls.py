from django.urls import path, re_path
from rest_framework.routers import DefaultRouter

from user.views import Register, Login ,CheckUsername, CheckPhone,Transform,UpdateInformation,CheckEmail,ResetPassword,\
                       CheckPassword,UploadImage,Logout,FocusUser,UserSearchView,MakeFriend,ResponseFriend,RefuseFriend,\
                       ReadMessage
from .views_api import AuthViewSet, UserViewSet, check_username, check_phone, check_email
from .interaction_api import InteractionViewSet


router = DefaultRouter()
router.register(r'auth', AuthViewSet, basename='auth')
router.register(r'user', UserViewSet, basename='user')
router.register(r'interaction', InteractionViewSet, basename='interaction')

urlpatterns=[
   path('register/',Register.as_view()),
   path('login/',Login.as_view()),
   re_path('check_username/(?P<username>[A-Za-z][A-Za-z0-9]{2,7})/',CheckUsername.as_view()),
   re_path(r'check_phone/(?P<phone>1[3589]\d{9})/',CheckPhone.as_view()),
   re_path('check_password/',CheckPassword.as_view()),
   re_path('check_email/(?P<email>[a-z0-9A-Z]+[- | a-z0-9A-Z . _]+@([a-z0-9A-Z]+(-[a-z0-9A-Z]+)?\.)+[a-z]{2,})/',CheckEmail.as_view()),
   path('transform/', Transform.as_view()),
   path('update_information/', UpdateInformation.as_view()),
   path('upload_image/',UploadImage.as_view()),
   path('reset_password/', ResetPassword.as_view()),
   path('logout/', Logout.as_view()),
   path('focus/', FocusUser.as_view()),
   path('make_friend/', MakeFriend.as_view()),
   path('response_friend/', ResponseFriend.as_view()),
   path('refuse_friend/', RefuseFriend.as_view()),
   path('read_message/', ReadMessage.as_view()),
   path('search_user/', UserSearchView()),
   
   # API路由
   path('api/check_username/', check_username),
   path('api/check_phone/', check_phone),
   path('api/check_email/', check_email),
]

# 添加DRF路由
urlpatterns += router.urls
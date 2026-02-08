from django.urls import path, include
from rest_framework.routers import DefaultRouter
from account_management.views.account import AuthViewSet

# 建立一個路由容器
router = DefaultRouter()

# 註冊 AuthViewSet，這會自動生成 /register/ 等路徑
# 因為我們在 ViewSet 裡寫的是 create 方法，對應 HTTP POST
router.register(r'auth', AuthViewSet, basename='auth')

urlpatterns = [
    path('', include(router.urls)),
]
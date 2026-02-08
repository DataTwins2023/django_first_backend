from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from account_management.serializers import RegisterSerializer

class AuthViewSet(viewsets.ViewSet):
    # 註冊帳號不需要權限檢查
    permission_classes = [AllowAny]

    def create(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message": "帳號創建成功",
                "username": user.username,
                "user_id": user.user_id
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
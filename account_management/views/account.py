from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated # 引入認證類別
from rest_framework.decorators import action # 引入 action 裝飾器
from account_management.serializers import RegisterSerializer, UserSerializer

class AuthViewSet(viewsets.ViewSet):
    # 這裡很關鍵：根據「動作」來決定誰可以進門
    def get_permissions(self):
        if self.action == 'create':
            # 註冊帳號時，不需要 Token (所有人都可以存取)
            return [AllowAny()]
        # 其他動作 (如 me)，必須帶著有效的 JWT Token
        return [IsAuthenticated()]
    

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
    
    # 取得個人資料功能 (網址會是 /accounts/auth/me/)
    @action(detail=False, methods=['get'])
    def me(self, request):
        # 因為有 IsAuthenticated 檢查，只要程式跑到這
        # request.user 就一定是當前登入的使用者物件
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    
    # 修改個人資料 (PATCH /accounts/auth/update_me/)
    @action(detail=False, methods=['patch'])
    def update_me(self, request):
        # 此時 request 已經被查驗官處理過了
        # 直接拿到的就是一個「完整的、從資料庫抓出來的」User 物件
        user = request.user
        # partial=True 代表「部分更新」，使用者可以只傳 email，不傳 username
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "資料更新成功",
                "data": serializer.data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # 4. 註銷帳號 (DELETE /accounts/auth/delete_me/)
    @action(detail=False, methods=['delete'])
    def delete_me(self, request):
        user = request.user
        user.delete()
        return Response({
            "message": "帳號已成功刪除，期待下次再見"
        }, status=status.HTTP_204_NO_CONTENT)
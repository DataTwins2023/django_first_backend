from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiParameter, inline_serializer
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from document_management.serializers import UploadFileSerializer, PartialUpdateSerializer
from rest_framework.response import Response
from document_management.models import Document

# 上傳檔案
class DocumentViewSet(ViewSet):
    lookup_field = 'document_id'
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def create(self, request):
        body = UploadFileSerializer(data=request.data)
        try:
            body.is_valid(raise_exception=True)
            file = body.validated_data.get('file')
            display_name = body.validated_data.get('display_name')
            description = body.validated_data.get('description')
        except Exception as e:
            return Response({"error": str(e)}, status=400)
        # 處理檔案上傳邏輯
        document = Document.objects.create(
            file_name=file.name,
            display_name=display_name,
            description=description
        )
        document.save()
        return Response({"message": "File uploaded successfully", "document_name": document.file_name})
    
    def destroy(self, request, document_id=None):
        # body = DeleteFileSerializer(data=request.data)
        try:
            document = Document.objects.get(document_id=document_id)
            document.delete()
        except Document.DoesNotExist:
            return Response({"error": "Document not found"}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=400)
        
        return Response({"message": "File deleted successfully"})
    
    def retrieve(self, request, document_id=None):
        try:
            # 撈出查詢參數
            query = request.query_params.get('display_name')
            document = Document.objects.get(document_id=document_id, display_name = query)
            data = {
                "file_name": document.file_name,
                "display_name": document.display_name,
                "description": document.description,
                "created_at": document.created_at,
                "updated_at": document.updated_at
            }
            return Response(data)
        except Document.DoesNotExist:
            return Response({"error": "Document not found"}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=400)
    
    # 部分更新
    def partial_update(self, request, document_id=None):
        try:
            document = Document.objects.get(document_id=document_id)
        except Document.DoesNotExist:
            return Response({"error": "Document not found"}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=400)

        try:
            # 1. 初始化 Serializer，傳入實例與新資料，並開啟 partial=True
            serializer = PartialUpdateSerializer(document, data=request.data, partial=True)

            # 2. 進行驗證
            # raise_exception=True 會自動在驗證失敗時回傳 400 Error 給前端，省去寫 if/else
            serializer.is_valid(raise_exception=True)

            # 3. 儲存更新後的資料
            # 這會觸發你在 Serializer 中定義的 update() 方法
            serializer.save()

            # 4. 回傳更新後的結果與 200 OK
            return Response(serializer.data, status=200)

        except Exception as e:
            return Response({"error": str(e)}, status=400)

            
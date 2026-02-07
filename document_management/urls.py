from django.urls import path
from rest_framework.routers import DefaultRouter
from document_management.views.document import DocumentViewSet

router = DefaultRouter()

router.register(r'documents', DocumentViewSet, basename='document')
urlpatterns = router.urls
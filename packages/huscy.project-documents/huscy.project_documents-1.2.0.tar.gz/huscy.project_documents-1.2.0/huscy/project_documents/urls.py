from rest_framework.routers import DefaultRouter
from rest_framework.viewsets import GenericViewSet
from rest_framework_nested.routers import NestedDefaultRouter

from huscy.project_documents import views


router = DefaultRouter()
router.register('documenttypes', views.DocumentTypeViewSet)
router.register('projects', GenericViewSet, basename='project')

project_router = NestedDefaultRouter(router, 'projects', lookup='project')
project_router.register('documents', views.DocumentViewSet, basename='document')

urlpatterns = router.urls
urlpatterns += project_router.urls

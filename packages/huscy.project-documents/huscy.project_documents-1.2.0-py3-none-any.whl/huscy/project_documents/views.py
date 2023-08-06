from django.shortcuts import get_object_or_404
from rest_framework import mixins, viewsets
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated
from reversion import set_comment
from reversion.views import RevisionMixin

from huscy.projects.models import Project
from huscy.project_documents import serializer, services
from huscy.project_documents.permissions import ChangeProjectPermissions


class DocumentViewSet(RevisionMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin,
                      mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated, ChangeProjectPermissions)
    serializer_class = serializer.DocumentSerializer

    def initial(self, request, *args, **kwargs):
        self.project = get_object_or_404(Project, pk=self.kwargs['project_pk'])
        super().initial(request, *args, **kwargs)

    def get_queryset(self):
        return services.get_documents(self.project)

    def perform_create(self, serializer):
        document = serializer.save(project=self.project)
        set_comment(f'Created document <ID-{document.id}>')

    def perform_destroy(self, document):
        document.delete()
        set_comment(f'Deleted document <ID-{document.id}')


class DocumentTypeViewSet(RevisionMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin,
                          mixins.ListModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    permission_classes = (DjangoModelPermissions, )
    queryset = services.get_document_types()
    serializer_class = serializer.DocumentTypeSerializer

    def perform_create(self, serializer):
        document_type = serializer.save()
        set_comment(f'Created document type "{document_type.name}"')

    def perform_destroy(self, document_type):
        services.delete_document_type(document_type)
        set_comment(f'Deleted document type "{document_type.name}"')

    def perform_update(self, serializer):
        document_type = serializer.save()
        set_comment(f'Updated document type "{document_type.name}"')

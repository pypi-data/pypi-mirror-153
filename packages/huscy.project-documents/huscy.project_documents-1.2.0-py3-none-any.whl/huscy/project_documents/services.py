from huscy.project_documents.models import Document, DocumentType


def create_document(project, filehandle, document_type, creator):
    filename = filehandle.name.split('/')[-1]

    return Document.objects.create(
        project=project,
        document_type=document_type,
        filehandle=filehandle,
        filename=filename,
        uploaded_by=creator,
    )


def create_document_type(name):
    return DocumentType.objects.create(name=name)


def delete_document_type(document_type):
    document_type.delete()


def get_document_types():
    return DocumentType.objects.order_by('name')


def get_documents(project=None):
    queryset = Document.objects.order_by('uploaded_at')
    if project is None:
        return queryset
    return queryset.filter(project=project)


def update_document_type(document_type, name):
    document_type.name = name
    document_type.save()
    return document_type

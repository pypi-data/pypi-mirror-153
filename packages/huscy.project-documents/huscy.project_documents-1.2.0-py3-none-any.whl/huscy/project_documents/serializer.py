from rest_framework import serializers

from huscy.project_documents import models, services


class DocumentSerializer(serializers.ModelSerializer):
    creator = serializers.HiddenField(default=serializers.CurrentUserDefault())
    document_type_name = serializers.CharField(source='document_type.name', read_only=True)

    class Meta:
        model = models.Document
        fields = (
            'id',
            'creator',
            'document_type',
            'document_type_name',
            'filehandle',
            'filename',
            'project',
            'uploaded_at',
        )
        read_only_fields = 'creator', 'filename', 'uploaded_at', 'project'

    def create(self, validated_data):
        return services.create_document(**validated_data)

    def to_representation(self, document):
        data = super().to_representation(document)
        data['uploaded_by'] = document.uploaded_by.get_full_name()
        return data


class DocumentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DocumentType
        fields = (
            'id',
            'name',
        )

    def create(self, validated_data):
        return services.create_document_type(**validated_data)

    def update(self, document_type, validated_data):
        return services.update_document_type(document_type, **validated_data)

from django.db import migrations, models
import huscy.project_documents.models


class Migration(migrations.Migration):

    dependencies = [
        ('project_documents', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='filehandle',
            field=models.FileField(max_length=255, upload_to=huscy.project_documents.models.Document.get_upload_path),
        ),
        migrations.AlterField(
            model_name='document',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='documenttype',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]

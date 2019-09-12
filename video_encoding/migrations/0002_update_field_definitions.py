# Generated by Django 2.1.3 on 2018-11-16 00:48

from django.db import migrations, models
import django.db.models.deletion
import video_encoding.fields
import video_encoding.models


class Migration(migrations.Migration):

    dependencies = [
        ('video_encoding', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='format',
            name='content_type',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType'),
        ),
        migrations.AlterField(
            model_name='format',
            name='duration',
            field=models.PositiveIntegerField(editable=False, null=True, verbose_name='Duration (s)'),
        ),
        migrations.AlterField(
            model_name='format',
            name='file',
            field=video_encoding.fields.VideoField(editable=False, height_field='height', max_length=2048, upload_to=video_encoding.models.upload_format_to, verbose_name='File', width_field='width'),
        ),
        migrations.AlterField(
            model_name='format',
            name='format',
            field=models.CharField(editable=False, max_length=255, verbose_name='Format'),
        ),
        migrations.AlterField(
            model_name='format',
            name='height',
            field=models.PositiveIntegerField(editable=False, null=True, verbose_name='Height'),
        ),
        migrations.AlterField(
            model_name='format',
            name='object_id',
            field=models.PositiveIntegerField(editable=False),
        ),
        migrations.AlterField(
            model_name='format',
            name='progress',
            field=models.PositiveSmallIntegerField(default=0, editable=False, verbose_name='Progress'),
        ),
        migrations.AlterField(
            model_name='format',
            name='width',
            field=models.PositiveIntegerField(editable=False, null=True, verbose_name='Width'),
        ),
    ]

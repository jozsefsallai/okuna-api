# Generated by Django 2.2.4 on 2019-08-26 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('openbook_posts', '0055_auto_20190826_1426'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postvideo',
            name='thumbnail_height',
            field=models.PositiveIntegerField(default=0, editable=False),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='postvideo',
            name='thumbnail_width',
            field=models.PositiveIntegerField(default=0, editable=False),
            preserve_default=False,
        ),
    ]

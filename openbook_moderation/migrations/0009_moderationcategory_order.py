# Generated by Django 2.2 on 2019-05-26 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('openbook_moderation', '0008_auto_20190521_2107'),
    ]

    operations = [
        migrations.AddField(
            model_name='moderationcategory',
            name='order',
            field=models.PositiveSmallIntegerField(default=99, editable=False),
            preserve_default=False,
        ),
    ]
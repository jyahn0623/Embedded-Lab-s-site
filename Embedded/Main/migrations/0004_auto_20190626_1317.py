# Generated by Django 2.1.2 on 2019-06-26 04:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0003_auto_20190626_1220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='p_birth_date',
            field=models.DateField(null=True, verbose_name='생년월일'),
        ),
    ]

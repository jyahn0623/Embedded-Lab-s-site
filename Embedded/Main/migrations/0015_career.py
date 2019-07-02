# Generated by Django 2.1.2 on 2019-07-02 11:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Main', '0014_auto_20190702_1025'),
    ]

    operations = [
        migrations.CreateModel(
            name='Career',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('c_content', models.CharField(max_length=30, verbose_name='내용')),
                ('c_date', models.DateField(null=True, verbose_name='날짜')),
                ('c_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='이름')),
            ],
        ),
    ]
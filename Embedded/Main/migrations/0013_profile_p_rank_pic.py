# Generated by Django 2.2 on 2019-07-01 23:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0012_schedule_s_finished_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='p_rank_pic',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='Main.RankPicture', verbose_name='계급 사진'),
        ),
    ]

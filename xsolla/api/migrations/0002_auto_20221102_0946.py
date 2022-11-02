# Generated by Django 2.2 on 2022-11-02 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pay',
            name='canceled',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='pay',
            name='order_id',
            field=models.IntegerField(),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='player_id',
            field=models.CharField(max_length=255),
            preserve_default=False,
        )
    ]

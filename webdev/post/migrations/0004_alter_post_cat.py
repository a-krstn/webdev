# Generated by Django 5.0.4 on 2024-05-10 13:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0003_alter_post_cat'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='cat',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='posts', to='post.category', verbose_name='Категория'),
        ),
    ]

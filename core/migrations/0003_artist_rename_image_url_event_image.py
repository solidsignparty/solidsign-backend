# Generated by Django 5.0.4 on 2024-04-23 16:38

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0002_event_uuid'),
    ]

    operations = [
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nickname', models.CharField(max_length=128, unique=True, verbose_name='Никнейм')),
                ('photo', models.ImageField(upload_to='artists/', verbose_name='Фото')),
            ],
            options={
                'verbose_name': 'Артист',
                'verbose_name_plural': 'Артисты',
            },
        ),
        migrations.RenameField(
            model_name='event',
            old_name='image_url',
            new_name='image',
        ),
    ]

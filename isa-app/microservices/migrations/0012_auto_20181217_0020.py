# Generated by Django 2.1 on 2018-12-17 00:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('microservices', '0011_recommendation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recommendation',
            name='recommended',
            field=models.ManyToManyField(related_name='_recommendation_recommended_+', to='microservices.Recommendation'),
        ),
    ]

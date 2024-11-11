# Generated by Django 4.2.3 on 2024-11-09 21:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_center', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='generatedreport',
            options={'verbose_name_plural': 'Generated Report Documents'},
        ),
        migrations.AlterField(
            model_name='paymentdocument',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='documents'),
        ),
    ]

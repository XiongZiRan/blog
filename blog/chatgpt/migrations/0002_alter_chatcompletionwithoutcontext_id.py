# Generated by Django 4.2 on 2023-04-30 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatgpt', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatcompletionwithoutcontext',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
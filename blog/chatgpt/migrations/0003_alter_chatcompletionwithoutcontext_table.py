# Generated by Django 4.2 on 2023-04-30 14:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chatgpt', '0002_alter_chatcompletionwithoutcontext_id'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='chatcompletionwithoutcontext',
            table='tb_chatcompletion_without_context',
        ),
    ]

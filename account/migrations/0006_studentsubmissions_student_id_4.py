# Generated by Django 5.1.6 on 2025-03-05 04:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_studentsubmissions_student_ids'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentsubmissions',
            name='student_id_4',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]

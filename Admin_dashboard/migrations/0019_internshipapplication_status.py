# Generated by Django 5.1.1 on 2024-10-17 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Admin_dashboard', '0018_alter_jobformsubmission_willing_to_relocate'),
    ]

    operations = [
        migrations.AddField(
            model_name='internshipapplication',
            name='status',
            field=models.CharField(choices=[('unreviewed', 'Unreviewed'), ('shortlisted', 'Shortlisted'), ('rejected', 'Rejected')], default='unreviewed', max_length=50),
        ),
    ]

# Generated by Django 5.1.1 on 2024-10-17 05:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Admin_dashboard', '0014_life_at_pinesphere_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobformsubmission',
            name='status',
            field=models.CharField(choices=[('unreviewed', 'Unreviewed'), ('shortlisted', 'Shortlisted'), ('rejected', 'Rejected')], default='unreviewed', max_length=50),
        ),
    ]

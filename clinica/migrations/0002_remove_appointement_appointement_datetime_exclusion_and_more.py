# Generated by Django 4.0.5 on 2022-06-28 12:39

import clinica.models
import django.contrib.postgres.constraints
import django.contrib.postgres.fields.ranges
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clinica', '0001_initial'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='appointement',
            name='appointement_datetime_exclusion',
        ),
        migrations.AddConstraint(
            model_name='appointement',
            constraint=django.contrib.postgres.constraints.ExclusionConstraint(expressions=[(clinica.models.DateRangeFunc('start_datetime', 'start_datetimeduration', django.contrib.postgres.fields.ranges.RangeBoundary()), '&&'), ('loaction', '=')], name='appointement_datetime_exclusion'),
        ),
    ]
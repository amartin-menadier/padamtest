# Generated by Django 3.2.5 on 2022-04-30 10:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('geography', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('licence_plate', models.CharField(max_length=10, verbose_name='Name of the bus')),
            ],
            options={
                'verbose_name_plural': 'Buses',
            },
        ),
        migrations.CreateModel(
            name='BusShift',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bus', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='fleet.bus')),
            ],
        ),
        migrations.CreateModel(
            name='Driver',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='driver', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BusStop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField()),
                ('busShift', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fleet.busshift')),
                ('place', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='geography.place')),
            ],
        ),
        migrations.AddField(
            model_name='busshift',
            name='driver',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='fleet.driver'),
        ),
    ]

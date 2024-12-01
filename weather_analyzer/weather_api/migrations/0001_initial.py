# Generated by Django 5.1.3 on 2024-12-01 13:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('name', models.CharField(db_index=True, max_length=255)),
                ('country_code', models.CharField(db_index=True, max_length=2)),
                ('state_code', models.CharField(max_length=2)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('timezone', models.CharField(max_length=255)),
                ('station_id', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='WeatherData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(db_index=True)),
                ('cloud_cover', models.IntegerField()),
                ('max_temperature', models.FloatField()),
                ('max_temperature_timestamp', models.BigIntegerField()),
                ('min_temperature', models.FloatField()),
                ('min_temperature_timestamp', models.BigIntegerField()),
                ('max_uv_index', models.FloatField()),
                ('max_wind_direction', models.FloatField()),
                ('max_wind_speed', models.FloatField()),
                ('max_wind_speed_timestamp', models.BigIntegerField()),
                ('avg_wind_speed', models.FloatField()),
                ('avg_wind_direction', models.FloatField()),
                ('avg_relative_humidity', models.IntegerField()),
                ('snow', models.FloatField()),
                ('snow_depth', models.FloatField()),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='weather_data', to='weather_api.city')),
            ],
            options={
                'indexes': [models.Index(fields=['city', 'date'], name='weather_api_city_id_def6e6_idx')],
                'constraints': [models.UniqueConstraint(fields=('city', 'date'), name='unique_city_date')],
            },
        ),
        migrations.CreateModel(
            name='WeeklyWeatherStatistics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('week_start_date', models.DateField(db_index=True)),
                ('avg_temperature', models.FloatField()),
                ('avg_wind_speed', models.FloatField()),
                ('total_snowfall', models.FloatField()),
                ('avg_cloud_cover', models.FloatField()),
                ('avg_uv_index', models.FloatField()),
                ('avg_week_relative_humidity', models.FloatField()),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='weekly_statistics', to='weather_api.city')),
            ],
            options={
                'indexes': [models.Index(fields=['city', 'week_start_date'], name='weather_api_city_id_6550bb_idx')],
            },
        ),
    ]
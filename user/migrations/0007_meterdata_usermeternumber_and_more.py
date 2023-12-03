# Generated by Django 4.2.7 on 2023-12-03 17:57

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0006_remove_userprofile_meternumber_usermeternumbers"),
    ]

    operations = [
        migrations.CreateModel(
            name="MeterData",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("lastUpdate", models.DateTimeField(default=django.utils.timezone.now)),
                ("day", models.DateField()),
                (
                    "hour_1",
                    models.DecimalField(decimal_places=3, default=0.0, max_digits=10),
                ),
                (
                    "hour_2",
                    models.DecimalField(decimal_places=3, default=0.0, max_digits=10),
                ),
                (
                    "hour_3",
                    models.DecimalField(decimal_places=3, default=0.0, max_digits=10),
                ),
                (
                    "hour_4",
                    models.DecimalField(decimal_places=3, default=0.0, max_digits=10),
                ),
                (
                    "hour_5",
                    models.DecimalField(decimal_places=3, default=0.0, max_digits=10),
                ),
                (
                    "hour_6",
                    models.DecimalField(decimal_places=3, default=0.0, max_digits=10),
                ),
                (
                    "hour_7",
                    models.DecimalField(decimal_places=3, default=0.0, max_digits=10),
                ),
                (
                    "hour_8",
                    models.DecimalField(decimal_places=3, default=0.0, max_digits=10),
                ),
                (
                    "hour_9",
                    models.DecimalField(decimal_places=3, default=0.0, max_digits=10),
                ),
                (
                    "hour_10",
                    models.DecimalField(decimal_places=3, default=0.0, max_digits=10),
                ),
                (
                    "hour_11",
                    models.DecimalField(decimal_places=3, default=0.0, max_digits=10),
                ),
                (
                    "hour_12",
                    models.DecimalField(decimal_places=3, default=0.0, max_digits=10),
                ),
                (
                    "hour_13",
                    models.DecimalField(decimal_places=3, default=0.0, max_digits=10),
                ),
                (
                    "hour_14",
                    models.DecimalField(decimal_places=3, default=0.0, max_digits=10),
                ),
                (
                    "hour_15",
                    models.DecimalField(decimal_places=3, default=0.0, max_digits=10),
                ),
                (
                    "hour_16",
                    models.DecimalField(decimal_places=3, default=0.0, max_digits=10),
                ),
                (
                    "hour_17",
                    models.DecimalField(decimal_places=3, default=0.0, max_digits=10),
                ),
                (
                    "hour_18",
                    models.DecimalField(decimal_places=3, default=0.0, max_digits=10),
                ),
                (
                    "hour_19",
                    models.DecimalField(decimal_places=3, default=0.0, max_digits=10),
                ),
                (
                    "hour_20",
                    models.DecimalField(decimal_places=3, default=0.0, max_digits=10),
                ),
                (
                    "hour_21",
                    models.DecimalField(decimal_places=3, default=0.0, max_digits=10),
                ),
                (
                    "hour_22",
                    models.DecimalField(decimal_places=3, default=0.0, max_digits=10),
                ),
                (
                    "hour_23",
                    models.DecimalField(decimal_places=3, default=0.0, max_digits=10),
                ),
                (
                    "hour_24",
                    models.DecimalField(decimal_places=3, default=0.0, max_digits=10),
                ),
            ],
        ),
        migrations.CreateModel(
            name="UserMeterNumber",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("meterNumber", models.CharField(max_length=200)),
                (
                    "intitialReading",
                    models.DecimalField(decimal_places=4, default=0.0, max_digits=10),
                ),
                ("flag", models.IntegerField()),
                ("start", models.DateTimeField(default=django.utils.timezone.now)),
                ("end", models.DateTimeField(blank=True, null=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="user.userprofile",
                    ),
                ),
            ],
        ),
        migrations.RemoveField(
            model_name="usermeternumbers",
            name="user",
        ),
        migrations.DeleteModel(
            name="UserData",
        ),
        migrations.DeleteModel(
            name="UserMeterNumbers",
        ),
        migrations.AddField(
            model_name="meterdata",
            name="meter",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="user.usermeternumber",
            ),
        ),
    ]
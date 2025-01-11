# Generated by Django 5.1 on 2025-01-10 23:17

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="VideoProject",
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
                ("title", models.CharField(max_length=200)),
                ("description", models.TextField(blank=True)),
                ("script", models.TextField(blank=True)),
                (
                    "base_media",
                    models.FileField(blank=True, null=True, upload_to="user_uploads/"),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="VideoTemplate",
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
                ("name", models.CharField(max_length=100)),
                ("description", models.TextField()),
                (
                    "preview_image",
                    models.ImageField(
                        blank=True, null=True, upload_to="templates/previews/"
                    ),
                ),
                ("json_structure", models.JSONField()),
                (
                    "category",
                    models.CharField(
                        choices=[
                            ("PROMO", "Promocional"),
                            ("EDUC", "Educativo"),
                            ("CORP", "Corporativo"),
                        ],
                        max_length=50,
                    ),
                ),
                (
                    "difficulty_level",
                    models.IntegerField(
                        choices=[(1, "Básico"), (2, "Intermedio"), (3, "Avanzado")]
                    ),
                ),
                (
                    "industry",
                    models.CharField(
                        choices=[
                            ("TECH", "Tecnología"),
                            ("RETL", "Retail"),
                            ("HLTH", "Salud"),
                        ],
                        max_length=50,
                    ),
                ),
                (
                    "estimated_duration",
                    models.IntegerField(help_text="Duración en segundos"),
                ),
            ],
            options={
                "indexes": [
                    models.Index(
                        fields=["category", "difficulty_level"],
                        name="video_app_v_categor_c3ad8d_idx",
                    ),
                    models.Index(
                        fields=["industry"], name="video_app_v_industr_77738a_idx"
                    ),
                ],
            },
        ),
    ]
# Generated by Django 5.1.2 on 2025-03-10 22:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blogs", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="blog",
            name="category",
            field=models.CharField(
                choices=[
                    ("travel", "Travel"),
                    ("food", "Food"),
                    ("health", "Health & Wellness"),
                    ("fitness", "Fitness"),
                    ("reading", "Reading"),
                    ("parenting", "Parenting"),
                    ("finance", "Personal Finance"),
                    ("fashion", "Fashion & Beauty"),
                    ("tech", "Technology & Gadgets"),
                    ("home", "Home & Living"),
                    ("hobbies", "Hobbies & Crafts"),
                    ("career", "Career & Work"),
                    ("relationships", "Relationships & Love"),
                    ("other", "Other"),
                ],
                default="other",
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name="blog",
            name="views",
            field=models.PositiveIntegerField(default=0),
        ),
    ]

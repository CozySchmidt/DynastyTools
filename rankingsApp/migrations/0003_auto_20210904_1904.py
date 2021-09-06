# Generated by Django 3.1.7 on 2021-09-05 02:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rankingsApp', '0002_matchup_player_rating_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rating',
            name='Player',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='PlayerRating', to='rankingsApp.player'),
        ),
        migrations.AddConstraint(
            model_name='rating',
            constraint=models.UniqueConstraint(fields=('User', 'Player'), name='user-player-unique'),
        ),
    ]

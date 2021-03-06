# Generated by Django 4.0.4 on 2022-05-27 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pollux', '0003_alter_trees_height_alter_trees_position'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='highways',
            options={'verbose_name': 'Voie de circulation', 'verbose_name_plural': 'Voies de circulation'},
        ),
        migrations.AlterModelOptions(
            name='lamps',
            options={'verbose_name': 'Luminaire'},
        ),
        migrations.AlterModelOptions(
            name='trees',
            options={'verbose_name': 'Arbre'},
        ),
        migrations.AddField(
            model_name='lamps',
            name='horizontal_angle',
            field=models.FloatField(default=360.0, verbose_name='Angle horizontal'),
        ),
        migrations.AlterField(
            model_name='highways',
            name='lanes',
            field=models.IntegerField(default=0, verbose_name='Nombre de voies'),
        ),
        migrations.AlterField(
            model_name='highways',
            name='name',
            field=models.CharField(default='', max_length=100, verbose_name='Nom de la voie'),
        ),
        migrations.AlterField(
            model_name='highways',
            name='type',
            field=models.CharField(default='', max_length=20, verbose_name='Type'),
        ),
        migrations.AlterField(
            model_name='highways',
            name='width',
            field=models.FloatField(default=0.0, verbose_name='Largeur'),
        ),
        migrations.AlterField(
            model_name='lamps',
            name='colour',
            field=models.IntegerField(default=5000, verbose_name='Température de couleur'),
        ),
        migrations.AlterField(
            model_name='lamps',
            name='day_impact',
            field=models.FloatField(default=0.0, verbose_name='Impact (jour)'),
        ),
        migrations.AlterField(
            model_name='lamps',
            name='height',
            field=models.FloatField(default=8.0, verbose_name='Hauteur'),
        ),
        migrations.AlterField(
            model_name='lamps',
            name='irc',
            field=models.IntegerField(default=75, verbose_name='Rendu de couleur'),
        ),
        migrations.AlterField(
            model_name='lamps',
            name='lowering_night',
            field=models.IntegerField(default=0, verbose_name='Réduction de puissance nocturne'),
        ),
        migrations.AlterField(
            model_name='lamps',
            name='nearest_way_dist',
            field=models.FloatField(default=-1.0, verbose_name='Distance voie la plus proche'),
        ),
        migrations.AlterField(
            model_name='lamps',
            name='night_impact',
            field=models.FloatField(default=0.0, verbose_name='Impact (nuit)'),
        ),
        migrations.AlterField(
            model_name='lamps',
            name='on_motion',
            field=models.BooleanField(default=False, verbose_name='Détection de mouvement?'),
        ),
        migrations.AlterField(
            model_name='lamps',
            name='orientation',
            field=models.FloatField(default=0.0, verbose_name='Orientation'),
        ),
        migrations.AlterField(
            model_name='lamps',
            name='power',
            field=models.IntegerField(default=150, verbose_name='Puissance'),
        ),
        migrations.AlterField(
            model_name='trees',
            name='day_impact',
            field=models.FloatField(default=0.0, verbose_name='Impact (jour)'),
        ),
        migrations.AlterField(
            model_name='trees',
            name='height',
            field=models.FloatField(default=0, verbose_name='Hauteur'),
        ),
        migrations.AlterField(
            model_name='trees',
            name='night_impact',
            field=models.FloatField(default=0.0, verbose_name='Impact (nuit)'),
        ),
        migrations.AlterField(
            model_name='trees',
            name='planted_date',
            field=models.IntegerField(default=0, verbose_name='Date de plantation'),
        ),
    ]

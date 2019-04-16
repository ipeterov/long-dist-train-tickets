# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-04-16 21:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import recurrence.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PlannedStop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('departure_time', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='PlannedTrain',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('departure_time', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='RailwayStation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Route',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('recurrences', recurrence.fields.RecurrenceField()),
            ],
        ),
        migrations.CreateModel(
            name='RouteStop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price_to_next', models.DecimalField(decimal_places=2, max_digits=6)),
                ('eta_delta', models.DurationField(help_text='Сколько надо прибавить к времени отбытия поезда чтобы получить время прибытия на остановку')),
                ('order', models.PositiveIntegerField()),
                ('route', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='stops', to='core.Route')),
                ('station', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.RailwayStation')),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=255)),
                ('state', models.CharField(choices=[('CREATED', 'Создан'), ('BOUGHT', 'Оплачен'), ('IN_USE', 'Используется'), ('USED', 'Использован')], max_length=31)),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('stops', models.ManyToManyField(to='core.PlannedStop')),
            ],
        ),
        migrations.CreateModel(
            name='TicketCounter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tickets_left', models.PositiveIntegerField()),
                ('planned_stop', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.PlannedStop')),
            ],
        ),
        migrations.CreateModel(
            name='TicketLimit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.PositiveIntegerField()),
                ('route', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ticket_limits', to='core.Route')),
            ],
        ),
        migrations.CreateModel(
            name='TicketType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='ticketlimit',
            name='ticket_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.TicketType'),
        ),
        migrations.AddField(
            model_name='ticketcounter',
            name='ticket_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.TicketType'),
        ),
        migrations.AddField(
            model_name='ticket',
            name='ticket_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.TicketType'),
        ),
        migrations.AddField(
            model_name='plannedtrain',
            name='route',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.Route'),
        ),
        migrations.AddField(
            model_name='plannedstop',
            name='planned_train',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.PlannedTrain'),
        ),
        migrations.AddField(
            model_name='plannedstop',
            name='stop',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.RouteStop'),
        ),
        migrations.AlterUniqueTogether(
            name='routestop',
            unique_together=set([('order', 'route')]),
        ),
    ]

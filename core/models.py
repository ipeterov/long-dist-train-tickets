from datetime import datetime, time

from django.db import models, connection
from django_fsm import FSMField, transition
from recurrence.fields import RecurrenceField

from core.managers import PlannedStopManager, TicketCounterManager, PlannedStopQuerySet


class RailwayStation(models.Model):
    """Железнодорожная станция"""

    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    def get_origin_destination_pairs(self, destination_station, departure_day):
        with connection.cursor() as cursor:
            cursor.execute('''
                    SELECT origin.id, destination.id FROM core_plannedstop origin
                    JOIN core_plannedstop destination ON origin_stop.route_id = destination_stop.route_id
                    JOIN core_routestop origin_stop ON origin.stop_id = origin_stop.id
                    JOIN core_routestop destination_stop ON destination.stop_id = destination_stop.id
                    WHERE
                        origin.departure_time BETWEEN %s AND %s
                        AND origin_stop.station_id = %s
                        AND destination_stop.station_id = %s
                        AND origin.planned_train_id = destination.planned_train_id
                ''', 
                (
                    datetime.combine(departure_day, time(0, 0)),
                    datetime.combine(departure_day, time(23, 59)),
                    self.id,
                    destination_station.id,
                )
            )
            return cursor.fetchall()


class Route(models.Model):
    """Маршрут"""

    name = models.CharField(max_length=255)
    recurrences = RecurrenceField()

    def __str__(self):
        return self.name


class TicketLimit(models.Model):
    """Задаёт количество мест определённого класса в поездах определённого маршрута"""

    ticket_type = models.ForeignKey('TicketType', on_delete=models.PROTECT)
    route = models.ForeignKey('Route', on_delete=models.CASCADE, related_name='ticket_limits')
    count = models.PositiveIntegerField()
    

class RouteStop(models.Model):
    """Секция маршрута"""

    class Meta:
        unique_together = ('order', 'route')

    route = models.ForeignKey('Route', on_delete=models.PROTECT, related_name='stops')
    station = models.ForeignKey('RailwayStation', on_delete=models.PROTECT)
    price_to_next = models.DecimalField(max_digits=6, decimal_places=2)
    eta_delta = models.DurationField(help_text='Сколько надо прибавить к времени отбытия поезда чтобы получить время прибытия на остановку')
    order = models.PositiveIntegerField()

    def __str__(self):
        return str(self.station)


class PlannedTrain(models.Model):
    """Запланированная поездка по определённому маршруту"""

    route = models.ForeignKey('Route', on_delete=models.PROTECT)
    departure_time = models.DateTimeField()

    def __str__(self):
        return str(self.route)


class PlannedStop(models.Model):
    """Секция запланированной поездки"""

    stop = models.ForeignKey('RouteStop', on_delete=models.PROTECT)
    planned_train = models.ForeignKey('PlannedTrain', on_delete=models.PROTECT)
    departure_time = models.DateTimeField()

    objects = PlannedStopManager.from_queryset(PlannedStopQuerySet)()

    def __str__(self):
        return 'Участок {} от остановки {} до следующей'.format(self.planned_train, self.stop)


class TicketCounter(models.Model):
    """Считает, сколько билетов определённого класса осталось на определённой секции маршрута."""

    ticket_type = models.ForeignKey('TicketType', on_delete=models.PROTECT)
    tickets_left = models.PositiveIntegerField()
    planned_stop = models.ForeignKey('PlannedStop', on_delete=models.PROTECT)

    objects = TicketCounterManager()


class TicketType(models.Model):
    """Тип билета, например плацкарт или купе"""

    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Ticket(models.Model):
    """Билет"""

    class STATE:
        CREATED = 'CREATED'
        BOUGHT = 'BOUGHT'
        IN_USE = 'IN_USE'
        USED = 'USED'

    state_choices = (
        (STATE.CREATED, 'Создан'),
        (STATE.BOUGHT, 'Оплачен'),
        (STATE.IN_USE, 'Используется'),
        (STATE.USED, 'Использован'),
    )

    description = models.CharField(max_length=255)
    ticket_type = models.ForeignKey('TicketType', on_delete=models.PROTECT)
    state = FSMField(choices=state_choices)
    stops = models.ManyToManyField('PlannedStop')
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.description

    @classmethod
    def create(cls, origin_planned_stop, destination_planned_stop, ticket_type):
        stops = PlannedStop.objects.all_stops(origin_planned_stop, destination_planned_stop)
        description = '{} - {} в {}'.format(
            origin_planned_stop.stop.station,
            destination_planned_stop.stop.station,
            origin_planned_stop.departure_time,
        )

        ticket = cls(
            description=description,
            ticket_type=ticket_type,
            state=cls.CREATED,
            price=stops.total_price(),
        )
        ticket.save()
        ticket.stops.add(*stops)
        return ticket

    @transition(field=state, source=STATE.CREATED, target=STATE.BOUGHT)
    def confirm_purchase(self):
        TicketCounter.objects.count_purchased_ticket(self.stops.all(), self.ticket_type) # По идее должно вернуть ошибку если нет мест

    @transition(field=state, source=STATE.BOUGHT, target=STATE.IN_USE)
    def confirm_boarding(self):
        pass

    @transition(field=state, source=STATE.IN_USE, target=STATE.USED)
    def confirm_arrival(self):
        pass

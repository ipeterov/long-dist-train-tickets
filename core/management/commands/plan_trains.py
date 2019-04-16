import datetime

from django.core.management.base import BaseCommand

from core.models import Route, RouteStop, PlannedTrain, PlannedStop, TicketCounter


class Command(BaseCommand):
    help = 'Создаёт PlannedTrain, PlannedStop и TicketCounter на days дней вперёд'

    def add_arguments(self, parser):
        parser.add_argument('days', type=int, nargs='?', default=7)

    def handle(self, *args, **options):
    	for route in Route.objects.all():
    		start = datetime.datetime.now()
    		end = datetime.datetime.now() + datetime.timedelta(days=options['days'])
    		for recurrence in route.recurrences.between(start, end):
    			planned_train = PlannedTrain.objects.create(
    				route=route,
    				departure_time=recurrence,
    			)

    			for stop in route.stops.all():
    				planned_stop = PlannedStop.objects.create(
    					stop=stop,
    					planned_train=planned_train,
    					departure_time=recurrence+stop.eta_delta,
    				)

    				for ticket_limit in route.ticket_limits.all():
    					TicketCounter.objects.create(
    						ticket_type=ticket_limit.ticket_type,
    						planned_stop=planned_stop,
    						tickets_left=ticket_limit.count,
    					)


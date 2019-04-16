from django.db import models, connection



class PlannedStopQuerySet(models.QuerySet):
	def total_price(self):
		return self.aggregate(models.Sum('stop__price_to_next'))['stop__price_to_next__sum']


class PlannedStopManager(models.Manager):
	def all_stops(self, origin_stop, destination_stop):
		return self.filter(stop__order__range=(origin_stop.stop.order, destination_stop.stop.order), stop__route=origin_stop.stop.route)

	def origin_and_destination_by_id(self, origin_stop_id, destination_stop_id):
		return self.filter(id__in=(origin_stop_id, destination_stop_id)).order_by('stop__order')


class TicketCounterManager(models.Manager):
	def tickets_left(self, planned_stops):
		tickets_left = {}
		for ticket_counter in self.values('ticket_type_id').annotate(models.Max('tickets_left')):
			tickets_left[ticket_counter['ticket_type_id']] = ticket_counter['tickets_left__max']

		return tickets_left

	def count_purchased_ticket(self, stops, ticket_type):
		self.filter(planned_stop__in=stops, ticket_type=ticket_type).update(tickets_left=models.F('tickets_left') - 1)
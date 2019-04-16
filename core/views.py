from django.http import JsonResponse

from core.models import PlannedStop, RailwayStation, Ticket, TicketType, TicketCounter
from core.forms import TicketListForm, CreateTicketForm, TicketForm

def all_stations(request):
    stations = []
    for station in RailwayStation.objects.all():
        stations.append({
            'id': station.id,
            'name': station.name,
        })

    return JsonResponse(stations, safe=False)


def list_tickets(request):
    form = TicketListForm(request.GET)

    if form.is_valid():
        origin_destination_pairs = form.cleaned_data['origin_station'].get_origin_destination_pairs(
            form.cleaned_data['destination_station'],
            form.cleaned_data['departure_day']
        )

        print(origin_destination_pairs)

        tickets = []
        for origin_stop_id, destination_stop_id in origin_destination_pairs:
            origin_stop, destination_stop = PlannedStop.objects.origin_and_destination_by_id(origin_stop_id, destination_stop_id)
            stops = PlannedStop.objects.all_stops(origin_stop, destination_stop)

            tickets.append({
                'route_name': origin_stop.stop.route.name,
                'price': stops.total_price(),
                'departure_time': origin_stop.departure_time,
                'arrival_time': destination_stop.departure_time,
                'tickets_left': TicketCounter.objects.tickets_left(stops),
                'origin_stop_id': origin_stop_id,
                'destination_stop_id': destination_stop_id,
            })

        return JsonResponse(tickets, safe=False)


def create_ticket(request):
    form = CreateTicketForm(request.GET)

    if form.is_valid():
        Ticket.create(
            form.cleaned_data['origin_planned_stop'],
            form.cleaned_data['destination_planned_stop'],
            form.cleaned_data['ticket_type']
        )
        return JsonResponse({'success': True})
    else:
        return JsonResponse(form.errors)


def confirm_purchase(request):
    form  = TicketForm(request.GET)

    if form.is_valid():
        ticket = form.cleaned_data['ticket']
        ticket.confirm_purchase()
        ticket.save()
        return JsonResponse({'success': True})
    else:
        return JsonResponse(form.errors)


def confirm_boarding(request):
    form  = TicketForm(request.GET)

    if form.is_valid():
        ticket = form.cleaned_data['ticket']
        ticket.confirm_boarding()
        ticket.save()
        return JsonResponse({'success': True})
    else:
        return JsonResponse(form.errors)


def confirm_arrival(request):
    form  = TicketForm(request.GET)

    if form.is_valid():
        ticket = form.cleaned_data['ticket']
        ticket.confirm_arrival()
        ticket.save()
        return JsonResponse({'success': True})
    else:
        return JsonResponse(form.errors)



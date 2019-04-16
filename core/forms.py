from django import forms

from core.models import RailwayStation, PlannedStop, TicketType, Ticket


class TicketListForm(forms.Form):
	origin_station = forms.ModelChoiceField(queryset=RailwayStation.objects)
	destination_station = forms.ModelChoiceField(queryset=RailwayStation.objects)
	departure_day = forms.DateField()


class CreateTicketForm(forms.Form):
	origin_planned_stop = forms.ModelChoiceField(queryset=PlannedStop.objects)
	destination_planned_stop = forms.ModelChoiceField(queryset=PlannedStop.objects)
	ticket_type = forms.ModelChoiceField(queryset=TicketType.objects)


class TicketForm(forms.Form):
	ticket = forms.ModelChoiceField(queryset=Ticket.objects)
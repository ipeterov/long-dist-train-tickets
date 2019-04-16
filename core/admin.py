from django.contrib import admin

from core.models import RailwayStation, TicketType, RouteStop, TicketLimit, Route, Ticket, PlannedTrain, PlannedStop, TicketCounter


class RouteStopInline(admin.TabularInline):
    model = RouteStop
    extra = 1


class TicketLimitInline(admin.TabularInline):
    model = TicketLimit
    extra = 1


class RouteAdmin(admin.ModelAdmin):
    inlines = [RouteStopInline, TicketLimitInline]


class TicketAdmin(admin.ModelAdmin):
    readonly_fields = ['ticket_type', 'state', 'price', 'description']
    exclude = ['stops']


class TicketCounterInline(admin.TabularInline):
    model = TicketCounter
    extra = 0


class PlannedStopAdmin(admin.ModelAdmin):
    inlines = [TicketCounterInline]


class PlannedStopInline(admin.TabularInline):
    model = PlannedStop
    extra = 0


class PlannedTrainAdmin(admin.ModelAdmin):
    inlines = [PlannedStopInline]


admin.site.register(RailwayStation)
admin.site.register(TicketType)
admin.site.register(Route, RouteAdmin)
admin.site.register(Ticket, TicketAdmin)
admin.site.register(PlannedTrain, PlannedTrainAdmin)
admin.site.register(PlannedStop, PlannedStopAdmin)
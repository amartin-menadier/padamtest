from django.contrib import admin
from . import models
from django.core.exceptions import ValidationError
from django import forms


@admin.register(models.Bus)
class BusAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Driver)
class DriverAdmin(admin.ModelAdmin):
    pass


class BusStopInlineFormset(forms.models.BaseInlineFormSet):
    def new_shift_overlaps_existing_shifts(self, new_shift_times, existing_shifts):
        """Returns False if the new shift does not overlap existing bus and driver's shifts, 
            else returns a list of str of the overlaping type(s) (driver, bus or both)"""
        not_available_type = []
        departure = min(new_shift_times)
        arrival = max(new_shift_times)
        for shifts in existing_shifts:
            for shift in shifts['set']:
                if arrival < shift.departure_time() or departure > shift.arrival_time():
                    continue
                elif shifts['type'] not in not_available_type:
                    not_available_type.append(shifts['type'])
        return not_available_type if not_available_type != [] else False

    def get_driver_and_bus_existing_shifts(self, form):
        """Returns both bus and driver's existing shifts or raises an error if either bus, driver or stops were not provided"""
        try:
            shift = form.cleaned_data.get('busShift')
            driver = shift.driver
            bus = shift.bus
        except:
            raise ValidationError('Missing data')
        bus_existing_shifts = models.BusShift.objects.filter(bus=bus)  # all existing shifts for the bus
        driver_existing_shifts = models.BusShift.objects.filter(driver=driver)  # all existing shifts for the driver
        return bus_existing_shifts, driver_existing_shifts

    def get_busStops_times(self):
        """Returns a list of all busStops' times provided in form"""
        times = []
        for form in self.forms:
            # Getting time of each busStop
            if self.can_delete and self._should_delete_form(form):
                continue
            time = form.cleaned_data.get('time')
            if not time:
                continue
            times.append(time)
        return times

    def clean(self):
        """Custom clean checks if the times given in the inline are compatbile with bus and driver's existing shifts. Else raises an error"""
        if any(self.errors):
            return
        if self.forms and self.forms[0]:
            bus_existing_shifts, driver_existing_shifts = self.get_driver_and_bus_existing_shifts(self.forms[0])
            times = self.get_busStops_times()
            unavailable_driver_or_bus = self.new_shift_overlaps_existing_shifts(times, [{'set': bus_existing_shifts, 'type': 'Bus'}, {'set': driver_existing_shifts, 'type': 'Driver'}])
            if unavailable_driver_or_bus:
                unavailable_count = len(unavailable_driver_or_bus)
                if unavailable_count == 1:  # Either bus or driver unavailable
                    error_msg = unavailable_driver_or_bus[0]
                else:  # unavailable_count == 2  Both bus and driver are unavailable
                    error_msg = 'Both bus and driver'
                raise forms.ValidationError('%(type)s not available at these times', params={'type': error_msg})
            # Both driver and bus are available at these times => no error raised
            super().clean()

class BusStopInline(admin.TabularInline):
    model = models.BusStop
    extra = 10
    formset = BusStopInlineFormset


@admin.register(models.BusShift)
class BusShiftAdmin(admin.ModelAdmin):
    list_display = ('bus', 'driver', 'departure_time', 'arrival_time', 'travel_time')
    inlines = [BusStopInline]
    list_filter = ['bus', 'driver']
    save_on_top = True

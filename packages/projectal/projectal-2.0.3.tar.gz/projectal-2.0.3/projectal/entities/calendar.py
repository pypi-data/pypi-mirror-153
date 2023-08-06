from projectal.errors import UnsupportedException

from projectal.entity import Entity


class CalendarItem(Entity):
    """
    This object represents entries within a calendar, like holidays or leaves.
    They are referred to as "Calendar Exceptions" in the web client.
    """
    _path = 'calendar'
    _name = 'CALENDAR'


class Calendar(Entity):
    """
    Implementation of the [Calendar](https://projectal.com/docs/latest/#tag/Calendar) API.

    The Calendar object acts as a "container" of calendar items based on type. Types of
    calendars are distinguished by name ("base_calendar", "location", "staff") and
    may contain a set of calendar items either for itself ("location", "staff") or
    for its holder ("base_calendar").
    """
    _path = 'calendar'
    _name = 'CALENDAR'

    def __init__(self, data):
        super(Calendar, self).__init__(data)

        # Override the inner "calendarList" with the expected type (they are CalendarItems
        # within the Calendar). We have to do this because the built-in conversion assumes
        # they are Calendars because of the name of the list.
        if self.get('calendarList'):
            cals_as_obj = []
            for cal in self.get('calendarList', []):
                cals_as_obj.append(CalendarItem(cal))
            self['calendarList'] = cals_as_obj


    @classmethod
    def create(cls, holder, entity):
        """Create a Calendar

        `holder`: `uuId` of the owner

        `entity`: The fields of the entity to be created
        """
        holder = holder['uuId'] if isinstance(holder, dict) else holder
        params = "?holder=" + holder
        return super().create(entity, params)

    @classmethod
    def list(cls, expand=False, links=None):
        raise UnsupportedException("Calendar list is not supported by the API.")

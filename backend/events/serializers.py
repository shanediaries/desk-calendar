from django.db.models import Q
from rest_framework import serializers
from .models import Event

class EventSerializer(serializers.ModelSerializer):
    duration = serializers.SerializerMethodField()
    repeat = serializers.CharField(default='NONE')

    class Meta:
        model = Event
        fields = ['id', 'name', 'start_time', 'end_time', 'duration', 'repeat', 'repeat_days']
        read_only_fields = ['id', 'duration']

    
    def validate(self, data):
        '''
        Ensure that the event start or end time does not overlap with existing events for the user.
        '''
        user = self.context['request'].user
        start_time = data['start_time']
        end_time = data['end_time']

        if data.get('repeat_days'):
            data['repeat'] = 'WEEKLY'

        overlapping_events = Event.objects.filter(
            user=user
        ).filter(
            Q(start_time__lte=start_time, end_time__gte=start_time) |
            Q(start_time__lte=end_time, end_time__gte=end_time)
        )

        if overlapping_events.exists():
            raise serializers.ValidationError(
                'The event start or end time conflicts with an existing event.'
            )

        # check repeating events
        start_time = data['start_time'].time()
        end_time = data['end_time'].time()
        repeat_days = data.get('repeat_days', '')
        new_repeat_days = set(repeat_days.split(',')) if repeat_days else set()

        overlapping_events = Event.objects.filter(
            user=user, repeat='WEEKLY'
        ).filter(
            Q(start_time__time__lte=start_time, end_time__time__gte=start_time) |
            Q(start_time__time__lte=end_time, end_time__time__gte=end_time)
        )

        for event in overlapping_events:
            if event.repeat_days:
                existing_repeat_days = set(event.repeat_days.split(','))
                if new_repeat_days & existing_repeat_days:
                    raise serializers.ValidationError(
                        f'The event overlaps with an existing event on repeated days: {", ".join(new_repeat_days & existing_repeat_days)}'
                    )

        return data

    def get_duration(self, obj):
        ''' Return the duration as a string (HH:MM:SS) '''
        duration = obj.duration  # This uses the `duration` property from the model
        total_seconds = int(duration.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        return f'{hours:02}:{minutes:02}:{seconds:02}'

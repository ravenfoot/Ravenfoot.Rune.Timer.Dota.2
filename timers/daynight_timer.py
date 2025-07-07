"""
DayNightTimer: Handles Dota 2's day/night cycle alert system.

Dota 2 alternates between day and night every 5 minutes (300 seconds).
This module pre-generates day/night transition points within a 60-minute window
and provides 15-second advance alerts to the main GUI.
"""

class DayNightTimer:
    """
    Tracks Dota 2's alternating day/night cycle and triggers alerts 15 seconds before each transition.
    """

    def __init__(self):
        """Initialize the timer with a pre-generated list of day/night cycle events."""
        self.events = self.generate_events()

    def generate_events(self):
        """
        Schedule cycle change times for 60 minutes of game time.
        - Day_Cycle: 0:00, 10:00, 20:00, ...
        - Night_Cycle: 5:00, 15:00, 25:00, ...
        Returns:
            List[Tuple[int, str]]: (event_time, cycle_type)
        """
        events = []
        t = 0
        is_day = True

        while t <= 3600:
            event_type = 'Day_Cycle' if is_day else 'Night_Cycle'
            events.append((t, event_type))
            t += 300
            is_day = not is_day

        return events

    def get_alerts(self, game_time: int) -> list:
        """
        Check if any cycle transitions should be announced at the given game_time.
        Alerts are triggered exactly 15 seconds before the actual transition.

        Args:
            game_time (int): The current time in-game, in seconds

        Returns:
            List[str]: A list of alert types ("Day_Cycle" or "Night_Cycle")
        """
        alerts = [cycle_type for spawn_time, cycle_type in self.events if spawn_time - 15 == game_time]
        return alerts

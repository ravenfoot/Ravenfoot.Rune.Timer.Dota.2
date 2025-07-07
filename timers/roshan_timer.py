"""
RoshanTimer: Handles Roshan spawn alerts for Dota 2.

Roshan respawns every 10 minutes (600 seconds).
This module precomputes Roshan spawn times for one hour of in-game time
and triggers alerts 10 seconds in advance.
"""

class RoshanTimer:
    """
    Tracks Roshan spawn intervals and generates alerts 10 seconds prior.
    """

    def __init__(self):
        """Initialize the timer with Roshan spawn events up to 3600s (1 hour)."""
        self.events = self.generate_events()

    def generate_events(self):
        """
        Compute Roshan spawn schedule at 10-minute intervals.
        Spawns occur at: 10:00, 20:00, 30:00, ..., up to 60:00.

        Returns:
            List[Tuple[int, str]]: (event_time, 'Roshan_Rune')
        """
        events = []
        t = 600  # Start at 10:00

        while t <= 3600:
            events.append((t, 'Roshan_Rune'))
            t += 600

        return events

    def get_alerts(self, game_time: int) -> list:
        """
        Check if Roshan is due to spawn soon.
        Triggers alert exactly 10 seconds before spawn.

        Args:
            game_time (int): Current in-game time in seconds

        Returns:
            List[str]: List of rune names (typically ["Roshan_Rune"])
        """
        return [rune for (t, rune) in self.events if t - 10 == game_time]

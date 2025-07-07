"""
RuneTimer: Tracks all major rune spawn timings in Dota 2.

This module generates spawn schedules for:
- Bounty Runes: Every 3 minutes starting at 0:00
- Water Runes: At 2:00 and 4:00 only
- Wisdom Runes: Every 7 minutes starting at 7:00
- Power Runes: Every 2 minutes starting at 6:00

All events are scheduled within a 60-minute window and alerts trigger 10 seconds before spawn.
"""

class RuneTimer:
    """
    Handles alert scheduling for rune spawns.
    Returns warnings 10 seconds before scheduled rune appearances.
    """

    def __init__(self):
        """Initialize with all rune spawn times precomputed up to 60 minutes."""
        self.events = self.generate_events()

    def generate_events(self):
        """
        Compute all rune spawn events in a one-hour game window.

        Returns:
            List[Tuple[int, str]]: (spawn_time, rune_name)
        """
        events = []

        # Bounty Runes every 180s starting from 0:00
        t = 0
        while t <= 3600:
            events.append((t, 'Bounty_Rune'))
            t += 180

        # Water Runes only at 2:00 and 4:00
        events.extend([(120, 'Water_Rune'), (240, 'Water_Rune')])

        # Wisdom Runes every 420s starting at 7:00
        t = 420
        while t <= 3600:
            events.append((t, 'Wisdom_Rune'))
            t += 420

        # Power Runes every 120s starting at 6:00
        t = 360
        while t <= 3600:
            events.append((t, 'Power_Rune'))
            t += 120

        return events

    def get_alerts(self, game_time: int) -> list:
        """
        Identify runes that are 10 seconds from spawning.

        Args:
            game_time (int): Current in-game time in seconds

        Returns:
            List[str]: Rune types triggering alerts
        """
        return [rune_name for spawn_time, rune_name in self.events if spawn_time - 10 == game_time]

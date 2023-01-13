import sys


class Utils():

    def running_from_binary():
        """ Determines if we're running as a script or binary

        Returns:
            bool: True if running as a binary
                False if running as a script
        """
        return getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS')
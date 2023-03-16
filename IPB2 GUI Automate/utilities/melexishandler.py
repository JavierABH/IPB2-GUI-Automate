import pyautogui
import time
import subprocess

class ProgramHandler:

    def open_application(app_path):
        """
        Opens an application specified by the given path.

        Args:
            app_path (str): The path of the application.

        Returns:
            None
        """
        try:
            subprocess.Popen(app_path)
            time.sleep(5)  # Wait 5 seconds for the application to open
        except Exception as e:
            print(f"Error opening application: {e}")

    def maximize_window():
        """
        Maximizes the active window.

        Returns:
            None
        """
        try:
            pyautogui.hotkey("win", "up")
            time.sleep(2)
        except Exception as e:
            print(f"Error maximizing window: {e}")

    def click_coordinates(x, y, time_duration=0.5):
        """
        Moves the mouse to the specified coordinate and clicks.

        Args:
            x (int): The X coordinate.
            y (int): The Y coordinate.
            time_duration (float, optional): The duration of the mouse movement. Defaults to 0.5 seconds.

        Returns:
            None
        """
        try:
            if isinstance(x, int) and isinstance(y, int):
                pyautogui.moveTo(x, y, duration=time_duration)
                pyautogui.click()
            else:
                raise ValueError("Coordinates must be integers.")
        except Exception as e:
            print(f"Error clicking on coordinate: {e}")

    def write_text(text):
        """
        Writes text on the keyboard.

        Args:
            text (str): The text to write.

        Returns:
            None
        """
        try:
            pyautogui.write(text)
        except Exception as e:
            print(f"Error writing text: {e}")

    def press_key(key):
        """
        Presses a key on the keyboard.

        Args:
            key (str): The key to press.

        Returns:
            None
        """
        try:
            pyautogui.press(key)
        except Exception as e:
            print(f"Error pressing key: {e}")

    def press_keys(*keys):
        """
        Presses multiple keys on the keyboard at the same time.

        Args:
            keys (str): The keys to press.

        Returns:
            None
        """
        try:
            pyautogui.hotkey(*keys)
        except Exception as e:
            print(f"Error pressing keys: {e}")

    def freeze(seconds):
        """
        Freezes the program for the specified number of seconds.

        Args:
            seconds (int): The number of seconds to freeze.

        Returns:
            None
        """
        time.sleep(seconds)

    def mouse_position():
        """
        Gets the current position of the mouse.

        Returns:
            tuple: The current position of the mouse in format (x, y).
        """
        try:
            position = pyautogui.position()
            return position
        except Exception as e:
            print(f"Error getting mouse position: {e}")

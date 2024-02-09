import tkinter as tk
from tkinter import ttk
from math import cos, sin, pi
from datetime import datetime
import pytz

class WorldClockApp:
    def __init__(self, root):
        self.root = root
        self.root.title("World Clocks")

        self.world_clocks = []

        for i in range(4):
            clock_frame = tk.Frame(root, padx=10, pady=10, borderwidth=2, relief="solid")
            clock_frame.grid(row=0, column=i, padx=10)

            clock = AnalogClock(clock_frame)
            self.world_clocks.append(clock)

            self.create_city_dropdown(clock, row=1, column=i)

    def create_city_dropdown(self, clock, row, column):
        city_label = tk.Label(self.root, text="Select City:")
        city_label.grid(row=row, column=column, pady=10, padx=20, sticky="e")

        selected_city = tk.StringVar()
        city_dropdown = ttk.Combobox(self.root, textvariable=selected_city, values=self.get_city_list())
        city_dropdown.grid(row=row + 1, column=column, pady=10, sticky="w")
        city_dropdown.bind("<<ComboboxSelected>>", lambda event, clock=clock, city=selected_city: self.update_clock(clock, city.get()))

    def update_clock(self, clock, selected_city):
        clock.start_ticking(selected_city)

    def get_city_list(self):
        return [
            "New York", "London", "Tokyo", "Sydney",
            "Dubai", "Los Angeles", "Berlin", "Singapore",
            "Mumbai", "Johannesburg", "Rio de Janeiro", "Auckland",
            "Hawaii", "UTC", "Paris", "Beijing", "Chicago", "Toronto",
            "Moscow", "Buenos Aires"
        ]

class AnalogClock:
    def __init__(self, root):
        self.canvas = tk.Canvas(root, width=150, height=150, bg="white")
        self.canvas.pack()

        self.hour_hand = None
        self.minute_hand = None
        self.second_hand = None

    def draw_clock(self):
        # Draw clock face
        self.canvas.create_oval(20, 20, 130, 130)

        # Draw hour, minute, and second hands
        self.hour_hand = self.canvas.create_line(75, 75, 75, 50, width=4, fill="black")
        self.minute_hand = self.canvas.create_line(75, 75, 75, 40, width=3, fill="blue")
        self.second_hand = self.canvas.create_line(75, 75, 75, 35, width=2, fill="red")

    def start_ticking(self, selected_city):
        self.draw_clock()
        self.update_time(selected_city)

    def update_time(self, selected_city):
        timezone = self.get_timezone(selected_city)

        if timezone:
            current_time = datetime.now(pytz.timezone(timezone))
            hours, minutes, seconds = current_time.hour, current_time.minute, current_time.second

            # Update hour hand
            hour_angle = (hours % 12 + minutes / 60) * 30
            self.rotate_hand(self.hour_hand, hour_angle)

            # Update minute hand
            minute_angle = (minutes + seconds / 60) * 6
            self.rotate_hand(self.minute_hand, minute_angle)

            # Update second hand
            second_angle = seconds * 6
            self.rotate_hand(self.second_hand, second_angle)

            self.canvas.after(1000, lambda: self.update_time(selected_city))

    def get_timezone(self, city_name):
        city_timezones = {
            "New York": "America/New_York",
            "London": "Europe/London",
            "Paris": "Europe/Paris",
            "Tokyo": "Asia/Tokyo",
            "Sydney": "Australia/Sydney",
            "Dubai": "Asia/Dubai",
            "Los Angeles": "America/Los_Angeles",
            "Berlin": "Europe/Berlin",
            "Singapore": "Asia/Singapore",
            "Mumbai": "Asia/Kolkata",
            "Johannesburg": "Africa/Johannesburg",
            "Rio de Janeiro": "America/Rio_de_Janeiro",
            "Auckland": "Pacific/Auckland",
            "Hawaii": "Pacific/Honolulu",
            "UTC": "UTC",
            "Beijing": "Asia/Shanghai",
            "Chicago": "America/Chicago",
            "Toronto": "America/Toronto",
            "Moscow": "Europe/Moscow",
            "Buenos Aires": "America/Argentina/Buenos_Aires",
        }

        return city_timezones.get(city_name, None)

    def rotate_hand(self, hand, angle):
        angle_rad = angle * pi / 180
        hand_length = 40
        hand_x = 75 + hand_length * sin(angle_rad)
        hand_y = 75 - hand_length * cos(angle_rad)

        self.canvas.coords(hand, 75, 75, hand_x, hand_y)

if __name__ == "__main__":
    root = tk.Tk()
    app = WorldClockApp(root)
    root.mainloop()
    
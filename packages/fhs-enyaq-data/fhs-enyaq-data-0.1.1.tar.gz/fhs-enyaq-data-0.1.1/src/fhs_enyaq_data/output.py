""" Loop. """
from datetime import datetime
from rich.console import Console

def console_str(my_str):
    # [22:12:14]
    now = datetime.now()

    current_time = now.strftime("%H:%M:%S")
    #Console.print(f"[cyan]\[{current_time}][/cyan] {my_str}")
    print(f"{current_time} | {my_str}")



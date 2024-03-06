import time
import winsound
import pyttsx3
from tkinter import *

windo = Tk()
windo.geometry("600x400")


def update_clock(timer_number, repetitions):
    global remaining_time, current_repetition
    print(repetitions)
    if remaining_time > 0:
        remaining_time -= 1
        hour = remaining_time // 3600
        minute = (remaining_time % 3600) // 60
        second = remaining_time % 60
        time_str = f"{hour:02d}:{minute:02d}:{second:02d}"
        text_clock.config(text=f"Timer {timer_number} ({current_repetition}/{repetitions}): {time_str}")
        windo.after(1000, lambda: update_clock(timer_number, repetitions))
    else:
        winsound.Beep(1000, 2000)  # Beep when time reaches zero
        if timer_number == 1:
            speak_sentence("First timer is done!")
            windo.after(1000, lambda: start_next_timer(2, repetitions))
        elif timer_number == 2:
            speak_sentence("Second timer is done!")
            current_repetition += 1
            if current_repetition <= repetitions:
                reset_timers()
                start_countdown()
            else:
                speak_sentence("All repetitions completed. Please enter a new set of timers and repetitions.")
                reset_timers()


def speak_sentence(sentence):
    engine = pyttsx3.init()
    engine.say(sentence)
    engine.runAndWait()


def start_countdown():
    global remaining_time, current_repetition

    time_str = time_input.get()
    repetitions_str = repetitions_input.get()

    try:
        repetitions = int(repetitions_str)
    except ValueError:
        speak_sentence("Please enter a valid number for repetitions.")
        return

    current_repetition = 1
    remaining_time = calculate_remaining_time(time_str)
    update_clock(1, repetitions)



def start_next_timer(timer_number, repetitions):
    global remaining_time

    new_time_str = new_time_input.get()

    if new_time_str:
        hour, minute, second = map(int, new_time_str.split(':'))
        remaining_time = hour * 3600 + minute * 60 + second
        update_clock(timer_number, repetitions)
    else:
        speak_sentence(f"Timer {timer_number} completed.")

        if timer_number < repetitions:
            windo.after(1000, lambda: start_next_timer(timer_number + 1, repetitions))
        else:
            speak_sentence("All repetitions completed. Please enter a new set of timers and repetitions.")
            reset_timers()


def reset_timers():
    time_input.delete(0, END)
    new_time_input.delete(0, END)
    repetitions_input.delete(0, END)
    text_clock.config(text="")


def calculate_remaining_time(time_str):
    hour, minute, second = map(int, time_str.split(':'))
    return hour * 3600 + minute * 60 + second


time_input = Entry(windo)
time_input.pack()

new_time_input = Entry(windo)
new_time_input.pack()

repetitions_input = Entry(windo)
repetitions_input.pack()

button_start_timers = Button(windo, text="Start Timers", command=start_countdown)
button_start_timers.pack()

text_clock = Label(windo, text="")
text_clock.pack(pady=20)

remaining_time = 0
current_repetition = 1

windo.mainloop()

import tkinter as tk
from tkinter import ttk
import random
import threading
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Define the sorting algorithms with visualization
def merge_sort(array, draw_array, speed):
    merge_sort_recursive(array, 0, len(array)-1, draw_array, speed)

def merge_sort_recursive(array, left, right, draw_array, speed):
    if left < right:
        mid = (left + right) // 2
        merge_sort_recursive(array, left, mid, draw_array, speed)
        merge_sort_recursive(array, mid + 1, right, draw_array, speed)
        merge(array, left, mid, right, draw_array, speed)

def merge(array, left, mid, right, draw_array, speed):
    left_part = array[left:mid+1]
    right_part = array[mid+1:right+1]
    left_idx, right_idx = 0, 0

    for array_idx in range(left, right + 1):
        if left_idx < len(left_part) and (right_idx >= len(right_part) or left_part[left_idx] <= right_part[right_idx]):
            array[array_idx] = left_part[left_idx]
            left_idx += 1
        else:
            array[array_idx] = right_part[right_idx]
            right_idx += 1
        draw_array(array, get_color_array(len(array), left, mid, right))
        window.after(speed)

def quick_sort(array, draw_array, speed):
    quick_sort_recursive(array, 0, len(array)-1, draw_array, speed)

def quick_sort_recursive(array, low, high, draw_array, speed):
    if low < high:
        pi = partition(array, low, high, draw_array, speed)
        quick_sort_recursive(array, low, pi-1, draw_array, speed)
        quick_sort_recursive(array, pi+1, high, draw_array, speed)

def partition(array, low, high, draw_array, speed):
    pivot = array[high]
    i = low - 1
    for j in range(low, high):
        if array[j] < pivot:
            i += 1
            array[i], array[j] = array[j], array[i]
            draw_array(array, get_color_array(len(array), low, high, i, j, pivot))
            window.after(speed)
    array[i+1], array[high] = array[high], array[i+1]
    draw_array(array, get_color_array(len(array), low, high, i, j, pivot))
    window.after(speed)
    return i + 1

def bubble_sort(array, draw_array, speed):
    for i in range(len(array) - 1):
        for j in range(len(array) - i - 1):
            if array[j] > array[j + 1]:
                array[j], array[j + 1] = array[j + 1], array[j]
                draw_array(array, ['green' if x == j or x == j + 1 else 'blue' for x in range(len(array))])
                window.after(speed)

def selection_sort(array, draw_array, speed):
    for i in range(len(array)):
        min_idx = i
        for j in range(i + 1, len(array)):
            if array[j] < array[min_idx]:
                min_idx = j
        array[i], array[min_idx] = array[min_idx], array[i]
        draw_array(array, ['green' if x == i or x == min_idx else 'blue' for x in range(len(array))])
        window.after(speed)

def insertion_sort(array, draw_array, speed):
    for i in range(1, len(array)):
        key = array[i]
        j = i - 1
        while j >= 0 and key < array[j]:
            array[j + 1] = array[j]
            j -= 1
            draw_array(array, ['green' if x == j or x == j + 1 else 'blue' for x in range(len(array))])
            window.after(speed)
        array[j + 1] = key
        draw_array(array, ['green' if x == i or x == j + 1 else 'blue' for x in range(len(array))])
        window.after(speed)

def heap_sort(array, draw_array, speed):
    n = len(array)
    for i in range(n // 2 - 1, -1, -1):
        heapify(array, n, i, draw_array, speed)
    for i in range(n-1, 0, -1):
        array[i], array[0] = array[0], array[i]
        draw_array(array, ['green' if x == i or x == 0 else 'blue' for x in range(len(array))])
        window.after(speed)
        heapify(array, i, 0, draw_array, speed)

def heapify(array, n, i, draw_array, speed):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2
    if left < n and array[left] > array[largest]:
        largest = left
    if right < n and array[right] > array[largest]:
        largest = right
    if largest != i:
        array[i], array[largest] = array[largest], array[i]
        draw_array(array, ['green' if x == i or x == largest else 'blue' for x in range(len(array))])
        window.after(speed)
        heapify(array, n, largest, draw_array, speed)

# Helper functions for drawing the array
def draw_array(array, color_array):
    canvas.delete("all")
    canvas_height = 380
    canvas_width = 800
    bar_width = canvas_width / (len(array) + 1)
    offset = 30
    spacing = 10
    normalized_array = [i / max(array) for i in array]
    for i, height in enumerate(normalized_array):
        x0 = i * bar_width + offset + spacing
        y0 = canvas_height - height * 340
        x1 = (i + 1) * bar_width + offset
        y1 = canvas_height
        canvas.create_rectangle(x0, y0, x1, y1, fill=color_array[i])
        canvas.create_text(x0 + 2, y0, anchor=tk.SW, text=str(array[i]))
    window.update_idletasks()

def get_color_array(array_length, low=None, high=None, mid=None, current=None, pivot=None):
    color_array = []
    for i in range(array_length):
        if low is not None and high is not None and i >= low and i <= high:
            if pivot is not None and i == pivot:
                color_array.append('orange')
            elif current is not None and i == current:
                color_array.append('red')
            else:
                color_array.append('yellow')
        else:
            color_array.append('blue')
    return color_array

# Main GUI setup
def generate_array():
    global array
    array = [random.randint(1, 100) for _ in range(100)]
    draw_array(array, ['blue' for x in range(len(array))])

def set_speed():
    if speed_menu.get() == 'Slow':
        return 200
    elif speed_menu.get() == 'Medium':
        return 100
    else:
        return 10

def start_sorting():
    global array
    speed = set_speed()
    threading.Thread(target=run_sorting_algorithm, args=(array, speed)).start()

def run_sorting_algorithm(array, speed):
    if algo_menu.get() == 'Bubble Sort':
        bubble_sort(array, draw_array, speed)
    elif algo_menu.get() == 'Merge Sort':
        merge_sort(array, draw_array, speed)
    elif algo_menu.get() == 'Quick Sort':
        quick_sort(array, draw_array, speed)
    elif algo_menu.get() == 'Selection Sort':
        selection_sort(array, draw_array, speed)
    elif algo_menu.get() == 'Insertion Sort':
        insertion_sort(array, draw_array, speed)
    elif algo_menu.get() == 'Heap Sort':
        heap_sort(array, draw_array, speed)

# Initialize window
window = tk.Tk()
window.title("Sorting Algorithm Visualizer")
window.maxsize(900, 600)
window.config(bg="black")

# Frame for UI controls
UI_frame = tk.Frame(window, width=900, height=200, bg="grey")
UI_frame.grid(row=0, column=0, padx=10, pady=5)

# Canvas for drawing the array
canvas = tk.Canvas(window, width=800, height=400, bg="white")
canvas.grid(row=1, column=0, padx=10, pady=5)

# User interface area
tk.Label(UI_frame, text="Algorithm: ", bg="grey").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
algo_menu = ttk.Combobox(UI_frame, values=['Bubble Sort', 'Merge Sort', 'Quick Sort', 'Selection Sort', 'Insertion Sort', 'Heap Sort'])
algo_menu.grid(row=0, column=1, padx=5, pady=5)
algo_menu.current(0)

tk.Label(UI_frame, text="Sorting Speed: ", bg="grey").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
speed_menu = ttk.Combobox(UI_frame, values=['Slow', 'Medium', 'Fast'])
speed_menu.grid(row=1, column=1, padx=5, pady=5)
speed_menu.current(0)

tk.Button(UI_frame, text="Start Sorting", command=start_sorting, bg="red").grid(row=2, column=1, padx=5, pady=5)
tk.Button(UI_frame, text="Generate Array", command=generate_array, bg="white").grid(row=2, column=0, padx=5, pady=5)

generate_array()
window.mainloop()

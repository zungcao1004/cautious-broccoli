import tkinter as tk
from tkinter import ttk
import psutil
import os

def set_cpu_affinity():
    selected_process = process_listbox.curselection()
    if not selected_process:
        status_label.config(text="No process selected.")
        return

    process_name = process_listbox.get(selected_process[0])
    pid = process_pids[process_name]

    try:
        proc = psutil.Process(pid)
        affinity = [i for i, var in enumerate(cpu_vars) if var.get()]
        proc.cpu_affinity(affinity)
        update_cpu_display(proc)
        status_label.config(text=f"Affinity set for PID {pid}.")
    except psutil.AccessDenied:
        status_label.config(text=f"Access denied to process {pid}. Run as admin.")
    except psutil.NoSuchProcess:
        status_label.config(text=f"Process {pid} no longer exists.")
        update_process_list()
    except Exception as e:
        status_label.config(text=f"An error occurred: {e}")

def update_cpu_display(proc):
    try:
        current_affinity = proc.cpu_affinity()
        for i, var in enumerate(cpu_vars):
            var.set(i in current_affinity)
    except psutil.NoSuchProcess:
        pass

def update_process_list():
    process_listbox.delete(0, tk.END)
    process_pids.clear()
    for proc in psutil.process_iter(['name', 'pid']):
        process_name = proc.info['name']
        if process_name == "so2game.exe":
            process_pid = proc.info['pid']
            display_name = f"{process_name} (PID: {process_pid})"
            if display_name not in process_pids:
                process_pids[display_name] = process_pid
                process_listbox.insert(tk.END, display_name)

def on_process_select(event):
    selected_process = process_listbox.curselection()
    if selected_process:
        process_name = process_listbox.get(selected_process[0])
        pid = process_pids[process_name]
        try:
            proc = psutil.Process(pid)
            update_cpu_display(proc)
        except psutil.NoSuchProcess:
            # status_label.config(text="Process no longer exists.")
            update_process_list()

def auto_set_cpu_affinity(process_name="so2game.exe"):
    try:
        cpu_count = os.cpu_count()
        if cpu_count is None:
            raise OSError("Could not determine CPU count.")

        processes = [proc for proc in psutil.process_iter(['name']) if proc.info['name'] == process_name]

        if not processes:
            status_label.config(text=f"No processes found with name '{process_name}'.")
            return

        for i, proc in enumerate(processes):
            cpu_index = i % cpu_count
            try:
                proc.cpu_affinity([cpu_index])
                print(f"Process {proc.pid} set to CPU {cpu_index}")
            except psutil.AccessDenied:
                print(f"Access denied to process {proc.pid}. Run as admin.")
            except psutil.NoSuchProcess:
                print(f"Process {proc.pid} no longer exists.")
            except Exception as e:
                print(f"An error occurred: {e}")

        status_label.config(text=f"Auto affinity set for {len(processes)} processes.")
    except Exception as e:
        status_label.config(text=f"Error: {e}")

def auto_set_cpu_affinity_exclude_cpu0(process_name="so2game.exe"):
    """Set CPU affinity for processes dynamically, excluding CPU 0."""
    try:
        cpu_count = os.cpu_count()
        if cpu_count is None or cpu_count <= 1:
            raise OSError("Insufficient CPU cores available.")

        # Define available cores (excluding CPU 0)
        available_cores = list(range(1, cpu_count))

        processes = [proc for proc in psutil.process_iter(['name']) if proc.info['name'] == process_name]
        if not processes:
            status_label.config(text=f"No processes found with name '{process_name}'.")
            return

        for i, proc in enumerate(processes):
            # Allocate processes to available cores, wrapping around if needed
            selected_core = available_cores[i % len(available_cores)]
            try:
                proc.cpu_affinity([selected_core])
                print(f"Process {proc.pid} set to CPU {selected_core}")
            except psutil.AccessDenied:
                print(f"Access denied to process {proc.pid}. Run as admin.")
            except psutil.NoSuchProcess:
                print(f"Process {proc.pid} no longer exists.")
            except Exception as e:
                print(f"An error occurred: {e}")

        status_label.config(text=f"Affinity set for {len(processes)} processes, excluding CPU 0.")
    except Exception as e:
        status_label.config(text=f"Error: {e}")

def auto_set_cpu_affinity_exclude_cpu0_and_cpu1(process_name="so2game.exe"):
    """Set CPU affinity for processes dynamically, excluding CPU 0 and CPU 1."""
    try:
        cpu_count = os.cpu_count()
        if cpu_count is None or cpu_count <= 2:
            raise OSError("Insufficient CPU cores available.")

        # Exclude CPU 0 and CPU 1
        available_cores = list(range(2, cpu_count))

        processes = [proc for proc in psutil.process_iter(['name']) if proc.info['name'] == process_name]
        if not processes:
            status_label.config(text=f"No processes found with name '{process_name}'.")
            return

        for i, proc in enumerate(processes):
            # Allocate processes to available cores, wrapping around if needed
            selected_core = available_cores[i % len(available_cores)]
            try:
                proc.cpu_affinity([selected_core])
                print(f"Process {proc.pid} set to CPU {selected_core}")
            except psutil.AccessDenied:
                print(f"Access denied to process {proc.pid}. Run as admin.")
            except psutil.NoSuchProcess:
                print(f"Process {proc.pid} no longer exists.")
            except Exception as e:
                print(f"An error occurred: {e}")

        status_label.config(text=f"Affinity set for {len(processes)} processes, excluding CPU 0 and CPU 1.")
    except Exception as e:
        status_label.config(text=f"Error: {e}")

def allocate_to_core_group(process_name="so2game.exe", core_group_size=2):
    """Allocate processes to groups of CPU cores."""
    try:
        cpu_count = os.cpu_count()
        if not cpu_count:
            raise OSError("Could not determine CPU count.")

        processes = [proc for proc in psutil.process_iter(['name']) if proc.info['name'] == process_name]
        if not processes:
            status_label.config(text=f"No processes found with name '{process_name}'.")
            return

        for i, proc in enumerate(processes):
            # Assign to a group of cores
            start_core = (i * core_group_size) % cpu_count
            core_group = list(range(start_core, start_core + core_group_size))
            try:
                proc.cpu_affinity(core_group)
                print(f"Process {proc.pid} assigned to cores {core_group}")
            except psutil.AccessDenied:
                print(f"Access denied to process {proc.pid}. Run as admin.")
            except psutil.NoSuchProcess:
                print(f"Process {proc.pid} no longer exists.")
            except Exception as e:
                print(f"An error occurred: {e}")

        status_label.config(text=f"Affinity set for {len(processes)} processes to core groups.")
    except Exception as e:
        status_label.config(text=f"Error: {e}")

def allocate_to_core_group_exclude_cpu0(process_name="so2game.exe", core_group_size=2):
    """Allocate processes to groups of CPU cores, excluding CPU 0."""
    try:
        cpu_count = os.cpu_count()
        if cpu_count is None or cpu_count <= 1:
            raise OSError("Insufficient CPU cores available.")

        # Exclude CPU 0
        available_cores = list(range(1, cpu_count))

        processes = [proc for proc in psutil.process_iter(['name']) if proc.info['name'] == process_name]
        if not processes:
            status_label.config(text=f"No processes found with name '{process_name}'.")
            return

        for i, proc in enumerate(processes):
            # Calculate core group starting index and wrap around
            start_index = (i * core_group_size) % len(available_cores)
            core_group = available_cores[start_index:start_index + core_group_size]
            try:
                proc.cpu_affinity(core_group)
                print(f"Process {proc.pid} assigned to cores {core_group}")
            except psutil.AccessDenied:
                print(f"Access denied to process {proc.pid}. Run as admin.")
            except psutil.NoSuchProcess:
                print(f"Process {proc.pid} no longer exists.")
            except Exception as e:
                print(f"An error occurred: {e}")

        status_label.config(text=f"Affinity set for {len(processes)} processes, excluding CPU 0.")
    except Exception as e:
        status_label.config(text=f"Error: {e}")

def allocate_to_core_group_exclude_cpu0_and_cpu1(process_name="so2game.exe", core_group_size=2):
    """Allocate processes to groups of CPU cores, excluding CPU 0 and CPU 1."""
    try:
        cpu_count = os.cpu_count()
        if cpu_count is None or cpu_count <= 2:
            raise OSError("Insufficient CPU cores available.")

        # Exclude CPU 0 and CPU 1
        available_cores = list(range(2, cpu_count))

        processes = [proc for proc in psutil.process_iter(['name']) if proc.info['name'] == process_name]
        if not processes:
            status_label.config(text=f"No processes found with name '{process_name}'.")
            return

        for i, proc in enumerate(processes):
            # Calculate core group starting index and wrap around
            start_index = (i * core_group_size) % len(available_cores)
            core_group = available_cores[start_index:start_index + core_group_size]
            try:
                proc.cpu_affinity(core_group)
                print(f"Process {proc.pid} assigned to cores {core_group}")
            except psutil.AccessDenied:
                print(f"Access denied to process {proc.pid}. Run as admin.")
            except psutil.NoSuchProcess:
                print(f"Process {proc.pid} no longer exists.")
            except Exception as e:
                print(f"An error occurred: {e}")

        status_label.config(text=f"Affinity set for {len(processes)} processes, excluding CPU 0 and CPU 1.")
    except Exception as e:
        status_label.config(text=f"Error: {e}")

root = tk.Tk()
root.title("CPU Affinity Manager")

process_pids = {}

# Main Frame (grid container)
main_frame = tk.Frame(root)
main_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

# Left Column (Process List and CPU List)
left_frame = tk.Frame(main_frame)
left_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

# Process List
process_frame = ttk.LabelFrame(left_frame, text="Processes")
process_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

process_listbox = tk.Listbox(process_frame, selectmode=tk.SINGLE, width=32)  
process_listbox.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
process_listbox.bind('<<ListboxSelect>>', on_process_select)

# CPU List
middle_frame = tk.Frame(main_frame)
middle_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
cpu_frame = ttk.LabelFrame(middle_frame, text="CPUs")
cpu_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

cpu_vars = []
cpu_count = os.cpu_count()
for i in range(cpu_count):
    var = tk.BooleanVar()
    tk.Checkbutton(cpu_frame, text=f"CPU {i}", variable=var).grid(row=i, column=0, sticky="w", padx=5, pady=2)
    cpu_vars.append(var)

# Right Column (Buttons and Status)
right_frame = tk.Frame(main_frame)
right_frame.grid(row=0, column=2, padx=5, pady=5, sticky="nsew")

# Buttons and Status Label
status_label = tk.Label(right_frame, text="")
status_label.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
status_label.config(text="Select a process to view or set affinity.")

set_button = tk.Button(right_frame, text="Set Affinity", command=set_cpu_affinity)
set_button.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")

refresh_button = tk.Button(right_frame, text="Refresh Processes", command=update_process_list)
refresh_button.grid(row=3, column=0, padx=5, pady=5, sticky="nsew")

single_core_label = tk.Label(right_frame, text="Single Core Allocation:")
single_core_label.grid(row=4, column=0, padx=5, pady=5, sticky="nsew")

auto_button = tk.Button(right_frame, text="Auto Set CPU Affinity", command=auto_set_cpu_affinity)
auto_button.grid(row=5, column=0, padx=5, pady=5, sticky="nsew")

auto_exclude_button = tk.Button(right_frame, text="Auto Set CPU Affinity (Exclude CPU 0)", command=auto_set_cpu_affinity_exclude_cpu0)
auto_exclude_button.grid(row=6, column=0, padx=5, pady=5, sticky="nsew")

auto_exclude_button = tk.Button(right_frame, text="Auto Set CPU Affinity (Exclude CPU 0 and CPU 1)", command=auto_set_cpu_affinity_exclude_cpu0_and_cpu1)
auto_exclude_button.grid(row=7, column=0, padx=5, pady=5, sticky="nsew")

core_group_label = tk.Label(right_frame, text="Core Group Allocation:")
core_group_label.grid(row=8, column=0, padx=5, pady=5, sticky="nsew")

group_button = tk.Button(right_frame, text="Allocate to Core Groups", command=lambda: allocate_to_core_group(core_group_size=2))
group_button.grid(row=9, column=0, padx=5, pady=5, sticky="nsew")

group_exclude_button = tk.Button(right_frame, text="Allocate to Core Groups (Exclude CPU 0)", command=lambda: allocate_to_core_group_exclude_cpu0(core_group_size=2))
group_exclude_button.grid(row=10, column=0, padx=5, pady=5, sticky="nsew")

group_exclude_button = tk.Button(right_frame, text="Allocate to Core Groups (Exclude CPU 0 and CPU 1)", command=lambda: allocate_to_core_group_exclude_cpu0_and_cpu1(core_group_size=2))
group_exclude_button.grid(row=11, column=0, padx=5, pady=5, sticky="nsew")

update_process_list()  # Initial population of process list

# Make the grid cells expand proportionally
# root.grid_rowconfigure(0, weight=1)
# root.grid_columnconfigure(0, weight=1)
main_frame.grid_rowconfigure(0, weight=1)
main_frame.grid_columnconfigure(0, weight=1)


root.mainloop()

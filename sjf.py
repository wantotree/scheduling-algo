# Non-Preemptive SJF Scheduling (with forced user input)

def get_int(prompt):
    """Force user to enter a valid integer."""
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Invalid input! Please enter a NUMBER.")

def get_pid(prompt):
    """Force user to enter a non-empty process ID."""
    while True:
        pid = input(prompt).strip()
        if pid != "":
            return pid
        print("Process ID cannot be empty!")

def sjf(processes):
    n = len(processes)
    p = [{"pid":pid, "arr":arr, "burst":burst, "done":False, "finish":0}
         for pid, arr, burst in processes]

    time = min(x["arr"] for x in p)
    gantt = []
    finished = 0

    while finished < n:
        ready = [x for x in p if not x["done"] and x["arr"] <= time]

        if not ready:
            time = min(x["arr"] for x in p if not x["done"])
            continue

        ready.sort(key=lambda x: (x["burst"], x["arr"]))
        cur = ready[0]

        start = time
        time += cur["burst"]
        cur["finish"] = time
        cur["done"] = True
        gantt.append((cur["pid"], start, time))
        finished += 1

    # Gantt chart
    print("\nGANTT CHART:")
    cur = gantt[0][1]
    print(cur, end=" ")
    for pid, s, e in gantt:
        print(f"[ {pid} ] {e}", end=" ")
    print("\n")

    # Table
    print(f"{'Process':<10}{'Arrival':>10}{'Burst':>10}"
          f"{'Turnaround':>15}{'Waiting':>12}")

    total_tat = total_wt = 0

    for x in p:
        tat = x["finish"] - x["arr"]
        wt = tat - x["burst"]
        total_tat += tat
        total_wt += wt
        print(f"{x['pid']:<10}{x['arr']:>10}{x['burst']:>10}"
              f"{tat:>15}{wt:>12}")

    print(f"\nAverage Turnaround Time = {total_tat/n:.2f}")
    print(f"Average Waiting Time = {total_wt/n:.2f}\n")


# ------------------------
#      INPUT SECTION
# ------------------------

print("=== SJF Scheduling ===")
n = get_int("Enter number of processes: ")

processes = []
for i in range(n):
    print(f"\nProcess {i+1}:")
    pid = get_pid("  Process ID: ")
    arr = get_int("  Arrival Time: ")
    burst = get_int("  Burst Time: ")
    processes.append((pid, arr, burst))

sjf(processes)

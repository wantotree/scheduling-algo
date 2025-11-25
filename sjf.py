# SJF Scheduling - Non-Preemptive, Fixed IDs & Arrival, Box-Style Gantt

def get_int(msg):
    while True:
        try:
            val = int(input(msg))
            if val > 0:
                return val
            print("Please enter a positive number!")
        except:
            print("Please enter a valid number.")

def sjf_fixed(processes):
    n = len(processes)
    for p in processes:
        p["done"] = False
        p["finish"] = 0

    time = 0
    gantt = []

    completed = 0
    while completed < n:
        ready = [p for p in processes if p["arr"] <= time and not p["done"]]
        if not ready:
            gantt.append(" ")  # idle
            time += 1
            continue

        ready.sort(key=lambda x: (x["burst"], x["arr"]))
        cur = ready[0]

        # Non-preemptive: execute fully
        for _ in range(cur["burst"]):
            gantt.append(cur["pid"])
            time += 1

        cur["finish"] = time
        cur["done"] = True
        completed += 1

    # Box-style Gantt chart
    print("\nGANTT CHART (Box Style):")
    print("+" + "---+"*len(gantt))
    for pid in gantt:
        print(f"|{pid:^3}", end="")
    print("|")
    print("+" + "---+"*len(gantt))
    print(" ".join(f"{i:^3}" for i in range(len(gantt))))

    # Table
    print(f"\n{'Process':<10}{'Arrival':>8}{'Burst':>8}{'Turnaround':>12}{'Waiting':>10}")
    total_tat = total_wt = 0
    for p in processes:
        tat = p["finish"] - p["arr"]
        wt = tat - p["burst"]
        total_tat += tat
        total_wt += wt
        print(f"{p['pid']:<10}{p['arr']:8}{p['burst']:8}{tat:12}{wt:10}")

    print(f"\nAverage Turnaround Time = {total_tat/n:.2f}")
    print(f"Average Waiting Time   = {total_wt/n:.2f}\n")

# -----------------------
# User chooses number of processes
# -----------------------
print("=== Non-Preemptive SJF Scheduling ===")
num_proc = get_int("Enter number of processes (max 26): ")

# Fixed process IDs (P1, P2, ...) and arrival times 0,1,2,...
processes = []
for i in range(num_proc):
    pid = f"P{i+1}"
    arr = i  # arrival times 0,1,2,...
    burst = get_int(f"Enter Burst Time for {pid}: ")
    processes.append({"pid":pid, "arr":arr, "burst":burst})

sjf_fixed(processes)

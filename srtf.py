# SRTF Scheduling - Fixed IDs & Arrival, user chooses number of processes

def get_int(msg):
    while True:
        try:
            val = int(input(msg))
            if val > 0:
                return val
            else:
                print("Please enter a positive number!")
        except:
            print("Please enter a valid number.")

def srtf_fixed(processes):
    n = len(processes)
    for p in processes:
        p["rem"] = p["burst"]
        p["finish"] = None

    time = 0
    gantt = []
    done = 0

    while done < n:
        ready = [p for p in processes if p["arr"] <= time and p["rem"] > 0]
        if not ready:
            gantt.append(" ")  # idle
            time += 1
            continue

        ready.sort(key=lambda x: (x["rem"], x["arr"]))
        cur = ready[0]

        gantt.append(cur["pid"])
        cur["rem"] -= 1
        time += 1

        if cur["rem"] == 0:
            cur["finish"] = time
            done += 1

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
print("=== Preemptive SRTF Scheduling ===")
num_proc = get_int("Enter number of processes (max 26): ")

# Fixed process IDs (P1, P2, ...) and arrival times 0,1,2,...
processes = []
for i in range(num_proc):
    pid = f"P{i+1}"
    arr = i  # arrival times 0,1,2,...
    burst = get_int(f"Enter Burst Time for {pid}: ")
    processes.append({"pid":pid, "arr":arr, "burst":burst})

srtf_fixed(processes)

# SRTF (Shortest Remaining Time First) - forced input, compact output

def get_int(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Invalid input! Please enter a NUMBER.")

def get_pid(prompt):
    while True:
        pid = input(prompt).strip()
        if pid:
            return pid
        print("Process ID cannot be empty!")

def srtf(processes):
    # processes: list of (pid, arrival, burst)
    n = len(processes)
    procs = []
    for pid,a,b in processes:
        procs.append({"pid":pid, "arr":a, "burst":b, "rem":b, "finish":None})

    time = min(p["arr"] for p in procs)
    finished = 0
    last_pid = None
    gantt = []  # list of (pid, start, end)

    while finished < n:
        # find ready process with smallest remaining time
        ready = [p for p in procs if p["arr"] <= time and p["rem"] > 0]
        if not ready:
            # jump to next arrival
            nxt = min(p["arr"] for p in procs if p["rem"] > 0)
            time = nxt
            continue

        # choose by remaining, tie-break by arrival then pid
        ready.sort(key=lambda x: (x["rem"], x["arr"], x["pid"]))
        cur = ready[0]

        # execute for 1 time unit (preemptive check each unit)
        if last_pid is None or last_pid != cur["pid"]:
            # start a new gantt segment
            gantt.append([cur["pid"], time, time+1])
        else:
            # extend the last segment
            gantt[-1][2] += 1

        last_pid = cur["pid"]
        cur["rem"] -= 1
        time += 1

        if cur["rem"] == 0:
            cur["finish"] = time
            finished += 1

    # Print compact GANTT CHART
    print("\nGANTT CHART:")
    if gantt:
        print(f"{gantt[0][1]}", end=" ")
        for pid, s, e in gantt:
            print(f"[ {pid} ] {e}", end=" ")
    else:
        print("No execution.")
    print("\n")

    # Print table
    print(f"{'Process':<10}{'Arrival':>8}{'Burst':>8}{'Turnaround':>12}{'Waiting':>10}")
    total_tat = total_wt = 0
    for p in procs:
        tat = p["finish"] - p["arr"]
        wt = tat - p["burst"]
        total_tat += tat
        total_wt += wt
        print(f"{p['pid']:<10}{p['arr']:8d}{p['burst']:8d}{tat:12d}{wt:10d}")

    print(f"\nAverage Turnaround Time = {total_tat/n:.2f}")
    print(f"Average Waiting Time   = {total_wt/n:.2f}\n")

if __name__ == "__main__":
    print("=== Shortest Remaining Time First (SRTF) Scheduling ===")
    n = get_int("Enter number of processes: ")
    processes = []
    for i in range(n):
        print(f"\nProcess {i+1}:")
        pid = get_pid("  Process ID: ")
        arr = get_int("  Arrival Time: ")
        burst = get_int("  Burst Time: ")
        processes.append((pid, arr, burst))

    srtf(processes)

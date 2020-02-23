import mysql.connector
import os
import matplotlib.pyplot as plt
import sys

# Returns a connection to the Slicer db
def connect_db():
    return mysql.connector.connect(
        host=os.getenv("RDS_HOST"),
        user=os.getenv("RDS_USERNAME"),
        passwd=os.getenv("RDS_PASSWORD"),
        database="slicer"
    )


# Returns the last n seconds of load for task.
def get_task_load(db, task, n):
    cursor = db.cursor()
    cursor.execute("SELECT COUNT(*) FROM expressions WHERE task = \'{}\' AND DATE_ADD(timestamp, INTERVAL {} SECOND) >= NOW() GROUP BY timestamp ORDER BY timestamp".format(task, n))
    return cursor.fetchall()

# Returns the provided string as a name safe for file formats.  
def safe_file_name(s):
    return "".join([c for c in s.lower().replace(" ", "") if c.isalpha() or c.isdigit() or c==' ']).rstrip()


# Runs the named benchmark for the duration (seconds).
def run_benchmark(name, duration):
    # Connect to slicer db for monitoring metrics
    db = connect_db()

    # TODO: Setup experiment (send admin messages)

    # Grab load from all tasks.
    task1_load = get_task_load(db, "task1", duration)
    task2_load = get_task_load(db, "task2", duration)
    task3_load = get_task_load(db, "task3", duration)
    
    # Plot each task load on same graph.
    plt.plot(task1_load, label="task 1", linestyle='solid')
    plt.plot(task2_load, label="task 2", linestyle='dotted')
    plt.plot(task3_load, label="task 3", linestyle='dashed')
    plt.xlabel("Time Elapsed (seconds)")
    plt.ylabel("# of Requests Recieved")
    plt.title("Task Load ({})".format(name))
    plt.legend()

    # Save resulting plot.
    plt.savefig("{}.eps".format(safe_file_name(name.strip())), format='eps', dpi=1200)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: python3 benchmark.py <sharding strategy> duration")
        sys.exit(1)
    run_benchmark(sys.argv[1], sys.argv[2])

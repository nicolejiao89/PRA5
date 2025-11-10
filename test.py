import requests, time, csv
import matplotlib.pyplot as plt  # for plotting

url = "http://ECE444MLDeployment-env.eba-vujnaidw.us-east-2.elasticbeanstalk.com/predict"

# Four test cases
test_cases = {
    "fake1": "Breaking! Aliens land on Mars and open a pizza shop.",
    "real1": "The prime minister announced new funding for schools.",
    "real2": "There are 365 days in a year.",
    "fake2": "Celebrity claims immortality potion found in cave."
}

all_latencies = {}  # store latencies for each case for plotting

for name, text in test_cases.items():
    times = []
    for i in range(100):
        start = time.time()
        r = requests.post(url, json={"message": text})
        end = time.time()
        times.append(end - start)

    # save for plotting
    all_latencies[name] = times

    # save CSV
    with open(f"{name}_latency.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["request_id", "latency_sec"])
        for i, t in enumerate(times, 1):
            writer.writerow([i, t])

    print(f"{name}: avg = {sum(times)/len(times):.3f}s")

# ---------- BOX PLOT PART ----------

# labels and data now guaranteed to match
labels = list(all_latencies.keys())
data = [all_latencies[name] for name in labels]

plt.figure(figsize=(8, 5))
plt.boxplot(data, tick_labels=labels)  # use tick_labels for matplotlib 3.9+
plt.ylabel("Latency (seconds)")
plt.title("API Latency Comparison Across Test Cases")
plt.grid(True, linestyle="--", alpha=0.6)
plt.savefig("latency_boxplot.png", dpi=300)
plt.show()

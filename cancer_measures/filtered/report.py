import os
import pandas as pd
from ydata_profiling import ProfileReport
from multiprocessing import Pool, cpu_count

# === CONFIG ===
INPUT_DIRS = ["country", "year"]
OUTPUT_DIRS = ["../reports/country", "../reports/year"]
os.makedirs("../reports/country", exist_ok=True)
os.makedirs("../reports/year", exist_ok=True)

# === Function to run in parallel ===
def profile_file(task):
    input_path, output_path = task
    try:
        if os.path.exists(output_path):
            return f"⏩ Skipped (already exists): {output_path}"

        df = pd.read_csv(input_path)
        if df.empty:
            return f"⚠️ Empty file: {input_path}"

        profile = ProfileReport(df, title=f"Profiling Report - {os.path.basename(input_path)}", explorative=True)
        profile.to_file(output_path)
        return f"✅ Report created: {output_path}"
    except Exception as e:
        return f"❌ Failed: {input_path} → {e}"

# === Collect all tasks (file paths) ===
def collect_tasks():
    tasks = []
    for input_dir, output_dir in zip(INPUT_DIRS, OUTPUT_DIRS):
        for file in os.listdir(input_dir):
            if file.endswith(".csv"):
                input_path = os.path.join(input_dir, file)
                output_path = os.path.join(output_dir, file.replace(".csv", ".html"))
                tasks.append((input_path, output_path))
    return tasks

# === Main ===
if __name__ == "__main__":
    tasks = collect_tasks()
    print(f"🚀 Starting profiling using {cpu_count()} CPU cores...")

    with Pool(processes=cpu_count()) as pool:
        results = pool.map(profile_file, tasks)

    for r in results:
        print(r)

    print("🎯 All profiling reports generated.")
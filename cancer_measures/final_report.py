import pandas as pd
from ydata_profiling import ProfileReport
import os

# Load the dataset
file_path = "predicted_cancer_data.csv"
df = pd.read_csv(file_path)

# Generate the profiling report
profile = ProfileReport(
    df,
    title="Dominant Cancer Types - Profiling Report",
    explorative=True
)

# Save the report
output_dir = "reports"
os.makedirs(output_dir, exist_ok=True)
output_file = os.path.join(output_dir, "predicted_cancer_data_profile.html")
profile.to_file(output_file)

print(f"✅ Report saved at: {output_file}")

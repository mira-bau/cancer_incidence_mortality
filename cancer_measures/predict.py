import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score

import warnings
warnings.filterwarnings("ignore")

# Load data
normalized_df = pd.read_csv("normalized_data.csv")

# Rescale rate
normalized_df["rate"] *= 100000

# Prepare data for regression (one row per cancer-country-year)
normalized_df["pollution_smoking"] = normalized_df["air_pollution"] * normalized_df["tobacco_use"]

# Encode cancer_name as categorical feature
normalized_df["cancer_code"] = normalized_df["cancer_name"].astype("category").cat.codes

feature_cols = [
    "air_pollution", "tobacco_use", "alcohol_use", "obesity_rate",
    "gdp_per_capita", "uhc_index", "population", "pollution_smoking",
    "cancer_code"
]

# Recreate X and y with updated features for incidence
inc_df = normalized_df[normalized_df["measure"] == "Incidence"].dropna(subset=feature_cols + ["rate"])
X_inc = inc_df[feature_cols]
y_inc = inc_df["rate"]

# Recreate X and y with updated features for mortality
mort_df = normalized_df[normalized_df["measure"] == "Mortality"].dropna(subset=feature_cols + ["rate"])
X_mort = mort_df[feature_cols]
y_mort = mort_df["rate"]

# ----------- Phase 1: Regression (Predict Cancer Rates) -----------

from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.neural_network import MLPRegressor

# Models to compare (regressors)
regression_models = {
    "RandomForestRegressor_Incidence": RandomForestRegressor(random_state=42),
    "XGBRegressor_Incidence": XGBRegressor(eval_metric="rmse", random_state=42),
    "RandomForestRegressor_Mortality": RandomForestRegressor(random_state=42),
    "XGBRegressor_Mortality": XGBRegressor(eval_metric="rmse", random_state=42)
}

regression_results = []

# Evaluate regression models
for name, model in regression_models.items():
    if "Incidence" in name:
        model.fit(X_inc, y_inc)
        y_pred = model.predict(X_inc)
        mae = mean_absolute_error(y_inc, y_pred)
        r2 = r2_score(y_inc, y_pred)
    else:
        model.fit(X_mort, y_mort)
        y_pred = model.predict(X_mort)
        mae = mean_absolute_error(y_mort, y_pred)
        r2 = r2_score(y_mort, y_pred)

    regression_results.append({
        "Model": name,
        "MAE": mae,
        "R2": r2
    })

regression_df = pd.DataFrame(regression_results)
print("\n📊 Phase 1: Regression Model Comparison (MAE & R²):")
print(regression_df)

# Update predictions with best regression models (using RandomForest here for consistency)
reg_inc = RandomForestRegressor(random_state=42)
reg_inc.fit(X_inc, y_inc)
inc_df["pred_rate"] = reg_inc.predict(X_inc)

reg_mort = RandomForestRegressor(random_state=42)
reg_mort.fit(X_mort, y_mort)
mort_df["pred_rate"] = reg_mort.predict(X_mort)

# Determine dominant cancers again
dom_inc = inc_df.groupby("country_name").apply(
    lambda df: df.loc[df["pred_rate"].idxmax()]["cancer_name"]
).reset_index().rename(columns={0: "predicted_dominant_incidence"})

dom_mort = mort_df.groupby("country_name").apply(
    lambda df: df.loc[df["pred_rate"].idxmax()]["cancer_name"]
).reset_index().rename(columns={0: "predicted_dominant_mortality"})

dominant_predictions = pd.merge(dom_inc, dom_mort, on="country_name", how="outer")
print(dominant_predictions.head())

# Evaluate regressors again with RandomForest models
y_inc_pred = reg_inc.predict(X_inc)
y_mort_pred = reg_mort.predict(X_mort)

print("📈 Incidence Regression Evaluation")
print("MAE:", mean_absolute_error(y_inc, y_inc_pred))
print("R^2:", r2_score(y_inc, y_inc_pred))

print("\n📉 Mortality Regression Evaluation")
print("MAE:", mean_absolute_error(y_mort, y_mort_pred))
print("R^2:", r2_score(y_mort, y_mort_pred))

from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

# Load labels from dominant cancer types file
dom_cancer_df = pd.read_csv("dominant_cancer_types.csv")

# Feature aggregation from normalized data
normalized_df["pollution_smoking"] = normalized_df["air_pollution"] * normalized_df["tobacco_use"]
feature_cols = [
    "air_pollution", "tobacco_use", "alcohol_use", "obesity_rate",
    "gdp_per_capita", "uhc_index", "population", "pollution_smoking"
]
agg_features = normalized_df.groupby("country_name")[feature_cols].mean().reset_index()

# Merge features with labels
merged = pd.merge(agg_features, dom_cancer_df, how="left", left_on="country_name", right_on="country_name")

# Incidence prediction
known_inc = merged.dropna(subset=["highest_incidence_cancer"])
unknown_inc = merged[merged["highest_incidence_cancer"].isna()]

le_inc = LabelEncoder()
# Rename classification label variables to avoid conflict with regression labels
y_inc_class = le_inc.fit_transform(known_inc["highest_incidence_cancer"])
X_inc = known_inc[feature_cols]

clf_inc = RandomForestClassifier(random_state=42)
clf_inc.fit(X_inc, y_inc_class)

# Predict for unknown
X_unknown_inc = unknown_inc[feature_cols]
pred_inc = clf_inc.predict(X_unknown_inc)
unknown_inc["predicted_incidence"] = le_inc.inverse_transform(pred_inc)

# Mortality prediction
known_mort = merged.dropna(subset=["highest_mortality_cancer"])
unknown_mort = merged[merged["highest_mortality_cancer"].isna()]

le_mort = LabelEncoder()
# Rename classification label variables to avoid conflict with regression labels
y_mort_class = le_mort.fit_transform(known_mort["highest_mortality_cancer"])
X_mort = known_mort[feature_cols]

clf_mort = RandomForestClassifier(random_state=42)
clf_mort.fit(X_mort, y_mort_class)

# Predict for unknown
X_unknown_mort = unknown_mort[feature_cols]
pred_mort = clf_mort.predict(X_unknown_mort)
unknown_mort["predicted_mortality"] = le_mort.inverse_transform(pred_mort)

# Combine and show results
filled = pd.merge(unknown_inc[["country_name", "predicted_incidence"]],
                  unknown_mort[["country_name", "predicted_mortality"]],
                  on="country_name", how="outer")

print("🩺 Predicted Dominant Cancer Types for Missing Countries:")
print(filled.head())

# Fill missing dominant cancer types using predictions
dom_cancer_df = pd.merge(dom_cancer_df, unknown_inc[["country_name", "predicted_incidence"]], on="country_name", how="left")
dom_cancer_df = pd.merge(dom_cancer_df, unknown_mort[["country_name", "predicted_mortality"]], on="country_name", how="left")

# Replace NaNs in original columns with predictions
dom_cancer_df["highest_incidence_cancer"] = dom_cancer_df["highest_incidence_cancer"].fillna(dom_cancer_df["predicted_incidence"])
dom_cancer_df["highest_mortality_cancer"] = dom_cancer_df["highest_mortality_cancer"].fillna(dom_cancer_df["predicted_mortality"])


# Drop helper columns
dom_cancer_df.drop(columns=["predicted_incidence", "predicted_mortality"], inplace=True)

# Show updated dataframe
print("🩺 Final dominant cancer types (gaps filled):")
print(dom_cancer_df.head())

# Save updated dominant cancer types with predictions
dom_cancer_df.to_csv("dominant_cancer_types_filled.csv", index=False)

# ----------- Phase 2: Classification (Predict Dominant Cancer Type) -----------

from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, f1_score, classification_report
from sklearn.model_selection import train_test_split

classification_models = {
    "RandomForest": RandomForestClassifier(random_state=42),
    "LogisticRegression": LogisticRegression(max_iter=500, random_state=42),
    "MLPClassifier": MLPClassifier(max_iter=500, random_state=42),
    "XGBoost": XGBClassifier(use_label_encoder=False, eval_metric="mlogloss", random_state=42)
}

classification_results = []

# --- Robust filtering of rare classes (incidence) ---
y_inc_series = pd.Series(y_inc_class, index=X_inc.index)
inc_series = y_inc_series
valid_inc_classes = inc_series.value_counts()[lambda x: x >= 2].index
valid_inc_indices = inc_series[inc_series.isin(valid_inc_classes)].index
X_inc_valid = X_inc.loc[valid_inc_indices]
y_inc_valid = y_inc_series.loc[valid_inc_indices].values

# --- Robust filtering of rare classes (mortality) ---
y_mort_series = pd.Series(y_mort_class, index=X_mort.index)
mort_series = y_mort_series
valid_mort_classes = mort_series.value_counts()[lambda x: x >= 2].index
valid_mort_indices = mort_series[mort_series.isin(valid_mort_classes)].index
X_mort_valid = X_mort.loc[valid_mort_indices]
y_mort_valid = y_mort_series.loc[valid_mort_indices].values

# --- Re-encode class labels to ensure 0...N-1 for XGBoost and compatibility ---
from sklearn.preprocessing import LabelEncoder

# Re-encode incidence labels after filtering
le_inc_filtered = LabelEncoder()
y_inc_valid = le_inc_filtered.fit_transform(y_inc_valid)

# Re-encode mortality labels after filtering
le_mort_filtered = LabelEncoder()
y_mort_valid = le_mort_filtered.fit_transform(y_mort_valid)

# --- Safe train/test split for classification task ---
X_inc_train, X_inc_test, y_inc_train, y_inc_test = train_test_split(
    X_inc_valid, y_inc_valid, test_size=0.2, random_state=42, stratify=y_inc_valid
)
X_mort_train, X_mort_test, y_mort_train, y_mort_test = train_test_split(
    X_mort_valid, y_mort_valid, test_size=0.2, random_state=42, stratify=y_mort_valid
)

# Evaluate classification models on incidence
for name, model in classification_models.items():
    model.fit(X_inc_train, y_inc_train)
    pred = model.predict(X_inc_test)
    acc = accuracy_score(y_inc_test, pred)
    f1 = f1_score(y_inc_test, pred, average='macro')
    classification_results.append({
        "Model": name + "_Incidence",
        "Accuracy": acc,
        "F1_macro": f1
    })

# Evaluate classification models on mortality
for name, model in classification_models.items():
    model.fit(X_mort_train, y_mort_train)
    pred = model.predict(X_mort_test)
    acc = accuracy_score(y_mort_test, pred)
    f1 = f1_score(y_mort_test, pred, average='macro')
    classification_results.append({
        "Model": name + "_Mortality",
        "Accuracy": acc,
        "F1_macro": f1
    })

classification_df = pd.DataFrame(classification_results)
print("\n📊 Phase 2: Classification Model Comparison (Accuracy & F1_macro):")
print(classification_df)


# Save model comparison tables to CSV
regression_df.to_csv("regression_model_comparison.csv", index=False)
classification_df.to_csv("classification_model_comparison.csv", index=False)


# ----------- Final: Predict missing dominant cancer types for all countries and save combined CSV -----------

# Use the trained RandomForestClassifier models to predict missing incidence and mortality values
final_inc_pred = clf_inc.predict(X_unknown_inc)
final_mort_pred = clf_mort.predict(X_unknown_mort)

unknown_inc["highest_incidence_cancer"] = le_inc.inverse_transform(final_inc_pred)
unknown_mort["highest_mortality_cancer"] = le_mort.inverse_transform(final_mort_pred)

# Merge predictions back to main dataset
final_df = pd.merge(dom_cancer_df, unknown_inc[["country_name", "highest_incidence_cancer"]], on="country_name", how="outer", suffixes=("", "_filled"))
final_df["highest_incidence_cancer"] = final_df["highest_incidence_cancer"].fillna(final_df["highest_incidence_cancer_filled"])
final_df.drop(columns=["highest_incidence_cancer_filled"], inplace=True)

final_df = pd.merge(final_df, unknown_mort[["country_name", "highest_mortality_cancer"]], on="country_name", how="outer", suffixes=("", "_filled"))
final_df["highest_mortality_cancer"] = final_df["highest_mortality_cancer"].fillna(final_df["highest_mortality_cancer_filled"])
final_df.drop(columns=["highest_mortality_cancer_filled"], inplace=True)

# Save final output
final_df.to_csv("dominant_cancer_types_all_filled_rf.csv", index=False)
print("✅ Saved: dominant_cancer_types_all_filled_rf.csv")

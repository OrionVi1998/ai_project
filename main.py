import numpy as np
import pandas as pd
from scipy.stats import chi2_contingency

df = pd.read_csv(
    "./latestdata.csv",
    dtype=
    {
        "ID": str,
        "age": str,
        "sex": str,
        "city": str,
        "province": str,
        "country": str,
        "latitude": float,
        "longitude": float,
        "geo_resolution": str,
        "date_onset_symptoms": str,
        "date_admission_hospital": str,
        "date_confirmation": str,
        "symptoms": str,
        "lives_in_Wuhan": str,
        "travel_history_dates": str,
        "travel_history_location": str,
        "reported_market_exposure": str,
        "additional_information": str,
        "chronic_disease": str,
        "source": str,
        "sequence_available": str,
        "outcome": str,
        "date_death_or_discharge": str,
        "notes_for_discussion": str,
        "location": str,
        "admin1": str,
        "admin2": str,
        "admin3": str,
        "country_new": str,
        "admin_id": float,
        "data_moderator_initials": str,
        "travel_history_binary": str
    },
    # nrows=1000
)

# df.astype({'date_onset_symptoms': 'datetime64[ns]'})
# df.astype({'date_admission_hospital': 'datetime64[ns]'})
# df.astype({'date_confirmation': 'datetime64[ns]'})
df.astype({'date_death_or_discharge': 'datetime64[ns]'})

print(df)

# Total of missing values
total_cells = np.prod(df.shape)
total_missing = df.isnull().sum().sum()

# Percentage of missing data
print((total_missing / total_cells) * 100)


# Clean age

def age_to_int(age_str):
    if isinstance(age_str, float):
        return None

    if "-" in age_str:
        age_min, age_max = age_str.split("-")
        if age_min == '':
            return int(age_max)
        if age_max == '':
            return int(age_min)
        age_min, age_max = int(age_min), int(age_max)
        return int((age_min + age_max) / 2)

    if "weeks" in age_str:
        return 0

    if "months" in age_str or "month" in age_str:
        num, _ = age_str.split(" ")
        if int(num) < 12:
            return 0
        return int(int(num) / 12)

    if age_str[-1] == "+" or age_str[-1] == "-":
        return int(age_str[:-1])

    return int(float(age_str))


df["age"] = df["age"].apply(age_to_int)
df["age"] = df["age"].fillna(int(df["age"].mean()))

df.info()

df = df[df['outcome'].notna()]

def is_correlated(var_name1, var_name2):
    try:
        ct = pd.crosstab(index=df[var_name1], columns=df[var_name2])
        chi2_res = chi2_contingency(ct, )
        p, x = chi2_res[1], "correlated" if chi2_res[1] < 0.05 else "not-correlated"
        return p, x
    except ValueError:
        return 0, "no data"


corr = [[],[]]
for var1 in df:
    if var1 != "ID":
        p_val, correlation = is_correlated(var1, "outcome")
        if correlation == "correlated":
            corr[0].append((p_val, var1))
        else:
            corr[1].append((p_val, var1))

corr[0].sort()
corr[1].sort()

print(corr[0],"\n", corr[1])

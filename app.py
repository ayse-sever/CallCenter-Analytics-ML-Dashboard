from flask import Flask, render_template, request
import pandas as pd
import joblib

app = Flask(__name__)

# =========================
# MODEL VE ENCODER YÜKLEME
# =========================

model = joblib.load("model/xgboost_model.pkl")
encoders = joblib.load("model/encoders.pkl")

# =========================
# VERİ YÜKLEME
# =========================

df = pd.read_csv("data/incident_event_log.csv")

# Tarih dönüşümü

df["opened_at"] = pd.to_datetime(df["opened_at"], errors="coerce", dayfirst=True)

df["resolved_at"] = pd.to_datetime(df["resolved_at"], errors="coerce", dayfirst=True)

# Zaman özellikleri

df["opened_hour"] = df["opened_at"].dt.hour

df["opened_weekday"] = df["opened_at"].dt.day_name()

df["opened_month"] = df["opened_at"].dt.month_name()

df["opened_day"] = df["opened_at"].dt.day

df["opened_quarter"] = df["opened_at"].dt.quarter

# Ek zaman özellikleri

df["is_weekend"] = df["opened_at"].dt.weekday >= 5

df["is_business_hours"] = df["opened_hour"].between(8, 17)

df["work_shift"] = pd.cut(
    df["opened_hour"], bins=[-1, 8, 16, 24], labels=["0", "1", "2"]
)

# =========================
# ANA SAYFA
# =========================


@app.route("/")
def home(prediction_text=None, active_page="genel", selected_values=None):

    data = df.copy()

    # Genel Bakış

    total_records = len(data)

    active_incidents = data[data["active"] == True].shape[0]

    completed_incidents = data[
        data["incident_state"].isin(["Resolved", "Closed"])
    ].shape[0]

    # Operasyon

    priority_counts = data["priority"].value_counts().to_dict()

    category_counts = data["category"].value_counts().head(10).to_dict()

    hour_counts = data["opened_hour"].value_counts().sort_index().to_dict()

    # SLA

    sla_success = data["made_sla"].value_counts().get(True, 0)

    sla_rate = round((sla_success / len(data)) * 100, 2)

    sla_rate_data = {"Başarılı": sla_rate, "İhlal": round(100 - sla_rate, 2)}

    # Çözüm süresi

    data["resolution_time"] = data["resolved_at"] - data["opened_at"]

    average_resolution_hours = round(
        data["resolution_time"].dt.total_seconds().mean() / 3600, 2
    )

    priority_resolution = (
        data.groupby("priority")["resolution_time"]
        .mean()
        .dt.total_seconds()
        .div(3600)
        .round(2)
        .to_dict()
    )

    data["month"] = data["opened_at"].dt.month_name()

    monthly_resolution = (
        data.groupby("month")["resolution_time"]
        .mean()
        .dt.total_seconds()
        .div(3600)
        .round(2)
        .to_dict()
    )

    longest = data.nlargest(10, "resolution_time")[["number", "resolution_time"]]

    longest["resolution_time"] = (
        longest["resolution_time"].dt.total_seconds() / 3600
    ).round(2)

    longest_incidents = dict(zip(longest["number"], longest["resolution_time"]))

    # Ekip

    team_counts = data["assignment_group"].value_counts().head(10).to_dict()

    employee_counts = data["assigned_to"].value_counts().head(10).to_dict()

    team_resolution = (
        data.groupby("assignment_group")["resolution_time"]
        .mean()
        .dt.total_seconds()
        .div(3600)
        .round(2)
        .sort_values(ascending=False)
        .head(10)
        .to_dict()
    )

    # Tahmin formu için seçenekler

    incident_states = sorted(data["incident_state"].dropna().unique())

    actives = sorted(data["active"].dropna().unique())

    contact_types = sorted(data["contact_type"].dropna().unique())

    locations = sorted(data["location"].dropna().unique())

    categories = sorted(data["category"].dropna().unique())

    subcategories = sorted(data["subcategory"].dropna().unique())

    symptoms = sorted(data["u_symptom"].dropna().unique())

    cmdb_cis = sorted(data["cmdb_ci"].dropna().unique())

    impacts = sorted(data["impact"].dropna().unique())

    urgencies = sorted(data["urgency"].dropna().unique())

    priorities = sorted(data["priority"].dropna().unique())

    assignment_groups = sorted(data["assignment_group"].dropna().unique())

    assigned_tos = sorted(data["assigned_to"].dropna().unique())

    knowledges = sorted(data["knowledge"].dropna().unique())

    opened_weekdays = sorted(data["opened_weekday"].dropna().unique())

    opened_months = sorted(data["opened_month"].dropna().unique())

    work_shifts = sorted(data["work_shift"].dropna().unique())

    return render_template(
        "index.html",
        selected_values=selected_values,
        active_page=active_page,
        total_records=total_records,
        active_incidents=active_incidents,
        completed_incidents=completed_incidents,
        average_resolution_hours=average_resolution_hours,
        priority_counts=priority_counts,
        category_counts=category_counts,
        hour_counts=hour_counts,
        sla_rate_data=sla_rate_data,
        priority_resolution=priority_resolution,
        monthly_resolution=monthly_resolution,
        longest_incidents=longest_incidents,
        team_counts=team_counts,
        employee_counts=employee_counts,
        team_resolution=team_resolution,
        prediction_text=prediction_text,
        priorities=priorities,
        impacts=impacts,
        urgencies=urgencies,
        categories=categories,
        subcategories=subcategories,
        assignment_groups=assignment_groups,
        incident_states=incident_states,
        actives=actives,
        contact_types=contact_types,
        locations=locations,
        symptoms=symptoms,
        cmdb_cis=cmdb_cis,
        assigned_tos=assigned_tos,
        knowledges=knowledges,
        opened_weekdays=opened_weekdays,
        opened_months=opened_months,
        work_shifts=work_shifts,
    )


# =========================
# TAHMİN
# =========================


@app.route("/predict", methods=["POST"])
def predict():

    print("1")

    priority = request.form["priority"]
    impact = request.form["impact"]
    urgency = request.form["urgency"]
    category = request.form["category"]
    subcategory = request.form["subcategory"]
    assignment_group = request.form["assignment_group"]
    reassignment_count = int(request.form["reassignment_count"])

    selected_values = {
        "Priority": priority,
        "Impact": impact,
        "Urgency": urgency,
        "Category": category,
        "Subcategory": subcategory,
        "Assignment Group": assignment_group,
        "Reassignment Count": reassignment_count,
    }

    print("2")

    priority = encoders["priority"].transform([priority])[0]

    impact = encoders["impact"].transform([impact])[0]

    urgency = encoders["urgency"].transform([urgency])[0]

    category = encoders["category"].transform([category])[0]

    subcategory = encoders["subcategory"].transform([subcategory])[0]

    assignment_group = encoders["assignment_group"].transform([assignment_group])[0]

    priority_score = {
        "1 - Critical": 4,
        "2 - High": 3,
        "3 - Moderate": 2,
        "4 - Low": 1,
    }[request.form["priority"]]

    impact_score = {"1 - High": 3, "2 - Medium": 2, "3 - Low": 1}[
        request.form["impact"]
    ]

    urgency_score = {"1 - High": 3, "2 - Medium": 2, "3 - Low": 1}[
        request.form["urgency"]
    ]

    incident_state = encoders["incident_state"].transform(["Active"])[0]

    contact_type = encoders["contact_type"].transform(["Phone"])[0]

    location = encoders["location"].transform(["Location 204"])[0]

    u_symptom = encoders["u_symptom"].transform(["Symptom 491"])[0]

    cmdb_ci = encoders["cmdb_ci"].transform(["?"])[0]

    assigned_to = encoders["assigned_to"].transform(["?"])[0]

    knowledge = False

    active = True

    reopen_count = 0

    sys_mod_count = 0

    opened_hour = 12

    print("WEEKDAY:", encoders["opened_weekday"].classes_)
    print("MONTH:", encoders["opened_month"].classes_)
    print("SHIFT:", encoders["work_shift"].classes_)

    opened_weekday = encoders["opened_weekday"].transform(["Monday"])[0]

    print(encoders["opened_month"].classes_)

    opened_month = encoders["opened_month"].transform(["April"])[0]

    opened_day = 15

    opened_quarter = 1

    is_weekend = False

    is_business_hours = True

    work_shift = encoders["work_shift"].transform(["Day"])[0]

    input_df = pd.DataFrame(
        {
            "incident_state": [incident_state],
            "active": [active],
            "reassignment_count": [reassignment_count],
            "reopen_count": [reopen_count],
            "sys_mod_count": [sys_mod_count],
            "contact_type": [contact_type],
            "location": [location],
            "category": [category],
            "subcategory": [subcategory],
            "u_symptom": [u_symptom],
            "cmdb_ci": [cmdb_ci],
            "impact": [impact],
            "urgency": [urgency],
            "priority": [priority],
            "assignment_group": [assignment_group],
            "assigned_to": [assigned_to],
            "knowledge": [knowledge],
            "opened_hour": [opened_hour],
            "opened_weekday": [opened_weekday],
            "opened_month": [opened_month],
            "opened_day": [opened_day],
            "opened_quarter": [opened_quarter],
            "is_weekend": [is_weekend],
            "is_business_hours": [is_business_hours],
            "work_shift": [work_shift],
            "priority_score": [priority_score],
            "impact_score": [impact_score],
            "urgency_score": [urgency_score],
        }
    )

    print(input_df)

    print(input_df)
    print(input_df.dtypes)

    try:
        prediction = model.predict(input_df)[0]
        print("TAHMİN:", prediction)

        prediction_text = f"Tahmini çözüm süresi: {round(prediction, 2)} saat"

    except Exception as e:
        import traceback

        traceback.print_exc()

        prediction_text = f"Hata: {e}"

    return home(prediction_text, "tahmin", selected_values)


# =========================
# ÇALIŞTIR
# =========================

if __name__ == "__main__":

    app.run(debug=True)

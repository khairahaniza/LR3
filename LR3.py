import json
import streamlit as st

rules_json = """
[
    {
        "name": "Top merit candidate",
        "priority": 100,
        "conditions": [
            ["cgpa", ">=", 3.7],
            ["co_curricular_score", ">=", 80],
            ["family_income", "<=", 8000],
            ["disciplinary_actions", "==", 0]
        ],
        "action": {
            "decision": "AWARD_FULL",
            "reason": "Excellent academic & co-curricular performance, with acceptable need"
        }
    },
    {
        "name": "Good candidate - partial scholarship",
        "priority": 80,
        "conditions": [
            ["cgpa", ">=", 3.3],
            ["co_curricular_score", ">=", 60],
            ["family_income", "<=", 12000],
            ["disciplinary_actions", "<=", 1]
        ],
        "action": {
            "decision": "AWARD_PARTIAL",
            "reason": "Good academic & involvement record with moderate need"
        }
    },
    {
        "name": "Need-based review",
        "priority": 70,
        "conditions": [
            ["cgpa", ">=", 2.5],
            ["family_income", "<=", 4000]
        ],
        "action": {
            "decision": "REVIEW",
            "reason": "High need but borderline academic score"
        }
    },
    {
        "name": "Low CGPA – not eligible",
        "priority": 95,
        "conditions": [
            ["cgpa", "<", 2.5]
        ],
        "action": {
            "decision": "REJECT",
            "reason": "CGPA below minimum scholarship requirement"
        }
    },
    {
        "name": "Serious disciplinary record",
        "priority": 90,
        "conditions": [
            ["disciplinary_actions", ">=", 2]
        ],
        "action": {
            "decision": "REJECT",
            "reason": "Too many disciplinary records"
        }
    }
]
"""

rules = json.loads(rules_json)

def evaluate_rules(applicant):
    matched_rules = []

    for rule in rules:
        conditions_met = True

        for condition in rule["conditions"]:
            field, operator, value = condition
            applicant_value = applicant[field]

            if operator == ">=":
                if not (applicant_value >= value): conditions_met = False
            elif operator == "<=":
                if not (applicant_value <= value): conditions_met = False
            elif operator == "==":
                if not (applicant_value == value): conditions_met = False
            elif operator == "<":
                if not (applicant_value < value): conditions_met = False
            elif operator == ">":
                if not (applicant_value > value): conditions_met = False

        if conditions_met:
            matched_rules.append(rule)

    if not matched_rules:
        return {"decision": "NO_DECISION", "reason": "No matching rule found."}

    best_rule = sorted(matched_rules, key=lambda r: r["priority"], reverse=True)[0]

    return {
        "rule_name": best_rule["name"],
        "decision": best_rule["action"]["decision"],
        "reason": best_rule["action"]["reason"]
    }

st.title("🎓 Scholarship Advisory Rule-Based System")

cgpa = st.number_input("CGPA", min_value=0.0, max_value=4.0, step=0.01)
co = st.number_input("Co-curricular Score", min_value=0, max_value=100)
income = st.number_input("Family Income (RM)")
discipline = st.number_input("Number of Disciplinary Actions", min_value=0, max_value=10)

if st.button("Evaluate Scholarship"):
    applicant = {
        "cgpa": cgpa,
        "co_curricular_score": co,
        "family_income": income,
        "disciplinary_actions": discipline
    }

    result = evaluate_rules(applicant)

    st.subheader("Result")
    st.write("📌 **Decision:**", result["decision"])
    st.write("📝 **Reason:**", result["reason"])


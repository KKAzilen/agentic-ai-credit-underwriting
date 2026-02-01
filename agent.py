import json

# -----------------------------
# Intake Agent
# -----------------------------
def intake_agent(applicant):
    required_fields = ["annual_income", "credit_score", "employment_type"]
    for field in required_fields:
        if field not in applicant:
            return False, f"Missing required field: {field}"
    return True, "Applicant data validated"


# -----------------------------
# Risk Assessment Agent
# -----------------------------
def risk_assessment_agent(applicant):
    score = 0

    if applicant["credit_score"] >= 700:
        score += 2
    elif applicant["credit_score"] >= 650:
        score += 1

    if applicant["annual_income"] >= 60000:
        score += 2
    elif applicant["annual_income"] >= 40000:
        score += 1

    return score


# -----------------------------
# Policy Check Agent
# -----------------------------
def policy_check_agent(applicant, risk_score):
    if applicant["credit_score"] < 600:
        return False, "Credit score below minimum policy threshold"

    if risk_score <= 1:
        return False, "Risk score too low"

    return True, "Policy checks passed"


# -----------------------------
# Decision Agent
# -----------------------------
def decision_agent(risk_score):
    if risk_score >= 4:
        return "Approved"
    elif risk_score >= 2:
        return "Manual Review"
    else:
        return "Rejected"


# -----------------------------
# Explanation Agent
# -----------------------------
def explanation_agent(applicant, decision):
    return (
        f"The application was {decision.lower()} based on a credit score of "
        f"{applicant['credit_score']} and an annual income of "
        f"{applicant['annual_income']}."
    )


# -----------------------------
# Orchestrator
# -----------------------------
def run_underwriting_pipeline(applicant):
    valid, message = intake_agent(applicant)
    if not valid:
        return {"id": applicant["id"], "decision": "Rejected", "reason": message}

    risk_score = risk_assessment_agent(applicant)

    policy_passed, policy_message = policy_check_agent(applicant, risk_score)
    if not policy_passed:
        return {"id": applicant["id"], "decision": "Rejected", "reason": policy_message}

    decision = decision_agent(risk_score)
    explanation = explanation_agent(applicant, decision)

    return {
        "id": applicant["id"],
        "decision": decision,
        "explanation": explanation
    }


# -----------------------------
# Run Example
# -----------------------------
if __name__ == "__main__":
    with open("sample_applicants.json") as f:
        applicants = json.load(f)

    for applicant in applicants:
        result = run_underwriting_pipeline(applicant)
        print(result)

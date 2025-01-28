import streamlit as st
import random

# Define life expectancy for demographic evaluation
LIFE_EXPECTANCY = {
    "Male": 73,
    "Female": 79,
    "Other": 76  # Default life expectancy for non-binary/unspecified gender
}

# Collect applicant demographics
applicant_info = {}

def collect_applicant_info():
    def submit_info():
        try:
            applicant_info["Name"] = name_entry.get().strip()
            applicant_info["Age"] = int(age_entry.get().strip())
            applicant_info["Gender"] = gender_var.get()
            applicant_info["Mobility Device"] = mobility_var.get()
            if not applicant_info["Name"] or not applicant_info["Gender"] or not applicant_info["Mobility Device"]:
                raise ValueError
            root.destroy()
        except ValueError:
            messagebox.showerror("Error", "Please fill out all fields correctly.")

# Track demographic submission
if "applicant_info" not in st.session_state:
    st.session_state["applicant_info"] = {"submitted": False}

if not st.session_state["applicant_info"].get("submitted", False):
    st.title("Demographics")
    st.write("Please provide your information below:")

    # Streamlit widgets for data collection
    name = st.text_input("Full Name:")
    age = st.number_input("Age:", min_value=0, max_value=120, step=1)
    gender = st.selectbox("Gender:", ["Male", "Female", "Other"])
    mobility_device = st.radio("Do you use a mobility device?", ["Yes", "No"])

    if st.button("Submit Demographics"):
        if name.strip() and age and gender and mobility_device:
            # Save demographic info to session state
            st.session_state["applicant_info"] = {
                "Name": name.strip(),
                "Age": int(age),
                "Gender": gender,
                "Mobility Device": mobility_device,
                "submitted": True
            }
            st.session_state["current_question_index"] = 0  # Ensure first question starts
            st.experimental_rerun()  # Reload to move directly to the first question
        else:
            st.error("Please fill out all fields correctly.")
else:
    # Ensure we transition to the first question immediately
    if st.session_state["current_question_index"] < len(randomized_questions):
        display_question(st.session_state["current_question_index"])
    else:
        st.title("Thank You!")
        st.write("You have completed the questionnaire.")
        st.write("Your responses:")
        st.json(st.session_state["responses"])

# Question submission logic
def display_question(index):
    question_data = randomized_questions[index][1]
    st.write(question_data["text"])

    # Radio buttons for answer choices
    selected_option = st.radio(
        "Choose an option:",
        options=list(question_data["options"].keys()),
        format_func=lambda x: question_data["options"][x],
        key=f"question_{index}",
    )

    # Button to submit the answer and move to the next question
    if st.button("Submit Answer", key=f"submit_answer_{index}"):
        if selected_option is not None:  # Check if an option is selected
            # Save the response
            st.session_state["responses"][randomized_questions[index][0]] = selected_option

            # Increment the question index
            st.session_state["current_question_index"] += 1  # Move to the next question

            # Rerender the application to display the next question
            st.experimental_rerun()
        else:
            # Display an error message if no option is selected
            st.error("Please select an option before proceeding.")

# Define the questions
questions = {
    "Q1": {
        "text": "How often do you use public transit?",
        "options": {
            0: "Daily",
            1: "Weekly",
            2: "Occasionally",
            3: "Rarely",
            4: "Never"
        }
    },
    "Q50": {
        "text": "How often do background noises interfere with your ability to hear transit announcements?",
        "options": {
            0: "Never",
            1: "Rarely",
            2: "Sometimes",
            3: "Often",
            4: "Always"
        }
    }
}  
# Shuffle the questions for randomness
randomized_questions = list(questions.items())
random.shuffle(randomized_questions)

responses = {}
current_question_index = 0

def calculate_score(responses):
    score = 0
    middle_count = 0
    for _, answer in responses.items():
        score += answer
        if answer == 2:
            middle_count += 1
    return score, middle_count

def classify_impairments_and_scores(responses):
    classifications = []
    category_scores = {
        "Vision Impairment": 0,
        "Cognitive Impairment": 0,
        "Physical Impairment": 0,
        "Hearing Impairment": 0,
    }

    vision_questions = ["Q3", "Q15", "Q24"]
    cognitive_questions = ["Q4", "Q12", "Q26"]
    physical_questions = ["Q2", "Q7", "Q29"]
    auditory_questions = ["Q16", "Q50"]

    for q in vision_questions:
        category_scores["Vision Impairment"] += responses.get(q, 0)
    for q in cognitive_questions:
        category_scores["Cognitive Impairment"] += responses.get(q, 0)
    for q in physical_questions:
        category_scores["Physical Impairment"] += responses.get(q, 0)
    for q in auditory_questions:
        category_scores["Hearing Impairment"] += responses.get(q, 0)

    if category_scores["Vision Impairment"] > 2:
        classifications.append("Vision Impairment")
    if category_scores["Cognitive Impairment"] > 2:
        classifications.append("Cognitive Impairment")
    if category_scores["Physical Impairment"] > 2:
        classifications.append("Physical Impairment")
    if category_scores["Hearing Impairment"] > 2:
        classifications.append("Hearing Impairment")

    return classifications, category_scores

def determine_eligibility(score, middle_count, total_questions, applicant_info):
    age = applicant_info["Age"]
    gender = applicant_info["Gender"]
    mobility_device = applicant_info["Mobility Device"]

    if age > LIFE_EXPECTANCY.get(gender, 76):
        return "Unconditional Eligibility"

    if score >= 120:  # Threshold for high scores
        return "Unconditional Eligibility"

    if mobility_device == "Yes":
        return "Conditional Eligibility"

    if middle_count >= total_questions * 0.75:
        return "Ineligible"
    elif 80 <= score < 120:  # Adjusted threshold for Conditional Eligibility
        return "Conditional Eligibility"
    else:
        return "Ineligible"

def determine_pca(responses):
    pca_questions = ["Q5", "Q18"]
    return any(responses.get(q, 0) > 2 for q in pca_questions)

def generate_justification(score, eligibility, middle_count, classifications, category_scores, applicant_info):
    justification = (
        f"Applicant {applicant_info['Name']} (age {applicant_info['Age']}, gender {applicant_info['Gender']}) "
        f"achieved an overall score of {score}, resulting in a determination of {eligibility}. "
    )

    if classifications:
        justification += f"This determination was influenced by challenges related to: {', '.join(classifications)}. "

    if middle_count > 0:
        justification += (
            f"The applicant selected {middle_count} neutral responses, indicating moderate challenges that influenced "
            f"the eligibility outcome. "
        )

    total_category_score = sum(category_scores.values())
    if total_category_score > 0:
        justification += "\n\nCategory Impact on Transit Eligibility (Percentage Breakdown):\n"
        for category, score in category_scores.items():
            percentage = (score / total_category_score) * 100
            justification += f"- {category}: {percentage:.1f}%\n"

    total_impairments = len(classifications)
    if total_impairments > 0:
        proportion = total_impairments / 4
        justification += (
            f"A total of {total_impairments} out of 4 potential impairments were identified, "
            f"indicating {proportion * 100:.1f}% of possible impairments may affect transit eligibility. "
        )
    else:
        justification += "No specific impairments were identified that affect transit eligibility. "

    if eligibility == "Unconditional Eligibility":
        justification += "The applicant demonstrates severe and consistent barriers to using fixed-route transit services. "
    elif eligibility == "Conditional Eligibility":
        justification += (
            "The applicant shows specific barriers that limit fixed-route transit use under certain conditions, "
            "such as weather, fatigue, or accessibility challenges. "
        )
    else:
        justification += (
            "The applicant does not demonstrate sufficient barriers to qualify for paratransit services. "
        )

    justification += "\n\nDetailed Statistical Breakdown:\n"
    justification += f"- Total Score: {score}\n"
    justification += f"- Neutral Responses: {middle_count} out of {len(questions)} questions\n"
    justification += f"- Challenges Identified in: {', '.join(classifications) if classifications else 'None'}\n"
    justification += (
        f"- Age vs. Life Expectancy: {applicant_info['Age']} years old, expected lifespan for {applicant_info['Gender']} is {LIFE_EXPECTANCY.get(applicant_info['Gender'], 76)} years.\n"
    )

    return justification

def calculate_and_display_results():
    score, middle_count = calculate_score(responses)
    classifications, category_scores = classify_impairments_and_scores(responses)
    eligibility = determine_eligibility(score, middle_count, len(questions), applicant_info)
    pca_needed = determine_pca(responses)

    justification = generate_justification(score, eligibility, middle_count, classifications, category_scores, applicant_info)

    for widget in frame.winfo_children():
        widget.destroy()

    result_label = tk.Label(
        frame,
        text=f"Overall Score: {score}\nEligibility: {eligibility}\nPCA Required: {pca_needed}",
        wraplength=400,
        justify="left",
    )
    result_label.pack(pady=10)

    breakdown_label = tk.Label(frame, text=justification, wraplength=400, justify="left")
    breakdown_label.pack(pady=10)

    close_button = tk.Button(frame, text="Close", command=root.destroy)
    close_button.pack(pady=20)

def next_question():
    global current_question_index, responses

    selected_option = var.get()
    if selected_option == -1:
        messagebox.showwarning("Input Required", "Please select an option before proceeding.")
        return

    question_key = randomized_questions[current_question_index][0]
    responses[question_key] = selected_option

    current_question_index += 1

    if current_question_index < len(randomized_questions):
        display_question()
    else:
        calculate_and_display_results()

def display_question():
    global current_question_index

    question_data = randomized_questions[current_question_index][1]

    for widget in frame.winfo_children():
        widget.destroy()

    question_label = tk.Label(frame, text=question_data["text"], wraplength=400, justify="left")
    question_label.pack(pady=10)

    global var
    var = tk.IntVar(value=-1)
    for value, option in question_data["options"].items():
        tk.Radiobutton(frame, text=option, variable=var, value=value).pack(anchor="w")

    next_button = tk.Button(frame, text="Next", command=next_question)
    next_button.pack(pady=20)

import streamlit as st

# Title of the application
st.title("Paratransit Eligibility Questionnaire")

# Display questions one by one
current_question_index = st.session_state.get("current_question_index", 0)
responses = st.session_state.get("responses", {})

# Function to display a question
def display_question(index):
    question_data = randomized_questions[index][1]
    st.write(question_data["text"])

    # Radio buttons for answer choices
    selected_option = st.radio(
        "Choose an option:",
        options=list(question_data["options"].keys()),
        format_func=lambda x: question "options"][x],
        key=f"question_{index}",
    )

    # Button to submit the answer and move to the next question
    if st.button("Submit Answer", key=f"submit_answer_{index}"):
        if selected_option is not None:  # Ensure an option is selected
            # Save the response
            st.session_state["responses"][randomized_questions[index][0]] = selected_option

            # Increment the question index
            st.session_state["current_question_index"] += 1

            # Rerun the app to display the next question
            st.experimental_rerun()
        else:
            # Display an error message if no option is selected
            st.error("Please select an option before proceeding.")

# Main flow logic
if "applicant_info" not in st.session_state or not st.session_state["applicant_info"].get("submitted"):
    st.title("Demographics")
    st.write("Please provide your demographic information below:")

    name = st.text_input("Full Name:")
    age = st.number_input("Age:", min_value=0, max_value=120, step=1)
    gender = st.selectbox("Gender:", ["Male", "Female", "Other"])
    mobility_device = st.radio("Do you use a mobility device?", ["Yes", "No"])

    if st.button("Submit Demographics"):
        if name and age and gender and mobility_device:
            st.session_state["applicant_info"] = {
                "Name": name.strip(),
                "Age": int(age),
                "Gender": gender,
                "Mobility Device": mobility_device,
                "submitted": True,
            }
            st.session_state["current_question_index"] = 0
            st.experimental_rerun()
        else:
            st.error("Please fill out all fields correctly.")
else:
    current_question_index = st.session_state.get("current_question_index", 0)

    if current_question_index < len(randomized_questions):
        display_question(current_question_index)
    else:
        st.title("Thank You!")
        st.write("You have completed the questionnaire.")
        st.write("Your responses:")
        st.json(st.session_state["responses"])

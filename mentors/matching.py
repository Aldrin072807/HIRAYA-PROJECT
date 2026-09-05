def convert_to_list(value):
    if not value:
        return []
    return [item.strip().lower() for item in value.split(",") if item.strip()]


def calculate_match(user_profile, mentor):
    student_skills = set(convert_to_list(user_profile.skills))
    mentor_skills = set(convert_to_list(mentor.expertise))

    if not student_skills:
        skill_score = 0
    else:
        matching_skills = student_skills.intersection(mentor_skills)
        skill_score = (len(matching_skills) / len(student_skills)) * 100

    career_score = 0
    if user_profile.career_interests:
        career_interest = user_profile.career_interests.strip().lower()
        mentor_career = mentor.career_field.strip().lower()
        if career_interest in mentor_career or mentor_career in career_interest:
            career_score = 100

    final_score = (skill_score * 0.7) + (career_score * 0.3)
    return round(final_score)
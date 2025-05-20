def calculate_average(grade_1:str, grade_2:str, grade_3:str)->str:
    grades_list = []

    if grade_1:
        grades_list.append(int(grade_1))
    if grade_2:
        grades_list.append(int(grade_2))
    if grade_3:
        grades_list.append(int(grade_3))

    return str(round(sum(grades_list) / grades_list.__len__())) if grades_list else ""
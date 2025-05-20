
from custom_types.students_struct import StudentsStruct

def order_by_alphabetical(studens:StudentsStruct)->StudentsStruct:
    return sorted(studens, key=lambda sub_list: sub_list[0].upper())

def order_by_best_average(studens:StudentsStruct)->StudentsStruct:
    return sorted(studens, key=lambda sub_list: sub_list[5], reverse=True)

def order_by_unordered(studens:StudentsStruct)->StudentsStruct:
    return studens

order_by_dict = {
    "unordered": order_by_unordered,
    "alphabetical": order_by_alphabetical,
    "best_average": order_by_best_average
}
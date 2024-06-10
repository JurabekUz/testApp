import random
import pandas as pd
from fpdf import FPDF


def get_students(file_path):
    try:
        df = pd.read_excel(file_path)
        shuffle_df = df.sample(frac=1)
        return shuffle_df
    except Exception as e:
        print(e)


def get_tests_groupby(file_path):
    try:
        df = pd.read_excel(file_path)
        df_group = df.groupby('Daraja')  # default: sort=True group_keys=True
        return df_group
    except Exception as e:
        return None

def generate_test_1(st_path, test_path, q_levels):
    students = get_students(st_path)
    tests = get_tests_groupby(test_path)
    result_tests = []
    test_answers = {}
    number = 1
    for index, student in students.iterrows():
        st_dict = student.to_dict()
        st_dict['number'] = number
        st_dict['questions'] = []
        for level in q_levels:
            n = level[2] - level[1] + 1
            level_tests = tests.get_group(
                level[0]
            ).sample(n=n).to_dict(orient='records')
            st_dict['questions'] += level_tests

        # reorder variants
        answer_list = []
        for num, question in enumerate(st_dict['questions'], start=1):
            variants = ['B', 'A', 'D', 'C']
            random.shuffle(variants)
            answer_letter = random.choice(variants)
            # question['A'], question[var] = question[var], question['A']
            a = question['A']
            text = question[answer_letter]
            question[answer_letter] = a
            question['A'] = text
            question['num'] = num
            answer_list.append(answer_letter)

        result_tests.append(st_dict)
        test_answers[number] = answer_list
        number += 1

    return result_tests, test_answers


def generate_test_2(st_path, test_path, count):
    students = get_students(st_path)
    df = pd.read_excel(test_path)
    result_tests = []
    test_answers = {}
    number = 1
    for index, student in students.iterrows():
        st_dict = student.to_dict()
        st_dict['number'] = number
        st_questions = df.sample(n=count).to_dict(orient='records')
        # reorder variants
        answer_list = []
        for num, question in enumerate(st_questions, start=1):
            variants = ['B', 'A', 'D', 'C']
            random.shuffle(variants)
            answer_letter = random.choice(variants)
            # question['A'], question[var] = question[var], question['A']
            a = question['A']
            text = question[answer_letter]
            question[answer_letter] = a
            question['A'] = text
            question['num'] = num
            answer_list.append(answer_letter)
        st_dict['questions'] = st_questions
        result_tests.append(st_dict)
        test_answers[number] = answer_list
        number += 1
    return result_tests, test_answers


def generate_test_3(st_path, test_path, count):
    students = get_students(st_path)
    df = pd.read_excel(test_path)
    result_tests = []
    number = 1
    for index, student in students.iterrows():
        st_dict = student.to_dict()
        st_dict['number'] = number
        st_questions = df.sample(n=count).to_dict(orient='records')
        st_dict['questions'] = st_questions
        result_tests.append(st_dict)
        number += 1
    return result_tests

def write_tests_to_pdf_1(result_tests, test_answers, test_type, science_name, teacher_name, ql):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    for test in result_tests:
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=f"{science_name.encode('latin-1', 'replace').decode('latin-1')} fanidan {test_type} Nazorat ishi", ln=True, align='C')
        pdf.cell(200, 10, txt=f"Topshiruvchi: {test['Guruh']} talabasi {test['FIO'].encode('latin-1', 'replace').decode('latin-1')}", ln=True)
        pdf.cell(200, 10, txt=f"Qabul qiluvchi: {teacher_name.encode('latin-1', 'replace').decode('latin-1')}", ln=True)
        pdf.cell(200, 10, txt=f"{test['number']} - Bilet", ln=True)
        pdf.ln(3)

        for question in test['questions']:
            pdf.multi_cell(0, 10, txt=f"{question['num']}. {question['Savol'].encode('latin-1', 'replace').decode('latin-1')}")
            if ql:
                pdf.cell(0, 10, txt=f"Qiyinlik darajasi: {question['Daraja']}", ln=True)
            pdf.cell(0, 10, txt=f"A: {str(question['A']).encode('latin-1', 'replace').decode('latin-1')}", ln=True)
            pdf.cell(0, 10, txt=f"B: {str(question['B']).encode('latin-1', 'replace').decode('latin-1')}", ln=True)
            pdf.cell(0, 10, txt=f"C: {str(question['C']).encode('latin-1', 'replace').decode('latin-1')}", ln=True)
            pdf.cell(0, 10, txt=f"D: {str(question['D']).encode('latin-1', 'replace').decode('latin-1')}", ln=True)
            pdf.ln(3)

    # write answers
    pdf.add_page()
    pdf.cell(200, 10, txt='Javoblar', ln=True, align='C')
    pdf.ln(5)
    for number, answer_list in test_answers.items():
        answer_text = ' '.join([f"{number}: {letter}" for number, letter in enumerate(answer_list, start=1)])
        pdf.multi_cell(0, 10, txt=f"{number}-Bilet: {answer_text}")
        pdf.ln(2)

    return pdf

def write_tests_to_pdf_3(result_tests, test_type, science_name, teacher_name):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    for test in result_tests:
        pdf.add_page()
        pdf.set_font("Arial", size=14)
        pdf.cell(200, 10, txt=f"{science_name.encode('latin-1', 'replace').decode('latin-1')} fanidan {test_type} Nazorat ishi", ln=True, align='C')
        pdf.cell(200, 10, txt=f"Topshiruvchi: {test['Guruh']} talabasi {test['FIO'].encode('latin-1', 'replace').decode('latin-1')}", ln=True)
        pdf.cell(200, 10, txt=f"Qabul qiluvchi: {teacher_name.encode('latin-1', 'replace').decode('latin-1')}", ln=True)
        pdf.cell(200, 10, txt=f"{test['number']} - Bilet", ln=True)
        pdf.ln(5)

        for num, question in enumerate(test['questions'], start=1):
            pdf.multi_cell(0, 10, txt=f"{num}. {question['Savol'].encode('latin-1', 'replace').decode('latin-1')}")
            pdf.ln(3)

    return pdf


import pandas as pd
from app.models import *


def export_sheet(writer, user, test_name):
    test = Test.get(test_name=test_name)
    feedback = Feedback.get(user_id=user, test_id=test.id)
    if feedback is None:
        feedback = 'N/A'
    else:
        feedback = feedback.feedback
    questions = Question.get_all(test_id=test.id)
    headers = ['', 'Self Evaluation', 'System Evaluation', 'Complete Status']

    data = [headers, [f'Student ID: {user}']]
    for question in questions:
        question_name = question.question_name
        score = Score.get(user_id=user, question_id=question.id)
        if score is None:
            data.append([question_name, '', ''])
            continue
        else:
            data.append([question_name, score.user_score, score.sys_score])
    data.append([f'Feedback for test({test_name}): {feedback}'])
    data.append([])  # Empty row, if there is a next user
    print(data)
    return data, headers



def export_to_excel(user, week):
    if type(user) == list:
        filename = 'result.xlsx'
        writer = pd.ExcelWriter(filename, engine='xlsxwriter')
        if week != '':
            for u in user:

                export_sheet(writer, u, week)
        writer._save()
    elif type(user) == str:
        filename = f'{user}\'s result.xlsx'
        writer = pd.ExcelWriter(filename, engine='xlsxwriter')
        if week != '':  # Admin specify the week
            data, headers = export_sheet(writer, user, week)
            df = pd.DataFrame(data=data)
            df.to_excel(writer, index=False, sheet_name=week, header=None)

            # Access the XlsxWriter workbook and worksheet objects from the DataFrame.
            workbook = writer.book
            worksheet = writer.sheets[week]
            formatting(workbook, worksheet, data, headers)

        else:
            tests = Test.get_all()
            for test in tests:
                export_sheet(writer, user, test.test_name)
    # Save the Excel file.
        writer._save()

def formatting(workbook, worksheet, data, headers):
    # Formatting header cells with bold and a light gray fill.
    header_format = workbook.add_format({
        'bold': True,
        'align': 'center',
        'valign': 'vcenter',
        'bg_color': '#D3D3D3',
        'border': 1
    })

    # Formatting for general cells with border.
    cell_format = workbook.add_format({
        'border': 1
    })

    no_border_format = workbook.add_format()

    # Formatting for the "Student ID" and "Feedback" rows.
    merge_format = workbook.add_format({
        'bold': True,
        'bg_color': '#D3D3D3',
        'align': 'center',
        'valign': 'vcenter',
        'border': 1
    })

    # Apply header formatting
    for col_num, value in enumerate(headers):
        worksheet.write(0, col_num, value, header_format)

    # Adjust column width
    for i, column in enumerate(data[0]):
        max_length = max((len(str(row[i])) if i < len(row) else 0 for row in data), default=0)
        worksheet.set_column(i, i, max_length + 2, cell_format)  # +2 for some extra spacing

    # Adjusting the row height for the headers.
    worksheet.set_row(0, 20)

    # Automatically locate and merge cells for "Student ID" and "Feedback" rows
    for row_num, row in enumerate(data):
        if row and row[0].startswith('Student ID:'):
            worksheet.merge_range(f'A{row_num + 1}:D{row_num + 1}', row[0], merge_format)
        elif row and row[0].startswith('Feedback for test'):
            worksheet.merge_range(f'A{row_num + 1}:D{row_num + 1}', row[0], merge_format)
    # Freeze the header row
    worksheet.freeze_panes(1, 0)


if __name__ == "__main__":
    export_to_excel(['111', '123'],'week1')
import pandas as pd
from app.models import *


def export_sheet(user, test_name):  # Take an int as user id(pk)
    test = Test.get(test_name=test_name)
    feedback = Feedback.get(user_id=user, test_id=test.id)
    if feedback is None:
        feedback = 'N/A'
    else:
        feedback = feedback.feedback
    questions = Question.get_all(test_id=test.id)
    headers = ['', 'Self Evaluation', 'System Evaluation', 'Complete Status']

    data = [headers, [f'Student ID: {User.get(id=user).username}']]
    for question in questions:
        question_name = question.question_name
        score = Score.get(user_id=user, question_id=question.id)

        if score is None:
            data.append([question_name, '', '', ''])
            continue
        else:
            complete = 'Completed' if score.attempt_chosen in [1, 2, 3] else 'Uncompleted'
            data.append([question_name, score.user_score, score.sys_score, complete])
    data.append([f'Feedback for test({test_name}): {feedback}'])
    data.append([])  # Empty row, if there is a next user
    return data, headers


def export_to_excel(user, week):
    filename = ''
    if type(user) == list:
        datas = []
        headers = []
        if week != '':
            filename = f'result_{week}.xlsx'
            writer = pd.ExcelWriter(filename, engine='xlsxwriter')

            for u in user:
                data, headers = export_sheet(u, week)
                if not datas:
                    datas = data
                else:
                    datas += data[1:]
            df = pd.DataFrame(data=datas)
            df.to_excel(writer, index=False, sheet_name=week, header=None)

            workbook = writer.book
            worksheet = writer.sheets[week]
            formatting(workbook, worksheet, datas, headers)
            writer._save()

        else:
            filename = 'result_all.xlsx'
            writer = pd.ExcelWriter(filename, engine='xlsxwriter')
            tests = Test.get_all()
            for test in tests:
                datas = []  # Empty the data for the next sheet
                for u in user:
                    data, headers = export_sheet(u, test.test_name)
                    if not datas:
                        datas = data
                    else:
                        datas += data[1:]
                df = pd.DataFrame(data=datas)
                df.to_excel(writer, index=False, sheet_name=test.test_name, header=None)

                workbook = writer.book
                worksheet = writer.sheets[test.test_name]
                formatting(workbook, worksheet, datas, headers)
            writer._save()

    elif type(user) == str:
        user_id = User.get(username=user).id
        filename = f'{user}\'s result.xlsx'
        writer = pd.ExcelWriter(filename, engine='xlsxwriter')
        if week != '':  # Admin specify the week
            data, headers = export_sheet(user_id, week)
            df = pd.DataFrame(data=data)
            df.to_excel(writer, index=False, sheet_name=week, header=None)

            workbook = writer.book
            worksheet = writer.sheets[week]
            formatting(workbook, worksheet, data, headers)

        else:
            tests = Test.get_all()
            for test in tests:
                data, headers = export_sheet(user_id, test.test_name)
                df = pd.DataFrame(data=data)
                df.to_excel(writer, index=False, sheet_name=test.test_name, header=None)

                workbook = writer.book
                worksheet = writer.sheets[test.test_name]
                formatting(workbook, worksheet, data, headers)
        # Save the Excel file.
        writer._save()
    return filename


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

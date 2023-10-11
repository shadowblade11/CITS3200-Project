import pandas as pd
from app.models import *

gray = {'bg_color': 'gray', 'bold': True, 'border': 1, 'text_wrap': True, 'align': 'center',
         'valign': 'vcenter'}
bold_center = {'bold': True, 'align': 'center', 'valign': 'vcenter', 'border': 1}

def export_to_excel(user, week):
    if type(user) == list:
        pass
    elif type(user) == str:
        if type(week) == str:
            test = Test.get(test_name=week)
            feedback = Feedback.get(user_id=user, test_id=test.id)
            if feedback is None:
                feedback = 'N/A'
            else:
                feedback = feedback.feedback
            questions = Question.get_all(test_id=test.id)
            scores = []
            headers = ['']
            for i in range(1, len(questions) + 1):
                headers.extend([f'Q{i} Self Evaluation', f'Q{i} System Evaluation'])

            headers.extend(['Feedback'])
            data = [headers]
            for question in questions:
                score = Score.get(user_id=user, question_id=question.id)
                if score is None:
                    scores.extend(['', ''])
                    continue
                scores.extend([score.user_score, score.sys_score])
            data.append([f'Student ID: {user}'])
            data.append([f'Test: {week}'] + scores + [feedback])

            df = pd.DataFrame(data=data)
            filename = f'{user}\'s {week} result.xlsx'
            writer = pd.ExcelWriter(filename, engine='xlsxwriter')
            df.to_excel(writer, index=False, sheet_name='Sheet1', header=None)

            # Access the XlsxWriter workbook and worksheet objects from the DataFrame.
            workbook = writer.book
            worksheet = writer.sheets['Sheet1']
            formatting(workbook, worksheet, data, headers, df)

            # Save the Excel file.
            writer._save()

        else:
            tests = Test.get_all()

def formatting(workbook, worksheet, data, headers, df):
    # Formatting definitions
    bold_center_format = workbook.add_format(bold_center)
    border_format = workbook.add_format({'border': 1})

    # Set formatting for headers
    worksheet.set_row(0, None, bold_center_format)
    gray_format = workbook.add_format(gray)
    border_format = workbook.add_format({'border': 1})

    for i in range(len(headers)):
        worksheet.write(0, i, headers[i], bold_center_format)  # Apply bold to headers

    # Populate the data
    for row in range(1, len(data)):
        for col in range(len(data[row])):
            cell_format = gray_format if col == 0 and (row % 3) == 1 else border_format
            worksheet.write(row, col, data[row][col], cell_format)

    # Dynamically adjust the width of the first column to fit "Student ID" and "Test"
    max_length_col_A = max(len(data[1][0]), len(data[2][0])) + 2
    worksheet.set_column('A:A', max_length_col_A)

    # Dynamically adjust the column width for the headers and scores
    for i, column in enumerate(df.columns, start=1):
        max_length = max(df[column].astype(str).map(len).max(), len(str(column))) + 2  # +2 for a little more space
        worksheet.set_column(i, i, max_length)

    for row in range(len(data)):
        if "Student ID:" in data[row][0]:
            worksheet.merge_range(row, 0, row, len(headers) - 1, data[row][0], gray_format)
        else:
            for col in range(len(data[row])):
                worksheet.write(row, col, data[row][col], border_format if col > 0 else None)

    # Increase width for feedback column
    feedback_col_idx = headers.index("Feedback")
    worksheet.set_column(feedback_col_idx, feedback_col_idx, 20)  # Set to 20, but adjust as needed

    # Freeze panes to keep header row visible while scrolling
    worksheet.freeze_panes(1, 0)


if __name__ == "__main__":
    export_to_excel('111','week1')


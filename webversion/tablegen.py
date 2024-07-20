from .models import Department, Schedule, College
import docx
from docx.shared import Mm, Cm
from docx.enum.section import WD_ORIENT
from docx.enum.table import WD_ROW_HEIGHT_RULE


def tablegenerator(college_id, user_id, some_list):
    doc = docx.Document()
    section = doc.sections[0]
    section.page_height = Mm(279.4)
    section.page_width = Mm(471.8)
    section.orientation = WD_ORIENT.LANDSCAPE
    days = {1:"Monday", 2:"Tuesday", 3:"Wednesday", 4:"Thursday", 5:"Friday"}
    times = {0:"PERIOD",1:"8:00 - 8:55", 2:"9:00 - 9:55", 3:"10:30 - 11:25", 4:"11:30 - 12:25", 5:"1:00 - 1:55", 6:"2:00 - 2:55", 7:"3:00 - 3:55", 8:"4:00 - 4:55", 9:"5:00 - 5:55", 10:"6:00 - 6:55"}
    departments = Department.objects.filter(college_main_id=college_id)
    max_yg = (departments.order_by("-max_yg").first()).max_yg
    college = College.objects.get(id=college_id)
    rows_per_day = college.rows_per_day
    days_per_week = college.days_per_week
    d_counter = 1
    years = ["FIRST", "SECOND", "THIRD", "FOURTH", "FIFTH", "SIXTH", "SEVENTH", "HEIGTH", "NINTH"]
    for m in range(1, max_yg+1):
        for key, day in list(days.items()):
            header1 = doc.add_heading(f"College Of {college.name}")
            par1 = doc.add_heading(f"{years[m-1]} YEAR", 4)
            par2 = doc.add_paragraph(f"{day}")
            table = doc.add_table(rows=11, cols=len(departments)+1)
            table.style = 'Table Grid'
            doc.add_paragraph('Adding space between tables')
            doc.add_page_break()
            trow = table.rows[0].cells
            counter = 1
            for department in departments:
                trow[counter].text = department.name
                counter = counter + 1
            tcol = table.columns[0].cells
            counter = 0
            for time in list(times.values()):
                tcol[counter].text = time
                counter = counter + 1
            for sch in some_list:
                year_group = sch.year_group
                max_yg_row = year_group * (rows_per_day * days_per_week)
                min_yg_row = (max_yg_row + 1) - (rows_per_day * days_per_week)
                if sch.year_group == m:
                    if sch.day == key:
                        ss_row = (sch.row - min_yg_row + 1) % rows_per_day
                        if ss_row == 0: ss_row = rows_per_day
                        table.rows[ss_row].cells[sch.column].text = (f"\n{sch.course_code}\t\n{sch.location_name }\t\n{sch.lecturer_name}\n")
                        table.rows[ss_row].height_rule = WD_ROW_HEIGHT_RULE.AT_LEAST
            
    doc.save('C:\\Users\\Abel_Nana_Kwesi\\Desktop\\gfg2.docx')

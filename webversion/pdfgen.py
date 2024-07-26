import pythoncom
from .models import College, Docs
from pathlib import Path
from docx2pdf import *
from django.core.files import File



def createPdf(college_id, batch, doc):
    college = College.objects.get(id=college_id)
    i_path = Path(f"{college.name}_{batch}.docx")
    pythoncom.CoInitialize()
    convert(i_path)
    path = Path(f"{college.name}_{batch}.pdf")
    with path.open(mode="rb") as f:
        doc.pdf = File(f, name=path.name)
        doc.save()
    f.close()

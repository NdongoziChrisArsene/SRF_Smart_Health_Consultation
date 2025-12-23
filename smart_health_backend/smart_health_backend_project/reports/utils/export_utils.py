import csv
from io import StringIO, BytesIO
from openpyxl import Workbook
from reportlab.platypus import SimpleDocTemplate, Table
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors


# -----------------------------
# 1. CSV EXPORT
# -----------------------------
def export_to_csv(data, headers):
    """
    Exports list of dictionaries to CSV format.
    Returns CSV content as a string.
    """
    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=headers)
    writer.writeheader()
    writer.writerows(data)
    return output.getvalue()


# -----------------------------
# 2. XLSX EXPORT
# -----------------------------
def export_to_xlsx(data, headers):
    """
    Exports list of dictionaries to an XLSX file.
    Returns file bytes.
    """
    wb = Workbook()
    ws = wb.active
    ws.append(headers)

    for row in data:
        ws.append([row.get(h) for h in headers])

    output = BytesIO()
    wb.save(output)
    return output.getvalue()


# -----------------------------
# 3. PDF EXPORT
# -----------------------------
def export_to_pdf(data, headers):
    """
    Exports list of dictionaries to a PDF table.
    Returns PDF file bytes.
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)

    table_data = [headers] + [
        [row.get(h, "") for h in headers]
        for row in data
    ]

    table = Table(table_data)
    table.setStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, colors.black),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ])

    doc.build([table])
    pdf = buffer.getvalue()
    buffer.close()
    return pdf

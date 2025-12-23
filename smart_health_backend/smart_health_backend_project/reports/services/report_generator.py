# from django.template.loader import render_to_string
# from weasyprint import HTML
# from django.core.files.base import ContentFile
# import logging

# logger = logging.getLogger(__name__)


# class ReportGenerator:
#     @staticmethod
#     def generate_pdf(template: str, context: dict) -> ContentFile:
#         html = render_to_string(template, context)
#         pdf_bytes = HTML(string=html).write_pdf()
#         return ContentFile(pdf_bytes)




































import pandas as pd
from django.template.loader import render_to_string
from weasyprint import HTML
from django.core.files.base import ContentFile
from io import BytesIO
import logging
from typing import List, Dict

logger = logging.getLogger(__name__)

class ReportGenerator:
    """
    Utility class for generating PDF, Excel, and CSV reports.
    """

    @staticmethod
    def generate_pdf(template: str, context: dict) -> ContentFile:
        """
        Generates a PDF from a Django template and context.

        Args:
            template (str): Path to Django template.
            context (dict): Context for rendering the template.

        Returns:
            ContentFile: PDF content ready to save in a FileField.
        """
        try:
            html = render_to_string(template, context)
            pdf_bytes = HTML(string=html).write_pdf()
            return ContentFile(pdf_bytes)
        except Exception as e:
            logger.error(f"Failed to generate PDF from template '{template}': {e}")
            raise RuntimeError(f"PDF generation failed: {e}") from e

    @staticmethod
    def generate_excel(data: List[Dict], sheet_name: str = "Sheet1") -> ContentFile:
        """
        Generates an Excel file from a list of dictionaries.

        Args:
            data (List[Dict]): Data for Excel.
            sheet_name (str): Optional sheet name.

        Returns:
            ContentFile: Excel file content.
        """
        try:
            df = pd.DataFrame(data)
            with BytesIO() as output:
                with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
                    df.to_excel(writer, index=False, sheet_name=sheet_name)
                return ContentFile(output.getvalue())
        except Exception as e:
            logger.error(f"Failed to generate Excel file: {e}")
            raise RuntimeError(f"Excel generation failed: {e}") from e

    @staticmethod
    def generate_csv(data: List[Dict], encoding: str = "utf-8") -> ContentFile:
        """
        Generates a CSV file from a list of dictionaries.

        Args:
            data (List[Dict]): Data for CSV.
            encoding (str): File encoding.

        Returns:
            ContentFile: CSV file content.
        """
        try:
            df = pd.DataFrame(data)
            csv_bytes = df.to_csv(index=False, encoding=encoding).encode(encoding)
            return ContentFile(csv_bytes)
        except Exception as e:
            logger.error(f"Failed to generate CSV file: {e}")
            raise RuntimeError(f"CSV generation failed: {e}") from e




































# import pandas as pd
# from django.template.loader import render_to_string
# from weasyprint import HTML
# from django.core.files.base import ContentFile
# from io import BytesIO

# class ReportGenerator:

#     @staticmethod
#     def generate_pdf(template, context):
#         html = render_to_string(template, context)
#         pdf_file = HTML(string=html).write_pdf()
#         return ContentFile(pdf_file)

#     @staticmethod
#     def generate_excel(data):
#         df = pd.DataFrame(data)
#         output = BytesIO()
#         df.to_excel(output, index=False)
#         return ContentFile(output.getvalue())

#     @staticmethod
#     def generate_csv(data):
#         df = pd.DataFrame(data)
#         return ContentFile(df.to_csv(index=False).encode())

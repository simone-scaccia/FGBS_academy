import markdown2
import pdfkit
from crewai.tools import BaseTool
from markdown_pdf import MarkdownPdf, Section

class MarkdownToPdfExporter(BaseTool):

    name: str = "markdown_to_pdf_exporter"

    description: str = "Convert Markdown text into a PDF file and save it in ./outputs"

    def _run(self, markdown_content: str) -> str:
        filename = "quiz.pdf"
        out_path: str = f"./outputs/{filename}"
        pdf = MarkdownPdf()
        pdf.meta["title"] = filename
        pdf.add_section(Section(markdown_content, toc=False))
        pdf.save(out_path)
        return f"PDF file saved to {out_path}"
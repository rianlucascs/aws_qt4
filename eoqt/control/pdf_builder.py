from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, ListItem
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from dataclasses import dataclass
from sys import path
from control.build_info import BuildInfo
from control.read_transations import ReadTransations

@dataclass
class PDFBuilder:

    def __init__(self):
        self.filename = 'Overview_System_Report.pdf'
        self._path = path[0]+f'\\control\\{self.filename}'
        self.doc = SimpleDocTemplate(self._path, pagesize=letter)

    def create_title(self, title_text, fontname='Times-Roman', fontsize=20):
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle('Title', parent=styles['Title'], fontName=fontname, fontSize=fontsize)
        title = Paragraph(f'<b>{title_text}</b><br /><br />', title_style, )
        return title
    
    def create_text(self, text_, fontname='Helvetica', fontsize=14, bold=False, italic=False):
        styles = getSampleStyleSheet()  
        normal_style = ParagraphStyle('Normal', parent=styles['Normal'], fontName=fontname, fontSize=fontsize,
                                      bold=bold, italic=italic)
        text = Paragraph(f'{text_}<br /><br /><br />',  normal_style)
        return text

    def crate_table(sekf, data):
        style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), (0.8, 0.8, 0.8)),  
                            ('TEXTCOLOR', (0, 0), (-1, 0), (0, 0, 0)),       
                            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),            
                            ('GRID', (0, 0), (-1, -1), 1, (0, 0, 0))])        
        table = Table(data)
        table.setStyle(style)
        return table

    def add_element(self, element):
        self.doc.build(element)

    def create(self):
        build_info = BuildInfo()
        title = self.create_title(build_info.title_text)
        text1 = self.create_text('Daily Returns')
        data_table1 = build_info.table_transations()
        table1 = self.crate_table(data_table1)
        text2 = self.create_text(('<br />'*2) + 'Cumulative financial Profit')
        table2 = self.crate_table(build_info.result_all_strategies())
        text3 = self.create_text(('<br />'*2) + f'Total results: R$ {ReadTransations().result("sum") :,.2f}', fontsize=11)
        text4 = self.create_text('Risk')
        text5 = self.create_text(build_info.risk(), fontsize=11)
        self.add_element([title, text1, table1, text2, table2, text3, text4, text5])


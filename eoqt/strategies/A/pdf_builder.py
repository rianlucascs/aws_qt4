from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Image   
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from sys import path

from build_info import BuildInfo
from acess import Acess

from log import LogQT

class PDFBuilder(Acess):

    def __init__(self):
        self.doc = SimpleDocTemplate(path[0]+f'\\Strategy{Acess()._name}_Report.pdf', pagesize=letter)
        self._name = Acess()._name
        LogQT('PDFBuilder start').startup

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
    
    def create_image(self, image_path, width=None, height=None):
        if width and height:
            image = Image(image_path, width=width, height=height)
        else:
            image = Image(image_path)
        return image

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

    def main(self):
        build_info = BuildInfo()
        title = self.create_title(build_info.title_text)
        text1 = self.create_text(f'Strategy Metrics and Settings', fontname='Helvetica', fontsize=14)
        table1 = self.crate_table(build_info.settings_table())
        space1 = self.create_text(f'')
        table2 = self.crate_table(build_info.metric_table())

        text2 = self.create_text(('<br />'*17) + f'Daily Results')
        image1 = self.create_image(f'{path[0]}\\image1{self._name}.png', 380, 250)
        image2 = self.create_image(f'{path[0]}\\image2{self._name}.png', 380, 250)

        space3 = self.create_text(f'<br />'*10)
        table3 = self.crate_table(build_info.result_table())

        text3 = self.create_text((f'<br />'*4) + build_info.last_predict_sign(), fontsize=11)
        
        self.add_element([
            title,
            text1, table1, space1, table2, 
            text2, image1, image2, 
            space3,
            table3,
            text3
            ])

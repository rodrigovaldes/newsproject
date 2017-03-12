import numpy as np

from plot_pred import build_plot

from pylatex import Document, MiniPage, PageStyle, Section, Subsection, Tabular, \
                    MultiColumn, Head, Foot, Figure, LargeText, \
                    MediumText, LineBreak, simple_page_number
from pylatex.utils import italic, bold, NoEscape

import os
import time

# subprocess error with gen_pdf
# filepath with the picture
# challenge, their package not stable
# newly added simple page number is not returning correct value

class Report:
    """docstring for ClassName"""
    
    def __init__(self, margin='1.0in', default_filepath='./reports/report'):
        

        parentdir= os.path.dirname(default_filepath)

        if not os.path.exists(parentdir):
            os.makedirs(parentdir)
        
        geometry_options = {'margin': margin, 'paperheight': '11in', \
                            'paperwidth':'8.5in'}
        
        self.doc = Document(default_filepath= default_filepath, \
                            geometry_options=geometry_options, font_size='large')
        

    def add_headfoot(self, header_image):
        '''
        '''
        header = PageStyle('header')
        
        today = time.strftime('%B %d %Y')
        company = 'Ochoa Valdés-Ortiz Zhang Ltd.'

        #add header
        with header.create(Head('C')) as cheader:
            with cheader.create(Figure(position='t!')) as graph:
                graph.add_image(header_image, width='300px')

        
        #left footer
        with header.create(Foot('L')):
            header.append(today)
            header.append(LineBreak())
            header.append(company)
        
        #right footer
        with header.create(Foot('R')):
            header.append(simple_page_number())

        
        self.doc.preamble.append(header)

        self.doc.change_document_style('header')

    def set_title(self, title, subtitle):
        '''
        '''
        with self.doc.create(MiniPage(align='c')):
            self.doc.append(LargeText(bold(title)))
            self.doc.append(LineBreak())
            self.doc.append(MediumText(italic(bold(subtitle))))

    def add_executive_summary(self, text):
        '''
        '''
        with self.doc.create(Section('Executive Summary')) as summary:
            with summary.create(Tabular('p{15.4cm}')) as sumtable:
                sumtable.add_hline()
                sumtable.add_row([italic(text)])
                sumtable.add_empty_row()
                sumtable.add_empty_row()


    def insert_graph(self, graph_fname):
        '''
        '''
        with self.doc.create(Figure(position='h!')) as graph:
            graph.add_image(graph_fname, width='300px')

    def insert_table(self, results):
        '''
        '''
        indie_var = ' '.join(results['independent_var'])

        section = Section('Statistical Results')

        table = Tabular('l p{10cm}')
        table.add_hline()
        table.add_row((MultiColumn(2, align='c', data=bold('Characteristics of Model')),))
        table.add_hline(cmidruleoption='r')
        table.add_row((bold('Model'), 'AR'), color='lightgray')
        table.add_row((bold('Lag variables'), results['lag']))
        table.add_row((bold('Independent variables'), indie_var), color='lightgray')
        table.add_row((bold('Number of differences'), results['num_diff']))
        table.add_row((NoEscape('\symbf{$R^2$}'), results['R2']), color='lightgray')
        table.add_row((bold('Durbin Watson Statistic'), results['stat']))
        table.add_hline()
        
        section.append(LineBreak())
        section.append(table)

        self.doc.append(section)

    def gen_pdf(self, filepath=None):
        '''
        '''
        self.doc.generate_pdf(filepath, clean_tex=False)


if __name__ == '__main__':

    #Rod passes me a list of df, and ten dictionaries

    header_image = '../commodity-pic.jpg'

    results = {'lag':1, 'R2': 0.99, 'stat': 5.66, 'num_diff': 4,\
               'independent_var': ['apple', 'banana', 'pear', 'peach']}
    
    r = Report()

    r.set_title('Forecast', 'Wheat')
    r.add_headfoot(header_image)
    r.add_executive_summary('Summary')
    r.insert_graph('../analysis/plot_result.png')
    r.insert_table(results)
    r.gen_pdf()
    
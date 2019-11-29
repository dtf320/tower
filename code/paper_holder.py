import re
import time
import os
from utils import *


class Paper:
    def __init__(self, title='',sec_title='',pdf='',year=''):
        if pdf == '':
            raise Exception('PDF name or category cannot be empty')
        if title == '' and sec_title == '':
            raise Exception('Title and simple_title cannot be empty at the same time.')

        self.title = title
        self.sec_title = sec_title
        self.pdf = pdf
        self.year = year

    def set_category(self, category):
        self.category = category
        return self

    def set_pdf(self, pdf):
        self.pdf = pdf
        return self

    @staticmethod
    def load_pdf_dir(pdf_dir):
        """
        加载目录中的所有pdf文件，依次生成Paper实例，目录名称就是该论文的类别

        :param pdf_dir:
        :return:
        """
        category = os.path.split(pdf_dir)[1]
        pdfs = os.listdir(pdf_dir)
        pdfs = [_ for _ in pdfs if _.endswith('.pdf')]
        papers = [Paper.pdf_name_convert_obj(p) for p in pdfs]
        sort_idx = sort_by_date([_.year for _ in papers])
        papers = [papers[k] for k in sort_idx]
        papers = [p.set_category(category) for p in papers]
        papers = [p.set_pdf('{}/{}'.format(category,p.pdf)) for p in papers]
        return papers


    @staticmethod
    def pdf_name_convert_obj(pdf):
        """
        目录名称就是论文的类别

        :param pdf: pdf文件名称  simple_title-title-year.pdf or title-year.pdf
        :return:
        """
        tmp = pdf[:-4].split('-')
        if len(tmp) == 2:
            title = tmp[0]
            year = tmp[1]
            sec_title = ''
        elif len(tmp) == 3:
            title = tmp[0]
            sec_title = tmp[1]
            year = tmp[2]
        else:
            raise Exception('{}命名错误， 格式为 simple_title-title-year-category.pdf 或 title-year-category.pdf'.format(pdf))
        return Paper(title,sec_title,year=year,pdf=pdf)


class PaperHolder:
    def __init__(self, paper_dir):
        self.paper_dir = os.path.realpath(paper_dir)
        self.parent_dir_of_papers = os.path.split(self.paper_dir)[0]
        self.dirname_papers = os.path.split(self.paper_dir)[1]
        self.base_file = os.path.join(os.path.split(__file__)[0],'base')

        with open(self.base_file, 'r') as f:
            self.context = f.read()
        self.context = re.sub('#{:last_update_time:}!', time.strftime('%d %b. %Y'),self.context)

        self.sections = []

    def make(self, html_name='index'):
        dir_list = os.listdir(self.paper_dir)
        sort_idx = sort_by_index(dir_list)
        dir_list = [dir_list[k] for k in sort_idx]
        for c in dir_list:
            cdir = os.path.join(self.paper_dir,c)
            if not os.path.isdir(cdir):
                continue
            papers = Paper.load_pdf_dir(cdir)
            self._add_section(c,papers)
        text = ''.join(self.sections)
        self.context = re.sub('#{:replace_this_way:}!', text, self.context)
        with open(os.path.join(self.parent_dir_of_papers,'{}.html'.format(html_name)),'w') as f:
            f.write(self.context)

    def _add_section(self, section_name, papers):
        """
        <h2>section_name</h2>
            <ol>
                <li>  </li>
            </ol>

        :param section_name:
        :param papers: [Paper(),Paper(),...]
        :return:
        """
        section_name = section_name.strip()
        text = ''
        text += '<h2>{}</h2>\n'.format(section_name)
        text += '<ol>\n'
        text += ''.join([self._create_li(_) for _ in papers])
        text += '</ol>\n'
        self.sections.append(text)

    def _create_li(self, paper):
        li = '<li><b>{}</b>[<a href="{}">pdf</a>] {},{}</li><br>\n'.format(paper.title,
                                                                          '{}/{}'.format(self.dirname_papers,paper.pdf),
                                                                          paper.sec_title,
                                                                          paper.year)
        return li


if __name__ == "__main__":
    holder = PaperHolder(paper_dir='../papers')
    holder.make()
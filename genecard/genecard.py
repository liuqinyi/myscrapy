import pandas as pd
import csv
import glob
from lxml import etree
import logging
import re, os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input_dir', help='Input html file dir', default='/NAS/Tasly_Knowledge_Base/Public-Database/GeneCards/GeneCardInfoHTML/')
parser.add_argument('-s', '--output_dir', help='output dir', default='output/')
parser.add_argument('-o', '--output_file', help='save csv file', default='genecard.csv')


# logging.basicConfig(filename='logger.log', level=logging.INFO)

def parseContent(texts, sep='|'):
    r = r'\r\n *'
    texts = [re.sub(r, '', text.strip()) for text in texts]
    contents = sep.join(list(filter(None, texts)))
    return contents


def parseString(str):
    str = re.sub(r'\s', ' ', str).strip()
    return re.sub(r' {2,}', ' ', str)


def parse_ul(ul, key_tag, value_tag):
    items = []
    for li in ul:
        keys = li.xpath('%s//text()' % key_tag)
        values = li.xpath('%s//text()' % value_tag)
        for key, value in zip(keys, values):
            items.append(key + value)
    return '|'.join(items)


def gene_data_generator(htmls, section, subsection):
    section_available_headers = section
    subsection_available_headers = subsection
    for html in htmls:
        file = html.split('/')[-1]
        ID = file.split('_')[-2]
        max_size = ''
        try:
            html = etree.parse(html, etree.HTMLParser())
            sections = html.xpath('//section')
            gene_name = parseString(html.xpath('string(//h1[@id="geneSymbol"]/strong/em)'))
            # 结果有160条左右数据缺失

            data = {}
            for col in subsection_available_headers:
                data[col] = 'NULL'
            data['ID'] = ID
            data['Gene Name'] = gene_name
            # print(gene_name)
            # print('++++++++++++++++++++++++')

            for sec_inx, section in enumerate(sections):
                section_header = parseContent(section.xpath('h2/text()'))
                if section_header not in section_available_headers:
                    continue
                # print('\nSection:', section_header)
                subsections = section.xpath('.//div[@class="gc-subsection"]')
                for subsection in subsections:
                    sub_header = parseString(subsection.xpath('string(.//h3)'))
                    sub_header = sub_header.split(' for')[0].strip()
                    if sub_header not in subsection_available_headers:
                        continue
                    # print('Subsection:', sub_header)
                    if section_header == 'Aliases':
                        if sub_header == 'Aliases':
                            aliase_main_name = parseContent(subsection.xpath('.//span/text()'))
                            aliase_name = parseContent(subsection.xpath('.//li/text()'))
                            content = '|'.join([aliase_main_name, aliase_name])
                            
                            data['Aliases'] = content
                        if sub_header == 'External Ids':
                            items = []
                            for li in subsection.xpath('.//li'):
                                id_source = li.xpath('text()')[0].strip()
                                id = li.xpath('a/text()')[0].strip()
                                items.append(id_source + id)
                            content = '|'.join(items)
                            
                            data['External Ids'] = content

                        if sub_header == 'Previous HGNC Symbols':
                            content = parseContent(subsection.xpath('.//li/text()'))
                            
                            data['Previous HGNC Symbols'] = content

                    if section_header == 'Summaries':
                        if sub_header == 'Entrez Gene Summary':
                            content = parseString(subsection.xpath('string(.//p)'))
                            data['Entrez Gene Summary'] = content
                        if sub_header == 'GeneCards Summary':
                            content = parseString(subsection.xpath('string(.//p)'))
                            data['GeneCards Summary'] = content
                        if sub_header == 'UniProtKB/Swiss-Prot':
                            content = parseString(subsection.xpath('string(.)'))
                            data['UniProtKB/Swiss-Prot'] = content
                        if sub_header == 'Additional gene information':
                            content = parseContent(subsection.xpath('.//ul[@class="list-inline"]/li//text()'))
                            data['Additional gene information'] = content
                        if sub_header == 'Gene Wiki entry':
                            content = parseString(subsection.xpath('string(.)'))
                            data['Gene Wiki entry'] = content
                        if sub_header == 'CIViC Summary':
                            content = parseString(subsection.xpath('string(.//p)'))
                            data['CIViC Summary'] = content
                        if sub_header == 'Tocris Summary':
                            content = parseString(subsection.xpath('string(.//p)'))
                            data['Tocris Summary'] = content

                    if section_header == 'Proteins':
                        if sub_header == 'Protein details':
                            content = parseString(subsection.xpath('string(div[@class="gc-subsection-inner-wrap"])'))
                            data['Protein details'] = content
                        if sub_header == 'Protein attributes':
                            content = parseString(subsection.xpath('string(div[@class="gc-subsection-inner-wrap"])'))
                            data['Protein attributes'] = content
                        if sub_header == 'Post-translational modifications':
                            content = parseString(subsection.xpath('string(div[@class="gc-subsection-inner-wrap"])'))
                            data['Post-translational modifications'] = content
                            
                    if section_header == 'Domains & Families':
                        if sub_header == 'Gene Families':
                            content = parseString(subsection.xpath('string(div[@class="gc-subsection-inner-wrap"])'))
                            data['Gene Families'] = content
                            
                        if sub_header == 'Protein Domains':
                            content = parseString(subsection.xpath('string(div[@class="gc-subsection-inner-wrap"])'))
                            data['Protein Domains'] = content
                            
                        if sub_header == 'Suggested Antigen Peptide Sequences':
                            content = parseString(subsection.xpath('string(div[@class="gc-subsection-inner-wrap"])'))
                            data['Suggested Antigen Peptide Sequences'] = content
                            
                        if sub_header == 'UniProtKB/Swiss-Prot:':
                            content = parseString(subsection.xpath('string(div[@class="gc-subsection-inner-wrap"])'))
                            
                            data['UniProtKB/Swiss-Prot:'] = content

                    if section_header == 'Function':
                        if sub_header == 'Molecular function':
                            content = parseString(subsection.xpath('string(div[@class="gc-subsection-inner-wrap"])'))
                            
                            data['Molecular function'] = content

                    if section_header == 'Localization':
                        if sub_header == 'Subcellular locations from UniProtKB/Swiss-Prot':
                            content = parseString(subsection.xpath('string(div[@class="gc-subsection-inner-wrap"])'))
                            
                            data['Subcellular locations from UniProtKB/Swiss-Prot'] = content

                    # 表格获取问题
                    if section_header == 'Pathways & Interactions':
                        if sub_header == 'SuperPathways':
                            content = parseContent(subsection.xpath('.//table//text()'), sep=' ')
                            data['SuperPathways'] = content
                    if section_header == 'Expression':
                        if sub_header == 'Protein differential expression in normal tissues from HIPED':
                            content = parseString(subsection.xpath('string(div[@class="gc-subsection-inner-wrap"])'))
                            data['Protein differential expression in normal tissues from HIPED'] = content
                            
                        if sub_header == 'mRNA differential expression in normal tissues according to GTEx':
                            content = parseString(subsection.xpath('string(div[@class="gc-subsection-inner-wrap"])'))
                            data['mRNA differential expression in normal tissues according to GTEx'] = content
                            
                        if sub_header == 'Protein tissue co-expression partners':
                            content = parseContent(subsection.xpath('.//ul//text()'))
                            data['Protein tissue co-expression partners'] = content
                            
                        if sub_header == 'mRNA Expression by UniProt/SwissProt':
                            content = parseString(subsection.xpath('string(div[@class="gc-subsection-inner-wrap"])'))
                            
                            data['mRNA Expression by UniProt/SwissProt'] = content
            # print(data)
            yield data
        except Exception as e:
            print('parse gene error:', html, '\tError is:', e)
            with open('error_file.log', 'a+', encoding='utf-8', newline='') as ef:
                ef.write(file)


def main(args):
    dir = args.input_dir
    save_dir = args.output_dir
    save_file = args.output_file
    if not os.path.isdir(save_dir):
        os.makedirs(save_dir)
    genecards_htmls = glob.glob(dir + '*.html')

    section = ['Aliases', 'Summaries', 'Proteins', 'Domains & Families', 'Function',
               'Localization', 'Pathways & Interactions', 'Expression']
    subsection = ['ID', 'Gene Name', 'Aliases', 'External Ids', 'Previous HGNC Symbols',
                  'Entrez Gene Summary', 'GeneCards Summary', 'UniProtKB/Swiss-Prot',
                  'CIViC Summary','Tocris Summary',
                  'Additional gene information', 'Gene Wiki entry',
                  'Protein details', 'Protein attributes', 'Post-translational modifications',
                  'Protein Domains', 'Suggested Antigen Peptide Sequences', 'UniProtKB/Swiss-Prot:',
                  'Molecular function',
                  'Subcellular locations from UniProtKB/Swiss-Prot',
                  'SuperPathways',
                  'Protein differential expression in normal tissues from HIPED',
                  'Protein tissue co-expression partners', 'mRNA Expression by UniProt/SwissProt',
                  'mRNA differential expression in normal tissues according to GTEx']

    save_file = save_dir + save_file
    with open(save_file, 'w', encoding='utf-8', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=subsection)
        writer.writeheader()
        for gene in gene_data_generator(genecards_htmls, section, subsection):
            writer.writerow(gene)


if __name__ == '__main__':
    args = parser.parse_args()
    main(args)

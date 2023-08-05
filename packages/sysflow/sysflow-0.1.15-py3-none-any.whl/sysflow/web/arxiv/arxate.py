from pybtex.database import parse_file, parse_string
from sysflow.web.arxiv.arxb import arxb, extract_from_text
from rich import print

def clean_key(bib_string): 
    # clean the key due to the accent
    # some issue with the parse_string
    # 
    # e.g.
    # @article{s{\o}rdal2019deep,
    # author = "S{\o}rdal, Vegard B. and Bergli, Joakim",
    # doi = "10.1103/physreva.100.042314",
    # url = "https://doi.org/10.1103%2Fphysreva.100.042314",
    # year = "2019",
    # month = "oct",
    # publisher = "American Physical Society ({APS})",
    # volume = "100",
    # number = "4",
    # title = "Deep reinforcement learning for quantum Szilard engine optimization",
    # journal = "Physical Review A"
    # }
    bib_string_list = bib_string.lstrip().split('\n')
    head_string = bib_string_list[0]
    new_head_string_list = []
    IsKey = False
    for s in head_string:
        if IsKey == False: 
            if s == '{': IsKey = True
        else: 
            if s == '{' or s == '\\' or s == '}':
                continue   
        new_head_string_list.append(s)
    new_head_string = ''.join(new_head_string_list)
    bib_string_list[0] = new_head_string
    bib_string = '\n'.join(bib_string_list)
    return bib_string


def update_arxiv_version(bib_data): 
    """
    Obtain the latest doi information for the arxiv paper.
    """
    for key, entry in bib_data.entries.items():
        if 'journal' in entry.fields._dict.keys() and entry.fields['journal'].startswith('arXiv preprint arXiv'): 
            arxid = extract_from_text(entry.fields['journal'])[0]
            arx_ref = arxb(arxid)
            arx_ref = clean_key(arx_ref)
            new_bib = parse_string(arx_ref, 'bibtex')
            new_entry = new_bib.entries[list(new_bib.entries.keys())[0]]  
            if 'journal' in new_entry.fields._dict.keys() and new_entry.fields['journal'].startswith('arXiv preprint arXiv'): 
                print('[grey69]  keep : arXiv {}[/grey69]'.format(arxid))
            else: 
                bib_data.entries[key] = new_entry  
                print('[bold magenta]upgrade[/bold magenta]: arXiv {} ==> {}'.format(arxid, new_entry.fields['journal']))
    
    return bib_data

def remove_abstract_information(bib_data):
    """
    remove abstract information in bib field.
    """
    for key, entry in bib_data.entries.items():
        if 'abstract' in entry.fields._dict.keys(): 
            entry.fields.pop('abstract')

    return bib_data


def convert_bibtex_keys(input_file: str, output_file: str):
    """
    Convert keys in a bibtex file to Google Scholar format.
    @input_file: string, input file name.
    @output_file: string, output file name.
    """
    bib_data = parse_file(input_file)
    bib_data = update_arxiv_version(bib_data)
    bib_data = remove_abstract_information(bib_data)
    with open(output_file, 'w', encoding='utf-8') as ofile:
        bib_data.to_file(ofile)

def main(): 
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', type=str, default='')
    parser.add_argument('output_file', type=str, nargs='?', default='')
    args = parser.parse_args()
    if args.output_file: 
        convert_bibtex_keys(args.input_file, args.output_file)
    else: 
        outfile = args.input_file
        outfile = outfile.split(".")
        outfile[-2] = outfile[-2] + "_out"
        outfile[-1] = "bib"
        outfile = ".".join(outfile)
        convert_bibtex_keys(args.input_file, outfile)

if __name__ == '__main__':
    # update the bib file with latest doi information
    main()

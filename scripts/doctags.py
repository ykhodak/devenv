import os
import sys
import glob
import re

class bclr:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'



def process_doc_files(tag_search):
    docs_dir = os.environ.get("DOCSHOME")
    gs = '{}/*.txt'.format(docs_dir)
    tag_pattern=r"^\S*\:$"
    snipet_pattern=r"\s*"
    for name in glob.glob(gs):
        filename, _ = os.path.splitext(os.path.basename(name))
        tag_header = ''
        with open(name, 'r') as f:
            for ln in f:
                if tag_header:
                    if re.search(snipet_pattern, ln):
                        ln = ln.strip()
                        if len(ln) > 0:
                            print(' {}'.format(ln))
                        else:
                            tag_header = ''
                else:
                    ln = ln.strip()
                    if re.search(tag_pattern, ln):
                        ln = ln[:-1]
                        all_found = True
                        for t in tag_search:
                            if ln.lower().find(t.lower()) == -1:
                                all_found = False
                                break
                        if all_found:
                            tag_header = '[{}]{}'.format(filename, ln)
                            print('{}{}{}' .format(bclr.OKCYAN, tag_header,bclr.ENDC))
    



if __name__ == '__main__':
    tag_search = []
    arg_num = len(sys.argv)
    if arg_num > 1:
        i=1
        while i < arg_num:
            v = sys.argv[i]
            tag_search.append(v)
            i += 1
    process_doc_files(tag_search)

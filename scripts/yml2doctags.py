import glob
import yaml
import os
import sys

class TagLine:
    def __init__(self, fileName, tag, note):
        self.fileName = fileName
        self.tag = tag
        self.note = note

class TagsDb:    
    file_col_width = 1
    tag_col_width = 1

    def __init__(self):
        self.docdir = None
        self.lines = []

    def collect_tags(self, tag_search):
        gsearch = '*.yml'
        if self.docdir is not None:
            gsearch = '{}/*.yml'.format(self.docdir)

        for name in glob.glob(gsearch):
            with open(name, 'r') as f:                
                y = yaml.safe_load(f)
                if y is not None:
                    base_name = os.path.splitext (name) [0]
                    base_name = os.path.basename(base_name)
                    for k in y.keys():
                        filter_in_line = True
                        if len(tag_search) > 0:
                            filter_in_line = True
                            for s in tag_search:
                                if k.find(s) == -1:
                                    filter_in_line = False
                                    break
                        if filter_in_line:
                            v = y[k]
                            if isinstance(v, list):
                                for i in v:
                                    t = TagLine (base_name, k, i)
                                    self.lines.append (t)
                            else:
                                t = TagLine(base_name, k, v)
                                self.lines.append (t)

    def calc_col_width(self) :
        self.file_col_width = 1
        self.tag_col_width = 1
        for t in self.lines:
            fname_len = len(t.fileName)
            tag_len = len(t.tag)
            if fname_len > self.file_col_width:
                self.file_col_width = fname_len
            if tag_len > self.tag_col_width:
                self.tag_col_width = tag_len

    def print_tags(self):
        for t in self.lines:
            name_str = '>{}'. format (t. fileName) .ljust (self.file_col_width+2)
            tag_str = '[{}]'.format(t.tag) .ljust (self.tag_col_width + 4)
            print ('{}{}{}'.format(name_str, tag_str, t.note))
    

if __name__ == '__main__':
    tag_search = []
    arg_num = len(sys.argv)
    tdb = TagsDb()
    if arg_num > 1:
        docdir = False
        i=1
        while i < arg_num:
            v = sys.argv[i]
            if v == '-w':
                docdir = True
            else:                
                if docdir:
                    docdir = False
                    tdb.docdir = v
                else:
                    tag_search.append(v)

            i += 1

    tdb.collect_tags(tag_search)
    tdb.calc_col_width()
    tdb.print_tags()

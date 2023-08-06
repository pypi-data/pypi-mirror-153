
import xmltodict
from pathlib import PurePath
import os
from time import sleep
import fcntl

class BaseName:
    def __init__(self, name="fast_dp"):
        self.name = name
        self.xml_pattern = ''.join([name,'.xml'])
        self.txt_pattern = ''.join([name,'.summary.txt'])
        self.csv_pattern = ''.join([name,'.summary.csv'])

def scan_directory(dirpath,
                   dirs_to_avoid=["dozor"],
                   sort_dirs=True,
                   filepatterns=["fast_dp.xml","autoPROC.xml"]):
    path_dict = {}
    for (dirpath,dirnames,filenames) in os.walk(dirpath,topdown=True):
        dirnames[:] = [d for d in dirnames if d not in dirs_to_avoid]
        for f in filenames:
            if f in filepatterns:
                path_dict[f"{os.path.join(dirpath,f)}"] = os.path.getmtime(os.path.join(dirpath,f))
    return path_dict

class DataDirectory:
    def __init__(self,dirpath,basename=None):
        self._basename = basename
        self._dirpath = dirpath
        self._observer_list = []
        self._path_dict = {}

    def attach(self,observer):
        self._observer_list.append(observer)
    
    def notify(self,path_set):
        [observer.update(path_set) for observer in self._observer_list]

    def check_directory(self):
        path_dict = scan_directory(
                        self._dirpath,
                        filepatterns=self._basename.xml_pattern)
        path_set_to_send = set([])
        for pd in path_dict:
            #check for new file
            if pd in self._path_dict:
                #check for update to file
                if path_dict[pd] - self._path_dict[pd] > 0:
                    path_set_to_send.add(pd)
            else:
                path_set_to_send.add(pd)

        if path_set_to_send:
            self.notify(sorted(path_set_to_send,key=os.path.getmtime))
        self._path_dict = path_dict

class FileObserver:
    def __init__(self,basename=None):
        self._basename = basename
        self._results = ''.join([make_header(),'\n'])
    def update(self, paths):
        new_results = '\n'.join([format_results_string(parse_fdp_xml(fp))
                                 for fp in paths if parse_fdp_xml(fp)])
        new_results = ''.join([new_results,'\n'])
        self._results = ''.join([self._results,new_results])
        with open(self._basename.txt_pattern,'w') as f:
            fcntl.flock(f,fcntl.LOCK_SH)
            f.write(self._results)

class DisplayObserver:
    def __init__(self):
        print(make_header())
    
    def update(self, paths): #display results in order files created
        [print(format_results_string(parse_fdp_xml(f))) for f in paths
         if parse_fdp_xml(f)]

def make_header():
    first_row = ''.join([f"{'':34}",
                         f'{"|---------------Overall------------------|":^14}',
                         f'{"|-------------Outer-Shell----------------|":^14}\n',])
    formatted_string=''.join([f'{"Sample Path":>34}',
                              f'{"Hi":>7}',
                              f'{"Lo":>7}',
                              f'{"R_mrg":>7}',
                              f'{"cc12":>7}',
                              f'{"comp":>7}',
                              f'{"mult":>7}',
                              f'{"Hi":>7}',
                              f'{"Lo":>7}',
                              f'{"R_mrg":>7}',
                              f'{"cc12":>7}',
                              f'{"comp":>7}',
                              f'{"mult":>7}',
                              f'{"symm":>12}',
                              f'{"a":>7}',
                              f'{"b":>7}',
                              f'{"c":>7}',
                              f'{"alpha":>7}',
                              f'{"beta":>7}',
                              f'{"gamma":>7}'])
    return ''.join([first_row,formatted_string])

def parse_fdp_xml(filename):

    with open(filename) as f:
        fdp_xml = xmltodict.parse(f.read())

    #sometimes there are multiple program attachment entries
    try:
        path=fdp_xml["AutoProcContainer"]\
                    ["AutoProcProgramContainer"]\
                    ["AutoProcProgramAttachment"]\
                    ["filePath"]
    except TypeError:
        path=fdp_xml["AutoProcContainer"]\
                    ["AutoProcProgramContainer"]\
                    ["AutoProcProgramAttachment"][0]\
                    ["filePath"] 

    path_parts = PurePath(path).parts
    sample_name_path = '/'.join([path_parts[-4],path_parts[-3]])
   
    try:
        #all resolution shells
        overall = fdp_xml["AutoProcContainer"]\
                         ["AutoProcScalingContainer"]\
                         ["AutoProcScalingStatistics"][0]
        #pertinent values for table                 
        res_lim_low_overall = float(overall["resolutionLimitLow"])
        res_lim_high_overall = float(overall["resolutionLimitHigh"])
        r_merge_overall = float(overall["rMerge"])
        cc_half_overall = float(overall["ccHalf"])
        comp_overall = float(overall["completeness"])
        mult_overall = float(overall["multiplicity"])
       
        #outer resolution shell
        outer = fdp_xml["AutoProcContainer"]\
                       ["AutoProcScalingContainer"]\
                       ["AutoProcScalingStatistics"][2]
        #pertinent values for table                 
        res_lim_low_outer = float(outer["resolutionLimitLow"])
        res_lim_high_outer = float(outer["resolutionLimitHigh"])
        r_merge_outer = float(outer["rMerge"])
        cc_half_outer = float(outer["ccHalf"])
        comp_outer = float(outer["completeness"])
        mult_outer = float(outer["multiplicity"])
        
        #symmetry info
        cell = fdp_xml["AutoProcContainer"]["AutoProc"]
        space_group = cell["spaceGroup"]
        a = float(cell["refinedCell_a"])
        b = float(cell["refinedCell_b"])
        c = float(cell["refinedCell_c"])
        alpha = float(cell["refinedCell_alpha"])
        beta = float(cell["refinedCell_beta"])
        gamma = float(cell["refinedCell_gamma"])

        return (sample_name_path,
                res_lim_high_overall,
                res_lim_low_overall,
                r_merge_overall,
                cc_half_overall,
                comp_overall,
                mult_overall,
                res_lim_high_outer,
                res_lim_low_outer,
                r_merge_outer,
                cc_half_outer,
                comp_outer,
                mult_outer,
                space_group,
                a,
                b,
                c,
                alpha,
                beta,
                gamma)

    except KeyError:
        return ''

def format_results_string(*args):
    result_string = args[0]
    try:
        formatted_string=''.join([f'{result_string[0]:>34}',#sample path
                                  f'{result_string[1]:7.2f}',#high res cut overall
                                  f'{result_string[2]:7.2f}',#low res cut overall
                                  f'{result_string[3]:7.3f}',#R_merge overall
                                  f'{result_string[4]:7.2f}',#cc12 overall
                                  f'{result_string[5]:7.2f}',#completeness overall
                                  f'{result_string[6]:7.2f}',#multiplicity overall
                                  f'{result_string[7]:7.2f}',#high res cut outer
                                  f'{result_string[8]:7.2f}',#low res cut outer
                                  f'{result_string[9]:7.3f}',#R_merge outer
                                  f'{result_string[10]:7.2f}',#cc12 outer
                                  f'{result_string[11]:7.2f}',#completeness outer
                                  f'{result_string[12]:7.2f}',#multiplicity outer
                                  f'{result_string[13]:>12}',#space group
                                  f'{result_string[14]:7.1f}',#a
                                  f'{result_string[15]:7.1f}',#b
                                  f'{result_string[16]:7.1f}',#c
                                  f'{result_string[17]:7.1f}',#alpha
                                  f'{result_string[18]:7.1f}',#beta
                                  f'{result_string[19]:7.1f}'])#gamma
        return formatted_string
    except IndexError:
        return result_string


if __name__ == "__main__":
    test_dir = os.getcwd()
    try:
        if os.path.basename(test_dir) == "fast_dp_dir":
            mx_directory = PurePath(test_dir).parent
            print(mx_directory)
            d = DataDirectory(mx_directory)
            dobs = DisplayObserver()
            fobs = FileObserver()
            d.attach(dobs)
            d.attach(fobs)
            while True:
                d.check_directory()
                sleep(10)
        else:
            print("summarytable must be launched from fast_dp_dir...")
    except KeyboardInterrupt:
        print("\nExiting gracefully...")


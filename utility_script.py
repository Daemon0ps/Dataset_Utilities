from MenuModules import *

@dataclass
class MS:
    def __init__(self):
        self = self
        self.src_path = CFG.src_path
        self.dest_path = CFG.dest_path
        self.bool_padding = CFG.bool_padding
        self.bool_resize_only = CFG.bool_resize_only
        self.bool_sequential_rename = CFG.bool_sequential_rename
        self.bool_transpose_images = CFG.bool_transpose_images
        self.bool_no_text_copy = CFG.bool_no_text_copy
        self.add_text_src = CFG.add_text_src
        self.add_text_data_front = CFG.add_text_data_front
        self.add_text_data_back = CFG.add_text_data_back
        self.append_sequence = CFG.append_sequence
        self.replace_text_src = CFG.replace_text_src
        self.text_data_replace = CFG.text_data_replace
        self.text_data_replacement = CFG.text_data_replacement
        self.replace_list = CFG.replace_list
        self.resize_w = CFG.resize_w
        self.resize_h = CFG.resize_h
        self.resize_src = CFG.resize_src
        self.resize_dest = CFG.resize_dest
        self.replace_text_file = CFG.replace_text_file
        self.img_files = CFG.img_files
        self.txt_types = CFG.txt_types

    @staticmethod
    def TagTable():

        while True:
            ms = ""
            mi_00 = "---Tags---"
            mi_00_c = "Current Page:"
            mi_01 = "Edit"
            mi_02 = "Delete"
            mi_03 = "Go To Page"
            mi_04 = "Next Page"
            mi_05 = "Previous Page"
            mi_06 = "Change List"
            mi_07 = "Apply Change List"
            mi_08 = "Re-Load Table and DELETE Changes"
            mi_000 = "Exit Program"
            os.system('cls' if os.name == 'nt' else 'clear')
            ms = str(f"{cp_y('*************************************************')}{cp_b(chr(10))}")
            ms = str(f"{cp_m('==========')}{cp_g(mi_00)}{cp_m('==========')}{cp_b(chr(10))}")
            ms = str(f"{cp_lr('[')}{cp_y('-- ')}{cp_c(mi_00_c)}:{cp_w(CFG.tag_page)}{cp_r(' of ')}{cp_w(len(CFG.tag_array_split))}{cp_y(' --')}{cp_lr(']')}{cp_b(chr(10))}")
            for i in range(0,len(CFG.tag_array_split[CFG.tag_page])-1):
                ms = str(f"{cp_g('(')}{cp_y(i)}{cp_g(')')} {cp_c(str(CFG.tag_array_split[CFG.tag_page][i]))}")
                if str(CFG.tag_array_split[CFG.tag_page][i]) in [x[0] for x in CFG.tag_table_change]:
                    tbl_chg = change_table_iter(CFG.tag_table_change,CFG.tag_array_split[CFG.tag_page][i])
                    ms = str(f"{cp_r(' - ')}{cp_ly(tbl_chg[2])}{cp_r(' - ')}{cp_lr(tbl_chg[1])}")
                    ms =  str(f"{cp_b(chr(10))}")
                else:
                    ms =  str(f"{cp_b(chr(10))}")
            ms = str(f"{cp_r('(')}{cp_w('E')}{cp_r(')')} {cp_g(mi_01)}{cp_b(chr(10))}")
            ms = str(f"{cp_r('(')}{cp_w('D')}{cp_r(')')} {cp_g(mi_02)}{cp_b(chr(10))}")
            ms = str(f"{cp_r('(')}{cp_w('G')}{cp_r(')')} {cp_g(mi_03)}{cp_b(chr(10))}")
            ms = str(f"{cp_r('(')}{cp_w('N')}{cp_r(')')} {cp_g(mi_04)}{cp_b(chr(10))}")
            if CFG.tag_page>0:
                ms = str(f"{cp_r('(')}{cp_w('P')}{cp_r(')')} {cp_g(mi_05)}{cp_b(chr(10))}")
            ms = str(f"{cp_r('(')}{cp_w('R')}{cp_r(')')} {cp_g(mi_06)}{cp_b(chr(10))}")
            ms = str(f"{cp_r('(')}{cp_w('A')}{cp_r(')')} {cp_g(mi_07)}{cp_b(chr(10))}")
            ms = str(f"{cp_r('(')}{cp_w('L')}{cp_r(')')} {cp_g(mi_08)}{cp_b(chr(10))}")
            ms = str(f"{cp_r('(')}{cp_w('0')}{cp_r(')')} {cp_g(mi_000)}{cp_b(chr(10))}")
            ms = str(f"{cp_y('*************************************************')}{cp_b(chr(10))}")
            ms = ms + str(f"{cp_b('Enter Option:')}")
            Menu_Input = unidecode(input("").strip().lower())
            if Menu_Input == "e":
                ms = (str(f"{cp_lf()}{chr(10)}{cp_y('EDIT Tag No:')}{cp_w(' ')}"))
                Menu_Input  = unidecode(input().strip())
                if Menu_Input is not None and int(Menu_Input) in [i for i in range(0,len(CFG.tag_array_split[CFG.tag_page])-1)]:
                    tag_no = int(Menu_Input)
                    ms = str(f"{cp_lf()}{cp_w(str(CFG.tag_array_split[CFG.tag_page][int(Menu_Input)]))}")
                    ms = (str(f"{cp_lf()}{chr(10)}{cp_y('Replacement: ')}{cp_w('')}"))
                    Menu_Input = unidecode(input().strip().lower())
                    if Menu_Input is not None and len(str(Menu_Input))>0:
                        CFG.tag_table_change.append([CFG.tag_array_split[CFG.tag_page][int(tag_no)],str(Menu_Input),"E"])
            if Menu_Input == "d":
                ms = (str(f"{cp_lf()}{chr(10)}{cp_y('DELETE Tag No:')}{cp_w(' ')}"))
                Menu_Input  = unidecode(input().strip())
                if Menu_Input is not None and int(Menu_Input) in [i for i in range(0,len(CFG.tag_array_split[CFG.tag_page])-1)]:
                    tag_no = int(Menu_Input)
                    ms = str(f"{cp_lf()}{cp_w(str(CFG.tag_array_split[CFG.tag_page][int(Menu_Input)]))}")
                    CFG.tag_table_change.append([CFG.tag_array_split[CFG.tag_page][int(tag_no)],"","D"])
            elif Menu_Input == "n":
                CFG.tag_page = CFG.tag_page + 1
            elif Menu_Input == "p":
                CFG.tag_page = CFG.tag_page - 1
            elif Menu_Input == "g":
                ms = (str(f"{cp_lf()}{chr(10)}{cp_y('Tag No:')}{cp_w('')}"))
                Menu_Input  = unidecode(input().strip())                
                if int(Menu_Input) in [i for i in range(0,len(CFG.tag_array_split)-1)]:
                    CFG.tag_page = int(Menu_Input)
            elif Menu_Input == "a":
                ms = str(f"{chr(10)}{cp_b('Please ')}{cp_w('CONFIRM')}{cp_b(':   ')}")
                ms =  (str(f"{chr(10)}{cp_b('(')}{cp_w('Y')}{cp_b(')')} {cp_w(' - YES ?  ')} {cp_b('(')}{cp_w('N')}{cp_b(')')} {cp_w(' - NO?')}"))
                Menu_Input = input("").strip() 
                if Menu_Input == "Y":
                    ApplyChanges()
            elif Menu_Input == "l":
                ms = str(f"{chr(10)}{cp_b('Please ')}{cp_w('CONFIRM')}{cp_b(':   ')}")
                ms =  (str(f"{chr(10)}{cp_b('(')}{cp_w('Y')}{cp_b(')')} {cp_w(' - YES ?  ')} {cp_b('(')}{cp_w('N')}{cp_b(')')} {cp_w(' - NO?')}"))
                Menu_Input = input("").strip() 
                if Menu_Input == "Y":
                    all_keywords()
                
            # elif Menu_Input == "A":
            #     ms = str(f"{chr(10)}{cp_b('Please ')}{cp_w('CONFIRM')}{cp_b(':   ')}")
            #     ms =  (str(f"{chr(10)}{cp_b('(')}{cp_w('Y')}{cp_b(')')} {cp_w(' - YES ?  ')} {cp_b('(')}{cp_w('N')}{cp_b(')')} {cp_w(' - NO?')}"))
            #     Menu_Input = input("").strip() 
            #     if Menu_Input == "Y":
            #         ApplyChanges()
            #     else:
            #         continue
            # elif Menu_Input == "7":
            #     kw_split = []
            #     ms = str(f"{chr(10)}{cp_y('Enter comma separated keywords(eg: key,word,list,sep )')}{cp_b(': ')}")
            #     ms = str(f"{chr(10)}")
            #     kw_split = input("").lower().strip().split(",")
            #     if kw_split is not None and len(kw_split)>0:
            #         for x in CFG.txt_kw:
            #             ms = str(f"{cp_y(x)}{cp_b(': ')}")
            #             CFG.txt_kw.append(str(x).strip().lower())
            #         ms = str(f"{chr(10)}{cp_b('Please ')}{cp_w('CONFIRM')}{cp_b(':   ')}")
            #         ms =  (str(f"{chr(10)}{cp_b('(')}{cp_w('Y')}{cp_b(')')} {cp_w(' - YES ?  ')} {cp_b('(')}{cp_w('N')}{cp_b(')')} {cp_w(' - NO?')}"))
            #         Menu_Input = input("").strip() 
            #         if Menu_Input == "Y":
            #             kw_move()
            #     else:
            #         continue
            if Menu_Input == "0":
                return
            elif Menu_Input not in ["0","1","2","3","4","5","6","0"]:
# ["0","1","2","3","4","5","6","7","8","9","0"]:
                continue

    @staticmethod
    def MainMenu():
        # (1)Text/Tag Utilities
        # (2)Image Utilities
        # (3)Tag Generation Utilities
        # (4)File Utilities
        # (5)Checkpoint Utilities
        # (6)Kohya_SS Training Module
        # (7)...
        # (8)...
        # (0)Exit Program
        ms=""
        mi_1 = "Text/Tag Utilities"
        mi_2 = "Image Utilities"
        mi_3 = "Tag Table"
        mi_4 = "File Utilities"
        mi_5 = "Checkpoint Utilities"
        mi_6 = "Kohya_SS Training Module"
        mi_7 = "..."
        mi_8 = "..."
        mi_000 = "Exit Program"
        ProgramBreak = False
        while ProgramBreak is False:
            os.system('cls' if os.name == 'nt' else 'clear')
            ms = str(f"{cp_y('*************************************************')}{cp_b(chr(10))}")
            ms = str(f"{cp_r('(')}{cp_w('1')}{cp_r(')')} {cp_g(mi_1)}{cp_b(chr(10))}")
            ms = str(f"{cp_r('(')}{cp_w('2')}{cp_r(')')} {cp_g(mi_2)}{cp_b(chr(10))}")
            ms = str(f"{cp_r('(')}{cp_w('3')}{cp_r(')')} {cp_g(mi_3)}{cp_b(chr(10))}")
            ms = str(f"{cp_r('(')}{cp_w('4')}{cp_r(')')} {cp_g(mi_4)}{cp_b(chr(10))}")
            ms = str(f"{cp_r('(')}{cp_w('5')}{cp_r(')')} {cp_g(mi_5)}{cp_b(chr(10))}")
            ms = str(f"{cp_r('(')}{cp_w('6')}{cp_r(')')} {cp_g(mi_6)}{cp_b(chr(10))}")
            ms = str(f"{cp_r('(')}{cp_w('7')}{cp_r(')')} {cp_g(mi_7)}{cp_b(chr(10))}")
            ms = str(f"{cp_r('(')}{cp_w('8')}{cp_r(')')} {cp_g(mi_8)}{cp_b(chr(10))}")
            ms = str(f"{cp_r('(')}{cp_w('0')}{cp_r(')')} {cp_g(mi_000)}{cp_b(chr(10))}")
            ms = str(f"{cp_y('*************************************************')}{cp_b(chr(10))}")
            ms = str(f"{cp_b('Enter Option:')}")

            Menu_Input = input("")
            if Menu_Input == "1":
                MS.TextFileUtilities()
            if Menu_Input == "2":
                cp_dg("MS.ImageUtilities")
            if Menu_Input == "3":
                cp_dg("MS.TagGeneration")
            if Menu_Input == "4":
                cp_dg("MS.FileUtilities")
            if Menu_Input == "5":
                cp_dg("MS.CheckpointUtilities")
            if Menu_Input == "6":
                cp_dg("MS.Kohya_SS")
            if Menu_Input == "0":
                sys.exit()
            ProgramBreak = False

    @staticmethod
    def TextFileUtilities():
        while True:
            ms = ""
            mi_00 = "---Tags/Keywords Utilities---"
            mi_00_c = "Current Paths:"
            mi_00_s = "Source Path: "
            mi_00_d = "Destination Path: "
            mi_01 = "Change Path"
            mi_02 = "Prepend/Append to all Tag Files"
            mi_03 = "Generate Keyword List"
            mi_04 = "Tags Table - Replace/Edit"
            mi_05 = "De-Duplicate Keywords & Sort"
            mi_06 = "Copy/Move by Keywords"
            mi_000 = "Exit Program"
            os.system('cls' if os.name == 'nt' else 'clear')
            ms = str(f"{cp_y('*************************************************')}{cp_b(chr(10))}")
            ms = str(f"{cp_m('==========')}{cp_g(mi_00)}{cp_m('==========')}{cp_b(chr(10))}")
            ms = str(f"{cp_lr('[')}{cp_y('-- ')}{cp_c(mi_00_c)}{cp_y(' --')}{cp_lr(']')}{cp_b(chr(10))}")
            ms = str(f"{cp_b('--->')}{cp_lg(mi_00_s)}{cp_w(CFG.src_path)}{cp_b(chr(10))}")
            ms = str(f"{cp_b('--->')}{cp_lg(mi_00_d)}{cp_w(CFG.dest_path)}{cp_b(chr(10))}")
            ms = str(f"{cp_r('(')}{cp_w('1')}{cp_r(')')} {cp_g(mi_01)}{cp_b(chr(10))}")
            ms = str(f"{cp_r('(')}{cp_w('2')}{cp_r(')')} {cp_g(mi_02)}{cp_b(chr(10))}")
            ms = str(f"{cp_r('(')}{cp_w('3')}{cp_r(')')} {cp_g(mi_03)}{cp_b(chr(10))}")
            ms = str(f"{cp_r('(')}{cp_w('4')}{cp_r(')')} {cp_g(mi_04)}{cp_b(chr(10))}")
            ms = str(f"{cp_r('(')}{cp_w('5')}{cp_r(')')} {cp_g(mi_05)}{cp_b(chr(10))}")
            ms = str(f"{cp_r('(')}{cp_w('6')}{cp_r(')')} {cp_g(mi_06)}{cp_b(chr(10))}")
            ms = str(f"{cp_r('(')}{cp_w('0')}{cp_r(')')} {cp_g(mi_000)}{cp_b(chr(10))}")
            ms = str(f"{cp_y('*************************************************')}{cp_b(chr(10))}")
            ms = ms + str(f"{cp_b('Enter Option:')}")
            Menu_Input = input("").strip()
            if Menu_Input == "1":
                ms =  (str(f"{chr(10)}{cp_b('(')}{cp_w('1')}{cp_b(')')} {cp_w(' - Source ?  ')} {cp_b('(')}{cp_w('2')}{cp_b(')')} {cp_w(' - Destination?')}"))
                ms =  (str(f"{cp_lf()}{chr(10)}{cp_y('Path Choice:')}{cp_w('')}"))
                Menu_Input  = input().strip()
                if Menu_Input == "1":
                    ms = str(f"{chr(10)}{cp_y('Enter ')}{cp_b('Source')}{cp_y(' Path:  ')}{cp_w('')}")
                    CFG.src_path  = input().strip()
                    CFG.src_path = CFG.src_path.replace('\\','/')
                    if right(CFG.src_path,1) != "/":
                        CFG.src_path = CFG.src_path+"/"                        
                    if not os.path.isdir(left(CFG.src_path,len(CFG.src_path)-1)):
                        CFG.dest_path = CFG.dest_path + str(f"{chr(10)}{cp_ow('')}{cp_r('Please enter a valid path')}{cp_ow(chr(10))}{cp_ow(chr(10))}")
                        CFG.dest_path = CFG.dest_path + str(f"{print(chr(10))}")
                        CFG.dest_path = ""
                        CFG.dest_path = "None"
                if Menu_Input == "2":
                    ms = str(f"{chr(10)}{cp_y('Enter ')}{cp_b('Destination')}{cp_y(' Path:  ')}{cp_w('')}")
                    CFG.dest_path  = input().strip()
                    CFG.dest_path = CFG.dest_path.replace('\\','/')
                    if right(CFG.dest_path,1) != "/":
                        CFG.dest_path = CFG.dest_path+"/"                        
                    if not os.path.isdir(left(CFG.dest_path,len(CFG.dest_path)-1)):
                        CFG.dest_path = CFG.dest_path + str(f"{chr(10)}{cp_ow('')}{cp_r('Please enter a valid path')}{cp_ow(chr(10))}{cp_ow(chr(10))}")
                        CFG.dest_path = CFG.dest_path + str(f"{print(chr(10))}")
                        CFG.dest_path = ""
                        CFG.dest_path = "None"
            elif Menu_Input == "2":
                CFG.add_text_data_front = ""
                CFG.add_text_data_back = ""
                ms = str(f"{chr(10)}{cp_b('(')}{cp_w('1')}{cp_b(')')} {cp_y('Front ? / ')} \
                    {cp_b('(')}{cp_w('2')}{cp_b(')')} {cp_y('Back ? / ')} \
                        {cp_b('(')}{cp_w('3')}{cp_b(')')} {cp_y(' Both?')}{chr(10)}")
                Menu_Input = input("").strip()
                if Menu_Input == "1":
                    ms = str(f"{chr(10)}{cp_b('Enter Data to append to ')}{cp_w('Front')}{cp_b(': ')}")
                    CFG.add_text_data_front  = input().strip()
                    text_add(CFG.add_text_data_front,CFG.add_text_data_back)
                elif Menu_Input == "1":
                    ms = str(f"{chr(10)}{cp_b('Enter Data to append to ')}{cp_w('Back')}{cp_b(': ')}")
                    CFG.add_text_data_back  = input().strip()
                    text_add(CFG.add_text_data_front,CFG.add_text_data_back)
                elif Menu_Input == "3":
                        ms = str(f"{chr(10)}{cp_b('Enter Data to Prepend to ')}{cp_w('Front')}{cp_b(': ')}")
                        CFG.add_text_data_front  = input().strip()
                        ms = str(f"{chr(10)}{cp_b('Enter Data to Append to ')}{cp_w('Back')}{cp_b(': ')}")
                        CFG.add_text_data_back  = input().strip()
                        text_add(CFG.add_text_data_front,CFG.add_text_data_back)
            elif Menu_Input == "3":
                ms = str(f"{chr(10)}{cp_b('Please ')}{cp_w('CONFIRM')}{cp_b(':   ')}")
                ms =  (str(f"{chr(10)}{cp_b('(')}{cp_w('Y')}{cp_b(')')} {cp_w(' - YES ?  ')} {cp_b('(')}{cp_w('N')}{cp_b(')')} {cp_w(' - NO?')}"))
                Menu_Input = input("").strip()
                if Menu_Input == "Y":
                    CFG.kw_save_bool = True
                    all_keywords()
                else:
                    continue
            elif Menu_Input == "4":
                CFG.kw_save_bool = False
                all_keywords()
                MS.TagTable()
            elif Menu_Input == "5":
                ms = str(f"{chr(10)}{cp_b('Please ')}{cp_w('CONFIRM')}{cp_b(':   ')}")
                ms =  (str(f"{chr(10)}{cp_b('(')}{cp_w('Y')}{cp_b(')')} {cp_w(' - YES ?  ')} {cp_b('(')}{cp_w('N')}{cp_b(')')} {cp_w(' - NO?')}"))
                Menu_Input = input("").strip() 
                if Menu_Input == "Y":
                    tag_dedup()
                else:
                    continue
            elif Menu_Input == "6":
                kw_split = []
                ms = str(f"{chr(10)}{cp_y('Enter comma separated keywords(eg: key,word,list,sep )')}{cp_b(': ')}")
                ms = str(f"{chr(10)}")
                kw_split = input("").lower().strip().split(",")
                if kw_split is not None and len(kw_split)>0:
                    for x in kw_split:
                        ms = str(f"{cp_y(x)}{cp_b(': ')}")
                        CFG.move_kw.append(str(x).strip().lower())
                    ms =  (str(f"{chr(10)}{cp_b('(')}{cp_w('1')}{cp_b(')')} {cp_w(' - COPY ?  ')} {cp_b('(')}{cp_w('2')}{cp_b(')')} {cp_w(' - MOVE?')}"))
                    ms =  (str(f"{cp_lf()}{chr(10)}{cp_y('Path Choice:')}{cp_w('')}"))
                    Menu_Input  = input().strip()
                    ms = str(f"{chr(10)}{cp_b('Please ')}{cp_w('CONFIRM')}{cp_b(':   ')}")
                    ms =  (str(f"{chr(10)}{cp_b('(')}{cp_w('Y')}{cp_b(')')} {cp_w(' - YES ?  ')} {cp_b('(')}{cp_w('N')}{cp_b(')')} {cp_w(' - NO?')}"))
                    Menu_Input = input("").strip() 
                    if Menu_Input == "Y":
                        kw_move()
                else:
                    continue
            elif Menu_Input == "0":
                return
            elif Menu_Input not in ["0","1","2","3","4","5","6"]:
# ["0","1","2","3","4","5","6","7","8","9","0"]:
                continue


    
MS.MainMenu()


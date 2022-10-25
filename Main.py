from sys import argv
import os

File = open(argv[1], "r")

Functions = {}
Varibles = {}
Modules = {}
Data = {}
Dims = {}

def Run(FileContent, Args):
    InFileSystemCreation = False
    HaveToExecute = False
    InLineComment = False
    InCondition = False
    InTerminal = False
    InFunction = False
    TempCondition = []
    InComment = False
    LastPath = "None"
    InModule = False
    InPython = False
    InTests = False
    InPrint = False
    InError = False
    InFile = False
    Shortcuts = {}
    InLoop = False
    LoopLong = 000
    InWarn = False
    TempLoop = []
    InLog = False
    LogLine = 1
    Cursor = ""
    for Line in FileContent:
        Line = Line.replace("    " , "").replace("\n" , "").replace("&Cursor", Cursor).replace("&Debug", f"Varibles : {Varibles} ; Shortcuts : {Shortcuts} ; Functions : {Functions} ; Modules : {Modules} ; Data : {Data} ;")
        if(InPython != False):
            if(Line.startswith("End Python")):
                InPython = False
            else:
                exec(Line)
        else:
            for Word in Line.split():
                if(InFunction == False):
                    if(Word[0] == "+"):
                        if(Word != "+"):
                            Line = Line.replace(Word, Args[int(Word.replace("+", ""))])
                        else:
                            Line = Line.replace(Word, str(Args))
                if(Word[0] == "$"):
                    if(Word != "$"):
                        if(Word[1:] in Varibles):
                            Line = Line.replace(Word, str(Varibles[Word[1:]]))
                        else:
                            Line = Line.replace(Word, "None")
                elif(Word[0:2] == "/$"):
                    if(Word != "/$"):
                        Line = Line.replace(Word, f"{eval(Word[2:])}")
                elif(Word[0:2] == "/*"):
                    if(Word != "/*"):
                        Line = Line.replace(Word, f"{exec(Word[2:])}")
                elif(Word[0:2] == "/#"):
                    if(Word != "/#"):
                        Line = Line.replace(Word, f"{open(Word[2:]).read()}")
                elif(Word == "/'"):
                    Line = Line.replace("/'{}'/".format(Line.split("/'")[1].split("'/")[0]),"")
            if(InComment != False):
                if(Line.startswith("'''")):
                    InComment = False
            elif(InFile != False):
                if(Line.startswith("End File")):
                    InFile = False
                else:
                    InFile.write(f"{Line}\n")
            elif(InFileSystemCreation == True):
                if(Line.startswith("End Folder")):
                    InFileSystemCreation = False
                else:
                    Line = Line.replace("&", LastPath)
                    os.mkdir(Line)
                    LastPath = Line
            elif(InTerminal == True):
                if(Line.startswith("End Terminal")):
                    InTerminal = False
                else:
                    os.system(Line)
            elif(InPrint == True):
                if(Line.startswith("End %")):
                    InPrint = False
                else:
                    print(Line)
            elif(InCondition == True):
                if(Line.startswith("End If")):
                    if(HaveToExecute == True):
                        Run(TempCondition , [])
                    InCondition = False
                    TempCondition = []
                else:
                    TempCondition.append(Line)
            elif(InLoop == True):
                if(Line.startswith("End Loop")):
                    InLoop = False
                    if(LoopLong == "Infinite"):
                        while True:
                            Run(TempLoop)
                    else:
                        for Loop in range(LoopLong):
                            Run(TempLoop)
                    TempLoop = []
                else:
                    TempLoop.append(Line)
            elif(InLog == True):
                if(Line.startswith("End Log")):
                    InLog = False
                else:
                    if(LogLine == 1):
                        try:
                            open(Data["LogFile"], "a").write(f"[Log] {Line}" + "\n")
                        except:
                            open("PYSLOG", "a").write(f"[Log] {Line}" + "\n")
                    else:
                        try:
                            open(Data["LogFile"], "a").write(f"| {Line}" + "\n")
                        except:
                            open("PYSLOG", "a").write(f"| {Line}" + "\n")
                    LogLine = LogLine + 1
            elif(InError == True):
                if(Line.startswith("End Error")):
                    InError = False
                else:
                    if(LogLine == 1):
                        try:
                            open(Data["LogFile"], "a").write(f"[Error] {Line}" + "\n")
                        except:
                            open("PYSLOG", "a").write(f"[Error] {Line}" + "\n")
                    else:
                        try:
                            open(Data["LogFile"], "a").write(f"| {Line}" + "\n")
                        except:
                            open("PYSLOG", "a").write(f"| {Line}" + "\n")
                    LogLine = LogLine + 1
            elif(InWarn == True):
                if(Line.startswith("End Warn")):
                    InWarn = False
                else:
                    if(LogLine == 1):
                        try:
                            open(Data["LogFile"], "a").write(f"[Warning] {Line}" + "\n")
                        except:
                            open("PYSLOG", "a").write(f"[Warning] {Line}" + "\n")
                    else:
                        try:
                            open(Data["LogFile"], "a").write(f"| {Line}" + "\n")
                        except:
                            open("PYSLOG", "a").write(f"| {Line}" + "\n")
                    LogLine = LogLine + 1
            else:
                if(InFunction != False):
                    if Line != f"End {InFunction}":
                        Functions[InFunction].append(Line)
                    else:
                        InFunction = False
                elif(InModule != False):
                    if Line != f"End {InModule}":
                        Modules[InModule].append(Line)
                    else:
                        InModule = False
                else:
                    if(Line.startswith("'")):
                        pass
                    elif(Line.startswith("Library")):
                        if(Line.split(" ")[1] == "Import"):
                            Run(open(Line[16:], "r"))
                        if(Line.split(" ")[1] == "Python"):
                            exec(f"import {Line.split(' ')[2]}")
                    elif(Line.startswith("Function")):
                        if(Line.split(" ")[1] == "def"):
                            Functions[Line.split(" ")[2]] = []
                            InFunction = Line.split(" ")[2]
                        else:
                            global Arguments 
                            if(" : " in Line):
                                Arguments = Line.split(" : ")[1]
                                Arguments = Arguments.split("|")
                            else:
                                Arguments = ""
                            Run(Functions[Line.split()[1]], Arguments)
                    elif(Line.startswith("Module")):
                        Modules[Line.split(" ")[1]] = []
                        InModule = Line.split(" ")[1]
                    elif(Line.startswith("Data")):
                        Data[Line.split(" : ")[0].replace("Data ", "")] = Line.split(" : ")[1]
                    elif(Line.startswith("Log")):
                        if(Line.split(" ")[1] != "Group"):
                            try:
                                open(Data["LogFile"], "a").write(f"[Log] {Line[4:]}" + "\n")
                            except:
                                open("PYSLOG", "a").write(f"[Log] {Line[4:]}" + "\n")
                        else:
                            LogLine = 1
                            InLog = True
                    elif(Line.startswith("Warn")):
                        if(Line.split(" ")[1] != "Group"):
                            try:
                                open(Data["LogFile"], "a").write(f"[Warning] {Line[5:]}" + "\n")
                            except:
                                open("PYSLOG", "a").write(f"[Warning] {Line[5:]}" + "\n")
                        else:
                            LogLine = 1
                            InWarn = True
                    elif(Line.startswith("Error")):
                        if(Line.split(" ")[1] != "Group"):
                            try:
                                open(Data["LogFile"], "a").write(f"[Error] {Line[6:]}" + "\n")
                            except:
                                open("PYSLOG", "a").write(f"[Error] {Line[6:]}" + "\n")
                        else:
                            LogLine = 1
                            InError = True
                    elif(Line.startswith("PythonFunction")):
                        exec(f"{Line[16:]}()")
                    elif(Line.startswith("%")):
                        if(Line == "%"):
                            InPrint = True
                        else:
                            print(Line[2:])
                    elif(Line.startswith("Debug")):
                        print(f"""
                            Varibles : {Varibles} ;
                            Shortcuts : {Shortcuts} ;
                            Functions : {Functions} ;
                            Modules : {Modules} ;
                            Data : {Data} ;
                        """)
                    elif(Line.startswith("Tests")):
                        if(Line.split(" ")[1] == "ON"):
                            InTests = True
                        elif(Line.split(" ")[1] == "OFF"):
                            InTests = False
                    elif(Line.startswith("Python")):
                        if(Line.split(" ")[1] == "Group"):
                            InPython = True
                        else:
                            exec(Line[8:])
                    elif(Line.startswith("'''")):
                        InComment = True
                    elif(Line.startswith("$")):
                        Varibles[Line.split()[1]] = eval(Line[2+len(Line.split()[1])+3:])
                    elif(Line.startswith("Input")):
                        Varibles[Line.split()[1]] = input(Line[7+len(Line.split()[1])+3:])
                    elif(Line.startswith("Cursor")):
                        Cursor = Varibles[Line.split()[1]]
                    elif(Line.startswith("File")):
                        if(Line.split()[1] == "Write"):
                            InFile = open(Line[12:], "a")
                        elif(Line.split()[1] == "Delete"):
                            os.remove(Line[12:])
                    elif(Line.startswith("Folder")):
                        if(Line.split()[1] == "Create"):
                            os.mkdir(Line[15:])
                        elif(Line.split()[1] == "Delete"):
                            os.rmdir(Line[12:])
                        elif(Line.split()[1] == "Group"):
                            PathNumber = 1
                            InFileSystemCreation = True
                    elif(Line.startswith("Terminal")):
                        if(Line.split()[1] == "Group"):
                            InTerminal = True
                        else:
                            os.system(Line[10:])
                    elif(Line.startswith("Loop")):
                        if(Line.split()[1] == "Infinite"):
                            LoopLong = "Infinite"
                        else:
                            LoopLong = int(Line.split()[1])
                        InLoop = True
                    elif(Line.startswith("If")):
                        if(eval(Line.replace("If ", ""))):
                            ConditionType = Line.replace("If ", "")
                            InCondition = True
                            TempCondition = []
                            HaveToExecute = True
                        else:
                            ConditionType = Line.replace("If ", "")
                            InCondition = True
                            TempCondition = []
                            HaveToExecute = False
                    elif(Line.startswith("@")):
                        if(Line[1:] in Modules):
                            Run(Modules[Line[1:]])
                    if(InTests == True):
                        if(Line != ""):
                            try:
                                Type = Data["TestsType"]
                            except:
                                print(f"[Tests] {Line} | Executed With No Errors !\n")
                            else:
                                if(Type == "Log"):
                                    try:
                                        open(Data["LogFile"], "a").write(f"[Tests] {Line} | Executed With No Errors !\n")
                                    except:
                                        open("PYSLOG", "a").write(f"[Tests] {Line} | Executed With No Errors !\n")
                                elif(Type == "Terminal"):
                                    print(f"[Tests] {Line} | Executed With No Errors !\n")

Run(File, ["","",""])
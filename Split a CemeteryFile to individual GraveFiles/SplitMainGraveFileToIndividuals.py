import os

# DEV paths
FileInPath = r"."
FileInName = r"SAMPLE Grave List.txt"
FileOutFldrName = "Generated files"

EntrySeperator = "===========================================DIV50==\n"
tempFileName = "trashFile"
pathSep = '\\'
FileOutExt = ".txt"
FileOutPath= FileInPath + pathSep + FileOutFldrName

fileIn = open(FileInPath + pathSep + FileInName, 'r', encoding='utf-8-sig')
prevFileOut = open(FileOutPath + pathSep + tempFileName + FileOutExt, 'w', encoding='utf-8-sig')
FileOut = prevFileOut

Line = fileIn.readline() 
while (Line != ""):
    # print (Line)
    if (Line == EntrySeperator):
        FileOut.write( EntrySeperator )
        Line = fileIn.readline() 
        # print (Line)
        # extract the plot ID for use in filename
        PID = Line[7:Line.find(' ', 8)]
        print (PID)
        FileOutName="plot " + PID
        if (Line == EntrySeperator):
            FileOutName = tempFileName
        prevFileOut.close()
        FileOut = open (FileOutPath + pathSep + FileOutName + FileOutExt, 'w', encoding='utf-8-sig')
        prevOutFile = FileOut
        FileOut.write(EntrySeperator)
    FileOut.write(Line)
    Line = fileIn.readline() 

fileIn.close()
FileOut.close() 
prevFileOut.close()
os.remove (FileOutPath + pathSep + tempFileName + FileOutExt)

input("Press Enter to continue.")

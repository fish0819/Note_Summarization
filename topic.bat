@ECHO OFF & SETLOCAL

SET RUN_DOTPY=python.exe TranslateNotes.py
SET PYTHON_PATH=C:\Python36

SET subject1=OM
SET chapters1=ch1 ch3 ch6 ch7 ch8 ch9 ch10 ch11 ch12 ch15 ch16 supplementA

SET subject2=DS
SET chapters2=ch2 ch3 ch4 ch5 ch6 ch78 ch9

for %%c in (%chapters1%) do python GetTopic.py %1 %subject1% %%c

for %%c in (%chapters2%) do python GetTopic.py %1 %subject2% %%c
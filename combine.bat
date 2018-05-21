@ECHO OFF & SETLOCAL

SET RUN_DOTPY=python.exe TranslateNotes.py
SET PYTHON_PATH=C:\Python36

SET subject1=OM
SET chapters1=ch1 ch3 ch6 ch7 ch8 ch9 ch10 ch11 ch12 ch15 ch16 supplementA
SET thres_cossim1=0.2

SET subject2=DS
SET chapters2=ch2 ch3 ch4 ch5 ch6 ch7 ch9
SET thres_cossim2=0.1

rem for %%c in (%chapters1%) do python CombineSlides.py %1 %subject1% %%c
rem for %%c in (%chapters2%) do python CombineSlides.py %1 %subject2% %%c

for %%c in (%chapters1%) do python CombineNotes.py %1 %subject1% %%c %thres_cossim1%
for %%c in (%chapters2%) do python CombineNotes.py %1 %subject2% %%c %thres_cossim2%
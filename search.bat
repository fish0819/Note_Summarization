@ECHO OFF & SETLOCAL ENABLEDELAYEDEXPANSION

SET PYTHON_PATH=C:\Python36

SET subject1=OM
SET chapters1=ch1 ch3 ch6 ch7 ch8 ch9 ch10 ch11 ch12 ch15 ch16 supplementA
SET thres_cossim1=0.2

SET subject2=DS
SET chapters2=ch2 ch3 ch4 ch5 ch6 ch7 ch9
SET thres_cossim2=0.1

SET thres_dissim=0.3

for %%c in (%chapters1%) do python SearchWebs.py %1 %subject1% %%c %thres_cossim1% %thres_dissim%
for %%c in (%chapters2%) do python SearchWebs.py %1 %subject2% %%c %thres_cossim2% %thres_dissim%

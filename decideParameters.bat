@ECHO OFF & SETLOCAL

SET RUN_DOTPY=python.exe TranslateNotes.py
SET PYTHON_PATH=C:\Python36

SET subject1=OM
SET chapters1=ch1 ch3 ch6 ch7 ch8 ch9 ch10 ch11 ch12 ch15 ch16 supplementA
SET threshold_cossim1=0.2

SET subject2=DS
SET chapters2=ch2 ch3 ch4 ch5 ch6 ch78 ch9
SET threshold_cossim2=0.1

for /R .\result\OM\ %%f in (*.csv) do python Evaluate.py %%f %threshold_cossim1%

for /R .\result\DS\ %%f in (*.csv) do python Evaluate.py %%f %threshold_cossim2%
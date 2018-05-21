@ECHO OFF & SETLOCAL

SET subject1=OM
SET chapters1=ch1 ch3 ch6 ch7 ch8 ch9 ch10 ch11 ch12 ch15 ch16 supplementA
SET thres_cossim1=0.2

SET subject2=DS
SET chapters2=ch2 ch3 ch4 ch5 ch6 ch7 ch9
SET thres_cossim2=0.1

for /R .\result\OM\ %%f in (*.csv) do python Evaluate.py %%f %thres_cossim1%
for /R .\result\DS\ %%f in (*.csv) do python Evaluate.py %%f %thres_cossim2%

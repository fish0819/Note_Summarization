@ECHO OFF & SETLOCAL ENABLEDELAYEDEXPANSION

SET subject1=OM
SET chapters1=ch1 ch3 ch6 ch7 ch8 ch9 ch10 ch11 ch12 ch15 ch16 supplementA
SET a1=0.2
SET b1=0.5
SET r1=0.3

SET subject2=DS
SET chapters2=ch2 ch3 ch4 ch5 ch6 ch78 ch9
SET a1=0.1
SET b1=0.4
SET r1=0.5

for %%c in (%chapters1%) do python OtherSummarizer.py %1 %subject1% %%c %a1% %b1% %r1%

for %%c in (%chapters2%) do python OtherSummarizer.py %1 %subject2% %%c %a2% %b2% %r2%
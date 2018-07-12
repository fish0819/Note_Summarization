@ECHO OFF & SETLOCAL ENABLEDELAYEDEXPANSION

SET subject1=OM
SET chapters1=ch1 ch3 ch6 ch7 ch8 ch9 ch10 ch11 ch12 ch15 ch16 supplementA

SET subject2=DS
SET chapters2=ch2 ch3 ch4 ch5 ch6 ch7 ch9

SET select_ratio1=0.25
SET select_ratio2=0.4
SET thres_support=10

for %%c in (%chapters1%) do (
    python OtherSummarizer.py %1 %subject1% %%c 0.1
    python OtherSummarizer-100.py %1 %subject1% %%c %select_ratio1%
    rem python Other_PatSum.py %1 %subject1% %%c %select_ratio1% %thres_support%
)

for %%c in (%chapters2%) do (
    python OtherSummarizer.py %1 %subject2% %%c 0.1
    python OtherSummarizer-100.py %1 %subject2% %%c %select_ratio2%
    rem python Other_PatSum.py %1 %subject2% %%c %select_ratio2% %thres_support%
)

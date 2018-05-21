@ECHO OFF & SETLOCAL

SET subject1=OM
SET chapters1=ch1 ch3 ch6 ch7 ch8 ch9 ch10 ch11 ch12 ch15 ch16 supplementA
SET thres_cossim1=0.2
SET a1=0.2
SET b1=0.5

SET subject2=DS
SET chapters2=ch2 ch3 ch4 ch5 ch6 ch7 ch9
SET thres_cossim2=0.1
SET a2=0.1
SET b2=0.4

SET threshold_score_list=0.05 0.1 0.15 0.2 0.25 0.3 0.35 0.4 0.45 0.5 0.55 0.65 0.7 0.8 0.9

rem for %%t in (%threshold_score_list%) do (
rem 	for %%c in (%chapters1%) do python Evaluate-1.py %1 %subject1% %%c %a1% %b1% %thres_cossim1% %%t
rem )

for %%t in (%threshold_score_list%) do (
	for %%c in (%chapters2%) do python Evaluate-1.py %1 %subject2% %%c %a2% %b2% %thres_cossim2% %%t
)
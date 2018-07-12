@ECHO OFF & SETLOCAL ENABLEDELAYEDEXPANSION

SET RUN_DOTPY=python.exe TranslateNotes.py
SET PYTHON_PATH=C:\Python36

SET subject1=OM
SET chapters1=ch1 ch3 ch6 ch7 ch8 ch9 ch10 ch11 ch12 ch15 ch16 supplementA
SET thres_cossim1=0.2
SET a1=0.2
SET b1=0.5
rem SET threshold_score1=0.5

SET subject2=DS
SET chapters2=ch2 ch3 ch4 ch5 ch6 ch7 ch9
SET thres_cossim2=0.1
SET a2=0.1
SET b2=0.4
rem SET threshold_score2=0.5

SET thres_score=0.6
for %%c in (%chapters1%) do python SelectSentences.py %1 %subject1% %%c %a1% %b1% %thres_cossim1% %thres_score%
for %%c in (%chapters2%) do python SelectSentences.py %1 %subject2% %%c %a2% %b2% %thres_cossim2% %thres_score%


rem SET threshold_score_list=0.05 0.1 0.15 0.2 0.25 0.3 0.35 0.4 0.45 0.5 0.55 0.65 0.7 0.8 0.9

:: test all threshold_fscore
rem for %%t in (%threshold_score_list%) do (
rem     for %%c in (%chapters1%) do python SelectSentences.py %1 %subject1% %%c %a1% %b1% %thres_cossim1% %%t
rem )

rem for %%t in (%threshold_score_list%) do (
rem     for %%c in (%chapters2%) do python SelectSentences.py %1 %subject2% %%c %a2% %b2% %thres_cossim2% %%t
rem )


:: test all combination of alpha, betta and gamma
rem SET alist=0 1 2 3 4 5 6 7 8 9 10
rem SET blist=0 1 2 3 4 5 6 7 8 9 10

rem for %%a in (%alist%) do (
rem     for %%b in (%blist%) do (
rem         SET /A "sum=%%a+%%b"
rem         :: LEQ less than or equal to
rem         if !sum! LEQ 10 (
rem             for %%c in (%chapters1%) do python SelectSentences.py %1 %subject1% %%c %%a %%b %thres_cossim1% %threshold_score1%
rem         )
rem     )
rem )

rem for %%a in (%alist%) do (
rem     for %%b in (%blist%) do (
rem         SET /A "sum=%%a+%%b"
rem         :: LEQ less than or equal to
rem         if !sum! LEQ 10 (
rem             for %%c in (%chapters2%) do python SelectSentences.py %1 %subject2% %%c %%a %%b %thres_cossim2% %threshold_score2%
rem         )
rem     )
rem )
@ECHO OFF & SETLOCAL

SET subject1=OM
SET chapters1=ch1 ch3 ch6 ch7 ch8 ch9 ch10 ch11 ch12 ch15 ch16 supplementA

SET subject2=DS
SET chapters2=ch2 ch3 ch4 ch5 ch6 ch78 ch9

SET threshold=0.05 0.1 0.15 0.2 0.25 0.3 0.35 0.4 0.45 0.5 0.55 0.6 0.7 0.8 0.9

rem for %%c in (%chapters1%) do (
rem 	for %%t in (%threshold%) do (
rem 		python CombineNotes.py %1 %subject1% %%c %%t
rem 		python MatchParagraphs.py %1 %subject1% %%c %%t
rem 		python CompareMatchBAndSJSD.py %1 %subject1% %%c %%t
rem 	)
rem )

for %%c in (%chapters2%) do (
	for %%t in (%threshold%) do (
		python CombineNotes.py %1 %subject2% %%c %%t
		python MatchParagraphs.py %1 %subject2% %%c %%t
		python CompareMatchBAndSJSD.py %1 %subject2% %%c %%t
	)
)
rem for %%c in (%chapters1%) do python CombineNotes.py %1 %subject1% %%c
rem for %%c in (%chapters2%) do python CombineNotes.py %1 %subject2% %%c
@ECHO OFF & SETLOCAL ENABLEDELAYEDEXPANSION

SET RUN_DOTPY=python.exe TranslateNotes.py
SET PYTHON_PATH=C:\Python36

SET subject1=OM
SET chapters1=ch1 ch3 ch6 ch7 ch8 ch9 ch10 ch11 ch12 ch15 ch16 supplementA

SET subject2=DS
SET chapters2=ch2 ch3 ch4 ch5 ch6 ch7 ch9

SET exam=exam1 exam2 exam3

for %%c in (%chapters1%) do (
	SET d=note/%subject1%/%%c/
	for /r %%f in (!d!*.docx) do python TranslateNotes.py %1 %subject1% %%c %%f
)

for %%c in (%chapters2%) do (
	SET d=note/%subject2%/%%c/
	for /r %%f in (!d!*.docx) do python TranslateNotes.py %1 %subject2% %%c %%f
)
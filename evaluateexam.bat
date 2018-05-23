@ECHO OFF & SETLOCAL

SET exam=1 2 3

SET subject1=OM
SET thres_cossim1=0.2
SET a1=0.2
SET b1=0.5

SET subject2=DS
SET thres_cossim2=0.1
SET a2=0.1
SET b2=0.4

SET thres_score=0.5

for %%e in (%exam%) do (
	python EvaluateExam.py %1 %subject1% %%e %a1% %b1% %thres_cossim1% %thres_score%
	python EvaluateExam.py %1 %subject2% %%e %a2% %b2% %thres_cossim2% %thres_score%
)
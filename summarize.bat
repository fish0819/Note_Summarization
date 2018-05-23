@ECHO OFF & SETLOCAL
:: run all files needed in this system

SET PYTHON_PATH=C:\Python36

SET subject1=OM
SET chapters1=ch1 ch3 ch6 ch7 ch8 ch9 ch10 ch11 ch12 ch15 ch16 supplementA

SET subject2=DS
SET chapters2=ch2 ch3 ch4 ch5 ch6 ch7 ch9

:: preprocess book contents
REM for %%c in (%chapters1%) do (
REM     python ProcessChapter.py %1 %subject1% %%c
REM     python ProcessBookContents.py %1 %subject1% %%c
REM     python ProcessBookIndex.py %1 %subject1% %%c
REM )
REM for %%c in (%chapters2%) do (
REM     python ProcessChapter.py %1 %subject2% %%c
REM     python ProcessBookContents.py %1 %subject2% %%c
REM     python ProcessBookIndex.py %1 %subject2% %%c
REM )

REM :: segment book contents
REM SET thres_dis=0.3
REM REM for %%c in (%chapters1%) do python SegmentBook.py %1 %subject1% %%c %thres_dis%
REM REM for %%c in (%chapters2%) do python SegmentBook.py %1 %subject2% %%c %thres_dis%
REM for %%c in (%chapters1%) do python SegmentBook_100.py %1 %subject1% %%c %thres_dis%
REM for %%c in (%chapters2%) do python SegmentBook_100.py %1 %subject2% %%c %thres_dis%

REM :: get book indexes
REM python GetBookIndex.py %1 OM
REM python GetBookIndex.py %1 DS
REM
REM :: get note terms
REM for %%c in (%chapters1%) do python GetNTerms.py %1 %subject1% %%c
REM for %%c in (%chapters2%) do python GetNTerms.py %1 %subject2% %%c
REM
REM :: get topics
REM for %%c in (%chapters1%) do python GetTopic.py %1 %subject1% %%c
REM for %%c in (%chapters2%) do python GetTopic.py %1 %subject2% %%c
REM
REM :: translate notes
REM for %%c in (%chapters1%) do (
REM 	SET d=note/%subject1%/%%c/
REM 	for /r %%f in (!d!*.docx) do python TranslateNotesWithoutWiki.py %1 !d! %%f
REM )
REM for %%c in (%chapters2%) do (
REM 	SET d=note/%subject2%/%%c/
REM 	for /r %%f in (!d!*.docx) do python TranslateNotesWithoutWiki.py %1 !d! %%f
REM )

:: combine slides and combine sentences in notes
SET thres_cossim1=0.2
SET thres_cossim2=0.1
REM for %%c in (%chapters1%) do python CombineSlides.py %1 %subject1% %%c
REM for %%c in (%chapters2%) do python CombineSlides.py %1 %subject2% %%c
REM for %%c in (%chapters1%) do python CombineNotes.py %1 %subject1% %%c %thres_cossim1%
REM for %%c in (%chapters2%) do python CombineNotes.py %1 %subject2% %%c %thres_cossim2%

REM :: match note paragraphs, slides and book paragraphs
REM for %%c in (%chapters1%) do python MatchParagraphs.py %1 %subject1% %%c %thres_cossim1%
REM for %%c in (%chapters2%) do python MatchParagraphs.py %1 %subject2% %%c %thres_cossim2%

:: select sentences from matched book paragraphs to form a summary
SET thres_score=0.5
SET a1=0.2
SET b1=0.5
SET a2=0.1
SET b2=0.4
REM for %%c in (%chapters1%) do python SelectSentences.py %1 %subject1% %%c %a1% %b1% %thres_cossim1% %thres_score%
REM for %%c in (%chapters2%) do python SelectSentences.py %1 %subject2% %%c %a2% %b2% %thres_cossim2% %thres_score%

REM :: evaluate the match of slide and book para
REM for %%c in (%chapters1%) do python CompareMatchBAndSJSD.py %1 %subject1% %%c %thres_cossim1%
REM for %%c in (%chapters2%) do python CompareMatchBAndSJSD.py %1 %subject2% %%c %thres_cossim2%

:: evaluate the jsd between summary and note (or book paragraphs, exam questions)
REM for %%c in (%chapters1%) do python Evaluate.py %1 %subject1% %%c %a1% %b1% %thres_cossim1% %thres_score%
for %%c in (%chapters2%) do python Evaluate.py %1 %subject2% %%c %a2% %b2% %thres_cossim2% %thres_score%

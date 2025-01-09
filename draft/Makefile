NAME = draft

$(NAME).pdf:
	latexmk -halt-on-error -f -shell-escape -pdf -quiet $(NAME).tex && rsync $(NAME).pdf ../$(NAME).pdf && make clean

clean:
	rm -f *.aux *.fdb_latexmk *.fls *.log *.bak* *.bbl *.blg *.out *Notes.bib *blx.bib *.run.xml *.toc *.spl
	
cleanpdf:
	rm -f $(NAME).pdf ../$(NAME).pdf

cleanall: clean cleanpdf


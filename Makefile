conda_base := $(shell conda info --base)

all: 
	make draft.pdf && make report.pdf

draft.pdf: 
	cd draft && latexmk -halt-on-error -f -shell-escape -pdf -quiet draft.tex && rsync draft.pdf ../draft.pdf && make clean

report.pdf:
	cd report && latexmk -halt-on-error -f -shell-escape -pdf -quiet report.tex && rsync report.pdf ../report.pdf && make clean

env-fluidsim-mpi:
	conda env create -f environment.yml
	
clean:
	rm -f **.aux **.fdb_latexmk **.fls **.log **.bak* **.bbl **.blg **.out **Notes.bib **blx.bib **.run.xml **.toc **.spl

cleanpdf:
	rm -f draft.pdf report.pdf draft/draft.pdf report/report.pdf  

cleanenv:
	@source $(conda_base)/etc/profile.d/conda.sh && conda deactivate || true
	@source $(conda_base)/etc/profile.d/conda.sh && conda env remove -n env-fluidsim-mpi2 || true 

cleanall: 
	clean && cleanenv && cleanpdf
	


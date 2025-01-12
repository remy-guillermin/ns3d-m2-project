conda_base := $(shell conda info --base)

all:
	make draft.pdf && make report.pdf && make env-fluidsim-mpi

draft.pdf:
	cd draft && latexmk -halt-on-error -f -shell-escape -pdf -quiet draft.tex && rsync draft.pdf ../draft.pdf && make cleanaux

report.pdf:
	cd report && latexmk -halt-on-error -f -shell-escape -pdf -quiet report.tex && rsync report.pdf ../report.pdf && make cleanaux

env-fluidsim-mpi:
	conda env create -f environment.yml

cleanaux:
	rm -f **.aux **.fdb_latexmk **.fls **.log **.bak* **.bbl **.blg **.out **Notes.bib **blx.bib **.run.xml **.toc **.spl

cleanpdf:
	rm -f draft.pdf report.pdf draft/draft.pdf report/report.pdf

cleanenv:
	@source $(conda_base)/etc/profile.d/conda.sh && \
	conda deactivate || true && \
	conda env remove -n env-fluidsim-mpi

clean:
	make cleanaux && make cleanenv && make cleanpdf



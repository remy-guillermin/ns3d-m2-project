conda_base := $(shell conda info --base)

all:
	make draft.pdf && make report.pdf && make slide.pdf

draft.pdf:
	cd draft && latexmk -halt-on-error -f -shell-escape -pdf -quiet draft.tex && rsync draft.pdf ../draft.pdf && cd ../ && make cleanaux

report.pdf:
	cd report && latexmk -halt-on-error -f -shell-escape -pdf -quiet report.tex && rsync report.pdf ../report.pdf && cd ../ && make cleanaux

slide.pdf:
	cd slides && latexmk -halt-on-error -f -shell-escape -pdf -quiet slide.tex && rsync slide.pdf ../slide.pdf && cd ../ && make cleanaux

env-fluidsim-mpi:
	conda env create -f environment.yml

cleanaux:
	rm -f */*.aux */*.fdb_latexmk */*.fls */*.log */*.bak* */*.bbl */*.blg */*.out */*Notes.bib */*blx.bib */*.run.xml */*.toc */*.spl

cleanpdf:
	rm -f draft.pdf report.pdf slide.pdf draft/draft.pdf report/report.pdf slides/slide.pdf

cleanenv:
	@source $(conda_base)/etc/profile.d/conda.sh && \
	conda deactivate || true && \
	conda env remove -n env-fluidsim-mpi

clean:
	make cleanaux && make cleanpdf && make cleanenv 



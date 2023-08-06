# Makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    = -n
SPHINXBUILD   = sphinx-build
PAPER         =
BUILDDIR      = _build

# Internal variables.
PAPEROPT_a4     = -D latex_paper_size=a4
PAPEROPT_letter = -D latex_paper_size=letter
ALLSPHINXOPTS   = -d $(BUILDDIR)/doctrees $(PAPEROPT_$(PAPER)) $(SPHINXOPTS) .
# the i18n builder cannot share the environment and doctrees with the others
I18NSPHINXOPTS  = $(PAPEROPT_$(PAPER)) $(SPHINXOPTS) .

VERSION = $(shell python version.py)

PANDOC_LATEX_IMAGE_NAME = pandoc_latex_image
PANDOC_LATEX_IMAGE_RUN  = docker run --rm --volume "$(shell pwd)/_build/latex:/usr/src" --entrypoint="" $(PANDOC_LATEX_IMAGE_NAME)

.PHONY: help clean html dirhtml singlehtml pickle json htmlhelp qthelp devhelp epub latex latexpdf xelatexpdf text \
	man changes linkcheck doctest gettext executenotebooks build-latex-image

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  html       to make standalone HTML files"
	@echo "  dirhtml    to make HTML files named index.html in directories"
	@echo "  singlehtml to make a single large HTML file"
	@echo "  pickle     to make pickle files"
	@echo "  json       to make JSON files"
	@echo "  htmlhelp   to make HTML files and a HTML help project"
	@echo "  epub       to make an epub"
	@echo "  latex      to make LaTeX files, you can set PAPER=a4 or PAPER=letter"
	@echo "  latexpdf   to make LaTeX files and run them through pdflatex"
	@echo "  xelatexpdf to make xeLaTeX files and run them through pdflatex"
	@echo "  text       to make text files"
	@echo "  man        to make manual pages"
	@echo "  texinfo    to make Texinfo files"
	@echo "  info       to make Texinfo files and run them through makeinfo"
	@echo "  gettext    to make PO message catalogs"
	@echo "  changes    to make an overview of all changed/added/deprecated items"
	@echo "  linkcheck  to check all external links for integrity"
	@echo "  doctest    to run all doctests embedded in the documentation (if enabled)"


build-latex-image:
	@if [ "$(shell docker images -q $(PANDOC_LATEX_IMAGE_NAME))" = "" ]; then\
		echo "Build pandoc-latex image";\
		docker build --tag $(PANDOC_LATEX_IMAGE_NAME) -f ../dockerfiles/latex.Dockerfile .;\
	fi


flake8-notebooks:
	# find the notebooks
	# ...that aren't in a hidden path (to avoid checkpoints, etc.)
	# ...and for each one, get Python code from nbconvert, and run flake8
	# ...after stripping lines beginning with '%' (ipython magic that messes up flake8)
	# (use a tempfile instead of a pipe b/c exit code from failing pipe isn't correct)
	mkdir -p $(BUILDDIR)
	# Using a tempfile (under $(BUILDDIR) so it's okay) instead of piping stdin/stdout
	# because pipes don't give the right exit code
	set -e; for notebook in `find . -iname '*.ipynb' -not -path '*/\.*'`;\
	do jupyter nbconvert $$notebook --output-dir $(BUILDDIR) --output temp.py --to python --template jupyter_template_for_flake8.tpl;\
	sed -i.bak '/^%/ d' $(BUILDDIR)/temp.py;\
	flake8 $(BUILDDIR)/temp.py --max-line-length=79 --show-source --ignore=E402;\
	done
	# Note:
	#  - The template strips markdown cells (since otherwise they would become comments that are too long)
	#  - notebook clarity is improved by importing where needed (rather than everything at the top), so ignore E402

clean:
	-rm -rf $(BUILDDIR)/*
	-rm -f datarobot_examples.zip

html:
	$(SPHINXBUILD) -W -b html $(ALLSPHINXOPTS) $(BUILDDIR)/html
	@echo
	@echo "Build finished. The HTML pages are in $(BUILDDIR)/html."

htmlzip: html
	cd $(BUILDDIR)/html && zip datarobot_docs_$(VERSION).zip -r ./*
	echo "\nMade $(BUILDDIR)/html/datarobot_docs_$(VERSION).zip for upload to readthedocs"

dirhtml:
	$(SPHINXBUILD) -W -b dirhtml $(ALLSPHINXOPTS) $(BUILDDIR)/dirhtml
	@echo
	@echo "Build finished. The HTML pages are in $(BUILDDIR)/dirhtml."

singlehtml:
	$(SPHINXBUILD) -W -b singlehtml $(ALLSPHINXOPTS) $(BUILDDIR)/singlehtml
	@echo
	@echo "Build finished. The HTML page is in $(BUILDDIR)/singlehtml."

pickle:
	$(SPHINXBUILD) -W -b pickle $(ALLSPHINXOPTS) $(BUILDDIR)/pickle
	@echo
	@echo "Build finished; now you can process the pickle files."

json:
	$(SPHINXBUILD) -W -b json $(ALLSPHINXOPTS) $(BUILDDIR)/json
	@echo
	@echo "Build finished; now you can process the JSON files."

htmlhelp:
	$(SPHINXBUILD) -W -b htmlhelp $(ALLSPHINXOPTS) $(BUILDDIR)/htmlhelp
	@echo
	@echo "Build finished; now you can run HTML Help Workshop with the" \
	      ".hhp project file in $(BUILDDIR)/htmlhelp."

epub:
	$(SPHINXBUILD) -W -b epub $(ALLSPHINXOPTS) $(BUILDDIR)/epub
	@echo
	@echo "Build finished. The epub file is in $(BUILDDIR)/epub."

latex:
	$(SPHINXBUILD) -W -b latex $(ALLSPHINXOPTS) $(BUILDDIR)/latex
	@echo
	@echo "Build finished; the LaTeX files are in $(BUILDDIR)/latex."
	@echo "Run \`make' in that directory to run these through (pdf)latex" \
	      "(use \`make latexpdf' here to do that automatically)."


latexpdf: build-latex-image
	$(SPHINXBUILD) -W -b latex $(ALLSPHINXOPTS) $(BUILDDIR)/latex
	@echo "Running LaTeX files through pdflatex..."
	$(PANDOC_LATEX_IMAGE_RUN) sh -c 'make PDFLATEX=xelatex all-pdf'
	@echo "Making index..."
	$(PANDOC_LATEX_IMAGE_RUN) sh -c 'makeindex *.idx'
	@echo "Re-running LaTeX files through xelatex to build index..."
	$(PANDOC_LATEX_IMAGE_RUN) sh -c 'make PDFLATEX=xelatex all-pdf'
	@echo "pdflatex finished; the PDF files are in $(BUILDDIR)/latex."

xelatexpdf:
	$(SPHINXBUILD) -W -b latex $(ALLSPHINXOPTS) $(BUILDDIR)/latex
	@echo "Running LaTeX files through xelatex..."
	$(PANDOC_LATEX_IMAGE_RUN) sh -c 'make PDFLATEX=xelatex all-pdf'
	@echo "Making index..."
	$(PANDOC_LATEX_IMAGE_RUN) sh -c 'makeindex *.idx'
	@echo "Re-running LaTeX files through xelatex to build index..."
	$(PANDOC_LATEX_IMAGE_RUN) sh -c 'make PDFLATEX=xelatex all-pdf'
	@echo "xelatex finished; the PDF files are in $(BUILDDIR)/latex."


text:
	$(SPHINXBUILD) -W -b text $(ALLSPHINXOPTS) $(BUILDDIR)/text
	@echo
	@echo "Build finished. The text files are in $(BUILDDIR)/text."

man:
	$(SPHINXBUILD) -W -b man $(ALLSPHINXOPTS) $(BUILDDIR)/man
	@echo
	@echo "Build finished. The manual pages are in $(BUILDDIR)/man."

texinfo:
	$(SPHINXBUILD) -W -b texinfo $(ALLSPHINXOPTS) $(BUILDDIR)/texinfo
	@echo
	@echo "Build finished. The Texinfo files are in $(BUILDDIR)/texinfo."
	@echo "Run \`make' in that directory to run these through makeinfo" \
	      "(use \`make info' here to do that automatically)."

info:
	$(SPHINXBUILD) -W -b texinfo $(ALLSPHINXOPTS) $(BUILDDIR)/texinfo
	@echo "Running Texinfo files through makeinfo..."
	make -C $(BUILDDIR)/texinfo info
	@echo "makeinfo finished; the Info files are in $(BUILDDIR)/texinfo."

gettext:
	$(SPHINXBUILD) -W -b gettext $(I18NSPHINXOPTS) $(BUILDDIR)/locale
	@echo
	@echo "Build finished. The message catalogs are in $(BUILDDIR)/locale."

changes:
	$(SPHINXBUILD) -W -b changes $(ALLSPHINXOPTS) $(BUILDDIR)/changes
	@echo
	@echo "The overview file is in $(BUILDDIR)/changes."

linkcheck:
	$(SPHINXBUILD) -W -b linkcheck $(ALLSPHINXOPTS) $(BUILDDIR)/linkcheck
	@echo
	@echo "Link check complete; look for any errors in the above output " \
	      "or in $(BUILDDIR)/linkcheck/output.txt."

doctest:
	$(SPHINXBUILD) -W -b doctest $(ALLSPHINXOPTS) $(BUILDDIR)/doctest
	@echo "Testing of doctests in the sources finished, look at the " \
	      "results in $(BUILDDIR)/doctest/output.txt."

executenotebooks:
	# Convenience method to execute the notebooks and
	# populate all of the output blocks prior to html document generation.
	# Runs all the notebooks under the examples directory, but excludes . files,
	# especially notebook checkpoint files in .ipynb_checkpoint directories
	#
	# Will stop on any error, notably missing data and API key files
	#
	# Notable nbconvert arguments
	# --ExecuteProcessor.timeout (seconds) needs to be large to allow DataRobot to run
	# --debug prints all executing commands to the console to see progress
	@echo "Executing all the Jupyter Notebooks. This may take a long time..."
	set -e; jupyter nbconvert --to notebook --execute \
		`find examples -not -path '*/\.*' -iname '*.ipynb'` \
	       	--inplace --ExecutePreprocessor.timeout=3600 --debug

# Based on https://gitlab.torproject.org/anarcat/presentations/-/blob/main/anarcat-tpa-okrs-2021/Makefile

export TEXINPUTS:=$(shell pwd)/../vendor/onion-tex/src/tex:${TEXINPUTS}

# The slides from pandoc do not work very well. the `\onioncolorlog`
# never renders (it stalls) and using the PNG logo doesn't
# work well as it gets rescaled and all fuzzy
#GENERATED=slides.pdf slides.tex tikz

# Instead just build upon a raw TeX file that i cargo culted from
# anarcat which cargo culted from ahf/okr2021-talk/main.tex
GENERATED=demoday.pdf

all: $(GENERATED)

%.pdf: %.tex
	mkdir -p tikz
	latexmk -pdf -verbose -pdflatex="pdflatex --shell-escape %O %S" $<

# Right now no markdown file is used
#%.tex: %.md
#	pandoc -t beamer -V theme:onion -s $< -o $@

clean:
	rm -rf $(GENERATED)

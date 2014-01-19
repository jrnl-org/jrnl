# A Makefile for commands I run frequently:

clean:
	rm -rf dist
	rm -rf _static
	rm -rf jrnl.egg-info

# Build GitHub Page from docs
docs:
	git checkout gh-pages ; \
	git checkout master docs ; \
	git checkout master jrnl ; \
	lessc --clean-css docs/_themes/jrnl/static/less/jrnl.less docs/_themes/jrnl/static/css/jrnl.css ; \
	cd docs ; \
	make html ; \
	cd .. ; \
	cp -r docs/_build/html/* . ; \
	git add -A ; \
	git commit -m "Updated docs from master" ; \
	git push -u origin gh-pages ; \
	git checkout master

# Upload to pipy
dist:
	python setup.py publish

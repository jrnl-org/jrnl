# This currently only builds gh-pages from docs

gh_pages:
	git checkout gh-pages ; \
	git checkout master docs ; \
	git checkout master jrnl ; \
	cd docs ; \
	make html ; \
	cd .. ; \
	cp -r docs/_build/html/* . ; \
	git add * ; \
	git commit -m "Updated docs from master" ; \
	git push -u origin gh-pages ; \
	git checkout master


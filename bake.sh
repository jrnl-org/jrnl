#! /bin/bash
git checkout master README.md
markdown2 README.md > tmp
cat templates/header.html tmp templates/footer.html > index.html
rm tmp
git add index.html
git commit -m "Updated Readme from master"
git push -u origin gh-pages

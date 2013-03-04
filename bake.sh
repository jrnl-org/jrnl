#! /bin/bash
git checkout master README.md
git checkout master CHANGELOG.md
markdown2 README.md > tmp_readme
markdown2 CHANGELOG.md > tmp_log
sed -i.bak 's/<li>\[/<li class="badge">\[/g' tmp_log
sed -i.bak 's/\[Fixed\]/<span class="change-fixed">Fixed<\/span>/g' tmp_log
sed -i.bak 's/\[Improved\]/<span class="change-improved">Improved<\/span>/g' tmp_log
sed -i.bak 's/\[New\]/<span class="change-new">New<\/span>/g' tmp_log
cat templates/header.html tmp_readme tmp_log templates/footer.html > index.html
rm tmp_readme tmp_log
git add index.html
git commit -m "Updated Readme from master"
git push -u origin gh-pages

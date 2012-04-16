#! /bin/bash
markdown2 README.md > tmp
cat templates/header.html tmp templates/footer.html > index.html
rm tmp

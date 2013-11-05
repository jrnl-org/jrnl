from fabric.api import *
from fabric.contrib.console import confirm

def create_sphinx_pages():
    """
    Create a new branch with Sphinx documentation ready to be published
    using GitHub's Pages system.

    Example usage:

        $ fab make_sphinx_branch

    Before you can publish your docs, you need to commit them to the repo.

        $ git add .
        $ git commit -am "First commit"

    Then publish the files by pushing them up to GitHub.

        $ git push origin gh-pages

    Then the docs will appear on GitHub at:

        http://<your_account_name>.github.com/<your_repo_name>/

    """
    # Create the new branch
    local("git branch gh-pages")
    # Move into it
    local("git checkout gh-pages")
    # Clear it out
    local("git symbolic-ref HEAD refs/heads/gh-pages")
    local("rm .git/index")
    local("git clean -fdx")
    # Install sphinx
    local("pip install sphinx")
    # Save the dependencies to the requirements file
    local("pip freeze > requirements.txt")
    # Warn the user of a quirk before configuring with Sphinx
    confirm(""".    ___ ___ _     ___ ___  _
  /\  |   | |_ |\ | |   |  / \ |\ |
 /--\ |   | |_ | \| |  _|_ \_/ | \|

Sphinx is about to start configuring your project.

You can accept the default settings it offers, EXCEPT ONE.

The second question it will ask is:

'Separate source and build directories (y/N) [n]:'

YOU MUST ANSWER YES. THAT MEANS YOU TYPE 'Y' AND PRESS ENTER.

DO YOU UNDERSTAND?""")
    # Start up a Sphinx project
    local("sphinx-quickstart")
    # Create the .nojekyll file GitHub requires
    local("touch .nojekyll")
    # Make the patches to Sphinx's Makefile we need
    local("echo '' >> Makefile")
    local("echo 'BUILDDIR      = ./' >> Makefile")
    local("echo '' >> Makefile")
    local("echo 'html:' >> Makefile")
    local("echo '\t$(SPHINXBUILD) -b html $(ALLSPHINXOPTS) $(BUILDDIR)' >> Makefile")
    local("echo '\t@echo' >> Makefile")
    local("echo '\t@echo \"Build finished. The HTML pages are in $(BUILDDIR)\"' >> Makefile")
    # Make the branch for the first time
    local("make html")

# Contributing

If you use jrnl, you can totally make our day by just saying "thanks for the code." It's your chance to make a programmer happy today! If you have a moment, let us know what you use jrnl for and how; it'll help us to make it even better!


# Table of Contents
 * [Docs and Typos](#docs-and-typos)
 * [Bugs](#bugs)
 * [Feature requests and ideas](#feature-requests-and-ideas)
 * [New programmers and programmers new to python](#new-programmers-and-programmers-new-to-python)
 * [Developing jrnl](#developing-jrnl)


## Docs and Typos

If you find a typo or a mistake in the docs, please fix it right away and send a pull request. The Right Way™ to fix the docs is to edit the `docs/*.md` files on the **master** branch. You can see the result if you run `make html` inside the project's root directory, which will open a browser that hot-reloads as you change the docs. This requires [mkdocs](https://www.mkdocs.org) to be installed. The `gh-pages` branch is automatically maintained and updates from `master`; you should never have to edit that.

## Bugs

Unfortunately, bugs happen. If you found one, please [open a new issue](https://github.com/jrnl-org/jrnl/issues/new/choose) and describe it as well as possible. If you're a programmer with some time, go ahead and send us a pull request that references the issue! We'll review as quickly as we can.

## Feature requests and ideas

So, you have an idea for a great feature? Awesome! We'd love to hear from you! Please [open a new issue](https://github.com/jrnl-org/jrnl/issues/new/choose) and describe the goal of the feature, and any relevant use cases. We'll discuss the issue with you, and decide if it's a good fit for the project.

When discussing new features, please keep in mind our design goals. jrnl strives to do one thing well. To us, that means:

* be _slim_
* have a simple interface
* avoid duplicating functionality

## New programmers and programmers new to python

Although jrnl has grown quite a bit since its inception, the overall complexity (for an end-user program) is fairly low, and we hope you'll find the code easy enough to understand.

If you have a question, please don't hesitate to ask! Python is known for its welcoming community and openness to novice programmers, so feel free to fork the code and play around with it! If you create something you want to share with us, please create a pull request. We never expect pull requests to be perfect, idiomatic, instantly mergeable code. We can work through it together!

## Developing jrnl

The jrnl source uses [poetry](https://poetry.eustace.io/) for dependency management. You will need to install it to develop journal.

 * To run tests: `make test` (or `poetry run behave` if on Windows)
 * To run the source: `poetry install` then `poetry shell` then run `jrnl` with or without arguments as necessary

For testing, jrnl uses [behave](https://behave.readthedocs.io/).

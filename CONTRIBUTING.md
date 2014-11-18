Contributing
============

If you use jrnl, you can totally make my day by just saying "thanks for the code" or by [tweeting about jrnl](https://twitter.com/intent/tweet?text=Write+your+memoirs+on+the+command+line.+Like+a+boss.+%23jrnl&url=http%3A%2F%2Fmaebert.github.io%2Fjrnl&via=maebert). It's your chance to make a programmer happy today! If you have a minute or two, let me know what you use jrnl for and how, it'll help me to make it even better. If you blog about jrnl, I'll send you a post card!


Docs & Typos
------------

If you find a typo or a mistake in the docs, just fix it right away and send a pull request. The Right Way™ to fix the docs is to edit the `docs/*.rst` files on the **master** branch. You can see the result if you run `make html` inside the project's root directory, and then open `docs/_build/html/index.html` in your browser. Note that this requires [lessc](http://lesscss.org/#using-less-installation) and [Sphinx](https://pypi.python.org/pypi/Sphinx) to be installed. Changes to the CSS or Javascript should be made on `docs/_themes/jrnl/`. The `gh-pages` branch is automatically maintained and updates from `master`; you should never have to edit that.

Bugs
----

They unfortunately happen. Specifically, I don't have a Windows machine to test on, so expect a few rough spots. If you found a bug, please [open a new issue](https://www.github.com/maebert/jrnl/issues/new) and describe it as well as possible. If you're a programmer and have a little time to spare, go ahead, fork the code and fix bugs you spot, it'll be much appreciated!


Feature requests and ideas
--------------------------

So, you have an idea for a great feature? Awesome. I love you. As with bugs, first you should [open a new issue](https://www.github.com/maebert/jrnl/issues/new) on GitHub, describe the use case and what the feature should accomplish. If we agree that this feature is useful, it will sooner or later get implemented. Even sooner if you roll up your sleeves and code it yourself ;-)

Keep in mind that the design goal of jrnl is to be _slim_. That means

* having as few dependencies as possible
* creating as little interface as possible to boost the learning curve
* doing one thing and one thing well

Beyond that, it should also play nice with other software and tools -- however, avoid duplicating functionality that existing tools already provide. For example, we played around with the idea of a git integrated journal so new entries would be stored in commits. However, the proposed implementation required a rather heavy git module for python as an dependency, and the same feature could be implemented with a little bit of shell scripting around jrnl.


A short note for new programmers and programmers new to python
--------------------------------------------------------------

Although jrnl grew quite a bit since I first started working on it, the overall complexity (for an end-user program) is fairly low, and I hope you'll find the code easy enough to understand -- if you have a question, don't hesitate to ask! Python is known for it's great community and openness to novice programmers. Feel free to fork the code and play around with it. If you think you created something worth sharing, create a pull request. I never expect pull requests to be perfect, idiomatic, instantly mergeable code, and we can work through it together. Go for it!

Contributing
============

If you use jrnl, you can totally make our day by just saying "thanks for the code." It's your chance to make a programmer happy today! If you have a moment, let us know what you use jrnl for and how; it'll help us to make it even better!


Docs & Typos
------------

If you find a typo or a mistake in the docs, please fix it right away and send a pull request. The Right Way™ to fix the docs is to edit the `docs/*.rst` files on the **master** branch. You can see the result if you run `make html` inside the project's root directory, and then open `docs/_build/html/index.html` in your browser. Note that this requires [lessc](http://lesscss.org/) and [Sphinx](https://pypi.python.org/pypi/Sphinx) to be installed. Changes to the CSS or Javascript should be made on `docs/_themes/jrnl/`. The `gh-pages` branch is automatically maintained and updates from `master`; you should never have to edit that.

Bugs
----

Unfortunately, bugs happen. If you found one, please [open a new issue](https://github.com/jrnl-org/jrnl/issues/new) and describe it as well as possible. If you're a programmer with some time, go ahead and send us a pull request! We'll review as quickly as we can.


Feature requests and ideas
--------------------------

So, you have an idea for a great feature? Awesome! We'd love to hear from you! Please [open a new issue](https://github.com/jrnl-org/jrnl/issues) and describe the goal of the feature, and any relvant use cases. We'll discuss the issue with you, and decide if it's a good fit for the project.

When discussing new features, please keep in mind our design goals. jrnl strives to do one thing well. To us, that means:

* be _slim_
* have a simple interface
* avoid dupicating functionality


A short note for new programmers and programmers new to python
--------------------------------------------------------------

Although jrnl has grown quite a bit since its inception. The overall complexity (for an end-user program) is fairly low, and we hope you'll find the code easy enough to understand.

If you have a question, please don't hesitate to ask! Python is known for its welcoming community and openness to novice programmers, so feel free to fork the code and play around with it! If you create something you want to share with us, please create a pull request. We never expect pull requests to be perfect, idiomatic, instantly mergeable code. We can work through it together!

# jrnl

*jrnl* is a simple journal application for your command line. Journals are stored as human readable plain text files - you can put them into a Dropbox folder for instant syncinc and you can be assured that your journal will still be readable in 2050, when all your fancy iPad journal applications will long be forgotten.

## Why keep a journal?

Journals aren't only for 13-year old girls and people who have too much time on their summer vacation. A journal helps you to keep track of the things you get done and how you did them. Your imagination may be limitless, but your memory isn't. For personal use, make it a good habit to write at least 20 words a day. Just to reflect what made this day special, why you haven't wasted it. For professional use, consider a text-based journal to be the perfect complement to your GTD todo list - a documentation of what and how you've done it.

## How to use?

to make a new entry, just type

    jrnl

and hit return. You will be asked to compose your entry. Everything until the first sentence mark (`.?!`) will be interpreted as the title, the rest as the body. In your journal file, the result may look like this:

    2012-03-29 17:16 Solved the animal-sorting problem.
    Solution is to squeeze each instance and Fourier-transform the emitted sound.

### Smart timestamps:

If we start our entry by e.g. `yesterday:` or `last week monday at 9am:` the entry's date will automatically be adjusted. 

### Viewing:

    jrnl -10   

will list you the ten latest entries,

    jrnl -from last year -to march   

everything that happened from the start of last year to the end of last march.

### Tagging:

Keep track of people, projects or locations: start names with an `@` character and all other things with a hash:

    Wonderful day on the #beach with @Tom and @Anna.

You can filter your journal entries just like this:

    jrnl -all @pinkie #WorldDomination

Will print all entries in which either `@pinkie` or `#WorldDomination` occured;

    jrnl -5 -and #pineapple #lubricant

the last five entries containing both `#pineapple` _and_ `#lubricant`.

## Installation

...

## Advanced configuration

After installation, _jrnl_ will create a file called `.jrnl_config` in your home directory. It's just a regular `json` file:

    {
        journal:       "~/journal.txt",
        default_hour:   9,
        default_minute: 0,
        timeformat:     "%Y-%m-%d %H:%M",
    }

Before using _jrnl_ I recommend changing your journal location to somewhere it belongs, for example your Dropbox folder.

 - `journal`: path to  your journal file
 - `default_hour` and `default_minute`: if you supply a date, such as `last thursday`, but no specific time, the entry will be created at this time
 - `timeformat`: how to format the timestamps in your journal, see the [python docs](http://docs.python.org/library/time.html#time.strftime) for reference
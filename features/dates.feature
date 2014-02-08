
@dates1 @dates @wip
Feature: Processing of (relative) dates and times
	# all these test are 'brittle', in that they depend on the day it is run
	# these results assume the test is run on Feb 8, 2014

	Scenario Outline: no date
		Given we use the config "basic.json"
		When we run "jrnl I saw Elvis <entry no>. He's alive!"
		Then we should get no error
		Then the journal should contain "<date out> I saw Elvis <entry no>"

		Examples: no date
			| date in	| date out			| entry no	|
			|			| 2014-02-08 09:00	| 1			|

	Scenario Outline: Test all sorts of (non-fixed) dates
		Given we use the config "empty.json"
		When we run "jrnl <date in>: I saw Elvis <entry no>."
		Then we should get no error
		Then the journal should contain "<date out> I saw Elvis <entry no>"

		Examples: strings
			| date in	| date out			| entry no	|
			| today		| 2014-02-08 09:00	| 2			|
			| tomorrow	| 2014-02-09 09:00	| 3			|
			| yesterday	| 2014-02-07 09:00	| 4			|

		Examples: strings with times
			| date in		| date out			| entry no	|
			| today	2pm		| 2014-02-08 14:00	| 5			|
			| today at 3pm	| 2014-02-08 15:00	| 6			|
			| today 8am		| 2014-02-08 08:00	| 7			|
			| today	16:27	| 2014-02-08 16:27	| 8			|
			| today 5:18	| 2014-02-08 05:18	| 9			|
			| today 6:47pm	| 2014-02-08 18:47	| 10		|

		Examples: days of the week
			| date in	| date out			| entry no	|
			| monday	| 2014-02-10 09:00	| 11		|
			| tuesday	| 2014-02-11 09:00	| 12		|
			| wednesday	| 2014-02-12 09:00	| 13		|
			| thursday	| 2014-02-13 09:00	| 14		|
			| friday	| 2014-02-14 09:00	| 15		|
			| saturday	| 2014-02-08 09:00	| 16		|
			| sunday	| 2014-02-09 09:00	| 17		|

		Examples: days of the week
			| date in	| date out			| entry no	|
			| mon		| 2014-02-10 09:00	| 18		|
			| tues		| 2014-02-11 09:00	| 19		|
			| wed		| 2014-02-12 09:00	| 20		|
			| thurs		| 2014-02-13 09:00	| 21		|
			| fri		| 2014-02-14 09:00	| 22		|
			| sat		| 2014-02-08 09:00	| 23		|
			| sun		| 2014-02-09 09:00	| 24		|
			| tue		| 2014-02-11 09:00	| 25		|
			| thu		| 2014-02-13 09:00	| 26		|

		Examples: days of the week with a time
			| date in		| date out			| entry no	|
			| mon at 5am	| 2014-02-10 05:00	| 27		|

		Examples: Qualified days of the week
			| date in		| date out	| entry no	|
			| last monday	|2014-02-03 09:00	| 28		|
			| next monday	|2014-02-10 09:00	| 29		|

		Examples: Just times
			| date in	| date out	| entry no	|
			| at 8pm	|2014-02-10 20:00	| 30		|
			| noon		|2014-02-10 12:00	| 31		|
			| midnight	|2014-02-10 00:00	| 32		|

		Examples: short months
			| date in	| date out			| entry no	|
			| jan		| 2015-01-01 09:00	| 33		|
			| feb		| 2014-02-01 09:00	| 34		|
			| mar		| 2014-03-01 09:00	| 35		|
			| apr		| 2014-04-01 09:00	| 36		|
			| may		| 2014-05-01 09:00	| 37		|
			| jun		| 2014-06-01 09:00	| 38		|
			| jul		| 2014-07-01 09:00	| 39		|
			| aug		| 2014-08-01 09:00	| 40		|
			| sep		| 2014-09-01 09:00	| 41		|
			| oct		| 2014-10-01 09:00	| 42		|
			| nov		| 2014-11-01 09:00	| 43		|
			| dec		| 2014-12-01 09:00	| 44		|
			| sept		| 2014-09-01 09:00	| 45		|

		Examples: long months
			| date in	| date out			| entry no	|
			| january	| 2015-01-01 09:00	| 46		|
			| february	| 2014-02-01 09:00	| 47		|
			| march		| 2014-03-01 09:00	| 48		|
			| april		| 2014-04-01 09:00	| 49		|
			| june		| 2014-06-01 09:00	| 50		|
			| july		| 2014-07-01 09:00	| 51		|
			| august	| 2014-08-01 09:00	| 52		|
			| september	| 2014-09-01 09:00	| 53		|
			| october	| 2014-10-01 09:00	| 54		|
			| november	| 2014-11-01 09:00	| 55		|
			| december	| 2014-12-01 09:00	| 56		|

		Examples: month + day (no year)
			| date in	| date out			| entry no	|
			| 7 apr		| 2014-04-07 09:00	| 57		|
			| apr 8		| 2014-04-08 09:00	| 58		|
			| 9 march	| 2014-03-09 09:00	| 59		|
			| march 10	| 2014-03-10 09:00	| 60		|

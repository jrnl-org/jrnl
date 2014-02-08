
@dates @wip
Feature: Processing of dates and times

	Scenario Outline: Test all sorts of dates
		Given we use the config "basic.json"
        When we run "jrnl" and enter "<date in> I saw Elvis. <entry no>"
        Then we should get no error
        and the journal should contain "<date out> I saw Elvis. <entry no>"

		Examples: no date
			| date in	| date out	| entry no	|
			|			|			| 1			|

		Examples: strings
			| date in	| date out	| entry no	|
			| today		|			| 2			|
			| tomorrow	|			| 3			|
			| yesterday	|			| 4			|

		Examples: strings with times
			| date in		| date out	| entry no	|
			| today	2pm		|			| 5			|
			| today at 3pm	|			| 6			|
			| today 8am		|			| 7			|
			| today	16:27	|			| 8			|
			| today 5:18	|			| 9			|
			| today 6:47pm	|			| 10		|

		Examples: days of the week
			| date in	| date out	| entry no	|
			| monday	|			| 11		|
			| tuesday	|			| 12		|
			| wednesday	|			| 13		|
			| thrusday	|			| 14		|
			| friday	|			| 15		|
			| saturday	|			| 16		|
			| sunday	|			| 17		|

		Examples: days of the week
			| date in	| date out	| entry no	|
			| mon		|			| 18		|
			| tues		|			| 19		|
			| wed		|			| 20		|
			| thrus		|			| 21		|
			| fri		|			| 22		|
			| sat		|			| 23		|
			| sun		|			| 24		|
			| tue		|			| 25		|
			| thr		|			| 26		|

		Examples: days of the week with a time
			| date in		| date out	| entry no	|
			| mon at 5am	|			| 27		|

		Examples: Qualified days of the week
			| date in		| date out	| entry no	|
			| last monday	|			| 28		|
			| next monday	|			| 29		|

		Examples: Just times
			| date in	| date out	| entry no	|
			| at 8pm	|			| 30		|
			| noon		|			| 31		|
			| midnight	|			| 32		|

		Examples: short months
			| date in	| date out	| entry no	|
			| jan		|			| 33		|
			| feb		|			| 34		|
			| mar		|			| 35		|
			| apr		|			| 36		|
			| may		|			| 37		|
			| jun		|			| 38		|
			| jul		|			| 39		|
			| aug		|			| 40		|
			| sep		|			| 41		|
			| oct		|			| 42		|
			| nov		|			| 43		|
			| dec		|			| 44		|
			| sept		|			| 45		|

		Examples: long months
			| date in	| date out	| entry no	|
			| january	|			| 46		|
			| february	|			| 47		|
			| march		|			| 48		|
			| april		|			| 49		|
			| june		|			| 50		|
			| july		|			| 51		|
			| august	|			| 52		|
			| september	|			| 53		|
			| october	|			| 54		|
			| november	|			| 55		|
			| december	|			| 56		|

		Examples: month + day (no year)
			| date in	| date out	| entry no	|
			| 7 apr		|			| 57		|
			| apr 8		|			| 58		|
			| 9 march	|			| 59		|
			| march 10	|			| 60		|

		Examples: year
			| date in	| date out			| entry no	|
			| 1998		| 1998-01-01 9:00	| 61		|
			| 2013		| 2013-01-01 9:00	| 62		|
			| 2014		| 2014-01-01 9:00	| 63		|
			| 2015		| 2015-01-01 9:00	| 64		|
			| 2051		| 2051-01-01 9:00	| 65		|

		Examples: year + month
			| date in			| date out			| entry no	|
			| jun 2013			| 2013-06-01 9:00	| 66		|
			| 2013 jul			| 2013-07-01 9:00	| 67		|
			| august 2013		| 2013-08-01 9:00	| 68		|
			| 2013 september	| 2013-09-01 9:00	| 69		|

		Examples: 'YYYY-MM-DD' dates (with and without times)
			| date in			| date out			| entry no	|
			| 2013-06-07		| 2013-06-07 9:00	| 70		|
			| 2013-06-07 8:11	| 2013-06-07 8:11	| 71		|
			| 2013-06-07 08:12	| 2013-06-07 8:12	| 72		|
			| 2013-06-07 20:13	| 2013-06-07 20:13	| 73		|

		Examples: 'YYYY-MMM-DD' dates (with and without times)
			| date in			| date out			| entry no	|
			| 2013-may-07		| 2013-05-07 9:00	| 74		|
			| 2013-may-07 8:11	| 2013-05-07 8:11	| 75		|
			| 2013-may-07 08:12	| 2013-05-07 8:12	| 76		|
			| 2013-may-07 20:13	| 2013-05-07 20:13	| 77		|

		Examples: Full dates, with written montsh
			| date in		| date out			| entry no	|
			| Feb 5, 2014	| 2014-02-05 9:00	| 78		|
			| Feb 06, 2014	| 2014-02-06 9:00	| 79		|
			| Feb. 7, 2014	| 2014-02-07 9:00	| 80		|
			| Feb. 08, 2014	| 2014-02-08 9:00	| 81		|
			| 9 Feb 2014	| 2014-02-09 9:00	| 82		|
			| 01 Feb 2014	| 2014-02-01 9:00	| 83		|
			| 2 Feb. 2014	| 2014-02-02 9:00	| 84		|
			| 03 Feb. 2014	| 2014-02-03 9:00	| 85		|

		Examples: 'YYYY/MM/DD' dates (with and without times)
			| date in			| date out			| entry no	|
			| 2013/06/07		| 2013-06-07 9:00	| 86		|
			| 2013/06/07 8:11	| 2013-06-07 8:11	| 87		|
			| 2013/06/07 08:12	| 2013-06-07 8:12	| 88		|
			| 2013/06/07 20:13	| 2013-06-07 20:13	| 89		|

		Examples: 'DD/MM/YYYY' dates (with and without times)
			| date in			| date out			| entry no	|
			| 13/06/2007		| 2007-06-13 9:00	| 90		|
			| 13/06/2007 8:11	| 2007-06-13 8:11	| 91		|
			| 13/06/2007 08:12	| 2007-06-13 8:12	| 92		|
			| 13/06/2007 20:13	| 2007-06-13 20:13	| 93		|

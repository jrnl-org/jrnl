
@dates2 @dates @wip
Feature: Processing of (fixed) dates and times

    Scenario Outline: Test all sorts of (fixed) dates
        Given we use the config "empty.json"
        When we run "jrnl <date in>: I saw Elvis <entry no>. He's Alive!"
        Then we should get no error
        Then the journal should contain "<date out> I saw Elvis <entry no>"

        Examples: year
            | date in   | date out          | entry no  |
            | 1998      | 1998-01-01 09:00  | 61        |
            | 2013      | 2013-01-01 09:00  | 62        |
            | 2014      | 2014-01-01 09:00  | 63        |
            | 2015      | 2015-01-01 09:00  | 64        |
            | 2051      | 2051-01-01 09:00  | 65        |

        Examples: year + month
            | date in           | date out          | entry no  |
            | jun 2013          | 2013-06-01 09:00  | 66        |
            | 2013 jul          | 2013-07-01 09:00  | 67        |
            | august 2013       | 2013-08-01 09:00  | 68        |
            | 2013 september    | 2013-09-01 09:00  | 69        |

        Examples: 'YYYY-MM-DD' dates (with and without times)
            | date in           | date out          | entry no  |
            | 2013-06-07        | 2013-06-07 09:00  | 70        |
            | 2013-06-07 8:11   | 2013-06-07 08:11  | 71        |
            | 2013-06-07 08:12  | 2013-06-07 08:12  | 72        |
            | 2013-06-07 20:13  | 2013-06-07 20:13  | 73        |

        Examples: 'YYYY-MMM-DD' dates (with and without times)
            | date in           | date out          | entry no  |
            | 2013-may-07       | 2013-05-07 09:00  | 74        |
            | 2013-may-07 8:11  | 2013-05-07 08:11  | 75        |
            | 2013-may-07 08:12 | 2013-05-07 08:12  | 76        |
            | 2013-may-07 20:13 | 2013-05-07 20:13  | 77        |

        Examples: Full dates, with written montsh
            | date in       | date out          | entry no  |
            | Feb 5, 2014   | 2014-02-05 09:00  | 78        |
            | Feb 06, 2014  | 2014-02-06 09:00  | 79        |
            | Feb. 7, 2014  | 2014-02-07 09:00  | 80        |
            | Feb. 08, 2014 | 2014-02-08 09:00  | 81        |
            | 9 Feb 2014    | 2014-02-09 09:00  | 82        |
            | 01 Feb 2014   | 2014-02-01 09:00  | 83        |
            | 2 Feb. 2014   | 2014-02-02 09:00  | 84        |
            | 03 Feb. 2014  | 2014-02-03 09:00  | 85        |

        Examples: 'YYYY/MM/DD' dates (with and without times)
            | date in           | date out          | entry no  |
            | 2013/06/07        | 2013-06-07 09:00  | 86        |
            | 2013/06/07 8:11   | 2013-06-07 08:11  | 87        |
            | 2013/06/07 08:12  | 2013-06-07 08:12  | 88        |
            | 2013/06/07 20:13  | 2013-06-07 20:13  | 89        |

        Examples: 'DD/MM/YYYY' dates (with and without times)
            | date in           | date out          | entry no  |
            | 13/06/2007        | 2007-06-13 09:00  | 90        |
            | 13/06/2007 8:11   | 2007-06-13 08:11  | 91        |
            | 13/06/2007 08:12  | 2007-06-13 08:12  | 92        |
            | 13/06/2007 20:13  | 2007-06-13 20:13  | 93        |

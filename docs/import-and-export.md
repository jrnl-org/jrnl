<!--
@TODO: Update this for v2.5
-->

## Export to files

You can specify the output file of your exported journal using the
`-o` argument

``` sh
jrnl --format md -o journal.md
```

The above command will generate a file named `journal.md`. If the`-o` argument is a
directory, jrnl will export each entry into an individual file

``` sh
jrnl --format json -o my_entries/
```

The contents of `my\_entries/` will then look like this:

``` output
my_entries/
|- 2013_06_03_a-beautiful-day.json
|- 2013_06_07_dinner-with-gabriel.json
|- ...
```

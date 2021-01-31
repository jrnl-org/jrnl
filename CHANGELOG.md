# Changelog

## [Unreleased](https://github.com/jrnl-org/jrnl/)

[Full Changelog](https://github.com/jrnl-org/jrnl/compare/v2.7...HEAD)

**Implemented enhancements:**

- Allow timestamps in command line for new entries with editor [\#1083](https://github.com/jrnl-org/jrnl/issues/1083)

**Fixed bugs:**

- Make journal selection behavior more consistent when there's a colon with no date [\#1164](https://github.com/jrnl-org/jrnl/pull/1164) ([wren](https://github.com/wren))

**Packaging:**

- Bump keyring from 21.8.0 to 22.0.1 [\#1168](https://github.com/jrnl-org/jrnl/pull/1168) ([dependabot[bot]](https://github.com/apps/dependabot))
- Bump pytest from 6.2.1 to 6.2.2 [\#1167](https://github.com/jrnl-org/jrnl/pull/1167) ([dependabot[bot]](https://github.com/apps/dependabot))

## [v2.7](https://pypi.org/project/jrnl/v2.7/) (2021-01-23)

[Full Changelog](https://github.com/jrnl-org/jrnl/compare/v2.7-beta...v2.7)

**Implemented enhancements:**

- Add new date format \(`--format date`\) for heatmapping [\#1146](https://github.com/jrnl-org/jrnl/pull/1146) ([KarimPwnz](https://github.com/KarimPwnz))
- Add new `-today-in-history`, `-month`, `-day`, and `-year` search filters [\#1145](https://github.com/jrnl-org/jrnl/pull/1145) ([KarimPwnz](https://github.com/KarimPwnz))
- Allow custom extensions when editing \(for easier syntax highlighting\) [\#1139](https://github.com/jrnl-org/jrnl/pull/1139) ([KarimPwnz](https://github.com/KarimPwnz))

**Fixed bugs:**

- Editor can't be launched on Windows when using full path to editor executable [\#1096](https://github.com/jrnl-org/jrnl/issues/1096)
- Fix OS compatibility issues for editors with spaces, slashes, and quotes [\#1153](https://github.com/jrnl-org/jrnl/pull/1153) ([micahellison](https://github.com/micahellison))
- Add delimiters in YAML format [\#1150](https://github.com/jrnl-org/jrnl/pull/1150) ([Seopril](https://github.com/Seopril))
- Fix keyring error handling [\#1138](https://github.com/jrnl-org/jrnl/pull/1138) ([KarimPwnz](https://github.com/KarimPwnz))
- Notify user when config directory can't be created because there is already a file with the same name [\#1134](https://github.com/jrnl-org/jrnl/pull/1134) ([micahellison](https://github.com/micahellison))

**Build:**

- Fix homebrew release, add options for release pipeline [\#1154](https://github.com/jrnl-org/jrnl/pull/1154) ([wren](https://github.com/wren))
- Fix changelog generator [\#1127](https://github.com/jrnl-org/jrnl/pull/1127) ([wren](https://github.com/wren))

**Documentation:**

- add instructions to add VSCode as an external editor for Windows [\#1155](https://github.com/jrnl-org/jrnl/issues/1155)
- Clarify editor documentation for PATH variable and VS Code [\#1160](https://github.com/jrnl-org/jrnl/pull/1160) ([micahellison](https://github.com/micahellison))
- Emphasize installing dependencies before testing [\#1148](https://github.com/jrnl-org/jrnl/pull/1148) ([gumatias](https://github.com/gumatias))
- Clarify installation documentation \(\#1097\) [\#1137](https://github.com/jrnl-org/jrnl/pull/1137) ([Seopril](https://github.com/Seopril))
- Fix broken search bar in docs site [\#1135](https://github.com/jrnl-org/jrnl/pull/1135) ([wren](https://github.com/wren))
- Fix search on docs site [\#1133](https://github.com/jrnl-org/jrnl/pull/1133) ([wren](https://github.com/wren))
- Add packaging label to changelog generator config [\#1132](https://github.com/jrnl-org/jrnl/pull/1132) ([wren](https://github.com/wren))
- Fix failing contrast test in accessibility tools on docs site [\#1126](https://github.com/jrnl-org/jrnl/pull/1126) ([wren](https://github.com/wren))

**Packaging:**

- Bump pyyaml from 5.3.1 to 5.4.1 [\#1158](https://github.com/jrnl-org/jrnl/pull/1158) ([dependabot[bot]](https://github.com/apps/dependabot))
- Bump keyring from 21.7.0 to 21.8.0 [\#1136](https://github.com/jrnl-org/jrnl/pull/1136) ([dependabot[bot]](https://github.com/apps/dependabot))
- Bump pytz from 2020.4 to 2020.5 [\#1130](https://github.com/jrnl-org/jrnl/pull/1130) ([dependabot-preview[bot]](https://github.com/apps/dependabot-preview))
- Bump pytest from 6.2.0 to 6.2.1 [\#1129](https://github.com/jrnl-org/jrnl/pull/1129) ([dependabot-preview[bot]](https://github.com/apps/dependabot-preview))
- Bump keyring from 21.5.0 to 21.7.0 [\#1128](https://github.com/jrnl-org/jrnl/pull/1128) ([dependabot-preview[bot]](https://github.com/apps/dependabot-preview))

## [v2.6](https://pypi.org/project/jrnl/v2.6/) (2020-12-20)

[Full Changelog](https://github.com/jrnl-org/jrnl/compare/v2.5...v2.6)

**Implemented enhancements:**

- Add ability to put --edit partly through a cli entry to move it to the editor [\#1091](https://github.com/jrnl-org/jrnl/pull/1091) ([wren](https://github.com/wren))
- Allow --edit flag partway through an entry [\#906](https://github.com/jrnl-org/jrnl/issues/906)

**Fixed bugs:**

- Check for readline module instead of Windows when initializing autocomplete in install [\#1104](https://github.com/jrnl-org/jrnl/pull/1104) ([micahellison](https://github.com/micahellison))
- Directory export crashes in Windows with certain characters - UnicodeEncodeError: 'locale' codec can't encode character [\#1089](https://github.com/jrnl-org/jrnl/issues/1089)
- Fix Unicode encoding failure in directory export when creating filenames from journal titles with certain characters [\#1090](https://github.com/jrnl-org/jrnl/pull/1090) ([micahellison](https://github.com/micahellison))
- Typo fix in output.py: "us" -\> "use" [\#1117](https://github.com/jrnl-org/jrnl/pull/1117) ([signal-9](https://github.com/signal-9))

**Build:**

- Add a release workflow for PyPI in CI \(Github Actions\) [\#1095](https://github.com/jrnl-org/jrnl/pull/1095) ([wren](https://github.com/wren))
- Add automatic deployment for homebrew releases \(and prereleases\) [\#1111](https://github.com/jrnl-org/jrnl/pull/1111) ([wren](https://github.com/wren))
- Add changelog generation workflow to github actions [\#1086](https://github.com/jrnl-org/jrnl/pull/1086) ([wren](https://github.com/wren))
- Add fix for changelog conditional always returning false [\#1101](https://github.com/jrnl-org/jrnl/pull/1101) ([wren](https://github.com/wren))
- Change approach for docs workflow to use pa11y-ci [\#1116](https://github.com/jrnl-org/jrnl/pull/1116) ([wren](https://github.com/wren))
- Changelog fixes [\#1088](https://github.com/jrnl-org/jrnl/pull/1088) ([wren](https://github.com/wren))
- Fix trigger for changelog [\#1114](https://github.com/jrnl-org/jrnl/pull/1114) ([wren](https://github.com/wren))
- Make changelog auto exclude stale and wontfix issues [\#1081](https://github.com/jrnl-org/jrnl/pull/1081) ([wren](https://github.com/wren))
- Migrate to Github Actions from Travis CI [\#1060](https://github.com/jrnl-org/jrnl/issues/1060)
- More changelog fixes [\#1092](https://github.com/jrnl-org/jrnl/pull/1092) ([wren](https://github.com/wren))
- Standardize version regex in release pipeline [\#1124](https://github.com/jrnl-org/jrnl/pull/1124) ([wren](https://github.com/wren))
- Udpate build badge in readme to point at github instead of travis [\#1094](https://github.com/jrnl-org/jrnl/pull/1094) ([wren](https://github.com/wren))
- Update all dependencies and lock file [\#1110](https://github.com/jrnl-org/jrnl/pull/1110) ([wren](https://github.com/wren))
- get rid of travis and circle configs \(in favor of github actions\) [\#1082](https://github.com/jrnl-org/jrnl/pull/1082) ([wren](https://github.com/wren))

**Documentation:**

- Add visual header to readme [\#1085](https://github.com/jrnl-org/jrnl/pull/1085) ([wren](https://github.com/wren))
- Comply with GPL by acknowledging all authors and including license info in each source file [\#1121](https://github.com/jrnl-org/jrnl/pull/1121) ([micahellison](https://github.com/micahellison))
- Fix lone closing parenthesis [\#1118](https://github.com/jrnl-org/jrnl/pull/1118) ([maebert](https://github.com/maebert))
- Make docs site \(jrnl.sh\) fully meet Web Content Accessibility Guidelines \(WCAG\) 2.1 [\#1105](https://github.com/jrnl-org/jrnl/pull/1105) ([wren](https://github.com/wren))
- Small accessibility fixes for docs site [\#1122](https://github.com/jrnl-org/jrnl/pull/1122) ([wren](https://github.com/wren))

## [v2.5](https://pypi.org/project/jrnl/v2.5/) (2020-11-07)

[Full Changelog](https://github.com/jrnl-org/jrnl/compare/v2.4.5...v2.5)

**Implemented enhancements:**

- 🚨 Deprecate Python 3.6 🚨 [\#992](https://github.com/jrnl-org/jrnl/issues/992)
- Add support for Python 3.9 [\#1017](https://github.com/jrnl-org/jrnl/issues/1017)
- Implement arg parsing library [\#866](https://github.com/jrnl-org/jrnl/issues/866)
- Rename `--export` to `--format` and `--export -o` to `--format --file`  [\#814](https://github.com/jrnl-org/jrnl/issues/814)
- Pull functionality out of util.py [\#737](https://github.com/jrnl-org/jrnl/issues/737)
- Support -not for individual @tag in the command line [\#374](https://github.com/jrnl-org/jrnl/issues/374)
- Add punctuation more commonly used in Asian languages \(ellipsis\) to sentence parsing [\#1044](https://github.com/jrnl-org/jrnl/pull/1044) ([felixonmars](https://github.com/felixonmars))
- Clean up help screen, get rid of util.py [\#1027](https://github.com/jrnl-org/jrnl/pull/1027) ([wren](https://github.com/wren))

**Fixed bugs:**

- Extra error when writing empty entry [\#1048](https://github.com/jrnl-org/jrnl/issues/1048)
- 'Edit on Github' Button in Documentation not working [\#1039](https://github.com/jrnl-org/jrnl/issues/1039)
- Decrypt jrnl file in dropbox on another machine fails  [\#1019](https://github.com/jrnl-org/jrnl/issues/1019)
- Listing jrnl entries by tag for non default journal seem to not work as expected. [\#875](https://github.com/jrnl-org/jrnl/issues/875)
- -and parameter seems to only work for the default journal [\#520](https://github.com/jrnl-org/jrnl/issues/520)
- Disable logging by default [\#1053](https://github.com/jrnl-org/jrnl/pull/1053) ([wren](https://github.com/wren))
- Partial refactor of cli.py \(mainly help screen and arg parsing\) [\#991](https://github.com/jrnl-org/jrnl/pull/991) ([wren](https://github.com/wren))

**Build:**

- Add accessibility testing for docs site \(https://jrnl.sh) [\#1067](https://github.com/jrnl-org/jrnl/pull/1067) ([wren](https://github.com/wren))
- Add circle ci config file for linux tests [\#1063](https://github.com/jrnl-org/jrnl/pull/1063) ([wren](https://github.com/wren))
- Lots of test refactoring [\#1042](https://github.com/jrnl-org/jrnl/pull/1042) ([wren](https://github.com/wren))
- Add support for Python 3.9 build testing [\#1018](https://github.com/jrnl-org/jrnl/pull/1018) ([micahellison](https://github.com/micahellison))
- Resolve Travis/Windows/pip issues with upgrade to cryptography 3.0 [\#1016](https://github.com/jrnl-org/jrnl/pull/1016) ([micahellison](https://github.com/micahellison))

**Updated documentation:**

- Clarify usage output between export and reading sections [\#344](https://github.com/jrnl-org/jrnl/issues/344)
- Fix "Edit on GitHub" button on docs site [\#1043](https://github.com/jrnl-org/jrnl/pull/1043) ([matildepark](https://github.com/matildepark))
- Correct typos in CONTRIBUTING.md [\#1040](https://github.com/jrnl-org/jrnl/pull/1040) ([felixonmars](https://github.com/felixonmars))
- Change styling of terminal on docs site, small copy changes [\#1038](https://github.com/jrnl-org/jrnl/pull/1038) ([wren](https://github.com/wren))
- Documentation updates [\#1032](https://github.com/jrnl-org/jrnl/pull/1032) ([micahellison](https://github.com/micahellison))
- Updated advanced.md in docs to reflect all four subkeys under colors … [\#1023](https://github.com/jrnl-org/jrnl/pull/1023) ([DacodaNelson](https://github.com/DacodaNelson))
- Update github issue templates to use new diagnostic command [\#1022](https://github.com/jrnl-org/jrnl/pull/1022) ([wren](https://github.com/wren))

## [v2.4.5](https://pypi.org/project/jrnl/v2.4.5/) (2020-07-31)

[Full Changelog](https://github.com/jrnl-org/jrnl/compare/v2.4.4...v2.4.5)

**Fixed bugs:**

- Add missing dependency \(packaging\) [\#1011](https://github.com/jrnl-org/jrnl/pull/1011) ([wren](https://github.com/wren))

## [v2.4.4](https://pypi.org/project/jrnl/v2.4.4/) (2020-07-25)

[Full Changelog](https://github.com/jrnl-org/jrnl/compare/v2.4.4...v2.4.3)

**Implemented enhancements:**

- Add --diagnostic argument [\#984](https://github.com/jrnl-org/jrnl/pull/984) ([micahellison](https://github.com/micahellison))
- Add tags to json and xml exporters [\#975](https://github.com/jrnl-org/jrnl/pull/975) ([eshrh](https://github.com/eshrh))
- Add extended metadata support for DayOne Classic [\#928](https://github.com/jrnl-org/jrnl/pull/928) ([MinchinWeb](https://github.com/MinchinWeb))

**Fixed bugs:**

- Allow editing of DayOne entries [\#1001](https://github.com/jrnl-org/jrnl/pull/1001) ([minchinweb](https://github.com/minchinweb), [micahellison](https://github.com/micahellison), [wren](https://github.com/wren))
- Create journal with absolute path when no path is specified [\#972](https://github.com/jrnl-org/jrnl/pull/972) ([eshrh](https://github.com/eshrh))

**Build:**

- Add unit testing via pytest [\#987](https://github.com/jrnl-org/jrnl/pull/987) ([micahellison](https://github.com/micahellison))
- Rename master branch to release [\#985](https://github.com/jrnl-org/jrnl/pull/985) ([wren](https://github.com/wren))

**Updated documentation:**

- Fix readme link to submit an issue [\#1002](https://github.com/jrnl-org/jrnl/pull/1002) ([wren](https://github.com/wren))
- Extensive modifications to overview.md [\#957](https://github.com/jrnl-org/jrnl/pull/957) ([guydebros](https://github.com/guydebros))

## [v2.4.3](https://pypi.org/project/jrnl/v2.4.3/) (2020-06-13)

[Full Changelog](https://github.com/jrnl-org/jrnl/compare/v2.4.2...v2.4.3)

**Implemented enhancements:**

- Speed up jrnl by 10%, improve slow imports [\#959](https://github.com/jrnl-org/jrnl/pull/959) ([wotgl](https://github.com/wotgl))

**Fixed bugs:**

- Fix set\_keychain errors [\#964](https://github.com/jrnl-org/jrnl/pull/964) ([eshrh](https://github.com/eshrh))
- Fix title splitting logic to account for both newlines and periods [\#958](https://github.com/jrnl-org/jrnl/pull/958) ([eshrh](https://github.com/eshrh))
- Fix editor config when an argument with a space is used [\#953](https://github.com/jrnl-org/jrnl/pull/953) ([wren](https://github.com/wren))
- Ask for password before adding entry instead of after [\#951](https://github.com/jrnl-org/jrnl/pull/951) ([ollybritton](https://github.com/ollybritton))
- Fix duplicate text in multiple tag search [\#948](https://github.com/jrnl-org/jrnl/pull/948) ([micahellison](https://github.com/micahellison))

**Build:**

- Fix for hanging Windows tests on Travis [\#969](https://github.com/jrnl-org/jrnl/pull/969) ([wren](https://github.com/wren))
- Ensure test data is always checked out with LF line endings [\#965](https://github.com/jrnl-org/jrnl/pull/965) ([micahellison](https://github.com/micahellison))
- Clean up templates and issues [\#954](https://github.com/jrnl-org/jrnl/pull/954) ([wren](https://github.com/wren))
- Update lockbot comment to encourage linking to issue [\#941](https://github.com/jrnl-org/jrnl/pull/941) ([MinchinWeb](https://github.com/MinchinWeb))

**Updated documentation:**

- Cleaned up usage.md for clarity, formatting, and grammar. [\#956](https://github.com/jrnl-org/jrnl/pull/956) ([guydebros](https://github.com/guydebros))

## [v2.4.2](https://pypi.org/project/jrnl/v2.4.2/) (2020-05-09)

[Full Changelog](https://github.com/jrnl-org/jrnl/compare/v2.4.1...v2.4.2)

**Fixed bugs:**

- Prevent filtered delete from deleting journal [\#935](https://github.com/jrnl-org/jrnl/pull/935) ([micahellison](https://github.com/micahellison))

**Build:**

- Make sure testing cleans up after itself [\#940](https://github.com/jrnl-org/jrnl/pull/940) ([wren](https://github.com/wren))
- Allow most recent pytz version and update dependencies [\#937](https://github.com/jrnl-org/jrnl/pull/937) ([micahellison](https://github.com/micahellison))
- Use gitlab to trigger releases in pipeline [\#947](https://github.com/jrnl-org/jrnl/pull/947) ([wren](https://github.com/wren))

**Updated documentation:**

- Change jrnl.sh GitHub new issue link to issue template chooser [\#936](https://github.com/jrnl-org/jrnl/pull/936) ([micahellison](https://github.com/micahellison))
- Improve privacy, security, and encryption documentation \#896 [\#925](https://github.com/jrnl-org/jrnl/pull/925) ([micahellison](https://github.com/micahellison))

## [v2.4.1](https://pypi.org/project/jrnl/v2.4.1/) (2020-05-02)

[Full Changelog](https://github.com/jrnl-org/jrnl/compare/v2.4...v2.4.1)

**Fixed bugs:**

- Disable --delete due to critical bug [\#934](https://github.com/jrnl-org/jrnl/pull/934) ([wren](https://github.com/wren))

## [v2.4](https://pypi.org/project/jrnl/v2.4/) (2020-04-25)

[Full Changelog](https://github.com/jrnl-org/jrnl/compare/v2.3.1...v2.4)

**Implemented enhancements:**

- Update keyring version from "^19.0" to "\>19.0, \<22.0" [\#914](https://github.com/jrnl-org/jrnl/pull/914) ([micahellison](https://github.com/micahellison))
- Allow tzlocal version \>1.5 \<3.0 instead of \>1.5 \<2.0 [\#900](https://github.com/jrnl-org/jrnl/pull/900) ([micahellison](https://github.com/micahellison))
- Interactive delete [\#650](https://github.com/jrnl-org/jrnl/pull/850) ([alichtman](https://github.com/alichtman))
- Upgrade license to GPLv3 [\#918](https://github.com/jrnl-org/jrnl/pull/918) ([wren](https://github.com/wren), [micahellison](https://github.com/micahellison))

**Fixed bugs:**

- Fix Python 3.9 incompatibility by updating plistlib [\#909](https://github.com/jrnl-org/jrnl/pull/909) ([MinchinWeb](https://github.com/MinchinWeb))
- Ensure exported entries end in a newline for Markdown and YAML exporters [\#908](https://github.com/jrnl-org/jrnl/pull/908) ([MinchinWeb](https://github.com/MinchinWeb))
- Fix typo in YAML exporter \("stared" -\> "starred"\) [\#907](https://github.com/jrnl-org/jrnl/pull/907) ([MinchinWeb](https://github.com/MinchinWeb))
- Fix for upgrade with missing journal [\#796](https://github.com/jrnl-org/jrnl/pull/796) ([dbxnr](https://github.com/dbxnr))

**Build:**

- Update Python versions in pipeline [\#910](https://github.com/jrnl-org/jrnl/pull/910) ([MinchinWeb](https://github.com/MinchinWeb))
- Update Poetry requirements for testing latest Python version [\#898](https://github.com/jrnl-org/jrnl/pull/898) ([wren](https://github.com/wren))
- Update makefile to match pipeline better [\#919](https://github.com/jrnl-org/jrnl/pull/919) ([wren](https://github.com/wren))

**Updated documentation:**

- Update the code of conduct [\#913](https://github.com/jrnl-org/jrnl/pull/913) ([wren](https://github.com/wren))
- Update twitter buttons, contribution in footer [\#905](https://github.com/jrnl-org/jrnl/pull/905) ([wren](https://github.com/wren))
- Change install doc guideline from pip to pipx [\#904](https://github.com/jrnl-org/jrnl/pull/904) ([micahellison](https://github.com/micahellison))
- Update twitter buttons, contribution in footer [\#905](https://github.com/jrnl-org/jrnl/pull/905) ([wren](https://github.com/wren))
- Clean up readme file [\#924](https://github.com/jrnl-org/jrnl/pull/924) ([wren](https://github.com/wren))
- Clarify that editing config isn't always destructive [\#923](https://github.com/jrnl-org/jrnl/pull/923) ([Epskampie](https://github.com/Epskampie))

## [v2.3](https://pypi.org/project/jrnl/v2.3/) (2020-03-21)

[Full Changelog](https://github.com/jrnl-org/jrnl/compare/v2.2...v2.3)

**Implemented enhancements:**

- Update YAML exporter to handle Dayone format [\#773](https://github.com/jrnl-org/jrnl/pull/773) ([MinchinWeb](https://github.com/MinchinWeb))
- Pretty print journal entries (add color) [\#692](https://github.com/jrnl-org/jrnl/pull/692) ([alichtman](https://github.com/alichtman))
- Allow journals to be saved into multiple files in a directory structure [\#485](https://github.com/jrnl-org/jrnl/pull/485) ([notbalanced](https://github.com/notbalanced))

**Fixed bugs:**

- Listing all entries in DayOne Classic journal throws IndexError [\#786](https://github.com/jrnl-org/jrnl/pull/786) ([MinchinWeb](https://github.com/MinchinWeb))
- Add UTC support for failing DayOne tests [\#785](https://github.com/jrnl-org/jrnl/pull/785) ([MinchinWeb](https://github.com/MinchinWeb))

**Build:**

- Stop multiple changelog generators from crashing into each other [\#845](https://github.com/jrnl-org/jrnl/pull/845) ([wren](https://github.com/wren))
- Don't re-run tests on deployment [\#839](https://github.com/jrnl-org/jrnl/pull/839) ([wren](https://github.com/wren))
- Put back build lines in Poetry config [\#838](https://github.com/jrnl-org/jrnl/pull/838) ([wren](https://github.com/wren))
- Restore emoji test [\#837](https://github.com/jrnl-org/jrnl/pull/837) ([micahellison](https://github.com/micahellison))
- Fix crashing unicode Travis tests on Windows and fail build if Windows tests fail [\#836](https://github.com/jrnl-org/jrnl/pull/836) ([micahellison](https://github.com/micahellison))
- Remove poetry from build system in pyproject config to fix `brew install` [\#830](https://github.com/jrnl-org/jrnl/pull/830) ([wren](https://github.com/wren))
- Fix all skipped tests on Travis Windows builds by preserving newlines [\#823](https://github.com/jrnl-org/jrnl/pull/823) ([micahellison](https://github.com/micahellison))

**Updated documentation:**

- Update url for "beautiful timeline" in export.md [\#879](https://github.com/jrnl-org/jrnl/pull/879) ([NGenetzky](https://github.com/NGenetzky))
- Docs: Fix broken links in recipes.md [\#854](https://github.com/jrnl-org/jrnl/pull/854) ([lrvl](https://github.com/lrvl))
- Fix configuration slashes and indentation in advanced usage documentation [\#852](https://github.com/jrnl-org/jrnl/pull/852) ([aallbrig](https://github.com/aallbrig))
- Fix fish history instructions. [\#846](https://github.com/jrnl-org/jrnl/pull/846) ([aureooms](https://github.com/aureooms))
- Update site description [\#841](https://github.com/jrnl-org/jrnl/pull/841) ([wren](https://github.com/wren))
- Get rid of dumb sex joke [\#840](https://github.com/jrnl-org/jrnl/pull/840) ([wren](https://github.com/wren))
- Updating/clarifying template explanation [\#829](https://github.com/jrnl-org/jrnl/pull/829) ([heymajor](https://github.com/heymajor))

## [v2.2](https://pypi.org/project/jrnl/v2.2/) (2020-02-01)

[Full Changelog](https://github.com/jrnl-org/jrnl/compare/v2.1.1...v2.2)

**Implemented enhancements:**

- Full text search \(case insensitive\) with "-contains" [\#740](https://github.com/jrnl-org/jrnl/pull/740) ([empireshades](https://github.com/empireshades))
- Reduce startup time by 55% [\#719](https://github.com/jrnl-org/jrnl/pull/719) ([maebert](https://github.com/maebert))
- Refactor password logic to prevent accidental password leakage [\#708](https://github.com/jrnl-org/jrnl/pull/708) ([pspeter](https://github.com/pspeter))
- Password confirmation [\#706](https://github.com/jrnl-org/jrnl/pull/706) ([pspeter](https://github.com/pspeter))

**Fixed bugs:**

- Close temp file before passing it to editor to prevent file locking issues in Windows [\#792](https://github.com/jrnl-org/jrnl/pull/792) ([micahellison](https://github.com/micahellison))
- Fix crash while encrypting a journal on first run without saving password [\#789](https://github.com/jrnl-org/jrnl/pull/789) ([dbxnr](https://github.com/dbxnr))

**Build:**

- Fix issue where jrnl would always out 'source' for version, fix Poetry config to build and publish properly [\#820](https://github.com/jrnl-org/jrnl/pull/820) ([wren](https://github.com/wren))
- Unpin poetry [\#808](https://github.com/jrnl-org/jrnl/pull/808) ([wren](https://github.com/wren))
- Fix all skipped tests on Travis Windows builds by preserving newlines [\#823](https://github.com/jrnl-org/jrnl/pull/823) ([micahellison](https://github.com/micahellison))
- Change PyPI auth method in build pipeline [\#807](https://github.com/jrnl-org/jrnl/pull/807) ([wren](https://github.com/wren))
- Automagically update the changelog you see before your very eyes! [\#806](https://github.com/jrnl-org/jrnl/pull/806) ([wren](https://github.com/wren))
- Update Black version and lock file to fix builds on develop branch [\#784](https://github.com/jrnl-org/jrnl/pull/784) ([wren](https://github.com/wren))
- Run black formatter on codebase for standardization [\#778](https://github.com/jrnl-org/jrnl/pull/778) ([wren](https://github.com/wren))
- Skip Broken Windows Tests [\#772](https://github.com/jrnl-org/jrnl/pull/772) ([wren](https://github.com/wren))
- Black Formatter [\#769](https://github.com/jrnl-org/jrnl/pull/769) ([MinchinWeb](https://github.com/MinchinWeb))
- Update lock file and testing suite for Python 3.8 [\#765](https://github.com/jrnl-org/jrnl/pull/765) ([wren](https://github.com/wren))
- Fix CI config to only deploy once [\#761](https://github.com/jrnl-org/jrnl/pull/761) ([wren](https://github.com/wren))
- More Travis-CI Testing [\#759](https://github.com/jrnl-org/jrnl/pull/759) ([MinchinWeb](https://github.com/MinchinWeb))

**Updated documentation:**

- Explain how fish can be configured to exclude jrnl commands from history by default [\#809](https://github.com/jrnl-org/jrnl/pull/809) ([aureooms](https://github.com/aureooms))
- Remove merge marker in recipes.md [\#782](https://github.com/jrnl-org/jrnl/pull/782) ([markphelps](https://github.com/markphelps))
- Fix merge conflict left-over [\#767](https://github.com/jrnl-org/jrnl/pull/767) ([thejspr](https://github.com/thejspr))
- Display header in docs on mobile devices [\#763](https://github.com/jrnl-org/jrnl/pull/763) ([maebert](https://github.com/maebert))

## [v2.1.1](https://pypi.org/project/jrnl/v2.1.1/) (2019-11-26)

[Full Changelog](https://github.com/jrnl-org/jrnl/compare/v2.1.post2...v2.1.1)

**Implemented enhancements:**

- Support Python 3.6+ [\#710](https://github.com/jrnl-org/jrnl/pull/710) ([pspeter](https://github.com/pspeter))
- Drop Python 2 support, add mocks in tests [\#705](https://github.com/jrnl-org/jrnl/pull/705) ([pspeter](https://github.com/pspeter))

**Fixed bugs:**

- Prevent readline usage on Windows, which was causing Active Python crashes on install [\#751](https://github.com/jrnl-org/jrnl/pull/751) ([micahellison](https://github.com/micahellison))
- Exit jrnl if no text entered into editor [\#744](https://github.com/jrnl-org/jrnl/pull/744) ([alichtman](https://github.com/alichtman))
- Fix crash when no keyring backend available [\#699](https://github.com/jrnl-org/jrnl/pull/699) ([pspeter](https://github.com/pspeter))
- Fix parsing Journals using a little-endian date format [\#694](https://github.com/jrnl-org/jrnl/pull/694) ([pspeter](https://github.com/pspeter))

**Updated documentation:**

- Update developer documentation [\#752](https://github.com/jrnl-org/jrnl/pull/752) ([micahellison](https://github.com/micahellison))
- Create templates for issues and pull requests [\#679](https://github.com/jrnl-org/jrnl/pull/679) ([C0DK](https://github.com/C0DK))
- Smaller doc fixes [\#649](https://github.com/jrnl-org/jrnl/pull/649) ([maebert](https://github.com/maebert))
- Move to mkdocs [\#611](https://github.com/jrnl-org/jrnl/pull/611) ([maebert](https://github.com/maebert))

## [v2.1.post2](https://pypi.org/project/jrnl/v2.1.post2/) (2019-11-11)

[Full Changelog](https://github.com/jrnl-org/jrnl/compare/v2.0.1...v2.1.post2)

**Fixed bugs:**

- Expand paths that use ~ to full path [\#704](https://github.com/jrnl-org/jrnl/pull/704) ([MinchinWeb](https://github.com/MinchinWeb))

**Build:**

- Separate local dev from pipeline releases [\#684](https://github.com/jrnl-org/jrnl/pull/684) ([wren](https://github.com/wren))
- Update version handling in source and travis deployments [\#683](https://github.com/jrnl-org/jrnl/pull/683) ([wren](https://github.com/wren))
- Use Poetry for dependency management and deployments [\#612](https://github.com/jrnl-org/jrnl/pull/612) ([maebert](https://github.com/maebert))

**Updated documentation:**

- Fix typos, spelling [\#734](https://github.com/jrnl-org/jrnl/pull/734) ([MinchinWeb](https://github.com/MinchinWeb))

## [v2.0.1](https://pypi.org/project/jrnl/v2.0.1/) (2019-09-26)

[Full Changelog](https://github.com/jrnl-org/jrnl/compare/v2.0.0...v2.0.1)

**Implemented enhancements:**

- Switch to hashmark Markdown headers on export \(Mk II\) [\#639](https://github.com/jrnl-org/jrnl/pull/639) ([MinchinWeb](https://github.com/MinchinWeb))
- Add '-not' flag for excluding tags from filter [\#637](https://github.com/jrnl-org/jrnl/pull/637) ([jprof](https://github.com/jprof))
- Handle KeyboardInterrupt when installing journal [\#550](https://github.com/jrnl-org/jrnl/pull/550) ([silenc3r](https://github.com/silenc3r))

**Fixed bugs:**

- Change pyYAML required version [\#660](https://github.com/jrnl-org/jrnl/pull/660) ([etnnth](https://github.com/etnnth))

**Updated documentation:**

- Fix references to Sphinx in CONTRIBUTING.md [\#655](https://github.com/jrnl-org/jrnl/pull/655) ([maebert](https://github.com/maebert))

## [v2.0.0](https://pypi.org/project/jrnl/v2.0.0/) (2019-08-24)

[Full Changelog](https://github.com/jrnl-org/jrnl/compare/1.9.8...v2.0.0)

🚨 **BREAKING CHANGES** 🚨

**Implemented enhancements:**
- Change cryptographic backend from PyCrypto to cryptography.io
- Config now respects XDG conventions and may move accordingly
- Config name changed from `journals.jrnl_name.journal` to `journals.jrnl_name.path`

**Fixed bugs:**

- Confirm that each journal can be parsed during upgrade, and abort upgrade if not [\#650](https://github.com/jrnl-org/jrnl/pull/650) ([micahellison](https://github.com/micahellison))
- Escape dates in square brackets [\#644](https://github.com/jrnl-org/jrnl/pull/644) ([wren](https://github.com/wren))
- Create encrypted journal [\#641](https://github.com/jrnl-org/jrnl/pull/641) ([gregorybodnar](https://github.com/gregorybodnar))
- Resolve issues around unreadable dates to allow markdown footnotes and prevent accidental deletion [\#623](https://github.com/jrnl-org/jrnl/pull/623) ([micahellison](https://github.com/micahellison))
- Update crypto module \#610 [\#621](https://github.com/jrnl-org/jrnl/pull/621) ([wren](https://github.com/wren))
- Fix issue \#584 YAMLLoadWarning [\#585](https://github.com/jrnl-org/jrnl/pull/585) ([wren](https://github.com/wren))

**Deprecated:**

- Deprecate Python 2 [\#624](https://github.com/jrnl-org/jrnl/pull/624) ([micahellison](https://github.com/micahellison))
- Config now saved as YAML (no more JSON)

**Build:**

- change pinned label to a super cool emoji ⭐️ [\#646](https://github.com/jrnl-org/jrnl/pull/646) ([wren](https://github.com/wren))
- Update Travis build badge and restore pypi badges [\#603](https://github.com/jrnl-org/jrnl/pull/603) ([micahellison](https://github.com/micahellison))

**Updated documentation:**

- Mention lack of Day One support and relevant history in readme [\#608](https://github.com/jrnl-org/jrnl/pull/608) ([micahellison](https://github.com/micahellison))
- Add a code of conduct file \(rather than adding to contributing\) [\#604](https://github.com/jrnl-org/jrnl/pull/604) ([wren](https://github.com/wren))
- Update docs to reflect merging jrnl-plus fork back upstream [\#601](https://github.com/jrnl-org/jrnl/pull/601) ([micahellison](https://github.com/micahellison))
- Add instructions for VS Code [\#544](https://github.com/jrnl-org/jrnl/pull/544) ([emceeaich](https://github.com/emceeaich))

## v1.9 (2014-07-21)

* __1.9.5__ Multi-word tags for DayOne Journals
* __1.9.4__ Fixed: Order of journal entries in file correct after --edit'ing
* __1.9.3__ Fixed: Tags at the beginning of lines
* __1.9.2__ Fixed: Tag search ignores email-addresses (thanks to @mjhoffman65)
* __1.9.1__ Fixed: Dates in the future can be parsed as well.
* __1.9.0__ Improved: Greatly improved date parsing. Also added an `-on` option for filtering

## v1.8 (2014-05-22)

* __1.8.7__ Fixed: -from and -to filters are inclusive (thanks to @grplyler)
* __1.8.6__ Improved: Tags like @C++ and @OS/2 work, too (thanks to @chaitan94)
* __1.8.5__ Fixed: file names when exporting to individual files contain full year (thanks to @jdevera)
* __1.8.4__ Improved: using external editors (thanks to @chrissexton)
* __1.8.3__ Fixed: export to text files and improves help (thanks to @igniteflow and @mpe)
* __1.8.2__ Better integration with environment variables (thanks to @ajaam and @matze)
* __1.8.1__ Minor bug fixes
* __1.8.0__ Official support for python 3.4

## v1.7 (2013-12-22)

* __1.7.22__ Fixed an issue with writing files when exporting entries containing non-ascii characters.
* __1.7.21__ jrnl now uses PKCS#7 padding.
* __1.7.20__ Minor fixes when parsing DayOne journals
* __1.7.19__ Creates full path to journal during installation if it doesn't exist yet
* __1.7.18__ Small update to parsing regex
* __1.7.17__ Fixes writing new lines between entries
* __1.7.16__ Even more unicode fixes!
* __1.7.15__ More unicode fixes
* __1.7.14__ Fix for trailing whitespaces (eg. when writing markdown code block)
* __1.7.13__ Fix for UTF-8 in DayOne journals
* __1.7.12__ Fixes a bug where filtering by tags didn't work for DayOne journals
* __1.7.11__ `-ls` will list all available journals (Thanks @jtan189)
* __1.7.10__ Supports `-3` as a shortcut for `-n 3` and updates to tzlocal 1.1
* __1.7.9__ Fix a logic bug so that jrnl -h and jrnl -v are possible even if jrnl not configured yet.
* __1.7.8__ Upgrade to parsedatetime 1.2
* __1.7.7__ Cleaned up imports, better unicode support
* __1.7.6__ Python 3 port for slugify
* __1.7.5__ Colorama is only needed on Windows. Smaller fixes
* __1.7.3__ Touches temporary files before opening them to allow more external editors.
* __1.7.2__ Dateutil added to requirements.
* __1.7.1__ Fixes issues with parsing time information in entries.
* __1.7.0__ Edit encrypted or DayOne journals with `jrnl --edit`.


## v1.6 (2013-11-05)

* __1.6.6__ -v prints the current version, also better strings for windows users. Furthermore, jrnl/jrnl.py moved to jrnl/cli.py
* __1.6.5__ Allows composing multi-line entries on the command line or importing files
* __1.6.4__ Fixed a bug that caused creating encrypted journals to fail
* __1.6.3__ New, pretty, _useful_ documentation!
* __1.6.2__ Starring entries now works for plain-text journals too!
* __1.6.1__ Attempts to fix broken config files automatically
* __1.6.0__ Passwords are now saved in the key-chain. The `password` field in `.jrnl_config` is soft-deprecated.

## v1.5 (2013-08-06)

* __1.5.7__ The `~` in journal config paths will now expand properly to e.g. `/Users/maebert`
* __1.5.6__ Fixed: Fixed a bug where on OS X, the timezone could only be accessed on administrator accounts.
* __1.5.5__ Fixed: Detects DayOne journals stored in `~/Library/Mobile Data` as well.
* __1.5.4__ DayOne journals can now handle tags
* __1.5.3__ Fixed: DayOne integration with older DayOne Journals
* __1.5.2__ Soft-deprecated `-to` for filtering by time and introduces `-until` instead.
* __1.5.1__ Fixed: Fixed a bug introduced in 1.5.0 that caused the entire journal to be printed after composing an entry
* __1.5.0__ Exporting, encrypting and displaying tags now takes your filter options into account. So you could export everything before May 2012: `jrnl -to 'may 2012' --export json`. Or encrypt all entries tagged with `@work` into a new journal: `jrnl @work --encrypt work_journal.txt`. Or display all tags of posts where Bob is also tagged: `jrnl @bob --tags`

## v1.4 (2013-07-22)

* __1.4.2__ Fixed: Tagging works again
* __1.4.0__ Unifies encryption between Python 2 and 3. If you have problems reading encrypted journals afterwards, first decrypt your journal with the __old__ jrnl version (install with `pip install jrnl==1.3.1`, then `jrnl --decrypt`), upgrade jrnl (`pip install jrnl --upgrade`) and encrypt it again (`jrnl --encrypt`).

## v1.3 (2013-07-17)

* __1.3.2__ Everything that is not direct output of jrnl will be written stderr to improve integration
* __1.3.0__ Export to multiple files
* __1.3.0__ Feature to export to given output file

## v1.2 (2013-07-15)

* __1.2.0__ Fixed: Timezone support for DayOne


## v1.1 (2013-06-09)

* __1.1.1__ Fixed: Unicode and Python3 issues resolved.
* __1.1.0__
    * JSON export exports tags as well.
    * Nicer error message when there is a syntactical error in your config file.
    * Unicode support

## v1.0 (2013-03-04)

* __1.0.5__ Backwards compatibility with `parsedatetime` 0.8.7
* __1.0.4__
    * Python 2.6 compatibility
    * Better utf-8 support
    * Python 3 compatibility
    * Respects the `XDG_CONFIG_HOME` environment variable for storing your configuration file (Thanks [evaryont](https://github.com/evaryont))

* __1.0.3__
    * Removed clint in favour of colorama
    * Fixed: Fixed a bug where showing tags failed when no tags are defined.
    * Fixed: Improvements to config parsing (Thanks [alapolloni](https://github.com/alapolloni))
    * Fixed: Fixes readline support on Windows
    * Fixed: Smaller fixes and typos
* __1.0.1__ (March 12, 2013) Fixed: Requires parsedatetime 1.1.2 or newer
* __1.0.0__
    * Integrates seamlessly with DayOne
    * Each journal can have individual settings
    * Fixed: A bug where jrnl would not go into compose mode
    * Fixed: A bug where jrnl would not add entries without timestamp
    * Fixed: Support for parsedatetime 1.x

## v0.3 (2012-05-24)

* __0.3.2__ Converts `\n` to new lines (if using directly on a command line, make sure to wrap your entry with quotes).
* __0.3.1__
    * Supports deleting of last entry.
    * Fixed: Fixes a bug where --encrypt or --decrypt without a target file would not work.
    * Supports a config option for setting word wrap.
    * Supports multiple journal files.
* __0.3.0__
    * Fixed: Dates such as "May 3" will now be interpreted as being in the past if the current day is at least 28 days in the future
    * Fixed: Bug where composed entry is lost when the journal file fails to load
    * Changed directory structure and install scripts (removing the necessity to make an alias from `jrnl` to `jrnl.py`)

## v0.2 (2012-04-16)

* __0.2.4__
    * Fixed: Parsing of new lines in journal files and entries
    * Adds support for encrypting and decrypting into new files
* __0.2.3__
    * Adds a `-short` option that will only display the titles of entries (or, when filtering by tags, the context of the tag)
    * Adds tag export
    * Adds coloured highlight of tags (by default, highlights all tags - when filtering by tags, only highlights search tags)
    * `.jrnl_config` will get automatically updated when updating jrnl to a new version
* __0.2.2__
    * Adds --encrypt and --decrypt to encrypt / decrypt existing journal files
    * Adds markdown export (kudos to dedan)
* __0.2.1__ Submitted to [PyPi](http://pypi.python.org/pypi/jrnl/0.2.1).
* __0.2.0__
    * Encrypts using CBC
    * Fixed: `key` has been renamed to `password` in config to avoid confusion. (The key use to encrypt and decrypt a journal is the SHA256-hash of the password.)

## v0.1 (2012-04-13)


* __0.1.1__
    * Fixed: Removed unnecessary print commands
    * Created the documentation
* __0.1.0__
    * Supports encrypted journals using AES encryption
    * Support external editors for composing entries
* __0.0.2__
    * Filtering by tags and dates
    * Fixed: Now using dedicated classes for Journals and entries

## v0.0 (2012-03-29)

* __0.0.1__ Composing entries works. That's pretty much it.


\* *This Changelog was automatically generated by [github_changelog_generator](https://github.com/github-changelog-generator/github-changelog-generator)*

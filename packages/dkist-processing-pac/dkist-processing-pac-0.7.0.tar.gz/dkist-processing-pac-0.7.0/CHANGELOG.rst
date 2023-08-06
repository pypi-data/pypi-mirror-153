v0.7.0 (2022-06-03)
===================

Misc
----

- Complete rewrite to convert SV code to Data Center context (`#9 <https://bitbucket.org/dkistdc/dkist-processing-pac/pull-requests/9>`__)


v0.6.2 (2022-04-28)
===================

Features
--------

- Relaxed version to FITS specification to move to SPEC0122 Rev F.

v0.6.1 (2022-04-27)
===================

Bugfixes
--------

- Don't modify dresser polarizer and retarder values when using it to initialize a `CalibrationSequence` object

v0.6.0 (2022-04-19)
===================

Features
--------

- Include `lmfit` `MinimizerResult` objects in return from `FittingFramework.run_core` (`#7 <https://bitbucket.org/dkistdc/dkist-processing-pac/pull-requests/7>`__)
- Refactor to create `FittingFramework.prepare_model_objects` function (`#7 <https://bitbucket.org/dkistdc/dkist-processing-pac/pull-requests/7>`__)


Documentation
-------------

- Add changelog and towncrier machinery (`#5 <https://bitbucket.org/dkistdc/dkist-processing-pac/pull-requests/5>`__)


v0.5.1 (2022-03-31)
===================

Misc
----

- Don't throw annoying telescope db warnings if there is only 1 time listed in db (`#4 <https://bitbucket.org/dkistdc/dkist-processing-pac/pull-requests/4>`__)


v0.5.0 (2022-03-24)
===================

Bugfixes
--------

- "Q_in" now *always* fixed to 0 if `use_M12` flag is set in fit mode (`#3 <https://bitbucket.org/dkistdc/dkist-processing-pac/pull-requests/3>`__)


v0.4.1 (2022-03-10)
===================

Features
--------

- Added more fit_modes (`M12_fitUV`, `fit_QUV`, `no_T`, `use_M12`, and `use_M12_globalRet_globalTrans`)

v0.4.0 (2022-03-10)
===================

Features
--------

- Single Calibration Sequence steps now expected to come from separate IPs (`#2 <https://bitbucket.org/dkistdc/dkist-processing-pac/pull-requests/2>`__)


Bugfixes
--------

- Use "none" instead of 0 for angle in headers when GOS optic not in the beam (`#2 <https://bitbucket.org/dkistdc/dkist-processing-pac/pull-requests/2>`__)


v0.3.5 (2022-02-22)
===================

First version to touch DKIST summit data

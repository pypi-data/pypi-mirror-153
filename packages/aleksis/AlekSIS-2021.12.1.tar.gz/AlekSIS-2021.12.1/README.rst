AlekSIS® — All-libre extensible kit for school information systems
==================================================================

What AlekSIS® is
----------------

`AlekSIS®`_ is a web-based school information system (SIS) which can be used to
manage and/or publish organisational subjects of educational institutions.

Formerly two separate projects (BiscuIT and SchoolApps), developed by
`Teckids e.V.`_ and a team of students at `Katharineum zu Lübeck`_, they
were merged into the AlekSIS project in 2020.

AlekSIS is a platform based on Django, that provides central funstions
and data structures that can be used by apps that are developed and provided
seperately. The AlekSIS team also maintains a set of official apps which
make AlekSIS a fully-featured software solutions for the information
management needs of schools.

By design, the platform can be used by schools to write their own apps for
specific needs they face, also in coding classes. Students are empowered to
create real-world applications that bring direct value to their environment.

AlekSIS is part of the `schul-frei`_ project as a component in sustainable
educational networks.

This package
------------

The ``aleksis`` package is a meta-package, which simply depends on the core
and all official apps as requirements. The dependencies are semantically versioned
and limited to the current `minor` version. If installing the distribution meta-package,
all apps will be kept up to date with bugfixes, but not introduce new features or breakage.

Official apps
-------------

+--------------------------------------+---------------------------------------------------------------------------------------------+
| App name                             | Purpose                                                                                     |
+======================================+=============================================================================================+
| `AlekSIS-App-Chronos`_               | The Chronos app provides functionality for digital timetables.                              |
+--------------------------------------+---------------------------------------------------------------------------------------------+
| `AlekSIS-App-DashboardFeeds`_        | The DashboardFeeds app provides functionality to add RSS or Atom feeds to dashboard         |
+--------------------------------------+---------------------------------------------------------------------------------------------+
| `AlekSIS-App-Hjelp`_                 | The Hjelp app provides functionality for aiding users.                                      |
+--------------------------------------+---------------------------------------------------------------------------------------------+
| `AlekSIS-App-LDAP`_                  | The LDAP app provides functionality to import users and groups from LDAP                    |
+--------------------------------------+---------------------------------------------------------------------------------------------+
| `AlekSIS-App-Untis`_                 | This app provides import and export functions to interact with Untis, a timetable software. |
+--------------------------------------+---------------------------------------------------------------------------------------------+
| `AlekSIS-App-Alsijil`_               | This app provides an online class register.                                                 |
+--------------------------------------+---------------------------------------------------------------------------------------------+
| `AlekSIS-App-CSVImport`_             | This app provides import functions to import data from CSV files.                           |
+--------------------------------------+---------------------------------------------------------------------------------------------+
| `AlekSIS-App-Resint`_                | This app provides time-base/live documents.                                                 |
+--------------------------------------+---------------------------------------------------------------------------------------------+


Licence
-------

::

  Licenced under the EUPL, version 1.2 or later, by Teckids e.V. (Bonn, Germany).

  For details, please see the README file of the official apps.

Please see the LICENCE.rst file accompanying this distribution for the
full licence text or on the `European Union Public Licence`_ website
https://joinup.ec.europa.eu/collection/eupl/guidelines-users-and-developers
(including all other official language versions).

Trademark
---------

AlekSIS® is a registered trademark of the AlekSIS open source project, represented
by Teckids e.V. Please refer to the `trademark policy`_ for hints on using the trademark
AlekSIS®.

.. _AlekSIS®: https://aleksis.org/
.. _Teckids e.V.: https://www.teckids.org/
.. _Katharineum zu Lübeck: https://www.katharineum.de/
.. _European Union Public Licence: https://eupl.eu/
.. _schul-frei: https://schul-frei.org/
.. _AlekSIS-Core: https://edugit.org/AlekSIS/official/AlekSIS-App-Core
.. _AlekSIS-App-Chronos: https://edugit.org/AlekSIS/official/AlekSIS-App-Chronos
.. _AlekSIS-App-DashboardFeeds: https://edugit.org/AlekSIS/official/AlekSIS-App-DashboardFeeds
.. _AlekSIS-App-Hjelp: https://edugit.org/AlekSIS/official/AlekSIS-App-Hjelp
.. _AlekSIS-App-LDAP: https://edugit.org/AlekSIS/official/AlekSIS-App-LDAP
.. _AlekSIS-App-Untis: https://edugit.org/AlekSIS/official/AlekSIS-App-Untis
.. _AlekSIS-App-Alsijil: https://edugit.org/AlekSIS/official/AlekSIS-App-Alsijil
.. _AlekSIS-App-CSVImport: https://edugit.org/AlekSIS/official/AlekSIS-App-CSVImport
.. _AlekSIS-App-Resint: https://edugit.org/AlekSIS/official/AlekSIS-App-Resint
.. _trademark policy: https://aleksis.org/pages/about

# gramps-web-pkg
Experimental packaging for the gramps-web project, instead of using containers

Packages being (or to be) created:
- gramps-web: meta package (WIP)
  - web site for gramps data bases: https://www.grampsweb.org/
  - dependencies:
    - gramps-webapi (WIP)
    - gramps-web-frontend (WIP)
- gramps-web-api: https://pypi.org/project/gramps-webapi/ (WIP)
  - back-end API for accessing gramps data bases
  - dependencies:
    - python-sifts: https://pypi.org/project/sifts/ (COPR)
    - python-webargs: https://pypi.org/project/webargs/ (COPR)

Key:
- COPR: package builds in Fedora COPR
  - https://copr.fedorainfracloud.org/coprs/ahs3/gramps-web/
- TBD: To Be Determined
- WIP: Work In Progress

Build Order:
1. python-sifts, python-webargs
1. python-gramps-webapi


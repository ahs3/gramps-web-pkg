Experimental packaging for the gramps-web project, instead of using containers

Packages being (or to be) created:
- gramps-web: meta package (WIP)
  - web site for gramps data bases: https://www.grampsweb.org/
  - unmet dependencies:
    - gramps-webapi (WIP)
    - gramps-web-frontend (WIP)
- gramps-web-api: https://pypi.org/project/gramps-webapi/ (WIP)
  - back-end API for accessing gramps data bases
  - unmet dependencies:
    - python-flask_jwt_extended: https://pypi.org/project/Flask-JWT-Extended/
      (COPR)
    - python-flask-limiter: https://pypi.org/project/flask-limiter/ (COPR)
    - python-ffmpeg-python: https://pypi.org/project/ffmpeg-python/ (COPR)
    - python-gramps-ql: https://pypi.org/project/gramps-ql/ (COPR)
    - python-sifts: https://pypi.org/project/sifts/ (COPR)
    - python-webargs: https://pypi.org/project/webargs/ (COPR)
- python-flask-limiter: https://pypi.org/project/flask-limiter/ (COPR)
  - rate limiting for Flask applications
  - unmet dependencies:
    - python-limits: https://pypi.org/project/limits/ (COPR)

Key:
- COPR: package builds in Fedora COPR
  - https://copr.fedorainfracloud.org/coprs/ahs3/gramps-web/
- TBD: To Be Determined
- WIP: Work In Progress

Build Order:
1. python-limits -> python-flask-limiter
1. These may be done in any order as part of this step: 
   python-flask_jwt_extended, python-ffpmeg-python, python-sifts,
   python-webargs, python-gramps-ql
1. python-gramps-webapi

Notes:
- python-ffmpeg-python:
  - does not appear to have support in Fedora 42
  - will gramps-web-api replace it?
  - Fedora 42 version builds without issue and is in the COPR, unchanged
    from the Fedora 41 version

TODO:
- documentation packages? are there some needed?

Experimental packaging for the gramps-web project, instead of using containers

Packages being (or to be) created:
- gramps-web: meta package (WIP)
  - web site for gramps data bases: https://www.grampsweb.org/
  - unmet dependencies:
    - python-gramps-webapi: https://pypi.org/project/gramps-webapi/ (COPR)
    - gramps-web-frontend (WIP)
- gramps-web-api: https://pypi.org/project/gramps-webapi/ (COPR)
  - back-end API for accessing gramps data bases
  - unmet dependencies:
    - python-flask_jwt_extended: https://pypi.org/project/Flask-JWT-Extended/
      (COPR)
    - python-flask-limiter: https://pypi.org/project/flask-limiter/ (COPR)
    - python-ffmpeg-python: https://pypi.org/project/ffmpeg-python/ (COPR)
    - python-gramps-ql: https://pypi.org/project/gramps-ql/ (COPR)
    - python-object-ql: https://pypi.org/project/object-ql/ (COPR)
    - python-sifts: https://pypi.org/project/sifts/ (COPR)
    - python-webargs: https://pypi.org/project/webargs/ (COPR)
- python-flask-limiter: https://pypi.org/project/flask-limiter/ (COPR)
  - rate limiting for Flask applications
  - unmet dependencies:
    - python-limits: https://pypi.org/project/limits/ (COPR)
- python-limits: https://pypi.org/project/limits/ (COPR)
  - unmet dependencies:
    - python-etcd3: https://pypi.org/project/etcd3/ (COPR)

Key:
- COPR: package builds in Fedora COPR
  - https://copr.fedorainfracloud.org/coprs/ahs3/gramps-web/
  - implies at least an initial version of a proper package
- TBD: To Be Determined
- WIP: Work In Progress

Build Order:
1. python-etcd3 -> python-limits -> python-flask-limiter
1. These may be done in any order as part of this step: 
   python-flask_jwt_extended, python-ffpmeg-python, python-sifts,
   python-webargs, python-gramps-ql, python-object-ql
1. python-gramps-webapi

Notes:
- python-ffmpeg-python:
  - does not appear to have support in Fedora 42
  - will gramps-web-api replace it?
  - Fedora 42 version builds without issue and is in the COPR, unchanged
    from the Fedora 41 version
- python-object-ql:
  - possible dependency loop?  seems to depend on the gramps package (the
    desktop application)
- Testing (aka using %check in the build):
  - python-limits testing relies on the module etcd3; this can be packaged,
    but has very old testing infrastructure.  Further, etcd3 uses a deprecated
    protobuf internally, so it can not really be used in python-limits tests.
    So, deferring %check in this package until we can figure out how to get
    testing in much better shape upstream.

TODO:
- documentation packages? are there some needed?
- turn on %check in the packages

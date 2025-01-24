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

Key:
- COPR: package builds in Fedora COPR
  - https://copr.fedorainfracloud.org/coprs/ahs3/gramps-web/
  - implies at least an initial version of a proper package
- TBD: To Be Determined
- WIP: Work In Progress

Build Order:
1. [python-etcd3 (for test only) ->] python-limits -> python-flask-limiter
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
  - %check will fail when tests are enabled but most tests seem to work
- python-object-ql:
  - possible dependency loop?  seems to depend on the gramps package (the
    desktop application)
- Testing (aka, for Fedora, using %check in the build):
  - Whilst automated testing is all well and good, a lot of these modules
    require access to pip or docker when running pytest or tox; in several
    cases, modules are required that appear to be neither in Fedora or
    Debian.  In at least one extreme case, the tests have not been updated
    in a long time and rely on a deprecated module.  Where possible, I am
    currently trying to test these by hand.  However, there is a lot of work
    required upstream to remove the need for network connections.
  - At best, %check will actually work, will be put in the package, and
    turned on by default, so the test will run at build time.
  - At worst, a rough draft of %check might be present, but turned off
    until things can be straightened out.
  - python-gramps-ql %check works fine

TODO:
- documentation packages? e.g. gramps-web-docs
- turn on %check in the packages

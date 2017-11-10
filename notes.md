## What I learned

### connexion
https://github.com/zalando/connexion

I was mainly attracted to trying out `connexion` as it seemed like a nice tool for someone who would maintain both the specification and the code implementation of a web API. In particular, I liked the idea of having the specification as the "source of truth" since it would relieve me the trouble of making sure the code implementation is in-sync with its original specification.

Overall, everything worked out as intended. I haven't ran into any major problems so far, but I'm a bit skeptical on whether the package is mature enough to support a fully fledged, "real-world" web API. My main issues include the sparse documentation and the relatively small userbase (haven't seen any notable web APIs using this package other than the company behind `connexion`). Another issue I had was that `connexion` is built *on top* of Flask instead of being designed as a Flask plugin. This makes `connexion` not play as nice with other Flask plugins (e.g. FlaskSQLAlchemy) (I also had a little trouble understanding how it would work with Gunicorn, but got it working in the end). At the time of this writing, it also does not support version 3.0 of the OpenAPI/Swagger specification.


Related issues:
- https://github.com/zalando/connexion/issues/417
- https://github.com/zalando/connexion/issues/420


### Heroku
https://www.heroku.com/

I was interested in trying out a cloud service that could host my web API for free. I'm most comfortable with AWS but I felt AWS would be overkill in this situation. I ended up choosing Heroku as it offered both free web and database hosting, had a nice getting-started guide, and seemed to require minimal setup/configuration effort.


### DPL
https://github.com/travis-ci/dpl

I decided to use this tool as it was referenced in [gitlab's example](https://docs.gitlab.com/ce/ci/examples/test-and-deploy-python-application-to-heroku.html) for deploying an application to Heroku using their CI service. Seems like Github has a more integrated solution


### GitLab's CI Runner only checks exit code of last command
A build/job can return success even if some of the commands inside the `script` field return a non-zero exit status. For example, the following job will always return successful because only the exit status of the last command is checked
```yaml
job1:
  stage: test
  script:
  - true && false
  - true && true
```

To ensure all commands are run successfully, I make sure to set `set -euo pipefail` before any commands are run. E.g.,
```yaml
image: python:3.6

before_script:
  - set -euo pipefail

stages:
  - test


job_that_fails:
  stage: test
  script:
  - true && false
  - true && true
```

Related issues:
- https://gitlab.com/gitlab-org/gitlab-ce/issues/20731
- https://gitlab.com/gitlab-org/gitlab-ce/issues/20730
- https://gitlab.com/gitlab-org/gitlab-ce/issues/20654


### Issues with pylint's circular import warnings
Pylint warns against circular imports even if the offending import is called within a function. In addition, pylint does not correctly identify the offending file and annotates an unrelated file instead. In the end, I had to disable the circular import warning in `.pylintrc`.

Related issues:
- https://github.com/PyCQA/pylint/issues/850
- https://github.com/PyCQA/pylint/issues/59


### Powershell and conda don't play nice
`activate` and `deactivate` commands for `conda` environments do not work in Windows PowerShell natively.

Related issues:
- https://github.com/conda/conda/issues/626

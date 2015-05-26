# tsspgallery
A study project of "Techniques of Software Development" subject in university.

KPI, 2015

### Running

To simply install the site and run under test environment, you will need to create virtualenv.

```
$ pip install virtualenv
```
Then create a virtualenv (see http://docs.python-guide.org/en/latest/dev/virtualenvs/).

After that install all necessary dependencies:

```
$ pip install -r req.txt
```

After that the site is ready, so run ```make``` to install the site (includes running migrations, creating superuser and running django builtin test server).

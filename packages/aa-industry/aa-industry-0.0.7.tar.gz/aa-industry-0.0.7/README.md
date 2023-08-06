# Industry plugin app for Alliance Auth

This is an Industry plugin app for [Alliance Auth](https://gitlab.com/allianceauth/allianceauth) (AA) that can be used as starting point to develop custom plugins.

![License](https://img.shields.io/badge/license-MIT-green)
![python](https://img.shields.io/badge/python-3.7-informational)
![django](https://img.shields.io/badge/django-3.1-informational)

## Installation

Run the pip command to install
```shell
$ pip install aa-industry
```

add the ```industry``` app to settings.py under ```INSTALLED_APPS```

run the migrations and collect static commands
```shell
$ python manage.py migrate
$ python manage.py collectstatic
```

## Updating

Run the pip command to install
```shell
$ pip install -U aa-industry
```

or 

```shell
$ pip install --upgrade aa-industry
```

run the migrations and collect static commands
```shell
$ python manage.py migrate
$ python manage.py collectstatic
```


## Permissions

To make it visible to users or groups you must provide the ```industry.view_industry``` permission.

## Scopes

The scopes required to see the industry jobs for the character and corporations are:

|Scope   |Permission|
|--------|-----------|
|esi-industry.read_character_jobs.v1|Read Character Jobs
|esi-industry.read_corporation_jobs.v1|Read Corporation Jobs
|esi-universe.read_structures.v1|Read Structure information (to retrieve the names)

## Contribute

If you made a new app for AA please consider sharing it with the rest of the community. For any questions on how to share your app please contact the AA devs on their Discord. You find the current community creations [here](https://gitlab.com/allianceauth/community-creations).

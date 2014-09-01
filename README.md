MineID
======

Open Source OAuth Provider for Minecraft

Install
-------

**1. Clone the repository**

```
git clone https://github.com/MineID/MineID.git
```

**2. Create a virtual environment**

This step is optional but highly recommended.

```
cd MineID
virtualenv .venv
soure .venv/bin/activate
```

**3. Install dependencies and sync database**

```
pip install -r requirements_core.txt
python manage.py syncdb --migrate --noinput --settings=mineid.dev_settings
```

Run
---

```
python manage.py runserver 0:8000 --settings=mineid.dev_settings
```

Upgrade
-------

**1. Pull changes**

Pull from the stable branch:

```
git pull origin stable
```

or from a specific version:

```
git checkout v1.0
```

**2. Install dependencies and sync database**

Repeat the step **3** from installation.

License
-------

LGPL (See LICENSE file for more info)

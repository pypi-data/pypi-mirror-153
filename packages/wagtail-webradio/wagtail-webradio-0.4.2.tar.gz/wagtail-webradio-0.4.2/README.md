# wagtail-webradio

Manage your web radio - e.g. podcats, programs - in Wagtail.

**Warning!** This project is still early on in its development lifecycle. It is
possible for breaking changes to occur between versions until reaching a stable
1.0. Feedback and pull requests are welcome.

## Requirements

This package requires the following:
- **Wagtail** (2.15 LTS)
- **Django** (3.1, 3.2)
- **Python 3** (3.7, 3.8, 3.9)

## Installation

1. Install using ``pip``:
   ```shell
   pip install wagtail-webradio
   ```
2. Add ``wagtail_webradio`` to your ``INSTALLED_APPS`` setting:
   ```python
   INSTALLED_APPS = [
       # ...
       'wagtail_webradio',
       # ...
   ]
   ```
3. Run ``python manage.py migrate`` to create the models

## Configuration
If you want, you can disable the possibility to upload a sound file or restrict
to a custom authorized MIME types in your setting file:
```python
# settings.py

WEBRADIO_SOUND_FILE = False  # default to True
WEBRADIO_AUTHORIZED_MIME_TYPES = ['audio/mpeg', 'audio/flac']
```
default authorized MIME types are `audio/ogg`, `audio/mpeg`, `audio/flac`,
and `audio/opus`.

## Usage
### Frontend components

A player with a playlist management is provided to be easily included into your
frontend. Under the hood, it uses [django-unicorn] with a bit of JavaScript to
manipulate the audio from the Web browser. It is currently unstyled but you can
find an [example][1] when using Bootstrap. You should also have a look to the
[template][2] of this component to know how to extend it.

To make use of it:

1. Install the ``player`` extra of this package:
   ```shell
   pip install wagtail-webradio[player]
   ```
2. Integrate ``Unicorn`` in your project by [following the documentation][3]
3. Configure ``Unicorn`` settings to look for this package's components:
   ```python
   UNICORN = {
       'APPS': ['wagtail_webradio'],
   }
   ```

Then, e.g. in ``base.html``, load the player scripts in the ``<head>`` of your
document and the component in the ``<body>``:
```django
<html>
  <head>
    <!-- […] -->

    <script src="{% static "wagtail_webradio/player/js/main.js" %}" defer></script>
  </head>
  <body>
    <! -- […] -->

    {% unicorn "player" %}

    <! -- […] -->
  </body>
</html>
```

In the case of multi-process production environment, you must switch to redis,
memcache or database caching to make Unicorn working correctly. For example with
memcache listening through unix socket, you can add in settings.py :
```
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.PyMemcacheCache',
        'LOCATION': 'unix:/var/run/memcached/memcached.sock',
    }
}
```

When the player scripts are loaded, you can simply add a song to the playlist
by defining a ``data-player-add-podcast`` or ``data-player-add`` attribute on an
element, and optionally ``data-player-autoplay`` to play the song once added:
```html
<button data-player-add-podcast="10" data-player-autoplay>Add a podcast by id</button>

<button data-player-add="{'title': 'Title', 'subtitle': 'Subtitle', 'url': 'http://example.org/song.ogg', 'thumbnail_url': 'http://example.org/thumb.png'}">
  Add a song
</button>
```

[1]: examples/player/styles.scss
[2]: wagtail_webradio/templates/wagtail_webradio/components/player.html
[3]: https://www.django-unicorn.com/docs/installation/#integrate-unicorn-with-django
[django-unicorn]: https://www.django-unicorn.com/

## Development
### Quick start

To set up a development environment, ensure that Python 3 is installed on your
system. Then:

1. Clone this repository
2. Create a virtual environment and activate it:
   ```shell
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install this package in develop mode with extra requirements:
   ```shell
   pip install -e .[test]
   ```

If you plan to upload the package on PyPi, you will also need to run:
```shell
pip install --upgrade build twine
```

### Contributing

The Python code is formatted and linted thanks to [flake8], [isort] and [black].
To ease the use of this tools, the following commands are available:
- `make lint`: check the Python code syntax and imports order
- `make format`: fix the Python code syntax and imports order

The tests are written with [pytest] and code coverage is measured with [coverage].
You can use the following commands for that:
- ``make test``: run the tests and output a quick report of code coverage
- ``make coverage``: run the tests and produce an HTML report of code coverage

When submitting a pull-request, please ensure that the code is well formatted
and covered, and that all the other tests pass.

[flake8]: https://flake8.pycqa.org/
[isort]: https://pycqa.github.io/isort/
[black]: https://black.readthedocs.io/
[pytest]: https://docs.pytest.org/
[coverage]: https://coverage.readthedocs.io/

## License

This extension is mainly developed by [Cliss XXI](https://www.cliss21.com) and
licensed under the [AGPLv3+](LICENSE). Any contribution is welcome!

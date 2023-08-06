from wagtail.tests.utils.form_data import nested_form_data, streamfield

import pytest
from webtest.forms import Field


def prettify_html(element, depth=0):
    """
    Turn an HTML element into a nicely formatted string. It is based on
    `django.test.html.Element.__str__` method and add indentation.
    """
    indent = '  ' * depth
    if isinstance(element, str):
        return '%s%s' % (indent, element)
    output = '%s<%s' % (indent, element.name)
    for key, value in element.attributes:
        if value:
            output += ' %s="%s"' % (key, value)
        else:
            output += ' %s' % key
    output += '>'
    if len(element.children) == 1 and isinstance(element.children[0], str):
        output += '%s</%s>' % (element.children[0], element.name)
    elif element.children:
        depth += 1
        for child in element.children:
            output += '\n%s' % (prettify_html(child, depth))
        output += '\n%s</%s>' % (indent, element.name)
    return output


def get_streamfield_form_data(name, items):
    """
    Return form data for a StreamField named `name` with given blocks `items`,
    which must be a list of 2-tuple (block_type, value).
    """
    # https://docs.wagtail.io/en/stable/advanced_topics/testing.html#wagtail.tests.utils.form_data.streamfield
    return nested_form_data({name: streamfield(items)})


def add_form_field(form, name, value=None, tag='input', pos=0, **kwargs):
    """Add an extra field to the given WebTest form object `form`."""
    field = Field(form, tag, name, pos, value, **kwargs)
    form.fields[name] = [field]
    form.field_order.append((name, field))
    return field


def add_form_data(form, data):
    """Add the form data `data` to the given WebTest form object `form`."""
    for name, value in data.items():
        add_form_field(form, name, value)


def add_inline_form_data(form, prefix, data, index=None):
    """
    Add the form data `data` to the given WebTest form object `form` as an
    inline formset with the prefix `prefix` at the index `index` - or the next
    one if empty.
    """
    total_forms_field_name = f'{prefix}-TOTAL_FORMS'
    if index is None:
        index = int(form[total_forms_field_name].value)
    data.setdefault('ORDER', str(index))
    data.setdefault('DELETE', '')
    for name, value in data.items():
        add_form_field(form, f'{prefix}-{index}-{name}', value)
    form[total_forms_field_name].value = str(index + 1)


class ViewTestMixin:
    """
    Provide facilities to integrate WebTest while testing some views.
    """

    #: The default URL to use in requests.
    url = None

    #: The default user to use for authenticated requests.
    user = None

    #: Whether CSRF checks must be enabled.
    csrf_checks = True

    @pytest.fixture(autouse=True)
    def setup_django_app(self, django_app_factory):
        self.django_app = django_app_factory(csrf_checks=self.csrf_checks)

    def _query(self, method, url=None, **kwargs):
        """
        Make a `method` request to `url` - or `self.url` if not given. For
        other arguments, see `webtest.app.TestApp.get`.
        """
        kwargs.setdefault('user', self.user)
        return getattr(self.django_app, method)(url or self.url, **kwargs)

    def get(self, url=None, params=None, **kwargs):
        return self._query('get', url, params=params, **kwargs)

    def post(self, url=None, params=None, **kwargs):
        return self._query('post', url, params=params, **kwargs)

    def put(self, url=None, params=None, **kwargs):
        return self._query('put', url, params=params, **kwargs)

    def delete(self, url=None, params=None, **kwargs):
        return self._query('delete', url, params=params, **kwargs)


class AdminViewTestMixin(ViewTestMixin):
    """
    Extend `ViewMixin` to make requests as an admin user.
    """

    @pytest.fixture(autouse=True)
    def setup_user(self, admin_user):
        self.user = admin_user

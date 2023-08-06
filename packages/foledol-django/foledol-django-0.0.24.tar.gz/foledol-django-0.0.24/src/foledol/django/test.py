from django.conf import settings
from django.urls import reverse


def login(test, username, space=settings.DEFAULT_SPACE):
    response = test.client.post(reverse(space + ':user_login'), {'username': username, 'password': 'pwd'}, follow=True)
    test.assertContains(response, 'home')


def set_default(obj, context):
    for key in obj.__dict__.keys():
        if key in context:
            continue
        value = obj.__dict__[key]
        if value is None:
            continue
        context[key] = value


def get_default_path(test, path, space=settings.DEFAULT_SPACE):
    return path if path else reverse(space + ':' + test.prefix + 's')


def get_and_post(test, url, context):
    response = test.client.get(url, context, follow=True)
    test.assertEqual(response.status_code, 200)
    response = test.client.post(url, context, follow=True)
    test.assertEqual(response.status_code, 200)
    return response


def create_object(test, context, ref, obj=None, path=None, space=settings.DEFAULT_SPACE):
    if obj:
        set_default(obj, context)
    context.update({
        'action': 'create',
        'path': ':' + get_default_path(test, path, space)
    })
    response = get_and_post(test, reverse(space + ':' + test.prefix + '_create'), context)
    test.assertContains(response, ref)


def update_object(test, pk, context, ref, path=None, space=settings.DEFAULT_SPACE):
    context.update({
        'action': 'update',
        'path': ':' + get_default_path(test, path, space)
    })
    response = get_and_post(test, reverse(space + ':' + test.prefix + '_update', kwargs={'pk': pk}), context)
    test.assertContains(response, ref)


def delete_object(test, pk, ref, path=None, space=settings.DEFAULT_SPACE):
    context = {
        'action': 'delete',
        'delete': '',
        'path': ':' + get_default_path(test, path, space)
    }
    response = test.client.get(reverse(space + ':' + test.prefix + '_delete', kwargs={'pk': pk}), context, follow=True)
    test.assertEqual(response.status_code, 200)
    response = test.client.post(reverse(space + ':' + test.prefix + '_delete', kwargs={'pk': pk}), context, follow=True)
    test.assertEqual(response.status_code, 200)
    test.assertNotContains(response, ref)


def search_object(test, item1, item2, space=settings.DEFAULT_SPACE):
    response = test.client.post(reverse(space + ':' + test.prefix + 's'), {'search': item1})
    test.assertEqual(response.status_code, 200)
    test.assertContains(response, item1)
    test.assertNotContains(response, item2)
    response = test.client.post(reverse(space + ':' + test.prefix + 's'), {'search': ''})
    test.assertContains(response, item1)
    test.assertContains(response, item2)


def filter_object_all(test, filters, space=settings.DEFAULT_SPACE):
    for filter in filters:
        filter_object(test, filter.name)
    test.client.post(reverse(space + ':' + test.prefix + 's'), {'filter_key': ''})


def filter_object(test, filter_key, space=settings.DEFAULT_SPACE):
    response = test.client.post(reverse(space + ':' + test.prefix + 's'), {'filter_key': filter_key})
    test.assertEqual(response.status_code, 200)


def download(test, action, url, content_type):
    response = test.client.post(url, {
        'action': action,
        'path': ':' + url,
    }, follow=True)
    test.assertEqual(response.status_code, 200)
    test.assertEqual(response['Content-Type'], content_type)
    return response


def print_object(test, action, url):
    return download(test, action, url, 'application/pdf')


def export_object(test, action, url):
    return download(test, action, url, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')


def export_object_as_txt(test, action, url):
    return download(test, action, url, 'text/plain')


def import_object(test, action, url, path, access='rb'):
    with open(path, access) as file:
        response = test.client.post(url, {
            'action': action,
            'path': ':' + url,
            'upload': file
        }, follow=True)
        test.assertEqual(response.status_code, 200)


def import_object_as_txt(test, action, url, path):
    import_object(test, action, url, path, access='r')


def run_object_module(test, action, url):
    response = test.client.post(url, {
        'action': action,
        'path': ':' + url,
    }, follow=True)
    test.assertEqual(response.status_code, 200)
    return response

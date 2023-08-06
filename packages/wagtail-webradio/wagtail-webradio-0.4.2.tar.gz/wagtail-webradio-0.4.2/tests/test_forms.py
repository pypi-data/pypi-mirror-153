from wagtail_webradio import forms


def test_sound_file_disabled_in_settings(settings):
    assert 'sound_file' not in forms.get_podcast_excluded_fields()
    settings.WEBRADIO_SOUND_FILE = False
    assert 'sound_file' in forms.get_podcast_excluded_fields()

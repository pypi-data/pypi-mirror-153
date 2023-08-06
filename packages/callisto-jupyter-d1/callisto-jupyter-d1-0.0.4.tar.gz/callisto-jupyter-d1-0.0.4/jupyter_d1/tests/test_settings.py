from jupyter_d1.settings import settings


def test_settings():
    assert settings.SECRET_KEY == "jukugoeir32*"
    assert settings.PUSH_NOTE_SECRET_KEY == "12iuf49f))("
    assert settings.WORK_NODE_ID == 433451
    assert settings.MOTHERSHIP_URL == "https://staging.callistoapp.com/api/v1"
    assert settings.WATCHDOG_ENABLED

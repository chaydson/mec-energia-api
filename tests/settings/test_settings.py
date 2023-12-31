import pytest
import os

from mec_energia import settings as s

@pytest.mark.order(1)    
def test_var_secret_key_is_available():
    assert s.SECRET_KEY is not None

@pytest.mark.order(1)    
def test_var_debug_is_available():
    assert s.DEBUG is not None

@pytest.mark.order(1)    
def test_var_test_is_available():
    assert s.TEST is not None
    assert s.TEST

@pytest.mark.order(1)    
def test_var_environment_is_available():
    assert s.ENVIRONMENT is not None
    assert s.ENVIRONMENT == 'test'

@pytest.mark.order(1)    
def test_var_mec_energia_url_is_available():
    assert s.MEC_ENERGIA_URL is not None

@pytest.mark.order(1)    
def test_var_mec_energia_email_is_available():
    assert s.MEC_ENERGIA_EMAIL is not None

@pytest.mark.order(1)    
def test_var_mec_energia_email_app_password_is_available():
    assert s.MEC_ENERGIA_EMAIL_APP_PASSWORD is not None



import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_show_ip_default(client):
    """Without X-Forwarded-For header, should show remote_addr (127.0.0.1)."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Your public IP is: 127.0.0.1' in response.data

def test_show_ip_x_forwarded_for(client):
    """With X-Forwarded-For header, should show that IP."""
    test_ip = '203.0.113.42'
    response = client.get('/', headers={'X-Forwarded-For': test_ip})
    assert response.status_code == 200
    assert f'Your public IP is: {test_ip}'.encode() in response.data

def test_html_structure(client):
    """Response should be valid minimal HTML."""
    response = client.get('/')
    data = response.data.decode()
    assert data.startswith('<html>')
    assert '<h1>Your public IP is:' in data
    assert data.endswith('</body></html>')

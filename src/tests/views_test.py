from Principal  import app
import pytest

class TestClass:
        
    def read_healthx_test(self):
        """Tests the healthx check endpoint"""
        response = app.test_client().get("/health/liveness")
        assert response.status_code == 200
        assert response.data == b'{"healthx":"ok"}\n' 

    def read_healthz_test(self):
        """Tests the healthz check endpoint"""
        response = app.test_client().get("/health/readiness")
        assert response.status_code == 200
        assert response.data == b'{"healthz":"ok"}\n'
    

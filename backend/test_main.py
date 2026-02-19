# backend/test_main.py
def test_inicio_falso():
    # Una prueba simple para ver si el sistema de tests funciona
    assert 1 + 1 == 2

def test_configuracion_api():
    # Aquí podrías importar tu 'app' de FastAPI y ver si responde
    from main import app
    assert app.title == "Rugby App Secure" # O el título que tenga tu API

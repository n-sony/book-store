from app import create_app
from config import FLASK_ENV

app = create_app(FLASK_ENV)

if __name__ == "__main__":
    app.run(debug=app.config.get("DEBUG", False))

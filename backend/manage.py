from dotenv import load_dotenv

from app import create_app  # ignore

load_dotenv(override=True)

app = create_app()

if __name__ == "__main__":
    app.run(port=5000, host="0.0.0.0", debug=True)

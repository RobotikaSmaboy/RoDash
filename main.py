from roboys_dash import create_app

app = create_app()

if __name__ == "__main__":
    app.run(port=34455, debug=True)

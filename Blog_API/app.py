from app import create_app, db

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {"db": db}


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)

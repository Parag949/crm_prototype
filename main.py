from website import create_app
app = create_app()
if __name__ == '__main__':
    app.run(debug=True)  # debug mode is on, so the server will restart on code changes
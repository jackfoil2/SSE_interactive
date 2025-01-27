from flask import Flask, render_template

app = Flask(__name__)

# Route for the main page
@app.route("/")
def index():
    return render_template("index.html")

# List of sections
sections = [1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 2.1, 2.2, 2.3, 2.4, 3.1, 4.1, 4.2, 4.3, 4.4, 4.5, 5.1, 5.2, 5.3, 6.1, 6.2, 6.3, 6.4]

# Helper function to create routes
def create_route(section):
    route = f"/{section}"
    html_file = f"{section}.html"

    @app.route(route, endpoint=f"section_{section}")
    def section_page():
        return render_template(html_file)

# Loop to dynamically create routes
for section in sections:
    create_route(section)

if __name__ == "__main__":
    app.run(debug=True)


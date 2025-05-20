from app import app
from app.api.resources.case import case_bp

app.register_blueprint(case_bp)

if __name__ == '__main__':

    app.run(host='0.0.0.0', port=5001, debug=True)
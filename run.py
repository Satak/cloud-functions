"""
This is a local testing wrapper for cloud functions

To run a cloud function:
python run.py folder.src.main
"""

if __name__ == '__main__':
    import sys
    import importlib
    from flask import Flask, request

    try:
        module_path = sys.argv[1]
        my_module = importlib.import_module(module_path)
    except IndexError:
        raise ValueError("No command line argument provided for the cloud function module path")

    app = Flask(__name__)

    @app.route('/', methods=['GET', 'POST', 'DELETE', 'PUT'])
    def index():
        return my_module.main(request)

    app.run(threaded=True, debug=True)

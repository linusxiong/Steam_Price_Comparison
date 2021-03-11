import json
import api
import spider


def run():
    api.app.run(debug=True, port=8080)



if __name__ == '__main__':
    run()

import json
import api
import spider


def run():
    api.app.run(host='0.0.0.0', debug=True, port=8080)



if __name__ == '__main__':
    run()

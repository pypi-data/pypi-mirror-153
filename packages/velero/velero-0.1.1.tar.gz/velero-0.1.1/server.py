# import bjoern
# from velero import app

# host = '0.0.0.0'
# port = 8000
# bjoern.listen(app, host, port)
# bjoern.run()

from velero import app

if __name__ == '__main__':
    # import bjoern
    host = "0.0.0.0"
    port = 8000

    # bjoern.listen(app, host, port)
    # bjoern.run(statsd=...)
    app.run(host=host, port=port, debug=True)

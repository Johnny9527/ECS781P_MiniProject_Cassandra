from flask import Flask, request
from cassandra.cluster import Cluster

cluster = Cluster(contact_points=['172.17.0.2'],port=9042)
session = cluster.connect()
app = Flask(__name__)

@app.route('/')
def hello():
    name = request.args.get("name","World")
    return('<h1>Hello, {}!</h1>'.format(name))

@app.route('/catdata/<title>')    # Respond with a specific cat name and its picture URL.
def profile(title):
    rows = session.execute( """Select * From catdata.stats where title = '{}'""".format(title))

    for catdata in rows:
        return('<h1>{} picture is in {}.</h1>'.format(title,catdata.url))

    return('<h1>That cat does not exist!</h1>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)

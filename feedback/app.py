from flask import Flask, render_template, request
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import socket
import os

app = Flask(__name__)

keyspace = 'feedback_data'
fb_table_name = 'feedbacks'
fb_text_field = 'feedback_text'

cass_ips = ["127.0.0.1"]
cass_port = 9042
cass_username = 'cassandra'
cass_password = ''

cluster = Cluster(cass_ips, port=cass_port, auth_provider=\
                  PlainTextAuthProvider(username=cass_username, password=cass_password))

session = cluster.connect(keyspace, wait_for_all_pools=False)


@app.route('/feedback', methods = ['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        feedback = request.form['feedback']
        query = f"INSERT INTO {keyspace}.{fb_table_name} (id, {fb_text_field}) VALUES (uuid(), '{feedback}')"
        session.execute(query)
        return render_template('feedback_sent.html')
    else:

        session.execute(f'USE {keyspace}')
        result = session.execute(f'SELECT * FROM {fb_table_name}')
        rows = []
        for row in result:
            rows.append(row.feedback_text)
        app.logger.info(rows)
        return render_template('feedback.html', feedbacks=rows)


if __name__=='__main__':
      app.run(debug=True, host='0.0.0.0', port=5555)

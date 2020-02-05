from sshtunnel import SSHTunnelForwarder
import psycopg2

cluster_name = "<cluste_name>"
bastion_port = <bastion_port>
ssh_username = "<ssh_user>"
ssh_pkey = "~/.ssh/ssh_key"
remote_target_name = "<remote_service>"
remote_target_port = 5432


server = SSHTunnelForwarder(
    (cluster_name, bastion_port),
    ssh_username=ssh_username,
    ssh_pkey=ssh_pkey,
    remote_bind_address=(remote_target_name, remote_target_port)
)

server.start()

local_port = server.local_bind_port

print(local_port)
conn = psycopg2.connect(host='localhost',
                        dbname="postgres",
                        user="postgres",
                        port=server.local_bind_port,
                        password="")

cur = conn.cursor()
cur.execute('SELECT * FROM pg_database;')
rows = cur.fetchall()
for row in rows:
    print(row)
cur.close()

conn.close()


server.stop()

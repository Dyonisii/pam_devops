from flask import Flask, render_template, request
import paramiko

app = Flask(__name__)


def execute_ssh_command(hostname, port, username, password, command):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname, port, username, password)
        stdin, stdout, stderr = ssh.exec_command(command)
        output = stdout.read().decode()
        ssh.close()
        return output
    except paramiko.SSHException as e:
        error_message = str(e).split("\n")[0]  
        return error_message


@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        
        command = request.form['command']
     
        result = execute_ssh_command('172.19.0.3', 22, 'root', 'sshpass1', command)
  
    return render_template('index.html', result=result)

if __name__ == '__main__':
   
    app.run(debug=True, host='0.0.0.0')

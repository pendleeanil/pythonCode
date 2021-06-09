# setup paramiko:
pip install paramiko

# In your Python Script:
import paramiko

# Define the ssh_client referring to paramiko sshclient object
ssh_client = paramiko.SSHClient()

# setting the Policy for automatically adding hostname and new host key to the local HostKeys object, and save it, which will be used by SSHClient.
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# Define a variable ‘k’ passing the RSA Private key to the variable
k = paramiko.RSAKey.from_private_key_file('C:\\id_rsa')

# Connection parameters
ssh_client.connect(hostname = "pfts.intuit.com", username = "svc_alteryx_pfts", pkey = k, timeout=100 )

# Opening the SFTP Channel
ftp_client=ssh_client.open_sftp()

# Opening the file in the SFTP Channel
remote_file = ftp_client.open(f'/from_tsheets/{filename}', 'r+')

# Reading the file
contents = remote_file.readlines()

# Creating a Pandas dataframe 
df = pd.DataFrame(contents)

# Writing to Alteryx for further process.
Alteryx.write(df, 1)

import ftplib
from ftplib import FTP, FTP_TLS

ftps = FTP_TLS('localhost')
ftps.login()
ftps = FTP_TLS('ftp.pureftpd.org')
ftps.login()
'230 Anonymous user logged in'
ftps.prot_p()
'200 Data protection level set to "private"'
ftps.nlst()
['6jack', 'OpenBSD', 'antilink', 'blogbench', 'bsdcam', 'clockspeed', 'djbdns-jedi', 'docs', 'eaccelerator-jedi', 'favicon.ico', 'francotone', 'fugu', 'ignore', 'libpuzzle', 'metalog', 'minidentd', 'misc', 'mysql-udf-global-user-variables', 'php-jenkins-hash', 'php-skein-hash', 'php-webdav', 'phpaudit', 'phpbench', 'pincaster', 'ping', 'posto', 'pub', 'public', 'public_keys', 'pure-ftpd', 'qscan', 'qtc', 'sharedance', 'skycache', 'sound', 'tmp', 'ucarp']

def get_file_ftps(host, path_to_file, ftps_configuration):
    """
        Copy an existing file from FTP via ftp://*host*/*path_to_file* link to home directory.
        The function return the full path to the file that has been downloaded.
    """
    # Construct FTP object and get the file on a server
    with ftplib.FTP_TLS(host, user = ftps_configuration["user"], passwd = ftps_configuration["psswd"]) as ftps:
        filename = re.findall("[^/]*$", path_to_file)[0]
        ftps.prot_p()
        with open(filename, "wb") as wf:
            ftps.retrbinary("RETR " + filename, wf.write)

    file_location = gc_write_dir + "/" + filename
    print("File " + path_to_file + " has got successfully.")
    return file_location 
from ftplib import FTP_TLS
ftps = FTP_TLS('localhost')
# login after securing control channel
ftps.login('maxlarbs', 'chocolat')           
# switch to secure data connection.. 
# IMPORTANT! Otherwise, only the user and password is encrypted and
# not all the file data.
ftps.prot_p()          
retour = ftps.retrlines('LIST')
print(retour)
ftps.close()
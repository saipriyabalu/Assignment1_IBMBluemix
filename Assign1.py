# References: https://console.bluemix.net/docs/starters/upload_app.html
#https://docs.openstack.org/developer/python-swiftclient/client-api.html
#https://twhiteman.netfirms.com/des.html
#http://docs.ceph.com/docs/master/radosgw/swift/python/


import os,pyDes
import keystoneclient.v3 as keystoneclient
import swiftclient.client as swiftclient

# User credentials
authenticationurl = 'https://identity.open.softlayer.com' + '/v3'
projectname = 'object_storage_9d3f0880_aeda_4c31_8763_49bfbdb81262'
password = 'w(l}3q.YV5i^7)7!'
userdomain = '1370727'
projectid = 'f375b1a0507e4576a24e5e5780497a7d'
userid = 'e32f0a6c156b4ffa88f018812cf0ad46'
region = 'dallas'
k = pyDes.des("DESCRYPT", pyDes.CBC, "\0\0\0\0\0\0\0\0", pad=None, padmode=pyDes.PAD_PKCS5)

# Swift client connection
connectionurl = swiftclient.Connection(key=password, authurl=authenticationurl, auth_version='3', os_options={"project_id": projectid, "user_id": userid, "region_name": region})

# Inititate variables
container_name = 'Saipriya_Test'
file_name = 'Sample_Upload.txt'
encodedfile = 'sample_test_saipriya.txt'
downloadedfile = 'sample_download.txt'
temporaryfile = "tmp.txt"

#Upload a file
def upload():
    verify_status = check_size()
    if verify_status == 1:
        connectionurl.put_container(container_name)
        print("\nContainer %s created successfully." % container_name)
        #Containers list
        print("\nContainer List:")
        for container in connectionurl.get_account()[1]:
            print(container['name'])
        file = open(file_name, 'r')
        cont = file.read()
        encr = k.encrypt(cont, padmode=pyDes.PAD_PKCS5)
        connectionurl.put_object(container_name, encodedfile, contents=encr)
        print('File encrypted successfully')
        print("Contents in the file:")
        print(encr)
        print('File uploaded successfully')
        file.close()
    elif verify_status == 2:
        print("Total size will exceed 10 MB")
        exit()
    elif verify_status == 3:
        print("Upload file size > 1 MB")
    elif verify_status == 4:
        print("File already exists in the container")


def check_size():
    totalsize = 0
    filesize = os.path.getsize(file_name)
    filesize = filesize / 2048

    for container in connectionurl.get_account()[1]:
        for data in connectionurl.get_container(container['name'])[1]:
            if encodedfile == data['name']:
                return 4
            totalsize = totalsize + data['bytes']
    totalsize = totalsize / 2048
    filesizeafter = filesize + totalsize
    if filesize < 1:
        if filesizeafter < 10:
            return 1
        else:
            return 2
    else:
        return 3

# Encrypt a file
def encrypt(file_name):
    readfile = open(file_name, 'r')
    cont_read = readfile.read()
    data = cont_read
    encrypt_message = k.encrypt(data,padmode=pyDes.PAD_PKCS5)
    readfile.close()
    print("Encrypted: %r" % encrypt_message)
    readfile = open(encodedfile, 'w')
    readfile.write(encrypt_message)
    readfile.close()

# Download the file
def download():
    download_file = connectionurl.get_object(container_name, encodedfile)
    fileContent = download_file[1]
    print(fileContent)
    decr = k.decrypt(fileContent,padmode=pyDes.PAD_PKCS5).decode('UTF-8')
    print(decr)
    file = open(downloadedfile, 'w')
    file.write(str(decr))
    file.close()
    print("\n File has been downloaded")

# Call the functions
upload()
download()

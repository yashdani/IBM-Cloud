import ibm_db, os, json

connection = ibm_db.connect("DATABASE=BLUDB;HOSTNAME=dashdb-txn-sbox-yp-dal09-04.services.dal.bluemix.net;PORT=50000;PROTOCOL=TCPIP;UID=vft79804;PWD=7c4r31g+3bwb6fxf;","","")

import os
import argparse
from socketClient import SocketClient
from configReader import ConfigPyFiTransfer


class PyFiTransfer:
    
    #Function to convert fully qualified file path into byte array (Socket transfer needs bytes)
    def getBytesfromFile(self,filename):
        try:
            fh = open(filename, 'rb')
            ba = bytearray(fh.read())
            return ba
        finally:
            fh.close()

    #TODO : Logic -> Sendcommand|DESTINATION_FILE_PATH|DESTINATION_FILE_NAME|DATA_OF_FILE_IN_BYTES
    #Example : FILE_KEY|/home/test/dest/path|thefileToBetransferred.txt|Thedatawithinthefileasbytes
    def createFileTransferCommand(self,destinationFullyQualifiedFileName,fileData):
        cmd = "FILE_KEY|"+destinationFullyQualifiedFileName+"|"+fileData
        return bytearray(cmd,'utf8')

# Correctly very naive approach will be changed later 
# populate the config object with the configuration in file transfer.yml (Look at configReader.py)
# From the config , get the source file path and file details and use the cofig destination details to transfer 
# file via socket 
#------------------Main Program---------------#
def main():
    try:

        parser = argparse.ArgumentParser(description='use --help for understanding params')

        parser.add_argument('-cf','--config_file', default='transfer.yml', help="Enter the fully qualified path to read config")
        parser.add_argument('-ip','--dest_ip', default='localhost', help="Enter the destination IP address")
        parser.add_argument('-port','--dest_port', default='9999', help="Enter the destination port address")
        parser.add_argument('-p', '--dest_file_path', default='', help="Enter the destination path for file transfer")
        parser.add_argument('-f', '--source_file', default='', help="Enter the file path to be entered from localhost address")
        configObj = ConfigPyFiTransfer()
        pft = PyFiTransfer()
        sock = SocketClient()
        configObj.getPyFiTransferConfig()
        fq_src_filename = os.path.join(configObj.source_file_path,configObj.source_file_name)
        fq_dest_filename = os.path.join(configObj.destination_folder,configObj.source_file_name)
        srcfile = open(fq_src_filename,"r")
        data_to_send = pft.createFileTransferCommand(fq_dest_filename,srcfile.read())
        sock.connect(configObj.destination_host,configObj.destination_port)
        sock.transfer(data_to_send)
    except Exception as e:
        print(e)
        
    finally:
        sock.close()

if __name__ == "__main__":
    main()
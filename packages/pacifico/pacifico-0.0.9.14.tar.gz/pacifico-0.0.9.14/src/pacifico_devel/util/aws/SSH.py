"""Copyright © 2020 Burrus Financial Intelligence, Ltda. (hereafter, BFI) Permission to include in application
software or to make digital or hard copies of part or all of this work is subject to the following licensing
agreement.
BFI Software License Agreement: Any User wishing to make a commercial use of the Software must contact BFI
at jacques.burrus@bfi.lat to arrange an appropriate license. Commercial use includes (1) integrating or incorporating
all or part of the source code into a product for sale or license by, or on behalf of, User to third parties,
or (2) distribution of the binary or source code to third parties for use with a commercial product sold or licensed
by, or on behalf of, User. """

import paramiko
import time
from ..aws import EC2, Enumerations
from ..cfg import Configuration


def connectSSH(ip_address, pemFilePath):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    privkey = paramiko.RSAKey.from_private_key_file(pemFilePath)
    try:
        client.connect(hostname=ip_address, username='centos', pkey=privkey)
        return client
    except (Exception, paramiko.BadHostKeyException, paramiko.AuthenticationException, paramiko.SSHException) as exception:
        print(exception)
        return __buildErrorOutput(str(exception))


def connectSSHByInstanceId(instanceId, pemFilePath, awsAccessKey, awsSecretKey):
    ip_address = EC2.getInstancePublicIPAddress(instanceId, awsAccessKey, awsSecretKey)
    client = connectSSH(ip_address, pemFilePath)
    return client


def __buildErrorOutput(message):
    status = 1
    error = message
    out = 'error'
    return status, error, out


def __executeCommandWithoutWaitingForCompletionUsingSudo(command, client):
    if not isinstance(client, tuple):
        client.get_transport()
        client.exec_command(command, get_pty=True)
        status = 0
        error = ''
        out = 'Sent without waiting for completion and with sudo permissions'
        return status, error, out
    else:
        return client


def __executeCommandWithoutWaitingForCompletion(command, client):
    if not isinstance(client, tuple):
        client.exec_command(command)
        status = 0
        error = ''
        out = 'Sent without waiting for completion'
        return status, error, out
    else:
        return client


def __executeCommandWaitingForCompletion(command, client, timeout):
    if not isinstance(client, tuple):
        stdin, stdout, stderr = client.exec_command(command, timeout=timeout)
        status = stdout.channel.recv_exit_status()
        error = stderr.read().decode('UTF-8')
        out = stdout.read().decode('UTF-8')
        return status, error, out
    else:
        return client


def __executeCommand(command, client, waitForCompletion=Enumerations.WaitForCompletion.Wait):
    if waitForCompletion == Enumerations.WaitForCompletion.NotWait:
        return __executeCommandWithoutWaitingForCompletion(command, client)
    elif waitForCompletion == Enumerations.WaitForCompletion.StartStop:
        return __executeCommandWithoutWaitingForCompletionUsingSudo(command, client)
    else:
        if waitForCompletion == Enumerations.WaitForCompletion.Wait:
            timeout = None
        else:
            timeout = waitForCompletion.getValue()
        return __executeCommandWaitingForCompletion(command, client, timeout)


def executeCommand(command, client, instanceId, waitForCompletion=Enumerations.WaitForCompletion.Wait,
                   awsAccessKey=None, awsSecretKey=None, pemFilePath=None):
    if command[:5] == './bfi':
        command = EC2.__getRoot() + command
        logFilepath = '/bfi/log/bfi_log_{}.txt'.format(instanceId)
        if waitForCompletion == Enumerations.WaitForCompletion.NotWait or waitForCompletion == Enumerations.WaitForCompletion.StartStop:
            # 2>&1: https://unix.stackexchange.com/questions/45913/is-there-a-way-to-redirect-nohup-output-to-a-log-file-other-than-nohup-out
            # command = 'ls'  # Tester
            command = command + ' > {} 2>&1'.format(logFilepath)
            if waitForCompletion == Enumerations.WaitForCompletion.StartStop:
                # shutdown:  # https://dev.to/aws/auto-stop-ec2-instances-when-they-finish-a-task-2f0i
                # sudo: https://www.youtube.com/watch?v=fVOFWehhc38
                command = "sudo -b sh -c '" + '{ su - centos -c "' + command + '"; shutdown now -h; ' + "}'"
            else:
                # nohup + &: https://docs.aws.amazon.com/es_es/codebuild/latest/userguide/build-env-ref-background-tasks.html
                # setsid: https://unix.stackexchange.com/questions/432258/issues-with-nohup-on-linux-instance-on-ec2-amazon-web-services
                command = 'setsid nohup {} &'.format(command)
        else:
            # | tee: https://stackoverflow.com/questions/13591374/command-output-redirect-to-file-and-terminal
            # exitcode fix: https://stackoverflow.com/questions/6871859/piping-command-output-to-tee-but-also-save-exit-code-of-command
            command = 'set -o pipefail && ' + command + ' 2>&1 | tee {}'.format(logFilepath)
        if waitForCompletion == Enumerations.WaitForCompletion.StartStop:
            if not EC2.isInstanceRunning(instanceId, awsAccessKey, awsSecretKey):
                EC2.startInstace(instanceId, awsAccessKey, awsSecretKey)
                time.sleep(60)
                client = connectSSHByInstanceId(instanceId, pemFilePath, awsAccessKey, awsSecretKey)
            return __executeCommand(command, client, waitForCompletion)
        return __executeCommand(command, client, waitForCompletion)
    else:
        return __buildErrorOutput('Invalid command')


def executeCommandInInstance(command, instanceId, pemFilePath, awsAccessKey, awsSecretKey,
                             waitForCompletion=Enumerations.WaitForCompletion.Wait):
    if EC2.isInstanceRunning(instanceId, awsAccessKey, awsSecretKey):
        client = connectSSHByInstanceId(instanceId, pemFilePath, awsAccessKey, awsSecretKey)
        if isInstanceBusy(client):
            return __buildErrorOutput('Instance is busy')
        else:
            return executeCommand(command, client, instanceId, waitForCompletion, awsAccessKey, awsSecretKey,
                                  pemFilePath)
    else:
        if waitForCompletion == Enumerations.WaitForCompletion.StartStop:
            client = connectSSHByInstanceId(instanceId, pemFilePath, awsAccessKey, awsSecretKey)
            return executeCommand(command, client, instanceId, waitForCompletion, awsAccessKey, awsSecretKey,
                                  pemFilePath)
        else:
            return __buildErrorOutput('Instance is stopped')


def copyFileFromInstance(filePathInstance, filepathLocal, instanceId, pemFilePath, awsAccessKey, awsSecretKey):
    client = connectSSHByInstanceId(instanceId, pemFilePath, awsAccessKey, awsSecretKey)
    if not isinstance(client, tuple):
        ftp_client = client.open_sftp()
        try:
            ftp_client.get(filePathInstance, filepathLocal)
        except:
            ftp_client.close()
            client.close()
        ftp_client.close()
        client.close()


def readFileFromInstance(filePathInstance, instanceId, pemFilePath, awsAccessKey, awsSecretKey):
    client = connectSSHByInstanceId(instanceId, pemFilePath, awsAccessKey, awsSecretKey)
    if not isinstance(client, tuple):
        ftp_client = client.open_sftp()
        dataAsString = ftp_client.open(filePathInstance, mode='r').read().decode("utf-8")
        ftp_client.close()
        client.close()
        return dataAsString
    else:
        return str(client)


def writeFileToInstance(filePathInstance, filepathLocal, instanceId, pemFilePath, awsAccessKey, awsSecretKey):
    client = connectSSHByInstanceId(instanceId, pemFilePath, awsAccessKey, awsSecretKey)
    if not isinstance(client, tuple):
        ftp_client = client.open_sftp()
        ftp_client.put(filepathLocal, filePathInstance)
        ftp_client.close()
        client.close()


def writeFileStringToInstance(stringData, filePath, instanceId, pemFilePath, awsAccessKey, awsSecretKey):
    client = connectSSHByInstanceId(instanceId, pemFilePath, awsAccessKey, awsSecretKey)
    if not isinstance(client, tuple):
        ftp_client = client.open_sftp()
        file = ftp_client.file(filePath, "a")
        file.write(stringData)
        file.flush()
        ftp_client.close()
        client.close()


def deleteFileFromInstance(filePathInstance, instanceId, pemFilePath, awsAccessKey, awsSecretKey):
    client = connectSSHByInstanceId(instanceId, pemFilePath, awsAccessKey, awsSecretKey)
    if not isinstance(client, tuple):
        ftp_client = client.open_sftp()
        ftp_client.remove(filePathInstance)
        ftp_client.close()
        client.close()

def renameFileFromInstance(filePathInstance, newFilePathInstance, instanceId, pemFilePath, awsAccessKey, awsSecretKey):
    client = connectSSHByInstanceId(instanceId, pemFilePath, awsAccessKey, awsSecretKey)
    if not isinstance(client, tuple):
        ftp_client = client.open_sftp()
        ftp_client.rename(filePathInstance, newFilePathInstance)
        ftp_client.close()
        client.close()


def getRunningProcessesInInstance(client):
    command = 'ps -A'  # == 'ps -e'
    status, error, out = __executeCommand(command, client)
    return out


def isProcessRunningInInstance(processName, client):
    processesString = getRunningProcessesInInstance(client)
    if processName in processesString:
        return True
    else:
        return False


def isInstanceBusy(client):
    processName = 'bfi'
    return isProcessRunningInInstance(processName, client)


if __name__ == '__main__':
    import time

    awsAccessKey = Configuration.get('AWS_ACCESS_KEY')
    awsSecretKey = Configuration.get('AWS_SECRET_KEY')
    instanceId = Configuration.get('COMPUTER_2_INSTANCE_ID')  # Configuration.get('COMPUTER_STATIC_2_INSTANCE_ID')
    pemFilePath = 'computer_key.pem'
    # Test commands

    command = './bfi_api -datawarehouse -refresh'
    statusCode, error, out = executeCommandInInstance(command, instanceId, pemFilePath, awsAccessKey, awsSecretKey,
                                                      Enumerations.WaitForCompletion.StartStop)
    print('out:')
    print(out)
    print('error:')
    print(error)
    print('statusCode:', statusCode)
    '''
    while True:
        client = connectSSHByInstanceId(instanceId, pemFilePath, awsAccessKey, awsSecretKey)
        print(isInstanceBusy(client))
        time.sleep(30)

    # Test waitForCompletion
    command = './bfi_api -bcs -upload -parameters' #'./bfi_api -help'  # './bfi_api ls'
    timeStart = time.time()
    statusCode, error, out = executeCommandInInstance(command, instanceId, pemFilePath, awsAccessKey, awsSecretKey)
    print(time.time() - timeStart)
    print(out)
    print(error)
    print(statusCode)
    print('-------------------------------')
    timeStart = time.time()
    statusCode, error, out = executeCommandInInstance(command, instanceId, pemFilePath, awsAccessKey, awsSecretKey, False)
    print(time.time() - timeStart)
    print(out)
    print(error)
    print(statusCode)
    #writeFileStringToInstance('12345', EC2.__getRoot() + 'test.txt', instanceId, pemFilePath, awsAccessKey, awsSecretKey)
    #writeFileToInstance(EC2.__getRoot() + 'computer_key.pem', 'tmp/computer_key.pem', instanceId, pemFilePath, awsAccessKey, awsSecretKey)
    #copyFileFromInstance(EC2.__getRoot() + 'test.txt', 'tmp/test.txt', instanceId, pemFilePath, awsAccessKey, awsSecretKey)
    #file = readFileFromInstance(EC2.__getRoot() + 'test.txt', instanceId, pemFilePath, awsAccessKey, awsSecretKey)
    #print(file)
    '''
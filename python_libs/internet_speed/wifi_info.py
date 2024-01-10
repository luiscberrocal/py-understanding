import subprocess


def get_wifi_ssid():
    subprocess_result = subprocess.Popen('iwgetid -r', shell=True, stdout=subprocess.PIPE)
    subprocess_output = subprocess_result.communicate()[0], subprocess_result.returncode
    network_name = subprocess_output[0].decode('utf-8')
    return network_name



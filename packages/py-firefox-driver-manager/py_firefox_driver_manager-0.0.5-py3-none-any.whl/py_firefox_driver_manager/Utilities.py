import sys
import os
import requests
import subprocess
import urllib.request
import urllib.error
import logging
import tarfile
import zipfile
from platinfo import PlatInfo
import glob

__author__ = 'Hamed  hamed.minaei@gmail.com'

DEFAULT_FILE_EXTENSIONS = {'linux': 'tar.gz',
                           'mac': 'tar.gz',
                           'win': 'zip'}

class GeckoFireFoxdriverManager:

    def __init__(self):
        self.version = self.get_latest_version()
        self.platform = None
        self.architecture = self.get_platform_architecture()
        self.directory = self.get_install_directory()
        pass

    def get_latest_version(self):
        response = requests.get('https://api.github.com/repos/mozilla/geckodriver/releases/latest')
        data = response.json()
        version = data['tag_name']
        return version


    def get_platform_architecture(self):
        if sys.platform.startswith('linux') and sys.maxsize > 2 ** 32:
            platform = 'linux'
            architecture = '64'
        elif sys.platform.startswith('linux'):
            platform = 'linux'
            architecture = '32'
        elif sys.platform == 'darwin':
            platform = 'mac'
            architecture = 'os'
        elif sys.platform.startswith('win') and sys.maxsize > 2 ** 32:
            platform = 'win'
            architecture = '64'
        elif sys.platform.startswith('win'):
            platform = 'win'
            architecture = '32'
        else:
            raise RuntimeError('Could not determine geckodriver download URL for this platform.')
        self.platform = platform
        self.architecture = architecture
        return architecture

    def get_downlaod_url(self):
        full_url = 'https://github.com/mozilla/geckodriver/releases/download/'+\
                   self.version+'/'+'geckodriver-'+self.version+'-'+\
                   self.platform+self.architecture+'.'+DEFAULT_FILE_EXTENSIONS[self.platform]
        return full_url

    def uncompress(self, file, directory):
        if self.platform == 'win':
            with zipfile.ZipFile(file, 'r') as zip_ref:
                zip_ref.extractall(directory)
        else:
            tar = tarfile.open(fileobj=file, mode='r:gz')
            tar.extractall(directory)
            tar.close()

    def get_install_directory(self):
        current_dir = os.path.abspath(os.path.abspath(os.getcwd()))
        os.chdir(current_dir)
        if not os.path.exists('firefox-geckodriver'):
            os.makedirs('firefox-geckodriver')
        return os.path.join(current_dir, 'firefox-geckodriver')

    def get_firefox_version(self):
        """
        :return: the version of firefox installed on client
        """

        if self.platform == 'linux':
            with subprocess.Popen(['firefox', '--version'], stdout=subprocess.PIPE) as proc:
                version = proc.stdout.read().decode('utf-8').replace('Mozilla Firefox', '').strip()
        elif self.platform == 'mac':
            process = subprocess.Popen(['/Applications/Firefox.app/Contents/MacOS/firefox', '--version'],
                                       stdout=subprocess.PIPE)
            version = process.communicate()[0].decode('UTF-8').replace('Mozilla Firefox', '').strip()
        elif self.platform == 'win':
            path1 = 'C:\\PROGRA~1\\Mozilla Firefox\\firefox.exe'
            path2 = 'C:\\PROGRA~2\\Mozilla Firefox\\firefox.exe'
            if os.path.exists(path1):
                process = subprocess.Popen([path1, '-v', '|', 'more'], stdout=subprocess.PIPE)
            elif os.path.exists(path2):
                process = subprocess.Popen([path2, '-v', '|', 'more'], stdout=subprocess.PIPE)
            else:
                return
            version = process.communicate()[0].decode('UTF-8').replace('Mozilla Firefox', '').strip()
        else:
            return
        return version
    
    def install_firefox(self):
        command = 'mozdownload --version=latest --destination='+self.get_install_directory()
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        if self.platform=='win':
           path = self.directory
           file_names = glob.glob(path+'/*firefox*.exe', recursive=True)
           if len(file_names)>0:
                 returned_value = subprocess.call(file_names[0], shell=True)
        elif self.platform=='linux':
            command = 'sudo apt install firefox'
            process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
            output, error = process.communicate()

    def check_firefox_installed(self):
        firefox_version = self.get_firefox_version()
        if not firefox_version:
            self.install_firefox()

    def download_geckodriver(self):
        url = self.get_downlaod_url()
        filenme = os.path.join(self.directory, 'geckodriver-'+self.version+'.'
                               +DEFAULT_FILE_EXTENSIONS[self.platform])
        urllib.request.urlretrieve(url, filenme)

    def install_geckodriver(self):
        self.check_firefox_installed()
        zipfilename = os.path.join(self.directory, 'geckodriver-'+self.version+'.'
                               +DEFAULT_FILE_EXTENSIONS[self.platform])
        if not os.path.isfile(zipfilename):
            self.download_geckodriver()

        file_names = glob.glob(self.directory + '/*geckodriver*', recursive=True)
        file_names.remove(zipfilename)
        if len(file_names)>0:
            return file_names[0]
        else:
            self.uncompress(zipfilename, self.directory)
            file_names = glob.glob(self.directory + '/*geckodriver*', recursive=True)
            file_names.remove(zipfilename)
            return file_names[0]












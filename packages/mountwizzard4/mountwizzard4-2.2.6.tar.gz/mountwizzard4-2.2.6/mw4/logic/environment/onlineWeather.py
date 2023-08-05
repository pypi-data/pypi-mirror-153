############################################################
# -*- coding: utf-8 -*-
#
#       #   #  #   #   #    #
#      ##  ##  #  ##  #    #
#     # # # #  # # # #    #  #
#    #  ##  #  ##  ##    ######
#   #   #   #  #   #       #
#
# Python-based Tool for interaction with the 10micron mounts
# GUI with PyQT5 for python
#
# written in python3, (c) 2019-2022 by mworion
# Licence APL2.0
#
###########################################################
# standard libraries
import logging

# external packages
import PyQt5.QtCore
import numpy as np
import requests

# local imports
from base.tpool import Worker


class WeatherSignals(PyQt5.QtCore.QObject):
    """
    """

    __all__ = ['WeatherSignals']
    dataReceived = PyQt5.QtCore.pyqtSignal(object)

    serverConnected = PyQt5.QtCore.pyqtSignal()
    serverDisconnected = PyQt5.QtCore.pyqtSignal(object)
    deviceConnected = PyQt5.QtCore.pyqtSignal(str)
    deviceDisconnected = PyQt5.QtCore.pyqtSignal(str)


class OnlineWeather(PyQt5.QtCore.QObject):
    """
    """

    __all__ = ['OnlineWeather']
    log = logging.getLogger(__name__)

    def __init__(self, app=None):
        super().__init__()

        self.app = app
        self.threadPool = app.threadPool
        self.signals = WeatherSignals()
        self.location = app.mount.obsSite.location

        # minimum set for driver package built in
        self.framework = ''
        self.run = {
            'onlineWeather': self
        }
        self.deviceName = ''

        self.data = {}
        self.defaultConfig = {
            'framework': '',
            'frameworks': {
                'onlineWeather': {
                    'deviceName': 'OnlineWeather',
                    'apiKey': '',
                    'hostaddress': 'api.openweathermap.org',
                }
            }
        }
        self.running = False
        self.hostaddress = ''
        self.apiKey = ''
        self._online = False
        self.app.update10s.connect(self.updateOpenWeatherMapData)

    @property
    def online(self):
        return self._online

    @online.setter
    def online(self, value):
        self._online = value
        if value:
            self.updateOpenWeatherMapData()

    def startCommunication(self, loadConfig=False):
        """
        :param loadConfig:
        :return: success of reconnecting to server
        """
        if not self.apiKey:
            return False

        self.running = True
        self.updateOpenWeatherMapData()
        self.signals.deviceConnected.emit('OnlineWeather')
        return True

    def stopCommunication(self):
        """
        :return: success of reconnecting to server
        """
        self.running = False
        self.data.clear()
        self.signals.deviceDisconnected.emit('OnlineWeather')
        return True

    @staticmethod
    def getDewPoint(tempAir, relativeHumidity):
        """
        Compute the dew point in degrees Celsius

        :param tempAir: current ambient temperature in degrees Celsius
        :param relativeHumidity: relative humidity in %
        :return: the dew point in degrees Celsius
        """
        if tempAir < -40 or tempAir > 80:
            return 0
        if relativeHumidity < 0 or relativeHumidity > 100:
            return 0

        A = 17.27
        B = 237.7
        alpha = ((A * tempAir) / (B + tempAir)) + np.log(relativeHumidity / 100.0)
        dewPoint = (B * alpha) / (A - alpha)
        return dewPoint

    def updateOpenWeatherMapDataWorker(self, data=None):
        """
        :param data:
        :return: success
        """
        if data is None:
            self.signals.dataReceived.emit(None)
            return False

        if 'list' not in data:
            self.signals.dataReceived.emit(None)
            return False

        if len(data['list']) == 0:
            self.signals.dataReceived.emit(None)
            return False

        val = data['list'][0]
        self.log.trace(f'onlineWeatherData:[{val}]')

        if 'main' in val:
            self.data['temperature'] = val['main']['temp'] - 273.15
            self.data['pressure'] = val['main']['grnd_level']
            self.data['humidity'] = val['main']['humidity']
            self.data['dewPoint'] = self.getDewPoint(self.data['temperature'],
                                                     self.data['humidity'])
        if 'clouds' in val:
            self.data['cloudCover'] = val['clouds']['all']

        if 'wind' in val:
            self.data['windSpeed'] = val['wind']['speed']
            self.data['windDir'] = val['wind']['deg']

        if 'rain' in val:
            self.data['rain'] = val['rain']['3h']

        self.signals.dataReceived.emit(self.data)
        return True

    def getOpenWeatherMapDataWorker(self, url=''):
        """
        :param url:
        :return: data
        """
        if not url:
            return None

        try:
            data = requests.get(url, timeout=30)
        except TimeoutError:
            self.log.warning(f'[{url}] not reachable')
            return None
        except Exception as e:
            self.log.critical(f'[{url}] general exception: [{e}]')
            return None
        if data.status_code != 200:
            self.log.warning(f'[{url}] status is not 200')
            return None

        return data.json()

    def getOpenWeatherMapData(self, url=''):
        """
        :param url:
        :return: true for test purpose
        """
        worker = Worker(self.getOpenWeatherMapDataWorker, url)
        worker.signals.result.connect(self.updateOpenWeatherMapDataWorker)
        self.threadPool.start(worker)
        return True

    def updateOpenWeatherMapData(self):
        """
        updateOpenWeatherMap downloads the actual OpenWeatherMap image and
        displays it in environment tab. it checks first if online is set,
        otherwise not download will take place. it will be updated every 10 minutes.

        :return: success
        """
        if not self.online and self.running:
            self.signals.dataReceived.emit(None)
            self.stopCommunication()
            return False
        if not self.running:
            return False

        lat = self.location.latitude.degrees
        lon = self.location.longitude.degrees

        webSite = f'http://{self.hostaddress}/data/2.5/forecast'
        url = f'{webSite}?lat={lat:1.2f}&lon={lon:1.2f}&APPID={self.apiKey}'
        self.getOpenWeatherMapData(url=url)
        self.log.debug(f'{url}')
        return True

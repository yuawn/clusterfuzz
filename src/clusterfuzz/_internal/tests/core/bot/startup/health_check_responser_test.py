# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""health check reposnser tests."""

import threading
import unittest

import mock
import requests

from python.bot.startup.health_responser import EXPECTED_PROCESSES
from python.bot.startup.health_responser import RESPONSER_IP
from python.bot.startup.health_responser import RESPONSER_PORT
from python.bot.startup.health_responser import run_server

RESPONSER_ADDR = f'http://{RESPONSER_IP}:{RESPONSER_PORT}'


class HealthCheckResponserTest(unittest.TestCase):
  """Test health check responser."""

  def setUp(self):
    self.server_thread = threading.Thread(target=run_server)
    self.server_thread.daemon = True
    self.server_thread.start()

  @mock.patch('python.bot.startup.health_responser.os')
  def test_healthy(self, mock_os):
    mock_os.popen().read.return_value = ' '.join(EXPECTED_PROCESSES)
    self.assertEqual(200, requests.get(f'{RESPONSER_ADDR}').status_code)

  @mock.patch('python.bot.startup.health_responser.os')
  def test_run_terminated(self, mock_os):
    mock_os.popen().read.return_value = EXPECTED_PROCESSES[0]
    self.assertEqual(500, requests.get(f'{RESPONSER_ADDR}').status_code)

  @mock.patch('python.bot.startup.health_responser.os')
  def test_run_bot_terminated(self, mock_os):
    mock_os.popen().read.return_value = EXPECTED_PROCESSES[1]
    self.assertEqual(500, requests.get(f'{RESPONSER_ADDR}').status_code)

  @mock.patch('python.bot.startup.health_responser.os')
  def test_both_terminated(self, mock_os):
    mock_os.popen().read.return_value = ''
    self.assertEqual(500, requests.get(f'{RESPONSER_ADDR}').status_code)
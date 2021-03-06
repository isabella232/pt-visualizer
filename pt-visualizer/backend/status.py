'''
// Copyright (c) 2015-2019 Intel Corporation
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
'''
import os
import psycopg2
import psycopg2.extras
import ConfigParser

SAT_HOME = os.environ.get('SAT_HOME')
# Set SAT_HOME for rest of the backend
if SAT_HOME is None:
    SAT_HOME = os.path.realpath(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)), '..', '..'))
    os.environ['SAT_HOME'] = SAT_HOME

CONFIG_FILE = os.path.join(SAT_HOME, 'conf', 'db_config')

#Singleton
ins = None
def getStatus():
    global ins
    if not ins:
        ins = Status()
    return ins

class Status(object):
    def __init__(self):
        self.dbconfig = {}
        self._initConfig()
        self.conn = psycopg2.connect(dbname=self.dbconfig['dbname'],
            user=self.dbconfig['user'], password=self.dbconfig['password'])
        self.cursor = self.conn.cursor()

    def getDbConfig(self, key):
        if key not in self.dbconfig:
            raise KeyError('DB config missing key ' + key)
        return self.dbconfig[key]

    def _initConfig(self):
        if not os.path.isfile(CONFIG_FILE):
            raise IOError("Config file not found!")
        self.config = ConfigParser.ConfigParser()
        self.config.read(CONFIG_FILE)
        self.dbconfig['dbname'] = self.config.get('DB', 'dbname')
        self.dbconfig['user'] = self.config.get('DB', 'user')
        self.dbconfig['password'] = self.config.get('DB', 'password')

    def createTracesTable(self):
        self.cursor.execute('CREATE TABLE IF NOT EXISTS public.traces (id serial, name varchar(256), description varchar(2048),' +
                     'created date, device varchar(2048), cpu_count int4, length int DEFAULT 0, ' +
                     "build varchar(2048) DEFAULT '', contact varchar(2048) DEFAULT '', " +
                     "screenshot boolean DEFAULT 'false', " +
                     "status smallint default 0, info varchar(2048) DEFAULT '', PRIMARY KEY(id))")
        self.conn.commit()


#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import warnings
from ai.h2o.sparkling.SharedBackendConfUtils import SharedBackendConfUtils


class SharedBackendConf(SharedBackendConfUtils):

    #
    # Getters
    #

    def cloudName(self):
        return self._get_option(self._jconf.cloudName())

    def isH2OReplEnabled(self):
        return self._jconf.isH2OReplEnabled()

    def backendClusterMode(self):
        return self._jconf.backendClusterMode()

    def isProgressBarEnabled(self):
        return self._jconf.isProgressBarEnabled()

    def isModelPrintAfterTrainingEnabled(self):
        return self._jconf.isModelPrintAfterTrainingEnabled()

    def scalaIntDefaultNum(self):
        return self._jconf.scalaIntDefaultNum()

    def isClusterTopologyListenerEnabled(self):
        return self._jconf.isClusterTopologyListenerEnabled()

    def isSparkVersionCheckEnabled(self):
        return self._jconf.isSparkVersionCheckEnabled()

    def isFailOnUnsupportedSparkParamEnabled(self):
        return self._jconf.isFailOnUnsupportedSparkParamEnabled()

    def jks(self):
        return self._get_option(self._jconf.jks())

    def jksPass(self):
        return self._get_option(self._jconf.jksPass())

    def jksAlias(self):
        return self._get_option(self._jconf.jksAlias())

    def sslCACert(self):
        return self._get_option(self._jconf.sslCACert())

    def hashLogin(self):
        return self._jconf.hashLogin()

    def ldapLogin(self):
        return self._jconf.ldapLogin()

    def kerberosLogin(self):
        return self._jconf.kerberosLogin()

    def loginConf(self):
        return self._get_option(self._jconf.loginConf())

    def userName(self):
        return self._get_option(self._jconf.userName())

    def password(self):
        return self._get_option(self._jconf.password())

    def sslConf(self):
        return self._get_option(self._jconf.sslConf())

    def autoFlowSsl(self):
        return self._jconf.autoFlowSsl()

    def logLevel(self):
        return self._jconf.logLevel()

    def logDir(self):
        return self._get_option(self._jconf.logDir())

    def backendHeartbeatInterval(self):
        return self._jconf.backendHeartbeatInterval()

    def cloudTimeout(self):
        return self._jconf.cloudTimeout()

    def nodeNetworkMask(self):
        return self._get_option(self._jconf.nodeNetworkMask())

    def stacktraceCollectorInterval(self):
        return self._jconf.stacktraceCollectorInterval()

    def contextPath(self):
        return self._get_option(self._jconf.contextPath())

    def flowScalaCellAsync(self):
        return self._jconf.flowScalaCellAsync()

    def maxParallelScalaCellJobs(self):
        return self._jconf.maxParallelScalaCellJobs()

    def internalPortOffset(self):
        return self._jconf.internalPortOffset()

    def basePort(self):
        return self._jconf.basePort()

    def mojoDestroyTimeout(self):
        return self._jconf.mojoDestroyTimeout()

    def extraProperties(self):
        return self._get_option(self._jconf.extraProperties())

    def flowExtraHttpHeaders(self):
        return self._get_option(self._jconf.flowExtraHttpHeaders())

    def flowProxyRequestMaxSize(self):
        return self._jconf.flowProxyRequestMaxSize()

    def flowProxyResponseMaxSize(self):
        return self._jconf.flowProxyResponseMaxSize()

    def isInternalSecureConnectionsEnabled(self):
        return self._jconf.isInternalSecureConnectionsEnabled()

    def isInsecureXGBoostAllowed(self):
        return self._jconf.isInsecureXGBoostAllowed()

    def flowDir(self):
        return self._get_option(self._jconf.flowDir())

    def clientIp(self):
        return self._get_option(self._jconf.clientIp())

    def clientWebPort(self):
        return self._jconf.clientWebPort()

    def clientVerboseOutput(self):
        return self._jconf.clientVerboseOutput()

    def clientNetworkMask(self):
        return self._get_option(self._jconf.clientNetworkMask())

    def clientFlowBaseurlOverride(self):
        return self._get_option(self._jconf.clientFlowBaseurlOverride())

    def runsInExternalClusterMode(self):
        return self._jconf.runsInExternalClusterMode()

    def runsInInternalClusterMode(self):
        return self._jconf.runsInInternalClusterMode()

    def clientCheckRetryTimeout(self):
        return self._jconf.clientCheckRetryTimeout()

    def verifySslCertificates(self):
        return self._jconf.verifySslCertificates()

    def isSslHostnameVerificationInInternalRestConnectionsEnabled(self):
        return self._jconf.isSslHostnameVerificationInInternalRestConnectionsEnabled()

    def isSslCertificateVerificationInInternalRestConnectionsEnabled(self):
        return self._jconf.isSslCertificateVerificationInInternalRestConnectionsEnabled()

    def isKerberizedHiveEnabled(self):
        return self._jconf.isKerberizedHiveEnabled()

    def hiveHost(self):
        return self._get_option(self._jconf.hiveHost())

    def hivePrincipal(self):
        return self._get_option(self._jconf.hivePrincipal())

    def hiveJdbcUrlPattern(self):
        return self._get_option(self._jconf.hiveJdbcUrlPattern())

    def hiveToken(self):
        return self._get_option(self._jconf.hiveToken())

    def icedDir(self):
        return self._get_option(self._jconf.icedDir())

    def restApiTimeout(self):
        return self._jconf.restApiTimeout()

    def nthreads(self):
        return self._jconf.nthreads()


    #
    # Setters
    #

    def setInternalClusterMode(self):
        self._jconf.setInternalClusterMode()
        return self

    def setExternalClusterMode(self):
        self._jconf.setExternalClusterMode()
        return self

    def setCloudName(self, arg0):
        self._jconf.setCloudName(arg0)
        return self

    def setNthreads(self, arg0):
        self._jconf.setNthreads(arg0)
        return self

    def setReplEnabled(self):
        self._jconf.setReplEnabled()
        return self

    def setReplDisabled(self):
        self._jconf.setReplDisabled()
        return self

    def setProgressBarEnabled(self):
        self._jconf.setProgressBarEnabled()
        return self

    def setProgressBarDisabled(self):
        self._jconf.setProgressBarDisabled()
        return self

    def setModelPrintAfterTrainingEnabled(self):
        self._jconf.setModelPrintAfterTrainingEnabled()
        return self

    def setModelPrintAfterTrainingDisabled(self):
        self._jconf.setModelPrintAfterTrainingDisabled()
        return self

    def setDefaultNumReplSessions(self, arg0):
        self._jconf.setDefaultNumReplSessions(arg0)
        return self

    def setClusterTopologyListenerEnabled(self):
        self._jconf.setClusterTopologyListenerEnabled()
        return self

    def setClusterTopologyListenerDisabled(self):
        self._jconf.setClusterTopologyListenerDisabled()
        return self

    def setSparkVersionCheckEnabled(self):
        self._jconf.setSparkVersionCheckEnabled()
        return self

    def setSparkVersionCheckDisabled(self):
        self._jconf.setSparkVersionCheckDisabled()
        return self

    def setFailOnUnsupportedSparkParamEnabled(self):
        self._jconf.setFailOnUnsupportedSparkParamEnabled()
        return self

    def setFailOnUnsupportedSparkParamDisabled(self):
        self._jconf.setFailOnUnsupportedSparkParamDisabled()
        return self

    def setJks(self, arg0):
        self._jconf.setJks(arg0)
        return self

    def setJksPass(self, arg0):
        self._jconf.setJksPass(arg0)
        return self

    def setJksAlias(self, arg0):
        self._jconf.setJksAlias(arg0)
        return self

    def setSslCACert(self, arg0):
        self._jconf.setSslCACert(arg0)
        return self

    def setHashLoginEnabled(self):
        self._jconf.setHashLoginEnabled()
        return self

    def setHashLoginDisabled(self):
        self._jconf.setHashLoginDisabled()
        return self

    def setLdapLoginEnabled(self):
        self._jconf.setLdapLoginEnabled()
        return self

    def setLdapLoginDisabled(self):
        self._jconf.setLdapLoginDisabled()
        return self

    def setKerberosLoginEnabled(self):
        self._jconf.setKerberosLoginEnabled()
        return self

    def setKerberosLoginDisabled(self):
        self._jconf.setKerberosLoginDisabled()
        return self

    def setLoginConf(self, arg0):
        self._jconf.setLoginConf(arg0)
        return self

    def setUserName(self, arg0):
        self._jconf.setUserName(arg0)
        return self

    def setPassword(self, arg0):
        self._jconf.setPassword(arg0)
        return self

    def setSslConf(self, arg0):
        self._jconf.setSslConf(arg0)
        return self

    def setAutoFlowSslEnabled(self):
        self._jconf.setAutoFlowSslEnabled()
        return self

    def setAutoFlowSslDisabled(self):
        self._jconf.setAutoFlowSslDisabled()
        return self

    def setLogLevel(self, arg0):
        self._jconf.setLogLevel(arg0)
        return self

    def setLogDir(self, arg0):
        self._jconf.setLogDir(arg0)
        return self

    def setBackendHeartbeatInterval(self, arg0):
        self._jconf.setBackendHeartbeatInterval(arg0)
        return self

    def setCloudTimeout(self, arg0):
        self._jconf.setCloudTimeout(arg0)
        return self

    def setNodeNetworkMask(self, arg0):
        self._jconf.setNodeNetworkMask(arg0)
        return self

    def setContextPath(self, arg0):
        self._jconf.setContextPath(arg0)
        return self

    def setStacktraceCollectorInterval(self, arg0):
        self._jconf.setStacktraceCollectorInterval(arg0)
        return self

    def setFlowScalaCellAsyncEnabled(self):
        self._jconf.setFlowScalaCellAsyncEnabled()
        return self

    def setFlowScalaCellAsyncDisabled(self):
        self._jconf.setFlowScalaCellAsyncDisabled()
        return self

    def setMaxParallelScalaCellJobs(self, arg0):
        self._jconf.setMaxParallelScalaCellJobs(arg0)
        return self

    def setInternalPortOffset(self, arg0):
        self._jconf.setInternalPortOffset(arg0)
        return self

    def setBasePort(self, arg0):
        self._jconf.setBasePort(arg0)
        return self

    def setMojoDestroyTimeout(self, arg0):
        self._jconf.setMojoDestroyTimeout(arg0)
        return self

    def setExtraProperties(self, arg0):
        self._jconf.setExtraProperties(arg0)
        return self

    def setFlowExtraHttpHeaders(self, *args):
        self._jconf.setFlowExtraHttpHeaders(*args)
        return self

    def setFlowProxyRequestMaxSize(self, arg0):
        self._jconf.setFlowProxyRequestMaxSize(arg0)
        return self

    def setFlowProxyResponseMaxSize(self, arg0):
        self._jconf.setFlowProxyResponseMaxSize(arg0)
        return self

    def setInternalSecureConnectionsEnabled(self):
        self._jconf.setInternalSecureConnectionsEnabled()
        return self

    def setInternalSecureConnectionsDisabled(self):
        self._jconf.setInternalSecureConnectionsDisabled()
        return self

    def setInsecureXGBoostAllowed(self):
        self._jconf.setInsecureXGBoostAllowed()
        return self

    def setInsecureXGBoostDenied(self):
        self._jconf.setInsecureXGBoostDenied()
        return self

    def setFlowDir(self, arg0):
        self._jconf.setFlowDir(arg0)
        return self

    def setClientIp(self, arg0):
        self._jconf.setClientIp(arg0)
        return self

    def setClientWebPort(self, arg0):
        self._jconf.setClientWebPort(arg0)
        return self

    def setClientVerboseEnabled(self):
        self._jconf.setClientVerboseEnabled()
        return self

    def setClientVerboseDisabled(self):
        self._jconf.setClientVerboseDisabled()
        return self

    def setClientNetworkMask(self, arg0):
        self._jconf.setClientNetworkMask(arg0)
        return self

    def setClientFlowBaseurlOverride(self, arg0):
        self._jconf.setClientFlowBaseurlOverride(arg0)
        return self

    def setClientCheckRetryTimeout(self, arg0):
        self._jconf.setClientCheckRetryTimeout(arg0)
        return self

    def setVerifySslCertificates(self, arg0):
        self._jconf.setVerifySslCertificates(arg0)
        return self

    def setSslHostnameVerificationInInternalRestConnectionsEnabled(self):
        self._jconf.setSslHostnameVerificationInInternalRestConnectionsEnabled()
        return self

    def setSslHostnameVerificationInInternalRestConnectionsDisabled(self):
        self._jconf.setSslHostnameVerificationInInternalRestConnectionsDisabled()
        return self

    def setSslCertificateVerificationInInternalRestConnectionsEnabled(self):
        self._jconf.setSslCertificateVerificationInInternalRestConnectionsEnabled()
        return self

    def setSslCertificateVerificationInInternalRestConnectionsDisabled(self):
        self._jconf.setSslCertificateVerificationInInternalRestConnectionsDisabled()
        return self

    def setKerberizedHiveEnabled(self):
        self._jconf.setKerberizedHiveEnabled()
        return self

    def setKerberizedHiveDisabled(self):
        self._jconf.setKerberizedHiveDisabled()
        return self

    def setHiveHost(self, arg0):
        self._jconf.setHiveHost(arg0)
        return self

    def setHivePrincipal(self, arg0):
        self._jconf.setHivePrincipal(arg0)
        return self

    def setHiveJdbcUrlPattern(self, arg0):
        self._jconf.setHiveJdbcUrlPattern(arg0)
        return self

    def setHiveToken(self, arg0):
        self._jconf.setHiveToken(arg0)
        return self

    def setIcedDir(self, arg0):
        self._jconf.setIcedDir(arg0)
        return self

    def setRestApiTimeout(self, arg0):
        self._jconf.setRestApiTimeout(arg0)
        return self

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

from ai.h2o.sparkling.ml.params.H2OMOJOModelParams import H2OSupervisedMOJOModelParams
from pyspark.ml.util import _jvm
from py4j.java_gateway import JavaObject
from ai.h2o.sparkling.Initializer import Initializer
from ai.h2o.sparkling.ml.models.H2OMOJOSettings import H2OMOJOSettings
from ai.h2o.sparkling.ml.params.H2OTypeConverters import H2OTypeConverters


class H2OStackedEnsembleMOJOModel(H2OSupervisedMOJOModelParams):

    @staticmethod
    def createFromMojo(pathToMojo, settings=H2OMOJOSettings.default()):
        # We need to make sure that Sparkling Water classes are available on the Spark driver and executor paths
        Initializer.load_sparkling_jar()
        javaModel = _jvm().ai.h2o.sparkling.ml.models.H2OStackedEnsembleMOJOModel.createFromMojo(pathToMojo, settings.toJavaObject())
        return H2OStackedEnsembleMOJOModel(javaModel)


    def getCrossValidationModels(self):
        cvModels = self._java_obj.getCrossValidationModelsAsArray()
        if cvModels is None:
            return None
        elif isinstance(cvModels, JavaObject):
            return [H2OStackedEnsembleMOJOModel(v) for v in cvModels]
        else:
            raise TypeError("Invalid type.")


    def getMetalearnerAlgorithm(self):
        value = self._java_obj.getMetalearnerAlgorithm()
        return value


    def getMetalearnerNfolds(self):
        value = self._java_obj.getMetalearnerNfolds()
        return value


    def getMetalearnerFoldAssignment(self):
        value = self._java_obj.getMetalearnerFoldAssignment()
        return value


    def getMetalearnerFoldCol(self):
        value = self._java_obj.getMetalearnerFoldCol()
        return value


    def getMetalearnerTransform(self):
        value = self._java_obj.getMetalearnerTransform()
        return value


    def getKeepLeveloneFrame(self):
        value = self._java_obj.getKeepLeveloneFrame()
        return value


    def getMetalearnerParams(self):
        value = self._java_obj.getMetalearnerParams()
        return value


    def getSeed(self):
        value = self._java_obj.getSeed()
        return value


    def getScoreTrainingSamples(self):
        value = self._java_obj.getScoreTrainingSamples()
        return value


    def getNfolds(self):
        value = self._java_obj.getNfolds()
        return value


    def getKeepCrossValidationModels(self):
        value = self._java_obj.getKeepCrossValidationModels()
        return value


    def getKeepCrossValidationPredictions(self):
        value = self._java_obj.getKeepCrossValidationPredictions()
        return value


    def getKeepCrossValidationFoldAssignment(self):
        value = self._java_obj.getKeepCrossValidationFoldAssignment()
        return value


    def getDistribution(self):
        value = self._java_obj.getDistribution()
        return value


    def getTweediePower(self):
        value = self._java_obj.getTweediePower()
        return value


    def getQuantileAlpha(self):
        value = self._java_obj.getQuantileAlpha()
        return value


    def getHuberAlpha(self):
        value = self._java_obj.getHuberAlpha()
        return value


    def getLabelCol(self):
        value = self._java_obj.getLabelCol()
        return value


    def getWeightCol(self):
        value = self._java_obj.getWeightCol()
        return value


    def getFoldCol(self):
        value = self._java_obj.getFoldCol()
        return value


    def getFoldAssignment(self):
        value = self._java_obj.getFoldAssignment()
        return value


    def getCategoricalEncoding(self):
        value = self._java_obj.getCategoricalEncoding()
        return value


    def getMaxCategoricalLevels(self):
        value = self._java_obj.getMaxCategoricalLevels()
        return value


    def getIgnoredCols(self):
        value = self._java_obj.getIgnoredCols()
        return H2OTypeConverters.scalaArrayToPythonArray(value)


    def getIgnoreConstCols(self):
        value = self._java_obj.getIgnoreConstCols()
        return value


    def getScoreEachIteration(self):
        value = self._java_obj.getScoreEachIteration()
        return value


    def getCheckpoint(self):
        value = self._java_obj.getCheckpoint()
        return value


    def getStoppingRounds(self):
        value = self._java_obj.getStoppingRounds()
        return value


    def getMaxRuntimeSecs(self):
        value = self._java_obj.getMaxRuntimeSecs()
        return value


    def getStoppingMetric(self):
        value = self._java_obj.getStoppingMetric()
        return value


    def getStoppingTolerance(self):
        value = self._java_obj.getStoppingTolerance()
        return value


    def getGainsliftBins(self):
        value = self._java_obj.getGainsliftBins()
        return value


    def getCustomMetricFunc(self):
        value = self._java_obj.getCustomMetricFunc()
        return value


    def getCustomDistributionFunc(self):
        value = self._java_obj.getCustomDistributionFunc()
        return value


    def getExportCheckpointsDir(self):
        value = self._java_obj.getExportCheckpointsDir()
        return value


    def getAucType(self):
        value = self._java_obj.getAucType()
        return value

    # Outputs


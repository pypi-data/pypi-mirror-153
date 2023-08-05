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

from warnings import warn
from pyspark import keyword_only
from ai.h2o.sparkling import Initializer
from ai.h2o.sparkling.ml.Utils import Utils
from ai.h2o.sparkling.ml.algos.H2OSupervisedAlgorithm import H2OSupervisedAlgorithm
from ai.h2o.sparkling.ml.params.H2OStackedEnsembleParams import H2OStackedEnsembleParams
from ai.h2o.sparkling.ml.algos.H2OStackedEnsembleExtras import H2OStackedEnsembleExtras


class H2OStackedEnsemble(H2OStackedEnsembleParams, H2OSupervisedAlgorithm, H2OStackedEnsembleExtras):

    @keyword_only
    def __init__(self,
                 blendingDataFrame=None,
                 baseAlgorithms=None,
                 columnsToCategorical=[],
                 keepBinaryModels=False,
                 withContributions=False,
                 dataFrameSerializer="ai.h2o.sparkling.utils.JSONDataFrameSerializer",
                 withLeafNodeAssignments=False,
                 namedMojoOutputColumns=True,
                 convertInvalidNumbersToNa=False,
                 detailedPredictionCol="detailed_prediction",
                 validationDataFrame=None,
                 featuresCols=[],
                 predictionCol="prediction",
                 convertUnknownCategoricalLevelsToNa=False,
                 splitRatio=1.0,
                 withStageResults=False,
                 metalearnerAlgorithm="AUTO",
                 metalearnerNfolds=0,
                 metalearnerFoldAssignment="AUTO",
                 metalearnerFoldCol=None,
                 metalearnerTransform="NONE",
                 keepLeveloneFrame=False,
                 metalearnerParams="",
                 seed=-1,
                 scoreTrainingSamples=10000,
                 modelId=None,
                 nfolds=0,
                 keepCrossValidationModels=True,
                 keepCrossValidationPredictions=False,
                 keepCrossValidationFoldAssignment=False,
                 parallelizeCrossValidation=True,
                 distribution="AUTO",
                 tweediePower=1.5,
                 quantileAlpha=0.5,
                 huberAlpha=0.9,
                 labelCol=None,
                 weightCol=None,
                 offsetCol=None,
                 foldCol=None,
                 foldAssignment="AUTO",
                 categoricalEncoding="AUTO",
                 maxCategoricalLevels=10,
                 ignoredCols=None,
                 ignoreConstCols=True,
                 scoreEachIteration=False,
                 checkpoint=None,
                 stoppingRounds=0,
                 maxRuntimeSecs=0.0,
                 stoppingMetric="AUTO",
                 stoppingTolerance=0.001,
                 gainsliftBins=-1,
                 customMetricFunc=None,
                 customDistributionFunc=None,
                 exportCheckpointsDir=None,
                 aucType="AUTO"):
        Initializer.load_sparkling_jar()
        super(H2OStackedEnsemble, self).__init__()
        self._java_obj = self._new_java_obj("ai.h2o.sparkling.ml.algos.H2OStackedEnsemble", self.uid)
        self._setDefaultValuesFromJava()
        kwargs = Utils.getInputKwargs(self)
        kwargs = self._updateInitKwargs(kwargs)

        if 'interactionPairs' in kwargs:
            warn("Interaction pairs are not supported!")
        self._set(**kwargs)
        self._transfer_params_to_java()

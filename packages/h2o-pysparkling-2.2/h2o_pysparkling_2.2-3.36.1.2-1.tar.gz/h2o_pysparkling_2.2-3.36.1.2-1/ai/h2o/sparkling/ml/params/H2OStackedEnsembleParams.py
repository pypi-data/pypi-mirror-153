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

from pyspark.ml.param import *
from ai.h2o.sparkling.ml.params.H2OTypeConverters import H2OTypeConverters
from ai.h2o.sparkling.ml.params.HasBlendingDataFrame import HasBlendingDataFrame
from ai.h2o.sparkling.ml.params.HasBaseAlgorithms import HasBaseAlgorithms


class H2OStackedEnsembleParams(HasBlendingDataFrame, HasBaseAlgorithms, Params):

    ##
    # Param definitions
    ##
    metalearnerAlgorithm = Param(
        Params._dummy(),
        "metalearnerAlgorithm",
        """Type of algorithm to use as the metalearner. Options include 'AUTO' (GLM with non negative weights; if validation_frame is present, a lambda search is performed), 'deeplearning' (Deep Learning with default parameters), 'drf' (Random Forest with default parameters), 'gbm' (GBM with default parameters), 'glm' (GLM with default parameters), 'naivebayes' (NaiveBayes with default parameters), or 'xgboost' (if available, XGBoost with default parameters).""",
        H2OTypeConverters.toEnumString("hex.ensemble.Metalearner$Algorithm"))

    metalearnerNfolds = Param(
        Params._dummy(),
        "metalearnerNfolds",
        """Number of folds for K-fold cross-validation of the metalearner algorithm (0 to disable or >= 2).""",
        H2OTypeConverters.toInt())

    metalearnerFoldAssignment = Param(
        Params._dummy(),
        "metalearnerFoldAssignment",
        """Cross-validation fold assignment scheme for metalearner cross-validation.  Defaults to AUTO (which is currently set to Random). The 'Stratified' option will stratify the folds based on the response variable, for classification problems.""",
        H2OTypeConverters.toEnumString("hex.Model$Parameters$FoldAssignmentScheme"))

    metalearnerFoldCol = Param(
        Params._dummy(),
        "metalearnerFoldCol",
        """Column with cross-validation fold index assignment per observation for cross-validation of the metalearner.""",
        H2OTypeConverters.toNullableString())

    metalearnerTransform = Param(
        Params._dummy(),
        "metalearnerTransform",
        """Transformation used for the level one frame.""",
        H2OTypeConverters.toEnumString("hex.ensemble.StackedEnsembleModel$StackedEnsembleParameters$MetalearnerTransform"))

    keepLeveloneFrame = Param(
        Params._dummy(),
        "keepLeveloneFrame",
        """Keep level one frame used for metalearner training.""",
        H2OTypeConverters.toBoolean())

    metalearnerParams = Param(
        Params._dummy(),
        "metalearnerParams",
        """Parameters for metalearner algorithm""",
        H2OTypeConverters.toString())

    seed = Param(
        Params._dummy(),
        "seed",
        """Seed for random numbers; passed through to the metalearner algorithm. Defaults to -1 (time-based random number)""",
        H2OTypeConverters.toInt())

    scoreTrainingSamples = Param(
        Params._dummy(),
        "scoreTrainingSamples",
        """Specify the number of training set samples for scoring. The value must be >= 0. To use all training samples, enter 0.""",
        H2OTypeConverters.toInt())

    modelId = Param(
        Params._dummy(),
        "modelId",
        """Destination id for this model; auto-generated if not specified.""",
        H2OTypeConverters.toNullableString())

    nfolds = Param(
        Params._dummy(),
        "nfolds",
        """Number of folds for K-fold cross-validation (0 to disable or >= 2).""",
        H2OTypeConverters.toInt())

    keepCrossValidationModels = Param(
        Params._dummy(),
        "keepCrossValidationModels",
        """Whether to keep the cross-validation models.""",
        H2OTypeConverters.toBoolean())

    keepCrossValidationPredictions = Param(
        Params._dummy(),
        "keepCrossValidationPredictions",
        """Whether to keep the predictions of the cross-validation models.""",
        H2OTypeConverters.toBoolean())

    keepCrossValidationFoldAssignment = Param(
        Params._dummy(),
        "keepCrossValidationFoldAssignment",
        """Whether to keep the cross-validation fold assignment.""",
        H2OTypeConverters.toBoolean())

    parallelizeCrossValidation = Param(
        Params._dummy(),
        "parallelizeCrossValidation",
        """Allow parallel training of cross-validation models""",
        H2OTypeConverters.toBoolean())

    distribution = Param(
        Params._dummy(),
        "distribution",
        """Distribution function""",
        H2OTypeConverters.toEnumString("hex.genmodel.utils.DistributionFamily"))

    tweediePower = Param(
        Params._dummy(),
        "tweediePower",
        """Tweedie power for Tweedie regression, must be between 1 and 2.""",
        H2OTypeConverters.toFloat())

    quantileAlpha = Param(
        Params._dummy(),
        "quantileAlpha",
        """Desired quantile for Quantile regression, must be between 0 and 1.""",
        H2OTypeConverters.toFloat())

    huberAlpha = Param(
        Params._dummy(),
        "huberAlpha",
        """Desired quantile for Huber/M-regression (threshold between quadratic and linear loss, must be between 0 and 1).""",
        H2OTypeConverters.toFloat())

    labelCol = Param(
        Params._dummy(),
        "labelCol",
        """Response variable column.""",
        H2OTypeConverters.toNullableString())

    weightCol = Param(
        Params._dummy(),
        "weightCol",
        """Column with observation weights. Giving some observation a weight of zero is equivalent to excluding it from the dataset; giving an observation a relative weight of 2 is equivalent to repeating that row twice. Negative weights are not allowed. Note: Weights are per-row observation weights and do not increase the size of the data frame. This is typically the number of times a row is repeated, but non-integer values are supported as well. During training, rows with higher weights matter more, due to the larger loss function pre-factor. If you set weight = 0 for a row, the returned prediction frame at that row is zero and this is incorrect. To get an accurate prediction, remove all rows with weight == 0.""",
        H2OTypeConverters.toNullableString())

    offsetCol = Param(
        Params._dummy(),
        "offsetCol",
        """Offset column. This will be added to the combination of columns before applying the link function.""",
        H2OTypeConverters.toNullableString())

    foldCol = Param(
        Params._dummy(),
        "foldCol",
        """Column with cross-validation fold index assignment per observation.""",
        H2OTypeConverters.toNullableString())

    foldAssignment = Param(
        Params._dummy(),
        "foldAssignment",
        """Cross-validation fold assignment scheme, if fold_column is not specified. The 'Stratified' option will stratify the folds based on the response variable, for classification problems.""",
        H2OTypeConverters.toEnumString("hex.Model$Parameters$FoldAssignmentScheme"))

    categoricalEncoding = Param(
        Params._dummy(),
        "categoricalEncoding",
        """Encoding scheme for categorical features""",
        H2OTypeConverters.toEnumString("hex.Model$Parameters$CategoricalEncodingScheme"))

    maxCategoricalLevels = Param(
        Params._dummy(),
        "maxCategoricalLevels",
        """For every categorical feature, only use this many most frequent categorical levels for model training. Only used for categorical_encoding == EnumLimited.""",
        H2OTypeConverters.toInt())

    ignoredCols = Param(
        Params._dummy(),
        "ignoredCols",
        """Names of columns to ignore for training.""",
        H2OTypeConverters.toNullableListString())

    ignoreConstCols = Param(
        Params._dummy(),
        "ignoreConstCols",
        """Ignore constant columns.""",
        H2OTypeConverters.toBoolean())

    scoreEachIteration = Param(
        Params._dummy(),
        "scoreEachIteration",
        """Whether to score during each iteration of model training.""",
        H2OTypeConverters.toBoolean())

    checkpoint = Param(
        Params._dummy(),
        "checkpoint",
        """Model checkpoint to resume training with.""",
        H2OTypeConverters.toNullableString())

    stoppingRounds = Param(
        Params._dummy(),
        "stoppingRounds",
        """Early stopping based on convergence of stopping_metric. Stop if simple moving average of length k of the stopping_metric does not improve for k:=stopping_rounds scoring events (0 to disable)""",
        H2OTypeConverters.toInt())

    maxRuntimeSecs = Param(
        Params._dummy(),
        "maxRuntimeSecs",
        """Maximum allowed runtime in seconds for model training. Use 0 to disable.""",
        H2OTypeConverters.toFloat())

    stoppingMetric = Param(
        Params._dummy(),
        "stoppingMetric",
        """Metric to use for early stopping (AUTO: logloss for classification, deviance for regression and anonomaly_score for Isolation Forest). Note that custom and custom_increasing can only be used in GBM and DRF with the Python client.""",
        H2OTypeConverters.toEnumString("hex.ScoreKeeper$StoppingMetric"))

    stoppingTolerance = Param(
        Params._dummy(),
        "stoppingTolerance",
        """Relative tolerance for metric-based stopping criterion (stop if relative improvement is not at least this much)""",
        H2OTypeConverters.toFloat())

    gainsliftBins = Param(
        Params._dummy(),
        "gainsliftBins",
        """Gains/Lift table number of bins. 0 means disabled.. Default value -1 means automatic binning.""",
        H2OTypeConverters.toInt())

    customMetricFunc = Param(
        Params._dummy(),
        "customMetricFunc",
        """Reference to custom evaluation function, format: `language:keyName=funcName`""",
        H2OTypeConverters.toNullableString())

    customDistributionFunc = Param(
        Params._dummy(),
        "customDistributionFunc",
        """Reference to custom distribution, format: `language:keyName=funcName`""",
        H2OTypeConverters.toNullableString())

    exportCheckpointsDir = Param(
        Params._dummy(),
        "exportCheckpointsDir",
        """Automatically export generated models to this directory.""",
        H2OTypeConverters.toNullableString())

    aucType = Param(
        Params._dummy(),
        "aucType",
        """Set default multinomial AUC type.""",
        H2OTypeConverters.toEnumString("hex.MultinomialAucType"))

    ##
    # Getters
    ##
    def getMetalearnerAlgorithm(self):
        return self.getOrDefault(self.metalearnerAlgorithm)

    def getMetalearnerNfolds(self):
        return self.getOrDefault(self.metalearnerNfolds)

    def getMetalearnerFoldAssignment(self):
        return self.getOrDefault(self.metalearnerFoldAssignment)

    def getMetalearnerFoldCol(self):
        return self.getOrDefault(self.metalearnerFoldCol)

    def getMetalearnerTransform(self):
        return self.getOrDefault(self.metalearnerTransform)

    def getKeepLeveloneFrame(self):
        return self.getOrDefault(self.keepLeveloneFrame)

    def getMetalearnerParams(self):
        return self.getOrDefault(self.metalearnerParams)

    def getSeed(self):
        return self.getOrDefault(self.seed)

    def getScoreTrainingSamples(self):
        return self.getOrDefault(self.scoreTrainingSamples)

    def getModelId(self):
        return self.getOrDefault(self.modelId)

    def getNfolds(self):
        return self.getOrDefault(self.nfolds)

    def getKeepCrossValidationModels(self):
        return self.getOrDefault(self.keepCrossValidationModels)

    def getKeepCrossValidationPredictions(self):
        return self.getOrDefault(self.keepCrossValidationPredictions)

    def getKeepCrossValidationFoldAssignment(self):
        return self.getOrDefault(self.keepCrossValidationFoldAssignment)

    def getParallelizeCrossValidation(self):
        return self.getOrDefault(self.parallelizeCrossValidation)

    def getDistribution(self):
        return self.getOrDefault(self.distribution)

    def getTweediePower(self):
        return self.getOrDefault(self.tweediePower)

    def getQuantileAlpha(self):
        return self.getOrDefault(self.quantileAlpha)

    def getHuberAlpha(self):
        return self.getOrDefault(self.huberAlpha)

    def getLabelCol(self):
        return self.getOrDefault(self.labelCol)

    def getWeightCol(self):
        return self.getOrDefault(self.weightCol)

    def getOffsetCol(self):
        return self.getOrDefault(self.offsetCol)

    def getFoldCol(self):
        return self.getOrDefault(self.foldCol)

    def getFoldAssignment(self):
        return self.getOrDefault(self.foldAssignment)

    def getCategoricalEncoding(self):
        return self.getOrDefault(self.categoricalEncoding)

    def getMaxCategoricalLevels(self):
        return self.getOrDefault(self.maxCategoricalLevels)

    def getIgnoredCols(self):
        return self.getOrDefault(self.ignoredCols)

    def getIgnoreConstCols(self):
        return self.getOrDefault(self.ignoreConstCols)

    def getScoreEachIteration(self):
        return self.getOrDefault(self.scoreEachIteration)

    def getCheckpoint(self):
        return self.getOrDefault(self.checkpoint)

    def getStoppingRounds(self):
        return self.getOrDefault(self.stoppingRounds)

    def getMaxRuntimeSecs(self):
        return self.getOrDefault(self.maxRuntimeSecs)

    def getStoppingMetric(self):
        return self.getOrDefault(self.stoppingMetric)

    def getStoppingTolerance(self):
        return self.getOrDefault(self.stoppingTolerance)

    def getGainsliftBins(self):
        return self.getOrDefault(self.gainsliftBins)

    def getCustomMetricFunc(self):
        return self.getOrDefault(self.customMetricFunc)

    def getCustomDistributionFunc(self):
        return self.getOrDefault(self.customDistributionFunc)

    def getExportCheckpointsDir(self):
        return self.getOrDefault(self.exportCheckpointsDir)

    def getAucType(self):
        return self.getOrDefault(self.aucType)

    ##
    # Setters
    ##
    def setMetalearnerAlgorithm(self, value):
        return self._set(metalearnerAlgorithm=value)

    def setMetalearnerNfolds(self, value):
        return self._set(metalearnerNfolds=value)

    def setMetalearnerFoldAssignment(self, value):
        return self._set(metalearnerFoldAssignment=value)

    def setMetalearnerFoldCol(self, value):
        return self._set(metalearnerFoldCol=value)

    def setMetalearnerTransform(self, value):
        return self._set(metalearnerTransform=value)

    def setKeepLeveloneFrame(self, value):
        return self._set(keepLeveloneFrame=value)

    def setMetalearnerParams(self, value):
        return self._set(metalearnerParams=value)

    def setSeed(self, value):
        return self._set(seed=value)

    def setScoreTrainingSamples(self, value):
        return self._set(scoreTrainingSamples=value)

    def setModelId(self, value):
        return self._set(modelId=value)

    def setNfolds(self, value):
        return self._set(nfolds=value)

    def setKeepCrossValidationModels(self, value):
        return self._set(keepCrossValidationModels=value)

    def setKeepCrossValidationPredictions(self, value):
        return self._set(keepCrossValidationPredictions=value)

    def setKeepCrossValidationFoldAssignment(self, value):
        return self._set(keepCrossValidationFoldAssignment=value)

    def setParallelizeCrossValidation(self, value):
        return self._set(parallelizeCrossValidation=value)

    def setDistribution(self, value):
        return self._set(distribution=value)

    def setTweediePower(self, value):
        return self._set(tweediePower=value)

    def setQuantileAlpha(self, value):
        return self._set(quantileAlpha=value)

    def setHuberAlpha(self, value):
        return self._set(huberAlpha=value)

    def setLabelCol(self, value):
        return self._set(labelCol=value)

    def setWeightCol(self, value):
        return self._set(weightCol=value)

    def setOffsetCol(self, value):
        return self._set(offsetCol=value)

    def setFoldCol(self, value):
        return self._set(foldCol=value)

    def setFoldAssignment(self, value):
        return self._set(foldAssignment=value)

    def setCategoricalEncoding(self, value):
        return self._set(categoricalEncoding=value)

    def setMaxCategoricalLevels(self, value):
        return self._set(maxCategoricalLevels=value)

    def setIgnoredCols(self, value):
        return self._set(ignoredCols=value)

    def setIgnoreConstCols(self, value):
        return self._set(ignoreConstCols=value)

    def setScoreEachIteration(self, value):
        return self._set(scoreEachIteration=value)

    def setCheckpoint(self, value):
        return self._set(checkpoint=value)

    def setStoppingRounds(self, value):
        return self._set(stoppingRounds=value)

    def setMaxRuntimeSecs(self, value):
        return self._set(maxRuntimeSecs=value)

    def setStoppingMetric(self, value):
        return self._set(stoppingMetric=value)

    def setStoppingTolerance(self, value):
        return self._set(stoppingTolerance=value)

    def setGainsliftBins(self, value):
        return self._set(gainsliftBins=value)

    def setCustomMetricFunc(self, value):
        return self._set(customMetricFunc=value)

    def setCustomDistributionFunc(self, value):
        return self._set(customDistributionFunc=value)

    def setExportCheckpointsDir(self, value):
        return self._set(exportCheckpointsDir=value)

    def setAucType(self, value):
        return self._set(aucType=value)

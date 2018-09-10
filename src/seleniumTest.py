from bs4 import BeautifulSoup
from selenium import webdriver
import json
from nupic.data.inference_shifter import InferenceShifter
from nupic.frameworks.opf.model_factory import ModelFactory
from datetime import datetime

browser = webdriver.PhantomJS()
MODEL_PARAMS={'aggregationInfo': {'days': 0,
                     'fields': [(u'timestamp', 'first'),
                                (u'currency', 'sum')],
                     'hours': 0,
                     'microseconds': 0,
                     'milliseconds': 0,
                     'minutes': 5,
                     'months': 0,
                     'seconds': 0,
                     'weeks': 0,
                     'years': 0},
 'model': 'HTMPrediction',
 'modelParams': {'anomalyParams': {u'anomalyCacheRecords': None,
                                   u'autoDetectThreshold': None,
                                   u'autoDetectWaitRecords': None},
                 'clParams': {'alpha': 0.050050000000000004,
                              'verbosity': 0,
                              'regionName': 'SDRClassifierRegion',
                              'steps': '1'},
                 'inferenceType': 'TemporalAnomaly',
                 'sensorParams': {'encoders': {u'raw_value': None,
                                               u'timestamp_dayOfWeek': None,
                                               u'timestamp_timeOfDay': None,
                                               u'timestamp_weekend': None,
                                               u'currency': {'clipInput': True,
                                                                  'fieldname': 'currency',
                                                                  'n': 272,
                                                                  'name': 'currency',
                                                                  'type': 'AdaptiveScalarEncoder',
                                                                  'w': 21
                                                                  }},
                                  'sensorAutoReset': None,
                                  'verbosity': 0
                                  },
                 'spEnable': True,
                 'spParams': {'columnCount': 2048,
                              'globalInhibition': 1,
                              'inputWidth': 0,
                              'numActiveColumnsPerInhArea': 40,
                              'potentialPct': 0.8,
                              'seed': 1956,
                              'spVerbosity': 0,
                              'spatialImp': 'cpp',
                              'synPermActiveInc': 0.05,
                              'synPermConnected': 0.1,
                              'synPermInactiveDec': 0.05015},
                 'tmEnable': True,
                 'tmParams': {'activationThreshold': 14,
                              'cellsPerColumn': 32,
                              'columnCount': 2048,
                              'globalDecay': 0.0,
                              'initialPerm': 0.21,
                              'inputWidth': 2048,
                              'maxAge': 0,
                              'maxSegmentsPerCell': 128,
                              'maxSynapsesPerSegment': 32,
                              'minThreshold': 11,
                              'newSynapseCount': 20,
                              'outputType': 'normal',
                              'pamLength': 3,
                              'permanenceDec': 0.1,
                              'permanenceInc': 0.1,
                              'seed': 1960,
                              'temporalImp': 'cpp',
                              'verbosity': 0},
                 'trainSPNetOnlyIfRequested': False},
 'predictAheadTime': None,
'version': 1}


def getCurrency():

    while 1:
        browser.get('https://www.investing.com/currencies/usd-try')
        soup = BeautifulSoup(browser.page_source, "html.parser")
        result = soup.find_all("span", {"id": "chart-info-last"})

        yield result


def timestamp():
    for resultSet in getCurrency():
        raw_data = resultSet
        for item in raw_data:
            #preProcessed = str(datetime.now())+","+item.text
            preProcessed = item.text
            yield preProcessed

         

if __name__ =="__main__":

    model = ModelFactory.create(MODEL_PARAMS)
    model.enableInference({"predictedField" : "currency"})
    
    for i in timestamp():
        preProcessed = i.strip()

        currency = float(preProcessed)


        result = model.run({
            "timestamp":datetime.now(),
            "currency":currency
        })


        print "time : {}".format(str(datetime.now()))
        print "Actual Currency : {}".format(currency)
        print "Predicted Currency : {}".format(result.inferences["multiStepBestPredictions"][1])
        print "Anomaly Score {}".format(result.inferences["anomalyScore"])
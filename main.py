import json, unittest, datetime

with open("./data-1.json","r") as f:
    jsonData1 = json.load(f)
with open("./data-2.json","r") as f:
    jsonData2 = json.load(f)
with open("./data-result.json","r") as f:
    jsonExpectedResult = json.load(f)


def convertFromFormat1 (jsonObject):

    result = {}
    result['deviceID'] = jsonObject['deviceID']
    result['deviceType'] = jsonObject['deviceType']
    result['timestamp'] = jsonObject['timestamp']
    result['data'] = {}
    result['data']['status'] = jsonObject['operationStatus']
    result['data']['temperature'] = jsonObject['temp']
    location = jsonObject['location']
    location_fields = location.split('/')
    result['location'] = {
        'country': location_fields[0],
        'city': location_fields[1],
        'area': location_fields[2],
        'factory': location_fields[3],
        'section': location_fields[4],
    }
    print('\nConverted data-1.json file : \n\n', result)
    return result


def convertFromFormat2 (jsonObject):

    result = {}
    device = jsonObject['device']
    result['deviceID'] = device['id']
    result['deviceType'] = device['type']
    iso_timestamp = jsonObject['timestamp']
    timestamp = int(datetime.datetime.fromisoformat(iso_timestamp[:-1]).timestamp() * 1000)
    result['timestamp'] = timestamp
    result['data'] = {}
    result['data']['status'] = jsonObject['data']['status']
    result['data']['temperature'] = jsonObject['data']['temperature']
    location = jsonObject['country'] + '/' + jsonObject['city'] + '/' + jsonObject['area'] + '/' + jsonObject['factory'] + '/' + jsonObject['section']
    location_fields = location.split('/')
    result['location'] = {
        'country': location_fields[0],
        'city': location_fields[1],
        'area': location_fields[2],
        'factory': location_fields[3],
        'section': location_fields[4],
    }
    print('\nConverted data-2.json file : \n\n', result)
    return result


def main (jsonObject):

    result = {}
    # Initially jsonObject = data-1.json which is missing device, hence it will go in if block
    if (jsonObject.get('device') == None):
        result = convertFromFormat1(jsonObject)
    else:
        result = convertFromFormat2(jsonObject)

    return result


class TestSolution(unittest.TestCase):

    def test_sanity(self):

        result = json.loads(json.dumps(jsonExpectedResult))
        self.assertEqual(
            result,
            jsonExpectedResult
        )

    def test_dataType1(self):

        result = main (jsonData1)
        self.assertEqual(
            result,
            jsonExpectedResult,
            'Converting from Type 1 failed'
        )

    def test_dataType2(self):

        result = main (jsonData2)
        self.assertEqual(
            result,
            jsonExpectedResult,
            'Converting from Type 2 failed'
        )

if __name__ == '__main__':
    unittest.main()

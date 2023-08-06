from rasa.utils.redactor import Redactor
from rasa.utils.redactor import get_count_digits
from rasa.utils.redactor import spanish2english

redactor = Redactor()
# It would not be wise to try and change these messages unless you have to.
msg_with_pci = """Received user message:
{
   "intent":{
      "name":"features_data_add",
      "confidence":0.10683724284172058
   },
   "entities":[
      {
         "start":0,
         "end":16,
         "text":"4761739001010010",
         "value":"4761739001010010",
         "confidence":1.0,
         "additional_info":{
            "value":4761739001010010,
            "type":"value"
         },
         "entity":"number",
         "extractor":"DucklingHTTPExtractor"
      }
   ],
   "intent_ranking":[
      {
         "name":"features_data_add",
         "confidence":0.10683724284172058
      },
      {
         "name":"this_phone",
         "confidence":0.07678905129432678
      },
      {
         "name":"affirm",
         "confidence":0.07138489931821823
      },
      {
         "name":"deny",
         "confidence":0.06736931204795837
      },
      {
         "name":"tech_support",
         "confidence":0.05541007220745087
      },
      {
         "name":"greet",
         "confidence":0.0402037613093853
      },
      {
         "name":"features_data_inquire",
         "confidence":0.02958683669567108
      },
      {
         "name":"features_data",
         "confidence":0.0289413183927536
      },
      {
         "name":"another_phone",
         "confidence":0.02866683341562748
      },
      {
         "name":"phone_number_change",
         "confidence":0.027637505903840065
      }
   ],
   "text":"4761739001010010",
   "asrConfidence":1,
   "recordingId":"None",
   "missed_intent":false,
   "message_id":"7f3ab5c8e9aa407dbba8553a3ac83671",
   "metadata":{
      "message_type":"DTMF",
      "dnis":"9282252208",
      "privacy_mode":true,
      "channel_id":1,
      "original_text":"4761739001010010",
      "type":"text",
      "active_form":"action_credit_card_collector",
      "requested_slot":"cc_number",
      "template_name":"utter_ask_cc_number",
      "asr_threshold":0.4,
      "nlu_threshold":0.63,
      "group":"cc_number"
   }
}
"""
msg_without_pci = """Received user message:
{
   "intent":{
      "name":"features_data_add",
      "confidence":0.****************
   },
   "entities":[
      {
         "start":0,
         "end":16,
         "text":"****************",
         "value":"****************",
         "confidence":1.0,
         "additional_info":{
            "value":****************,
            "type":"value"
         },
         "entity":"number",
         "extractor":"DucklingHTTPExtractor"
      }
   ],
   "intent_ranking":[
      {
         "name":"features_data_add",
         "confidence":0.****************
      },
      {
         "name":"this_phone",
         "confidence":0.****************
      },
      {
         "name":"affirm",
         "confidence":0.****************
      },
      {
         "name":"deny",
         "confidence":0.****************
      },
      {
         "name":"tech_support",
         "confidence":0.****************
      },
      {
         "name":"greet",
         "confidence":0.****************
      },
      {
         "name":"features_data_inquire",
         "confidence":0.****************
      },
      {
         "name":"features_data",
         "confidence":0.****************
      },
      {
         "name":"another_phone",
         "confidence":0.****************
      },
      {
         "name":"phone_number_change",
         "confidence":0.****************
      }
   ],
   "text":"****************",
   "asrConfidence":1,
   "recordingId":"None",
   "missed_intent":false,
   "message_id":"7f3ab5c8e9aa407dbba8553a3ac83671",
   "metadata":{
      "message_type":"DTMF",
      "dnis":"9282252208",
      "privacy_mode":true,
      "channel_id":1,
      "original_text":"****************",
      "type":"text",
      "active_form":"action_credit_card_collector",
      "requested_slot":"cc_number",
      "template_name":"utter_ask_cc_number",
      "asr_threshold":0.4,
      "nlu_threshold":0.63,
      "group":"cc_number"
   }
}
"""
msg_without_pci_strict = """Received user message:
{
   "intent":{
      "name":"features_data_add",
      "confidence":0.****************
   },
   "entities":[
      {
         "start":0,
         "end":16,
         "text":"****************",
         "value":"****************",
         "confidence":1.0,
         "additional_info":{
            "value":****************,
            "type":"value"
         },
         "entity":"number",
         "extractor":"DucklingHTTPExtractor"
      }
   ],
   "intent_ranking":[
      {
         "name":"features_data_add",
         "confidence":0.****************
      },
      {
         "name":"this_phone",
         "confidence":0.****************
      },
      {
         "name":"affirm",
         "confidence":0.****************
      },
      {
         "name":"deny",
         "confidence":0.****************
      },
      {
         "name":"tech_support",
         "confidence":0.****************
      },
      {
         "name":"greet",
         "confidence":0.****************
      },
      {
         "name":"features_data_inquire",
         "confidence":0.****************
      },
      {
         "name":"features_data",
         "confidence":0.****************
      },
      {
         "name":"another_phone",
         "confidence":0.****************
      },
      {
         "name":"phone_number_change",
         "confidence":0.****************
      }
   ],
   "text":"****************",
   "asrConfidence":1,
   "recordingId":"None",
   "missed_intent":false,
   "message_id":"7f3ab5c8e9aa****************dbba****************a3ac83671",
   "metadata":{
      "message_type":"DTMF",
      "dnis":"9282252208",
      "privacy_mode":true,
      "channel_id":1,
      "original_text":"****************",
      "type":"text",
      "active_form":"action_credit_card_collector",
      "requested_slot":"cc_number",
      "template_name":"utter_ask_cc_number",
      "asr_threshold":0.4,
      "nlu_threshold":0.63,
      "group":"cc_number"
   }
}
"""

dict_with_pci = {
    "intent": {
        "name": "features_data_add",
        "confidence": 0.10683724284172058
    },
    "entities": [
        {
            "start": 0,
            "end": 16,
            "text": "4761739001010010",
            "value": "4761739001010010",
            "confidence": 1.0,
            "additional_info": {
                "value": 4761739001010010,
                "type": "value"
            },
            "entity": "number",
            "extractor": "DucklingHTTPExtractor"
        }
    ],
    "intent_ranking": [
        {
            "name": "features_data_add",
            "confidence": 0.10683724284172058
        },
        {
            "name": "this_phone",
            "confidence": 0.07678905129432678
        },
        {
            "name": "affirm",
            "confidence": 0.07138489931821823
        },
        {
            "name": "deny",
            "confidence": 0.06736931204795837
        },
        {
            "name": "tech_support",
            "confidence": 0.05541007220745087
        },
        {
            "name": "greet",
            "confidence": 0.0402037613093853
        },
        {
            "name": "features_data_inquire",
            "confidence": 0.02958683669567108
        },
        {
            "name": "features_data",
            "confidence": 0.0289413183927536
        },
        {
            "name": "another_phone",
            "confidence": 0.02866683341562748
        },
        {
            "name": "phone_number_change",
            "confidence": 0.027637505903840065
        }
    ],
    "text": "4761739001010010",
    "asrConfidence": 1,
    "recordingId": "None",
    "missed_intent": False,
    "message_id": "7f3ab5c8e9aa407dbba8553a3ac83671",
    "metadata": {
        "message_type": "DTMF",
        "dnis": "9282252208",
        "privacy_mode": True,
        "channel_id": 1,
        "original_text": "4761739001010010",
        "type": "text",
        "active_form": "action_credit_card_collector",
        "requested_slot": "cc_number",
        "template_name": "utter_ask_cc_number",
        "asr_threshold": 0.4,
        "nlu_threshold": 0.63,
        "group": "cc_number"
    },
    "useless_field": None
}
dict_without_pci = {
    "intent": {
        "name": "features_data_add",
        "confidence": 0.10683724284172058
    },
    "entities": [
        {
            "start": 0,
            "end": 16,
            "text": "****************",
            "value": "****************",
            "confidence": 1.0,
            "additional_info": {
                "value": "****************",
                "type": "value"
            },
            "entity": "number",
            "extractor": "DucklingHTTPExtractor"
        }
    ],
    "intent_ranking": [
        {
            "name": "features_data_add",
            "confidence": 0.10683724284172058
        },
        {
            "name": "this_phone",
            "confidence": 0.07678905129432678
        },
        {
            "name": "affirm",
            "confidence": 0.07138489931821823
        },
        {
            "name": "deny",
            "confidence": 0.06736931204795837
        },
        {
            "name": "tech_support",
            "confidence": 0.05541007220745087
        },
        {
            "name": "greet",
            "confidence": 0.0402037613093853
        },
        {
            "name": "features_data_inquire",
            "confidence": 0.02958683669567108
        },
        {
            "name": "features_data",
            "confidence": 0.0289413183927536
        },
        {
            "name": "another_phone",
            "confidence": 0.02866683341562748
        },
        {
            "name": "phone_number_change",
            "confidence": 0.027637505903840065
        }
    ],
    "text": "****************",
    "asrConfidence": 1,
    "recordingId": "None",
    "missed_intent": False,
    "message_id": "7f3ab5c8e9aa407dbba8553a3ac83671",
    "metadata": {
        "message_type": "DTMF",
        "dnis": "9282252208",
        "privacy_mode": True,
        "channel_id": 1,
        "original_text": "****************",
        "type": "text",
        "active_form": "action_credit_card_collector",
        "requested_slot": "cc_number",
        "template_name": "utter_ask_cc_number",
        "asr_threshold": 0.4,
        "nlu_threshold": 0.63,
        "group": "cc_number"
    },
    "useless_field": None
}

list_with_pci = ["4761739001010010", 4761739001010010,
                 {"value": 4761739001010010, "additional_info": {"value": "4761739001010010"}}]
list_without_pci = ["****************", "****************",
                    {"value": "****************", "additional_info": {"value": "****************"}}]
entity_list_one_entry_with_pci = [
    {
        "start": 0,
        "end": 16,
        "text": "4761739001010010",
        "value": "4761739001010010",
        "confidence": 1.0,
        "additional_info": {
            "value": 4761739001010010,
            "type": "value"
        },
        "entity": "number",
        "extractor": "DucklingHTTPExtractor"
    }
]
entity_list_one_entry_without_pci = [
    {
        "start": 0,
        "end": 16,
        "text": "****************",
        "value": "****************",
        "confidence": 1.0,
        "additional_info": {
            "value": "****************",
            "type": "value"
        },
        "entity": "number",
        "extractor": "DucklingHTTPExtractor"
    }
]

entity_list_many_entries_with_pci = [
    {'start': 0, 'end': 1, 'text': '1', 'value': 1, 'confidence': 1.0, 'additional_info': {'value': 1, 'type': 'value'},
     'entity': 'number', 'extractor': 'DucklingHTTPExtractor'},
    {'start': 1, 'end': 2, 'text': '1', 'value': 1, 'confidence': 1.0, 'additional_info': {'value': 1, 'type': 'value'},
     'entity': 'number', 'extractor': 'DucklingHTTPExtractor'},
    {'start': 2, 'end': 3, 'text': '1', 'value': 1, 'confidence': 1.0, 'additional_info': {'value': 1, 'type': 'value'},
     'entity': 'number', 'extractor': 'DucklingHTTPExtractor'},
    {'start': 3, 'end': 4, 'text': '1', 'value': 1, 'confidence': 1.0, 'additional_info': {'value': 1, 'type': 'value'},
     'entity': 'number', 'extractor': 'DucklingHTTPExtractor'},
    {'start': 0, 'end': 1, 'text': '1', 'value': 1, 'confidence': 1.0, 'additional_info': {'value': 1, 'type': 'value'},
     'entity': 'number', 'extractor': 'DucklingHTTPExtractor'},
    {'start': 1, 'end': 2, 'text': '1', 'value': 1, 'confidence': 1.0, 'additional_info': {'value': 1, 'type': 'value'},
     'entity': 'number', 'extractor': 'DucklingHTTPExtractor'},
    {'start': 2, 'end': 3, 'text': '1', 'value': 1, 'confidence': 1.0, 'additional_info': {'value': 1, 'type': 'value'},
     'entity': 'number', 'extractor': 'DucklingHTTPExtractor'},
    {'start': 3, 'end': 4, 'text': '1', 'value': 1, 'confidence': 1.0, 'additional_info': {'value': 1, 'type': 'value'},
     'entity': 'number', 'extractor': 'DucklingHTTPExtractor'},
    {'start': 4, 'end': 5, 'text': '1', 'value': 1, 'confidence': 1.0, 'additional_info': {'value': 1, 'type': 'value'},
     'entity': 'number', 'extractor': 'DucklingHTTPExtractor'},
    {'start': 5, 'end': 6, 'text': '1', 'value': 1, 'confidence': 1.0, 'additional_info': {'value': 1, 'type': 'value'},
     'entity': 'number', 'extractor': 'DucklingHTTPExtractor'},
    {'start': 6, 'end': 7, 'text': '1', 'value': 1, 'confidence': 1.0, 'additional_info': {'value': 1, 'type': 'value'},
     'entity': 'number', 'extractor': 'DucklingHTTPExtractor'},
    {'start': 7, 'end': 8, 'text': '1', 'value': 1, 'confidence': 1.0, 'additional_info': {'value': 1, 'type': 'value'},
     'entity': 'number', 'extractor': 'DucklingHTTPExtractor'},
    {'start': 8, 'end': 9, 'text': '1', 'value': 1, 'confidence': 1.0, 'additional_info': {'value': 1, 'type': 'value'},
     'entity': 'number', 'extractor': 'DucklingHTTPExtractor'},
    {'start': 9, 'end': 10, 'text': '1', 'value': 1, 'confidence': 1.0,
     'additional_info': {'value': 1, 'type': 'value'},
     'entity': 'number', 'extractor': 'DucklingHTTPExtractor'},
    {'start': 10, 'end': 11, 'text': '1', 'value': 1, 'confidence': 1.0,
     'additional_info': {'value': 1, 'type': 'value'},
     'entity': 'number', 'extractor': 'DucklingHTTPExtractor'},
    {'start': 11, 'end': 12, 'text': '1', 'value': 1, 'confidence': 1.0,
     'additional_info': {'value': 1, 'type': 'value'},
     'entity': 'number', 'extractor': 'DucklingHTTPExtractor'},
]
entity_list_many_entries_without_pci = [
    {'additional_info': {'type': 'value', 'value': '*'},
     'confidence': 1.0,
     'end': 1,
     'entity': 'number',
     'extractor': 'DucklingHTTPExtractor',
     'start': 0,
     'text': '*',
     'value': '*'},
    {'additional_info': {'type': 'value', 'value': '*'},
     'confidence': 1.0,
     'end': 2,
     'entity': 'number',
     'extractor': 'DucklingHTTPExtractor',
     'start': 1,
     'text': '*',
     'value': '*'},
    {'additional_info': {'type': 'value', 'value': '*'},
     'confidence': 1.0,
     'end': 3,
     'entity': 'number',
     'extractor': 'DucklingHTTPExtractor',
     'start': 2,
     'text': '*',
     'value': '*'},
    {'additional_info': {'type': 'value', 'value': '*'},
     'confidence': 1.0,
     'end': 4,
     'entity': 'number',
     'extractor': 'DucklingHTTPExtractor',
     'start': 3,
     'text': '*',
     'value': '*'},
    {'additional_info': {'type': 'value', 'value': '*'},
     'confidence': 1.0,
     'end': 1,
     'entity': 'number',
     'extractor': 'DucklingHTTPExtractor',
     'start': 0,
     'text': '*',
     'value': '*'},
    {'additional_info': {'type': 'value', 'value': '*'},
     'confidence': 1.0,
     'end': 2,
     'entity': 'number',
     'extractor': 'DucklingHTTPExtractor',
     'start': 1,
     'text': '*',
     'value': '*'},
    {'additional_info': {'type': 'value', 'value': '*'},
     'confidence': 1.0,
     'end': 3,
     'entity': 'number',
     'extractor': 'DucklingHTTPExtractor',
     'start': 2,
     'text': '*',
     'value': '*'},
    {'additional_info': {'type': 'value', 'value': '*'},
     'confidence': 1.0,
     'end': 4,
     'entity': 'number',
     'extractor': 'DucklingHTTPExtractor',
     'start': 3,
     'text': '*',
     'value': '*'},
    {'additional_info': {'type': 'value', 'value': '*'},
     'confidence': 1.0,
     'end': 5,
     'entity': 'number',
     'extractor': 'DucklingHTTPExtractor',
     'start': 4,
     'text': '*',
     'value': '*'},
    {'additional_info': {'type': 'value', 'value': '*'},
     'confidence': 1.0,
     'end': 6,
     'entity': 'number',
     'extractor': 'DucklingHTTPExtractor',
     'start': 5,
     'text': '*',
     'value': '*'},
    {'additional_info': {'type': 'value', 'value': '*'},
     'confidence': 1.0,
     'end': 7,
     'entity': 'number',
     'extractor': 'DucklingHTTPExtractor',
     'start': 6,
     'text': '*',
     'value': '*'},
    {'additional_info': {'type': 'value', 'value': '*'},
     'confidence': 1.0,
     'end': 8,
     'entity': 'number',
     'extractor': 'DucklingHTTPExtractor',
     'start': 7,
     'text': '*',
     'value': '*'},
    {'additional_info': {'type': 'value', 'value': '*'},
     'confidence': 1.0,
     'end': 9,
     'entity': 'number',
     'extractor': 'DucklingHTTPExtractor',
     'start': 8,
     'text': '*',
     'value': '*'},
    {'additional_info': {'type': 'value', 'value': '*'},
     'confidence': 1.0,
     'end': 10,
     'entity': 'number',
     'extractor': 'DucklingHTTPExtractor',
     'start': 9,
     'text': '*',
     'value': '*'},
    {'additional_info': {'type': 'value', 'value': '*'},
     'confidence': 1.0,
     'end': 11,
     'entity': 'number',
     'extractor': 'DucklingHTTPExtractor',
     'start': 10,
     'text': '*',
     'value': '*'},
    {'additional_info': {'type': 'value', 'value': '*'},
     'confidence': 1.0,
     'end': 12,
     'entity': 'number',
     'extractor': 'DucklingHTTPExtractor',
     'start': 11,
     'text': '*',
     'value': '*'}]

event_no_pci = {'event': 'user', 'timestamp': 1621281543.1603343,
                'metadata': {'dnis': '9282252467', 'message_type': 'SPOKEN',
                             'partials': ['Ok', 'Ok so', 'Ok so', "Ok so i've been", "Ok so i've been having",
                                          "Ok so i've been having an effect", "Ok so i've been having an issue",
                                          "Ok so i've been having an issue with",
                                          "Ok so i've been having an issue where",
                                          "Ok so i've been having an issue where some",
                                          "Ok so i've been having an issue where some static",
                                          "Ok so i've been having an issue where some static i want to",
                                          "Ok so i've been having an issue where some static i want to cross the line",
                                          "Ok so i've been having an issue where some static i want to cross the line on the phone",
                                          "Ok so i've been having an issue where some static i want to cross the line on the phone",
                                          "Ok so i've been having an issue where some static i want to cross the line on the phone and"],
                             'channel_id': 1, 'type': 'text', 'template_name': 'temp_help_message',
                             'asr_threshold': 0.2, 'nlu_threshold': 0.63},
                'text': "OK, so I've been having an issue with some static, I want to cross the line on my phone and it",
                'parse_data': {'intent': {'name': 'add_subscriber', 'confidence': 0.6653156280517578}, 'entities': [],
                               'intent_ranking': [{'name': 'add_subscriber', 'confidence': 0.6653156280517578},
                                                  {'name': 'plan_info', 'confidence': 0.06193934753537178},
                                                  {'name': 'phone_number_change', 'confidence': 0.053489990532398224},
                                                  {'name': 'autopay', 'confidence': 0.013421786949038506},
                                                  {'name': 'autopay_update', 'confidence': 0.013023709878325462},
                                                  {'name': 'pay_someone_else', 'confidence': 0.00991435069590807},
                                                  {'name': 'remove_subscriber', 'confidence': 0.009756733663380146},
                                                  {'name': 'reactivate', 'confidence': 0.009636330418288708},
                                                  {'name': 'change_plan', 'confidence': 0.009616482071578503},
                                                  {'name': 'another_phone', 'confidence': 0.009423586539924145}],
                               'text': "Ok so i've been having an issue where some static i want to cross the line on the phone",
                               'asrConfidence': 1, 'recordingId': None, 'missed_intent': None,
                               'message_id': '6524399f26124e8d87957f6c6ecb5a39',
                               'metadata': {'dnis': '9282252467', 'message_type': 'SPOKEN',
                                            'partials': ['Ok', 'Ok so', 'Ok so', "Ok so i've been",
                                                         "Ok so i've been having", "Ok so i've been having an effect",
                                                         "Ok so i've been having an issue",
                                                         "Ok so i've been having an issue with",
                                                         "Ok so i've been having an issue where",
                                                         "Ok so i've been having an issue where some",
                                                         "Ok so i've been having an issue where some static",
                                                         "Ok so i've been having an issue where some static i want to",
                                                         "Ok so i've been having an issue where some static i want to cross the line",
                                                         "Ok so i've been having an issue where some static i want to cross the line on the phone",
                                                         "Ok so i've been having an issue where some static i want to cross the line on the phone",
                                                         "Ok so i've been having an issue where some static i want to cross the line on the phone and"],
                                            'channel_id': 1, 'type': 'text', 'template_name': 'temp_help_message',
                                            'asr_threshold': 0.2, 'nlu_threshold': 0.63}},
                'input_channel': 'OMNI_VOICE_00001', 'message_id': '6524399f26124e8d87957f6c6ecb5a39',
                'entities_redacted': []}
event_with_pci = {'event': 'user', 'timestamp': 1621281543.1603343,
                  'metadata': {'dnis': '9282252467', 'message_type': 'SPOKEN',
                               'partials': ['1', '1 2', '1 2', "1 2 3"],
                               'channel_id': 1, 'type': 'text', 'template_name': 'temp_help_message',
                               'asr_threshold': 0.2, 'nlu_threshold': 0.63},
                  'text': "1 2 3",
                  'parse_data': {'intent': {'name': 'add_subscriber', 'confidence': 0.6653156280517578},
                                 'entities': [{'start': 0, 'end': 1, 'text': '1', 'value': 1, 'confidence': 1.0,
                                               'additional_info': {'value': 1, 'type': 'value'},
                                               'entity': 'number', 'extractor': 'DucklingHTTPExtractor'},
                                              {'start': 1, 'end': 2, 'text': '2', 'value': 2, 'confidence': 1.0,
                                               'additional_info': {'value': 2, 'type': 'value'},
                                               'entity': 'number', 'extractor': 'DucklingHTTPExtractor'},
                                              {'start': 2, 'end': 3, 'text': '3', 'value': 3, 'confidence': 1.0,
                                               'additional_info': {'value': 3, 'type': 'value'},
                                               'entity': 'number', 'extractor': 'DucklingHTTPExtractor'}],
                                 'intent_ranking': [{'name': 'add_subscriber', 'confidence': 0.6653156280517578},
                                                    {'name': 'plan_info', 'confidence': 0.06193934753537178},
                                                    {'name': 'phone_number_change',
                                                     'confidence': 0.053489990532398224},
                                                    {'name': 'autopay', 'confidence': 0.013421786949038506},
                                                    {'name': 'autopay_update', 'confidence': 0.013023709878325462},
                                                    {'name': 'pay_someone_else', 'confidence': 0.00991435069590807},
                                                    {'name': 'remove_subscriber', 'confidence': 0.009756733663380146},
                                                    {'name': 'reactivate', 'confidence': 0.009636330418288708},
                                                    {'name': 'change_plan', 'confidence': 0.009616482071578503},
                                                    {'name': 'another_phone', 'confidence': 0.009423586539924145}],
                                 'text': "1 2 3",
                                 'asrConfidence': 1, 'recordingId': None, 'missed_intent': None,
                                 'message_id': '6524399f26124e8d87957f6c6ecb5a39',
                                 'metadata': {'dnis': '9282252467', 'message_type': 'SPOKEN',
                                              'partials': ['1', '1 2', '1 2', "1 2 3"],
                                              'channel_id': 1, 'type': 'text', 'template_name': 'temp_help_message',
                                              'asr_threshold': 0.2, 'nlu_threshold': 0.63}},
                  'input_channel': 'OMNI_VOICE_00001', 'message_id': '6524399f26124e8d87957f6c6ecb5a39',
                  'entities_redacted': [{'start': 0, 'end': 1, 'text': '1', 'value': 1, 'confidence': 1.0,
                                         'additional_info': {'value': 1, 'type': 'value'},
                                         'entity': 'number', 'extractor': 'DucklingHTTPExtractor'},
                                        {'start': 1, 'end': 2, 'text': '2', 'value': 2, 'confidence': 1.0,
                                         'additional_info': {'value': 2, 'type': 'value'},
                                         'entity': 'number', 'extractor': 'DucklingHTTPExtractor'},
                                        {'start': 2, 'end': 3, 'text': '3', 'value': 3, 'confidence': 1.0,
                                         'additional_info': {'value': 3, 'type': 'value'},
                                         'entity': 'number', 'extractor': 'DucklingHTTPExtractor'}]}
event_with_redacted_pci = {'event': 'user', 'timestamp': 1621281543.1603343,
                           'metadata': {'dnis': '9282252467', 'message_type': 'SPOKEN',
                                        'partials': ['****', '**** ****', '**** ****', "**** **** ****"],
                                        'channel_id': 1, 'type': 'text', 'template_name': 'temp_help_message',
                                        'asr_threshold': 0.2, 'nlu_threshold': 0.63},
                           'text': "**** **** ****",
                           'parse_data': {'intent': {'name': 'add_subscriber', 'confidence': 0.6653156280517578},
                                          'entities': [
                                              {'start': 0, 'end': 1, 'text': '*', 'value': '*', 'confidence': 1.0,
                                               'additional_info': {'value': '*', 'type': 'value'},
                                               'entity': 'number', 'extractor': 'DucklingHTTPExtractor'},
                                              {'start': 1, 'end': 2, 'text': '*', 'value': '*', 'confidence': 1.0,
                                               'additional_info': {'value': '*', 'type': 'value'},
                                               'entity': 'number', 'extractor': 'DucklingHTTPExtractor'},
                                              {'start': 2, 'end': 3, 'text': '*', 'value': '*', 'confidence': 1.0,
                                               'additional_info': {'value': '*', 'type': 'value'},
                                               'entity': 'number', 'extractor': 'DucklingHTTPExtractor'}],
                                          'intent_ranking': [
                                              {'name': 'add_subscriber', 'confidence': 0.6653156280517578},
                                              {'name': 'plan_info', 'confidence': 0.06193934753537178},
                                              {'name': 'phone_number_change',
                                               'confidence': 0.053489990532398224},
                                              {'name': 'autopay', 'confidence': 0.013421786949038506},
                                              {'name': 'autopay_update', 'confidence': 0.013023709878325462},
                                              {'name': 'pay_someone_else', 'confidence': 0.00991435069590807},
                                              {'name': 'remove_subscriber', 'confidence': 0.009756733663380146},
                                              {'name': 'reactivate', 'confidence': 0.009636330418288708},
                                              {'name': 'change_plan', 'confidence': 0.009616482071578503},
                                              {'name': 'another_phone', 'confidence': 0.009423586539924145}],
                                          'text': "**** **** ****",
                                          'asrConfidence': 1, 'recordingId': None, 'missed_intent': None,
                                          'message_id': '6524399f26124e8d87957f6c6ecb5a39',
                                          'metadata': {'dnis': '9282252467', 'message_type': 'SPOKEN',
                                                       'partials': ['****', '**** ****', '**** ****', "**** **** ****"],
                                                       'channel_id': 1, 'type': 'text',
                                                       'template_name': 'temp_help_message',
                                                       'asr_threshold': 0.2, 'nlu_threshold': 0.63}},
                           'input_channel': 'OMNI_VOICE_00001', 'message_id': '6524399f26124e8d87957f6c6ecb5a39',
                           'entities_redacted': [{'start': 0, 'end': 1, 'text': '*', 'value': '*', 'confidence': 1.0,
                                                  'additional_info': {'value': '*', 'type': 'value'},
                                                  'entity': 'number', 'extractor': 'DucklingHTTPExtractor'},
                                                 {'start': 1, 'end': 2, 'text': '*', 'value': '*', 'confidence': 1.0,
                                                  'additional_info': {'value': '*', 'type': 'value'},
                                                  'entity': 'number', 'extractor': 'DucklingHTTPExtractor'},
                                                 {'start': 2, 'end': 3, 'text': '*', 'value': '*', 'confidence': 1.0,
                                                  'additional_info': {'value': '*', 'type': 'value'},
                                                  'entity': 'number', 'extractor': 'DucklingHTTPExtractor'}]}
event_with_cc_num = {'event': 'user', 'timestamp': 1621281543.1603343,
                     'metadata': {'dnis': '9282252467', 'message_type': 'SPOKEN',
                                  'partials': ['1', '1 2', '1 2', "1 2 3"],
                                  'channel_id': 1, 'type': 'text', 'template_name': 'temp_help_message',
                                  'asr_threshold': 0.2, 'nlu_threshold': 0.63},
                     'text': "1111111111111",
                     'parse_data': {'intent': {'name': 'add_subscriber', 'confidence': 0.6653156280517578},
                                    'entities': [{'start': 0, 'end': 1, 'text': '1', 'value': 1, 'confidence': 1.0,
                                                  'additional_info': {'value': 1, 'type': 'value'},
                                                  'entity': 'number', 'extractor': 'DucklingHTTPExtractor'},
                                                 {'start': 1, 'end': 2, 'text': '1', 'value': 1, 'confidence': 1.0,
                                                  'additional_info': {'value': 1, 'type': 'value'},
                                                  'entity': 'number', 'extractor': 'DucklingHTTPExtractor'},
                                                 {'start': 2, 'end': 3, 'text': '1', 'value': 1, 'confidence': 1.0,
                                                  'additional_info': {'value': 1, 'type': 'value'},
                                                  'entity': 'number', 'extractor': 'DucklingHTTPExtractor'},
                                                 {'start': 3, 'end': 4, 'text': '1', 'value': 1, 'confidence': 1.0,
                                                  'additional_info': {'value': 1, 'type': 'value'},
                                                  'entity': 'number', 'extractor': 'DucklingHTTPExtractor'},
                                                 {'start': 0, 'end': 1, 'text': '1', 'value': 1, 'confidence': 1.0,
                                                  'additional_info': {'value': 1, 'type': 'value'},
                                                  'entity': 'number', 'extractor': 'DucklingHTTPExtractor'},
                                                 {'start': 1, 'end': 2, 'text': '1', 'value': 1, 'confidence': 1.0,
                                                  'additional_info': {'value': 1, 'type': 'value'},
                                                  'entity': 'number', 'extractor': 'DucklingHTTPExtractor'},
                                                 {'start': 2, 'end': 3, 'text': '1', 'value': 1, 'confidence': 1.0,
                                                  'additional_info': {'value': 1, 'type': 'value'},
                                                  'entity': 'number', 'extractor': 'DucklingHTTPExtractor'},
                                                 {'start': 3, 'end': 4, 'text': '1', 'value': 1, 'confidence': 1.0,
                                                  'additional_info': {'value': 1, 'type': 'value'},
                                                  'entity': 'number', 'extractor': 'DucklingHTTPExtractor'},
                                                 {'start': 4, 'end': 5, 'text': '1', 'value': 1, 'confidence': 1.0,
                                                  'additional_info': {'value': 1, 'type': 'value'},
                                                  'entity': 'number', 'extractor': 'DucklingHTTPExtractor'},
                                                 {'start': 5, 'end': 6, 'text': '1', 'value': 1, 'confidence': 1.0,
                                                  'additional_info': {'value': 1, 'type': 'value'},
                                                  'entity': 'number', 'extractor': 'DucklingHTTPExtractor'},
                                                 {'start': 6, 'end': 7, 'text': '1', 'value': 1, 'confidence': 1.0,
                                                  'additional_info': {'value': 1, 'type': 'value'},
                                                  'entity': 'number', 'extractor': 'DucklingHTTPExtractor'},
                                                 {'start': 7, 'end': 8, 'text': '1', 'value': 1, 'confidence': 1.0,
                                                  'additional_info': {'value': 1, 'type': 'value'},
                                                  'entity': 'number', 'extractor': 'DucklingHTTPExtractor'},
                                                 {'start': 8, 'end': 9, 'text': '1', 'value': 1, 'confidence': 1.0,
                                                  'additional_info': {'value': 1, 'type': 'value'},
                                                  'entity': 'number', 'extractor': 'DucklingHTTPExtractor'},
                                                 {'start': 9, 'end': 10, 'text': '1', 'value': 1, 'confidence': 1.0,
                                                  'additional_info': {'value': 1, 'type': 'value'},
                                                  'entity': 'number', 'extractor': 'DucklingHTTPExtractor'},
                                                 {'start': 10, 'end': 11, 'text': '1', 'value': 1, 'confidence': 1.0,
                                                  'additional_info': {'value': 1, 'type': 'value'},
                                                  'entity': 'number', 'extractor': 'DucklingHTTPExtractor'},
                                                 {'start': 11, 'end': 12, 'text': '1', 'value': 1, 'confidence': 1.0,
                                                  'additional_info': {'value': 1, 'type': 'value'},
                                                  'entity': 'number', 'extractor': 'DucklingHTTPExtractor'}],
                                    'intent_ranking': [{'name': 'add_subscriber', 'confidence': 0.6653156280517578},
                                                       {'name': 'plan_info', 'confidence': 0.06193934753537178},
                                                       {'name': 'phone_number_change',
                                                        'confidence': 0.053489990532398224},
                                                       {'name': 'autopay', 'confidence': 0.013421786949038506},
                                                       {'name': 'autopay_update', 'confidence': 0.013023709878325462},
                                                       {'name': 'pay_someone_else', 'confidence': 0.00991435069590807},
                                                       {'name': 'remove_subscriber',
                                                        'confidence': 0.009756733663380146},
                                                       {'name': 'reactivate', 'confidence': 0.009636330418288708},
                                                       {'name': 'change_plan', 'confidence': 0.009616482071578503},
                                                       {'name': 'another_phone', 'confidence': 0.009423586539924145}],
                                    'text': "1111111111111",
                                    'asrConfidence': 1, 'recordingId': None, 'missed_intent': None,
                                    'message_id': '6524399f26124e8d87957f6c6ecb5a39',
                                    'metadata': {'dnis': '9282252467', 'message_type': 'SPOKEN',
                                                 'partials': ['1', '1 2', '1 2', "1 2 3"],
                                                 'channel_id': 1, 'type': 'text', 'template_name': 'temp_help_message',
                                                 'asr_threshold': 0.2, 'nlu_threshold': 0.63}},
                     'input_channel': 'OMNI_VOICE_00001', 'message_id': '6524399f26124e8d87957f6c6ecb5a39',
                     'entities_redacted': [
                         {'start': 0, 'end': 1, 'text': '1', 'value': 1, 'confidence': 1.0,
                          'additional_info': {'value': 1, 'type': 'value'},
                          'entity': 'number', 'extractor': 'DucklingHTTPExtractor'},
                         {'start': 1, 'end': 2, 'text': '1', 'value': 1, 'confidence': 1.0,
                          'additional_info': {'value': 1, 'type': 'value'},
                          'entity': 'number', 'extractor': 'DucklingHTTPExtractor'},
                         {'start': 2, 'end': 3, 'text': '1', 'value': 1, 'confidence': 1.0,
                          'additional_info': {'value': 1, 'type': 'value'},
                          'entity': 'number', 'extractor': 'DucklingHTTPExtractor'},
                         {'start': 3, 'end': 4, 'text': '1', 'value': 1, 'confidence': 1.0,
                          'additional_info': {'value': 1, 'type': 'value'},
                          'entity': 'number', 'extractor': 'DucklingHTTPExtractor'},
                         {'start': 0, 'end': 1, 'text': '1', 'value': 1, 'confidence': 1.0,
                          'additional_info': {'value': 1, 'type': 'value'},
                          'entity': 'number', 'extractor': 'DucklingHTTPExtractor'},
                         {'start': 1, 'end': 2, 'text': '1', 'value': 1, 'confidence': 1.0,
                          'additional_info': {'value': 1, 'type': 'value'},
                          'entity': 'number', 'extractor': 'DucklingHTTPExtractor'},
                         {'start': 2, 'end': 3, 'text': '1', 'value': 1, 'confidence': 1.0,
                          'additional_info': {'value': 1, 'type': 'value'},
                          'entity': 'number', 'extractor': 'DucklingHTTPExtractor'},
                         {'start': 3, 'end': 4, 'text': '1', 'value': 1, 'confidence': 1.0,
                          'additional_info': {'value': 1, 'type': 'value'},
                          'entity': 'number', 'extractor': 'DucklingHTTPExtractor'},
                         {'start': 4, 'end': 5, 'text': '1', 'value': 1, 'confidence': 1.0,
                          'additional_info': {'value': 1, 'type': 'value'},
                          'entity': 'number', 'extractor': 'DucklingHTTPExtractor'},
                         {'start': 5, 'end': 6, 'text': '1', 'value': 1, 'confidence': 1.0,
                          'additional_info': {'value': 1, 'type': 'value'},
                          'entity': 'number', 'extractor': 'DucklingHTTPExtractor'},
                         {'start': 6, 'end': 7, 'text': '1', 'value': 1, 'confidence': 1.0,
                          'additional_info': {'value': 1, 'type': 'value'},
                          'entity': 'number', 'extractor': 'DucklingHTTPExtractor'},
                         {'start': 7, 'end': 8, 'text': '1', 'value': 1, 'confidence': 1.0,
                          'additional_info': {'value': 1, 'type': 'value'},
                          'entity': 'number', 'extractor': 'DucklingHTTPExtractor'},
                         {'start': 8, 'end': 9, 'text': '1', 'value': 1, 'confidence': 1.0,
                          'additional_info': {'value': 1, 'type': 'value'},
                          'entity': 'number', 'extractor': 'DucklingHTTPExtractor'},
                         {'start': 9, 'end': 10, 'text': '1', 'value': 1, 'confidence': 1.0,
                          'additional_info': {'value': 1, 'type': 'value'},
                          'entity': 'number', 'extractor': 'DucklingHTTPExtractor'},
                         {'start': 10, 'end': 11, 'text': '1', 'value': 1, 'confidence': 1.0,
                          'additional_info': {'value': 1, 'type': 'value'},
                          'entity': 'number', 'extractor': 'DucklingHTTPExtractor'},
                         {'start': 11, 'end': 12, 'text': '1', 'value': 1, 'confidence': 1.0,
                          'additional_info': {'value': 1, 'type': 'value'},
                          'entity': 'number', 'extractor': 'DucklingHTTPExtractor'}]}
event_with_cc_num_redacted = {
    'entities_redacted': [
        {'additional_info': {'type': 'value', 'value': '*'},
         'confidence': 1.0,
         'end': 1,
         'entity': 'number',
         'extractor': 'DucklingHTTPExtractor',
         'start': 0,
         'text': '*',
         'value': '*'},
        {'additional_info': {'type': 'value', 'value': '*'},
         'confidence': 1.0,
         'end': 2,
         'entity': 'number',
         'extractor': 'DucklingHTTPExtractor',
         'start': 1,
         'text': '*',
         'value': '*'},
        {'additional_info': {'type': 'value', 'value': '*'},
         'confidence': 1.0,
         'end': 3,
         'entity': 'number',
         'extractor': 'DucklingHTTPExtractor',
         'start': 2,
         'text': '*',
         'value': '*'},
        {'additional_info': {'type': 'value', 'value': '*'},
         'confidence': 1.0,
         'end': 4,
         'entity': 'number',
         'extractor': 'DucklingHTTPExtractor',
         'start': 3,
         'text': '*',
         'value': '*'},
        {'additional_info': {'type': 'value', 'value': '*'},
         'confidence': 1.0,
         'end': 1,
         'entity': 'number',
         'extractor': 'DucklingHTTPExtractor',
         'start': 0,
         'text': '*',
         'value': '*'},
        {'additional_info': {'type': 'value', 'value': '*'},
         'confidence': 1.0,
         'end': 2,
         'entity': 'number',
         'extractor': 'DucklingHTTPExtractor',
         'start': 1,
         'text': '*',
         'value': '*'},
        {'additional_info': {'type': 'value', 'value': '*'},
         'confidence': 1.0,
         'end': 3,
         'entity': 'number',
         'extractor': 'DucklingHTTPExtractor',
         'start': 2,
         'text': '*',
         'value': '*'},
        {'additional_info': {'type': 'value', 'value': '*'},
         'confidence': 1.0,
         'end': 4,
         'entity': 'number',
         'extractor': 'DucklingHTTPExtractor',
         'start': 3,
         'text': '*',
         'value': '*'},
        {'additional_info': {'type': 'value', 'value': '*'},
         'confidence': 1.0,
         'end': 5,
         'entity': 'number',
         'extractor': 'DucklingHTTPExtractor',
         'start': 4,
         'text': '*',
         'value': '*'},
        {'additional_info': {'type': 'value', 'value': '*'},
         'confidence': 1.0,
         'end': 6,
         'entity': 'number',
         'extractor': 'DucklingHTTPExtractor',
         'start': 5,
         'text': '*',
         'value': '*'},
        {'additional_info': {'type': 'value', 'value': '*'},
         'confidence': 1.0,
         'end': 7,
         'entity': 'number',
         'extractor': 'DucklingHTTPExtractor',
         'start': 6,
         'text': '*',
         'value': '*'},
        {'additional_info': {'type': 'value', 'value': '*'},
         'confidence': 1.0,
         'end': 8,
         'entity': 'number',
         'extractor': 'DucklingHTTPExtractor',
         'start': 7,
         'text': '*',
         'value': '*'},
        {'additional_info': {'type': 'value', 'value': '*'},
         'confidence': 1.0,
         'end': 9,
         'entity': 'number',
         'extractor': 'DucklingHTTPExtractor',
         'start': 8,
         'text': '*',
         'value': '*'},
        {'additional_info': {'type': 'value', 'value': '*'},
         'confidence': 1.0,
         'end': 10,
         'entity': 'number',
         'extractor': 'DucklingHTTPExtractor',
         'start': 9,
         'text': '*',
         'value': '*'},
        {'additional_info': {'type': 'value', 'value': '*'},
         'confidence': 1.0,
         'end': 11,
         'entity': 'number',
         'extractor': 'DucklingHTTPExtractor',
         'start': 10,
         'text': '*',
         'value': '*'},
        {'additional_info': {'type': 'value', 'value': '*'},
         'confidence': 1.0,
         'end': 12,
         'entity': 'number',
         'extractor': 'DucklingHTTPExtractor',
         'start': 11,
         'text': '*',
         'value': '*'}],
    'event': 'user',
    'input_channel': 'OMNI_VOICE_00001',
    'message_id': '6524399f26124e8d87957f6c6ecb5a39',
    'metadata': {'asr_threshold': 0.2,
                 'channel_id': 1,
                 'dnis': '9282252467',
                 'message_type': 'SPOKEN',
                 'nlu_threshold': 0.63,
                 'partials': ['1', '12', '12', '123'],
                 'template_name': 'temp_help_message',
                 'type': 'text'},
    'parse_data': {'asrConfidence': 1,
                   'entities': [
                       {'additional_info': {'type': 'value',
                                            'value': '*'},
                        'confidence': 1.0,
                        'end': 1,
                        'entity': 'number',
                        'extractor': 'DucklingHTTPExtractor',
                        'start': 0,
                        'text': '*',
                        'value': '*'},
                       {'additional_info': {'type': 'value',
                                            'value': '*'},
                        'confidence': 1.0,
                        'end': 2,
                        'entity': 'number',
                        'extractor': 'DucklingHTTPExtractor',
                        'start': 1,
                        'text': '*',
                        'value': '*'},
                       {'additional_info': {'type': 'value',
                                            'value': '*'},
                        'confidence': 1.0,
                        'end': 3,
                        'entity': 'number',
                        'extractor': 'DucklingHTTPExtractor',
                        'start': 2,
                        'text': '*',
                        'value': '*'},
                       {'additional_info': {'type': 'value',
                                            'value': '*'},
                        'confidence': 1.0,
                        'end': 4,
                        'entity': 'number',
                        'extractor': 'DucklingHTTPExtractor',
                        'start': 3,
                        'text': '*',
                        'value': '*'},
                       {'additional_info': {'type': 'value',
                                            'value': '*'},
                        'confidence': 1.0,
                        'end': 1,
                        'entity': 'number',
                        'extractor': 'DucklingHTTPExtractor',
                        'start': 0,
                        'text': '*',
                        'value': '*'},
                       {'additional_info': {'type': 'value',
                                            'value': '*'},
                        'confidence': 1.0,
                        'end': 2,
                        'entity': 'number',
                        'extractor': 'DucklingHTTPExtractor',
                        'start': 1,
                        'text': '*',
                        'value': '*'},
                       {'additional_info': {'type': 'value',
                                            'value': '*'},
                        'confidence': 1.0,
                        'end': 3,
                        'entity': 'number',
                        'extractor': 'DucklingHTTPExtractor',
                        'start': 2,
                        'text': '*',
                        'value': '*'},
                       {'additional_info': {'type': 'value',
                                            'value': '*'},
                        'confidence': 1.0,
                        'end': 4,
                        'entity': 'number',
                        'extractor': 'DucklingHTTPExtractor',
                        'start': 3,
                        'text': '*',
                        'value': '*'},
                       {'additional_info': {'type': 'value',
                                            'value': '*'},
                        'confidence': 1.0,
                        'end': 5,
                        'entity': 'number',
                        'extractor': 'DucklingHTTPExtractor',
                        'start': 4,
                        'text': '*',
                        'value': '*'},
                       {'additional_info': {'type': 'value',
                                            'value': '*'},
                        'confidence': 1.0,
                        'end': 6,
                        'entity': 'number',
                        'extractor': 'DucklingHTTPExtractor',
                        'start': 5,
                        'text': '*',
                        'value': '*'},
                       {'additional_info': {'type': 'value',
                                            'value': '*'},
                        'confidence': 1.0,
                        'end': 7,
                        'entity': 'number',
                        'extractor': 'DucklingHTTPExtractor',
                        'start': 6,
                        'text': '*',
                        'value': '*'},
                       {'additional_info': {'type': 'value',
                                            'value': '*'},
                        'confidence': 1.0,
                        'end': 8,
                        'entity': 'number',
                        'extractor': 'DucklingHTTPExtractor',
                        'start': 7,
                        'text': '*',
                        'value': '*'},
                       {'additional_info': {'type': 'value',
                                            'value': '*'},
                        'confidence': 1.0,
                        'end': 9,
                        'entity': 'number',
                        'extractor': 'DucklingHTTPExtractor',
                        'start': 8,
                        'text': '*',
                        'value': '*'},
                       {'additional_info': {'type': 'value',
                                            'value': '*'},
                        'confidence': 1.0,
                        'end': 10,
                        'entity': 'number',
                        'extractor': 'DucklingHTTPExtractor',
                        'start': 9,
                        'text': '*',
                        'value': '*'},
                       {'additional_info': {'type': 'value',
                                            'value': '*'},
                        'confidence': 1.0,
                        'end': 11,
                        'entity': 'number',
                        'extractor': 'DucklingHTTPExtractor',
                        'start': 10,
                        'text': '*',
                        'value': '*'},
                       {'additional_info': {'type': 'value',
                                            'value': '*'},
                        'confidence': 1.0,
                        'end': 12,
                        'entity': 'number',
                        'extractor': 'DucklingHTTPExtractor',
                        'start': 11,
                        'text': '*',
                        'value': '*'}],
                   'intent': {'confidence': 0.6653156280517578,
                              'name': 'add_subscriber'},
                   'intent_ranking': [
                       {'confidence': 0.6653156280517578,
                        'name': 'add_subscriber'},
                       {'confidence': 0.06193934753537178,
                        'name': 'plan_info'},
                       {'confidence': 0.053489990532398224,
                        'name': 'phone_number_change'},
                       {'confidence': 0.013421786949038506,
                        'name': 'autopay'},
                       {'confidence': 0.013023709878325462,
                        'name': 'autopay_update'},
                       {'confidence': 0.00991435069590807,
                        'name': 'pay_someone_else'},
                       {'confidence': 0.009756733663380146,
                        'name': 'remove_subscriber'},
                       {'confidence': 0.009636330418288708,
                        'name': 'reactivate'},
                       {'confidence': 0.009616482071578503,
                        'name': 'change_plan'},
                       {'confidence': 0.009423586539924145,
                        'name': 'another_phone'}],
                   'message_id': '6524399f26124e8d87957f6c6ecb5a39',
                   'metadata': {'asr_threshold': 0.2,
                                'channel_id': 1,
                                'dnis': '9282252467',
                                'message_type': 'SPOKEN',
                                'nlu_threshold': 0.63,
                                'partials': ['1', '12', '12', '123'],
                                'template_name': 'temp_help_message',
                                'type': 'text'},
                   'missed_intent': None,
                   'recordingId': None,
                   'text': '****************'},
    'text': '****************',
    'timestamp': 1621281543.1603343}

event_with_cc_num_2 = {
    'sender_id': '05fa294af33745a5b34ee30c7b06b996',
    'event': 'user',
    'timestamp': 1627090353.228758,
    'metadata': {
        'replyType': 'text',
        'channel_id': 1,
        'original_text': 'my cc is 1111111111111111',
        'should_redact': False,
        'type': 'text',
        'template_name': 'utter_greet',
        'asr_threshold': 0.2,
        'nlu_threshold': 0.67,
        'group': 'SALUTATION'
    },
    'text': 'my cc is 1111111111111111',
    'parse_data': {
        'intent': {
            'name': 'None',
            'confidence': 0.5955944657325745
        },
        'entities': [{
            'start': 9,
            'end': 12,
            'text': '1',
            'value': 1,
            'confidence': 1.0,
            'additional_info': {
                'value': 1,
                'type': 'value'
            },
            'entity': 'number',
            'extractor': 'DucklingHTTPExtractor'
        }, {
            'start': 13,
            'end': 16,
            'text': '1',
            'value': 1,
            'confidence': 1.0,
            'additional_info': {
                'value': 1,
                'type': 'value'
            },
            'entity': 'number',
            'extractor': 'DucklingHTTPExtractor'
        }, {
            'start': 17,
            'end': 20,
            'text': '1',
            'value': 1,
            'confidence': 1.0,
            'additional_info': {
                'value': 1,
                'type': 'value'
            },
            'entity': 'number',
            'extractor': 'DucklingHTTPExtractor'
        }, {
            'start': 21,
            'end': 24,
            'text': '1',
            'value': 1,
            'confidence': 1.0,
            'additional_info': {
                'value': 1,
                'type': 'value'
            },
            'entity': 'number',
            'extractor': 'DucklingHTTPExtractor'
        }, {
            'start': 25,
            'end': 28,
            'text': '1',
            'value': 1,
            'confidence': 1.0,
            'additional_info': {
                'value': 1,
                'type': 'value'
            },
            'entity': 'number',
            'extractor': 'DucklingHTTPExtractor'
        }, {
            'start': 29,
            'end': 32,
            'text': '1',
            'value': 1,
            'confidence': 1.0,
            'additional_info': {
                'value': 1,
                'type': 'value'
            },
            'entity': 'number',
            'extractor': 'DucklingHTTPExtractor'
        }, {
            'start': 33,
            'end': 36,
            'text': '1',
            'value': 1,
            'confidence': 1.0,
            'additional_info': {
                'value': 1,
                'type': 'value'
            },
            'entity': 'number',
            'extractor': 'DucklingHTTPExtractor'
        }, {
            'start': 37,
            'end': 40,
            'text': '1',
            'value': 1,
            'confidence': 1.0,
            'additional_info': {
                'value': 1,
                'type': 'value'
            },
            'entity': 'number',
            'extractor': 'DucklingHTTPExtractor'
        }, {
            'start': 41,
            'end': 44,
            'text': '1',
            'value': 1,
            'confidence': 1.0,
            'additional_info': {
                'value': 1,
                'type': 'value'
            },
            'entity': 'number',
            'extractor': 'DucklingHTTPExtractor'
        }, {
            'start': 45,
            'end': 48,
            'text': '1',
            'value': 1,
            'confidence': 1.0,
            'additional_info': {
                'value': 1,
                'type': 'value'
            },
            'entity': 'number',
            'extractor': 'DucklingHTTPExtractor'
        }, {
            'start': 49,
            'end': 52,
            'text': '1',
            'value': 1,
            'confidence': 1.0,
            'additional_info': {
                'value': 1,
                'type': 'value'
            },
            'entity': 'number',
            'extractor': 'DucklingHTTPExtractor'
        }, {
            'start': 53,
            'end': 56,
            'text': '1',
            'value': 1,
            'confidence': 1.0,
            'additional_info': {
                'value': 1,
                'type': 'value'
            },
            'entity': 'number',
            'extractor': 'DucklingHTTPExtractor'
        }, {
            'start': 57,
            'end': 60,
            'text': '1',
            'value': 1,
            'confidence': 1.0,
            'additional_info': {
                'value': 1,
                'type': 'value'
            },
            'entity': 'number',
            'extractor': 'DucklingHTTPExtractor'
        }, {
            'start': 61,
            'end': 64,
            'text': '1',
            'value': 1,
            'confidence': 1.0,
            'additional_info': {
                'value': 1,
                'type': 'value'
            },
            'entity': 'number',
            'extractor': 'DucklingHTTPExtractor'
        }, {
            'start': 65,
            'end': 68,
            'text': '1',
            'value': 1,
            'confidence': 1.0,
            'additional_info': {
                'value': 1,
                'type': 'value'
            },
            'entity': 'number',
            'extractor': 'DucklingHTTPExtractor'
        }, {
            'start': 69,
            'end': 72,
            'text': '1',
            'value': 1,
            'confidence': 1.0,
            'additional_info': {
                'value': 1,
                'type': 'value'
            },
            'entity': 'number',
            'extractor': 'DucklingHTTPExtractor'
        }],
        'intent_ranking': [{
            'name': 'None',
            'confidence': 0.5955944657325745
        }, {
            'name': 'card',
            'confidence': 0.4034712314605713
        }, {
            'name': 'freeze',
            'confidence': 0.0006689034635201097
        }, {
            'name': 'language',
            'confidence': 0.00012367829913273454
        }, {
            'name': 'autopay',
            'confidence': 0.00010715128155425191
        }, {
            'name': 'disconnect',
            'confidence': 1.715622602205258e-05
        }, {
            'name': 'handoff',
            'confidence': 9.751319339557085e-06
        }, {
            'name': 'thanks',
            'confidence': 3.094106205026037e-06
        }, {
            'name': 'transfer',
            'confidence': 3.039700004592305e-06
        }, {
            'name': 'deny',
            'confidence': 1.0337059848097851e-06
        }],
        'text': 'my cc is 1111111111111111',
        'asrConfidence': 1,
        'recordingId': None,
        'missed_intent': True,
        'message_id': '10837e5268ca40579d8fc90ba63a554c',
        'metadata': {
            'replyType': 'text',
            'channel_id': 1,
            'original_text': 'my cc is 1111111111111111',
            'should_redact': False,
            'type': 'text',
            'template_name': 'utter_greet',
            'asr_threshold': 0.2,
            'nlu_threshold': 0.67,
            'group': 'SALUTATION'
        }
    },
    'input_channel': 'OMNI_WEBCHAT_00001',
    'message_id': '10837e5268ca40579d8fc90ba63a554c',
    'entities_redacted': [
        {
            'start': 9,
            'end': 12,
            'text': '1',
            'value': 1,
            'confidence': 1.0,
            'additional_info': {
                'value': 1,
                'type': 'value'
            },
            'entity': 'number',
            'extractor': 'DucklingHTTPExtractor'
        }, {
            'start': 13,
            'end': 16,
            'text': '1',
            'value': 1,
            'confidence': 1.0,
            'additional_info': {
                'value': 1,
                'type': 'value'
            },
            'entity': 'number',
            'extractor': 'DucklingHTTPExtractor'
        }, {
            'start': 17,
            'end': 20,
            'text': '1',
            'value': 1,
            'confidence': 1.0,
            'additional_info': {
                'value': 1,
                'type': 'value'
            },
            'entity': 'number',
            'extractor': 'DucklingHTTPExtractor'
        }, {
            'start': 21,
            'end': 24,
            'text': '1',
            'value': 1,
            'confidence': 1.0,
            'additional_info': {
                'value': 1,
                'type': 'value'
            },
            'entity': 'number',
            'extractor': 'DucklingHTTPExtractor'
        }, {
            'start': 25,
            'end': 28,
            'text': '1',
            'value': 1,
            'confidence': 1.0,
            'additional_info': {
                'value': 1,
                'type': 'value'
            },
            'entity': 'number',
            'extractor': 'DucklingHTTPExtractor'
        }, {
            'start': 29,
            'end': 32,
            'text': '1',
            'value': 1,
            'confidence': 1.0,
            'additional_info': {
                'value': 1,
                'type': 'value'
            },
            'entity': 'number',
            'extractor': 'DucklingHTTPExtractor'
        }, {
            'start': 33,
            'end': 36,
            'text': '1',
            'value': 1,
            'confidence': 1.0,
            'additional_info': {
                'value': 1,
                'type': 'value'
            },
            'entity': 'number',
            'extractor': 'DucklingHTTPExtractor'
        }, {
            'start': 37,
            'end': 40,
            'text': '1',
            'value': 1,
            'confidence': 1.0,
            'additional_info': {
                'value': 1,
                'type': 'value'
            },
            'entity': 'number',
            'extractor': 'DucklingHTTPExtractor'
        }, {
            'start': 41,
            'end': 44,
            'text': '1',
            'value': 1,
            'confidence': 1.0,
            'additional_info': {
                'value': 1,
                'type': 'value'
            },
            'entity': 'number',
            'extractor': 'DucklingHTTPExtractor'
        }, {
            'start': 45,
            'end': 48,
            'text': '1',
            'value': 1,
            'confidence': 1.0,
            'additional_info': {
                'value': 1,
                'type': 'value'
            },
            'entity': 'number',
            'extractor': 'DucklingHTTPExtractor'
        }, {
            'start': 49,
            'end': 52,
            'text': '1',
            'value': 1,
            'confidence': 1.0,
            'additional_info': {
                'value': 1,
                'type': 'value'
            },
            'entity': 'number',
            'extractor': 'DucklingHTTPExtractor'
        }, {
            'start': 53,
            'end': 56,
            'text': '1',
            'value': 1,
            'confidence': 1.0,
            'additional_info': {
                'value': 1,
                'type': 'value'
            },
            'entity': 'number',
            'extractor': 'DucklingHTTPExtractor'
        }, {
            'start': 57,
            'end': 60,
            'text': '1',
            'value': 1,
            'confidence': 1.0,
            'additional_info': {
                'value': 1,
                'type': 'value'
            },
            'entity': 'number',
            'extractor': 'DucklingHTTPExtractor'
        }, {
            'start': 61,
            'end': 64,
            'text': '1',
            'value': 1,
            'confidence': 1.0,
            'additional_info': {
                'value': 1,
                'type': 'value'
            },
            'entity': 'number',
            'extractor': 'DucklingHTTPExtractor'
        }, {
            'start': 65,
            'end': 68,
            'text': '1',
            'value': 1,
            'confidence': 1.0,
            'additional_info': {
                'value': 1,
                'type': 'value'
            },
            'entity': 'number',
            'extractor': 'DucklingHTTPExtractor'
        }, {
            'start': 69,
            'end': 72,
            'text': '1',
            'value': 1,
            'confidence': 1.0,
            'additional_info': {
                'value': 1,
                'type': 'value'
            },
            'entity': 'number',
            'extractor': 'DucklingHTTPExtractor'
        }]
}
event_with_cc_num_2_redacted = {
    'sender_id': '05fa294af33745a5b34ee30c7b06b996',
    'event': 'user',
    'timestamp': 1627090353.228758,
    'metadata': {
        'replyType': 'text',
        'channel_id': 1,
        'original_text': 'my cc is ****************',
        'should_redact': False,
        'type': 'text',
        'template_name': 'utter_greet',
        'asr_threshold': 0.2,
        'nlu_threshold': 0.67,
        'group': 'SALUTATION'
    },
    'text': 'my cc is ****************',
    'parse_data': {
        'intent': {
            'name': 'None',
            'confidence': 0.5955944657325745
        },
        'entities': [
            {
                'start': 9,
                'end': 12,
                'text': '*',
                'value': '*',
                'confidence': 1.0,
                'additional_info': {
                    'value': '*',
                    'type': 'value'
                },
                'entity': 'number',
                'extractor': 'DucklingHTTPExtractor'
            }, {
                'start': 13,
                'end': 16,
                'text': '*',
                'value': '*',
                'confidence': 1.0,
                'additional_info': {
                    'value': '*',
                    'type': 'value'
                },
                'entity': 'number',
                'extractor': 'DucklingHTTPExtractor'
            }, {
                'start': 17,
                'end': 20,
                'text': '*',
                'value': '*',
                'confidence': 1.0,
                'additional_info': {
                    'value': '*',
                    'type': 'value'
                },
                'entity': 'number',
                'extractor': 'DucklingHTTPExtractor'
            }, {
                'start': 21,
                'end': 24,
                'text': '*',
                'value': '*',
                'confidence': 1.0,
                'additional_info': {
                    'value': '*',
                    'type': 'value'
                },
                'entity': 'number',
                'extractor': 'DucklingHTTPExtractor'
            }, {
                'start': 25,
                'end': 28,
                'text': '*',
                'value': '*',
                'confidence': 1.0,
                'additional_info': {
                    'value': '*',
                    'type': 'value'
                },
                'entity': 'number',
                'extractor': 'DucklingHTTPExtractor'
            }, {
                'start': 29,
                'end': 32,
                'text': '*',
                'value': '*',
                'confidence': 1.0,
                'additional_info': {
                    'value': '*',
                    'type': 'value'
                },
                'entity': 'number',
                'extractor': 'DucklingHTTPExtractor'
            }, {
                'start': 33,
                'end': 36,
                'text': '*',
                'value': '*',
                'confidence': 1.0,
                'additional_info': {
                    'value': '*',
                    'type': 'value'
                },
                'entity': 'number',
                'extractor': 'DucklingHTTPExtractor'
            }, {
                'start': 37,
                'end': 40,
                'text': '*',
                'value': '*',
                'confidence': 1.0,
                'additional_info': {
                    'value': '*',
                    'type': 'value'
                },
                'entity': 'number',
                'extractor': 'DucklingHTTPExtractor'
            }, {
                'start': 41,
                'end': 44,
                'text': '*',
                'value': '*',
                'confidence': 1.0,
                'additional_info': {
                    'value': '*',
                    'type': 'value'
                },
                'entity': 'number',
                'extractor': 'DucklingHTTPExtractor'
            }, {
                'start': 45,
                'end': 48,
                'text': '*',
                'value': '*',
                'confidence': 1.0,
                'additional_info': {
                    'value': '*',
                    'type': 'value'
                },
                'entity': 'number',
                'extractor': 'DucklingHTTPExtractor'
            }, {
                'start': 49,
                'end': 52,
                'text': '*',
                'value': '*',
                'confidence': 1.0,
                'additional_info': {
                    'value': '*',
                    'type': 'value'
                },
                'entity': 'number',
                'extractor': 'DucklingHTTPExtractor'
            }, {
                'start': 53,
                'end': 56,
                'text': '*',
                'value': '*',
                'confidence': 1.0,
                'additional_info': {
                    'value': '*',
                    'type': 'value'
                },
                'entity': 'number',
                'extractor': 'DucklingHTTPExtractor'
            }, {
                'start': 57,
                'end': 60,
                'text': '*',
                'value': '*',
                'confidence': 1.0,
                'additional_info': {
                    'value': '*',
                    'type': 'value'
                },
                'entity': 'number',
                'extractor': 'DucklingHTTPExtractor'
            }, {
                'start': 61,
                'end': 64,
                'text': '*',
                'value': '*',
                'confidence': 1.0,
                'additional_info': {
                    'value': '*',
                    'type': 'value'
                },
                'entity': 'number',
                'extractor': 'DucklingHTTPExtractor'
            }, {
                'start': 65,
                'end': 68,
                'text': '*',
                'value': '*',
                'confidence': 1.0,
                'additional_info': {
                    'value': '*',
                    'type': 'value'
                },
                'entity': 'number',
                'extractor': 'DucklingHTTPExtractor'
            }, {
                'start': 69,
                'end': 72,
                'text': '*',
                'value': '*',
                'confidence': 1.0,
                'additional_info': {
                    'value': '*',
                    'type': 'value'
                },
                'entity': 'number',
                'extractor': 'DucklingHTTPExtractor'
            }],
        'intent_ranking': [
            {
                'name': 'None',
                'confidence': 0.5955944657325745
            }, {
                'name': 'card',
                'confidence': 0.4034712314605713
            }, {
                'name': 'freeze',
                'confidence': 0.0006689034635201097
            }, {
                'name': 'language',
                'confidence': 0.00012367829913273454
            }, {
                'name': 'autopay',
                'confidence': 0.00010715128155425191
            }, {
                'name': 'disconnect',
                'confidence': 1.715622602205258e-05
            }, {
                'name': 'handoff',
                'confidence': 9.751319339557085e-06
            }, {
                'name': 'thanks',
                'confidence': 3.094106205026037e-06
            }, {
                'name': 'transfer',
                'confidence': 3.039700004592305e-06
            }, {
                'name': 'deny',
                'confidence': 1.0337059848097851e-06
            }],
        'text': 'my cc is ****************',
        'asrConfidence': 1,
        'recordingId': None,
        'missed_intent': True,
        'message_id': '10837e5268ca40579d8fc90ba63a554c',
        'metadata': {
            'replyType': 'text',
            'channel_id': 1,
            'original_text': 'my cc is ****************',
            'should_redact': False,
            'type': 'text',
            'template_name': 'utter_greet',
            'asr_threshold': 0.2,
            'nlu_threshold': 0.67,
            'group': 'SALUTATION'
        }
    },
    'input_channel': 'OMNI_WEBCHAT_00001',
    'message_id': '10837e5268ca40579d8fc90ba63a554c',
    'entities_redacted': [
        {
            'start': 9,
            'end': 12,
            'text': '*',
            'value': '*',
            'confidence': 1.0,
            'additional_info': {
                'value': '*',
                'type': 'value'
            },
            'entity': 'number',
            'extractor': 'DucklingHTTPExtractor'
        }, {
            'start': 13,
            'end': 16,
            'text': '*',
            'value': '*',
            'confidence': 1.0,
            'additional_info': {
                'value': '*',
                'type': 'value'
            },
            'entity': 'number',
            'extractor': 'DucklingHTTPExtractor'
        }, {
            'start': 17,
            'end': 20,
            'text': '*',
            'value': '*',
            'confidence': 1.0,
            'additional_info': {
                'value': '*',
                'type': 'value'
            },
            'entity': 'number',
            'extractor': 'DucklingHTTPExtractor'
        }, {
            'start': 21,
            'end': 24,
            'text': '*',
            'value': '*',
            'confidence': 1.0,
            'additional_info': {
                'value': '*',
                'type': 'value'
            },
            'entity': 'number',
            'extractor': 'DucklingHTTPExtractor'
        }, {
            'start': 25,
            'end': 28,
            'text': '*',
            'value': '*',
            'confidence': 1.0,
            'additional_info': {
                'value': '*',
                'type': 'value'
            },
            'entity': 'number',
            'extractor': 'DucklingHTTPExtractor'
        }, {
            'start': 29,
            'end': 32,
            'text': '*',
            'value': '*',
            'confidence': 1.0,
            'additional_info': {
                'value': '*',
                'type': 'value'
            },
            'entity': 'number',
            'extractor': 'DucklingHTTPExtractor'
        }, {
            'start': 33,
            'end': 36,
            'text': '*',
            'value': '*',
            'confidence': 1.0,
            'additional_info': {
                'value': '*',
                'type': 'value'
            },
            'entity': 'number',
            'extractor': 'DucklingHTTPExtractor'
        }, {
            'start': 37,
            'end': 40,
            'text': '*',
            'value': '*',
            'confidence': 1.0,
            'additional_info': {
                'value': '*',
                'type': 'value'
            },
            'entity': 'number',
            'extractor': 'DucklingHTTPExtractor'
        }, {
            'start': 41,
            'end': 44,
            'text': '*',
            'value': '*',
            'confidence': 1.0,
            'additional_info': {
                'value': '*',
                'type': 'value'
            },
            'entity': 'number',
            'extractor': 'DucklingHTTPExtractor'
        }, {
            'start': 45,
            'end': 48,
            'text': '*',
            'value': '*',
            'confidence': 1.0,
            'additional_info': {
                'value': '*',
                'type': 'value'
            },
            'entity': 'number',
            'extractor': 'DucklingHTTPExtractor'
        }, {
            'start': 49,
            'end': 52,
            'text': '*',
            'value': '*',
            'confidence': 1.0,
            'additional_info': {
                'value': '*',
                'type': 'value'
            },
            'entity': 'number',
            'extractor': 'DucklingHTTPExtractor'
        }, {
            'start': 53,
            'end': 56,
            'text': '*',
            'value': '*',
            'confidence': 1.0,
            'additional_info': {
                'value': '*',
                'type': 'value'
            },
            'entity': 'number',
            'extractor': 'DucklingHTTPExtractor'
        }, {
            'start': 57,
            'end': 60,
            'text': '*',
            'value': '*',
            'confidence': 1.0,
            'additional_info': {
                'value': '*',
                'type': 'value'
            },
            'entity': 'number',
            'extractor': 'DucklingHTTPExtractor'
        }, {
            'start': 61,
            'end': 64,
            'text': '*',
            'value': '*',
            'confidence': 1.0,
            'additional_info': {
                'value': '*',
                'type': 'value'
            },
            'entity': 'number',
            'extractor': 'DucklingHTTPExtractor'
        }, {
            'start': 65,
            'end': 68,
            'text': '*',
            'value': '*',
            'confidence': 1.0,
            'additional_info': {
                'value': '*',
                'type': 'value'
            },
            'entity': 'number',
            'extractor': 'DucklingHTTPExtractor'
        }, {
            'start': 69,
            'end': 72,
            'text': '*',
            'value': '*',
            'confidence': 1.0,
            'additional_info': {
                'value': '*',
                'type': 'value'
            },
            'entity': 'number',
            'extractor': 'DucklingHTTPExtractor'
        }]
}


spanish_event_with_cc_number = {
        "sender_id": "CAb6bf537d509119433250320ac0c640ccc115dfb1",
        "event": "user",
        "timestamp": 1645850635.3806438,
        "metadata": {
            "dnis": "7112014981",
            "privacy_mode": True,
            "request_id": "RQb6bf****************d****************ac0c****************ccc****************dfb1",
            "message_type": "GRAMMAR",
            "error_type": "no_match",
            "error_message": "No Match",
            "reporting_error_type": "no_match",
            "reporting_error_message": "No Match",
            "no_match_input": "uno uno dos dos tres tres quatro quatro seis siete nueve cero cero dos cinco cinco",
            "grammar_input_mode": "speech",
            "channel_id": "3",
            "original_text": "",
            "should_redact": True,
            "type": "text",
            "error": True,
            "active_form": "action_credit_card_collector",
            "requested_slot": "cc_number",
            "template_name": "utter_ask_cc_number",
            "asr_threshold": 0.0,
            "nlu_threshold": 0.63,
            "group": "cc_number"
        },
        "text": "",
        "parse_data": {
            "intent": {
                "name": None,
                "confidence": 0.0
            },
            "entities": [],
            "text": "",
            "asrConfidence": 1,
            "recordingId": None,
            "missed_intent": False,
            "message_id": "fc636e003e704bb3a3005177e170ef56",
            "metadata": {
                "dnis": "7112014981",
                "privacy_mode": True,
                "request_id": "RQb6bf****************d****************ac0c****************ccc****************dfb1",
                "message_type": "GRAMMAR",
                "error_type": "no_match",
                "error_message": "No Match",
                "reporting_error_type": "no_match",
                "reporting_error_message": "No Match",
                "no_match_input": "uno uno dos dos tres tres quatro quatro seis siete nueve cero cero dos cinco cinco",
                "grammar_input_mode": "speech",
                "channel_id": "3",
                "original_text": "",
                "should_redact": True,
                "type": "text",
                "error": True,
                "active_form": "action_credit_card_collector",
                "requested_slot": "cc_number",
                "template_name": "utter_ask_cc_number",
                "asr_threshold": 0.0,
                "nlu_threshold": 0.63,
                "group": "cc_number"
            }
        },
        "input_channel": "OMNI_VOICE_00001",
        "message_id": "fc636e003e704bb3a3005177e170ef56",
        "entities_redacted": [],
        "step_number": 686
    }

spanish_event_without_cc_number = {
        "sender_id": "CAb6bf537d509119433250320ac0c640ccc115dfb1",
        "event": "user",
        "timestamp": 1645850635.3806438,
        "metadata": {
            "dnis": "7112014981",
            "privacy_mode": True,
            "request_id": "RQb6bf****************d****************ac0c****************ccc****************dfb1",
            "message_type": "GRAMMAR",
            "error_type": "no_match",
            "error_message": "No Match",
            "reporting_error_type": "no_match",
            "reporting_error_message": "No Match",
            "no_match_input": "****************",
            "grammar_input_mode": "speech",
            "channel_id": "3",
            "original_text": "",
            "should_redact": True,
            "type": "text",
            "error": True,
            "active_form": "action_credit_card_collector",
            "requested_slot": "cc_number",
            "template_name": "utter_ask_cc_number",
            "asr_threshold": 0.0,
            "nlu_threshold": 0.63,
            "group": "cc_number"
        },
        "text": "",
        "parse_data": {
            "intent": {
                "name": None,
                "confidence": 0.0
            },
            "entities": [],
            "text": "",
            "asrConfidence": 1,
            "recordingId": None,
            "missed_intent": False,
            "message_id": "fc636e003e704bb3a3005177e170ef56",
            "metadata": {
                "dnis": "7112014981",
                "privacy_mode": True,
                "request_id": "RQb6bf****************d****************ac0c****************ccc****************dfb1",
                "message_type": "GRAMMAR",
                "error_type": "no_match",
                "error_message": "No Match",
                "reporting_error_type": "no_match",
                "reporting_error_message": "No Match",
                "no_match_input": "****************",
                "grammar_input_mode": "speech",
                "channel_id": "3",
                "original_text": "",
                "should_redact": True,
                "type": "text",
                "error": True,
                "active_form": "action_credit_card_collector",
                "requested_slot": "cc_number",
                "template_name": "utter_ask_cc_number",
                "asr_threshold": 0.0,
                "nlu_threshold": 0.63,
                "group": "cc_number"
            }
        },
        "input_channel": "OMNI_VOICE_00001",
        "message_id": "fc636e003e704bb3a3005177e170ef56",
        "entities_redacted": [],
        "step_number": 686
    }

spanish_event_with_cc_number_partial = {
        "sender_id": "CAb6bf537d509119433250320ac0c640ccc115dfb1",
        "event": "user",
        "timestamp": 1645850635.3806438,
        "metadata": {
            "dnis": "7112014981",
            "privacy_mode": True,
            "request_id": "RQb6bf****************d****************ac0c****************ccc****************dfb1",
            "message_type": "GRAMMAR",
            "error_type": "no_match",
            "error_message": "No Match",
            "reporting_error_type": "no_match",
            "reporting_error_message": "No Match",
            "no_match_input": "uno dos",
            "grammar_input_mode": "speech",
            "channel_id": "3",
            "original_text": "",
            "should_redact": True,
            "type": "text",
            "error": True,
            "active_form": "action_credit_card_collector",
            "requested_slot": "cc_number",
            "template_name": "utter_ask_cc_number",
            "asr_threshold": 0.0,
            "nlu_threshold": 0.63,
            "group": "cc_number"
        },
        "text": "",
        "parse_data": {
            "intent": {
                "name": None,
                "confidence": 0.0
            },
            "entities": [],
            "text": "",
            "asrConfidence": 1,
            "recordingId": None,
            "missed_intent": False,
            "message_id": "fc636e003e704bb3a3005177e170ef56",
            "metadata": {
                "dnis": "7112014981",
                "privacy_mode": True,
                "request_id": "RQb6bf****************d****************ac0c****************ccc****************dfb1",
                "message_type": "GRAMMAR",
                "error_type": "no_match",
                "error_message": "No Match",
                "reporting_error_type": "no_match",
                "reporting_error_message": "No Match",
                "no_match_input": "uno dos",
                "grammar_input_mode": "speech",
                "channel_id": "3",
                "original_text": "",
                "should_redact": True,
                "type": "text",
                "error": True,
                "active_form": "action_credit_card_collector",
                "requested_slot": "cc_number",
                "template_name": "utter_ask_cc_number",
                "asr_threshold": 0.0,
                "nlu_threshold": 0.63,
                "group": "cc_number"
            }
        },
        "input_channel": "OMNI_VOICE_00001",
        "message_id": "fc636e003e704bb3a3005177e170ef56",
        "entities_redacted": [],
        "step_number": 686
    }

spanish_event_without_cc_number_partial = {
    'sender_id': 'CAb6bf537d509119433250320ac0c640ccc115dfb1',
    'event': 'user',
    'timestamp': 1645850635.3806438,
    'metadata': {
        'dnis': '7112014981',
        'privacy_mode': True,
        'request_id': 'RQb6bf****************d****************ac0c****************ccc****************dfb1',
        'message_type': 'GRAMMAR',
        'error_type': 'no_match',
        'error_message': 'No Match',
        'reporting_error_type': 'no_match',
        'reporting_error_message': 'No Match',
        'no_match_input': '****',
        'grammar_input_mode': 'speech',
        'channel_id': '3',
        'original_text': '',
        'should_redact': True,
        'type': 'text',
        'error': True,
        'active_form': 'action_credit_card_collector',
        'requested_slot': 'cc_number',
        'template_name': 'utter_ask_cc_number',
        'asr_threshold': 0.0,
        'nlu_threshold': 0.63,
        'group': 'cc_number'
    },
    'text': '',
    'parse_data': {
        'intent': {
            'name': None,
            'confidence': 0.0
        },
        'entities': [],
        'text': '',
        'asrConfidence': 1,
        'recordingId': None,
        'missed_intent': False,
        'message_id': 'fc636e003e704bb3a3005177e170ef56',
        'metadata': {
            'dnis': '7112014981',
            'privacy_mode': True,
            'request_id': 'RQb6bf****************d****************ac0c****************ccc****************dfb1',
            'message_type': 'GRAMMAR',
            'error_type': 'no_match',
            'error_message': 'No Match',
            'reporting_error_type': 'no_match',
            'reporting_error_message': 'No Match',
            'no_match_input': '****',
            'grammar_input_mode': 'speech',
            'channel_id': '3',
            'original_text': '',
            'should_redact': True,
            'type': 'text',
            'error': True,
            'active_form': 'action_credit_card_collector',
            'requested_slot': 'cc_number',
            'template_name': 'utter_ask_cc_number',
            'asr_threshold': 0.0,
            'nlu_threshold': 0.63,
            'group': 'cc_number'
        }
    },
    'input_channel': 'OMNI_VOICE_00001',
    'message_id': 'fc636e003e704bb3a3005177e170ef56',
    'entities_redacted': [],
    'step_number': 686
}

def test_string_redaction():
    assert redactor.redact_string(msg_with_pci) == msg_without_pci

def test_string_redaction_spacing():
    msg = "1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1"
    msg_redacted = '****************'
    assert redactor.redact_string(msg) == msg_redacted


def test_string_redaction_strict():
    assert redactor.redact_string_strict(msg_with_pci) == msg_without_pci_strict

def test_string_redaction_spacing_strict():
    msg = "1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1"
    msg_redacted = '****************'
    assert redactor.redact_string_strict(msg) == msg_redacted

def test_redact_int_len_1():
    assert redactor.redact_int(1) == 1


def test_redact_int_len_1_strict():
    assert redactor.redact_int_strict(1) == 1


def test_redact_int_len_3_strict():
    assert redactor.redact_int_strict(100) == '***'


def test_redact_int_len_4_strict():
    assert redactor.redact_int_strict(1001) == '****'


def test_redact_int_len_6_strict():
    assert redactor.redact_int_strict(100123) == '******'


def test_redact_int_len_10_strict():
    assert redactor.redact_int(1234567890) == 1234567890


def test_redact_int_len_10():
    assert redactor.redact_int(1234567890) == 1234567890


def test_redact_int_len_11():
    assert redactor.redact_int(12345678901) == 12345678901


def test_redact_int_len_12():
    assert redactor.redact_int(123456789012) == 123456789012


def test_redact_int_len_13():
    assert redactor.redact_int(1234567890123) == '*************'


def test_redact_int_len_15():
    assert redactor.redact_int(123456789012345) == '***************'


def test_redact_int_len_16():
    assert redactor.redact_int(1234567890123456) == '****************'


def test_redact_int_len_19():
    assert redactor.redact_int(1234567890123456789) == '*******************'


def test_redact_float_not_int():
    assert redactor.redact_float(123456789012345.6) == 123456789012345.6


def test_redact_float_low_digit_count_int():
    assert redactor.redact_float(1234567890.0) == 1234567890.0


def test_redact_float_high_digit_count_int():
    assert redactor.redact_float(4761739001010010.0) == '****************'


def test_redact_list():
    assert redactor.redact_list(list_with_pci) == list_without_pci


def test_redact_entity_list_one_entry():
    assert redactor.redact_entity_list(entity_list_one_entry_with_pci) == entity_list_one_entry_without_pci


def test_redact_entity_list_many_entries():
    assert redactor.redact_entity_list(entity_list_many_entries_with_pci) == entity_list_many_entries_without_pci


def test_redact_dictionary():
    assert redactor.redact_dict(dict_with_pci) == dict_without_pci


def test_redact_event_no_pci():
    assert redactor.redact_event(event_no_pci) == event_no_pci


def test_redact_event_full_pci_redact():
    assert redactor.redact_event_complete(event_with_pci) == event_with_redacted_pci


def test_redact_event_general_redaction():
    assert redactor.redact_event(event_with_cc_num) == event_with_cc_num_redacted


def test_redact_event_general_redaction_2():
    assert redactor.redact_event(event_with_cc_num_2) == event_with_cc_num_2_redacted


def test_get_digit_length():
    assert get_count_digits(-99999999999999999999) == 20
    assert get_count_digits(-10000000000000000000) == 20
    assert get_count_digits(-9999999999999999999) == 19
    assert get_count_digits(-1000000000000000000) == 19
    assert get_count_digits(-999999999999999999) == 18
    assert get_count_digits(-100000000000000000) == 18
    assert get_count_digits(-99999999999999999) == 17
    assert get_count_digits(-10000000000000000) == 17
    assert get_count_digits(-9999999999999999) == 16
    assert get_count_digits(-1000000000000000) == 16
    assert get_count_digits(-999999999999999) == 15
    assert get_count_digits(-100000000000000) == 15
    assert get_count_digits(-99999999999999) == 14
    assert get_count_digits(-10000000000000) == 14
    assert get_count_digits(-9999999999999) == 13
    assert get_count_digits(-1000000000000) == 13
    assert get_count_digits(-999999999999) == 12
    assert get_count_digits(-100000000000) == 12
    assert get_count_digits(-99999999999) == 11
    assert get_count_digits(-10000000000) == 11
    assert get_count_digits(-9999999999) == 10
    assert get_count_digits(-1000000000) == 10
    assert get_count_digits(-999999999) == 9
    assert get_count_digits(-100000000) == 9
    assert get_count_digits(-99999999) == 8
    assert get_count_digits(-10000000) == 8
    assert get_count_digits(-9999999) == 7
    assert get_count_digits(-1000000) == 7
    assert get_count_digits(-999999) == 6
    assert get_count_digits(-100000) == 6
    assert get_count_digits(-99999) == 5
    assert get_count_digits(-10000) == 5
    assert get_count_digits(-9999) == 4
    assert get_count_digits(-1000) == 4
    assert get_count_digits(-999) == 3
    assert get_count_digits(-100) == 3
    assert get_count_digits(-99) == 2
    assert get_count_digits(-10) == 2
    assert get_count_digits(-9) == 1
    assert get_count_digits(-1) == 1
    assert get_count_digits(0) == 1
    assert get_count_digits(1) == 1
    assert get_count_digits(9) == 1
    assert get_count_digits(10) == 2
    assert get_count_digits(99) == 2
    assert get_count_digits(100) == 3
    assert get_count_digits(999) == 3
    assert get_count_digits(1000) == 4
    assert get_count_digits(9999) == 4
    assert get_count_digits(10000) == 5
    assert get_count_digits(99999) == 5
    assert get_count_digits(100000) == 6
    assert get_count_digits(999999) == 6
    assert get_count_digits(1000000) == 7
    assert get_count_digits(9999999) == 7
    assert get_count_digits(10000000) == 8
    assert get_count_digits(99999999) == 8
    assert get_count_digits(100000000) == 9
    assert get_count_digits(999999999) == 9
    assert get_count_digits(1000000000) == 10
    assert get_count_digits(9999999999) == 10
    assert get_count_digits(10000000000) == 11
    assert get_count_digits(99999999999) == 11
    assert get_count_digits(100000000000) == 12
    assert get_count_digits(999999999999) == 12
    assert get_count_digits(1000000000000) == 13
    assert get_count_digits(9999999999999) == 13
    assert get_count_digits(10000000000000) == 14
    assert get_count_digits(99999999999999) == 14
    assert get_count_digits(100000000000000) == 15
    assert get_count_digits(999999999999999) == 15
    assert get_count_digits(1000000000000000) == 16
    assert get_count_digits(9999999999999999) == 16
    assert get_count_digits(10000000000000000) == 17
    assert get_count_digits(99999999999999999) == 17
    assert get_count_digits(100000000000000000) == 18
    assert get_count_digits(999999999999999999) == 18
    assert get_count_digits(1000000000000000000) == 19
    assert get_count_digits(9999999999999999999) == 19
    assert get_count_digits(10000000000000000000) == 20
    assert get_count_digits(99999999999999999999) == 20



def test_spanish2english_noredaction():
    test_str = "esta es una oración en español muy larga sin dígitos numéricos. Este es un mensaje muy simple que no debe ser alterado de ninguna manera por nuestra lógica de redacción."
    assert test_str == spanish2english(test_str)


def test_spanish2english_no_redaction_contains_uno_but_not_standalone():
    test_str = "Esta es una oración que contiene una palabra que es un dígito pero no como una palabra independiente. Esa prueba es si vemos lo mismo que la entrada cuando no redactamos algunos"
    assert test_str == spanish2english(test_str)


def test_spanish2english_with_redactions():
    test_str = "uno dos tres quatro cinco seis siete ocho nueve cero"
    assert "one two three four five six seven eight nine zero" == spanish2english(test_str)


def test_spanish_event_with_cc():
    assert spanish_event_without_cc_number == redactor.redact_event(spanish_event_with_cc_number)

def test_spanish_event_with_partial_cc():
    assert spanish_event_without_cc_number_partial == redactor.redact_event_complete(spanish_event_with_cc_number_partial)

import re
from math import floor, log10
from text2digits import text2digits
import logging
t2d = text2digits.Text2Digits()
logger = logging.getLogger()  # get the root logger

spanish_digit_set = {"cero", "uno", "dos", "tres", "quatro", "cinco", "seis", "siete", "ocho", "nueve"}

spanish_to_english_digit_map = {"cero": "zero", "uno": "one", "dos": "two", "tres": "three", "quatro": "four",
                                "cinco": "five", "seis": "six", "siete": "seven", "ocho": "eight", "nueve": "nine"}


def spanish2english(message: str):
    message_words = message.split()
    if any(digit_string in message_words for digit_string in spanish_digit_set):
        redacted_message = ''
        for word in message_words:
            if word.lower() in spanish_digit_set:
                redacted_message += spanish_to_english_digit_map.get(word.lower()) + " "
            else:
                redacted_message += word + " "

        redacted_message = redacted_message.rstrip().lstrip()
        return redacted_message
    else:
        return message


# Disclaimer: only tested up to ints of digit length of 20. sys.maxlength is 19 digits on a 64 bit processor.
def get_count_digits(number: int):
    """Return number of digits in a number."""

    if number == 0:
        return 1

    number = abs(number)
    #  Because of floating point errors, numbers larger than 999999999999997 must be calculated in an iterable manner.
    if number <= 999999999999997:
        return floor(log10(number)) + 1

    count = 0
    while number:
        count += 1
        number //= 10
    return count


class Redactor:

    # used for general case redaction
    def redact_string(self, message: str):
        digit_msg = spanish2english(message)
        try:
            digit_msg = t2d.convert(digit_msg)
        except Exception:
            logger.info("text to digit conversion failed")

        formatted_msg = re.sub("(?<=\\d) +(?=\\d)", "", digit_msg)
        return re.sub(r"(?<!\d)(\d{12,})(?!\d)", '****************', formatted_msg)

    # used when message is marked as pci
    def redact_string_strict(self, record: str):
        digit_msg = spanish2english(record)
        try:
            digit_msg = t2d.convert(record)
        except Exception:
            logger.info("text to digit conversion failed")

        formatted_msg = re.sub("(?<=\\d) +(?=\\d)", "", digit_msg)
        return re.sub(r"(?<!\d)(\d{3}|\d{4}|\d{6}|\d{12,})(?!\d)", '****************', formatted_msg)

    def redact_string_complete(self, message):
        digit_msg = spanish2english(message)
        try:
            digit_msg = t2d.convert(digit_msg)
        except Exception:
            logger.info("text to digit conversion failed")
        formatted_msg = re.sub("(?<=\\d) +(?=\\d)", "", digit_msg)
        return self.redact_alphanum_sub(str(digit_msg))

    def redact_int(self, number: int):
        """ Turns all integers with more than 11 digits into '*' strings of the same digit length """
        num_len = get_count_digits(number)
        if num_len > 12:
            return ''.ljust(num_len, '*')  # a string of '*' chars as long as the number is
        else:
            return number

    def redact_int_strict(self, number: int):
        num_len = get_count_digits(number)
        if num_len > 11 or num_len in [3, 4, 6]:
            return ''.ljust(num_len, '*')  # a string of '*' chars as long as the number is
        else:
            return number

    def redact_float(self, number: float):
        if number.is_integer():
            val = self.redact_int(int(number))
            if isinstance(val, int):
                return float(val)
            else:
                return val
        else:
            return number

    def redact_float_strict(self, number: float):
        if number.is_integer():
            val = self.redact_int_strict(int(number))
            if isinstance(val, int):
                return float(val)
            else:
                return val
        else:
            return number

    def redact_list(self, collection: list):
        result = []
        for item in collection:
            result.append(self.redact_generic(item))
        return result

    def redact_entity_list(self, entities: list):
        result = []
        number_count = 0
        for entity in entities:
            entity_type = entity.get('entity')
            start = entity.get('start')
            end = entity.get('end')
            if 'number' == entity_type and isinstance(start, int) and isinstance(end, int):
                number_count += (end - start)
            result.append(self.redact_generic(entity))
        if number_count > 11:
            for entity in result:
                if isinstance(entity['value'], int):
                    entity['text'] = ''.ljust(get_count_digits(entity.get('value')), '*')
                    entity['value'] = ''.ljust(get_count_digits(entity.get('value')), '*')
                additional_value = entity.get('additional_info')
                if additional_value and isinstance(additional_value.get('value'), int):
                    entity['additional_info']['value'] = ''.ljust(get_count_digits(additional_value.get('value')), '*')

        return result

    def redact_entity_list_complete(self, entities: list):
        result = []
        for entity in entities:
            result.append(self.redact_entity_complete(entity))
        return result

    def redact_entity_complete(self, entity: dict):
        result = {}
        for key in entity.keys():
            if key == 'text':
                result[key] = '*'
            elif key == 'value':
                result[key] = '*'
            elif key == 'additional_info':
                result[key] = self.redact_entity_complete(entity[key])
            else:
                result[key] = self.redact_generic(entity[key])
        return result

    def redact_dict(self, table: dict):
        result = {}
        for key in table.keys():
            if key == self.redact_generic(key):
                if key == 'entities' or key == 'entities_redacted':
                    result[key] = self.redact_entity_list(table[key])
                elif key == 'timestamp':
                    # do nothing
                    result[key] = table[key]
                elif str(key).lower().endswith("id"):
                    # do nothing
                    result[key] = table[key]
                else:
                    result[key] = self.redact_generic(table[key])
        return result

    def redact_dict_complete(self, table: dict):
        result = {}
        for key in table.keys():
            if key == self.redact_generic(key):
                if key == 'entities':
                    result[key] = self.redact_entity_list_complete(table[key])
                elif key == 'timestamp':
                    # do nothing
                    result[key] = table[key]
                elif str(key).lower().endswith("id"):
                    # do nothing
                    result[key] = table[key]
                else:
                    result[key] = self.redact_generic(table[key])
        return result

    # Use in general case
    def redact_generic(self, message):
        if isinstance(message, str):
            return self.redact_string(message)
        elif isinstance(message, dict):
            return self.redact_dict(message)
        elif isinstance(message, list):
            return self.redact_list(message)
        elif isinstance(message, int):
            return self.redact_int(message)
        elif isinstance(message, float):
            return self.redact_float(message)
        elif isinstance(message, bool):
            return message
        elif message is None:
            return message
        else:
            return self.redact_string(str(message))

    # Use when message is not constrained, e.g. logging events
    def redact_generic_strict(self, message):
        if isinstance(message, str):
            return self.redact_string_strict(message)
        elif isinstance(message, dict):
            return self.redact_dict(message)
        elif isinstance(message, list):
            return self.redact_list(message)
        elif isinstance(message, int):
            return self.redact_int_strict(message)
        elif isinstance(message, float):
            return self.redact_float_strict(message)
        elif isinstance(message, bool):
            return message
        elif message is None:
            return message
        else:
            return self.redact_string(str(message))

    def redact_alphanum_sub(self, message):
        return re.sub("[0-9a-zA-Z]+", "****", str(message))

    def redact_partials_list(self, partials: list):
        result = []
        for partial in partials:
            result.append(self.redact_alphanum_sub(partial))
        return result

    def redact_metadata_complete(self, metadata: dict):
        result = {}
        for key in metadata.keys():
            if key == 'partials':
                result[key] = self.redact_partials_list(metadata[key])
            elif str(key) == 'original_text' or str(key) == 'no_match_input':
                result[key] = self.redact_string_complete(metadata[key])
            else:
                result[key] = self.redact_generic_strict(metadata[key])
        return result

    def redact_event(self, event: dict):
        result = {}
        for key in event.keys():
            if key == self.redact_generic(key):
                if key == 'entities_redacted':
                    result[key] = self.redact_entity_list(event[key])
                elif str(key).lower().endswith("id"):
                    # do nothing
                    result[key] = event[key]
                else:
                    result[key] = self.redact_generic(event[key])
        return result

    def redact_event_complete(self, event: dict):
        result = {}
        for key in event.keys():
            if key == self.redact_generic(key):
                if key == 'metadata':
                    result[key] = self.redact_metadata_complete(event[key])
                elif key == 'entities' or key == 'entities_redacted':
                    result[key] = self.redact_entity_list_complete(event[key])
                elif key == 'parse_data':
                    result[key] = self.redact_event_complete(event[key])
                elif str(key).find('text') != -1:
                    result[key] = self.redact_string_complete(event[key])
                elif str(key).lower().endswith("id"):
                    # do nothing
                    result[key] = event[key]
                else:
                    result[key] = self.redact_generic(event[key])
        return result
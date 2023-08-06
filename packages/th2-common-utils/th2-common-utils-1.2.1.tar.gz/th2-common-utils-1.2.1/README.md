# th2-common-utils-py (1.2.1)
Python library with useful functions for **developers and QA needs**.

## Installation
```
pip install th2-common-utils
```

## Usage
### 1. Message fields access 

The library provides a convenient way for Message fields access.

Instead of this:
```python
msg.fields['BO5Items'].list_value.values[0].message_value.fields['segment_instance_number'].message_value.fields['segment_number'].simple_value
```
You can do this:
```python
import th2_common_utils

msg['BO5Items'][0]['segment_instance_number']['segment_number']
```

### 2. Converters

* `message_to_dict(message)` - note, you will lose all metadata of the Message.
* `dict_to_message(fields, session_alias, message_type)` - where:
    * *fields* - required argument - message fields as a python dict;
    * *session_alias* and *message_type* - optional arguments - used to generate message metadata.
* `dict_to_root_message_filter(message_type, message_filter, metadata_filter, ignore_fields, check_repeating_group_order,
time_precision, decimal_precision)` - all arguments are optional.
* `message_to_typed_message(message, message_type)` - where:
    * *message* - Message object;
    * *message_type* - TypedMessage **class object**.
* `message_to_table(message)` - where:
    * *message* - Message object or dict.

To import functions above:
```python
from th2_common_utils import message_to_dict, dict_to_message # ...
```

### 3. Working with events

`th2-common-utils` provides methods to work with events:
* `create_event_body(component)` - creates event body from `component` as bytes.
* `create_event_id()` - creates EventID.
* `create_event(id, parent_id, start_timestamp, end_timestamp, status, name, 
type, body, attached_message_ids)` - creates event; all arguments are optional.
* `create_timestamp()` - creates `Timestamp` with current time.

To use functions above:
```python
from th2_common_utils import create_event, create_event_id

my_event = create_event(id=create_event_id(),
                        name='My event',
                        #... )
```

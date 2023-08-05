# Ruleau

A Python Rules Engine library

## Using the library

A username and password is required. This can be passed directly to the ApiAdapter (i.e. via the CLI) or these can
be set in the environment variables.

```text
RULEAU_USERNAME=myusername
RULEAU_PASSWORD=mypassword
```

```python
from ruleau import execute, rule, ApiAdapter, Process

# create a rule
@rule(rule_id="rul_1", name="Is adult")
def over_18(_, payload):
    return "age" in payload and payload["age"] >= 18

# create a payload (the answers to the rule's questions)
payload = {"age": 17}

# execute the rule against the payload
result = execute(over_18, payload, Process.create_process_from_rule(over_18))

# integrate with the backend web API with password and username in env
api_adapter = ApiAdapter(
    base_url="http://localhost:8000/"
)
# or pass directly to ApiAdapter:
api_adapter = ApiAdapter(
    base_url="http://localhost:8000/", username=myusername, password=mypassword
)

# sync the process
# Usually only needed once. For efficiency, it is advisable to keep these lines out of any loop.
process = Process.create_process_from_rule(over_18)
api_adapter.sync_process(process)

# send the results
result = execute(over_18, payload, process, api_adapter=api_adapter, case_id="ca_1280")
# result.result will be False due to applicant being 17

# if the rule for this case is overriden in the backend
# then running again will return True

```

### Organisational Data

Optionally a Process can be assigned as set of "tags" called Organisational Data which can be used
to filter or categorise rules and results.

Each Process must have these specified up front by setting the Organisational Scheme like so:

```python
api_adapter = ApiAdapter(
    base_url="http://localhost:8000",
)

org_scheme: List[OrganisationalScheme] = [
    OrganisationalScheme(
        id="location",  # ID Used to refer to the tag when organisational data is posted
        display_name="Location",  # Label used on the UI when being displayed
        display_default=True,  # If true, will appear on the UI by default, otherwise is hidden
        type="string",  # Either a `string`, `integer`, `float` or `date` type
    ),
    OrganisationalScheme(
        id="internal_id",  # ID Used to refer to the tag when organisational data is posted
        display_name="ID",  # Label used on the UI when being displayed
        display_default=True,  # If true, will appear on the UI by default, otherwise is hidden
        type="integer",  # Either a `string`, `integer`, `float` or `date` type
    )
]

api_adapter.publish_organisational_scheme(over_18, org_scheme)
```

Once set data can be provided when a ruleset is executed by updating the API Adapter using its
`with_organisational_data` method like so:

```python
api_adapter = ApiAdapter(
    base_url="http://localhost:8000/"
).with_organisational_data([
    {"key": "location", "value": "Bristol"},
    {"key": "internal_id", "value": 5}
])

process = Process.create_process_from_rule(over_18)
api_adapter.sync_process(process)

result = execute(over_18, payload, process, api_adapter=api_adapter, case_id="ca_1280")
```

Optionally we can also set the order by which Organisational Data appears on the UI by posting
to the UI Layout Metadata endpoint as in this example:

```python
ui_layout_metadata: UiLayoutMetadata = {
    # Defines the order the tags will appear on the cases page
    "case_org_data_order": [{"id": "internal_id"}, {"id": "location"}],
    # Defines the order the tags will appear on the overrides page
    "override_org_data_order": [{"id": "department"}],
    # See "Case Payload UI Specification" for details
    "data_payload_presentation": None,
}

api_adapter.publish_ui_layout_metadata(
    payload_has_patient_rule, ui_layout_metadata
)
```

### Case Payload UI Specification

In the Ruleau UI we display the case payload as it was executed for a case, and allow users to override the data
with values when said case is next reexecuted.

By default we work out the structure of case payload automatically to display it in the UI, this will perform basic
validation such as checking if the data override provided for a case matches the type in the original payload.

However you can use UI Layout Metadata to publish a JSON Schema specification that defines how case payloads for a
process should be displayed and validated, allowing for customisation of what overrides can be specified for the data.

In order to do this, please see the below example setting a JSON Schema for a case:

```python
ui_layout_metadata: UiLayoutMetadata = {
    # See "Organisational Data" for details
    "case_org_data_order": [],
    # See "Organisational Data" for details
    "override_org_data_order": [],
    # X
    "data_payload_presentation": {
        "type": "object",
        "properties": {
            "street_address": { "type": "string" },
            "city": { "type": "string" },
            "state": { "type": "string" }
        },
        "required": ["street_address", "city", "state"]
    },
}

api_adapter.publish_ui_layout_metadata(
    payload_has_patient_rule, ui_layout_metadata
)
```

The above example tells the UI a case payload for this process is expected to have 3 fields:

* street_address
* city
* state

All 3 of them are required text fields, and can be overridden on a case by case basis in the UI.

### JSON Schema Rules & Limitations

As a JSON Schema could define any shape of data, even one wildly different from the case payloads posted for a process,
we have to impose set of rules & limitations to ensure they are compatible with the payloads displayed on the UI.

1. On a case payload please always provide all the keys, even if null, rather than excluding the keys with no values
    * For example please use `{"a": null, "b": "abc"}` over `{"b": "abc"}` if `a` is optional
2. A custom JSON schema must only define one type for a given property
    * We don't support multiple types in a single field
        * Lists containing both strings and numbers aren't allowed
        * Nor are properties that can be either a string or number, for example
3. Everything in the custom JSON schema must be in the payload
    * No fields should exist in the schema that aren't on the payloads
    * For example if the schema specifies a field `a`, that field should be present in all case payloads, even if null
4. However not everything in the payload has to be in the JSON schema
    * For example the payload may have fields `a`, `b` and `c`, however you only wish field `b` to be editable
    * In that case, adding just the `b` field to the Schema means that is the only field the UI will allow data overrides for
5. If a custom JSON schema isn't defined, and a field is always `null` in a case, it won't be shown on the data overrides UI
    * This is as we are not able to generate a JSON schema from a `null` field (we cannot tell what type is required)
    * This can be resolved by using a custom JSON schema and specifying what the field should be when not `null`
    * In the example below the payload has a `null` `wind_sensor` field, by specifying it in the schema it can still be edited in the UI

Please see below for an example of a custom JSON schema and the expected case payload:

**Case Payload**

```json
{
  "case_id": "001",
  "temperature": 27,
  "wind_speed": 0.4,
  "humidity": 30,
  "cloud_cover": 20,
  "precipitation": 0,
  "last_checks": [],
  "pending_checks": [],
  "sensor_status": {
    "wind_sensor": null,
    "cloud_reader": null,
    "rain_indicator": null
  }
}
```

**JSON Schema**

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https:///www.unai.com/schemas/unit_test_schema.json",
  "type": "object",
  "properties": {
    "case_id": { "type": "string", "title": "Case Id" },
    "humidity": { "type": "number", "title": "Humidity" },
    "wind_speed": { "type": "number", "title": "Wind Speed" },
    "cloud_cover": { "type": "number", "title": "Cloud Cover" },
    "last_checks": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "date": { "type": "string", "title": "Date" },
          "checked_by": { "type": "string", "title": "Checked By" }
        },
        "required": [ "date", "checked_by" ]
      },
      "title": "Last Checks"
    },
    "temperature": { "type": "number", "title": "Temperature" },
    "precipitation": { "type": "number", "title": "Precipitation" },
    "sensor_status": {
      "type": "object",
      "properties": {
        "wind_sensor": { "type": "string", "title": "Wind Sensor" },
        "cloud_reader": { "type": "string", "title": "Cloud Reader" },
        "rain_indicator": { "type": "string", "title": "Rain Indicator" }
      },
      "title": "Sensor Status"
    },
    "pending_checks": {
      "type": "array",
      "items": {
        "type": "string"
      },
      "title": "Pending Checks"
    }
  }
}
```

### Testing Rules

Rules should be tested using [doctest](https://docs.python.org/3/library/doctest.html).

Example of these tests can be found in the [Kitchen Sink example](https://gitlab.com/unai-ltd/unai-decision/ruleau-core/-/tree/develop/examples/kitchen_sink/rules.py).

### Generating Documentation

Documentation for the rules can be generated using the `ruleau-docs` command.

The usage is as follows:
```
ruleau-docs [--output-dir=<argument>] filename
```

For example for a file of rules called `rules.py` run:
```
ruleau-docs rules.py
```

## Building & Testing the Library

### Pre-requisites

* [Python 3.9+](https://www.python.org/downloads/)

Package requirements installed by running:

```shell
pip install -r requirements-dev.txt
```

### Running the Tests

To run all unit tests in the project use the following command:

```shell
pytest
```

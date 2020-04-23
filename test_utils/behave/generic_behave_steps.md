# Generic Behave Steps: #

The generic steps that are available in the Behave framework for testing REST APIs

Author: Brian DeSimone  
Date: 05/03/2019

**NOTE:** This is a work in progress and more generic steps will be added over time as needed

<!-- toc -->

- [JSON Path](#json-path)
- [Generic Steps](#generic-steps)
  - [Headers](#headers)
  - [Memory and Variables](#memory-and-variables)
  - [Payload Generation](#payload-generation)
  - [Payload Modification](#payload-modification)
- [Generic Assert Steps](#generic-assert-steps)
  - [Header Validation](#header-validation)
  - [Schema Validation](#schema-validation)
  - [Collection Size Validation](#collection-size-validation)
- [Accessing Behave Context Variables](#accessing-behave-context-variables)
- [Examples](#examples)

<!-- tocstop -->

## JSON Path: ##

These generic steps use JSON path expressions to search for key/value pairs.
Please look [here](https://restfulapi.net/json-jsonpath/) for more on JSON path.

## Generic Steps: ##
The following steps are available to use when generating dynamic test data, sending REST requests, and asserting on those requests.

#### Headers ####

Steps to set header values one at a time or all at once in a table

```gherkin
Given request header ".*" is set to ".*"
Given request header ".*" is set to "none"
Given request header ".*" is set to "null"
Given request header ".*" is set to "empty string"

Given request headers:
  | header        | header_value     |
  | content-type  | application/json |
  | Accept        | application/json |
  | Authorization | Bearer <token>   |
```

#### Memory and Variables ####

**NOTE:** The following steps use JSON path to evaluate the \<key>  

Step to save a JSON response key/value pair to the Behave Context as ```ctx.{value_name}```

```gherkin
And the JSON response at "<key>" is saved as "<value_name>"
```

Step to save a string to the behave context as ```ctx.{value_name}```

```gherkin
Given the value "<value>" is saved as "<value_name>"
```

Step to print the value saved at ```ctx.context_attribute``` for debugging purposes

```gherkin
Given the context value at "<context_attribute>" is printed
```

Step to save a JSON request payload key/value pair to the Behave Context as ```ctx.{value_name}```

```gherkin
Given the JSON payload at "<key>" is saved as "<value_name>"
```

Step to save a JSON response position of a key value pair. This is useful if you have multiple items in a collection that you want assert against.

```gherkin
And the position where "<key>" is "<value>" is saved from the JSON response at "<json_key>"
```

#### Payload Generation ####

Step to create your own JSON payload that is saved to the Behave context as ```ctx.request_data```

```gherkin
Given the following JSON payload:
  | attribute        | value  |
  | first_attribute  | value1 |
  | second_attribute | value2 |
```

The payload that is created and saved to ```ctx.request_data``` looks like this:

```json
{
  "first_attribute": "value1",
  "second_attribute": "value2"
}
```

Step to create your own JSON payload that is saved to the Behave content as ```ctx.<value_name>```

```gherkin
Given the following JSON payload saved as "<value_name>":
  | attribute        | value  |
  | first_attribute  | value1 |
  | second_attribute | value2 |
```

The payload that is created and saved to ```ctx.<value_name>``` looks like this:

```json
{
  "first_attribute": "value1",
  "second_attribute": "value2"
}
```

#### Payload Modification ####

The following steps use JSON path to evaluate the \<target_key>. JSON path allows for modifying nested keys in this step.

Step to modify a payload key/value pair that is saved on the behave context at ```ctx.request_data```

```gherkin
Given the JSON request payload at "<target_key>" is modified to be "<intended_value>"
Given the JSON request payload at "<target_key>" is modified to be "none"
Given the JSON request payload at "<target_key>" is modified to be "null"
Given the JSON request payload at "<target_key>" is modified to be "empty"
Given the JSON request payload at "<target_key>" is modified to be "empty string"
```

## Generic Assert Steps ##

#### Header Validation ####

Steps to validate REST response content type headers

```gherkin
Then the response content header should be json|JSON
Then the response content header should not be json|JSON
```

Steps to validate REST response headers

```gherkin
Then the response headers should be the following:
  | header_name  | header_value     |
  | content-type | application/json |
  | Accept       | application/json |

Then the response headers should not be the following:
  | header_name  | header_value     |
  | content-type | application/json |
  | Accept       | application/json |
```

Steps to validate REST response content (good for 204 no-content validations)

```gherkin
Then the json|JSON response should have no content
Then the json|JSON response should have content
```

#### Schema Validation ####

Steps to validate REST JSON responses contain keys.  

The following steps use JSON path to evaluate the \<key>

```gherkin
Then the JSON response should include "<key>"
Then the JSON response should not include "<key>"

Then the JSON response should include the following:
  | attribute               |
  | a_key                   |
  | first_key.nested_key    |
  | a_list[0].nested_key |

Then the JSON response should not include the following:  
  | attribute               |
  | a_key                   |
  | first_key.nested_key    |
  | a_list[0].nested_key |
```

Steps to validate REST JSON responses contain a specific data type at a key

The following steps use JSON path to evaluate the \<key>

The \<data_type> is the python data type and it follows python syntax

```gherkin
Then the JSON response at "<key>" should have data type <data_type>
Then the JSON response at "<key>" should not have data type <data_type>

Then the JSON response should have the following data types:
  | attribute               | data_type |
  | a_key                   | str       |
  | first_key               | dict      |
  | first_key.nested_key    | int       |
  | a_list[0].nested_key    | list      |

Then the JSON response should not have the following data types:
  | attribute               | data_type |
  | a_key                   | str       |
  | first_key               | dict      |
  | first_key.nested_key    | int       |
  | a_list[0].nested_key    | list      |
```

Steps to validate REST JSON responses have a key/value pair as expected

The following steps use JSON path to evaluate the \<key>

The \<value> can be anything or evaluated with ```ctx.<value>``` by using \<{value}>

```gherkin
Then the JSON response at "<key>" should be "<value>"
Then the JSON response at "<key>" should not be "<value>"

Then the JSON response should be the following:
  | attribute               | value       |
  | a_key                   | some_string |
  | first_key.nested_key    | some_int    |
  | a_list[0].nested_key    | {ctx.value} |

Then the JSON response should not be the following:
  | attribute               | value       |
  | a_key                   | some_string |
  | first_key.nested_key    | some_int    |
  | a_list[0].nested_key    | {ctx.value} |
```

#### Collection Size Validation ####

Steps to validate REST JSON responses that have a collection (dict or list) in the payload are a certain size

The following steps use JSON path to evaluate the \<key>

\<entries> can be replaced by anything... if you list is a list of apps then you can use "apps" here. It is arbitrary

```gherkin
Then the JSON response at "<key>" should have <size_int> <entries>
Then the JSON response at "<key>" should not have <size_int> <entries>
```

## Accessing Behave Context Variables: ##

From any generic Behave step that reads in values, you can have that value interpolated by the context for variables that are stored.
This means that if you use {some_string} we will search the context for ```ctx.some_string``` and replace that with the value of what is stored on the context.

This can be done in any of the above generic steps.

## Examples: ##
[Create App Feature](https://github.com/NarrativeScience/talos/blob/master/tests-integration/features/status_code_tests/api_config_server/create_app.feature)
[Get App Feature](https://github.com/NarrativeScience/talos/blob/master/tests-integration/features/status_code_tests/api_config_server/get_app.feature)

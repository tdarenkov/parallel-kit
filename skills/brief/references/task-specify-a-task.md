
# Task Spec

> Define structured research tasks with customizable input and output schemas. 

## Task Spec

A Task Specification ([Task Spec](https://docs.parallel.ai/api-reference/tasks/create-task-run.md#body-task-spec-output-schema)) is a declarative template that defines the structure and requirements for the outputs of a web research operation. While optional in each Task Run, Task Specs provide significant advantages when you need precise control over your research data.

Task Specs ensure consistent results by enforcing a specific output structure across multiple runs. They validate schema against expected formats and create reusable templates for common research patterns. By defining the expected outputs clearly, they also serve as self-documentation for your tasks, making them easier to understand and maintain.

| Component | Required | Purpose | Format |
| - | - | - | - |
| **Output Schema** | Yes | Defines the structure and fields of the task result | JSON Schema or Text |
| **Input Schema** | No | Specifies expected input parameters and their formats | JSON Schema or Text |

## Task Spec Structure

A Task Spec consists of:

| Field | Type | Required | Description |
| - | - | - | - |
| `output_schema` | Schema object or string | Yes | Description and structure of the desired output |
| `input_schema` | Schema object or string | No | Description and structure of input parameters |

> [!NOTE]
>
> When providing a bare string for `input_schema` or `output_schema`, it's equivalent to a text schema with that string as the description.

## Schema Types

Task Spec supports three schema formats:

> [!TIP]
>
> When using the [Python SDK](https://pypi.org/project/parallel-web/), Parallel Tasks also support Pydantic objects in Task Spec

> [!NOTE]
>
> `auto` mode enables Deep Research style outputs only in processors `pro` and above. Read more about Deep Research [here](https://docs.parallel.ai/task-api/examples/task-deep-research.md).

> [tab] JSON Schema
>
> ```json theme={"system"}
> {
>   "json_schema": {
>     "type": "object",
>     "properties": {
>       "population": {
>         "type": "string",
>         "description": "Current population with year of estimate"
>       },
>       "area": {
>         "type": "string",
>         "description": "Total area in square kilometers and square miles"
>       }
>     },
>     "required": ["population", "area"]
>   },
>   "type": "json"
> }
> ```

> [tab] Text Schema
>
> ```json theme={"system"}
> {
>   "description": "Summary of the country's economic indicators for 2023",
>   "type": "text"
> }
> ```

> [tab] Auto Schema
>
> ```json theme={"system"}
> {
>   "type": "auto"
> }
> ```

> [!NOTE]
>
> See [Best Practices](https://docs.parallel.ai/task-api/best-practices.md) for guidance on writing effective Task Specs.

## Output Schema Validation Rules

The Task API enforces several restrictions on output schemas to ensure compatibility and performance:

### Schema Structure Rules

| Rule | Type | Description |
| - | - | - |
| Root type must be object | error | The root schema must have `"type": "object"` |
| Root must have properties | error | The root object must have a `properties` field |
| Root cannot use anyOf | error | The root level cannot use `anyOf` |
| Standalone null type | error | `null` type is only allowed in union types or anyOf |
| All fields must be required | warning | All properties should be listed in the `required` array |
| additionalProperties must be false | warning | All object types should set `additionalProperties: false` |

> [!NOTE]
>
> While all fields must be required in the schema, you can create optional parameters by using a union type with `null`. For example, `"type": ["string", "null"]` allows a field to be either a string or null, effectively making it optional while maintaining schema compliance.

### Size and Complexity Limits

> [!WARNING]
>
> **25,000 character limit:** The combined length of your task specification AND input data cannot exceed 25,000 characters. This includes:
>
> * All field names and descriptions in your schemas
> * The `objective` or `description` text
> * Your input data (the entity you're researching)
>
> If you hit this limit, simplify your schema descriptions or reduce input size. For large input data, consider splitting into multiple tasks.

| Rule | Type | Limit | Description |
| - | - | - | - |
| Nesting depth | error | 5 levels | Maximum nesting depth of objects and arrays |
| Total properties | error | 100 | Maximum total number of properties across all levels |
| Total string length | error | 25,000 chars | Maximum total string length for names and values |
| Enum values | error | 500 | Maximum number of enum values across all properties |
| Large enum string length | error | 7,500 chars | Maximum string length for enums with >250 values |
| Task spec size | error | 15,000 chars | Maximum length of the task specification alone |
| **Total size** | error | **25,000 chars** | **Maximum combined length of task specification + input data** |

### Unsupported Keywords

The following JSON Schema keywords are not supported in output schemas:

`contains`, `format`, `maxContains`, `maxItems`, `maxLength`, `maxProperties`, `maximum`, `minContains`, `minItems`, `minLength`, `minimum`, `minProperties`, `multipleOf`, `pattern`, `patternProperties`, `propertyNames`, `uniqueItems`, `unevaluatedItems`, `unevaluatedProperties`

irements: it has an object root type with properties, all fields are required, and `additionalProperties` is set to false.

### Common Schema Errors to Avoid

Here are examples of common schema errors and how to fix them:

> [tab] Root Type Error
>
> ```json theme={"system"}
> {
>   "type": "array",  // Error: Root type must be "object"
>   "items": {
>     "type": "object",
>     "properties": {
>       "name": { "type": "string" }
>     }
>   }
> }
> ```
>
> **Fix:** Change the root type to "object" and move array properties to a field:
>
> ```json theme={"system"}
> {
>   "type": "object",
>   "properties": {
>     "items": {
>       "type": "array",
>       "items": {
>         "type": "object",
>         "properties": {
>           "name": { "type": "string" }
>         },
>         "required": ["name"]
>       }
>     }
>   },
>   "required": ["items"],
>   "additionalProperties": false
> }
> ```

> [tab] AnyOf Error
>
> ```json theme={"system"}
> {
>   "type": "object",
>   "anyOf": [  // Error: Root level cannot use anyOf
>     {
>       "properties": {
>         "field1": { "type": "string" }
>       }
>     },
>     {
>       "properties": {
>         "field2": { "type": "string" }
>       }
>     }
>   ]
> }
> ```
>
> **Fix:** Combine the properties into a single object:
>
> ```json theme={"system"}
> {
>   "type": "object",
>   "properties": {
>     "field1": { "type": "string" },
>     "field2": { "type": "string" }
>   },
>   "required": ["field1", "field2"],
>   "additionalProperties": false
> }
> ```

> [tab] Missing Required
>
> ```json theme={"system"}
> {
>   "type": "object",
>   "properties": {
>     "field1": { "type": "string" },
>     "field2": { "type": "string" }
>   },
>   "required": ["field1"]  // Warning: All fields should be required
> }
> ```
>
> **Fix:** Add all fields to the required array:
>
> ```json theme={"system"}
> {
>   "type": "object",
>   "properties": {
>     "field1": { "type": "string" },
>     "field2": { "type": "string" }
>   },
>   "required": ["field1", "field2"],
>   "additionalProperties": false
> }
> ```

> [tab] Additional Properties
>
> ```json theme={"system"}
> {
>   "type": "object",
>   "properties": {
>     "field1": { "type": "string" },
>     "field2": { "type": "string" }
>   },
>   "required": ["field1", "field2"],
>   "additionalProperties": true  // Warning: should be false
> }
> ```
>
> **Fix:** Set additionalProperties to false:
>
> ```json theme={"system"}
> {
>   "type": "object",
>   "properties": {
>     "field1": { "type": "string" },
>     "field2": { "type": "string" }
>   },
>   "required": ["field1", "field2"],
>   "additionalProperties": false
> }
> ```

> [tab] Unsupported Keywords
>
> ```json theme={"system"}
> {
>   "type": "object",
>   "properties": {
>     "field1": {
>       "type": "string",
>       "minLength": 5  // Error: Unsupported keyword
>     }
>   },
>   "required": ["field1"],
>   "additionalProperties": false
> }
> ```
>
> **Fix:** Remove unsupported keywords and use descriptions instead:
>
> ```json theme={"system"}
> {
>   "type": "object",
>   "properties": {
>     "field1": {
>       "type": "string",
>       "description": "A string with at least 5 characters"
>     }
>   },
>   "required": ["field1"],
>   "additionalProperties": false
> }
> ```

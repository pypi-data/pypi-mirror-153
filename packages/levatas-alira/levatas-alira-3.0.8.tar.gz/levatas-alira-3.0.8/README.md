# Alira Platform

## Table of Contents

-   [Running a pipeline](#running-a-pipeline)
-   [Instances](#instances)
-   [Modules](#modules)
    -   [Rest module](#rest-module)
    -   [Map module](#map-module)
    -   [Selection module](#selection-module)
    -   [Flagging module](#flagging-module)
    -   [Email module](#email-module)
    -   [S3 module](#s3-module)
    -   [Twilio module](#twilio-module)
    -   [SocketIO module](#socketio-module)
-   [Implementing custom code](#implementing-custom-code)
-   [Running the test suite](#running-the-test-suite)
-   [What's New](WHATSNEW.md)

## Running a pipeline

To run a pipeline, you can use the `alira.Pipeline` class. Here is an example of how to initialize it and run it:

```python
from alira import Pipeline

pipeline = Pipeline(
    configuration_directory="/path/to/model/folder",
    redis_server="redis://redis:6379/"
)
pipeline.run({
    "prediction": 1,
    "confidence": 0.85,
    "files": ["image1.jpg"],
    "metadata": {
        "sample": 123
    }
})
```

The `Pipeline` constructor receives the following arguments:

-   `configuration_directory`: The directory containing the pipeline configuration file. If `pipeline_configuration` is not specified, the `Pipeline` class will try to load the configuration from a file named `pipeline.yml` in this directory.
-   `pipeline_configuration`: The path to the pipeline configuration file or a stream containing the configuration. This attribute is optional and mostly used for testing purposes. It's also useful in case you want to use a different configuration file than the one inside `configuration_directory`.
-   `redis_server`: The URL of the Redis server.

The `pipeline.run()` function returns the instance object created by the pipeline. Keep in mind that pipeline modules run asynchronously, so the returned instance will not contain any modifications made by the pipeline modules.

## Instances

An instance is an individual request sent through a pipeline. Instances are automatically created from the JSON object used when running the pipeline.

An instance is an object of the class `alira.instance.Instance` and has the following attributes:

-   `id`: A unique identifier associated to the instance.
-   `prediction`: `1` if the prediction is positive, `0` if negative.
-   `confidence`: A float between 0 and 1 indicating the confidence on the prediction.
-   `files`: A list of files associated with this instance.
-   `metadata`: A dictionary of metadata attributes associated with this instance. This property is initialized using all of the attributes in the JSON object used when running the pipeline.
-   `properties`: A dictionary of properties contributed by each module of the pipeline.

To get a specific attribute of an instance, use the `get_attribute()` method with the path to access the attribute. For example, to get the value of an attribute named `sample` that's part of the metadata of an instance, use `instance.get_attribute("metadata.sample")`. This method will raise an exception if the attribute does not exist. If you want to use a default value in case the attribute doesn't exist, use `instance.get_attribute("metadata.sample", default=0)`.

Internally, `get_attribute()` uses JMESPath to access attributes in the instance. For more information, check [JMESPath's specification](https://jmespath.org/specification.html).

You can create an instance directly from a JSON object using the `Instance.create()` static method. This method looks for top-level attributes that match the instance's properties. Everthing else that don't match will be automatically added as part of the `metadata` attribute. For example:

```python
instance = Instance.create({
    "prediction": 1,
    "confidence": 0.85,
    "files": ["image1.jpg"],
    "sample": 123,
    "hello": {
        "company": "levatas"
    },
    "metadata": {
        "value2": 234
    }
})
```

The above instance will end-up with the following attributes:

-   `instance.prediction = 1`
-   `instance.confidence = 0.85`
-   `instance.files = [image1.jpg]`
-   `instance.metadata = { "sample": 123, "hello": { "company": "levatas" }, "value2": 234 }`

## Modules

### Rest module

You can use the Rest module to send every instance processed by the pipeline to a remote endpoint.

Here is an example:

```yaml
name: thermal

dependencies:
    - module: alira.modules.RestAuthentication
      service: http://192.168.0.1:4200/
      username: levatas
      password: password

pipeline:
    - module: alira.modules.Rest
      files_directory: images
      files: files
      upload_files: true
```

The connect to the endpoint exposed by the Rest module, we need to authenticate our pipeline and use an access token for every subsequent request. This is the responsibility of the `RestAuthentication` module specified under the `dependencies` section.

When configuring the `RestAuthentication` module, you need to specify the following attributes:

-   `service`: The base URL of the endpoint. If not specified, the module will try to use the `ALIRA_REST_SERVICE` environment variable.
-   `username`: The username to authenticate with the Rest service. If not specified, the module will try to use the `ALIRA_REST_USERNAME` environment variable.
-   `password`: The password to authenticate with the Rest service. If not specified, the module will try to use the `ALIRA_REST_PASSWORD` environment variable.

The second component is the `Rest` module specified as one of the steps in the pipeline. Here is the list of supported attributes:

-   `files_directory`: The directory where the files associated to an instance are currently stored. If not specified, the module will default to a `files` folder inside the model directory.
-   `files`: The name of the attribute on every instance containing the list of files associated with it. If not specified, the module will use the `files` attribute.
-   `upload_files`: A boolean value indicating whether the files should be uploaded to the Rest endpoint. If this attribute is not specified, its default value is `true`.

Keep in mind that the Rest module supports up to 50MB of data per request. This limitation affects the size of the files that can be uploaded.

### Map module

You can use the Map module to apply a given function to every instance processed by the pipeline.

A simple way to implement and reference a function is by using a `pipeline.py` file in the same directory as the configuration file. You can find more information about this under [Implementing custom code](#implementing-custom-code).

Here is an example:

```yaml
name: thermal

pipeline:
    - module: alira.modules.Map
      function: thermal.pipeline.map
```

The `Map` module defined above expects a function with the following signature:

```python
def map(instance) -> dict:
    return {
        "hello": "world"
    }
```

The properties returned by the function will be automatically added to the instance as part of its `properties` dictionary under a key with the same name as the function. For example, the above setup will add a `map` key to the instance's `properties` dictionary containing the result of the function. However, if you specify the `module_id` attribute, the result of the function will be added under a key with the same name as `module_id`. For example, the following configuration will add the result of the `map()` function under `instance.properties["sample"]`.

```yaml
name: thermal

pipeline:
    - module: alira.modules.Map
      module_id: sample
      function: thermal.pipeline.map
```

### Selection module

You can use the Selection module to select a percentage of instances as they go through the pipeline and flag them for human review. Having a group of instances reviewed by humans gives the model a baseline understanding of its performance, and allows it to compute metrics that can later be extrapolated to all processed instances.

```yaml
name: thermal

pipeline:
    - module: alira.modules.Selection
      percentage: 0.2
```

The above example will extend `instance.properties` with a new `selected` attribute under the `selection` key. The value of this attribute will be `1` if the instance has been selected for review, and `0` otherwise.

### Flagging module

You can use the Flagging module to optimize the decision of routing instances for human review.

There are two implementations of the Flagging module:

-   `alira.modules.Flagging`
-   `alira.modules.CostSensitiveFlagging`

#### `alira.modules.Flagging`

This implementation optimizes the decision of routing instances to a human using a threshold. Any instance with a confidence below the threshold will be sent for human review.

```yaml
name: thermal

pipeline:
    - module: alira.modules.Flagging
      threshold: 0.7
```

This module will extend `instance.properties` with a new `flagging` key containing the attribute `flagged`. This attribute indicates whether the instance has been flagged for human review. This attribute is `1` if the instance has been flagged for review, and `0` otherwise.

#### `alira.modules.CostSensitiveFlagging`

This implementation uses cost sensitivity criteria to reduce the cost of mistakes.

```yaml
name: thermal

pipeline:
    - module: alira.modules.CostSensitiveFlagging
      fp_cost: 100
      fn_cost: 1000
      human_review_cost: 10
```

When configuring the module, you can specify the following attributes:

-   `fp_cost` (`float`): The cost of a false positive prediction. This attribute is optional and when not specified the module will assume the cost is `0`.
-   `fn_cost` (`float`): The cost of a false negative prediction. This attribute is optional and when not specified the module will assume the cost is `0`.
-   `human_review_cost` (`float`): The cost sending this instance for human review. This attribute is optional and when not specified the module will assume the cost is `0`.

This module will extend `instance.properties` with a new `flagging` key containing the following attributes:

-   `flagged`: Whether the instance has been flagged for human review. This attribute is `1` if the instance has been flagged for review, and `0` otherwise.
-   `cost_prediction_positive`: The cost associated with a positive prediction.
-   `cost_prediction_negative`: The cost associated with a negative prediction.

### Email module

You can use the Email module to send email notifications to a list of email addresses. This module works directly with an SMTP server to relay emails or uses the Rest service to send emails from a centralized location.

```yaml
name: thermal

pipeline:
    - module: alira.modules.Email
      filtering: alira.instance.onlyPositiveInstances
      sender: spot@levatas.com
      recipients:
          - user1@levatas.com
          - user2@levatas.com
      subject: Random subject
      template_filename: template.html
      files: files
      files_directory: files
      relay: smtp
```

Here is an example `template.html` file:

```html
<!DOCTYPE html>
<html>
    <body>
        <span>prediction:</span>
        <span>[[prediction]]</span>
        <span>confidence:</span>
        <span>[[confidence]]</span>
        <img src="[[properties.image_file]]" />
    </body>
</html>
```

When configuring the module, you can specify the following attributes:

-   `filtering`: An optional function that will be used to filter the instance and decide whether the module should process it. If this function is not specified, the instance will be processed. For convenience purposes, there are two predefined functions that you can use:
    -   `alira.instance.onlyPositiveInstances`: Only positive instances will be considered.
    -   `alira.instance.onlyNegativeInstances`: Only negative instances will be considered.
-   `sender`: The email address where the notification will come from.
-   `recipients`: The list of email addresses that will receive the notification.
-   `subject`: The subject of the email notification.
-   `template_filename`: The name of the HTML template file that will be used to construct the email notification. This file should be located in the same directory as the pipeline configuration file.
-   `files`: The instance's field that will be used to extract the list of files that will be send as attachments in the email notification. This attribute is optional and when not specified the module will use `instance.files`.
-   `files_directory`: The directory where the files associated to an instance are currently stored. If not specified, the module will default to a `files` folder inside the model directory.
-   `relay`: The relay mechanism used by this module to send email notifications. This attribute is optional and when not specified the module will use `smtp`. The following values are supported:
    -   `smtp`: Email notifications will be sent using an SMTP server. For this mechanism to work, make sure that the SMTP configuration is properly set using the appropriate environment variables as specified below.
    -   `rest`: Email notifications will be relayed using the Rest service. For this mechanism to work, the Rest module must be configured before the Email module.

If using `relay: smtp`, the module will look for the SMTP server configuration in the following environment variables:

- `ALIRA_SMTP_HOST`: The SMTP server hostname. For example, use `smtp-relay.gmail.com` to send emails using Gmail's SMTP server.
- `ALIRA_SMTP_PORT`: The SMTP server port. For example, use `465` to send emails using Gmail's SMTP server.
- `ALIRA_SMTP_USERNAME`: The SMTP server username. For example, use `spot@levatas.com` to send emails from the default Levatas' email address.
- `ALIRA_SMTP_PASSWORD`: The SMTP server password. 

The Email module extends the instance with a dictionary under `properties.email` containing the following attributes:

-   `status`: The status of the operation. It's either `SUCCESS`, `FAILURE`, or `SKIPPED`. The latter happens whenever the instance has been filtered out by the function specified as the `filtering` attribute.
-   `message`: An optional message with more information about the status of the module execution.

### S3 module

You can use the S3 module to upload the files associated with an instance to an S3 location.

```yaml
name: thermal

pipeline:
    - module: alira.modules.S3
      filtering: alira.instance.onlyPositiveInstances
      autogenerate_name: true
      bucket: sample-bucket
      key_prefix: files
      public: true
      files: files
      files_directory: files
```

When configuring the module, you can specify the following attributes:

-   `module_id`: An optional identifier for this module. This identifier is used to construct the dictionary key that will be added to `instance.properties`. If `module_id` is not specified, the dictionary key will be `s3`.
-   `filtering`: An optional function that will be used to filter the instance and decide whether the module should process it. If this function is not specified, the instance will be processed. For convenience purposes, there are two predefined functions that you can use:
    -   `alira.instance.onlyPositiveInstances`: Only positive instances will be considered.
    -   `alira.instance.onlyNegativeInstances`: Only negative instances will be considered.
-   `bucket`: The S3 bucket where the files will be stored.
-   `key_prefix`: The key prefix that will be used when storing the files in the S3 bucket.
-   `public`: Whether the uploaded files should be publicly accessible.
-   `autogenerate_name`: If this attribute is `true`, the module will generate a unique name for each uploaded file. If this attribute is `false`, the module will use the original file's name. By default, this attribute is `false`.
-   `files`: The instance's field that will be used to extract the list of files that will be uploaded to S3. This attribute is optional and when not specified the module will use `instance.files`.
-   `files_directory`: The directory where the files associated to an instance are currently stored. If not specified, the module will default to a `/files` folder inside the model directory.

This module extends the instance with a dictionary under `properties.s3` containing the following attributes (if the attribute `module_id` is specified, the dictionary key will have that name):

-   `status`: The status of the operation. It's either `SUCCESS`, `FAILURE`, or `SKIPPED`. The latter happens whenever the instance has been filtered out by the function specified as the `filtering` attribute.
-   `message`: An optional message with more information about the status of the module execution.
-   `files`: A list of URLs pointing to the files.

### Twilio module

You can use the Twilio module to send text message notifications to a list of phone numbers.

```yaml
name: thermal

pipeline:
    - module: alira.modules.Twilio
      filtering: alira.instance.onlyPositiveInstances
      sender: +11234567890
      recipients:
          - +11234567890
          - +11234567891
      template_filename: template.txt
      media: properties.s3.files[0]
```

Here is an example `template.txt` file:

```txt
prediction: [[prediction]]
confidence: [[confidence]]
metadata_attribute: [[metadata.attr1]]
```

When configuring the module, you can specify the following attributes:

-   `filtering`: An optional function that will be used to filter the instance and decide whether the module should process it. If this function is not specified, the instance will be processed. For convenience purposes, there are two predefined functions that you can use:
    -   `alira.instance.onlyPositiveInstances`: Only positive instances will be considered.
    -   `alira.instance.onlyNegativeInstances`: Only negative instances will be considered.
-   `sender`: The phone number where the notifications will come from.
-   `recipients`: The list of phone numbers that will receive the notification.
-   `template_filename`: The name of the text template file that will be used to construct the notification. This file should be located in the same directory as the pipeline configuration file.
-   `media`: Specifies the instance's attribute containing the URL of the file that will be sent as part of the notification.

This module extends the instance with a dictionary under `properties.twilio` containing the following attributes:

-   `status`: The status of the operation. It's either `SUCCESS`, `FAILURE`, or `SKIPPED`. The latter happens whenever the instance has been filtered out by the function specified as the `filtering` attribute.
-   `message`: An optional message with more information about the status of the module execution.

### SocketIO module

You can use the SocketIO module to send real-time notifications to a socketio endpoint. For example, this module can be used to display real-time predictions on a web interface.

```yaml
name: thermal

pipeline:
    - module: alira.modules.SocketIO
      endpoint: http://192.168.0.32:5003
```

When configuring the module, you can specify the following attributes:

-   `endpoint`: The URL of the socketio endpoint that will receive the notification.

## Implementing custom code

Several modules require a function to do some sort of processing. For example, the [Map module](#map-module) requires a function that will be called to extend the supplied instance.

You can implement your own custom function by including a `pipeline.py` file in the same directory where the `pipeline.yml` file is located. The pipeline will automatically load this file and make every function in it available under the following namespace: `{pipeline name}.pipeline.{function name}`.

For example, look at the following `pipeline.py` file:

```python
def sample_function(instance: Instance) -> dict:
    return {
        "hello": "world"
    }
```

You can reference `sample_function()` from your `pipeline.yml` as follows:

```yaml
name: thermal

pipeline:
    - module: alira.modules.Map
      function: thermal.pipeline.sample_function
```

This is the breakdown of the `function` attribute:

-   `thermal`: The name of the pipeline.
-   `pipeline`: This is an arbitrary section indicating that this code is part of the `pipeline.py` file.
-   `sample_function`: The name of the function that will be called (this function should exist in the `pipeline.py` file.)

## Running the test suite

To run the test suite, you can follow the instructions below:

1. Create a `.env` file in the root of the project. (See below for the contents of the file.)
2. Create and activate a virtual environment
3. Install the requirements from the `requirements.txt` file
4. Run the unit tests using the `pytest` command.

```shell
$ python3 -m venv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
$ pytest -s
```

Here is an example of the `.env` file:

```
ALIRA_AWS_ACCESS_KEY_ID=[your access key]
ALIRA_AWS_SECRET_ACCESS_KEY=[your secret key]
ALIRA_AWS_REGION_NAME=[your region name]

ALIRA_TWILIO_ACCOUNT_SID=[Twilio account sid]
ALIRA_TWILIO_AUTH_TOKEN=[Twilio auth token]

ALIRA_REST_SERVICE=[the base URL of the Alira Rest service]
ALIRA_REST_USERNAME=[the username of the Alira Rest customer]
ALIRA_REST_PASSWORD=[the password of the Alira Rest customer]

ALIRA_SMTP_HOST=smtp-relay.gmail.com
ALIRA_SMTP_PORT=465
ALIRA_SMTP_USERNAME=spot@levatas.com
ALIRA_SMTP_PASSWORD=[application password]

TEST_EMAIL_MODULE_RECIPIENT=[your email address]
TEST_TWILIO_MODULE_SENDER=[your phone number]
TEST_TWILIO_MODULE_RECIPIENT=[your phone number]
```

### Integration tests

Some of the tests require Redis and the Alira Rest service to be running. To run these tests, you can follow the instructions below.

First, run a Redis server by downloading and starting a Redis container:

```shell
$ docker pull redis:6.2.5
$ docker container run -it --name redis -p 6379:6379 --rm redis:6.2.5
```

The test suite uses a queue named `tests`, so we need to run a Redis worker listening on this queue:

```shell
$ rq worker --with-scheduler --logging_level=INFO tests
```

Then, run the Alira Rest service by following the instructions on that project.

With Redis, the worker, and Alira Rest running, you can run the tests:

```shell
$ pytest -s -m redis
```

To run the integration tests, you can use the following command:

```shell
$ pytest -s -m integration
```

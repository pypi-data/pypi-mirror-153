# integ-tests

<!--BEGIN STABILITY BANNER-->---


![cdk-constructs: Experimental](https://img.shields.io/badge/cdk--constructs-experimental-important.svg?style=for-the-badge)

> The APIs of higher level constructs in this module are experimental and under active development.
> They are subject to non-backward compatible changes or removal in any future version. These are
> not subject to the [Semantic Versioning](https://semver.org/) model and breaking changes will be
> announced in the release notes. This means that while you may use them, you may need to update
> your source code when upgrading to a newer version of this package.

---
<!--END STABILITY BANNER-->

## Overview

This library is meant to be used in combination with the [integ-runner]() CLI
to enable users to write and execute integration tests for AWS CDK Constructs.

An integration test should be defined as a CDK application, and
there should be a 1:1 relationship between an integration test and a CDK application.

So for example, in order to create an integration test called `my-function`
we would need to create a file to contain our integration test application.

*test/integ.my-function.ts*

```python
app = App()
stack = Stack()
lambda_.Function(stack, "MyFunction",
    runtime=lambda_.Runtime.NODEJS_12_X,
    handler="index.handler",
    code=lambda_.Code.from_asset(path.join(__dirname, "lambda-handler"))
)
```

This is a self contained CDK application which we could deploy by running

```bash
cdk deploy --app 'node test/integ.my-function.js'
```

In order to turn this into an integration test, all that is needed is to
use the `IntegTest` construct.

```python
# app: App
# stack: Stack

IntegTest(app, "Integ", test_cases=[stack])
```

You will notice that the `stack` is registered to the `IntegTest` as a test case.
Each integration test can contain multiple test cases, which are just instances
of a stack. See the [Usage](#usage) section for more details.

## Usage

### IntegTest

Suppose you have a simple stack, that only encapsulates a Lambda function with a
certain handler:

```python
class StackUnderTest(Stack):
    def __init__(self, scope, id, *, architecture=None, description=None, env=None, stackName=None, tags=None, synthesizer=None, terminationProtection=None, analyticsReporting=None):
        super().__init__(scope, id, architecture=architecture, description=description, env=env, stackName=stackName, tags=tags, synthesizer=synthesizer, terminationProtection=terminationProtection, analyticsReporting=analyticsReporting)

        lambda_.Function(self, "Handler",
            runtime=lambda_.Runtime.NODEJS_12_X,
            handler="index.handler",
            code=lambda_.Code.from_asset(path.join(__dirname, "lambda-handler")),
            architecture=architecture
        )
```

You may want to test this stack under different conditions. For example, we want
this stack to be deployed correctly, regardless of the architecture we choose
for the Lambda function. In particular, it should work for both `ARM_64` and
`X86_64`. So you can create an `IntegTestCase` that exercises both scenarios:

```python
class StackUnderTest(Stack):
    def __init__(self, scope, id, *, architecture=None, description=None, env=None, stackName=None, tags=None, synthesizer=None, terminationProtection=None, analyticsReporting=None):
        super().__init__(scope, id, architecture=architecture, description=description, env=env, stackName=stackName, tags=tags, synthesizer=synthesizer, terminationProtection=terminationProtection, analyticsReporting=analyticsReporting)

        lambda_.Function(self, "Handler",
            runtime=lambda_.Runtime.NODEJS_12_X,
            handler="index.handler",
            code=lambda_.Code.from_asset(path.join(__dirname, "lambda-handler")),
            architecture=architecture
        )

# Beginning of the test suite
app = App()

IntegTest(app, "DifferentArchitectures",
    test_cases=[
        StackUnderTest(app, "Stack1",
            architecture=lambda_.Architecture.ARM_64
        ),
        StackUnderTest(app, "Stack2",
            architecture=lambda_.Architecture.X86_64
        )
    ]
)
```

This is all the instruction you need for the integration test runner to know
which stacks to synthesize, deploy and destroy. But you may also need to
customize the behavior of the runner by changing its parameters. For example:

```python
app = App()

stack_under_test = Stack(app, "StackUnderTest")

stack = Stack(app, "stack")

test_case = IntegTest(app, "CustomizedDeploymentWorkflow",
    test_cases=[stack_under_test],
    diff_assets=True,
    stack_update_workflow=True,
    cdk_command_options=CdkCommands(
        deploy=DeployCommand(
            args=DeployOptions(
                require_approval=RequireApproval.NEVER,
                json=True
            )
        ),
        destroy=DestroyCommand(
            args=DestroyOptions(
                force=True
            )
        )
    )
)
```

### IntegTestCaseStack

In the majority of cases an integration test will contain a single `IntegTestCase`.
By default when you create an `IntegTest` an `IntegTestCase` is created for you
and all of your test cases are registered to this `IntegTestCase`. The `IntegTestCase`
and `IntegTestCaseStack` constructs are only needed when it is necessary to
defined different options for individual test cases.

For example, you might want to have one test case where `diffAssets` is enabled.

```python
# app: App
# stack_under_test: Stack

test_case_with_assets = IntegTestCaseStack(app, "TestCaseAssets",
    diff_assets=True
)

IntegTest(app, "Integ", test_cases=[stack_under_test, test_case_with_assets])
```

## Assertions

This library also provides a utility to make assertions against the infrastructure that the integration test deploys.

There are two main scenarios in which assertions are created.

* Part of an integration test using `integ-runner`

In this case you would create an integration test using the `IntegTest` construct and then make assertions using the `assert` property.
You should **not** utilize the assertion constructs directly, but should instead use the `methods` on `IntegTest.assert`.

```python
# app: App
# stack: Stack


integ = IntegTest(app, "Integ", test_cases=[stack])
integ.assertions.aws_api_call("S3", "getObject")
```

* Part of a  normal CDK deployment

In this case you may be using assertions as part of a normal CDK deployment in order to make an assertion on the infrastructure
before the deployment is considered successful. In this case you can utilize the assertions constructs directly.

```python
# my_app_stack: Stack


AwsApiCall(my_app_stack, "GetObject",
    service="S3",
    api="getObject"
)
```

### DeployAssert

Assertions are created by using the `DeployAssert` construct. This construct creates it's own `Stack` separate from
any stacks that you create as part of your integration tests. This `Stack` is treated differently from other stacks
by the `integ-runner` tool. For example, this stack will not be diffed by the `integ-runner`.

`DeployAssert` also provides utilities to register your own assertions.

```python
# my_custom_resource: CustomResource
# stack: Stack
# app: App


integ = IntegTest(app, "Integ", test_cases=[stack])
integ.assertions.expect("CustomAssertion",
    ExpectedResult.object_like({"foo": "bar"}),
    ActualResult.from_custom_resource(my_custom_resource, "data"))
```

In the above example an assertion is created that will trigger a user defined `CustomResource`
and assert that the `data` attribute is equal to `{ foo: 'bar' }`.

### AwsApiCall

A common method to retrieve the "actual" results to compare with what is expected is to make an
AWS API call to receive some data. This library does this by utilizing CloudFormation custom resources
which means that CloudFormation will call out to a Lambda Function which will
use the AWS JavaScript SDK to make the API call.

This can be done by using the class directory (in the case of a normal deployment):

```python
# stack: Stack


AwsApiCall(stack, "MyAssertion",
    service="SQS",
    api="receiveMessage",
    parameters={
        "QueueUrl": "url"
    }
)
```

Or by using the `awsApiCall` method on `DeployAssert` (when writing integration tests):

```python
# app: App
# stack: Stack

integ = IntegTest(app, "Integ",
    test_cases=[stack]
)
integ.assertions.aws_api_call("SQS", "receiveMessage", {
    "QueueUrl": "url"
})
```

### EqualsAssertion

This library currently provides the ability to assert that two values are equal
to one another by utilizing the `EqualsAssertion` class. This utilizes a Lambda
backed `CustomResource` which in tern uses the [Match](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.assertions.Match.html) utility from the
[@aws-cdk/assertions](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.assertions-readme.html) library.

```python
# app: App
# stack: Stack
# queue: sqs.Queue
# fn: lambda.IFunction


integ = IntegTest(app, "Integ",
    test_cases=[stack]
)

integ.assertions.invoke_function(
    function_name=fn.function_name,
    invocation_type=InvocationType.EVENT,
    payload=JSON.stringify({"status": "OK"})
)

message = integ.assertions.aws_api_call("SQS", "receiveMessage", {
    "QueueUrl": queue.queue_url,
    "WaitTimeSeconds": 20
})

message.assert_at_path("Messages.0.Body", ExpectedResult.object_like({
    "request_context": {
        "condition": "Success"
    },
    "request_payload": {
        "status": "OK"
    },
    "response_context": {
        "status_code": 200
    },
    "response_payload": "success"
}))
```

#### Match

`integ-tests` also provides a `Match` utility similar to the `@aws-cdk/assertions` module. `Match`
can be used to construct the `ExpectedResult`.

```python
# message: AwsApiCall


message.expect(ExpectedResult.object_like({
    "Messages": Match.array_with([{
        "Body": {
            "Values": Match.array_with([{"Asdf": 3}]),
            "Message": Match.string_like_regexp("message")
        }
    }
    ])
}))
```

### Examples

#### Invoke a Lambda Function

In this example there is a Lambda Function that is invoked and
we assert that the payload that is returned is equal to '200'.

```python
# lambda_function: lambda.IFunction
# app: App


stack = Stack(app, "cdk-integ-lambda-bundling")

integ = IntegTest(app, "IntegTest",
    test_cases=[stack]
)

invoke = integ.assertions.invoke_function(
    function_name=lambda_function.function_name
)
invoke.expect(ExpectedResult.object_like({
    "Payload": "200"
}))
```

#### Make an AWS API Call

In this example there is a StepFunctions state machine that is executed
and then we assert that the result of the execution is successful.

```python
# app: App
# stack: Stack
# sm: IStateMachine


test_case = IntegTest(app, "IntegTest",
    test_cases=[stack]
)

# Start an execution
start = test_case.assertions.aws_api_call("StepFunctions", "startExecution", {
    "state_machine_arn": sm.state_machine_arn
})

# describe the results of the execution
describe = test_case.assertions.aws_api_call("StepFunctions", "describeExecution", {
    "execution_arn": start.get_att_string("executionArn")
})

# assert the results
describe.expect(ExpectedResult.object_like({
    "status": "SUCCEEDED"
}))
```

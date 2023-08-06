# AWS Systems Manager Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

![cdk-constructs: Stable](https://img.shields.io/badge/cdk--constructs-stable-success.svg?style=for-the-badge)

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

## Installation

Install the module:

```console
$ npm i @aws-cdk/aws-ssm
```

Import it into your code:

```python
import aws_cdk.aws_ssm as ssm
```

## Using existing SSM Parameters in your CDK app

You can reference existing SSM Parameter Store values that you want to use in
your CDK app by using `ssm.StringParameter.fromStringParameterAttributes`:

```python
# Retrieve the latest value of the non-secret parameter
# with name "/My/String/Parameter".
string_value = ssm.StringParameter.from_string_parameter_attributes(self, "MyValue",
    parameter_name="/My/Public/Parameter"
).string_value
string_value_version_from_token = ssm.StringParameter.from_string_parameter_attributes(self, "MyValueVersionFromToken",
    parameter_name="/My/Public/Parameter",
    # parameter version from token
    version=parameter_version
).string_value

# Retrieve a specific version of the secret (SecureString) parameter.
# 'version' is always required.
secret_value = ssm.StringParameter.from_secure_string_parameter_attributes(self, "MySecureValue",
    parameter_name="/My/Secret/Parameter",
    version=5
)
secret_value_version_from_token = ssm.StringParameter.from_secure_string_parameter_attributes(self, "MySecureValueVersionFromToken",
    parameter_name="/My/Secret/Parameter",
    # parameter version from token
    version=parameter_version
)
```

## Creating new SSM Parameters in your CDK app

You can create either `ssm.StringParameter` or `ssm.StringListParameter`s in
a CDK app. These are public (not secret) values. Parameters of type
*SecureString* cannot be created directly from a CDK application; if you want
to provision secrets automatically, use Secrets Manager Secrets (see the
`@aws-cdk/aws-secretsmanager` package).

```python
ssm.StringParameter(self, "Parameter",
    allowed_pattern=".*",
    description="The value Foo",
    parameter_name="FooParameter",
    string_value="Foo",
    tier=ssm.ParameterTier.ADVANCED
)
```

```python
# Create a new SSM Parameter holding a String
param = ssm.StringParameter(stack, "StringParameter",
    # description: 'Some user-friendly description',
    # name: 'ParameterName',
    string_value="Initial parameter value"
)

# Grant read access to some Role
param.grant_read(role)

# Create a new SSM Parameter holding a StringList
list_parameter = ssm.StringListParameter(stack, "StringListParameter",
    # description: 'Some user-friendly description',
    # name: 'ParameterName',
    string_list_value=["Initial parameter value A", "Initial parameter value B"]
)
```

When specifying an `allowedPattern`, the values provided as string literals
are validated against the pattern and an exception is raised if a value
provided does not comply.

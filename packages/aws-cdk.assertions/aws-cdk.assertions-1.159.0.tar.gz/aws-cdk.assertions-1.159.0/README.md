# Assertions

<!--BEGIN STABILITY BANNER-->---


![cdk-constructs: Stable](https://img.shields.io/badge/cdk--constructs-stable-success.svg?style=for-the-badge)

---
<!--END STABILITY BANNER-->

If you're migrating from the old `assert` library, the migration guide can be found in
[our GitHub repository](https://github.com/aws/aws-cdk/blob/master/packages/@aws-cdk/assertions/MIGRATING.md).

Functions for writing test asserting against CDK applications, with focus on CloudFormation templates.

The `Template` class includes a set of methods for writing assertions against CloudFormation templates. Use one of the `Template.fromXxx()` static methods to create an instance of this class.

To create `Template` from CDK stack, start off with:

```python
from aws_cdk.core import Stack
from aws_cdk.assertions import Template

stack = Stack()
# ...
template = Template.from_stack(stack)
```

Alternatively, assertions can be run on an existing CloudFormation template -

```python
template_json = "{ \"Resources\": ... }" # The CloudFormation template as JSON serialized string.
template = Template.from_string(template_json)
```

## Full Template Match

The simplest assertion would be to assert that the template matches a given
template.

```python
template.template_matches({
    "Resources": {
        "BarLogicalId": {
            "Type": "Foo::Bar",
            "Properties": {
                "Baz": "Qux"
            }
        }
    }
})
```

By default, the `templateMatches()` API will use the an 'object-like' comparison,
which means that it will allow for the actual template to be a superset of the
given expectation. See [Special Matchers](#special-matchers) for details on how
to change this.

Snapshot testing is a common technique to store a snapshot of the output and
compare it during future changes. Since CloudFormation templates are human readable,
they are a good target for snapshot testing.

The `toJSON()` method on the `Template` can be used to produce a well formatted JSON
of the CloudFormation template that can be used as a snapshot.

See [Snapshot Testing in Jest](https://jestjs.io/docs/snapshot-testing) and [Snapshot
Testing in Java](https://json-snapshot.github.io/).

## Counting Resources

This module allows asserting the number of resources of a specific type found
in a template.

```python
template.resource_count_is("Foo::Bar", 2)
```

## Resource Matching & Retrieval

Beyond resource counting, the module also allows asserting that a resource with
specific properties are present.

The following code asserts that the `Properties` section of a resource of type
`Foo::Bar` contains the specified properties -

```python
template.has_resource_properties("Foo::Bar", {
    "Foo": "Bar",
    "Baz": 5,
    "Qux": ["Waldo", "Fred"]
})
```

Alternatively, if you would like to assert the entire resource definition, you
can use the `hasResource()` API.

```python
template.has_resource("Foo::Bar", {
    "Properties": {"Foo": "Bar"},
    "DependsOn": ["Waldo", "Fred"]
})
```

Beyond assertions, the module provides APIs to retrieve matching resources.
The `findResources()` API is complementary to the `hasResource()` API, except,
instead of asserting its presence, it returns the set of matching resources.

By default, the `hasResource()` and `hasResourceProperties()` APIs perform deep
partial object matching. This behavior can be configured using matchers.
See subsequent section on [special matchers](#special-matchers).

## Output and Mapping sections

The module allows you to assert that the CloudFormation template contains an Output
that matches specific properties. The following code asserts that a template contains
an Output with a `logicalId` of `Foo` and the specified properties -

```python
expected = {
    "Value": "Bar",
    "Export": {"Name": "ExportBaz"}
}
template.has_output("Foo", expected)
```

If you want to match against all Outputs in the template, use `*` as the `logicalId`.

```python
template.has_output("*", {
    "Value": "Bar",
    "Export": {"Name": "ExportBaz"}
})
```

`findOutputs()` will return a set of outputs that match the `logicalId` and `props`,
and you can use the `'*'` special case as well.

```python
result = template.find_outputs("*", {"Value": "Fred"})
expect(result.Foo).to_equal({"Value": "Fred", "Description": "FooFred"})
expect(result.Bar).to_equal({"Value": "Fred", "Description": "BarFred"})
```

The APIs `hasMapping()`, `findMappings()`, `hasCondition()`, and `hasCondtions()` provide similar functionalities.

## Special Matchers

The expectation provided to the `hasXxx()`, `findXxx()` and `templateMatches()`
APIs, besides carrying literal values, as seen in the above examples, also accept
special matchers.

They are available as part of the `Match` class.

### Object Matchers

The `Match.objectLike()` API can be used to assert that the target is a superset
object of the provided pattern.
This API will perform a deep partial match on the target.
Deep partial matching is where objects are matched partially recursively. At each
level, the list of keys in the target is a subset of the provided pattern.

```python
# Given a template -
# {
#   "Resources": {
#     "MyBar": {
#       "Type": "Foo::Bar",
#       "Properties": {
#         "Fred": {
#           "Wobble": "Flob",
#           "Bob": "Cat"
#         }
#       }
#     }
#   }
# }

# The following will NOT throw an assertion error
template.has_resource_properties("Foo::Bar", {
    "Fred": Match.object_like({
        "Wobble": "Flob"
    })
})

# The following will throw an assertion error
template.has_resource_properties("Foo::Bar", {
    "Fred": Match.object_like({
        "Brew": "Coffee"
    })
})
```

The `Match.objectEquals()` API can be used to assert a target as a deep exact
match.

### Presence and Absence

The `Match.absent()` matcher can be used to specify that a specific
value should not exist on the target. This can be used within `Match.objectLike()`
or outside of any matchers.

```python
# Given a template -
# {
#   "Resources": {
#     "MyBar": {
#       "Type": "Foo::Bar",
#       "Properties": {
#         "Fred": {
#           "Wobble": "Flob",
#         }
#       }
#     }
#   }
# }

# The following will NOT throw an assertion error
template.has_resource_properties("Foo::Bar", {
    "Fred": Match.object_like({
        "Bob": Match.absent()
    })
})

# The following will throw an assertion error
template.has_resource_properties("Foo::Bar", {
    "Fred": Match.object_like({
        "Wobble": Match.absent()
    })
})
```

The `Match.anyValue()` matcher can be used to specify that a specific value should be found
at the location. This matcher will fail if when the target location has null-ish values
(i.e., `null` or `undefined`).

This matcher can be combined with any of the other matchers.

```python
# Given a template -
# {
#   "Resources": {
#     "MyBar": {
#       "Type": "Foo::Bar",
#       "Properties": {
#         "Fred": {
#           "Wobble": ["Flob", "Flib"],
#         }
#       }
#     }
#   }
# }

# The following will NOT throw an assertion error
template.has_resource_properties("Foo::Bar", {
    "Fred": {
        "Wobble": [Match.any_value(), Match.any_value()]
    }
})

# The following will throw an assertion error
template.has_resource_properties("Foo::Bar", {
    "Fred": {
        "Wimble": Match.any_value()
    }
})
```

### Array Matchers

The `Match.arrayWith()` API can be used to assert that the target is equal to or a subset
of the provided pattern array.
This API will perform subset match on the target.

```python
# Given a template -
# {
#   "Resources": {
#     "MyBar": {
#       "Type": "Foo::Bar",
#       "Properties": {
#         "Fred": ["Flob", "Cat"]
#       }
#     }
#   }
# }

# The following will NOT throw an assertion error
template.has_resource_properties("Foo::Bar", {
    "Fred": Match.array_with(["Flob"])
})

# The following will throw an assertion error
template.has_resource_properties("Foo::Bar", Match.object_like({
    "Fred": Match.array_with(["Wobble"])
}))
```

*Note:* The list of items in the pattern array should be in order as they appear in the
target array. Out of order will be recorded as a match failure.

Alternatively, the `Match.arrayEquals()` API can be used to assert that the target is
exactly equal to the pattern array.

### String Matchers

The `Match.stringLikeRegexp()` API can be used to assert that the target matches the
provided regular expression.

```python
# Given a template -
# {
#   "Resources": {
#     "MyBar": {
#       "Type": "Foo::Bar",
#       "Properties": {
#         "Template": "const includeHeaders = true;"
#       }
#     }
#   }
# }

# The following will NOT throw an assertion error
template.has_resource_properties("Foo::Bar", {
    "Template": Match.string_like_regexp("includeHeaders = (true|false)")
})

# The following will throw an assertion error
template.has_resource_properties("Foo::Bar", {
    "Template": Match.string_like_regexp("includeHeaders = null")
})
```

### Not Matcher

The not matcher inverts the search pattern and matches all patterns in the path that does
not match the pattern specified.

```python
# Given a template -
# {
#   "Resources": {
#     "MyBar": {
#       "Type": "Foo::Bar",
#       "Properties": {
#         "Fred": ["Flob", "Cat"]
#       }
#     }
#   }
# }

# The following will NOT throw an assertion error
template.has_resource_properties("Foo::Bar", {
    "Fred": Match.not(["Flob"])
})

# The following will throw an assertion error
template.has_resource_properties("Foo::Bar", Match.object_like({
    "Fred": Match.not(["Flob", "Cat"])
}))
```

### Serialized JSON

Often, we find that some CloudFormation Resource types declare properties as a string,
but actually expect JSON serialized as a string.
For example, the [`BuildSpec` property of `AWS::CodeBuild::Project`](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-source.html#cfn-codebuild-project-source-buildspec),
the [`Definition` property of `AWS::StepFunctions::StateMachine`](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-stepfunctions-statemachine.html#cfn-stepfunctions-statemachine-definition),
to name a couple.

The `Match.serializedJson()` matcher allows deep matching within a stringified JSON.

```python
# Given a template -
# {
#   "Resources": {
#     "MyBar": {
#       "Type": "Foo::Bar",
#       "Properties": {
#         "Baz": "{ \"Fred\": [\"Waldo\", \"Willow\"] }"
#       }
#     }
#   }
# }

# The following will NOT throw an assertion error
template.has_resource_properties("Foo::Bar", {
    "Baz": Match.serialized_json({
        "Fred": Match.array_with(["Waldo"])
    })
})

# The following will throw an assertion error
template.has_resource_properties("Foo::Bar", {
    "Baz": Match.serialized_json({
        "Fred": ["Waldo", "Johnny"]
    })
})
```

## Capturing Values

The matcher APIs documented above allow capturing values in the matching entry
(Resource, Output, Mapping, etc.). The following code captures a string from a
matching resource.

```python
# Given a template -
# {
#   "Resources": {
#     "MyBar": {
#       "Type": "Foo::Bar",
#       "Properties": {
#         "Fred": ["Flob", "Cat"],
#         "Waldo": ["Qix", "Qux"],
#       }
#     }
#   }
# }

fred_capture = Capture()
waldo_capture = Capture()
template.has_resource_properties("Foo::Bar", {
    "Fred": fred_capture,
    "Waldo": ["Qix", waldo_capture]
})

fred_capture.as_array() # returns ["Flob", "Cat"]
waldo_capture.as_string()
```

With captures, a nested pattern can also be specified, so that only targets
that match the nested pattern will be captured. This pattern can be literals or
further Matchers.

```python
# Given a template -
# {
#   "Resources": {
#     "MyBar1": {
#       "Type": "Foo::Bar",
#       "Properties": {
#         "Fred": ["Flob", "Cat"],
#       }
#     }
#     "MyBar2": {
#       "Type": "Foo::Bar",
#       "Properties": {
#         "Fred": ["Qix", "Qux"],
#       }
#     }
#   }
# }

capture = Capture(Match.array_with(["Cat"]))
template.has_resource_properties("Foo::Bar", {
    "Fred": capture
})

capture.as_array()
```

When multiple resources match the given condition, each `Capture` defined in
the condition will capture all matching values. They can be paged through using
the `next()` API. The following example illustrates this -

```python
# Given a template -
# {
#   "Resources": {
#     "MyBar": {
#       "Type": "Foo::Bar",
#       "Properties": {
#         "Fred": "Flob",
#       }
#     },
#     "MyBaz": {
#       "Type": "Foo::Bar",
#       "Properties": {
#         "Fred": "Quib",
#       }
#     }
#   }
# }

fred_capture = Capture()
template.has_resource_properties("Foo::Bar", {
    "Fred": fred_capture
})

fred_capture.as_string() # returns "Flob"
fred_capture.next() # returns true
fred_capture.as_string()
```

## Asserting Annotations

In addition to template matching, we provide an API for annotation matching.
[Annotations](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.Annotations.html)
can be added via the [Aspects](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.Aspects.html)
API. You can learn more about Aspects [here](https://docs.aws.amazon.com/cdk/v2/guide/aspects.html).

Say you have a `MyAspect` and a `MyStack` that uses `MyAspect`:

```python
import aws_cdk.core as cdk
from constructs import Construct, IConstruct

class MyAspect(cdk.IAspect):
    def visit(self, node):
        if node instanceof cdk.CfnResource && node.cfn_resource_type == "Foo::Bar":
            self.error(node, "we do not want a Foo::Bar resource")

    def error(self, node, message):
        cdk.Annotations.of(node).add_error(message)

class MyStack(cdk.Stack):
    def __init__(self, scope, id):
        super().__init__(scope, id)

        stack = cdk.Stack()
        cdk.CfnResource(stack, "Foo",
            type="Foo::Bar",
            properties={
                "Fred": "Thud"
            }
        )
        cdk.Aspects.of(stack).add(MyAspect())
```

We can then assert that the stack contains the expected Error:

```python
# import { Annotations } from '@aws-cdk/assertions';

Annotations.from_stack(stack).has_error("/Default/Foo", "we do not want a Foo::Bar resource")
```

Here are the available APIs for `Annotations`:

* `hasError()`, `hasNoError()`, and `findError()`
* `hasWarning()`, `hasNoWarning()`, and `findWarning()`
* `hasInfo()`, `hasNoInfo()`, and `findInfo()`

The corresponding `findXxx()` API is complementary to the `hasXxx()` API, except instead
of asserting its presence, it returns the set of matching messages.

In addition, this suite of APIs is compatable with `Matchers` for more fine-grained control.
For example, the following assertion works as well:

```python
Annotations.from_stack(stack).has_error("/Default/Foo",
    Match.string_like_regexp(".*Foo::Bar.*"))
```

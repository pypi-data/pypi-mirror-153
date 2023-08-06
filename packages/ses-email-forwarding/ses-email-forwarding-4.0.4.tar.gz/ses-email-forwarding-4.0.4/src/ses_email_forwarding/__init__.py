'''
# @seeebiii/ses-email-forwarding

This [AWS CDK](https://aws.amazon.com/cdk/) construct allows you to setup email forwarding mappings in [AWS SES](https://aws.amazon.com/ses/) to receive emails from your domain and forward them to another email address.
All of this is possible without hosting your own email server, you just need a domain.

For example, if you own a domain `example.org` and want to receive emails for `hello@example.org` and `privacy@example.org`, you can forward emails to `whatever@provider.com`.
This is achieved by using a Lambda function that forwards the emails using [aws-lambda-ses-forwarder](https://github.com/arithmetric/aws-lambda-ses-forwarder).

This construct is creating quite a few resources under the hood and can also automatically verify your domain and email addresses in SES.
Consider reading the [Architecture](#architecture) section below if you want to know more about the details.

## Examples

Forward all emails received under `hello@example.org` to `whatever+hello@provider.com`:

```javascript
new EmailForwardingRuleSet(this, 'EmailForwardingRuleSet', {
  // make the underlying rule set the active one
  enableRuleSet: true,
  // define how emails are being forwarded
  emailForwardingProps: [{
    // your domain name you want to use for receiving and sending emails
    domainName: 'example.org',
    // a prefix that is used for the From email address to forward your mails
    fromPrefix: 'noreply',
    // a list of mappings between a prefix and target email address
    emailMappings: [{
      // the prefix matching the receiver address as <prefix>@<domainName>
      receivePrefix: 'hello',
      // the target email address(es) that you want to forward emails to
      targetEmails: ['whatever+hello@provider.com']
    }]
  }]
});
```

Forward all emails to `hello@example.org` to `whatever+hello@provider.com` and verify the domain `example.org` in SES:

```javascript
new EmailForwardingRuleSet(this, 'EmailForwardingRuleSet', {
  emailForwardingProps: [{
    domainName: 'example.org',
    // let the construct automatically verify your domain
    verifyDomain: true,
    fromPrefix: 'noreply',
    emailMappings: [{
      receivePrefix: 'hello',
      targetEmails: ['whatever+hello@provider.com']
    }]
  }]
});
```

If you don't want to verify your domain in SES or you are in the SES sandbox, you can still send emails to verified email addresses.
Use the property `verifyTargetEmailAddresses` in this case and set it to `true`.

For a full & up-to-date reference of the available options, please look at the source code of  [`EmailForwardingRuleSet`](lib/email-forwarding-rule-set.ts) and [`EmailForwardingRule`](lib/email-forwarding-rule.ts).

#### Note

Since the verification of domains requires to lookup the Route53 domains in your account, you need to define your AWS account and region.
You can do it like this in your CDK stack:

```python
const app = new cdk.App();

class EmailForwardingSetupStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    new EmailForwardingRuleSet(this, 'EmailForwardingRuleSet', {
      // define your config here
    });
  }
}

new EmailForwardingSetupStack(app, 'EmailForwardingSetupStack', {
  env: {
    account: '<account-id>',
    region: '<region>'
  }
});
```

## Use Cases

* Build a landing page on AWS and offer an email address to contact you.
* Use various aliases to register for different services and forward all mails to the same target email address.

There are probably more - happy to hear them :)

## Install

### npm

```shell
npm i -D @seeebiii/ses-email-forwarding
```

Take a look at [package.json](./package.json) to make sure you're installing the correct version compatible with your current AWS CDK version.
See more details on npmjs.com: https://www.npmjs.com/package/@seeebiii/ses-email-forwarding

### Maven

```xml
<dependency>
  <groupId>de.sebastianhesse.cdk-constructs</groupId>
  <artifactId>ses-email-forwarding</artifactId>
  <version>4.0.1</version>
</dependency>
```

See more details on mvnrepository.com: https://mvnrepository.com/artifact/de.sebastianhesse.cdk-constructs/ses-email-forwarding/

#### Example Code

```java
package com.example;

import de.sebastianhesse.cdk.ses.email.forwarding.EmailForwardingProps;
import de.sebastianhesse.cdk.ses.email.forwarding.EmailForwardingRuleSet;
import de.sebastianhesse.cdk.ses.email.forwarding.EmailMapping;
import java.util.Arrays;
import software.amazon.awscdk.core.App;

import software.amazon.awscdk.core.Construct;
import software.amazon.awscdk.core.Environment;
import software.amazon.awscdk.core.Stack;
import software.amazon.awscdk.core.StackProps;

public class SesEmailForwardingJavaTestApp {
    public static void main(final String[] args) {
        App app = new App();

        new SesEmailForwardingJavaTestStack(app, "CdkEmailForwardingJavaTestStack", StackProps.builder()
                .env(Environment.builder()
                        .account("123456789") // TODO: replace with your account id
                        .region("us-east-1") // TODO: replace with your region
                        .build()
                )
                .build());

        app.synth();
    }

    static class SesEmailForwardingJavaTestStack extends Stack {
        public SesEmailForwardingJavaTestStack(final Construct scope, final String id) {
            this(scope, id, null);
        }

        public SesEmailForwardingJavaTestStack(final Construct scope, final String id, final StackProps props) {
            super(scope, id, props);

            EmailForwardingProps exampleProperties = EmailForwardingProps.builder()
                    .domainName("example.org")
                    // true if you own the domain in Route53, false if you need to manually verify it
                    .verifyDomain(true)
                    .fromPrefix("noreply")
                    .emailMappings(Arrays.asList(
                            EmailMapping.builder()
                                    .receiveEmail("hello@example.org")
                                    .targetEmails(Arrays.asList("email+hello@provider.com"))
                                    .build(),
                            EmailMapping.builder()
                                    .receiveEmail("privacy@example.org")
                                    .targetEmails(Arrays.asList("email+privacy@provider.com"))
                                    .build()
                            )
                    )
                    .build();

            EmailForwardingRuleSet.Builder.create(this, "example-rule-set")
                    .ruleSetName("example-rule-set")
                    .emailForwardingProps(Arrays.asList(exampleProperties))
                    .build();
        }
    }
}
```

### Python

```shell
pip install ses-email-forwarding
```

See more details on PyPi: https://pypi.org/project/ses-email-forwarding/

### .NET / C#

An artifact is pushed up to NuGet.org: https://www.nuget.org/packages/Ses.Email.Forwarding/

#### Project Scaffolding & Installation

```bash
# Create a new directory
mkdir ExampleApplication && cd ExampleApplication

# Scaffold a C# CDK project
cdk init --language csharp

# Add dependencies
cd src/ExampleApplication
dotnet add package Ses.Email.Forwarding
dotnet add package Amazon.CDK.AWS.SNS.Subscriptions

# Remove example stack and global suppressions (silenced by way of using discards)
rm ExampleApplicationStack.cs GlobalSuppressions.cs
```

#### Example Usage

```csharp
using Amazon.CDK;
using Amazon.CDK.AWS.SNS;
using Amazon.CDK.AWS.SNS.Subscriptions;
using SebastianHesse.CdkConstructs;
using Construct = Constructs.Construct;

namespace ExampleApplication
{
    public sealed class Program
    {
        public static void Main()
        {
            var app = new App();

            _ = new MailboxStack(app, nameof(MailboxStack), new StackProps
            {
                Env = new Environment
                {
                    // Replace with desired account
                    Account = "000000000000",

                    // Replace with desired region
                    Region = "us-east-1"
                }
            });

            app.Synth();
        }
    }

    public sealed class MailboxStack : Stack
    {
        public MailboxStack(Construct scope, string id, IStackProps props = null) : base(scope, id, props)
        {
            var notificationTopic = new Topic(this, nameof(EmailForwardingProps.NotificationTopic));

            // 'Bounce' and 'Complaint' notification types, in association with the domain being verified, will be sent
            // to this email address
            notificationTopic.AddSubscription(new EmailSubscription("admin@provider.com"));

            _ = new EmailForwardingRuleSet(this, nameof(EmailForwardingRuleSet), new EmailForwardingRuleSetProps
            {
                EmailForwardingProps = new IEmailForwardingProps[]
                {
                    new EmailForwardingProps
                    {
                        // If your domain name has already been verified as a domain identity in SES, this does not
                        // need to be toggled on
                        VerifyDomain = true,

                        // This is the prefix that will be used in the email address used to forward emails
                        FromPrefix = "noreply",

                        // This domain name will be used to send and receive emails
                        DomainName = "example.org",

                        // A list of mappings between a prefix and target email addresses
                        EmailMappings = new IEmailMapping[]
                        {
                            new EmailMapping
                            {
                                // Emails received by hello@example.org will be forwarded
                                ReceivePrefix = "hello",

                                // Emails will be forwarded to admin+hello@provider.com
                                TargetEmails = new []
                                {
                                    "admin+hello@provider.com"
                                }
                            }
                        },

                        // This notification topic be published to when events in association with 'Bounce' and
                        // 'Complaint' notification types occur
                        NotificationTopic = notificationTopic
                    }
                }
            });
        }
    }
}
```

## Usage

This package provides two constructs: [`EmailForwardingRuleSet`](lib/email-forwarding-rule-set.ts) and [`EmailForwardingRule`](lib/email-forwarding-rule.ts).
The `EmailForwardingRuleSet` is a wrapper around `ReceiptRuleSet` but adds a bit more magic to e.g. verify a domain or target email address.
Similarly, `EmailForwardingRule` is a wrapper around `ReceiptRule` but adds two SES rule actions to forward the email addresses appropriately.

This means if you want the full flexibility, you can use the `EmailForwardingRule` construct in your stack.

### Sending E-Mails over SMTP

You can also send emails over SES using this construct because it provides the basics for sending emails: a verified SES domain or email address identity.
You need to do the following if you're using the `EmailForwardingRuleSetConstruct`:

1. Set the `verifyDomain` or `verifyTargetEmailAddresses` to `true`.
2. [Create SMTP credentials in AWS SES](https://docs.aws.amazon.com/ses/latest/DeveloperGuide/smtp-credentials.html?icmpid=docs_ses_console) and save them somewhere.
3. Setup your email program or application to use the SMTP settings.

## Architecture

The `EmailForwardingRuleSet` creates a `EmailForwardingRule` for each forward mapping.
Each rule contains an `S3Action` to store the incoming emails and a Lambda Function to forward the emails to the target email addresses.
The Lambda function is just a thin wrapper around the [aws-lambda-ses-forwarder](https://github.com/arithmetric/aws-lambda-ses-forwarder) library.
Since this library expects a JSON config with the email mappings, the `EmailForwardingRule` will create an SSM parameter to store the config.
(Note: this is not ideal because an SSM parameter is limited in the size and hence, this might be changed later)
The Lambda function receives a reference to this parameter as an environment variable (and a bit more) and forwards everything to the library.

In order to verify a domain or email address, the `EmailForwardingRuleSet` construct is using the package [@seeebiii/ses-verify-identities](https://www.npmjs.com/package/@seeebiii/ses-verify-identities).
It provides constructs to verify the SES identities.
For domains, it creates appropriate Route53 records like MX, TXT and Cname (for DKIM).
For email addresses, it calls the AWS API to initiate email address verification.

## TODO

* Encrypt email files on S3 bucket by either using S3 bucket encryption (server side) or enable client encryption using SES actions

## Contributing

I'm happy to receive any contributions!
Just open an issue or pull request :)

These commands should help you while developing:

* `npx projen`          init [projen](https://github.com/projen/projen) and synthesize changes in [.projenrc.js](.projenrc.js) to the project
* `yarn build`          compile typescript to js
* `yarn watch`          watch for changes and compile
* `yarn test`           perform the jest unit tests
* `yarn eslint`         validate code against best practices

## Thanks

Thanks a lot to [arithmetric](https://github.com/arithmetric) for providing the NPM package [aws-lambda-ses-forwarder](https://github.com/arithmetric/aws-lambda-ses-forwarder).
This CDK construct is using it in the Lambda function to forward the emails.

## Author

[Sebastian Hesse](https://www.sebastianhesse.de) - Freelancer for serverless cloud projects on AWS.

## License

MIT License

Copyright (c) 2022 [Sebastian Hesse](https://www.sebastianhesse.de)

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from ._jsii import *

import aws_cdk.aws_s3
import aws_cdk.aws_ses
import aws_cdk.aws_sns
import constructs


@jsii.data_type(
    jsii_type="@seeebiii/ses-email-forwarding.EmailForwardingProps",
    jsii_struct_bases=[],
    name_mapping={
        "domain_name": "domainName",
        "email_mappings": "emailMappings",
        "from_prefix": "fromPrefix",
        "bucket": "bucket",
        "bucket_prefix": "bucketPrefix",
        "notification_topic": "notificationTopic",
        "notification_types": "notificationTypes",
        "verify_domain": "verifyDomain",
        "verify_target_email_addresses": "verifyTargetEmailAddresses",
    },
)
class EmailForwardingProps:
    def __init__(
        self,
        *,
        domain_name: builtins.str,
        email_mappings: typing.Sequence["EmailMapping"],
        from_prefix: builtins.str,
        bucket: typing.Optional[aws_cdk.aws_s3.Bucket] = None,
        bucket_prefix: typing.Optional[builtins.str] = None,
        notification_topic: typing.Optional[aws_cdk.aws_sns.Topic] = None,
        notification_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        verify_domain: typing.Optional[builtins.bool] = None,
        verify_target_email_addresses: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param domain_name: The domain name for which you want to receive emails using SES, e.g. ``example.org``.
        :param email_mappings: A list of email mappings to define the receive email address and target email addresses to which the emails are forwarded to.
        :param from_prefix: A prefix that is used as the sender address of the forwarded mail, e.g. ``noreply``.
        :param bucket: Optional: an S3 bucket to store the received emails. If none is provided, a new one will be created. Default: A new bucket.
        :param bucket_prefix: Optional: a prefix for the email files that are stored on the S3 bucket. Default: inbox/
        :param notification_topic: Optional: an SNS topic to receive notifications about sending events like bounces or complaints. The events are defined by ``notificationTypes`` using {@link NotificationType}. If no topic is defined, a new one will be created. Default: A new SNS topic.
        :param notification_types: Optional: a list of {@link NotificationType}s to define which sending events should be subscribed. Default: ['Bounce', 'Complaint']
        :param verify_domain: Optional: true if you want to verify the domain identity in SES, false otherwise. Default: false
        :param verify_target_email_addresses: Optional: true if you want to initiate the verification of your target email addresses, false otherwise. If ``true``, a verification email is sent out to all target email addresses. Then, the owner of an email address needs to verify it by clicking the link in the verification email. Please note in case you don't verify your sender domain, it's required to verify your target email addresses in order to send mails to them. Default: false
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "domain_name": domain_name,
            "email_mappings": email_mappings,
            "from_prefix": from_prefix,
        }
        if bucket is not None:
            self._values["bucket"] = bucket
        if bucket_prefix is not None:
            self._values["bucket_prefix"] = bucket_prefix
        if notification_topic is not None:
            self._values["notification_topic"] = notification_topic
        if notification_types is not None:
            self._values["notification_types"] = notification_types
        if verify_domain is not None:
            self._values["verify_domain"] = verify_domain
        if verify_target_email_addresses is not None:
            self._values["verify_target_email_addresses"] = verify_target_email_addresses

    @builtins.property
    def domain_name(self) -> builtins.str:
        '''The domain name for which you want to receive emails using SES, e.g. ``example.org``.'''
        result = self._values.get("domain_name")
        assert result is not None, "Required property 'domain_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def email_mappings(self) -> typing.List["EmailMapping"]:
        '''A list of email mappings to define the receive email address and target email addresses to which the emails are forwarded to.

        :see: EmailMapping
        '''
        result = self._values.get("email_mappings")
        assert result is not None, "Required property 'email_mappings' is missing"
        return typing.cast(typing.List["EmailMapping"], result)

    @builtins.property
    def from_prefix(self) -> builtins.str:
        '''A prefix that is used as the sender address of the forwarded mail, e.g. ``noreply``.'''
        result = self._values.get("from_prefix")
        assert result is not None, "Required property 'from_prefix' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def bucket(self) -> typing.Optional[aws_cdk.aws_s3.Bucket]:
        '''Optional: an S3 bucket to store the received emails.

        If none is provided, a new one will be created.

        :default: A new bucket.
        '''
        result = self._values.get("bucket")
        return typing.cast(typing.Optional[aws_cdk.aws_s3.Bucket], result)

    @builtins.property
    def bucket_prefix(self) -> typing.Optional[builtins.str]:
        '''Optional: a prefix for the email files that are stored on the S3 bucket.

        :default: inbox/
        '''
        result = self._values.get("bucket_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def notification_topic(self) -> typing.Optional[aws_cdk.aws_sns.Topic]:
        '''Optional: an SNS topic to receive notifications about sending events like bounces or complaints.

        The events are defined by ``notificationTypes`` using {@link NotificationType}. If no topic is defined, a new one will be created.

        :default: A new SNS topic.
        '''
        result = self._values.get("notification_topic")
        return typing.cast(typing.Optional[aws_cdk.aws_sns.Topic], result)

    @builtins.property
    def notification_types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Optional: a list of {@link NotificationType}s to define which sending events should be subscribed.

        :default: ['Bounce', 'Complaint']
        '''
        result = self._values.get("notification_types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def verify_domain(self) -> typing.Optional[builtins.bool]:
        '''Optional: true if you want to verify the domain identity in SES, false otherwise.

        :default: false
        '''
        result = self._values.get("verify_domain")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def verify_target_email_addresses(self) -> typing.Optional[builtins.bool]:
        '''Optional: true if you want to initiate the verification of your target email addresses, false otherwise.

        If ``true``, a verification email is sent out to all target email addresses. Then, the owner of an email address needs to verify it by clicking the link in the verification email.
        Please note in case you don't verify your sender domain, it's required to verify your target email addresses in order to send mails to them.

        :default: false
        '''
        result = self._values.get("verify_target_email_addresses")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EmailForwardingProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EmailForwardingRule(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@seeebiii/ses-email-forwarding.EmailForwardingRule",
):
    '''A construct to define an email forwarding rule that can either be used together with {@link EmailForwardingRuleSet} or as a standalone rule.

    It creates two rule actions:

    - One S3 action to save all incoming mails to an S3 bucket.
    - One Lambda action to forward all incoming mails to a list of configured emails.

    The Lambda function is using the NPM package ``aws-lambda-ses-forwarder`` to forward the mails.
    '''

    def __init__(
        self,
        parent: constructs.Construct,
        name: builtins.str,
        *,
        domain_name: builtins.str,
        email_mapping: typing.Sequence["EmailMapping"],
        from_prefix: builtins.str,
        id: builtins.str,
        rule_set: aws_cdk.aws_ses.IReceiptRuleSet,
        bucket: typing.Optional[aws_cdk.aws_s3.Bucket] = None,
        bucket_prefix: typing.Optional[builtins.str] = None,
        enable_lambda_logging: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param parent: -
        :param name: -
        :param domain_name: The domain name of the email addresses, e.g. 'example.org'. It is used to connect the ``fromPrefix`` and ``receivePrefix`` properties with a proper domain.
        :param email_mapping: An email mapping similar to what the NPM library ``aws-lambda-ses-forwarder`` expects.
        :param from_prefix: A prefix that is used as the sender address of the forwarded mail, e.g. ``noreply``.
        :param id: An id for the rule. This will mainly be used to provide a name to the underlying rule but may also be used as a prefix for other resources.
        :param rule_set: The rule set this rule belongs to.
        :param bucket: A bucket to store the email files to. If no bucket is provided, a new one will be created using a managed KMS key to encrypt the bucket. Default: A new bucket will be created.
        :param bucket_prefix: A prefix for the email files that are saved to the bucket. Default: inbox/
        :param enable_lambda_logging: Enable log messages in Lambda function which forwards emails. Default: true
        '''
        props = EmailForwardingRuleProps(
            domain_name=domain_name,
            email_mapping=email_mapping,
            from_prefix=from_prefix,
            id=id,
            rule_set=rule_set,
            bucket=bucket,
            bucket_prefix=bucket_prefix,
            enable_lambda_logging=enable_lambda_logging,
        )

        jsii.create(self.__class__, self, [parent, name, props])


@jsii.data_type(
    jsii_type="@seeebiii/ses-email-forwarding.EmailForwardingRuleProps",
    jsii_struct_bases=[],
    name_mapping={
        "domain_name": "domainName",
        "email_mapping": "emailMapping",
        "from_prefix": "fromPrefix",
        "id": "id",
        "rule_set": "ruleSet",
        "bucket": "bucket",
        "bucket_prefix": "bucketPrefix",
        "enable_lambda_logging": "enableLambdaLogging",
    },
)
class EmailForwardingRuleProps:
    def __init__(
        self,
        *,
        domain_name: builtins.str,
        email_mapping: typing.Sequence["EmailMapping"],
        from_prefix: builtins.str,
        id: builtins.str,
        rule_set: aws_cdk.aws_ses.IReceiptRuleSet,
        bucket: typing.Optional[aws_cdk.aws_s3.Bucket] = None,
        bucket_prefix: typing.Optional[builtins.str] = None,
        enable_lambda_logging: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param domain_name: The domain name of the email addresses, e.g. 'example.org'. It is used to connect the ``fromPrefix`` and ``receivePrefix`` properties with a proper domain.
        :param email_mapping: An email mapping similar to what the NPM library ``aws-lambda-ses-forwarder`` expects.
        :param from_prefix: A prefix that is used as the sender address of the forwarded mail, e.g. ``noreply``.
        :param id: An id for the rule. This will mainly be used to provide a name to the underlying rule but may also be used as a prefix for other resources.
        :param rule_set: The rule set this rule belongs to.
        :param bucket: A bucket to store the email files to. If no bucket is provided, a new one will be created using a managed KMS key to encrypt the bucket. Default: A new bucket will be created.
        :param bucket_prefix: A prefix for the email files that are saved to the bucket. Default: inbox/
        :param enable_lambda_logging: Enable log messages in Lambda function which forwards emails. Default: true
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "domain_name": domain_name,
            "email_mapping": email_mapping,
            "from_prefix": from_prefix,
            "id": id,
            "rule_set": rule_set,
        }
        if bucket is not None:
            self._values["bucket"] = bucket
        if bucket_prefix is not None:
            self._values["bucket_prefix"] = bucket_prefix
        if enable_lambda_logging is not None:
            self._values["enable_lambda_logging"] = enable_lambda_logging

    @builtins.property
    def domain_name(self) -> builtins.str:
        '''The domain name of the email addresses, e.g. 'example.org'. It is used to connect the ``fromPrefix`` and ``receivePrefix`` properties with a proper domain.'''
        result = self._values.get("domain_name")
        assert result is not None, "Required property 'domain_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def email_mapping(self) -> typing.List["EmailMapping"]:
        '''An email mapping similar to what the NPM library ``aws-lambda-ses-forwarder`` expects.

        :see: EmailMapping
        '''
        result = self._values.get("email_mapping")
        assert result is not None, "Required property 'email_mapping' is missing"
        return typing.cast(typing.List["EmailMapping"], result)

    @builtins.property
    def from_prefix(self) -> builtins.str:
        '''A prefix that is used as the sender address of the forwarded mail, e.g. ``noreply``.'''
        result = self._values.get("from_prefix")
        assert result is not None, "Required property 'from_prefix' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> builtins.str:
        '''An id for the rule.

        This will mainly be used to provide a name to the underlying rule but may also be used as a prefix for other resources.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def rule_set(self) -> aws_cdk.aws_ses.IReceiptRuleSet:
        '''The rule set this rule belongs to.'''
        result = self._values.get("rule_set")
        assert result is not None, "Required property 'rule_set' is missing"
        return typing.cast(aws_cdk.aws_ses.IReceiptRuleSet, result)

    @builtins.property
    def bucket(self) -> typing.Optional[aws_cdk.aws_s3.Bucket]:
        '''A bucket to store the email files to.

        If no bucket is provided, a new one will be created using a managed KMS key to encrypt the bucket.

        :default: A new bucket will be created.
        '''
        result = self._values.get("bucket")
        return typing.cast(typing.Optional[aws_cdk.aws_s3.Bucket], result)

    @builtins.property
    def bucket_prefix(self) -> typing.Optional[builtins.str]:
        '''A prefix for the email files that are saved to the bucket.

        :default: inbox/
        '''
        result = self._values.get("bucket_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_lambda_logging(self) -> typing.Optional[builtins.bool]:
        '''Enable log messages in Lambda function which forwards emails.

        :default: true
        '''
        result = self._values.get("enable_lambda_logging")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EmailForwardingRuleProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EmailForwardingRuleSet(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@seeebiii/ses-email-forwarding.EmailForwardingRuleSet",
):
    '''A construct for AWS SES to forward all emails of certain domains and email addresses to a list of target email addresses.

    It also verifies (or at least initiates verification of) the related domains and email addresses in SES.

    The construct can be helpful if you don't want to host your own SMTP server but still want to receive emails to your existing email inbox.
    One use case is if you're just building some sort of landing page and want to quickly setup email receiving for your domain without yet another separate email inbox.

    This construct can...

    - create a new receipt rule set (or use an existing one),
    - attach a list of rules to forward incoming emails to other target email addresses,
    - verify a given domain in SES (automatically if domain is managed by Route53, otherwise it'll just initiate the verification),
    - initiate verification for all target email addresses that are provided for receiving the forwarded emails.
    '''

    def __init__(
        self,
        parent: constructs.Construct,
        name: builtins.str,
        *,
        email_forwarding_props: typing.Sequence[EmailForwardingProps],
        enable_rule_set: typing.Optional[builtins.bool] = None,
        rule_set: typing.Optional[aws_cdk.aws_ses.IReceiptRuleSet] = None,
        rule_set_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param parent: -
        :param name: -
        :param email_forwarding_props: A list of mapping options to define how emails should be forwarded.
        :param enable_rule_set: Optional: whether to enable the rule set or not. Default: true
        :param rule_set: Optional: an existing SES receipt rule set. If none is provided, a new one will be created using the name provided with ``ruleSetName`` or a default one.
        :param rule_set_name: Optional: provide a name for the receipt rule set that this construct creates if you don't provide one. Default: custom-rule-set
        '''
        props = EmailForwardingRuleSetProps(
            email_forwarding_props=email_forwarding_props,
            enable_rule_set=enable_rule_set,
            rule_set=rule_set,
            rule_set_name=rule_set_name,
        )

        jsii.create(self.__class__, self, [parent, name, props])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="emailForwardingMappings")
    def email_forwarding_mappings(self) -> typing.List[typing.Any]:
        return typing.cast(typing.List[typing.Any], jsii.get(self, "emailForwardingMappings"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="ruleSet")
    def rule_set(self) -> aws_cdk.aws_ses.IReceiptRuleSet:
        return typing.cast(aws_cdk.aws_ses.IReceiptRuleSet, jsii.get(self, "ruleSet"))


@jsii.data_type(
    jsii_type="@seeebiii/ses-email-forwarding.EmailForwardingRuleSetProps",
    jsii_struct_bases=[],
    name_mapping={
        "email_forwarding_props": "emailForwardingProps",
        "enable_rule_set": "enableRuleSet",
        "rule_set": "ruleSet",
        "rule_set_name": "ruleSetName",
    },
)
class EmailForwardingRuleSetProps:
    def __init__(
        self,
        *,
        email_forwarding_props: typing.Sequence[EmailForwardingProps],
        enable_rule_set: typing.Optional[builtins.bool] = None,
        rule_set: typing.Optional[aws_cdk.aws_ses.IReceiptRuleSet] = None,
        rule_set_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param email_forwarding_props: A list of mapping options to define how emails should be forwarded.
        :param enable_rule_set: Optional: whether to enable the rule set or not. Default: true
        :param rule_set: Optional: an existing SES receipt rule set. If none is provided, a new one will be created using the name provided with ``ruleSetName`` or a default one.
        :param rule_set_name: Optional: provide a name for the receipt rule set that this construct creates if you don't provide one. Default: custom-rule-set
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "email_forwarding_props": email_forwarding_props,
        }
        if enable_rule_set is not None:
            self._values["enable_rule_set"] = enable_rule_set
        if rule_set is not None:
            self._values["rule_set"] = rule_set
        if rule_set_name is not None:
            self._values["rule_set_name"] = rule_set_name

    @builtins.property
    def email_forwarding_props(self) -> typing.List[EmailForwardingProps]:
        '''A list of mapping options to define how emails should be forwarded.'''
        result = self._values.get("email_forwarding_props")
        assert result is not None, "Required property 'email_forwarding_props' is missing"
        return typing.cast(typing.List[EmailForwardingProps], result)

    @builtins.property
    def enable_rule_set(self) -> typing.Optional[builtins.bool]:
        '''Optional: whether to enable the rule set or not.

        :default: true
        '''
        result = self._values.get("enable_rule_set")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def rule_set(self) -> typing.Optional[aws_cdk.aws_ses.IReceiptRuleSet]:
        '''Optional: an existing SES receipt rule set.

        If none is provided, a new one will be created using the name provided with ``ruleSetName`` or a default one.
        '''
        result = self._values.get("rule_set")
        return typing.cast(typing.Optional[aws_cdk.aws_ses.IReceiptRuleSet], result)

    @builtins.property
    def rule_set_name(self) -> typing.Optional[builtins.str]:
        '''Optional: provide a name for the receipt rule set that this construct creates if you don't provide one.

        :default: custom-rule-set
        '''
        result = self._values.get("rule_set_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EmailForwardingRuleSetProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@seeebiii/ses-email-forwarding.EmailMapping",
    jsii_struct_bases=[],
    name_mapping={
        "target_emails": "targetEmails",
        "receive_email": "receiveEmail",
        "receive_prefix": "receivePrefix",
    },
)
class EmailMapping:
    def __init__(
        self,
        *,
        target_emails: typing.Sequence[builtins.str],
        receive_email: typing.Optional[builtins.str] = None,
        receive_prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param target_emails: A list of target email addresses that should receive the forwarded emails for the given email addresses matched by either ``receiveEmail`` or ``receivePrefix``. Make sure that you only specify email addresses that are verified by SES. Otherwise SES won't send them out. Example: ``['foobar@gmail.com', 'foo+bar@gmail.com', 'whatever@example.org']``
        :param receive_email: You can define a string that is matching an email address, e.g. ``hello@example.org``. If this property is defined, the ``receivePrefix`` will be ignored. You must define either this property or ``receivePrefix``, otherwise no emails will be forwarded.
        :param receive_prefix: A short way to match a specific email addresses by only providing a prefix, e.g. ``hello``. The prefix will be combined with the given domain name from {@link EmailForwardingRuleProps}. If an email was sent to this specific email address, all emails matching this receiver will be forwarded to all email addresses defined in ``targetEmails``. If ``receiveEmail`` property is defined as well, then ``receiveEmail`` is preferred. Hence, only define one of them.
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "target_emails": target_emails,
        }
        if receive_email is not None:
            self._values["receive_email"] = receive_email
        if receive_prefix is not None:
            self._values["receive_prefix"] = receive_prefix

    @builtins.property
    def target_emails(self) -> typing.List[builtins.str]:
        '''A list of target email addresses that should receive the forwarded emails for the given email addresses matched by either ``receiveEmail`` or ``receivePrefix``.

        Make sure that you only specify email addresses that are verified by SES. Otherwise SES won't send them out.

        Example: ``['foobar@gmail.com', 'foo+bar@gmail.com', 'whatever@example.org']``
        '''
        result = self._values.get("target_emails")
        assert result is not None, "Required property 'target_emails' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def receive_email(self) -> typing.Optional[builtins.str]:
        '''You can define a string that is matching an email address, e.g. ``hello@example.org``.

        If this property is defined, the ``receivePrefix`` will be ignored. You must define either this property or ``receivePrefix``, otherwise no emails will be forwarded.
        '''
        result = self._values.get("receive_email")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def receive_prefix(self) -> typing.Optional[builtins.str]:
        '''A short way to match a specific email addresses by only providing a prefix, e.g. ``hello``. The prefix will be combined with the given domain name from {@link EmailForwardingRuleProps}. If an email was sent to this specific email address, all emails matching this receiver will be forwarded to all email addresses defined in ``targetEmails``.

        If ``receiveEmail`` property is defined as well, then ``receiveEmail`` is preferred. Hence, only define one of them.
        '''
        result = self._values.get("receive_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EmailMapping(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "EmailForwardingProps",
    "EmailForwardingRule",
    "EmailForwardingRuleProps",
    "EmailForwardingRuleSet",
    "EmailForwardingRuleSetProps",
    "EmailMapping",
]

publication.publish()

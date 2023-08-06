'''
# shady-island

[![Apache 2.0](https://img.shields.io/github/license/libreworks/shady-island)](https://github.com/libreworks/shady-island/blob/main/LICENSE)
[![npm](https://img.shields.io/npm/v/shady-island)](https://www.npmjs.com/package/shady-island)
[![GitHub Workflow Status (branch)](https://img.shields.io/github/workflow/status/libreworks/shady-island/release/main?label=release)](https://github.com/libreworks/shady-island/actions/workflows/release.yml)
[![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/libreworks/shady-island?sort=semver)](https://github.com/libreworks/shady-island/releases)
[![codecov](https://codecov.io/gh/libreworks/shady-island/branch/main/graph/badge.svg?token=OHTRGNTSPO)](https://codecov.io/gh/libreworks/shady-island)

Utilities and constructs for the AWS CDK.

## Features

* Create IPv6 CIDRs and routes for subnets in a VPC with the `CidrContext` construct.
* Set the `AssignIpv6AddressOnCreation` property of subnets in a VPC with the `AssignOnLaunch` construct.

## Documentation

* [TypeScript API Reference](https://libreworks.github.io/shady-island/api/API.html)
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

import aws_cdk
import aws_cdk.aws_ec2
import aws_cdk.aws_kms
import aws_cdk.aws_logs
import constructs


@jsii.data_type(
    jsii_type="shady-island.AssignOnLaunchProps",
    jsii_struct_bases=[],
    name_mapping={"vpc": "vpc", "vpc_subnets": "vpcSubnets"},
)
class AssignOnLaunchProps:
    def __init__(
        self,
        *,
        vpc: aws_cdk.aws_ec2.IVpc,
        vpc_subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection] = None,
    ) -> None:
        '''(experimental) Properties for creating a new {@link AssignOnLaunch}.

        :param vpc: (experimental) The VPC whose subnets will be configured.
        :param vpc_subnets: (experimental) Which subnets to assign IPv6 addresses upon ENI creation.

        :stability: experimental
        '''
        if isinstance(vpc_subnets, dict):
            vpc_subnets = aws_cdk.aws_ec2.SubnetSelection(**vpc_subnets)
        self._values: typing.Dict[str, typing.Any] = {
            "vpc": vpc,
        }
        if vpc_subnets is not None:
            self._values["vpc_subnets"] = vpc_subnets

    @builtins.property
    def vpc(self) -> aws_cdk.aws_ec2.IVpc:
        '''(experimental) The VPC whose subnets will be configured.

        :stability: experimental
        '''
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(aws_cdk.aws_ec2.IVpc, result)

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[aws_cdk.aws_ec2.SubnetSelection]:
        '''(experimental) Which subnets to assign IPv6 addresses upon ENI creation.

        :stability: experimental
        '''
        result = self._values.get("vpc_subnets")
        return typing.cast(typing.Optional[aws_cdk.aws_ec2.SubnetSelection], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AssignOnLaunchProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="shady-island.CidrContextProps",
    jsii_struct_bases=[],
    name_mapping={
        "vpc": "vpc",
        "address_pool": "addressPool",
        "assign_address_on_launch": "assignAddressOnLaunch",
        "cidr_block": "cidrBlock",
        "cidr_count": "cidrCount",
    },
)
class CidrContextProps:
    def __init__(
        self,
        *,
        vpc: aws_cdk.aws_ec2.IVpc,
        address_pool: typing.Optional[builtins.str] = None,
        assign_address_on_launch: typing.Optional[builtins.bool] = None,
        cidr_block: typing.Optional[builtins.str] = None,
        cidr_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(experimental) Properties for creating a new {@link CidrContext}.

        :param vpc: (experimental) The VPC whose subnets will be configured.
        :param address_pool: (experimental) The ID of a BYOIP IPv6 address pool from which to allocate the CIDR block. If this parameter is not specified or is undefined, the CIDR block will be provided by AWS.
        :param assign_address_on_launch: (experimental) Whether this VPC should auto-assign an IPv6 address to launched ENIs. True by default.
        :param cidr_block: (experimental) An IPv6 CIDR block from the IPv6 address pool to use for this VPC. The {@link EnableIpv6Props#addressPool} attribute is required if this parameter is specified.
        :param cidr_count: (experimental) Split the CIDRs into this many groups (by default one for each subnet).

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "vpc": vpc,
        }
        if address_pool is not None:
            self._values["address_pool"] = address_pool
        if assign_address_on_launch is not None:
            self._values["assign_address_on_launch"] = assign_address_on_launch
        if cidr_block is not None:
            self._values["cidr_block"] = cidr_block
        if cidr_count is not None:
            self._values["cidr_count"] = cidr_count

    @builtins.property
    def vpc(self) -> aws_cdk.aws_ec2.IVpc:
        '''(experimental) The VPC whose subnets will be configured.

        :stability: experimental
        '''
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(aws_cdk.aws_ec2.IVpc, result)

    @builtins.property
    def address_pool(self) -> typing.Optional[builtins.str]:
        '''(experimental) The ID of a BYOIP IPv6 address pool from which to allocate the CIDR block.

        If this parameter is not specified or is undefined, the CIDR block will be
        provided by AWS.

        :stability: experimental
        '''
        result = self._values.get("address_pool")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def assign_address_on_launch(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether this VPC should auto-assign an IPv6 address to launched ENIs.

        True by default.

        :stability: experimental
        '''
        result = self._values.get("assign_address_on_launch")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def cidr_block(self) -> typing.Optional[builtins.str]:
        '''(experimental) An IPv6 CIDR block from the IPv6 address pool to use for this VPC.

        The {@link EnableIpv6Props#addressPool} attribute is required if this
        parameter is specified.

        :stability: experimental
        '''
        result = self._values.get("cidr_block")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cidr_count(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Split the CIDRs into this many groups (by default one for each subnet).

        :stability: experimental
        '''
        result = self._values.get("cidr_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CidrContextProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="shady-island.EncryptedLogGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "log_group_name": "logGroupName",
        "encryption_key": "encryptionKey",
        "removal_policy": "removalPolicy",
        "retention": "retention",
    },
)
class EncryptedLogGroupProps:
    def __init__(
        self,
        *,
        log_group_name: builtins.str,
        encryption_key: typing.Optional[aws_cdk.aws_kms.IKey] = None,
        removal_policy: typing.Optional[aws_cdk.RemovalPolicy] = None,
        retention: typing.Optional[aws_cdk.aws_logs.RetentionDays] = None,
    ) -> None:
        '''(experimental) Constructor properties for EncryptedLogGroup.

        :param log_group_name: (experimental) Name of the log group. We need a log group name ahead of time because otherwise the key policy would create a cyclical dependency.
        :param encryption_key: (experimental) The KMS Key to encrypt the log group with. Default: A new KMS key will be created
        :param removal_policy: (experimental) Whether the key and group should be retained when they are removed from the Stack. Default: RemovalPolicy.RETAIN
        :param retention: (experimental) How long, in days, the log contents will be retained. Default: RetentionDays.TWO_YEARS

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "log_group_name": log_group_name,
        }
        if encryption_key is not None:
            self._values["encryption_key"] = encryption_key
        if removal_policy is not None:
            self._values["removal_policy"] = removal_policy
        if retention is not None:
            self._values["retention"] = retention

    @builtins.property
    def log_group_name(self) -> builtins.str:
        '''(experimental) Name of the log group.

        We need a log group name ahead of time because otherwise the key policy
        would create a cyclical dependency.

        :stability: experimental
        '''
        result = self._values.get("log_group_name")
        assert result is not None, "Required property 'log_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def encryption_key(self) -> typing.Optional[aws_cdk.aws_kms.IKey]:
        '''(experimental) The KMS Key to encrypt the log group with.

        :default: A new KMS key will be created

        :stability: experimental
        '''
        result = self._values.get("encryption_key")
        return typing.cast(typing.Optional[aws_cdk.aws_kms.IKey], result)

    @builtins.property
    def removal_policy(self) -> typing.Optional[aws_cdk.RemovalPolicy]:
        '''(experimental) Whether the key and group should be retained when they are removed from the Stack.

        :default: RemovalPolicy.RETAIN

        :stability: experimental
        '''
        result = self._values.get("removal_policy")
        return typing.cast(typing.Optional[aws_cdk.RemovalPolicy], result)

    @builtins.property
    def retention(self) -> typing.Optional[aws_cdk.aws_logs.RetentionDays]:
        '''(experimental) How long, in days, the log contents will be retained.

        :default: RetentionDays.TWO_YEARS

        :stability: experimental
        '''
        result = self._values.get("retention")
        return typing.cast(typing.Optional[aws_cdk.aws_logs.RetentionDays], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EncryptedLogGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="shady-island.IAssignOnLaunch")
class IAssignOnLaunch(typing_extensions.Protocol):
    '''(experimental) Interface for the AssignOnLaunch class.

    :stability: experimental
    '''

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> aws_cdk.aws_ec2.IVpc:
        '''(experimental) The IPv6-enabled VPC.

        :stability: experimental
        '''
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="vpcPlacement")
    def vpc_placement(self) -> aws_cdk.aws_ec2.SelectedSubnets:
        '''(experimental) The chosen subnets for address assignment on ENI launch.

        :stability: experimental
        '''
        ...


class _IAssignOnLaunchProxy:
    '''(experimental) Interface for the AssignOnLaunch class.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "shady-island.IAssignOnLaunch"

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> aws_cdk.aws_ec2.IVpc:
        '''(experimental) The IPv6-enabled VPC.

        :stability: experimental
        '''
        return typing.cast(aws_cdk.aws_ec2.IVpc, jsii.get(self, "vpc"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="vpcPlacement")
    def vpc_placement(self) -> aws_cdk.aws_ec2.SelectedSubnets:
        '''(experimental) The chosen subnets for address assignment on ENI launch.

        :stability: experimental
        '''
        return typing.cast(aws_cdk.aws_ec2.SelectedSubnets, jsii.get(self, "vpcPlacement"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IAssignOnLaunch).__jsii_proxy_class__ = lambda : _IAssignOnLaunchProxy


@jsii.interface(jsii_type="shady-island.ICidrContext")
class ICidrContext(typing_extensions.Protocol):
    '''(experimental) Interface for the CidrContext class.

    :stability: experimental
    '''

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> aws_cdk.aws_ec2.IVpc:
        '''(experimental) The IPv6-enabled VPC.

        :stability: experimental
        '''
        ...


class _ICidrContextProxy:
    '''(experimental) Interface for the CidrContext class.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "shady-island.ICidrContext"

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> aws_cdk.aws_ec2.IVpc:
        '''(experimental) The IPv6-enabled VPC.

        :stability: experimental
        '''
        return typing.cast(aws_cdk.aws_ec2.IVpc, jsii.get(self, "vpc"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ICidrContext).__jsii_proxy_class__ = lambda : _ICidrContextProxy


@jsii.interface(jsii_type="shady-island.IEncryptedLogGroup")
class IEncryptedLogGroup(typing_extensions.Protocol):
    '''(experimental) A log group encrypted by a KMS customer managed key.

    :stability: experimental
    '''

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="key")
    def key(self) -> aws_cdk.aws_kms.IKey:
        '''(experimental) The KMS encryption key.

        :stability: experimental
        '''
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="logGroup")
    def log_group(self) -> aws_cdk.aws_logs.ILogGroup:
        '''(experimental) The log group.

        :stability: experimental
        '''
        ...


class _IEncryptedLogGroupProxy:
    '''(experimental) A log group encrypted by a KMS customer managed key.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "shady-island.IEncryptedLogGroup"

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="key")
    def key(self) -> aws_cdk.aws_kms.IKey:
        '''(experimental) The KMS encryption key.

        :stability: experimental
        '''
        return typing.cast(aws_cdk.aws_kms.IKey, jsii.get(self, "key"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="logGroup")
    def log_group(self) -> aws_cdk.aws_logs.ILogGroup:
        '''(experimental) The log group.

        :stability: experimental
        '''
        return typing.cast(aws_cdk.aws_logs.ILogGroup, jsii.get(self, "logGroup"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IEncryptedLogGroup).__jsii_proxy_class__ = lambda : _IEncryptedLogGroupProxy


class Tier(metaclass=jsii.JSIIMeta, jsii_type="shady-island.Tier"):
    '''(experimental) A deployment environment with a specific purpose and audience.

    You can create any Tier you like, but we include those explained by DTAP.

    :see: https://en.wikipedia.org/wiki/Development,_testing,_acceptance_and_production
    :stability: experimental
    '''

    def __init__(self, id: builtins.str, label: builtins.str) -> None:
        '''(experimental) Creates a new Tier.

        :param id: - The machine-readable identifier for this tier (e.g. prod).
        :param label: - The human-readable label for this tier (e.g. Production).

        :stability: experimental
        '''
        jsii.create(self.__class__, self, [id, label])

    @jsii.member(jsii_name="applyTags")
    def apply_tags(self, construct: constructs.IConstruct) -> None:
        '''(experimental) Adds the label of this tier as a tag to the provided construct.

        :param construct: -

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "applyTags", [construct]))

    @jsii.member(jsii_name="matches")
    def matches(self, other: "Tier") -> builtins.bool:
        '''(experimental) Compares this tier to the provided value and tests for equality.

        :param other: - The value to compare.

        :return: Whether the provided value is equal to this tier.

        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.invoke(self, "matches", [other]))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="ACCEPTANCE")
    def ACCEPTANCE(cls) -> "Tier":
        '''(experimental) A tier that represents an acceptance environment.

        :stability: experimental
        '''
        return typing.cast("Tier", jsii.sget(cls, "ACCEPTANCE"))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="DEVELOPMENT")
    def DEVELOPMENT(cls) -> "Tier":
        '''(experimental) A tier that represents a development environment.

        :stability: experimental
        '''
        return typing.cast("Tier", jsii.sget(cls, "DEVELOPMENT"))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="PRODUCTION")
    def PRODUCTION(cls) -> "Tier":
        '''(experimental) A tier that represents a production environment.

        :stability: experimental
        '''
        return typing.cast("Tier", jsii.sget(cls, "PRODUCTION"))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="TESTING")
    def TESTING(cls) -> "Tier":
        '''(experimental) A tier that represents a testing environment.

        :stability: experimental
        '''
        return typing.cast("Tier", jsii.sget(cls, "TESTING"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        '''(experimental) The machine-readable identifier for this tier (e.g. prod).

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="label")
    def label(self) -> builtins.str:
        '''(experimental) The human-readable label for this tier (e.g. Production).

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "label"))


class Workload(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="shady-island.Workload",
):
    '''(experimental) A collection of Stacks in an Environment representing a deployment Tier.

    Derive a subclass of ``Workload`` and create your stacks within.

    The difference between this object and a ``Stage`` is that a ``Stage`` is meant
    to be deployed with CDK Pipelines. This class can be used with ``cdk deploy``.
    This class also provides context loading capabilities.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        tier: Tier,
        base_domain_name: typing.Optional[builtins.str] = None,
        context_file: typing.Optional[builtins.str] = None,
        env: typing.Optional[aws_cdk.Environment] = None,
        workload_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Creates a new Workload.

        :param scope: - The construct scope.
        :param id: - The construct ID.
        :param tier: (experimental) The deployment tier.
        :param base_domain_name: (experimental) The base domain name used to create the FQDN for public resources.
        :param context_file: (experimental) The filesystem path to a JSON file that contains context values to load. Using this property allows you to load different context values within each instantiated ``Workload``, directly from a file you can check into source control.
        :param env: (experimental) The AWS environment (account/region) where this stack will be deployed.
        :param workload_name: (experimental) The machine identifier for this workload. This value will be used to create the ``publicDomainName`` property. By default, the ``stackName`` property used to create ``Stack`` constructs in the ``createStack`` method will begin with this Workload's ``workloadName`` and its ``tier`` separated by hyphens. Consider providing a constant ``workloadName`` value to the superclass constructor in your derived class. Default: - The id passed to the ``Workload`` constructor, but in lowercase

        :stability: experimental
        '''
        props = WorkloadProps(
            tier=tier,
            base_domain_name=base_domain_name,
            context_file=context_file,
            env=env,
            workload_name=workload_name,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="isWorkload") # type: ignore[misc]
    @builtins.classmethod
    def is_workload(cls, x: typing.Any) -> builtins.bool:
        '''(experimental) Test whether the given construct is a Workload.

        :param x: - The value to test.

        :return: Whether the value is a Workload object.

        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isWorkload", [x]))

    @jsii.member(jsii_name="of") # type: ignore[misc]
    @builtins.classmethod
    def of(cls, construct: constructs.IConstruct) -> "Workload":
        '''(experimental) Return the Workload the construct is contained within, fails if there is no workload up the tree.

        :param construct: - The construct whose parent nodes will be searched.

        :return: The Workload containing the construct

        :stability: experimental
        :throws: Error - if none of the construct's parents are a workload
        '''
        return typing.cast("Workload", jsii.sinvoke(cls, "of", [construct]))

    @jsii.member(jsii_name="createStack")
    def create_stack(
        self,
        id: builtins.str,
        *,
        analytics_reporting: typing.Optional[builtins.bool] = None,
        description: typing.Optional[builtins.str] = None,
        env: typing.Optional[aws_cdk.Environment] = None,
        stack_name: typing.Optional[builtins.str] = None,
        synthesizer: typing.Optional[aws_cdk.IStackSynthesizer] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        termination_protection: typing.Optional[builtins.bool] = None,
    ) -> aws_cdk.Stack:
        '''(experimental) Adds a stack to the Workload.

        This method will return a ``Stack`` with this Workload as its scope. By
        default, the ``stackName`` property provided to the ``Stack`` will be this
        Workload's ``workloadName``, its ``tier``, and the value of the ``id``
        parameter separated by hyphens, all in lowercase.

        :param id: - The Stack construct id (e.g. "Network").
        :param analytics_reporting: Include runtime versioning information in this Stack. Default: ``analyticsReporting`` setting of containing ``App``, or value of 'aws:cdk:version-reporting' context key
        :param description: A description of the stack. Default: - No description.
        :param env: The AWS environment (account/region) where this stack will be deployed. Set the ``region``/``account`` fields of ``env`` to either a concrete value to select the indicated environment (recommended for production stacks), or to the values of environment variables ``CDK_DEFAULT_REGION``/``CDK_DEFAULT_ACCOUNT`` to let the target environment depend on the AWS credentials/configuration that the CDK CLI is executed under (recommended for development stacks). If the ``Stack`` is instantiated inside a ``Stage``, any undefined ``region``/``account`` fields from ``env`` will default to the same field on the encompassing ``Stage``, if configured there. If either ``region`` or ``account`` are not set nor inherited from ``Stage``, the Stack will be considered "*environment-agnostic*"". Environment-agnostic stacks can be deployed to any environment but may not be able to take advantage of all features of the CDK. For example, they will not be able to use environmental context lookups such as ``ec2.Vpc.fromLookup`` and will not automatically translate Service Principals to the right format based on the environment's AWS partition, and other such enhancements. Default: - The environment of the containing ``Stage`` if available, otherwise create the stack will be environment-agnostic.
        :param stack_name: Name to deploy the stack with. Default: - Derived from construct path.
        :param synthesizer: Synthesis method to use while deploying this stack. Default: - ``DefaultStackSynthesizer`` if the ``@aws-cdk/core:newStyleStackSynthesis`` feature flag is set, ``LegacyStackSynthesizer`` otherwise.
        :param tags: Stack tags that will be applied to all the taggable resources and the stack itself. Default: {}
        :param termination_protection: Whether to enable termination protection for this stack. Default: false

        :stability: experimental

        Example::

            const exampleDev = new Workload(app, 'Example', {
              tier: Tier.DEVELOPMENT,
              env: { account: '123456789012', region: 'us-east-1' },
            });
            const networkStack = exampleDev.createStack('Network', {});
            assert.strictEqual(networkStack.stackName, 'example-dev-network').
            
            You can override the `env` and `stackName` properties in the `props`
            argument if desired.
        '''
        props = aws_cdk.StackProps(
            analytics_reporting=analytics_reporting,
            description=description,
            env=env,
            stack_name=stack_name,
            synthesizer=synthesizer,
            tags=tags,
            termination_protection=termination_protection,
        )

        return typing.cast(aws_cdk.Stack, jsii.invoke(self, "createStack", [id, props]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="stacks")
    def stacks(self) -> typing.List[aws_cdk.Stack]:
        '''
        :return: The stacks created by invoking ``createStack``

        :stability: experimental
        '''
        return typing.cast(typing.List[aws_cdk.Stack], jsii.get(self, "stacks"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tier")
    def tier(self) -> Tier:
        '''(experimental) The deployment tier.

        :stability: experimental
        '''
        return typing.cast(Tier, jsii.get(self, "tier"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="workloadName")
    def workload_name(self) -> builtins.str:
        '''(experimental) The prefix used in the default ``stackName`` provided to child Stacks.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "workloadName"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="account")
    def account(self) -> typing.Optional[builtins.str]:
        '''(experimental) The default account for all resources defined within this workload.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "account"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="publicDomainName")
    def public_domain_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The domain name to use for resources that expose public endpoints.

        You can use ``Workload.of(this).publicDomainName`` as the ``zoneName`` of a
        Route 53 hosted zone.

        Any construct that creates public DNS resources (e.g. those of API Gateway,
        Application Load Balancing, CloudFront) can use this property to format
        a FQDN for itself by adding a subdomain.

        :default: - If ``baseDomainName`` was empty, this will be ``undefined``

        :stability: experimental

        Example::

            const app = new App();
            const workload = new Workload(app, "Foobar", {
              tier: Tier.PRODUCTION,
              baseDomainName: 'example.com'
            });
            assert.strictEqual(workload.publicDomainName, 'prod.foobar.example.com');
            const stack = workload.createStack("DNS");
            const hostedZone = new HostedZone(stack, "HostedZone", {
              zoneName: `${workload.publicDomainName}`
            });
            const api = new RestApi(stack, "API", {
              restApiName: "foobar",
              domainName: { domainName: `api.${workload.publicDomainName}` },
            });
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "publicDomainName"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="region")
    def region(self) -> typing.Optional[builtins.str]:
        '''(experimental) The default region for all resources defined within this workload.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "region"))


@jsii.data_type(
    jsii_type="shady-island.WorkloadProps",
    jsii_struct_bases=[],
    name_mapping={
        "tier": "tier",
        "base_domain_name": "baseDomainName",
        "context_file": "contextFile",
        "env": "env",
        "workload_name": "workloadName",
    },
)
class WorkloadProps:
    def __init__(
        self,
        *,
        tier: Tier,
        base_domain_name: typing.Optional[builtins.str] = None,
        context_file: typing.Optional[builtins.str] = None,
        env: typing.Optional[aws_cdk.Environment] = None,
        workload_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Constructor properties for a Workload.

        :param tier: (experimental) The deployment tier.
        :param base_domain_name: (experimental) The base domain name used to create the FQDN for public resources.
        :param context_file: (experimental) The filesystem path to a JSON file that contains context values to load. Using this property allows you to load different context values within each instantiated ``Workload``, directly from a file you can check into source control.
        :param env: (experimental) The AWS environment (account/region) where this stack will be deployed.
        :param workload_name: (experimental) The machine identifier for this workload. This value will be used to create the ``publicDomainName`` property. By default, the ``stackName`` property used to create ``Stack`` constructs in the ``createStack`` method will begin with this Workload's ``workloadName`` and its ``tier`` separated by hyphens. Consider providing a constant ``workloadName`` value to the superclass constructor in your derived class. Default: - The id passed to the ``Workload`` constructor, but in lowercase

        :stability: experimental
        '''
        if isinstance(env, dict):
            env = aws_cdk.Environment(**env)
        self._values: typing.Dict[str, typing.Any] = {
            "tier": tier,
        }
        if base_domain_name is not None:
            self._values["base_domain_name"] = base_domain_name
        if context_file is not None:
            self._values["context_file"] = context_file
        if env is not None:
            self._values["env"] = env
        if workload_name is not None:
            self._values["workload_name"] = workload_name

    @builtins.property
    def tier(self) -> Tier:
        '''(experimental) The deployment tier.

        :stability: experimental
        '''
        result = self._values.get("tier")
        assert result is not None, "Required property 'tier' is missing"
        return typing.cast(Tier, result)

    @builtins.property
    def base_domain_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The base domain name used to create the FQDN for public resources.

        :stability: experimental
        '''
        result = self._values.get("base_domain_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def context_file(self) -> typing.Optional[builtins.str]:
        '''(experimental) The filesystem path to a JSON file that contains context values to load.

        Using this property allows you to load different context values within each
        instantiated ``Workload``, directly from a file you can check into source
        control.

        :stability: experimental
        '''
        result = self._values.get("context_file")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def env(self) -> typing.Optional[aws_cdk.Environment]:
        '''(experimental) The AWS environment (account/region) where this stack will be deployed.

        :stability: experimental
        '''
        result = self._values.get("env")
        return typing.cast(typing.Optional[aws_cdk.Environment], result)

    @builtins.property
    def workload_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The machine identifier for this workload.

        This value will be used to create the ``publicDomainName`` property.

        By default, the ``stackName`` property used to create ``Stack`` constructs in
        the ``createStack`` method will begin with this Workload's ``workloadName`` and
        its ``tier`` separated by hyphens.

        Consider providing a constant ``workloadName`` value to the superclass
        constructor in your derived class.

        :default: - The id passed to the ``Workload`` constructor, but in lowercase

        :stability: experimental

        Example::

            class MyWorkload extends Workload {
              constructor(scope: Construct, id: string, props: WorkloadProps) {
                super(scope, id, { ...props, workloadName: 'my-workload' });
              }
            }
        '''
        result = self._values.get("workload_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkloadProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IAssignOnLaunch)
class AssignOnLaunch(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="shady-island.AssignOnLaunch",
):
    '''(experimental) Enables the "assignIpv6AddressOnCreation" attribute on selected subnets.

    :see: {@link https://github.com/aws/aws-cdk/issues/5927}
    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        vpc: aws_cdk.aws_ec2.IVpc,
        vpc_subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection] = None,
    ) -> None:
        '''(experimental) Creates a new BetterVpc.

        :param scope: - The construct scope.
        :param id: - The construct ID.
        :param vpc: (experimental) The VPC whose subnets will be configured.
        :param vpc_subnets: (experimental) Which subnets to assign IPv6 addresses upon ENI creation.

        :stability: experimental
        '''
        options = AssignOnLaunchProps(vpc=vpc, vpc_subnets=vpc_subnets)

        jsii.create(self.__class__, self, [scope, id, options])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> aws_cdk.aws_ec2.IVpc:
        '''(experimental) The IPv6-enabled VPC.

        :stability: experimental
        '''
        return typing.cast(aws_cdk.aws_ec2.IVpc, jsii.get(self, "vpc"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="vpcPlacement")
    def vpc_placement(self) -> aws_cdk.aws_ec2.SelectedSubnets:
        '''(experimental) The chosen subnets for address assignment on ENI launch.

        :stability: experimental
        '''
        return typing.cast(aws_cdk.aws_ec2.SelectedSubnets, jsii.get(self, "vpcPlacement"))


@jsii.implements(ICidrContext)
class CidrContext(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="shady-island.CidrContext",
):
    '''(experimental) Allocates IPv6 CIDRs and routes for subnets in a VPC.

    :see: {@link https://github.com/aws/aws-cdk/issues/5927}
    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        vpc: aws_cdk.aws_ec2.IVpc,
        address_pool: typing.Optional[builtins.str] = None,
        assign_address_on_launch: typing.Optional[builtins.bool] = None,
        cidr_block: typing.Optional[builtins.str] = None,
        cidr_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(experimental) Creates a new BetterVpc.

        :param scope: - The construct scope.
        :param id: - The construct ID.
        :param vpc: (experimental) The VPC whose subnets will be configured.
        :param address_pool: (experimental) The ID of a BYOIP IPv6 address pool from which to allocate the CIDR block. If this parameter is not specified or is undefined, the CIDR block will be provided by AWS.
        :param assign_address_on_launch: (experimental) Whether this VPC should auto-assign an IPv6 address to launched ENIs. True by default.
        :param cidr_block: (experimental) An IPv6 CIDR block from the IPv6 address pool to use for this VPC. The {@link EnableIpv6Props#addressPool} attribute is required if this parameter is specified.
        :param cidr_count: (experimental) Split the CIDRs into this many groups (by default one for each subnet).

        :stability: experimental
        '''
        options = CidrContextProps(
            vpc=vpc,
            address_pool=address_pool,
            assign_address_on_launch=assign_address_on_launch,
            cidr_block=cidr_block,
            cidr_count=cidr_count,
        )

        jsii.create(self.__class__, self, [scope, id, options])

    @jsii.member(jsii_name="assignPrivateSubnetCidrs")
    def _assign_private_subnet_cidrs(
        self,
        vpc: aws_cdk.aws_ec2.IVpc,
        cidrs: typing.Sequence[builtins.str],
        cidr_block: aws_cdk.CfnResource,
    ) -> None:
        '''(experimental) Override the template;

        set the IPv6 CIDR for private subnets.

        :param vpc: - The VPC of the subnets.
        :param cidrs: - The possible IPv6 CIDRs to assign.
        :param cidr_block: - The CfnVPCCidrBlock the subnets depend on.

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "assignPrivateSubnetCidrs", [vpc, cidrs, cidr_block]))

    @jsii.member(jsii_name="assignPublicSubnetCidrs")
    def _assign_public_subnet_cidrs(
        self,
        vpc: aws_cdk.aws_ec2.IVpc,
        cidrs: typing.Sequence[builtins.str],
        cidr_block: aws_cdk.CfnResource,
    ) -> None:
        '''(experimental) Override the template;

        set the IPv6 CIDR for isolated subnets.

        :param vpc: - The VPC of the subnets.
        :param cidrs: - The possible IPv6 CIDRs to assign.
        :param cidr_block: - The CfnVPCCidrBlock the subnets depend on.

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "assignPublicSubnetCidrs", [vpc, cidrs, cidr_block]))

    @jsii.member(jsii_name="validateCidrCount")
    def _validate_cidr_count(
        self,
        vpc: aws_cdk.aws_ec2.IVpc,
        cidr_count: typing.Optional[jsii.Number] = None,
    ) -> jsii.Number:
        '''(experimental) Figure out the minimun required CIDR subnets and the number desired.

        :param vpc: - The VPC.
        :param cidr_count: - Optional. Divide the VPC CIDR into this many subsets.

        :stability: experimental
        '''
        return typing.cast(jsii.Number, jsii.invoke(self, "validateCidrCount", [vpc, cidr_count]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> aws_cdk.aws_ec2.IVpc:
        '''(experimental) The IPv6-enabled VPC.

        :stability: experimental
        '''
        return typing.cast(aws_cdk.aws_ec2.IVpc, jsii.get(self, "vpc"))


@jsii.implements(IEncryptedLogGroup)
class EncryptedLogGroup(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="shady-island.EncryptedLogGroup",
):
    '''(experimental) A log group encrypted by a KMS customer managed key.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        log_group_name: builtins.str,
        encryption_key: typing.Optional[aws_cdk.aws_kms.IKey] = None,
        removal_policy: typing.Optional[aws_cdk.RemovalPolicy] = None,
        retention: typing.Optional[aws_cdk.aws_logs.RetentionDays] = None,
    ) -> None:
        '''(experimental) Creates a new EncryptedLogGroup.

        :param scope: -
        :param id: -
        :param log_group_name: (experimental) Name of the log group. We need a log group name ahead of time because otherwise the key policy would create a cyclical dependency.
        :param encryption_key: (experimental) The KMS Key to encrypt the log group with. Default: A new KMS key will be created
        :param removal_policy: (experimental) Whether the key and group should be retained when they are removed from the Stack. Default: RemovalPolicy.RETAIN
        :param retention: (experimental) How long, in days, the log contents will be retained. Default: RetentionDays.TWO_YEARS

        :stability: experimental
        '''
        props = EncryptedLogGroupProps(
            log_group_name=log_group_name,
            encryption_key=encryption_key,
            removal_policy=removal_policy,
            retention=retention,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="key")
    def key(self) -> aws_cdk.aws_kms.IKey:
        '''(experimental) The KMS encryption key.

        :stability: experimental
        '''
        return typing.cast(aws_cdk.aws_kms.IKey, jsii.get(self, "key"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="logGroup")
    def log_group(self) -> aws_cdk.aws_logs.ILogGroup:
        '''(experimental) The log group.

        :stability: experimental
        '''
        return typing.cast(aws_cdk.aws_logs.ILogGroup, jsii.get(self, "logGroup"))


__all__ = [
    "AssignOnLaunch",
    "AssignOnLaunchProps",
    "CidrContext",
    "CidrContextProps",
    "EncryptedLogGroup",
    "EncryptedLogGroupProps",
    "IAssignOnLaunch",
    "ICidrContext",
    "IEncryptedLogGroup",
    "Tier",
    "Workload",
    "WorkloadProps",
]

publication.publish()

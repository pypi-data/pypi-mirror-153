'''
# cdk-library-control-tower-lifecycle-events

NOTE: This project is in active development.

This construct library contains events that represent lifecycle events in Control Tower or events related to actions in Control Tower. See the [API](API.md) for full details on the available constructs.

## References

* [Reference](https://github.com/aws/aws-cdk/issues/3235) for creating constructs that extend and existing one more easily
* [Control Tower Lifecycle Events](https://docs.aws.amazon.com/controltower/latest/userguide/lifecycle-events.html) AWS doc
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

import aws_cdk.aws_events
import constructs


@jsii.data_type(
    jsii_type="@renovosolutions/cdk-library-control-tower-lifecycle-events.BaseRuleProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "enabled": "enabled",
        "event_bus": "eventBus",
        "event_state": "eventState",
        "rule_name": "ruleName",
        "targets": "targets",
    },
)
class BaseRuleProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[builtins.bool] = None,
        event_bus: typing.Optional[aws_cdk.aws_events.IEventBus] = None,
        event_state: typing.Optional["EventStates"] = None,
        rule_name: typing.Optional[builtins.str] = None,
        targets: typing.Optional[typing.Sequence[aws_cdk.aws_events.IRuleTarget]] = None,
    ) -> None:
        '''
        :param description: A description of the rule's purpose. Default: - A rule for new account creation in Organizations
        :param enabled: Indicates whether the rule is enabled. Default: true
        :param event_bus: The event bus to associate with this rule. Default: - The default event bus.
        :param event_state: Which event state should this rule trigger for. Default: - EventStates.SUCCEEDED
        :param rule_name: A name for the rule. Default: - AWS CloudFormation generates a unique physical ID and uses that ID for the rule name. For more information, see Name Type.
        :param targets: Targets to invoke when this rule matches an event. Default: - No targets.
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if enabled is not None:
            self._values["enabled"] = enabled
        if event_bus is not None:
            self._values["event_bus"] = event_bus
        if event_state is not None:
            self._values["event_state"] = event_state
        if rule_name is not None:
            self._values["rule_name"] = rule_name
        if targets is not None:
            self._values["targets"] = targets

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the rule's purpose.

        :default: - A rule for new account creation in Organizations
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''Indicates whether the rule is enabled.

        :default: true
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def event_bus(self) -> typing.Optional[aws_cdk.aws_events.IEventBus]:
        '''The event bus to associate with this rule.

        :default: - The default event bus.
        '''
        result = self._values.get("event_bus")
        return typing.cast(typing.Optional[aws_cdk.aws_events.IEventBus], result)

    @builtins.property
    def event_state(self) -> typing.Optional["EventStates"]:
        '''Which event state should this rule trigger for.

        :default: - EventStates.SUCCEEDED
        '''
        result = self._values.get("event_state")
        return typing.cast(typing.Optional["EventStates"], result)

    @builtins.property
    def rule_name(self) -> typing.Optional[builtins.str]:
        '''A name for the rule.

        :default:

        - AWS CloudFormation generates a unique physical ID and uses that ID
        for the rule name. For more information, see Name Type.
        '''
        result = self._values.get("rule_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def targets(self) -> typing.Optional[typing.List[aws_cdk.aws_events.IRuleTarget]]:
        '''Targets to invoke when this rule matches an event.

        :default: - No targets.
        '''
        result = self._values.get("targets")
        return typing.cast(typing.Optional[typing.List[aws_cdk.aws_events.IRuleTarget]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BaseRuleProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CreatedAccountByOrganizationsRule(
    aws_cdk.aws_events.Rule,
    metaclass=jsii.JSIIMeta,
    jsii_type="@renovosolutions/cdk-library-control-tower-lifecycle-events.CreatedAccountByOrganizationsRule",
):
    '''A rule for matching events from CloudTrail where Organizations created a new account.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        description: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[builtins.bool] = None,
        event_bus: typing.Optional[aws_cdk.aws_events.IEventBus] = None,
        event_state: typing.Optional["EventStates"] = None,
        rule_name: typing.Optional[builtins.str] = None,
        targets: typing.Optional[typing.Sequence[aws_cdk.aws_events.IRuleTarget]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param description: A description of the rule's purpose. Default: - A rule for new account creation in Organizations
        :param enabled: Indicates whether the rule is enabled. Default: true
        :param event_bus: The event bus to associate with this rule. Default: - The default event bus.
        :param event_state: Which event state should this rule trigger for. Default: - EventStates.SUCCEEDED
        :param rule_name: A name for the rule. Default: - AWS CloudFormation generates a unique physical ID and uses that ID for the rule name. For more information, see Name Type.
        :param targets: Targets to invoke when this rule matches an event. Default: - No targets.
        '''
        props = BaseRuleProps(
            description=description,
            enabled=enabled,
            event_bus=event_bus,
            event_state=event_state,
            rule_name=rule_name,
            targets=targets,
        )

        jsii.create(self.__class__, self, [scope, id, props])


class CreatedAccountRule(
    aws_cdk.aws_events.Rule,
    metaclass=jsii.JSIIMeta,
    jsii_type="@renovosolutions/cdk-library-control-tower-lifecycle-events.CreatedAccountRule",
):
    '''A rule for matching events from CloudTrail where Control Tower created a new account.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        ou_id: typing.Optional[builtins.str] = None,
        ou_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[builtins.bool] = None,
        event_bus: typing.Optional[aws_cdk.aws_events.IEventBus] = None,
        event_state: typing.Optional["EventStates"] = None,
        rule_name: typing.Optional[builtins.str] = None,
        targets: typing.Optional[typing.Sequence[aws_cdk.aws_events.IRuleTarget]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param ou_id: The OU ID to match.
        :param ou_name: The OU name to match.
        :param description: A description of the rule's purpose. Default: - A rule for new account creation in Organizations
        :param enabled: Indicates whether the rule is enabled. Default: true
        :param event_bus: The event bus to associate with this rule. Default: - The default event bus.
        :param event_state: Which event state should this rule trigger for. Default: - EventStates.SUCCEEDED
        :param rule_name: A name for the rule. Default: - AWS CloudFormation generates a unique physical ID and uses that ID for the rule name. For more information, see Name Type.
        :param targets: Targets to invoke when this rule matches an event. Default: - No targets.
        '''
        props = OuRuleProps(
            ou_id=ou_id,
            ou_name=ou_name,
            description=description,
            enabled=enabled,
            event_bus=event_bus,
            event_state=event_state,
            rule_name=rule_name,
            targets=targets,
        )

        jsii.create(self.__class__, self, [scope, id, props])


class DeregisteredOrganizationalUnitRule(
    aws_cdk.aws_events.Rule,
    metaclass=jsii.JSIIMeta,
    jsii_type="@renovosolutions/cdk-library-control-tower-lifecycle-events.DeregisteredOrganizationalUnitRule",
):
    '''A rule for matching events from CloudTrail where Control Tower deregistered an Organizational Unit.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        ou_id: typing.Optional[builtins.str] = None,
        ou_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[builtins.bool] = None,
        event_bus: typing.Optional[aws_cdk.aws_events.IEventBus] = None,
        event_state: typing.Optional["EventStates"] = None,
        rule_name: typing.Optional[builtins.str] = None,
        targets: typing.Optional[typing.Sequence[aws_cdk.aws_events.IRuleTarget]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param ou_id: The OU ID to match.
        :param ou_name: The OU name to match.
        :param description: A description of the rule's purpose. Default: - A rule for new account creation in Organizations
        :param enabled: Indicates whether the rule is enabled. Default: true
        :param event_bus: The event bus to associate with this rule. Default: - The default event bus.
        :param event_state: Which event state should this rule trigger for. Default: - EventStates.SUCCEEDED
        :param rule_name: A name for the rule. Default: - AWS CloudFormation generates a unique physical ID and uses that ID for the rule name. For more information, see Name Type.
        :param targets: Targets to invoke when this rule matches an event. Default: - No targets.
        '''
        props = OuRuleProps(
            ou_id=ou_id,
            ou_name=ou_name,
            description=description,
            enabled=enabled,
            event_bus=event_bus,
            event_state=event_state,
            rule_name=rule_name,
            targets=targets,
        )

        jsii.create(self.__class__, self, [scope, id, props])


class DisabledGuardrailRule(
    aws_cdk.aws_events.Rule,
    metaclass=jsii.JSIIMeta,
    jsii_type="@renovosolutions/cdk-library-control-tower-lifecycle-events.DisabledGuardrailRule",
):
    '''A rule for matching events from CloudTrail where a guard rail was disabled via Control Tower for an Organizational Unit.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        guardrail_behavior: typing.Optional["GuardrailBehaviors"] = None,
        guardrail_id: typing.Optional[builtins.str] = None,
        ou_id: typing.Optional[builtins.str] = None,
        ou_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[builtins.bool] = None,
        event_bus: typing.Optional[aws_cdk.aws_events.IEventBus] = None,
        event_state: typing.Optional["EventStates"] = None,
        rule_name: typing.Optional[builtins.str] = None,
        targets: typing.Optional[typing.Sequence[aws_cdk.aws_events.IRuleTarget]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param guardrail_behavior: The guardrail behavior to match.
        :param guardrail_id: The guardrail ID to match.
        :param ou_id: The OU ID to match.
        :param ou_name: The OU name to match.
        :param description: A description of the rule's purpose. Default: - A rule for new account creation in Organizations
        :param enabled: Indicates whether the rule is enabled. Default: true
        :param event_bus: The event bus to associate with this rule. Default: - The default event bus.
        :param event_state: Which event state should this rule trigger for. Default: - EventStates.SUCCEEDED
        :param rule_name: A name for the rule. Default: - AWS CloudFormation generates a unique physical ID and uses that ID for the rule name. For more information, see Name Type.
        :param targets: Targets to invoke when this rule matches an event. Default: - No targets.
        '''
        props = GuardrailRuleProps(
            guardrail_behavior=guardrail_behavior,
            guardrail_id=guardrail_id,
            ou_id=ou_id,
            ou_name=ou_name,
            description=description,
            enabled=enabled,
            event_bus=event_bus,
            event_state=event_state,
            rule_name=rule_name,
            targets=targets,
        )

        jsii.create(self.__class__, self, [scope, id, props])


class EnabledGuardrailRule(
    aws_cdk.aws_events.Rule,
    metaclass=jsii.JSIIMeta,
    jsii_type="@renovosolutions/cdk-library-control-tower-lifecycle-events.EnabledGuardrailRule",
):
    '''A rule for matching events from CloudTrail where a guardrail was enabled via Control Tower for an Organizational Unit.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        guardrail_behavior: typing.Optional["GuardrailBehaviors"] = None,
        guardrail_id: typing.Optional[builtins.str] = None,
        ou_id: typing.Optional[builtins.str] = None,
        ou_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[builtins.bool] = None,
        event_bus: typing.Optional[aws_cdk.aws_events.IEventBus] = None,
        event_state: typing.Optional["EventStates"] = None,
        rule_name: typing.Optional[builtins.str] = None,
        targets: typing.Optional[typing.Sequence[aws_cdk.aws_events.IRuleTarget]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param guardrail_behavior: The guardrail behavior to match.
        :param guardrail_id: The guardrail ID to match.
        :param ou_id: The OU ID to match.
        :param ou_name: The OU name to match.
        :param description: A description of the rule's purpose. Default: - A rule for new account creation in Organizations
        :param enabled: Indicates whether the rule is enabled. Default: true
        :param event_bus: The event bus to associate with this rule. Default: - The default event bus.
        :param event_state: Which event state should this rule trigger for. Default: - EventStates.SUCCEEDED
        :param rule_name: A name for the rule. Default: - AWS CloudFormation generates a unique physical ID and uses that ID for the rule name. For more information, see Name Type.
        :param targets: Targets to invoke when this rule matches an event. Default: - No targets.
        '''
        props = GuardrailRuleProps(
            guardrail_behavior=guardrail_behavior,
            guardrail_id=guardrail_id,
            ou_id=ou_id,
            ou_name=ou_name,
            description=description,
            enabled=enabled,
            event_bus=event_bus,
            event_state=event_state,
            rule_name=rule_name,
            targets=targets,
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.enum(
    jsii_type="@renovosolutions/cdk-library-control-tower-lifecycle-events.EventStates"
)
class EventStates(enum.Enum):
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"


@jsii.enum(
    jsii_type="@renovosolutions/cdk-library-control-tower-lifecycle-events.GuardrailBehaviors"
)
class GuardrailBehaviors(enum.Enum):
    DETECTIVE = "DETECTIVE"
    PREVENTATIVE = "PREVENTATIVE"


@jsii.data_type(
    jsii_type="@renovosolutions/cdk-library-control-tower-lifecycle-events.GuardrailRuleProps",
    jsii_struct_bases=[BaseRuleProps],
    name_mapping={
        "description": "description",
        "enabled": "enabled",
        "event_bus": "eventBus",
        "event_state": "eventState",
        "rule_name": "ruleName",
        "targets": "targets",
        "guardrail_behavior": "guardrailBehavior",
        "guardrail_id": "guardrailId",
        "ou_id": "ouId",
        "ou_name": "ouName",
    },
)
class GuardrailRuleProps(BaseRuleProps):
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[builtins.bool] = None,
        event_bus: typing.Optional[aws_cdk.aws_events.IEventBus] = None,
        event_state: typing.Optional[EventStates] = None,
        rule_name: typing.Optional[builtins.str] = None,
        targets: typing.Optional[typing.Sequence[aws_cdk.aws_events.IRuleTarget]] = None,
        guardrail_behavior: typing.Optional[GuardrailBehaviors] = None,
        guardrail_id: typing.Optional[builtins.str] = None,
        ou_id: typing.Optional[builtins.str] = None,
        ou_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param description: A description of the rule's purpose. Default: - A rule for new account creation in Organizations
        :param enabled: Indicates whether the rule is enabled. Default: true
        :param event_bus: The event bus to associate with this rule. Default: - The default event bus.
        :param event_state: Which event state should this rule trigger for. Default: - EventStates.SUCCEEDED
        :param rule_name: A name for the rule. Default: - AWS CloudFormation generates a unique physical ID and uses that ID for the rule name. For more information, see Name Type.
        :param targets: Targets to invoke when this rule matches an event. Default: - No targets.
        :param guardrail_behavior: The guardrail behavior to match.
        :param guardrail_id: The guardrail ID to match.
        :param ou_id: The OU ID to match.
        :param ou_name: The OU name to match.
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if enabled is not None:
            self._values["enabled"] = enabled
        if event_bus is not None:
            self._values["event_bus"] = event_bus
        if event_state is not None:
            self._values["event_state"] = event_state
        if rule_name is not None:
            self._values["rule_name"] = rule_name
        if targets is not None:
            self._values["targets"] = targets
        if guardrail_behavior is not None:
            self._values["guardrail_behavior"] = guardrail_behavior
        if guardrail_id is not None:
            self._values["guardrail_id"] = guardrail_id
        if ou_id is not None:
            self._values["ou_id"] = ou_id
        if ou_name is not None:
            self._values["ou_name"] = ou_name

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the rule's purpose.

        :default: - A rule for new account creation in Organizations
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''Indicates whether the rule is enabled.

        :default: true
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def event_bus(self) -> typing.Optional[aws_cdk.aws_events.IEventBus]:
        '''The event bus to associate with this rule.

        :default: - The default event bus.
        '''
        result = self._values.get("event_bus")
        return typing.cast(typing.Optional[aws_cdk.aws_events.IEventBus], result)

    @builtins.property
    def event_state(self) -> typing.Optional[EventStates]:
        '''Which event state should this rule trigger for.

        :default: - EventStates.SUCCEEDED
        '''
        result = self._values.get("event_state")
        return typing.cast(typing.Optional[EventStates], result)

    @builtins.property
    def rule_name(self) -> typing.Optional[builtins.str]:
        '''A name for the rule.

        :default:

        - AWS CloudFormation generates a unique physical ID and uses that ID
        for the rule name. For more information, see Name Type.
        '''
        result = self._values.get("rule_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def targets(self) -> typing.Optional[typing.List[aws_cdk.aws_events.IRuleTarget]]:
        '''Targets to invoke when this rule matches an event.

        :default: - No targets.
        '''
        result = self._values.get("targets")
        return typing.cast(typing.Optional[typing.List[aws_cdk.aws_events.IRuleTarget]], result)

    @builtins.property
    def guardrail_behavior(self) -> typing.Optional[GuardrailBehaviors]:
        '''The guardrail behavior to match.'''
        result = self._values.get("guardrail_behavior")
        return typing.cast(typing.Optional[GuardrailBehaviors], result)

    @builtins.property
    def guardrail_id(self) -> typing.Optional[builtins.str]:
        '''The guardrail ID to match.'''
        result = self._values.get("guardrail_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ou_id(self) -> typing.Optional[builtins.str]:
        '''The OU ID to match.'''
        result = self._values.get("ou_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ou_name(self) -> typing.Optional[builtins.str]:
        '''The OU name to match.'''
        result = self._values.get("ou_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GuardrailRuleProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@renovosolutions/cdk-library-control-tower-lifecycle-events.OuRuleProps",
    jsii_struct_bases=[BaseRuleProps],
    name_mapping={
        "description": "description",
        "enabled": "enabled",
        "event_bus": "eventBus",
        "event_state": "eventState",
        "rule_name": "ruleName",
        "targets": "targets",
        "ou_id": "ouId",
        "ou_name": "ouName",
    },
)
class OuRuleProps(BaseRuleProps):
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[builtins.bool] = None,
        event_bus: typing.Optional[aws_cdk.aws_events.IEventBus] = None,
        event_state: typing.Optional[EventStates] = None,
        rule_name: typing.Optional[builtins.str] = None,
        targets: typing.Optional[typing.Sequence[aws_cdk.aws_events.IRuleTarget]] = None,
        ou_id: typing.Optional[builtins.str] = None,
        ou_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param description: A description of the rule's purpose. Default: - A rule for new account creation in Organizations
        :param enabled: Indicates whether the rule is enabled. Default: true
        :param event_bus: The event bus to associate with this rule. Default: - The default event bus.
        :param event_state: Which event state should this rule trigger for. Default: - EventStates.SUCCEEDED
        :param rule_name: A name for the rule. Default: - AWS CloudFormation generates a unique physical ID and uses that ID for the rule name. For more information, see Name Type.
        :param targets: Targets to invoke when this rule matches an event. Default: - No targets.
        :param ou_id: The OU ID to match.
        :param ou_name: The OU name to match.
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if enabled is not None:
            self._values["enabled"] = enabled
        if event_bus is not None:
            self._values["event_bus"] = event_bus
        if event_state is not None:
            self._values["event_state"] = event_state
        if rule_name is not None:
            self._values["rule_name"] = rule_name
        if targets is not None:
            self._values["targets"] = targets
        if ou_id is not None:
            self._values["ou_id"] = ou_id
        if ou_name is not None:
            self._values["ou_name"] = ou_name

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the rule's purpose.

        :default: - A rule for new account creation in Organizations
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''Indicates whether the rule is enabled.

        :default: true
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def event_bus(self) -> typing.Optional[aws_cdk.aws_events.IEventBus]:
        '''The event bus to associate with this rule.

        :default: - The default event bus.
        '''
        result = self._values.get("event_bus")
        return typing.cast(typing.Optional[aws_cdk.aws_events.IEventBus], result)

    @builtins.property
    def event_state(self) -> typing.Optional[EventStates]:
        '''Which event state should this rule trigger for.

        :default: - EventStates.SUCCEEDED
        '''
        result = self._values.get("event_state")
        return typing.cast(typing.Optional[EventStates], result)

    @builtins.property
    def rule_name(self) -> typing.Optional[builtins.str]:
        '''A name for the rule.

        :default:

        - AWS CloudFormation generates a unique physical ID and uses that ID
        for the rule name. For more information, see Name Type.
        '''
        result = self._values.get("rule_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def targets(self) -> typing.Optional[typing.List[aws_cdk.aws_events.IRuleTarget]]:
        '''Targets to invoke when this rule matches an event.

        :default: - No targets.
        '''
        result = self._values.get("targets")
        return typing.cast(typing.Optional[typing.List[aws_cdk.aws_events.IRuleTarget]], result)

    @builtins.property
    def ou_id(self) -> typing.Optional[builtins.str]:
        '''The OU ID to match.'''
        result = self._values.get("ou_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ou_name(self) -> typing.Optional[builtins.str]:
        '''The OU name to match.'''
        result = self._values.get("ou_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OuRuleProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RegisteredOrganizationalUnitRule(
    aws_cdk.aws_events.Rule,
    metaclass=jsii.JSIIMeta,
    jsii_type="@renovosolutions/cdk-library-control-tower-lifecycle-events.RegisteredOrganizationalUnitRule",
):
    '''A rule for matching events from CloudTrail where Control Tower registered a new Organizational Unit.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        description: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[builtins.bool] = None,
        event_bus: typing.Optional[aws_cdk.aws_events.IEventBus] = None,
        event_state: typing.Optional[EventStates] = None,
        rule_name: typing.Optional[builtins.str] = None,
        targets: typing.Optional[typing.Sequence[aws_cdk.aws_events.IRuleTarget]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param description: A description of the rule's purpose. Default: - A rule for new account creation in Organizations
        :param enabled: Indicates whether the rule is enabled. Default: true
        :param event_bus: The event bus to associate with this rule. Default: - The default event bus.
        :param event_state: Which event state should this rule trigger for. Default: - EventStates.SUCCEEDED
        :param rule_name: A name for the rule. Default: - AWS CloudFormation generates a unique physical ID and uses that ID for the rule name. For more information, see Name Type.
        :param targets: Targets to invoke when this rule matches an event. Default: - No targets.
        '''
        props = BaseRuleProps(
            description=description,
            enabled=enabled,
            event_bus=event_bus,
            event_state=event_state,
            rule_name=rule_name,
            targets=targets,
        )

        jsii.create(self.__class__, self, [scope, id, props])


class SetupLandingZoneRule(
    aws_cdk.aws_events.Rule,
    metaclass=jsii.JSIIMeta,
    jsii_type="@renovosolutions/cdk-library-control-tower-lifecycle-events.SetupLandingZoneRule",
):
    '''A rule for matching events from CloudTrail where a landing zone was setup via Control Tower.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        description: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[builtins.bool] = None,
        event_bus: typing.Optional[aws_cdk.aws_events.IEventBus] = None,
        event_state: typing.Optional[EventStates] = None,
        rule_name: typing.Optional[builtins.str] = None,
        targets: typing.Optional[typing.Sequence[aws_cdk.aws_events.IRuleTarget]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param description: A description of the rule's purpose. Default: - A rule for new account creation in Organizations
        :param enabled: Indicates whether the rule is enabled. Default: true
        :param event_bus: The event bus to associate with this rule. Default: - The default event bus.
        :param event_state: Which event state should this rule trigger for. Default: - EventStates.SUCCEEDED
        :param rule_name: A name for the rule. Default: - AWS CloudFormation generates a unique physical ID and uses that ID for the rule name. For more information, see Name Type.
        :param targets: Targets to invoke when this rule matches an event. Default: - No targets.
        '''
        props = BaseRuleProps(
            description=description,
            enabled=enabled,
            event_bus=event_bus,
            event_state=event_state,
            rule_name=rule_name,
            targets=targets,
        )

        jsii.create(self.__class__, self, [scope, id, props])


class UpdatedLandingZoneRule(
    aws_cdk.aws_events.Rule,
    metaclass=jsii.JSIIMeta,
    jsii_type="@renovosolutions/cdk-library-control-tower-lifecycle-events.UpdatedLandingZoneRule",
):
    '''A rule for matching events from CloudTrail where a landing zone was updated via Control Tower.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        description: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[builtins.bool] = None,
        event_bus: typing.Optional[aws_cdk.aws_events.IEventBus] = None,
        event_state: typing.Optional[EventStates] = None,
        rule_name: typing.Optional[builtins.str] = None,
        targets: typing.Optional[typing.Sequence[aws_cdk.aws_events.IRuleTarget]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param description: A description of the rule's purpose. Default: - A rule for new account creation in Organizations
        :param enabled: Indicates whether the rule is enabled. Default: true
        :param event_bus: The event bus to associate with this rule. Default: - The default event bus.
        :param event_state: Which event state should this rule trigger for. Default: - EventStates.SUCCEEDED
        :param rule_name: A name for the rule. Default: - AWS CloudFormation generates a unique physical ID and uses that ID for the rule name. For more information, see Name Type.
        :param targets: Targets to invoke when this rule matches an event. Default: - No targets.
        '''
        props = BaseRuleProps(
            description=description,
            enabled=enabled,
            event_bus=event_bus,
            event_state=event_state,
            rule_name=rule_name,
            targets=targets,
        )

        jsii.create(self.__class__, self, [scope, id, props])


class UpdatedManagedAccountRule(
    aws_cdk.aws_events.Rule,
    metaclass=jsii.JSIIMeta,
    jsii_type="@renovosolutions/cdk-library-control-tower-lifecycle-events.UpdatedManagedAccountRule",
):
    '''A rule for matching events from CloudTrail where Control Tower updated a managed account.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        account_id: typing.Optional[builtins.str] = None,
        account_name: typing.Optional[builtins.str] = None,
        ou_id: typing.Optional[builtins.str] = None,
        ou_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[builtins.bool] = None,
        event_bus: typing.Optional[aws_cdk.aws_events.IEventBus] = None,
        event_state: typing.Optional[EventStates] = None,
        rule_name: typing.Optional[builtins.str] = None,
        targets: typing.Optional[typing.Sequence[aws_cdk.aws_events.IRuleTarget]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param account_id: The account ID to match.
        :param account_name: The account name to match.
        :param ou_id: The OU ID to match.
        :param ou_name: The OU name to match.
        :param description: A description of the rule's purpose. Default: - A rule for new account creation in Organizations
        :param enabled: Indicates whether the rule is enabled. Default: true
        :param event_bus: The event bus to associate with this rule. Default: - The default event bus.
        :param event_state: Which event state should this rule trigger for. Default: - EventStates.SUCCEEDED
        :param rule_name: A name for the rule. Default: - AWS CloudFormation generates a unique physical ID and uses that ID for the rule name. For more information, see Name Type.
        :param targets: Targets to invoke when this rule matches an event. Default: - No targets.
        '''
        props = AccountRuleProps(
            account_id=account_id,
            account_name=account_name,
            ou_id=ou_id,
            ou_name=ou_name,
            description=description,
            enabled=enabled,
            event_bus=event_bus,
            event_state=event_state,
            rule_name=rule_name,
            targets=targets,
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="@renovosolutions/cdk-library-control-tower-lifecycle-events.AccountRuleProps",
    jsii_struct_bases=[BaseRuleProps],
    name_mapping={
        "description": "description",
        "enabled": "enabled",
        "event_bus": "eventBus",
        "event_state": "eventState",
        "rule_name": "ruleName",
        "targets": "targets",
        "account_id": "accountId",
        "account_name": "accountName",
        "ou_id": "ouId",
        "ou_name": "ouName",
    },
)
class AccountRuleProps(BaseRuleProps):
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[builtins.bool] = None,
        event_bus: typing.Optional[aws_cdk.aws_events.IEventBus] = None,
        event_state: typing.Optional[EventStates] = None,
        rule_name: typing.Optional[builtins.str] = None,
        targets: typing.Optional[typing.Sequence[aws_cdk.aws_events.IRuleTarget]] = None,
        account_id: typing.Optional[builtins.str] = None,
        account_name: typing.Optional[builtins.str] = None,
        ou_id: typing.Optional[builtins.str] = None,
        ou_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param description: A description of the rule's purpose. Default: - A rule for new account creation in Organizations
        :param enabled: Indicates whether the rule is enabled. Default: true
        :param event_bus: The event bus to associate with this rule. Default: - The default event bus.
        :param event_state: Which event state should this rule trigger for. Default: - EventStates.SUCCEEDED
        :param rule_name: A name for the rule. Default: - AWS CloudFormation generates a unique physical ID and uses that ID for the rule name. For more information, see Name Type.
        :param targets: Targets to invoke when this rule matches an event. Default: - No targets.
        :param account_id: The account ID to match.
        :param account_name: The account name to match.
        :param ou_id: The OU ID to match.
        :param ou_name: The OU name to match.
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if enabled is not None:
            self._values["enabled"] = enabled
        if event_bus is not None:
            self._values["event_bus"] = event_bus
        if event_state is not None:
            self._values["event_state"] = event_state
        if rule_name is not None:
            self._values["rule_name"] = rule_name
        if targets is not None:
            self._values["targets"] = targets
        if account_id is not None:
            self._values["account_id"] = account_id
        if account_name is not None:
            self._values["account_name"] = account_name
        if ou_id is not None:
            self._values["ou_id"] = ou_id
        if ou_name is not None:
            self._values["ou_name"] = ou_name

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the rule's purpose.

        :default: - A rule for new account creation in Organizations
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''Indicates whether the rule is enabled.

        :default: true
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def event_bus(self) -> typing.Optional[aws_cdk.aws_events.IEventBus]:
        '''The event bus to associate with this rule.

        :default: - The default event bus.
        '''
        result = self._values.get("event_bus")
        return typing.cast(typing.Optional[aws_cdk.aws_events.IEventBus], result)

    @builtins.property
    def event_state(self) -> typing.Optional[EventStates]:
        '''Which event state should this rule trigger for.

        :default: - EventStates.SUCCEEDED
        '''
        result = self._values.get("event_state")
        return typing.cast(typing.Optional[EventStates], result)

    @builtins.property
    def rule_name(self) -> typing.Optional[builtins.str]:
        '''A name for the rule.

        :default:

        - AWS CloudFormation generates a unique physical ID and uses that ID
        for the rule name. For more information, see Name Type.
        '''
        result = self._values.get("rule_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def targets(self) -> typing.Optional[typing.List[aws_cdk.aws_events.IRuleTarget]]:
        '''Targets to invoke when this rule matches an event.

        :default: - No targets.
        '''
        result = self._values.get("targets")
        return typing.cast(typing.Optional[typing.List[aws_cdk.aws_events.IRuleTarget]], result)

    @builtins.property
    def account_id(self) -> typing.Optional[builtins.str]:
        '''The account ID to match.'''
        result = self._values.get("account_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def account_name(self) -> typing.Optional[builtins.str]:
        '''The account name to match.'''
        result = self._values.get("account_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ou_id(self) -> typing.Optional[builtins.str]:
        '''The OU ID to match.'''
        result = self._values.get("ou_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ou_name(self) -> typing.Optional[builtins.str]:
        '''The OU name to match.'''
        result = self._values.get("ou_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccountRuleProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AccountRuleProps",
    "BaseRuleProps",
    "CreatedAccountByOrganizationsRule",
    "CreatedAccountRule",
    "DeregisteredOrganizationalUnitRule",
    "DisabledGuardrailRule",
    "EnabledGuardrailRule",
    "EventStates",
    "GuardrailBehaviors",
    "GuardrailRuleProps",
    "OuRuleProps",
    "RegisteredOrganizationalUnitRule",
    "SetupLandingZoneRule",
    "UpdatedLandingZoneRule",
    "UpdatedManagedAccountRule",
]

publication.publish()

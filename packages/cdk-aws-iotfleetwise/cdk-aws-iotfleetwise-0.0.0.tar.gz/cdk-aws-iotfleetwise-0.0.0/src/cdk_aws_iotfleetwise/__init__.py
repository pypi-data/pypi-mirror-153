'''
[![NPM version](https://badge.fury.io/js/cdk-iotfleetwise.svg)](https://badge.fury.io/js/cdk-iotfleetwise)
[![PyPI version](https://badge.fury.io/py/cdk-iotfleetwise.svg)](https://badge.fury.io/py/cdk-iotfleetwise)
[![release](https://github.com/aws-samples/cdk-iotfleetwise/actions/workflows/release.yml/badge.svg)](https://github.com/aws-samples/cdk-iotfleetwise/actions/workflows/release.yml)

# cdk-aws-iotfleetwise

L2 CDK construct to provision AWS IoT Fleetwise

# Install

### Typescript

```sh
npm install cdk-aws-iotfleetwise
```

[API Reference](doc/api-typescript.md)

#### Python

```sh
pip install cdk-aws-iotfleetwise
```

[API Reference](doc/api-python.md)

# Sample

```python

    const database = new ts.CfnDatabase(this, 'Database', {
      databaseName: 'FleetWise',
    });

    const table = new ts.CfnTable(this, 'Table', {
      databaseName: 'FleetWise',
      tableName: 'FleetWise',
    });

    const role = new aim.Role(this, 'Role', {
      assumedBy: new aim.ServicePrincipal('iotfleetwise.amazonaws.com'),
      managedPolicies: [
        aim.ManagedPolicy.fromAwsManagedPolicyName('AdministratorAccess'),
      ],

    });

    const signalCatalog = new ifw.SignalCatalog(this, 'SignalCatalog', {
      database,
      table,
      role,
      nodes: [
        new ifw.SignalCatalogBranch('Vehicle', 'Vehicle'),
        new ifw.SignalCatalogSensor('EngineTorque', 'Vehicle.EngineTorque', 'DOUBLE'),
      ],
    });

    const model_a = new ifw.VehicleModel(this, 'ModelA', {
      signalCatalog,
      name: 'modelA',
      description: 'Model A vehicle',
      networkInterfaces: [new ifw.CanVehicleInterface('1', 'vcan0')],
      signals: [
        new ifw.CanVehicleSignal('EngineTorque', 'Vehicle.EngineTorque', '1',
          401, // messageId
          1.0, // factor
          true, // isBigEndian
          false, // isSigned
          8, // lenght
          0.0, // offset
          9), // startBit
      ],
    });

    const vin100 = new ifw.Vehicle(this, 'vin100', {
      vehicleId: 'vin100',
      vehicleModel: model_a,
      createIotThing: true
    });

    new ifw.Campaign(this, 'Campaign', {
      name: 'TimeBasedCampaign',
      target: vin100,
      collectionScheme: new ifw.TimeBasedCollectionScheme(cdk.Duration.seconds(10)),
      signals: [
        new ifw.CampaignSignal('Vehicle.EngineTorque'),
      ],
    });
```

## Getting started

To deploy a simple end-to-end example you can use the following commands

```sh
yarn install
projen && projen build
npx cdk -a lib/integ.full.js deploy
```

The deploy takes about 15 mins mostly due to compilation of the IoT FleetWise agent in the
EC2 instance that simulate the vehicle. Once deploy is finshed, approve the campaign with the command:

```sh
aws iotfleetwise update-campaign --campaign-name FwTimeBasedCampaign --action APPROVE
```

and data will start to show up in the Timestream table.

## TODO

Warning: this construct should be considered at alpha stage and is not feature complete.

* Reduce Lambda log retention to 1d
* Apply the least priviledge principle to roles
* Implement updates for all the custom resources
* Fleet
* Conditional campaigns

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more
information.

## License

This code is licensed under the MIT-0 License. See the LICENSE file.
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
import aws_cdk.aws_iam
import aws_cdk.aws_lambda
import aws_cdk.aws_timestream
import constructs


class Campaign(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-aws-iotfleetwise.Campaign",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        props: "ICampaign",
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param props: -
        '''
        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "arn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="target")
    def target(self) -> "Vehicle":
        return typing.cast("Vehicle", jsii.get(self, "target"))


class CampaignSignal(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-aws-iotfleetwise.CampaignSignal",
):
    def __init__(
        self,
        name: builtins.str,
        max_sample_count: typing.Optional[jsii.Number] = None,
        minimum_sampling_interval: typing.Optional[aws_cdk.Duration] = None,
    ) -> None:
        '''
        :param name: -
        :param max_sample_count: -
        :param minimum_sampling_interval: -
        '''
        jsii.create(self.__class__, self, [name, max_sample_count, minimum_sampling_interval])

    @jsii.member(jsii_name="toObject")
    def to_object(self) -> typing.Mapping[typing.Any, typing.Any]:
        return typing.cast(typing.Mapping[typing.Any, typing.Any], jsii.invoke(self, "toObject", []))


class CollectionScheme(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-aws-iotfleetwise.CollectionScheme",
):
    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="toObject")
    def to_object(self) -> typing.Mapping[typing.Any, typing.Any]:
        return typing.cast(typing.Mapping[typing.Any, typing.Any], jsii.invoke(self, "toObject", []))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="scheme")
    def _scheme(self) -> typing.Mapping[typing.Any, typing.Any]:
        return typing.cast(typing.Mapping[typing.Any, typing.Any], jsii.get(self, "scheme"))

    @_scheme.setter
    def _scheme(self, value: typing.Mapping[typing.Any, typing.Any]) -> None:
        jsii.set(self, "scheme", value)


@jsii.interface(jsii_type="cdk-aws-iotfleetwise.ICampaign")
class ICampaign(typing_extensions.Protocol):
    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="collectionScheme")
    def collection_scheme(self) -> CollectionScheme:
        ...

    @collection_scheme.setter
    def collection_scheme(self, value: CollectionScheme) -> None:
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        ...

    @name.setter
    def name(self, value: builtins.str) -> None:
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="signals")
    def signals(self) -> typing.List[CampaignSignal]:
        ...

    @signals.setter
    def signals(self, value: typing.List[CampaignSignal]) -> None:
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="target")
    def target(self) -> "Vehicle":
        ...

    @target.setter
    def target(self, value: "Vehicle") -> None:
        ...


class _ICampaignProxy:
    __jsii_type__: typing.ClassVar[str] = "cdk-aws-iotfleetwise.ICampaign"

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="collectionScheme")
    def collection_scheme(self) -> CollectionScheme:
        return typing.cast(CollectionScheme, jsii.get(self, "collectionScheme"))

    @collection_scheme.setter
    def collection_scheme(self, value: CollectionScheme) -> None:
        jsii.set(self, "collectionScheme", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="signals")
    def signals(self) -> typing.List[CampaignSignal]:
        return typing.cast(typing.List[CampaignSignal], jsii.get(self, "signals"))

    @signals.setter
    def signals(self, value: typing.List[CampaignSignal]) -> None:
        jsii.set(self, "signals", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="target")
    def target(self) -> "Vehicle":
        return typing.cast("Vehicle", jsii.get(self, "target"))

    @target.setter
    def target(self, value: "Vehicle") -> None:
        jsii.set(self, "target", value)

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ICampaign).__jsii_proxy_class__ = lambda : _ICampaignProxy


@jsii.interface(jsii_type="cdk-aws-iotfleetwise.IServiceCatalogProps")
class IServiceCatalogProps(typing_extensions.Protocol):
    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="database")
    def database(self) -> aws_cdk.aws_timestream.CfnDatabase:
        ...

    @database.setter
    def database(self, value: aws_cdk.aws_timestream.CfnDatabase) -> None:
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="nodes")
    def nodes(self) -> typing.List["SignalCatalogNode"]:
        ...

    @nodes.setter
    def nodes(self, value: typing.List["SignalCatalogNode"]) -> None:
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="role")
    def role(self) -> aws_cdk.aws_iam.Role:
        ...

    @role.setter
    def role(self, value: aws_cdk.aws_iam.Role) -> None:
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="table")
    def table(self) -> aws_cdk.aws_timestream.CfnTable:
        ...

    @table.setter
    def table(self, value: aws_cdk.aws_timestream.CfnTable) -> None:
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        ...

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        ...

    @name.setter
    def name(self, value: typing.Optional[builtins.str]) -> None:
        ...


class _IServiceCatalogPropsProxy:
    __jsii_type__: typing.ClassVar[str] = "cdk-aws-iotfleetwise.IServiceCatalogProps"

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="database")
    def database(self) -> aws_cdk.aws_timestream.CfnDatabase:
        return typing.cast(aws_cdk.aws_timestream.CfnDatabase, jsii.get(self, "database"))

    @database.setter
    def database(self, value: aws_cdk.aws_timestream.CfnDatabase) -> None:
        jsii.set(self, "database", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="nodes")
    def nodes(self) -> typing.List["SignalCatalogNode"]:
        return typing.cast(typing.List["SignalCatalogNode"], jsii.get(self, "nodes"))

    @nodes.setter
    def nodes(self, value: typing.List["SignalCatalogNode"]) -> None:
        jsii.set(self, "nodes", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="role")
    def role(self) -> aws_cdk.aws_iam.Role:
        return typing.cast(aws_cdk.aws_iam.Role, jsii.get(self, "role"))

    @role.setter
    def role(self, value: aws_cdk.aws_iam.Role) -> None:
        jsii.set(self, "role", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="table")
    def table(self) -> aws_cdk.aws_timestream.CfnTable:
        return typing.cast(aws_cdk.aws_timestream.CfnTable, jsii.get(self, "table"))

    @table.setter
    def table(self, value: aws_cdk.aws_timestream.CfnTable) -> None:
        jsii.set(self, "table", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "description", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @name.setter
    def name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "name", value)

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IServiceCatalogProps).__jsii_proxy_class__ = lambda : _IServiceCatalogPropsProxy


@jsii.interface(jsii_type="cdk-aws-iotfleetwise.IVehicle")
class IVehicle(typing_extensions.Protocol):
    '''Interface.'''

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="createIotThing")
    def create_iot_thing(self) -> builtins.bool:
        ...

    @create_iot_thing.setter
    def create_iot_thing(self, value: builtins.bool) -> None:
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="vehicleId")
    def vehicle_id(self) -> builtins.str:
        ...

    @vehicle_id.setter
    def vehicle_id(self, value: builtins.str) -> None:
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="vehicleModel")
    def vehicle_model(self) -> "VehicleModel":
        ...

    @vehicle_model.setter
    def vehicle_model(self, value: "VehicleModel") -> None:
        ...


class _IVehicleProxy:
    '''Interface.'''

    __jsii_type__: typing.ClassVar[str] = "cdk-aws-iotfleetwise.IVehicle"

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="createIotThing")
    def create_iot_thing(self) -> builtins.bool:
        return typing.cast(builtins.bool, jsii.get(self, "createIotThing"))

    @create_iot_thing.setter
    def create_iot_thing(self, value: builtins.bool) -> None:
        jsii.set(self, "createIotThing", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="vehicleId")
    def vehicle_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vehicleId"))

    @vehicle_id.setter
    def vehicle_id(self, value: builtins.str) -> None:
        jsii.set(self, "vehicleId", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="vehicleModel")
    def vehicle_model(self) -> "VehicleModel":
        return typing.cast("VehicleModel", jsii.get(self, "vehicleModel"))

    @vehicle_model.setter
    def vehicle_model(self, value: "VehicleModel") -> None:
        jsii.set(self, "vehicleModel", value)

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IVehicle).__jsii_proxy_class__ = lambda : _IVehicleProxy


@jsii.interface(jsii_type="cdk-aws-iotfleetwise.IVehicleModel")
class IVehicleModel(typing_extensions.Protocol):
    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        ...

    @name.setter
    def name(self, value: builtins.str) -> None:
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="networkInterfaces")
    def network_interfaces(self) -> typing.List["VehicleInterface"]:
        ...

    @network_interfaces.setter
    def network_interfaces(self, value: typing.List["VehicleInterface"]) -> None:
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="signalCatalog")
    def signal_catalog(self) -> "SignalCatalog":
        ...

    @signal_catalog.setter
    def signal_catalog(self, value: "SignalCatalog") -> None:
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="signals")
    def signals(self) -> typing.List["VehicleSignal"]:
        ...

    @signals.setter
    def signals(self, value: typing.List["VehicleSignal"]) -> None:
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        ...

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        ...


class _IVehicleModelProxy:
    __jsii_type__: typing.ClassVar[str] = "cdk-aws-iotfleetwise.IVehicleModel"

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="networkInterfaces")
    def network_interfaces(self) -> typing.List["VehicleInterface"]:
        return typing.cast(typing.List["VehicleInterface"], jsii.get(self, "networkInterfaces"))

    @network_interfaces.setter
    def network_interfaces(self, value: typing.List["VehicleInterface"]) -> None:
        jsii.set(self, "networkInterfaces", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="signalCatalog")
    def signal_catalog(self) -> "SignalCatalog":
        return typing.cast("SignalCatalog", jsii.get(self, "signalCatalog"))

    @signal_catalog.setter
    def signal_catalog(self, value: "SignalCatalog") -> None:
        jsii.set(self, "signalCatalog", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="signals")
    def signals(self) -> typing.List["VehicleSignal"]:
        return typing.cast(typing.List["VehicleSignal"], jsii.get(self, "signals"))

    @signals.setter
    def signals(self, value: typing.List["VehicleSignal"]) -> None:
        jsii.set(self, "signals", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "description", value)

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IVehicleModel).__jsii_proxy_class__ = lambda : _IVehicleModelProxy


class SignalCatalog(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-aws-iotfleetwise.SignalCatalog",
):
    '''The Signal Catalog represents the list of all signals that you want to collect from all the vehicles.

    The AWS IoT Fleetwise preview can only support a single Signal Catalog per account.
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        props: IServiceCatalogProps,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param props: -
        '''
        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "arn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="lambdaLayer")
    def lambda_layer(self) -> aws_cdk.aws_lambda.LayerVersion:
        return typing.cast(aws_cdk.aws_lambda.LayerVersion, jsii.get(self, "lambdaLayer"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="lambdaRole")
    def lambda_role(self) -> aws_cdk.aws_iam.Role:
        return typing.cast(aws_cdk.aws_iam.Role, jsii.get(self, "lambdaRole"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the signal catalog.'''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))


class SignalCatalogNode(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-aws-iotfleetwise.SignalCatalogNode",
):
    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="toObject")
    def to_object(self) -> typing.Mapping[typing.Any, typing.Any]:
        return typing.cast(typing.Mapping[typing.Any, typing.Any], jsii.invoke(self, "toObject", []))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="node")
    def _node(self) -> typing.Mapping[typing.Any, typing.Any]:
        return typing.cast(typing.Mapping[typing.Any, typing.Any], jsii.get(self, "node"))

    @_node.setter
    def _node(self, value: typing.Mapping[typing.Any, typing.Any]) -> None:
        jsii.set(self, "node", value)


class SignalCatalogSensor(
    SignalCatalogNode,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-aws-iotfleetwise.SignalCatalogSensor",
):
    def __init__(
        self,
        name: builtins.str,
        fully_qualified_name: builtins.str,
        data_type: builtins.str,
        unit: typing.Optional[builtins.str] = None,
        min: typing.Optional[jsii.Number] = None,
        max: typing.Optional[jsii.Number] = None,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: -
        :param fully_qualified_name: -
        :param data_type: -
        :param unit: -
        :param min: -
        :param max: -
        :param description: -
        '''
        jsii.create(self.__class__, self, [name, fully_qualified_name, data_type, unit, min, max, description])


class TimeBasedCollectionScheme(
    CollectionScheme,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-aws-iotfleetwise.TimeBasedCollectionScheme",
):
    def __init__(self, period: aws_cdk.Duration) -> None:
        '''
        :param period: -
        '''
        jsii.create(self.__class__, self, [period])


class Vehicle(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-aws-iotfleetwise.Vehicle",
):
    '''The vehicle of a specific type from which IoT FleetWise collect signals.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        props: IVehicle,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param props: -
        '''
        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "arn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="vehicleModel")
    def vehicle_model(self) -> "VehicleModel":
        return typing.cast("VehicleModel", jsii.get(self, "vehicleModel"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="certificateArn")
    def certificate_arn(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "certificateArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="certificateId")
    def certificate_id(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "certificateId"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="certificatePem")
    def certificate_pem(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "certificatePem"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="endpointAddress")
    def endpoint_address(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endpointAddress"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="privateKey")
    def private_key(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "privateKey"))


class VehicleInterface(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-aws-iotfleetwise.VehicleInterface",
):
    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="toObject")
    def to_object(self) -> typing.Mapping[typing.Any, typing.Any]:
        return typing.cast(typing.Mapping[typing.Any, typing.Any], jsii.invoke(self, "toObject", []))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="intf")
    def _intf(self) -> typing.Mapping[typing.Any, typing.Any]:
        return typing.cast(typing.Mapping[typing.Any, typing.Any], jsii.get(self, "intf"))

    @_intf.setter
    def _intf(self, value: typing.Mapping[typing.Any, typing.Any]) -> None:
        jsii.set(self, "intf", value)


class VehicleModel(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-aws-iotfleetwise.VehicleModel",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        props: IVehicleModel,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param props: -
        '''
        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="signalCatalog")
    def signal_catalog(self) -> SignalCatalog:
        return typing.cast(SignalCatalog, jsii.get(self, "signalCatalog"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))


class VehicleSignal(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-aws-iotfleetwise.VehicleSignal",
):
    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="toObject")
    def to_object(self) -> typing.Mapping[typing.Any, typing.Any]:
        return typing.cast(typing.Mapping[typing.Any, typing.Any], jsii.invoke(self, "toObject", []))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="signal")
    def _signal(self) -> typing.Mapping[typing.Any, typing.Any]:
        return typing.cast(typing.Mapping[typing.Any, typing.Any], jsii.get(self, "signal"))

    @_signal.setter
    def _signal(self, value: typing.Mapping[typing.Any, typing.Any]) -> None:
        jsii.set(self, "signal", value)


class CanVehicleInterface(
    VehicleInterface,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-aws-iotfleetwise.CanVehicleInterface",
):
    def __init__(self, interface_id: builtins.str, name: builtins.str) -> None:
        '''
        :param interface_id: -
        :param name: -
        '''
        jsii.create(self.__class__, self, [interface_id, name])


class CanVehicleSignal(
    VehicleSignal,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-aws-iotfleetwise.CanVehicleSignal",
):
    def __init__(
        self,
        name: builtins.str,
        fully_qualified_name: builtins.str,
        interface_id: builtins.str,
        message_id: jsii.Number,
        factor: jsii.Number,
        is_big_endian: builtins.bool,
        is_signed: builtins.bool,
        length: jsii.Number,
        offset: jsii.Number,
        start_bit: jsii.Number,
    ) -> None:
        '''
        :param name: -
        :param fully_qualified_name: -
        :param interface_id: -
        :param message_id: -
        :param factor: -
        :param is_big_endian: -
        :param is_signed: -
        :param length: -
        :param offset: -
        :param start_bit: -
        '''
        jsii.create(self.__class__, self, [name, fully_qualified_name, interface_id, message_id, factor, is_big_endian, is_signed, length, offset, start_bit])


class SignalCatalogBranch(
    SignalCatalogNode,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-aws-iotfleetwise.SignalCatalogBranch",
):
    def __init__(
        self,
        name: builtins.str,
        fully_qualified_name: builtins.str,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: -
        :param fully_qualified_name: -
        :param description: -
        '''
        jsii.create(self.__class__, self, [name, fully_qualified_name, description])


__all__ = [
    "Campaign",
    "CampaignSignal",
    "CanVehicleInterface",
    "CanVehicleSignal",
    "CollectionScheme",
    "ICampaign",
    "IServiceCatalogProps",
    "IVehicle",
    "IVehicleModel",
    "SignalCatalog",
    "SignalCatalogBranch",
    "SignalCatalogNode",
    "SignalCatalogSensor",
    "TimeBasedCollectionScheme",
    "Vehicle",
    "VehicleInterface",
    "VehicleModel",
    "VehicleSignal",
]

publication.publish()

'''
![GitHub Workflow Status](https://img.shields.io/github/workflow/status/gotodeploy/cdk-valheim/Build) [![GitHub license](https://img.shields.io/github/license/gotodeploy/cdk-valheim)](https://github.com/gotodeploy/cdk-valheim/blob/main/LICENSE) ![npm](https://img.shields.io/npm/dw/cdk-valheim?label=npm) ![PyPI - Downloads](https://img.shields.io/pypi/dw/cdk-valheim?label=PyPI)

# cdk-valheim

A high level CDK construct of [Valheim](https://www.valheimgame.com/) dedicated server.

![](assets/images/diagram.png)

## Features

* Fargate cluster to run a Valheim server, with EFS for persistence (schedulable)
* Hourly AWS Backup with 3 days retention (customizable)
* [lloesche/valheim-server](https://github.com/lloesche/valheim-server-docker) as the default container image (replaceable)

See [integration test](src/integ.valheim.ts) for an example.

## API Doc

See [API.md](API.md)

## References

* [On-demand, serverless Valheim server setup with AWS CDK, Discord Interactions and GitLab CI](https://briancaffey.github.io/2021/03/18/on-demand-dedicated-serverless-valheim-server-with-cdk-discrod-interactions/)
* [Grantapher/discord-cdk-valheim](https://github.com/Grantapher/discord-cdk-valheim)

## Examples

The construct is published to both npm and PyPI.

### TypeScript

```python
new ValheimWorld(stack, 'ValheimWorld', {
  cpu: 2048,
  memoryLimitMiB: 4096,
  schedules: [{
    start: { hour: '12', weekDay: '1-5' },
    stop: { hour: '1', weekDay: '1-5' },
  }],
  environment: {
    SERVER_NAME: 'CDK Valheim',
    WORLD_NAME: 'Amazon',
    SERVER_PASS: 'fargate',
    BACKUPS: 'false',
  },
});
```

### Python

```python
ValheimWorld(
    self,
    'ValheimWorld',
    cpu=2048,
    memory_limit_mib=4096,
    schedules=[ValheimWorldScalingSchedule(
        start=CronOptions(hour='12', week_day='1-5'),
        stop=CronOptions(hour='1', week_day='1-5'),
    )],
    environment={
        'SERVER_NAME': 'CDK Valheim',
        'WORLD_NAME': 'Amazon',
        'SERVER_PASS': 'fargate',
        'BACKUPS': 'false',
    })
```

## Testing

* Unit test and snapshot test

```sh
npx projen test
```

* Integration test

```sh
npx cdk -a "npx ts-node src/integ.valheim.ts" diff
npx cdk -a "npx ts-node src/integ.valheim.ts" deploy
```
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

import aws_cdk.aws_applicationautoscaling
import aws_cdk.aws_backup
import aws_cdk.aws_ec2
import aws_cdk.aws_ecs
import aws_cdk.aws_efs
import constructs


class ValheimWorld(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-valheim.ValheimWorld",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        backup_plan: typing.Optional[aws_cdk.aws_backup.BackupPlan] = None,
        container_path: typing.Optional[builtins.str] = None,
        cpu: typing.Optional[jsii.Number] = None,
        desired_count: typing.Optional[jsii.Number] = None,
        environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        file_system: typing.Optional[aws_cdk.aws_efs.FileSystem] = None,
        image: typing.Optional[aws_cdk.aws_ecs.ContainerImage] = None,
        log_group: typing.Optional[aws_cdk.aws_ecs.LogDriver] = None,
        memory_limit_mib: typing.Optional[jsii.Number] = None,
        schedules: typing.Optional[typing.Sequence["ValheimWorldScalingScheduleProps"]] = None,
        vpc: typing.Optional[aws_cdk.aws_ec2.IVpc] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param backup_plan: AWS Backup plan for EFS. Default: - Hourly backup with 3 days retension.
        :param container_path: The path on the container to mount the host volume at. Default: - /config/
        :param cpu: The number of cpu units used by the task. For tasks using the Fargate launch type, this field is required and you must use one of the following values, which determines your range of valid values for the memory parameter: 256 (.25 vCPU) - Available memory values: 512 (0.5 GB), 1024 (1 GB), 2048 (2 GB) 512 (.5 vCPU) - Available memory values: 1024 (1 GB), 2048 (2 GB), 3072 (3 GB), 4096 (4 GB) 1024 (1 vCPU) - Available memory values: 2048 (2 GB), 3072 (3 GB), 4096 (4 GB), 5120 (5 GB), 6144 (6 GB), 7168 (7 GB), 8192 (8 GB) 2048 (2 vCPU) - Available memory values: Between 4096 (4 GB) and 16384 (16 GB) in increments of 1024 (1 GB) 4096 (4 vCPU) - Available memory values: Between 8192 (8 GB) and 30720 (30 GB) in increments of 1024 (1 GB) Default: 1024
        :param desired_count: Desired count of Fargate container. Set 0 for maintenance. Default: - 1
        :param environment: The environment variables to pass to the container. Default: - No environment variables.
        :param file_system: Persistent storage for save data. Default: - Amazon EFS for default persistent storage.
        :param image: The image used to start a container. This string is passed directly to the Docker daemon. Images in the Docker Hub registry are available by default. Other repositories are specified with either repository-url/image:tag or repository-url/image@digest. Default: - `lloesche/valheim-server <https://hub.docker.com/r/lloesche/valheim-server>`_
        :param log_group: Valheim Server log Group. Default: - Create the new AWS Cloudwatch Log Group for Valheim Server.
        :param memory_limit_mib: The amount (in MiB) of memory used by the task. For tasks using the Fargate launch type, this field is required and you must use one of the following values, which determines your range of valid values for the cpu parameter: 512 (0.5 GB), 1024 (1 GB), 2048 (2 GB) - Available cpu values: 256 (.25 vCPU) 1024 (1 GB), 2048 (2 GB), 3072 (3 GB), 4096 (4 GB) - Available cpu values: 512 (.5 vCPU) 2048 (2 GB), 3072 (3 GB), 4096 (4 GB), 5120 (5 GB), 6144 (6 GB), 7168 (7 GB), 8192 (8 GB) - Available cpu values: 1024 (1 vCPU) Between 4096 (4 GB) and 16384 (16 GB) in increments of 1024 (1 GB) - Available cpu values: 2048 (2 vCPU) Between 8192 (8 GB) and 30720 (30 GB) in increments of 1024 (1 GB) - Available cpu values: 4096 (4 vCPU) Default: 2048
        :param schedules: Running schedules. Default: - Always running.
        :param vpc: The VPC where your ECS instances will be running or your ENIs will be deployed. Default: - creates a new VPC with two AZs
        '''
        props = ValheimWorldProps(
            backup_plan=backup_plan,
            container_path=container_path,
            cpu=cpu,
            desired_count=desired_count,
            environment=environment,
            file_system=file_system,
            image=image,
            log_group=log_group,
            memory_limit_mib=memory_limit_mib,
            schedules=schedules,
            vpc=vpc,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="backupPlan")
    def backup_plan(self) -> aws_cdk.aws_backup.BackupPlan:
        return typing.cast(aws_cdk.aws_backup.BackupPlan, jsii.get(self, "backupPlan"))

    @backup_plan.setter
    def backup_plan(self, value: aws_cdk.aws_backup.BackupPlan) -> None:
        jsii.set(self, "backupPlan", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="fileSystem")
    def file_system(self) -> aws_cdk.aws_efs.FileSystem:
        return typing.cast(aws_cdk.aws_efs.FileSystem, jsii.get(self, "fileSystem"))

    @file_system.setter
    def file_system(self, value: aws_cdk.aws_efs.FileSystem) -> None:
        jsii.set(self, "fileSystem", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="service")
    def service(self) -> aws_cdk.aws_ecs.FargateService:
        return typing.cast(aws_cdk.aws_ecs.FargateService, jsii.get(self, "service"))

    @service.setter
    def service(self, value: aws_cdk.aws_ecs.FargateService) -> None:
        jsii.set(self, "service", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="schedules")
    def schedules(self) -> typing.Optional[typing.List["ValheimWorldScalingSchedule"]]:
        return typing.cast(typing.Optional[typing.List["ValheimWorldScalingSchedule"]], jsii.get(self, "schedules"))

    @schedules.setter
    def schedules(
        self,
        value: typing.Optional[typing.List["ValheimWorldScalingSchedule"]],
    ) -> None:
        jsii.set(self, "schedules", value)


@jsii.data_type(
    jsii_type="cdk-valheim.ValheimWorldProps",
    jsii_struct_bases=[],
    name_mapping={
        "backup_plan": "backupPlan",
        "container_path": "containerPath",
        "cpu": "cpu",
        "desired_count": "desiredCount",
        "environment": "environment",
        "file_system": "fileSystem",
        "image": "image",
        "log_group": "logGroup",
        "memory_limit_mib": "memoryLimitMiB",
        "schedules": "schedules",
        "vpc": "vpc",
    },
)
class ValheimWorldProps:
    def __init__(
        self,
        *,
        backup_plan: typing.Optional[aws_cdk.aws_backup.BackupPlan] = None,
        container_path: typing.Optional[builtins.str] = None,
        cpu: typing.Optional[jsii.Number] = None,
        desired_count: typing.Optional[jsii.Number] = None,
        environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        file_system: typing.Optional[aws_cdk.aws_efs.FileSystem] = None,
        image: typing.Optional[aws_cdk.aws_ecs.ContainerImage] = None,
        log_group: typing.Optional[aws_cdk.aws_ecs.LogDriver] = None,
        memory_limit_mib: typing.Optional[jsii.Number] = None,
        schedules: typing.Optional[typing.Sequence["ValheimWorldScalingScheduleProps"]] = None,
        vpc: typing.Optional[aws_cdk.aws_ec2.IVpc] = None,
    ) -> None:
        '''
        :param backup_plan: AWS Backup plan for EFS. Default: - Hourly backup with 3 days retension.
        :param container_path: The path on the container to mount the host volume at. Default: - /config/
        :param cpu: The number of cpu units used by the task. For tasks using the Fargate launch type, this field is required and you must use one of the following values, which determines your range of valid values for the memory parameter: 256 (.25 vCPU) - Available memory values: 512 (0.5 GB), 1024 (1 GB), 2048 (2 GB) 512 (.5 vCPU) - Available memory values: 1024 (1 GB), 2048 (2 GB), 3072 (3 GB), 4096 (4 GB) 1024 (1 vCPU) - Available memory values: 2048 (2 GB), 3072 (3 GB), 4096 (4 GB), 5120 (5 GB), 6144 (6 GB), 7168 (7 GB), 8192 (8 GB) 2048 (2 vCPU) - Available memory values: Between 4096 (4 GB) and 16384 (16 GB) in increments of 1024 (1 GB) 4096 (4 vCPU) - Available memory values: Between 8192 (8 GB) and 30720 (30 GB) in increments of 1024 (1 GB) Default: 1024
        :param desired_count: Desired count of Fargate container. Set 0 for maintenance. Default: - 1
        :param environment: The environment variables to pass to the container. Default: - No environment variables.
        :param file_system: Persistent storage for save data. Default: - Amazon EFS for default persistent storage.
        :param image: The image used to start a container. This string is passed directly to the Docker daemon. Images in the Docker Hub registry are available by default. Other repositories are specified with either repository-url/image:tag or repository-url/image@digest. Default: - `lloesche/valheim-server <https://hub.docker.com/r/lloesche/valheim-server>`_
        :param log_group: Valheim Server log Group. Default: - Create the new AWS Cloudwatch Log Group for Valheim Server.
        :param memory_limit_mib: The amount (in MiB) of memory used by the task. For tasks using the Fargate launch type, this field is required and you must use one of the following values, which determines your range of valid values for the cpu parameter: 512 (0.5 GB), 1024 (1 GB), 2048 (2 GB) - Available cpu values: 256 (.25 vCPU) 1024 (1 GB), 2048 (2 GB), 3072 (3 GB), 4096 (4 GB) - Available cpu values: 512 (.5 vCPU) 2048 (2 GB), 3072 (3 GB), 4096 (4 GB), 5120 (5 GB), 6144 (6 GB), 7168 (7 GB), 8192 (8 GB) - Available cpu values: 1024 (1 vCPU) Between 4096 (4 GB) and 16384 (16 GB) in increments of 1024 (1 GB) - Available cpu values: 2048 (2 vCPU) Between 8192 (8 GB) and 30720 (30 GB) in increments of 1024 (1 GB) - Available cpu values: 4096 (4 vCPU) Default: 2048
        :param schedules: Running schedules. Default: - Always running.
        :param vpc: The VPC where your ECS instances will be running or your ENIs will be deployed. Default: - creates a new VPC with two AZs
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if backup_plan is not None:
            self._values["backup_plan"] = backup_plan
        if container_path is not None:
            self._values["container_path"] = container_path
        if cpu is not None:
            self._values["cpu"] = cpu
        if desired_count is not None:
            self._values["desired_count"] = desired_count
        if environment is not None:
            self._values["environment"] = environment
        if file_system is not None:
            self._values["file_system"] = file_system
        if image is not None:
            self._values["image"] = image
        if log_group is not None:
            self._values["log_group"] = log_group
        if memory_limit_mib is not None:
            self._values["memory_limit_mib"] = memory_limit_mib
        if schedules is not None:
            self._values["schedules"] = schedules
        if vpc is not None:
            self._values["vpc"] = vpc

    @builtins.property
    def backup_plan(self) -> typing.Optional[aws_cdk.aws_backup.BackupPlan]:
        '''AWS Backup plan for EFS.

        :default: - Hourly backup with 3 days retension.
        '''
        result = self._values.get("backup_plan")
        return typing.cast(typing.Optional[aws_cdk.aws_backup.BackupPlan], result)

    @builtins.property
    def container_path(self) -> typing.Optional[builtins.str]:
        '''The path on the container to mount the host volume at.

        :default: - /config/
        '''
        result = self._values.get("container_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cpu(self) -> typing.Optional[jsii.Number]:
        '''The number of cpu units used by the task.

        For tasks using the Fargate launch type,
        this field is required and you must use one of the following values,
        which determines your range of valid values for the memory parameter:

        256 (.25 vCPU) - Available memory values: 512 (0.5 GB), 1024 (1 GB), 2048 (2 GB)

        512 (.5 vCPU) - Available memory values: 1024 (1 GB), 2048 (2 GB), 3072 (3 GB), 4096 (4 GB)

        1024 (1 vCPU) - Available memory values: 2048 (2 GB), 3072 (3 GB), 4096 (4 GB), 5120 (5 GB), 6144 (6 GB), 7168 (7 GB), 8192 (8 GB)

        2048 (2 vCPU) - Available memory values: Between 4096 (4 GB) and 16384 (16 GB) in increments of 1024 (1 GB)

        4096 (4 vCPU) - Available memory values: Between 8192 (8 GB) and 30720 (30 GB) in increments of 1024 (1 GB)

        :default: 1024
        '''
        result = self._values.get("cpu")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def desired_count(self) -> typing.Optional[jsii.Number]:
        '''Desired count of Fargate container.

        Set 0 for maintenance.

        :default: - 1
        '''
        result = self._values.get("desired_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def environment(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The environment variables to pass to the container.

        :default: - No environment variables.
        '''
        result = self._values.get("environment")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def file_system(self) -> typing.Optional[aws_cdk.aws_efs.FileSystem]:
        '''Persistent storage for save data.

        :default: - Amazon EFS for default persistent storage.
        '''
        result = self._values.get("file_system")
        return typing.cast(typing.Optional[aws_cdk.aws_efs.FileSystem], result)

    @builtins.property
    def image(self) -> typing.Optional[aws_cdk.aws_ecs.ContainerImage]:
        '''The image used to start a container.

        This string is passed directly to the Docker daemon.
        Images in the Docker Hub registry are available by default.
        Other repositories are specified with either repository-url/image:tag or repository-url/image@digest.

        :default: - `lloesche/valheim-server <https://hub.docker.com/r/lloesche/valheim-server>`_
        '''
        result = self._values.get("image")
        return typing.cast(typing.Optional[aws_cdk.aws_ecs.ContainerImage], result)

    @builtins.property
    def log_group(self) -> typing.Optional[aws_cdk.aws_ecs.LogDriver]:
        '''Valheim Server log Group.

        :default: - Create the new AWS Cloudwatch Log Group for Valheim Server.
        '''
        result = self._values.get("log_group")
        return typing.cast(typing.Optional[aws_cdk.aws_ecs.LogDriver], result)

    @builtins.property
    def memory_limit_mib(self) -> typing.Optional[jsii.Number]:
        '''The amount (in MiB) of memory used by the task.

        For tasks using the Fargate launch type,
        this field is required and you must use one of the following values, which determines your range of valid values for the cpu parameter:

        512 (0.5 GB), 1024 (1 GB), 2048 (2 GB) - Available cpu values: 256 (.25 vCPU)

        1024 (1 GB), 2048 (2 GB), 3072 (3 GB), 4096 (4 GB) - Available cpu values: 512 (.5 vCPU)

        2048 (2 GB), 3072 (3 GB), 4096 (4 GB), 5120 (5 GB), 6144 (6 GB), 7168 (7 GB), 8192 (8 GB) - Available cpu values: 1024 (1 vCPU)

        Between 4096 (4 GB) and 16384 (16 GB) in increments of 1024 (1 GB) - Available cpu values: 2048 (2 vCPU)

        Between 8192 (8 GB) and 30720 (30 GB) in increments of 1024 (1 GB) - Available cpu values: 4096 (4 vCPU)

        :default: 2048
        '''
        result = self._values.get("memory_limit_mib")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def schedules(
        self,
    ) -> typing.Optional[typing.List["ValheimWorldScalingScheduleProps"]]:
        '''Running schedules.

        :default: - Always running.
        '''
        result = self._values.get("schedules")
        return typing.cast(typing.Optional[typing.List["ValheimWorldScalingScheduleProps"]], result)

    @builtins.property
    def vpc(self) -> typing.Optional[aws_cdk.aws_ec2.IVpc]:
        '''The VPC where your ECS instances will be running or your ENIs will be deployed.

        :default: - creates a new VPC with two AZs
        '''
        result = self._values.get("vpc")
        return typing.cast(typing.Optional[aws_cdk.aws_ec2.IVpc], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ValheimWorldProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ValheimWorldScalingSchedule(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-valheim.ValheimWorldScalingSchedule",
):
    '''Represents the schedule to determine when the server starts or terminates.'''

    def __init__(
        self,
        *,
        start: aws_cdk.aws_applicationautoscaling.CronOptions,
        stop: aws_cdk.aws_applicationautoscaling.CronOptions,
    ) -> None:
        '''
        :param start: Options to configure a cron expression for server for server launching schedule. All fields are strings so you can use complex expressions. Absence of a field implies '*' or '?', whichever one is appropriate. Only comma separated numbers and hypens are allowed.
        :param stop: Options to configure a cron expression for server zero-scale schedule. All fields are strings so you can use complex expressions. Absence of a field implies '*' or '?', whichever one is appropriate. Only comma separated numbers and hypens are allowed.
        '''
        schedule = ValheimWorldScalingScheduleProps(start=start, stop=stop)

        jsii.create(self.__class__, self, [schedule])

    @jsii.member(jsii_name="toCronOptions")
    def to_cron_options(self) -> aws_cdk.aws_applicationautoscaling.CronOptions:
        '''Returns the cron options merged properties for both start and stop.'''
        return typing.cast(aws_cdk.aws_applicationautoscaling.CronOptions, jsii.invoke(self, "toCronOptions", []))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="start")
    def start(self) -> aws_cdk.aws_applicationautoscaling.CronOptions:
        '''Options to configure a cron expression for server for server launching schedule.

        All fields are strings so you can use complex expressions. Absence of
        a field implies '*' or '?', whichever one is appropriate. Only comma
        separated numbers and hypens are allowed.
        '''
        return typing.cast(aws_cdk.aws_applicationautoscaling.CronOptions, jsii.get(self, "start"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="stop")
    def stop(self) -> aws_cdk.aws_applicationautoscaling.CronOptions:
        '''Options to configure a cron expression for server zero-scale schedule.

        All fields are strings so you can use complex expressions. Absence of
        a field implies '*' or '?', whichever one is appropriate. Only comma
        separated numbers and hypens are allowed.
        '''
        return typing.cast(aws_cdk.aws_applicationautoscaling.CronOptions, jsii.get(self, "stop"))


@jsii.data_type(
    jsii_type="cdk-valheim.ValheimWorldScalingScheduleProps",
    jsii_struct_bases=[],
    name_mapping={"start": "start", "stop": "stop"},
)
class ValheimWorldScalingScheduleProps:
    def __init__(
        self,
        *,
        start: aws_cdk.aws_applicationautoscaling.CronOptions,
        stop: aws_cdk.aws_applicationautoscaling.CronOptions,
    ) -> None:
        '''Options for ValheimWorldScalingSchedule.

        :param start: Options to configure a cron expression for server for server launching schedule. All fields are strings so you can use complex expressions. Absence of a field implies '*' or '?', whichever one is appropriate. Only comma separated numbers and hypens are allowed.
        :param stop: Options to configure a cron expression for server zero-scale schedule. All fields are strings so you can use complex expressions. Absence of a field implies '*' or '?', whichever one is appropriate. Only comma separated numbers and hypens are allowed.
        '''
        if isinstance(start, dict):
            start = aws_cdk.aws_applicationautoscaling.CronOptions(**start)
        if isinstance(stop, dict):
            stop = aws_cdk.aws_applicationautoscaling.CronOptions(**stop)
        self._values: typing.Dict[str, typing.Any] = {
            "start": start,
            "stop": stop,
        }

    @builtins.property
    def start(self) -> aws_cdk.aws_applicationautoscaling.CronOptions:
        '''Options to configure a cron expression for server for server launching schedule.

        All fields are strings so you can use complex expressions. Absence of
        a field implies '*' or '?', whichever one is appropriate. Only comma
        separated numbers and hypens are allowed.
        '''
        result = self._values.get("start")
        assert result is not None, "Required property 'start' is missing"
        return typing.cast(aws_cdk.aws_applicationautoscaling.CronOptions, result)

    @builtins.property
    def stop(self) -> aws_cdk.aws_applicationautoscaling.CronOptions:
        '''Options to configure a cron expression for server zero-scale schedule.

        All fields are strings so you can use complex expressions. Absence of
        a field implies '*' or '?', whichever one is appropriate. Only comma
        separated numbers and hypens are allowed.
        '''
        result = self._values.get("stop")
        assert result is not None, "Required property 'stop' is missing"
        return typing.cast(aws_cdk.aws_applicationautoscaling.CronOptions, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ValheimWorldScalingScheduleProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "ValheimWorld",
    "ValheimWorldProps",
    "ValheimWorldScalingSchedule",
    "ValheimWorldScalingScheduleProps",
]

publication.publish()

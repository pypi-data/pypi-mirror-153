import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from .._jsii import *

import aws_cdk
import constructs


class Ttl(constructs.Construct, metaclass=jsii.JSIIMeta, jsii_type="pwed-cdk.ttl.Ttl"):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        ttl: aws_cdk.Duration,
        poll_interval: typing.Optional[aws_cdk.Duration] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param ttl: 
        :param poll_interval: 

        :stability: experimental
        '''
        props = TtlProps(ttl=ttl, poll_interval=poll_interval)

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="pwed-cdk.ttl.TtlProps",
    jsii_struct_bases=[],
    name_mapping={"ttl": "ttl", "poll_interval": "pollInterval"},
)
class TtlProps:
    def __init__(
        self,
        *,
        ttl: aws_cdk.Duration,
        poll_interval: typing.Optional[aws_cdk.Duration] = None,
    ) -> None:
        '''
        :param ttl: 
        :param poll_interval: 

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "ttl": ttl,
        }
        if poll_interval is not None:
            self._values["poll_interval"] = poll_interval

    @builtins.property
    def ttl(self) -> aws_cdk.Duration:
        '''
        :stability: experimental
        '''
        result = self._values.get("ttl")
        assert result is not None, "Required property 'ttl' is missing"
        return typing.cast(aws_cdk.Duration, result)

    @builtins.property
    def poll_interval(self) -> typing.Optional[aws_cdk.Duration]:
        '''
        :stability: experimental
        '''
        result = self._values.get("poll_interval")
        return typing.cast(typing.Optional[aws_cdk.Duration], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TtlProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "Ttl",
    "TtlProps",
]

publication.publish()

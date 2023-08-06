'''
Toumoro cdk userpool and client
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

import aws_cdk.aws_cognito
import constructs


class TmUserPoolClient(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@toumoro-cdk/cognito.TmUserPoolClient",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        user_pool_props: typing.Optional[aws_cdk.aws_cognito.UserPoolProps] = None,
        user_pool_client_props: typing.Any = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param user_pool_props: -
        :param user_pool_client_props: -
        '''
        jsii.create(self.__class__, self, [scope, id, user_pool_props, user_pool_client_props])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="defaultUserPoolClientProps")
    def default_user_pool_client_props(self) -> typing.Any:
        return typing.cast(typing.Any, jsii.get(self, "defaultUserPoolClientProps"))

    @default_user_pool_client_props.setter
    def default_user_pool_client_props(self, value: typing.Any) -> None:
        jsii.set(self, "defaultUserPoolClientProps", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="defaultUserPoolProps")
    def default_user_pool_props(self) -> aws_cdk.aws_cognito.UserPoolProps:
        return typing.cast(aws_cdk.aws_cognito.UserPoolProps, jsii.get(self, "defaultUserPoolProps"))

    @default_user_pool_props.setter
    def default_user_pool_props(self, value: aws_cdk.aws_cognito.UserPoolProps) -> None:
        jsii.set(self, "defaultUserPoolProps", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="userPool")
    def user_pool(self) -> aws_cdk.aws_cognito.UserPool:
        return typing.cast(aws_cdk.aws_cognito.UserPool, jsii.get(self, "userPool"))

    @user_pool.setter
    def user_pool(self, value: aws_cdk.aws_cognito.UserPool) -> None:
        jsii.set(self, "userPool", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="userPoolClient")
    def user_pool_client(self) -> aws_cdk.aws_cognito.UserPoolClient:
        return typing.cast(aws_cdk.aws_cognito.UserPoolClient, jsii.get(self, "userPoolClient"))

    @user_pool_client.setter
    def user_pool_client(self, value: aws_cdk.aws_cognito.UserPoolClient) -> None:
        jsii.set(self, "userPoolClient", value)


__all__ = [
    "TmUserPoolClient",
]

publication.publish()

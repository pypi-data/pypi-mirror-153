import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from ._jsii import *

import cdktf
import constructs


class Account(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="hashicorp_boundary.Account",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/boundary/r/account boundary_account}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        auth_method_id: builtins.str,
        type: builtins.str,
        description: typing.Optional[builtins.str] = None,
        login_name: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        password: typing.Optional[builtins.str] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/boundary/r/account boundary_account} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param auth_method_id: The resource ID for the auth method. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/account#auth_method_id Account#auth_method_id}
        :param type: The resource type. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/account#type Account#type}
        :param description: The account description. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/account#description Account#description}
        :param login_name: The login name for this account. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/account#login_name Account#login_name}
        :param name: The account name. Defaults to the resource name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/account#name Account#name}
        :param password: The account password. Only set on create, changes will not be reflected when updating account. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/account#password Account#password}
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        '''
        config = AccountConfig(
            auth_method_id=auth_method_id,
            type=type,
            description=description,
            login_name=login_name,
            name=name,
            password=password,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetLoginName")
    def reset_login_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLoginName", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetPassword")
    def reset_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPassword", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="authMethodIdInput")
    def auth_method_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authMethodIdInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="loginNameInput")
    def login_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "loginNameInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="authMethodId")
    def auth_method_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authMethodId"))

    @auth_method_id.setter
    def auth_method_id(self, value: builtins.str) -> None:
        jsii.set(self, "authMethodId", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        jsii.set(self, "description", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="loginName")
    def login_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "loginName"))

    @login_name.setter
    def login_name(self, value: builtins.str) -> None:
        jsii.set(self, "loginName", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        jsii.set(self, "password", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        jsii.set(self, "type", value)


@jsii.data_type(
    jsii_type="hashicorp_boundary.AccountConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "auth_method_id": "authMethodId",
        "type": "type",
        "description": "description",
        "login_name": "loginName",
        "name": "name",
        "password": "password",
    },
)
class AccountConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        auth_method_id: builtins.str,
        type: builtins.str,
        description: typing.Optional[builtins.str] = None,
        login_name: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        password: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param auth_method_id: The resource ID for the auth method. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/account#auth_method_id Account#auth_method_id}
        :param type: The resource type. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/account#type Account#type}
        :param description: The account description. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/account#description Account#description}
        :param login_name: The login name for this account. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/account#login_name Account#login_name}
        :param name: The account name. Defaults to the resource name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/account#name Account#name}
        :param password: The account password. Only set on create, changes will not be reflected when updating account. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/account#password Account#password}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        self._values: typing.Dict[str, typing.Any] = {
            "auth_method_id": auth_method_id,
            "type": type,
        }
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if description is not None:
            self._values["description"] = description
        if login_name is not None:
            self._values["login_name"] = login_name
        if name is not None:
            self._values["name"] = name
        if password is not None:
            self._values["password"] = password

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[cdktf.ITerraformDependable]], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[cdktf.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[cdktf.TerraformProvider], result)

    @builtins.property
    def auth_method_id(self) -> builtins.str:
        '''The resource ID for the auth method.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/account#auth_method_id Account#auth_method_id}
        '''
        result = self._values.get("auth_method_id")
        assert result is not None, "Required property 'auth_method_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''The resource type.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/account#type Account#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The account description.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/account#description Account#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def login_name(self) -> typing.Optional[builtins.str]:
        '''The login name for this account.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/account#login_name Account#login_name}
        '''
        result = self._values.get("login_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The account name. Defaults to the resource name.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/account#name Account#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''The account password. Only set on create, changes will not be reflected when updating account.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/account#password Account#password}
        '''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccountConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccountOidc(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="hashicorp_boundary.AccountOidc",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/boundary/r/account_oidc boundary_account_oidc}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        auth_method_id: builtins.str,
        description: typing.Optional[builtins.str] = None,
        issuer: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        subject: typing.Optional[builtins.str] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/boundary/r/account_oidc boundary_account_oidc} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param auth_method_id: The resource ID for the auth method. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/account_oidc#auth_method_id AccountOidc#auth_method_id}
        :param description: The account description. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/account_oidc#description AccountOidc#description}
        :param issuer: The OIDC issuer. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/account_oidc#issuer AccountOidc#issuer}
        :param name: The account name. Defaults to the resource name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/account_oidc#name AccountOidc#name}
        :param subject: The OIDC subject. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/account_oidc#subject AccountOidc#subject}
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        '''
        config = AccountOidcConfig(
            auth_method_id=auth_method_id,
            description=description,
            issuer=issuer,
            name=name,
            subject=subject,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetIssuer")
    def reset_issuer(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIssuer", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetSubject")
    def reset_subject(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubject", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="authMethodIdInput")
    def auth_method_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authMethodIdInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="issuerInput")
    def issuer_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "issuerInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="subjectInput")
    def subject_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subjectInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="authMethodId")
    def auth_method_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authMethodId"))

    @auth_method_id.setter
    def auth_method_id(self, value: builtins.str) -> None:
        jsii.set(self, "authMethodId", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        jsii.set(self, "description", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="issuer")
    def issuer(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "issuer"))

    @issuer.setter
    def issuer(self, value: builtins.str) -> None:
        jsii.set(self, "issuer", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="subject")
    def subject(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subject"))

    @subject.setter
    def subject(self, value: builtins.str) -> None:
        jsii.set(self, "subject", value)


@jsii.data_type(
    jsii_type="hashicorp_boundary.AccountOidcConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "auth_method_id": "authMethodId",
        "description": "description",
        "issuer": "issuer",
        "name": "name",
        "subject": "subject",
    },
)
class AccountOidcConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        auth_method_id: builtins.str,
        description: typing.Optional[builtins.str] = None,
        issuer: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        subject: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param auth_method_id: The resource ID for the auth method. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/account_oidc#auth_method_id AccountOidc#auth_method_id}
        :param description: The account description. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/account_oidc#description AccountOidc#description}
        :param issuer: The OIDC issuer. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/account_oidc#issuer AccountOidc#issuer}
        :param name: The account name. Defaults to the resource name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/account_oidc#name AccountOidc#name}
        :param subject: The OIDC subject. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/account_oidc#subject AccountOidc#subject}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        self._values: typing.Dict[str, typing.Any] = {
            "auth_method_id": auth_method_id,
        }
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if description is not None:
            self._values["description"] = description
        if issuer is not None:
            self._values["issuer"] = issuer
        if name is not None:
            self._values["name"] = name
        if subject is not None:
            self._values["subject"] = subject

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[cdktf.ITerraformDependable]], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[cdktf.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[cdktf.TerraformProvider], result)

    @builtins.property
    def auth_method_id(self) -> builtins.str:
        '''The resource ID for the auth method.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/account_oidc#auth_method_id AccountOidc#auth_method_id}
        '''
        result = self._values.get("auth_method_id")
        assert result is not None, "Required property 'auth_method_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The account description.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/account_oidc#description AccountOidc#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def issuer(self) -> typing.Optional[builtins.str]:
        '''The OIDC issuer.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/account_oidc#issuer AccountOidc#issuer}
        '''
        result = self._values.get("issuer")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The account name. Defaults to the resource name.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/account_oidc#name AccountOidc#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subject(self) -> typing.Optional[builtins.str]:
        '''The OIDC subject.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/account_oidc#subject AccountOidc#subject}
        '''
        result = self._values.get("subject")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccountOidcConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccountPassword(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="hashicorp_boundary.AccountPassword",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/boundary/r/account_password boundary_account_password}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        auth_method_id: builtins.str,
        type: builtins.str,
        description: typing.Optional[builtins.str] = None,
        login_name: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        password: typing.Optional[builtins.str] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/boundary/r/account_password boundary_account_password} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param auth_method_id: The resource ID for the auth method. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/account_password#auth_method_id AccountPassword#auth_method_id}
        :param type: The resource type. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/account_password#type AccountPassword#type}
        :param description: The account description. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/account_password#description AccountPassword#description}
        :param login_name: The login name for this account. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/account_password#login_name AccountPassword#login_name}
        :param name: The account name. Defaults to the resource name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/account_password#name AccountPassword#name}
        :param password: The account password. Only set on create, changes will not be reflected when updating account. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/account_password#password AccountPassword#password}
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        '''
        config = AccountPasswordConfig(
            auth_method_id=auth_method_id,
            type=type,
            description=description,
            login_name=login_name,
            name=name,
            password=password,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetLoginName")
    def reset_login_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLoginName", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetPassword")
    def reset_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPassword", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="authMethodIdInput")
    def auth_method_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authMethodIdInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="loginNameInput")
    def login_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "loginNameInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="authMethodId")
    def auth_method_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authMethodId"))

    @auth_method_id.setter
    def auth_method_id(self, value: builtins.str) -> None:
        jsii.set(self, "authMethodId", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        jsii.set(self, "description", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="loginName")
    def login_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "loginName"))

    @login_name.setter
    def login_name(self, value: builtins.str) -> None:
        jsii.set(self, "loginName", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        jsii.set(self, "password", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        jsii.set(self, "type", value)


@jsii.data_type(
    jsii_type="hashicorp_boundary.AccountPasswordConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "auth_method_id": "authMethodId",
        "type": "type",
        "description": "description",
        "login_name": "loginName",
        "name": "name",
        "password": "password",
    },
)
class AccountPasswordConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        auth_method_id: builtins.str,
        type: builtins.str,
        description: typing.Optional[builtins.str] = None,
        login_name: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        password: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param auth_method_id: The resource ID for the auth method. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/account_password#auth_method_id AccountPassword#auth_method_id}
        :param type: The resource type. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/account_password#type AccountPassword#type}
        :param description: The account description. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/account_password#description AccountPassword#description}
        :param login_name: The login name for this account. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/account_password#login_name AccountPassword#login_name}
        :param name: The account name. Defaults to the resource name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/account_password#name AccountPassword#name}
        :param password: The account password. Only set on create, changes will not be reflected when updating account. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/account_password#password AccountPassword#password}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        self._values: typing.Dict[str, typing.Any] = {
            "auth_method_id": auth_method_id,
            "type": type,
        }
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if description is not None:
            self._values["description"] = description
        if login_name is not None:
            self._values["login_name"] = login_name
        if name is not None:
            self._values["name"] = name
        if password is not None:
            self._values["password"] = password

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[cdktf.ITerraformDependable]], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[cdktf.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[cdktf.TerraformProvider], result)

    @builtins.property
    def auth_method_id(self) -> builtins.str:
        '''The resource ID for the auth method.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/account_password#auth_method_id AccountPassword#auth_method_id}
        '''
        result = self._values.get("auth_method_id")
        assert result is not None, "Required property 'auth_method_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''The resource type.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/account_password#type AccountPassword#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The account description.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/account_password#description AccountPassword#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def login_name(self) -> typing.Optional[builtins.str]:
        '''The login name for this account.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/account_password#login_name AccountPassword#login_name}
        '''
        result = self._values.get("login_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The account name. Defaults to the resource name.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/account_password#name AccountPassword#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''The account password. Only set on create, changes will not be reflected when updating account.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/account_password#password AccountPassword#password}
        '''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccountPasswordConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AuthMethod(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="hashicorp_boundary.AuthMethod",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/boundary/r/auth_method boundary_auth_method}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        scope_id: builtins.str,
        type: builtins.str,
        description: typing.Optional[builtins.str] = None,
        min_login_name_length: typing.Optional[jsii.Number] = None,
        min_password_length: typing.Optional[jsii.Number] = None,
        name: typing.Optional[builtins.str] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/boundary/r/auth_method boundary_auth_method} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param scope_id: The scope ID. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/auth_method#scope_id AuthMethod#scope_id}
        :param type: The resource type. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/auth_method#type AuthMethod#type}
        :param description: The auth method description. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/auth_method#description AuthMethod#description}
        :param min_login_name_length: The minimum login name length. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/auth_method#min_login_name_length AuthMethod#min_login_name_length}
        :param min_password_length: The minimum password length. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/auth_method#min_password_length AuthMethod#min_password_length}
        :param name: The auth method name. Defaults to the resource name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/auth_method#name AuthMethod#name}
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        '''
        config = AuthMethodConfig(
            scope_id=scope_id,
            type=type,
            description=description,
            min_login_name_length=min_login_name_length,
            min_password_length=min_password_length,
            name=name,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetMinLoginNameLength")
    def reset_min_login_name_length(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinLoginNameLength", []))

    @jsii.member(jsii_name="resetMinPasswordLength")
    def reset_min_password_length(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinPasswordLength", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="minLoginNameLengthInput")
    def min_login_name_length_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minLoginNameLengthInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="minPasswordLengthInput")
    def min_password_length_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minPasswordLengthInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="scopeIdInput")
    def scope_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scopeIdInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        jsii.set(self, "description", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="minLoginNameLength")
    def min_login_name_length(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minLoginNameLength"))

    @min_login_name_length.setter
    def min_login_name_length(self, value: jsii.Number) -> None:
        jsii.set(self, "minLoginNameLength", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="minPasswordLength")
    def min_password_length(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minPasswordLength"))

    @min_password_length.setter
    def min_password_length(self, value: jsii.Number) -> None:
        jsii.set(self, "minPasswordLength", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="scopeId")
    def scope_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scopeId"))

    @scope_id.setter
    def scope_id(self, value: builtins.str) -> None:
        jsii.set(self, "scopeId", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        jsii.set(self, "type", value)


@jsii.data_type(
    jsii_type="hashicorp_boundary.AuthMethodConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "scope_id": "scopeId",
        "type": "type",
        "description": "description",
        "min_login_name_length": "minLoginNameLength",
        "min_password_length": "minPasswordLength",
        "name": "name",
    },
)
class AuthMethodConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        scope_id: builtins.str,
        type: builtins.str,
        description: typing.Optional[builtins.str] = None,
        min_login_name_length: typing.Optional[jsii.Number] = None,
        min_password_length: typing.Optional[jsii.Number] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param scope_id: The scope ID. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/auth_method#scope_id AuthMethod#scope_id}
        :param type: The resource type. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/auth_method#type AuthMethod#type}
        :param description: The auth method description. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/auth_method#description AuthMethod#description}
        :param min_login_name_length: The minimum login name length. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/auth_method#min_login_name_length AuthMethod#min_login_name_length}
        :param min_password_length: The minimum password length. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/auth_method#min_password_length AuthMethod#min_password_length}
        :param name: The auth method name. Defaults to the resource name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/auth_method#name AuthMethod#name}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        self._values: typing.Dict[str, typing.Any] = {
            "scope_id": scope_id,
            "type": type,
        }
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if description is not None:
            self._values["description"] = description
        if min_login_name_length is not None:
            self._values["min_login_name_length"] = min_login_name_length
        if min_password_length is not None:
            self._values["min_password_length"] = min_password_length
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[cdktf.ITerraformDependable]], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[cdktf.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[cdktf.TerraformProvider], result)

    @builtins.property
    def scope_id(self) -> builtins.str:
        '''The scope ID.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/auth_method#scope_id AuthMethod#scope_id}
        '''
        result = self._values.get("scope_id")
        assert result is not None, "Required property 'scope_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''The resource type.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/auth_method#type AuthMethod#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The auth method description.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/auth_method#description AuthMethod#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def min_login_name_length(self) -> typing.Optional[jsii.Number]:
        '''The minimum login name length.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/auth_method#min_login_name_length AuthMethod#min_login_name_length}
        '''
        result = self._values.get("min_login_name_length")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_password_length(self) -> typing.Optional[jsii.Number]:
        '''The minimum password length.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/auth_method#min_password_length AuthMethod#min_password_length}
        '''
        result = self._values.get("min_password_length")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The auth method name. Defaults to the resource name.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/auth_method#name AuthMethod#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AuthMethodConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AuthMethodOidc(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="hashicorp_boundary.AuthMethodOidc",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/boundary/r/auth_method_oidc boundary_auth_method_oidc}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        scope_id: builtins.str,
        account_claim_maps: typing.Optional[typing.Sequence[builtins.str]] = None,
        allowed_audiences: typing.Optional[typing.Sequence[builtins.str]] = None,
        api_url_prefix: typing.Optional[builtins.str] = None,
        callback_url: typing.Optional[builtins.str] = None,
        claims_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
        client_id: typing.Optional[builtins.str] = None,
        client_secret: typing.Optional[builtins.str] = None,
        client_secret_hmac: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        disable_discovered_config_validation: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        idp_ca_certs: typing.Optional[typing.Sequence[builtins.str]] = None,
        is_primary_for_scope: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        issuer: typing.Optional[builtins.str] = None,
        max_age: typing.Optional[jsii.Number] = None,
        name: typing.Optional[builtins.str] = None,
        signing_algorithms: typing.Optional[typing.Sequence[builtins.str]] = None,
        state: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/boundary/r/auth_method_oidc boundary_auth_method_oidc} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param scope_id: The scope ID. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/auth_method_oidc#scope_id AuthMethodOidc#scope_id}
        :param account_claim_maps: Account claim maps for the to_claim of sub. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/auth_method_oidc#account_claim_maps AuthMethodOidc#account_claim_maps}
        :param allowed_audiences: Audiences for which the provider responses will be allowed. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/auth_method_oidc#allowed_audiences AuthMethodOidc#allowed_audiences}
        :param api_url_prefix: The API prefix to use when generating callback URLs for the provider. Should be set to an address at which the provider can reach back to the controller. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/auth_method_oidc#api_url_prefix AuthMethodOidc#api_url_prefix}
        :param callback_url: The URL that should be provided to the IdP for callbacks. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/auth_method_oidc#callback_url AuthMethodOidc#callback_url}
        :param claims_scopes: Claims scopes. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/auth_method_oidc#claims_scopes AuthMethodOidc#claims_scopes}
        :param client_id: The client ID assigned to this auth method from the provider. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/auth_method_oidc#client_id AuthMethodOidc#client_id}
        :param client_secret: The secret key assigned to this auth method from the provider. Once set, only the hash will be kept and the original value can be removed from configuration. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/auth_method_oidc#client_secret AuthMethodOidc#client_secret}
        :param client_secret_hmac: The HMAC of the client secret returned by the Boundary controller, which is used for comparison after initial setting of the value. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/auth_method_oidc#client_secret_hmac AuthMethodOidc#client_secret_hmac}
        :param description: The auth method description. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/auth_method_oidc#description AuthMethodOidc#description}
        :param disable_discovered_config_validation: Disables validation logic ensuring that the OIDC provider's information from its discovery endpoint matches the information here. The validation is only performed at create or update time. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/auth_method_oidc#disable_discovered_config_validation AuthMethodOidc#disable_discovered_config_validation}
        :param idp_ca_certs: A list of CA certificates to trust when validating the IdP's token signatures. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/auth_method_oidc#idp_ca_certs AuthMethodOidc#idp_ca_certs}
        :param is_primary_for_scope: When true, makes this auth method the primary auth method for the scope in which it resides. The primary auth method for a scope means the the user will be automatically created when they login using an OIDC account. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/auth_method_oidc#is_primary_for_scope AuthMethodOidc#is_primary_for_scope}
        :param issuer: The issuer corresponding to the provider, which must match the issuer field in generated tokens. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/auth_method_oidc#issuer AuthMethodOidc#issuer}
        :param max_age: The max age to provide to the provider, indicating how much time is allowed to have passed since the last authentication before the user is challenged again. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/auth_method_oidc#max_age AuthMethodOidc#max_age}
        :param name: The auth method name. Defaults to the resource name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/auth_method_oidc#name AuthMethodOidc#name}
        :param signing_algorithms: Allowed signing algorithms for the provider's issued tokens. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/auth_method_oidc#signing_algorithms AuthMethodOidc#signing_algorithms}
        :param state: Can be one of 'inactive', 'active-private', or 'active-public'. Currently automatically set to active-public. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/auth_method_oidc#state AuthMethodOidc#state}
        :param type: The type of auth method; hardcoded. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/auth_method_oidc#type AuthMethodOidc#type}
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        '''
        config = AuthMethodOidcConfig(
            scope_id=scope_id,
            account_claim_maps=account_claim_maps,
            allowed_audiences=allowed_audiences,
            api_url_prefix=api_url_prefix,
            callback_url=callback_url,
            claims_scopes=claims_scopes,
            client_id=client_id,
            client_secret=client_secret,
            client_secret_hmac=client_secret_hmac,
            description=description,
            disable_discovered_config_validation=disable_discovered_config_validation,
            idp_ca_certs=idp_ca_certs,
            is_primary_for_scope=is_primary_for_scope,
            issuer=issuer,
            max_age=max_age,
            name=name,
            signing_algorithms=signing_algorithms,
            state=state,
            type=type,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="resetAccountClaimMaps")
    def reset_account_claim_maps(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccountClaimMaps", []))

    @jsii.member(jsii_name="resetAllowedAudiences")
    def reset_allowed_audiences(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedAudiences", []))

    @jsii.member(jsii_name="resetApiUrlPrefix")
    def reset_api_url_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApiUrlPrefix", []))

    @jsii.member(jsii_name="resetCallbackUrl")
    def reset_callback_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCallbackUrl", []))

    @jsii.member(jsii_name="resetClaimsScopes")
    def reset_claims_scopes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClaimsScopes", []))

    @jsii.member(jsii_name="resetClientId")
    def reset_client_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientId", []))

    @jsii.member(jsii_name="resetClientSecret")
    def reset_client_secret(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientSecret", []))

    @jsii.member(jsii_name="resetClientSecretHmac")
    def reset_client_secret_hmac(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientSecretHmac", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetDisableDiscoveredConfigValidation")
    def reset_disable_discovered_config_validation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisableDiscoveredConfigValidation", []))

    @jsii.member(jsii_name="resetIdpCaCerts")
    def reset_idp_ca_certs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdpCaCerts", []))

    @jsii.member(jsii_name="resetIsPrimaryForScope")
    def reset_is_primary_for_scope(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsPrimaryForScope", []))

    @jsii.member(jsii_name="resetIssuer")
    def reset_issuer(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIssuer", []))

    @jsii.member(jsii_name="resetMaxAge")
    def reset_max_age(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxAge", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetSigningAlgorithms")
    def reset_signing_algorithms(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSigningAlgorithms", []))

    @jsii.member(jsii_name="resetState")
    def reset_state(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetState", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="accountClaimMapsInput")
    def account_claim_maps_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "accountClaimMapsInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="allowedAudiencesInput")
    def allowed_audiences_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedAudiencesInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="apiUrlPrefixInput")
    def api_url_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apiUrlPrefixInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="callbackUrlInput")
    def callback_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "callbackUrlInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="claimsScopesInput")
    def claims_scopes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "claimsScopesInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="clientIdInput")
    def client_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientIdInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="clientSecretHmacInput")
    def client_secret_hmac_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientSecretHmacInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="clientSecretInput")
    def client_secret_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientSecretInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="disableDiscoveredConfigValidationInput")
    def disable_discovered_config_validation_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "disableDiscoveredConfigValidationInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="idpCaCertsInput")
    def idp_ca_certs_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "idpCaCertsInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="isPrimaryForScopeInput")
    def is_primary_for_scope_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "isPrimaryForScopeInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="issuerInput")
    def issuer_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "issuerInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="maxAgeInput")
    def max_age_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxAgeInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="scopeIdInput")
    def scope_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scopeIdInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="signingAlgorithmsInput")
    def signing_algorithms_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "signingAlgorithmsInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="stateInput")
    def state_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stateInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="accountClaimMaps")
    def account_claim_maps(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "accountClaimMaps"))

    @account_claim_maps.setter
    def account_claim_maps(self, value: typing.List[builtins.str]) -> None:
        jsii.set(self, "accountClaimMaps", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="allowedAudiences")
    def allowed_audiences(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedAudiences"))

    @allowed_audiences.setter
    def allowed_audiences(self, value: typing.List[builtins.str]) -> None:
        jsii.set(self, "allowedAudiences", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="apiUrlPrefix")
    def api_url_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "apiUrlPrefix"))

    @api_url_prefix.setter
    def api_url_prefix(self, value: builtins.str) -> None:
        jsii.set(self, "apiUrlPrefix", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="callbackUrl")
    def callback_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "callbackUrl"))

    @callback_url.setter
    def callback_url(self, value: builtins.str) -> None:
        jsii.set(self, "callbackUrl", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="claimsScopes")
    def claims_scopes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "claimsScopes"))

    @claims_scopes.setter
    def claims_scopes(self, value: typing.List[builtins.str]) -> None:
        jsii.set(self, "claimsScopes", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientId"))

    @client_id.setter
    def client_id(self, value: builtins.str) -> None:
        jsii.set(self, "clientId", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="clientSecret")
    def client_secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientSecret"))

    @client_secret.setter
    def client_secret(self, value: builtins.str) -> None:
        jsii.set(self, "clientSecret", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="clientSecretHmac")
    def client_secret_hmac(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientSecretHmac"))

    @client_secret_hmac.setter
    def client_secret_hmac(self, value: builtins.str) -> None:
        jsii.set(self, "clientSecretHmac", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        jsii.set(self, "description", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="disableDiscoveredConfigValidation")
    def disable_discovered_config_validation(
        self,
    ) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "disableDiscoveredConfigValidation"))

    @disable_discovered_config_validation.setter
    def disable_discovered_config_validation(
        self,
        value: typing.Union[builtins.bool, cdktf.IResolvable],
    ) -> None:
        jsii.set(self, "disableDiscoveredConfigValidation", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="idpCaCerts")
    def idp_ca_certs(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "idpCaCerts"))

    @idp_ca_certs.setter
    def idp_ca_certs(self, value: typing.List[builtins.str]) -> None:
        jsii.set(self, "idpCaCerts", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="isPrimaryForScope")
    def is_primary_for_scope(self) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "isPrimaryForScope"))

    @is_primary_for_scope.setter
    def is_primary_for_scope(
        self,
        value: typing.Union[builtins.bool, cdktf.IResolvable],
    ) -> None:
        jsii.set(self, "isPrimaryForScope", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="issuer")
    def issuer(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "issuer"))

    @issuer.setter
    def issuer(self, value: builtins.str) -> None:
        jsii.set(self, "issuer", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="maxAge")
    def max_age(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxAge"))

    @max_age.setter
    def max_age(self, value: jsii.Number) -> None:
        jsii.set(self, "maxAge", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="scopeId")
    def scope_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scopeId"))

    @scope_id.setter
    def scope_id(self, value: builtins.str) -> None:
        jsii.set(self, "scopeId", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="signingAlgorithms")
    def signing_algorithms(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "signingAlgorithms"))

    @signing_algorithms.setter
    def signing_algorithms(self, value: typing.List[builtins.str]) -> None:
        jsii.set(self, "signingAlgorithms", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @state.setter
    def state(self, value: builtins.str) -> None:
        jsii.set(self, "state", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        jsii.set(self, "type", value)


@jsii.data_type(
    jsii_type="hashicorp_boundary.AuthMethodOidcConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "scope_id": "scopeId",
        "account_claim_maps": "accountClaimMaps",
        "allowed_audiences": "allowedAudiences",
        "api_url_prefix": "apiUrlPrefix",
        "callback_url": "callbackUrl",
        "claims_scopes": "claimsScopes",
        "client_id": "clientId",
        "client_secret": "clientSecret",
        "client_secret_hmac": "clientSecretHmac",
        "description": "description",
        "disable_discovered_config_validation": "disableDiscoveredConfigValidation",
        "idp_ca_certs": "idpCaCerts",
        "is_primary_for_scope": "isPrimaryForScope",
        "issuer": "issuer",
        "max_age": "maxAge",
        "name": "name",
        "signing_algorithms": "signingAlgorithms",
        "state": "state",
        "type": "type",
    },
)
class AuthMethodOidcConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        scope_id: builtins.str,
        account_claim_maps: typing.Optional[typing.Sequence[builtins.str]] = None,
        allowed_audiences: typing.Optional[typing.Sequence[builtins.str]] = None,
        api_url_prefix: typing.Optional[builtins.str] = None,
        callback_url: typing.Optional[builtins.str] = None,
        claims_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
        client_id: typing.Optional[builtins.str] = None,
        client_secret: typing.Optional[builtins.str] = None,
        client_secret_hmac: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        disable_discovered_config_validation: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        idp_ca_certs: typing.Optional[typing.Sequence[builtins.str]] = None,
        is_primary_for_scope: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        issuer: typing.Optional[builtins.str] = None,
        max_age: typing.Optional[jsii.Number] = None,
        name: typing.Optional[builtins.str] = None,
        signing_algorithms: typing.Optional[typing.Sequence[builtins.str]] = None,
        state: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param scope_id: The scope ID. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/auth_method_oidc#scope_id AuthMethodOidc#scope_id}
        :param account_claim_maps: Account claim maps for the to_claim of sub. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/auth_method_oidc#account_claim_maps AuthMethodOidc#account_claim_maps}
        :param allowed_audiences: Audiences for which the provider responses will be allowed. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/auth_method_oidc#allowed_audiences AuthMethodOidc#allowed_audiences}
        :param api_url_prefix: The API prefix to use when generating callback URLs for the provider. Should be set to an address at which the provider can reach back to the controller. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/auth_method_oidc#api_url_prefix AuthMethodOidc#api_url_prefix}
        :param callback_url: The URL that should be provided to the IdP for callbacks. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/auth_method_oidc#callback_url AuthMethodOidc#callback_url}
        :param claims_scopes: Claims scopes. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/auth_method_oidc#claims_scopes AuthMethodOidc#claims_scopes}
        :param client_id: The client ID assigned to this auth method from the provider. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/auth_method_oidc#client_id AuthMethodOidc#client_id}
        :param client_secret: The secret key assigned to this auth method from the provider. Once set, only the hash will be kept and the original value can be removed from configuration. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/auth_method_oidc#client_secret AuthMethodOidc#client_secret}
        :param client_secret_hmac: The HMAC of the client secret returned by the Boundary controller, which is used for comparison after initial setting of the value. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/auth_method_oidc#client_secret_hmac AuthMethodOidc#client_secret_hmac}
        :param description: The auth method description. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/auth_method_oidc#description AuthMethodOidc#description}
        :param disable_discovered_config_validation: Disables validation logic ensuring that the OIDC provider's information from its discovery endpoint matches the information here. The validation is only performed at create or update time. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/auth_method_oidc#disable_discovered_config_validation AuthMethodOidc#disable_discovered_config_validation}
        :param idp_ca_certs: A list of CA certificates to trust when validating the IdP's token signatures. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/auth_method_oidc#idp_ca_certs AuthMethodOidc#idp_ca_certs}
        :param is_primary_for_scope: When true, makes this auth method the primary auth method for the scope in which it resides. The primary auth method for a scope means the the user will be automatically created when they login using an OIDC account. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/auth_method_oidc#is_primary_for_scope AuthMethodOidc#is_primary_for_scope}
        :param issuer: The issuer corresponding to the provider, which must match the issuer field in generated tokens. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/auth_method_oidc#issuer AuthMethodOidc#issuer}
        :param max_age: The max age to provide to the provider, indicating how much time is allowed to have passed since the last authentication before the user is challenged again. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/auth_method_oidc#max_age AuthMethodOidc#max_age}
        :param name: The auth method name. Defaults to the resource name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/auth_method_oidc#name AuthMethodOidc#name}
        :param signing_algorithms: Allowed signing algorithms for the provider's issued tokens. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/auth_method_oidc#signing_algorithms AuthMethodOidc#signing_algorithms}
        :param state: Can be one of 'inactive', 'active-private', or 'active-public'. Currently automatically set to active-public. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/auth_method_oidc#state AuthMethodOidc#state}
        :param type: The type of auth method; hardcoded. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/auth_method_oidc#type AuthMethodOidc#type}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        self._values: typing.Dict[str, typing.Any] = {
            "scope_id": scope_id,
        }
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if account_claim_maps is not None:
            self._values["account_claim_maps"] = account_claim_maps
        if allowed_audiences is not None:
            self._values["allowed_audiences"] = allowed_audiences
        if api_url_prefix is not None:
            self._values["api_url_prefix"] = api_url_prefix
        if callback_url is not None:
            self._values["callback_url"] = callback_url
        if claims_scopes is not None:
            self._values["claims_scopes"] = claims_scopes
        if client_id is not None:
            self._values["client_id"] = client_id
        if client_secret is not None:
            self._values["client_secret"] = client_secret
        if client_secret_hmac is not None:
            self._values["client_secret_hmac"] = client_secret_hmac
        if description is not None:
            self._values["description"] = description
        if disable_discovered_config_validation is not None:
            self._values["disable_discovered_config_validation"] = disable_discovered_config_validation
        if idp_ca_certs is not None:
            self._values["idp_ca_certs"] = idp_ca_certs
        if is_primary_for_scope is not None:
            self._values["is_primary_for_scope"] = is_primary_for_scope
        if issuer is not None:
            self._values["issuer"] = issuer
        if max_age is not None:
            self._values["max_age"] = max_age
        if name is not None:
            self._values["name"] = name
        if signing_algorithms is not None:
            self._values["signing_algorithms"] = signing_algorithms
        if state is not None:
            self._values["state"] = state
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[cdktf.ITerraformDependable]], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[cdktf.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[cdktf.TerraformProvider], result)

    @builtins.property
    def scope_id(self) -> builtins.str:
        '''The scope ID.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/auth_method_oidc#scope_id AuthMethodOidc#scope_id}
        '''
        result = self._values.get("scope_id")
        assert result is not None, "Required property 'scope_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def account_claim_maps(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Account claim maps for the to_claim of sub.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/auth_method_oidc#account_claim_maps AuthMethodOidc#account_claim_maps}
        '''
        result = self._values.get("account_claim_maps")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def allowed_audiences(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Audiences for which the provider responses will be allowed.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/auth_method_oidc#allowed_audiences AuthMethodOidc#allowed_audiences}
        '''
        result = self._values.get("allowed_audiences")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def api_url_prefix(self) -> typing.Optional[builtins.str]:
        '''The API prefix to use when generating callback URLs for the provider.

        Should be set to an address at which the provider can reach back to the controller.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/auth_method_oidc#api_url_prefix AuthMethodOidc#api_url_prefix}
        '''
        result = self._values.get("api_url_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def callback_url(self) -> typing.Optional[builtins.str]:
        '''The URL that should be provided to the IdP for callbacks.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/auth_method_oidc#callback_url AuthMethodOidc#callback_url}
        '''
        result = self._values.get("callback_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def claims_scopes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Claims scopes.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/auth_method_oidc#claims_scopes AuthMethodOidc#claims_scopes}
        '''
        result = self._values.get("claims_scopes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def client_id(self) -> typing.Optional[builtins.str]:
        '''The client ID assigned to this auth method from the provider.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/auth_method_oidc#client_id AuthMethodOidc#client_id}
        '''
        result = self._values.get("client_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_secret(self) -> typing.Optional[builtins.str]:
        '''The secret key assigned to this auth method from the provider.

        Once set, only the hash will be kept and the original value can be removed from configuration.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/auth_method_oidc#client_secret AuthMethodOidc#client_secret}
        '''
        result = self._values.get("client_secret")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_secret_hmac(self) -> typing.Optional[builtins.str]:
        '''The HMAC of the client secret returned by the Boundary controller, which is used for comparison after initial setting of the value.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/auth_method_oidc#client_secret_hmac AuthMethodOidc#client_secret_hmac}
        '''
        result = self._values.get("client_secret_hmac")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The auth method description.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/auth_method_oidc#description AuthMethodOidc#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disable_discovered_config_validation(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Disables validation logic ensuring that the OIDC provider's information from its discovery endpoint matches the information here.

        The validation is only performed at create or update time.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/auth_method_oidc#disable_discovered_config_validation AuthMethodOidc#disable_discovered_config_validation}
        '''
        result = self._values.get("disable_discovered_config_validation")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    @builtins.property
    def idp_ca_certs(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of CA certificates to trust when validating the IdP's token signatures.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/auth_method_oidc#idp_ca_certs AuthMethodOidc#idp_ca_certs}
        '''
        result = self._values.get("idp_ca_certs")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def is_primary_for_scope(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''When true, makes this auth method the primary auth method for the scope in which it resides.

        The primary auth method for a scope means the the user will be automatically created when they login using an OIDC account.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/auth_method_oidc#is_primary_for_scope AuthMethodOidc#is_primary_for_scope}
        '''
        result = self._values.get("is_primary_for_scope")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    @builtins.property
    def issuer(self) -> typing.Optional[builtins.str]:
        '''The issuer corresponding to the provider, which must match the issuer field in generated tokens.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/auth_method_oidc#issuer AuthMethodOidc#issuer}
        '''
        result = self._values.get("issuer")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_age(self) -> typing.Optional[jsii.Number]:
        '''The max age to provide to the provider, indicating how much time is allowed to have passed since the last authentication before the user is challenged again.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/auth_method_oidc#max_age AuthMethodOidc#max_age}
        '''
        result = self._values.get("max_age")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The auth method name. Defaults to the resource name.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/auth_method_oidc#name AuthMethodOidc#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def signing_algorithms(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Allowed signing algorithms for the provider's issued tokens.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/auth_method_oidc#signing_algorithms AuthMethodOidc#signing_algorithms}
        '''
        result = self._values.get("signing_algorithms")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def state(self) -> typing.Optional[builtins.str]:
        '''Can be one of 'inactive', 'active-private', or 'active-public'. Currently automatically set to active-public.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/auth_method_oidc#state AuthMethodOidc#state}
        '''
        result = self._values.get("state")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''The type of auth method; hardcoded.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/auth_method_oidc#type AuthMethodOidc#type}
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AuthMethodOidcConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AuthMethodPassword(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="hashicorp_boundary.AuthMethodPassword",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/boundary/r/auth_method_password boundary_auth_method_password}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        scope_id: builtins.str,
        description: typing.Optional[builtins.str] = None,
        min_login_name_length: typing.Optional[jsii.Number] = None,
        min_password_length: typing.Optional[jsii.Number] = None,
        name: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/boundary/r/auth_method_password boundary_auth_method_password} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param scope_id: The scope ID. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/auth_method_password#scope_id AuthMethodPassword#scope_id}
        :param description: The auth method description. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/auth_method_password#description AuthMethodPassword#description}
        :param min_login_name_length: The minimum login name length. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/auth_method_password#min_login_name_length AuthMethodPassword#min_login_name_length}
        :param min_password_length: The minimum password length. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/auth_method_password#min_password_length AuthMethodPassword#min_password_length}
        :param name: The auth method name. Defaults to the resource name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/auth_method_password#name AuthMethodPassword#name}
        :param type: The resource type, hardcoded per resource. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/auth_method_password#type AuthMethodPassword#type}
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        '''
        config = AuthMethodPasswordConfig(
            scope_id=scope_id,
            description=description,
            min_login_name_length=min_login_name_length,
            min_password_length=min_password_length,
            name=name,
            type=type,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetMinLoginNameLength")
    def reset_min_login_name_length(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinLoginNameLength", []))

    @jsii.member(jsii_name="resetMinPasswordLength")
    def reset_min_password_length(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinPasswordLength", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="minLoginNameLengthInput")
    def min_login_name_length_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minLoginNameLengthInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="minPasswordLengthInput")
    def min_password_length_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minPasswordLengthInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="scopeIdInput")
    def scope_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scopeIdInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        jsii.set(self, "description", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="minLoginNameLength")
    def min_login_name_length(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minLoginNameLength"))

    @min_login_name_length.setter
    def min_login_name_length(self, value: jsii.Number) -> None:
        jsii.set(self, "minLoginNameLength", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="minPasswordLength")
    def min_password_length(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minPasswordLength"))

    @min_password_length.setter
    def min_password_length(self, value: jsii.Number) -> None:
        jsii.set(self, "minPasswordLength", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="scopeId")
    def scope_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scopeId"))

    @scope_id.setter
    def scope_id(self, value: builtins.str) -> None:
        jsii.set(self, "scopeId", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        jsii.set(self, "type", value)


@jsii.data_type(
    jsii_type="hashicorp_boundary.AuthMethodPasswordConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "scope_id": "scopeId",
        "description": "description",
        "min_login_name_length": "minLoginNameLength",
        "min_password_length": "minPasswordLength",
        "name": "name",
        "type": "type",
    },
)
class AuthMethodPasswordConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        scope_id: builtins.str,
        description: typing.Optional[builtins.str] = None,
        min_login_name_length: typing.Optional[jsii.Number] = None,
        min_password_length: typing.Optional[jsii.Number] = None,
        name: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param scope_id: The scope ID. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/auth_method_password#scope_id AuthMethodPassword#scope_id}
        :param description: The auth method description. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/auth_method_password#description AuthMethodPassword#description}
        :param min_login_name_length: The minimum login name length. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/auth_method_password#min_login_name_length AuthMethodPassword#min_login_name_length}
        :param min_password_length: The minimum password length. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/auth_method_password#min_password_length AuthMethodPassword#min_password_length}
        :param name: The auth method name. Defaults to the resource name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/auth_method_password#name AuthMethodPassword#name}
        :param type: The resource type, hardcoded per resource. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/auth_method_password#type AuthMethodPassword#type}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        self._values: typing.Dict[str, typing.Any] = {
            "scope_id": scope_id,
        }
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if description is not None:
            self._values["description"] = description
        if min_login_name_length is not None:
            self._values["min_login_name_length"] = min_login_name_length
        if min_password_length is not None:
            self._values["min_password_length"] = min_password_length
        if name is not None:
            self._values["name"] = name
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[cdktf.ITerraformDependable]], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[cdktf.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[cdktf.TerraformProvider], result)

    @builtins.property
    def scope_id(self) -> builtins.str:
        '''The scope ID.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/auth_method_password#scope_id AuthMethodPassword#scope_id}
        '''
        result = self._values.get("scope_id")
        assert result is not None, "Required property 'scope_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The auth method description.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/auth_method_password#description AuthMethodPassword#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def min_login_name_length(self) -> typing.Optional[jsii.Number]:
        '''The minimum login name length.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/auth_method_password#min_login_name_length AuthMethodPassword#min_login_name_length}
        '''
        result = self._values.get("min_login_name_length")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_password_length(self) -> typing.Optional[jsii.Number]:
        '''The minimum password length.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/auth_method_password#min_password_length AuthMethodPassword#min_password_length}
        '''
        result = self._values.get("min_password_length")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The auth method name. Defaults to the resource name.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/auth_method_password#name AuthMethodPassword#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''The resource type, hardcoded per resource.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/auth_method_password#type AuthMethodPassword#type}
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AuthMethodPasswordConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BoundaryProvider(
    cdktf.TerraformProvider,
    metaclass=jsii.JSIIMeta,
    jsii_type="hashicorp_boundary.BoundaryProvider",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/boundary boundary}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        addr: builtins.str,
        alias: typing.Optional[builtins.str] = None,
        auth_method_id: typing.Optional[builtins.str] = None,
        password_auth_method_login_name: typing.Optional[builtins.str] = None,
        password_auth_method_password: typing.Optional[builtins.str] = None,
        recovery_kms_hcl: typing.Optional[builtins.str] = None,
        tls_insecure: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        token: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/boundary boundary} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param addr: The base url of the Boundary API, e.g. "http://127.0.0.1:9200". If not set, it will be read from the "BOUNDARY_ADDR" env var. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary#addr BoundaryProvider#addr}
        :param alias: Alias name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary#alias BoundaryProvider#alias}
        :param auth_method_id: The auth method ID e.g. ampw_1234567890. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary#auth_method_id BoundaryProvider#auth_method_id}
        :param password_auth_method_login_name: The auth method login name for password-style auth methods. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary#password_auth_method_login_name BoundaryProvider#password_auth_method_login_name}
        :param password_auth_method_password: The auth method password for password-style auth methods. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary#password_auth_method_password BoundaryProvider#password_auth_method_password}
        :param recovery_kms_hcl: Can be a heredoc string or a path on disk. If set, the string/file will be parsed as HCL and used with the recovery KMS mechanism. While this is set, it will override any other authentication information; the KMS mechanism will always be used. See Boundary's KMS docs for examples: https://boundaryproject.io/docs/configuration/kms Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary#recovery_kms_hcl BoundaryProvider#recovery_kms_hcl}
        :param tls_insecure: When set to true, does not validate the Boundary API endpoint certificate. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary#tls_insecure BoundaryProvider#tls_insecure}
        :param token: The Boundary token to use, as a string or path on disk containing just the string. If set, the token read here will be used in place of authenticating with the auth method specified in "auth_method_id", although the recovery KMS mechanism will still override this. Can also be set with the BOUNDARY_TOKEN environment variable. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary#token BoundaryProvider#token}
        '''
        config = BoundaryProviderConfig(
            addr=addr,
            alias=alias,
            auth_method_id=auth_method_id,
            password_auth_method_login_name=password_auth_method_login_name,
            password_auth_method_password=password_auth_method_password,
            recovery_kms_hcl=recovery_kms_hcl,
            tls_insecure=tls_insecure,
            token=token,
        )

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="resetAlias")
    def reset_alias(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAlias", []))

    @jsii.member(jsii_name="resetAuthMethodId")
    def reset_auth_method_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthMethodId", []))

    @jsii.member(jsii_name="resetPasswordAuthMethodLoginName")
    def reset_password_auth_method_login_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPasswordAuthMethodLoginName", []))

    @jsii.member(jsii_name="resetPasswordAuthMethodPassword")
    def reset_password_auth_method_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPasswordAuthMethodPassword", []))

    @jsii.member(jsii_name="resetRecoveryKmsHcl")
    def reset_recovery_kms_hcl(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRecoveryKmsHcl", []))

    @jsii.member(jsii_name="resetTlsInsecure")
    def reset_tls_insecure(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTlsInsecure", []))

    @jsii.member(jsii_name="resetToken")
    def reset_token(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetToken", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="addrInput")
    def addr_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "addrInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="aliasInput")
    def alias_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "aliasInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="authMethodIdInput")
    def auth_method_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authMethodIdInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="passwordAuthMethodLoginNameInput")
    def password_auth_method_login_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordAuthMethodLoginNameInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="passwordAuthMethodPasswordInput")
    def password_auth_method_password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordAuthMethodPasswordInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="recoveryKmsHclInput")
    def recovery_kms_hcl_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "recoveryKmsHclInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tlsInsecureInput")
    def tls_insecure_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "tlsInsecureInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tokenInput")
    def token_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tokenInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="addr")
    def addr(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "addr"))

    @addr.setter
    def addr(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "addr", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="alias")
    def alias(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "alias"))

    @alias.setter
    def alias(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "alias", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="authMethodId")
    def auth_method_id(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authMethodId"))

    @auth_method_id.setter
    def auth_method_id(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "authMethodId", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="passwordAuthMethodLoginName")
    def password_auth_method_login_name(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordAuthMethodLoginName"))

    @password_auth_method_login_name.setter
    def password_auth_method_login_name(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        jsii.set(self, "passwordAuthMethodLoginName", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="passwordAuthMethodPassword")
    def password_auth_method_password(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordAuthMethodPassword"))

    @password_auth_method_password.setter
    def password_auth_method_password(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        jsii.set(self, "passwordAuthMethodPassword", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="recoveryKmsHcl")
    def recovery_kms_hcl(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "recoveryKmsHcl"))

    @recovery_kms_hcl.setter
    def recovery_kms_hcl(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "recoveryKmsHcl", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tlsInsecure")
    def tls_insecure(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "tlsInsecure"))

    @tls_insecure.setter
    def tls_insecure(
        self,
        value: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]],
    ) -> None:
        jsii.set(self, "tlsInsecure", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="token")
    def token(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "token"))

    @token.setter
    def token(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "token", value)


@jsii.data_type(
    jsii_type="hashicorp_boundary.BoundaryProviderConfig",
    jsii_struct_bases=[],
    name_mapping={
        "addr": "addr",
        "alias": "alias",
        "auth_method_id": "authMethodId",
        "password_auth_method_login_name": "passwordAuthMethodLoginName",
        "password_auth_method_password": "passwordAuthMethodPassword",
        "recovery_kms_hcl": "recoveryKmsHcl",
        "tls_insecure": "tlsInsecure",
        "token": "token",
    },
)
class BoundaryProviderConfig:
    def __init__(
        self,
        *,
        addr: builtins.str,
        alias: typing.Optional[builtins.str] = None,
        auth_method_id: typing.Optional[builtins.str] = None,
        password_auth_method_login_name: typing.Optional[builtins.str] = None,
        password_auth_method_password: typing.Optional[builtins.str] = None,
        recovery_kms_hcl: typing.Optional[builtins.str] = None,
        tls_insecure: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        token: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param addr: The base url of the Boundary API, e.g. "http://127.0.0.1:9200". If not set, it will be read from the "BOUNDARY_ADDR" env var. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary#addr BoundaryProvider#addr}
        :param alias: Alias name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary#alias BoundaryProvider#alias}
        :param auth_method_id: The auth method ID e.g. ampw_1234567890. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary#auth_method_id BoundaryProvider#auth_method_id}
        :param password_auth_method_login_name: The auth method login name for password-style auth methods. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary#password_auth_method_login_name BoundaryProvider#password_auth_method_login_name}
        :param password_auth_method_password: The auth method password for password-style auth methods. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary#password_auth_method_password BoundaryProvider#password_auth_method_password}
        :param recovery_kms_hcl: Can be a heredoc string or a path on disk. If set, the string/file will be parsed as HCL and used with the recovery KMS mechanism. While this is set, it will override any other authentication information; the KMS mechanism will always be used. See Boundary's KMS docs for examples: https://boundaryproject.io/docs/configuration/kms Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary#recovery_kms_hcl BoundaryProvider#recovery_kms_hcl}
        :param tls_insecure: When set to true, does not validate the Boundary API endpoint certificate. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary#tls_insecure BoundaryProvider#tls_insecure}
        :param token: The Boundary token to use, as a string or path on disk containing just the string. If set, the token read here will be used in place of authenticating with the auth method specified in "auth_method_id", although the recovery KMS mechanism will still override this. Can also be set with the BOUNDARY_TOKEN environment variable. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary#token BoundaryProvider#token}
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "addr": addr,
        }
        if alias is not None:
            self._values["alias"] = alias
        if auth_method_id is not None:
            self._values["auth_method_id"] = auth_method_id
        if password_auth_method_login_name is not None:
            self._values["password_auth_method_login_name"] = password_auth_method_login_name
        if password_auth_method_password is not None:
            self._values["password_auth_method_password"] = password_auth_method_password
        if recovery_kms_hcl is not None:
            self._values["recovery_kms_hcl"] = recovery_kms_hcl
        if tls_insecure is not None:
            self._values["tls_insecure"] = tls_insecure
        if token is not None:
            self._values["token"] = token

    @builtins.property
    def addr(self) -> builtins.str:
        '''The base url of the Boundary API, e.g. "http://127.0.0.1:9200". If not set, it will be read from the "BOUNDARY_ADDR" env var.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary#addr BoundaryProvider#addr}
        '''
        result = self._values.get("addr")
        assert result is not None, "Required property 'addr' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def alias(self) -> typing.Optional[builtins.str]:
        '''Alias name.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary#alias BoundaryProvider#alias}
        '''
        result = self._values.get("alias")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def auth_method_id(self) -> typing.Optional[builtins.str]:
        '''The auth method ID e.g. ampw_1234567890.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary#auth_method_id BoundaryProvider#auth_method_id}
        '''
        result = self._values.get("auth_method_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def password_auth_method_login_name(self) -> typing.Optional[builtins.str]:
        '''The auth method login name for password-style auth methods.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary#password_auth_method_login_name BoundaryProvider#password_auth_method_login_name}
        '''
        result = self._values.get("password_auth_method_login_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def password_auth_method_password(self) -> typing.Optional[builtins.str]:
        '''The auth method password for password-style auth methods.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary#password_auth_method_password BoundaryProvider#password_auth_method_password}
        '''
        result = self._values.get("password_auth_method_password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def recovery_kms_hcl(self) -> typing.Optional[builtins.str]:
        '''Can be a heredoc string or a path on disk.

        If set, the string/file will be parsed as HCL and used with the recovery KMS mechanism. While this is set, it will override any other authentication information; the KMS mechanism will always be used. See Boundary's KMS docs for examples: https://boundaryproject.io/docs/configuration/kms

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary#recovery_kms_hcl BoundaryProvider#recovery_kms_hcl}
        '''
        result = self._values.get("recovery_kms_hcl")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tls_insecure(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''When set to true, does not validate the Boundary API endpoint certificate.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary#tls_insecure BoundaryProvider#tls_insecure}
        '''
        result = self._values.get("tls_insecure")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    @builtins.property
    def token(self) -> typing.Optional[builtins.str]:
        '''The Boundary token to use, as a string or path on disk containing just the string.

        If set, the token read here will be used in place of authenticating with the auth method specified in "auth_method_id", although the recovery KMS mechanism will still override this. Can also be set with the BOUNDARY_TOKEN environment variable.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary#token BoundaryProvider#token}
        '''
        result = self._values.get("token")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BoundaryProviderConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CredentialLibraryVault(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="hashicorp_boundary.CredentialLibraryVault",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/boundary/r/credential_library_vault boundary_credential_library_vault}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        credential_store_id: builtins.str,
        path: builtins.str,
        description: typing.Optional[builtins.str] = None,
        http_method: typing.Optional[builtins.str] = None,
        http_request_body: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/boundary/r/credential_library_vault boundary_credential_library_vault} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param credential_store_id: The ID of the credential store that this library belongs to. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/credential_library_vault#credential_store_id CredentialLibraryVault#credential_store_id}
        :param path: The path in Vault to request credentials from. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/credential_library_vault#path CredentialLibraryVault#path}
        :param description: The Vault credential library description. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/credential_library_vault#description CredentialLibraryVault#description}
        :param http_method: The HTTP method the library uses when requesting credentials from Vault. Defaults to 'GET'. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/credential_library_vault#http_method CredentialLibraryVault#http_method}
        :param http_request_body: The body of the HTTP request the library sends to Vault when requesting credentials. Only valid if ``http_method`` is set to ``POST``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/credential_library_vault#http_request_body CredentialLibraryVault#http_request_body}
        :param name: The Vault credential library name. Defaults to the resource name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/credential_library_vault#name CredentialLibraryVault#name}
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        '''
        config = CredentialLibraryVaultConfig(
            credential_store_id=credential_store_id,
            path=path,
            description=description,
            http_method=http_method,
            http_request_body=http_request_body,
            name=name,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetHttpMethod")
    def reset_http_method(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpMethod", []))

    @jsii.member(jsii_name="resetHttpRequestBody")
    def reset_http_request_body(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpRequestBody", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="credentialStoreIdInput")
    def credential_store_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "credentialStoreIdInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="httpMethodInput")
    def http_method_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "httpMethodInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="httpRequestBodyInput")
    def http_request_body_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "httpRequestBodyInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="credentialStoreId")
    def credential_store_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "credentialStoreId"))

    @credential_store_id.setter
    def credential_store_id(self, value: builtins.str) -> None:
        jsii.set(self, "credentialStoreId", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        jsii.set(self, "description", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="httpMethod")
    def http_method(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "httpMethod"))

    @http_method.setter
    def http_method(self, value: builtins.str) -> None:
        jsii.set(self, "httpMethod", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="httpRequestBody")
    def http_request_body(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "httpRequestBody"))

    @http_request_body.setter
    def http_request_body(self, value: builtins.str) -> None:
        jsii.set(self, "httpRequestBody", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        jsii.set(self, "path", value)


@jsii.data_type(
    jsii_type="hashicorp_boundary.CredentialLibraryVaultConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "credential_store_id": "credentialStoreId",
        "path": "path",
        "description": "description",
        "http_method": "httpMethod",
        "http_request_body": "httpRequestBody",
        "name": "name",
    },
)
class CredentialLibraryVaultConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        credential_store_id: builtins.str,
        path: builtins.str,
        description: typing.Optional[builtins.str] = None,
        http_method: typing.Optional[builtins.str] = None,
        http_request_body: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param credential_store_id: The ID of the credential store that this library belongs to. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/credential_library_vault#credential_store_id CredentialLibraryVault#credential_store_id}
        :param path: The path in Vault to request credentials from. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/credential_library_vault#path CredentialLibraryVault#path}
        :param description: The Vault credential library description. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/credential_library_vault#description CredentialLibraryVault#description}
        :param http_method: The HTTP method the library uses when requesting credentials from Vault. Defaults to 'GET'. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/credential_library_vault#http_method CredentialLibraryVault#http_method}
        :param http_request_body: The body of the HTTP request the library sends to Vault when requesting credentials. Only valid if ``http_method`` is set to ``POST``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/credential_library_vault#http_request_body CredentialLibraryVault#http_request_body}
        :param name: The Vault credential library name. Defaults to the resource name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/credential_library_vault#name CredentialLibraryVault#name}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        self._values: typing.Dict[str, typing.Any] = {
            "credential_store_id": credential_store_id,
            "path": path,
        }
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if description is not None:
            self._values["description"] = description
        if http_method is not None:
            self._values["http_method"] = http_method
        if http_request_body is not None:
            self._values["http_request_body"] = http_request_body
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[cdktf.ITerraformDependable]], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[cdktf.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[cdktf.TerraformProvider], result)

    @builtins.property
    def credential_store_id(self) -> builtins.str:
        '''The ID of the credential store that this library belongs to.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/credential_library_vault#credential_store_id CredentialLibraryVault#credential_store_id}
        '''
        result = self._values.get("credential_store_id")
        assert result is not None, "Required property 'credential_store_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def path(self) -> builtins.str:
        '''The path in Vault to request credentials from.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/credential_library_vault#path CredentialLibraryVault#path}
        '''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The Vault credential library description.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/credential_library_vault#description CredentialLibraryVault#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def http_method(self) -> typing.Optional[builtins.str]:
        '''The HTTP method the library uses when requesting credentials from Vault. Defaults to 'GET'.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/credential_library_vault#http_method CredentialLibraryVault#http_method}
        '''
        result = self._values.get("http_method")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def http_request_body(self) -> typing.Optional[builtins.str]:
        '''The body of the HTTP request the library sends to Vault when requesting credentials.

        Only valid if ``http_method`` is set to ``POST``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/credential_library_vault#http_request_body CredentialLibraryVault#http_request_body}
        '''
        result = self._values.get("http_request_body")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The Vault credential library name. Defaults to the resource name.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/credential_library_vault#name CredentialLibraryVault#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CredentialLibraryVaultConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CredentialStoreVault(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="hashicorp_boundary.CredentialStoreVault",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/boundary/r/credential_store_vault boundary_credential_store_vault}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        address: builtins.str,
        scope_id: builtins.str,
        token: builtins.str,
        ca_cert: typing.Optional[builtins.str] = None,
        client_certificate: typing.Optional[builtins.str] = None,
        client_certificate_key: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        namespace: typing.Optional[builtins.str] = None,
        tls_server_name: typing.Optional[builtins.str] = None,
        tls_skip_verify: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/boundary/r/credential_store_vault boundary_credential_store_vault} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param address: The address to Vault server. This should be a complete URL such as 'https://127.0.0.1:8200'. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/credential_store_vault#address CredentialStoreVault#address}
        :param scope_id: The scope for this credential store. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/credential_store_vault#scope_id CredentialStoreVault#scope_id}
        :param token: A token used for accessing Vault. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/credential_store_vault#token CredentialStoreVault#token}
        :param ca_cert: A PEM-encoded CA certificate to verify the Vault server's TLS certificate. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/credential_store_vault#ca_cert CredentialStoreVault#ca_cert}
        :param client_certificate: A PEM-encoded client certificate to use for TLS authentication to the Vault server. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/credential_store_vault#client_certificate CredentialStoreVault#client_certificate}
        :param client_certificate_key: A PEM-encoded private key matching the client certificate from 'client_certificate'. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/credential_store_vault#client_certificate_key CredentialStoreVault#client_certificate_key}
        :param description: The Vault credential store description. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/credential_store_vault#description CredentialStoreVault#description}
        :param name: The Vault credential store name. Defaults to the resource name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/credential_store_vault#name CredentialStoreVault#name}
        :param namespace: The namespace within Vault to use. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/credential_store_vault#namespace CredentialStoreVault#namespace}
        :param tls_server_name: Name to use as the SNI host when connecting to Vault via TLS. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/credential_store_vault#tls_server_name CredentialStoreVault#tls_server_name}
        :param tls_skip_verify: Whether or not to skip TLS verification. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/credential_store_vault#tls_skip_verify CredentialStoreVault#tls_skip_verify}
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        '''
        config = CredentialStoreVaultConfig(
            address=address,
            scope_id=scope_id,
            token=token,
            ca_cert=ca_cert,
            client_certificate=client_certificate,
            client_certificate_key=client_certificate_key,
            description=description,
            name=name,
            namespace=namespace,
            tls_server_name=tls_server_name,
            tls_skip_verify=tls_skip_verify,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="resetCaCert")
    def reset_ca_cert(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCaCert", []))

    @jsii.member(jsii_name="resetClientCertificate")
    def reset_client_certificate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientCertificate", []))

    @jsii.member(jsii_name="resetClientCertificateKey")
    def reset_client_certificate_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientCertificateKey", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetNamespace")
    def reset_namespace(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNamespace", []))

    @jsii.member(jsii_name="resetTlsServerName")
    def reset_tls_server_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTlsServerName", []))

    @jsii.member(jsii_name="resetTlsSkipVerify")
    def reset_tls_skip_verify(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTlsSkipVerify", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="clientCertificateKeyHmac")
    def client_certificate_key_hmac(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientCertificateKeyHmac"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tokenHmac")
    def token_hmac(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tokenHmac"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="addressInput")
    def address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "addressInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="caCertInput")
    def ca_cert_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "caCertInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="clientCertificateInput")
    def client_certificate_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientCertificateInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="clientCertificateKeyInput")
    def client_certificate_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientCertificateKeyInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="namespaceInput")
    def namespace_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "namespaceInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="scopeIdInput")
    def scope_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scopeIdInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tlsServerNameInput")
    def tls_server_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tlsServerNameInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tlsSkipVerifyInput")
    def tls_skip_verify_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "tlsSkipVerifyInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tokenInput")
    def token_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tokenInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="address")
    def address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "address"))

    @address.setter
    def address(self, value: builtins.str) -> None:
        jsii.set(self, "address", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="caCert")
    def ca_cert(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "caCert"))

    @ca_cert.setter
    def ca_cert(self, value: builtins.str) -> None:
        jsii.set(self, "caCert", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="clientCertificate")
    def client_certificate(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientCertificate"))

    @client_certificate.setter
    def client_certificate(self, value: builtins.str) -> None:
        jsii.set(self, "clientCertificate", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="clientCertificateKey")
    def client_certificate_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientCertificateKey"))

    @client_certificate_key.setter
    def client_certificate_key(self, value: builtins.str) -> None:
        jsii.set(self, "clientCertificateKey", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        jsii.set(self, "description", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="namespace")
    def namespace(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "namespace"))

    @namespace.setter
    def namespace(self, value: builtins.str) -> None:
        jsii.set(self, "namespace", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="scopeId")
    def scope_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scopeId"))

    @scope_id.setter
    def scope_id(self, value: builtins.str) -> None:
        jsii.set(self, "scopeId", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tlsServerName")
    def tls_server_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tlsServerName"))

    @tls_server_name.setter
    def tls_server_name(self, value: builtins.str) -> None:
        jsii.set(self, "tlsServerName", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tlsSkipVerify")
    def tls_skip_verify(self) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "tlsSkipVerify"))

    @tls_skip_verify.setter
    def tls_skip_verify(
        self,
        value: typing.Union[builtins.bool, cdktf.IResolvable],
    ) -> None:
        jsii.set(self, "tlsSkipVerify", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="token")
    def token(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "token"))

    @token.setter
    def token(self, value: builtins.str) -> None:
        jsii.set(self, "token", value)


@jsii.data_type(
    jsii_type="hashicorp_boundary.CredentialStoreVaultConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "address": "address",
        "scope_id": "scopeId",
        "token": "token",
        "ca_cert": "caCert",
        "client_certificate": "clientCertificate",
        "client_certificate_key": "clientCertificateKey",
        "description": "description",
        "name": "name",
        "namespace": "namespace",
        "tls_server_name": "tlsServerName",
        "tls_skip_verify": "tlsSkipVerify",
    },
)
class CredentialStoreVaultConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        address: builtins.str,
        scope_id: builtins.str,
        token: builtins.str,
        ca_cert: typing.Optional[builtins.str] = None,
        client_certificate: typing.Optional[builtins.str] = None,
        client_certificate_key: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        namespace: typing.Optional[builtins.str] = None,
        tls_server_name: typing.Optional[builtins.str] = None,
        tls_skip_verify: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
    ) -> None:
        '''
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param address: The address to Vault server. This should be a complete URL such as 'https://127.0.0.1:8200'. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/credential_store_vault#address CredentialStoreVault#address}
        :param scope_id: The scope for this credential store. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/credential_store_vault#scope_id CredentialStoreVault#scope_id}
        :param token: A token used for accessing Vault. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/credential_store_vault#token CredentialStoreVault#token}
        :param ca_cert: A PEM-encoded CA certificate to verify the Vault server's TLS certificate. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/credential_store_vault#ca_cert CredentialStoreVault#ca_cert}
        :param client_certificate: A PEM-encoded client certificate to use for TLS authentication to the Vault server. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/credential_store_vault#client_certificate CredentialStoreVault#client_certificate}
        :param client_certificate_key: A PEM-encoded private key matching the client certificate from 'client_certificate'. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/credential_store_vault#client_certificate_key CredentialStoreVault#client_certificate_key}
        :param description: The Vault credential store description. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/credential_store_vault#description CredentialStoreVault#description}
        :param name: The Vault credential store name. Defaults to the resource name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/credential_store_vault#name CredentialStoreVault#name}
        :param namespace: The namespace within Vault to use. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/credential_store_vault#namespace CredentialStoreVault#namespace}
        :param tls_server_name: Name to use as the SNI host when connecting to Vault via TLS. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/credential_store_vault#tls_server_name CredentialStoreVault#tls_server_name}
        :param tls_skip_verify: Whether or not to skip TLS verification. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/credential_store_vault#tls_skip_verify CredentialStoreVault#tls_skip_verify}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        self._values: typing.Dict[str, typing.Any] = {
            "address": address,
            "scope_id": scope_id,
            "token": token,
        }
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if ca_cert is not None:
            self._values["ca_cert"] = ca_cert
        if client_certificate is not None:
            self._values["client_certificate"] = client_certificate
        if client_certificate_key is not None:
            self._values["client_certificate_key"] = client_certificate_key
        if description is not None:
            self._values["description"] = description
        if name is not None:
            self._values["name"] = name
        if namespace is not None:
            self._values["namespace"] = namespace
        if tls_server_name is not None:
            self._values["tls_server_name"] = tls_server_name
        if tls_skip_verify is not None:
            self._values["tls_skip_verify"] = tls_skip_verify

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[cdktf.ITerraformDependable]], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[cdktf.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[cdktf.TerraformProvider], result)

    @builtins.property
    def address(self) -> builtins.str:
        '''The address to Vault server. This should be a complete URL such as 'https://127.0.0.1:8200'.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/credential_store_vault#address CredentialStoreVault#address}
        '''
        result = self._values.get("address")
        assert result is not None, "Required property 'address' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def scope_id(self) -> builtins.str:
        '''The scope for this credential store.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/credential_store_vault#scope_id CredentialStoreVault#scope_id}
        '''
        result = self._values.get("scope_id")
        assert result is not None, "Required property 'scope_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def token(self) -> builtins.str:
        '''A token used for accessing Vault.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/credential_store_vault#token CredentialStoreVault#token}
        '''
        result = self._values.get("token")
        assert result is not None, "Required property 'token' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ca_cert(self) -> typing.Optional[builtins.str]:
        '''A PEM-encoded CA certificate to verify the Vault server's TLS certificate.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/credential_store_vault#ca_cert CredentialStoreVault#ca_cert}
        '''
        result = self._values.get("ca_cert")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_certificate(self) -> typing.Optional[builtins.str]:
        '''A PEM-encoded client certificate to use for TLS authentication to the Vault server.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/credential_store_vault#client_certificate CredentialStoreVault#client_certificate}
        '''
        result = self._values.get("client_certificate")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_certificate_key(self) -> typing.Optional[builtins.str]:
        '''A PEM-encoded private key matching the client certificate from 'client_certificate'.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/credential_store_vault#client_certificate_key CredentialStoreVault#client_certificate_key}
        '''
        result = self._values.get("client_certificate_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The Vault credential store description.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/credential_store_vault#description CredentialStoreVault#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The Vault credential store name. Defaults to the resource name.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/credential_store_vault#name CredentialStoreVault#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def namespace(self) -> typing.Optional[builtins.str]:
        '''The namespace within Vault to use.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/credential_store_vault#namespace CredentialStoreVault#namespace}
        '''
        result = self._values.get("namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tls_server_name(self) -> typing.Optional[builtins.str]:
        '''Name to use as the SNI host when connecting to Vault via TLS.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/credential_store_vault#tls_server_name CredentialStoreVault#tls_server_name}
        '''
        result = self._values.get("tls_server_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tls_skip_verify(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Whether or not to skip TLS verification.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/credential_store_vault#tls_skip_verify CredentialStoreVault#tls_skip_verify}
        '''
        result = self._values.get("tls_skip_verify")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CredentialStoreVaultConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Group(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="hashicorp_boundary.Group",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/boundary/r/group boundary_group}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        scope_id: builtins.str,
        description: typing.Optional[builtins.str] = None,
        member_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/boundary/r/group boundary_group} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param scope_id: The scope ID in which the resource is created. Defaults to the provider's ``default_scope`` if unset. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/group#scope_id Group#scope_id}
        :param description: The group description. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/group#description Group#description}
        :param member_ids: Resource IDs for group members, these are most likely boundary users. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/group#member_ids Group#member_ids}
        :param name: The group name. Defaults to the resource name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/group#name Group#name}
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        '''
        config = GroupConfig(
            scope_id=scope_id,
            description=description,
            member_ids=member_ids,
            name=name,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetMemberIds")
    def reset_member_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMemberIds", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="memberIdsInput")
    def member_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "memberIdsInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="scopeIdInput")
    def scope_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scopeIdInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        jsii.set(self, "description", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="memberIds")
    def member_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "memberIds"))

    @member_ids.setter
    def member_ids(self, value: typing.List[builtins.str]) -> None:
        jsii.set(self, "memberIds", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="scopeId")
    def scope_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scopeId"))

    @scope_id.setter
    def scope_id(self, value: builtins.str) -> None:
        jsii.set(self, "scopeId", value)


@jsii.data_type(
    jsii_type="hashicorp_boundary.GroupConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "scope_id": "scopeId",
        "description": "description",
        "member_ids": "memberIds",
        "name": "name",
    },
)
class GroupConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        scope_id: builtins.str,
        description: typing.Optional[builtins.str] = None,
        member_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param scope_id: The scope ID in which the resource is created. Defaults to the provider's ``default_scope`` if unset. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/group#scope_id Group#scope_id}
        :param description: The group description. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/group#description Group#description}
        :param member_ids: Resource IDs for group members, these are most likely boundary users. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/group#member_ids Group#member_ids}
        :param name: The group name. Defaults to the resource name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/group#name Group#name}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        self._values: typing.Dict[str, typing.Any] = {
            "scope_id": scope_id,
        }
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if description is not None:
            self._values["description"] = description
        if member_ids is not None:
            self._values["member_ids"] = member_ids
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[cdktf.ITerraformDependable]], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[cdktf.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[cdktf.TerraformProvider], result)

    @builtins.property
    def scope_id(self) -> builtins.str:
        '''The scope ID in which the resource is created. Defaults to the provider's ``default_scope`` if unset.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/group#scope_id Group#scope_id}
        '''
        result = self._values.get("scope_id")
        assert result is not None, "Required property 'scope_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The group description.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/group#description Group#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def member_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Resource IDs for group members, these are most likely boundary users.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/group#member_ids Group#member_ids}
        '''
        result = self._values.get("member_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The group name. Defaults to the resource name.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/group#name Group#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GroupConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Host(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="hashicorp_boundary.Host",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/boundary/r/host boundary_host}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        host_catalog_id: builtins.str,
        type: builtins.str,
        address: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/boundary/r/host boundary_host} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param host_catalog_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host#host_catalog_id Host#host_catalog_id}.
        :param type: The type of host. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host#type Host#type}
        :param address: The static address of the host resource as ``<IP>`` (note: port assignment occurs in the target resource definition, do not add :port here) or a domain name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host#address Host#address}
        :param description: The host description. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host#description Host#description}
        :param name: The host name. Defaults to the resource name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host#name Host#name}
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        '''
        config = HostConfig(
            host_catalog_id=host_catalog_id,
            type=type,
            address=address,
            description=description,
            name=name,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="resetAddress")
    def reset_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAddress", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="addressInput")
    def address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "addressInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="hostCatalogIdInput")
    def host_catalog_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostCatalogIdInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="address")
    def address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "address"))

    @address.setter
    def address(self, value: builtins.str) -> None:
        jsii.set(self, "address", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        jsii.set(self, "description", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="hostCatalogId")
    def host_catalog_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostCatalogId"))

    @host_catalog_id.setter
    def host_catalog_id(self, value: builtins.str) -> None:
        jsii.set(self, "hostCatalogId", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        jsii.set(self, "type", value)


class HostCatalog(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="hashicorp_boundary.HostCatalog",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/boundary/r/host_catalog boundary_host_catalog}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        scope_id: builtins.str,
        type: builtins.str,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/boundary/r/host_catalog boundary_host_catalog} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param scope_id: The scope ID in which the resource is created. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host_catalog#scope_id HostCatalog#scope_id}
        :param type: The host catalog type. Only ``static`` is supported. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host_catalog#type HostCatalog#type}
        :param description: The host catalog description. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host_catalog#description HostCatalog#description}
        :param name: The host catalog name. Defaults to the resource name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host_catalog#name HostCatalog#name}
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        '''
        config = HostCatalogConfig(
            scope_id=scope_id,
            type=type,
            description=description,
            name=name,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="scopeIdInput")
    def scope_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scopeIdInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        jsii.set(self, "description", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="scopeId")
    def scope_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scopeId"))

    @scope_id.setter
    def scope_id(self, value: builtins.str) -> None:
        jsii.set(self, "scopeId", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        jsii.set(self, "type", value)


@jsii.data_type(
    jsii_type="hashicorp_boundary.HostCatalogConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "scope_id": "scopeId",
        "type": "type",
        "description": "description",
        "name": "name",
    },
)
class HostCatalogConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        scope_id: builtins.str,
        type: builtins.str,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param scope_id: The scope ID in which the resource is created. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host_catalog#scope_id HostCatalog#scope_id}
        :param type: The host catalog type. Only ``static`` is supported. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host_catalog#type HostCatalog#type}
        :param description: The host catalog description. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host_catalog#description HostCatalog#description}
        :param name: The host catalog name. Defaults to the resource name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host_catalog#name HostCatalog#name}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        self._values: typing.Dict[str, typing.Any] = {
            "scope_id": scope_id,
            "type": type,
        }
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if description is not None:
            self._values["description"] = description
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[cdktf.ITerraformDependable]], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[cdktf.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[cdktf.TerraformProvider], result)

    @builtins.property
    def scope_id(self) -> builtins.str:
        '''The scope ID in which the resource is created.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host_catalog#scope_id HostCatalog#scope_id}
        '''
        result = self._values.get("scope_id")
        assert result is not None, "Required property 'scope_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''The host catalog type. Only ``static`` is supported.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host_catalog#type HostCatalog#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The host catalog description.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host_catalog#description HostCatalog#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The host catalog name. Defaults to the resource name.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host_catalog#name HostCatalog#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HostCatalogConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HostCatalogPlugin(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="hashicorp_boundary.HostCatalogPlugin",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/boundary/r/host_catalog_plugin boundary_host_catalog_plugin}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        scope_id: builtins.str,
        attributes_json: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        internal_force_update: typing.Optional[builtins.str] = None,
        internal_hmac_used_for_secrets_config_hmac: typing.Optional[builtins.str] = None,
        internal_secrets_config_hmac: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        plugin_id: typing.Optional[builtins.str] = None,
        plugin_name: typing.Optional[builtins.str] = None,
        secrets_hmac: typing.Optional[builtins.str] = None,
        secrets_json: typing.Optional[builtins.str] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/boundary/r/host_catalog_plugin boundary_host_catalog_plugin} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param scope_id: The scope ID in which the resource is created. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host_catalog_plugin#scope_id HostCatalogPlugin#scope_id}
        :param attributes_json: The attributes for the host catalog. Either values encoded with the "jsonencode" function, pre-escaped JSON string, or a file:// or env:// path. Set to a string "null" or remove the block to clear all attributes in the host catalog. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host_catalog_plugin#attributes_json HostCatalogPlugin#attributes_json}
        :param description: The host catalog description. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host_catalog_plugin#description HostCatalogPlugin#description}
        :param internal_force_update: Internal only. Used to force update so that we can always check the value of secrets. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host_catalog_plugin#internal_force_update HostCatalogPlugin#internal_force_update}
        :param internal_hmac_used_for_secrets_config_hmac: Internal only. The Boundary-provided HMAC used to calculate the current value of the HMAC'd config. Used for drift detection. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host_catalog_plugin#internal_hmac_used_for_secrets_config_hmac HostCatalogPlugin#internal_hmac_used_for_secrets_config_hmac}
        :param internal_secrets_config_hmac: Internal only. HMAC of (serverSecretsHmac + config secrets). Used for proper secrets handling. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host_catalog_plugin#internal_secrets_config_hmac HostCatalogPlugin#internal_secrets_config_hmac}
        :param name: The host catalog name. Defaults to the resource name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host_catalog_plugin#name HostCatalogPlugin#name}
        :param plugin_id: The ID of the plugin that should back the resource. This or plugin_name must be defined. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host_catalog_plugin#plugin_id HostCatalogPlugin#plugin_id}
        :param plugin_name: The name of the plugin that should back the resource. This or plugin_id must be defined. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host_catalog_plugin#plugin_name HostCatalogPlugin#plugin_name}
        :param secrets_hmac: The HMAC'd secrets value returned from the server. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host_catalog_plugin#secrets_hmac HostCatalogPlugin#secrets_hmac}
        :param secrets_json: The secrets for the host catalog. Either values encoded with the "jsonencode" function, pre-escaped JSON string, or a file:// or env:// path. Set to a string "null" to clear any existing values. NOTE: Unlike "attributes_json", removing this block will NOT clear secrets from the host catalog; this allows injecting secrets for one call, then removing them for storage. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host_catalog_plugin#secrets_json HostCatalogPlugin#secrets_json}
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        '''
        config = HostCatalogPluginConfig(
            scope_id=scope_id,
            attributes_json=attributes_json,
            description=description,
            internal_force_update=internal_force_update,
            internal_hmac_used_for_secrets_config_hmac=internal_hmac_used_for_secrets_config_hmac,
            internal_secrets_config_hmac=internal_secrets_config_hmac,
            name=name,
            plugin_id=plugin_id,
            plugin_name=plugin_name,
            secrets_hmac=secrets_hmac,
            secrets_json=secrets_json,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="resetAttributesJson")
    def reset_attributes_json(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAttributesJson", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetInternalForceUpdate")
    def reset_internal_force_update(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInternalForceUpdate", []))

    @jsii.member(jsii_name="resetInternalHmacUsedForSecretsConfigHmac")
    def reset_internal_hmac_used_for_secrets_config_hmac(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInternalHmacUsedForSecretsConfigHmac", []))

    @jsii.member(jsii_name="resetInternalSecretsConfigHmac")
    def reset_internal_secrets_config_hmac(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInternalSecretsConfigHmac", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetPluginId")
    def reset_plugin_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPluginId", []))

    @jsii.member(jsii_name="resetPluginName")
    def reset_plugin_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPluginName", []))

    @jsii.member(jsii_name="resetSecretsHmac")
    def reset_secrets_hmac(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecretsHmac", []))

    @jsii.member(jsii_name="resetSecretsJson")
    def reset_secrets_json(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecretsJson", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attributesJsonInput")
    def attributes_json_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "attributesJsonInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="internalForceUpdateInput")
    def internal_force_update_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "internalForceUpdateInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="internalHmacUsedForSecretsConfigHmacInput")
    def internal_hmac_used_for_secrets_config_hmac_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "internalHmacUsedForSecretsConfigHmacInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="internalSecretsConfigHmacInput")
    def internal_secrets_config_hmac_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "internalSecretsConfigHmacInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="pluginIdInput")
    def plugin_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pluginIdInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="pluginNameInput")
    def plugin_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pluginNameInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="scopeIdInput")
    def scope_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scopeIdInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="secretsHmacInput")
    def secrets_hmac_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretsHmacInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="secretsJsonInput")
    def secrets_json_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretsJsonInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attributesJson")
    def attributes_json(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "attributesJson"))

    @attributes_json.setter
    def attributes_json(self, value: builtins.str) -> None:
        jsii.set(self, "attributesJson", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        jsii.set(self, "description", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="internalForceUpdate")
    def internal_force_update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "internalForceUpdate"))

    @internal_force_update.setter
    def internal_force_update(self, value: builtins.str) -> None:
        jsii.set(self, "internalForceUpdate", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="internalHmacUsedForSecretsConfigHmac")
    def internal_hmac_used_for_secrets_config_hmac(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "internalHmacUsedForSecretsConfigHmac"))

    @internal_hmac_used_for_secrets_config_hmac.setter
    def internal_hmac_used_for_secrets_config_hmac(self, value: builtins.str) -> None:
        jsii.set(self, "internalHmacUsedForSecretsConfigHmac", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="internalSecretsConfigHmac")
    def internal_secrets_config_hmac(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "internalSecretsConfigHmac"))

    @internal_secrets_config_hmac.setter
    def internal_secrets_config_hmac(self, value: builtins.str) -> None:
        jsii.set(self, "internalSecretsConfigHmac", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="pluginId")
    def plugin_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pluginId"))

    @plugin_id.setter
    def plugin_id(self, value: builtins.str) -> None:
        jsii.set(self, "pluginId", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="pluginName")
    def plugin_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pluginName"))

    @plugin_name.setter
    def plugin_name(self, value: builtins.str) -> None:
        jsii.set(self, "pluginName", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="scopeId")
    def scope_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scopeId"))

    @scope_id.setter
    def scope_id(self, value: builtins.str) -> None:
        jsii.set(self, "scopeId", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="secretsHmac")
    def secrets_hmac(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretsHmac"))

    @secrets_hmac.setter
    def secrets_hmac(self, value: builtins.str) -> None:
        jsii.set(self, "secretsHmac", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="secretsJson")
    def secrets_json(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretsJson"))

    @secrets_json.setter
    def secrets_json(self, value: builtins.str) -> None:
        jsii.set(self, "secretsJson", value)


@jsii.data_type(
    jsii_type="hashicorp_boundary.HostCatalogPluginConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "scope_id": "scopeId",
        "attributes_json": "attributesJson",
        "description": "description",
        "internal_force_update": "internalForceUpdate",
        "internal_hmac_used_for_secrets_config_hmac": "internalHmacUsedForSecretsConfigHmac",
        "internal_secrets_config_hmac": "internalSecretsConfigHmac",
        "name": "name",
        "plugin_id": "pluginId",
        "plugin_name": "pluginName",
        "secrets_hmac": "secretsHmac",
        "secrets_json": "secretsJson",
    },
)
class HostCatalogPluginConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        scope_id: builtins.str,
        attributes_json: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        internal_force_update: typing.Optional[builtins.str] = None,
        internal_hmac_used_for_secrets_config_hmac: typing.Optional[builtins.str] = None,
        internal_secrets_config_hmac: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        plugin_id: typing.Optional[builtins.str] = None,
        plugin_name: typing.Optional[builtins.str] = None,
        secrets_hmac: typing.Optional[builtins.str] = None,
        secrets_json: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param scope_id: The scope ID in which the resource is created. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host_catalog_plugin#scope_id HostCatalogPlugin#scope_id}
        :param attributes_json: The attributes for the host catalog. Either values encoded with the "jsonencode" function, pre-escaped JSON string, or a file:// or env:// path. Set to a string "null" or remove the block to clear all attributes in the host catalog. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host_catalog_plugin#attributes_json HostCatalogPlugin#attributes_json}
        :param description: The host catalog description. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host_catalog_plugin#description HostCatalogPlugin#description}
        :param internal_force_update: Internal only. Used to force update so that we can always check the value of secrets. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host_catalog_plugin#internal_force_update HostCatalogPlugin#internal_force_update}
        :param internal_hmac_used_for_secrets_config_hmac: Internal only. The Boundary-provided HMAC used to calculate the current value of the HMAC'd config. Used for drift detection. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host_catalog_plugin#internal_hmac_used_for_secrets_config_hmac HostCatalogPlugin#internal_hmac_used_for_secrets_config_hmac}
        :param internal_secrets_config_hmac: Internal only. HMAC of (serverSecretsHmac + config secrets). Used for proper secrets handling. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host_catalog_plugin#internal_secrets_config_hmac HostCatalogPlugin#internal_secrets_config_hmac}
        :param name: The host catalog name. Defaults to the resource name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host_catalog_plugin#name HostCatalogPlugin#name}
        :param plugin_id: The ID of the plugin that should back the resource. This or plugin_name must be defined. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host_catalog_plugin#plugin_id HostCatalogPlugin#plugin_id}
        :param plugin_name: The name of the plugin that should back the resource. This or plugin_id must be defined. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host_catalog_plugin#plugin_name HostCatalogPlugin#plugin_name}
        :param secrets_hmac: The HMAC'd secrets value returned from the server. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host_catalog_plugin#secrets_hmac HostCatalogPlugin#secrets_hmac}
        :param secrets_json: The secrets for the host catalog. Either values encoded with the "jsonencode" function, pre-escaped JSON string, or a file:// or env:// path. Set to a string "null" to clear any existing values. NOTE: Unlike "attributes_json", removing this block will NOT clear secrets from the host catalog; this allows injecting secrets for one call, then removing them for storage. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host_catalog_plugin#secrets_json HostCatalogPlugin#secrets_json}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        self._values: typing.Dict[str, typing.Any] = {
            "scope_id": scope_id,
        }
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if attributes_json is not None:
            self._values["attributes_json"] = attributes_json
        if description is not None:
            self._values["description"] = description
        if internal_force_update is not None:
            self._values["internal_force_update"] = internal_force_update
        if internal_hmac_used_for_secrets_config_hmac is not None:
            self._values["internal_hmac_used_for_secrets_config_hmac"] = internal_hmac_used_for_secrets_config_hmac
        if internal_secrets_config_hmac is not None:
            self._values["internal_secrets_config_hmac"] = internal_secrets_config_hmac
        if name is not None:
            self._values["name"] = name
        if plugin_id is not None:
            self._values["plugin_id"] = plugin_id
        if plugin_name is not None:
            self._values["plugin_name"] = plugin_name
        if secrets_hmac is not None:
            self._values["secrets_hmac"] = secrets_hmac
        if secrets_json is not None:
            self._values["secrets_json"] = secrets_json

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[cdktf.ITerraformDependable]], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[cdktf.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[cdktf.TerraformProvider], result)

    @builtins.property
    def scope_id(self) -> builtins.str:
        '''The scope ID in which the resource is created.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host_catalog_plugin#scope_id HostCatalogPlugin#scope_id}
        '''
        result = self._values.get("scope_id")
        assert result is not None, "Required property 'scope_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def attributes_json(self) -> typing.Optional[builtins.str]:
        '''The attributes for the host catalog.

        Either values encoded with the "jsonencode" function, pre-escaped JSON string, or a file:// or env:// path. Set to a string "null" or remove the block to clear all attributes in the host catalog.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host_catalog_plugin#attributes_json HostCatalogPlugin#attributes_json}
        '''
        result = self._values.get("attributes_json")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The host catalog description.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host_catalog_plugin#description HostCatalogPlugin#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def internal_force_update(self) -> typing.Optional[builtins.str]:
        '''Internal only. Used to force update so that we can always check the value of secrets.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host_catalog_plugin#internal_force_update HostCatalogPlugin#internal_force_update}
        '''
        result = self._values.get("internal_force_update")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def internal_hmac_used_for_secrets_config_hmac(
        self,
    ) -> typing.Optional[builtins.str]:
        '''Internal only. The Boundary-provided HMAC used to calculate the current value of the HMAC'd config. Used for drift detection.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host_catalog_plugin#internal_hmac_used_for_secrets_config_hmac HostCatalogPlugin#internal_hmac_used_for_secrets_config_hmac}
        '''
        result = self._values.get("internal_hmac_used_for_secrets_config_hmac")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def internal_secrets_config_hmac(self) -> typing.Optional[builtins.str]:
        '''Internal only. HMAC of (serverSecretsHmac + config secrets). Used for proper secrets handling.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host_catalog_plugin#internal_secrets_config_hmac HostCatalogPlugin#internal_secrets_config_hmac}
        '''
        result = self._values.get("internal_secrets_config_hmac")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The host catalog name. Defaults to the resource name.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host_catalog_plugin#name HostCatalogPlugin#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def plugin_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the plugin that should back the resource. This or plugin_name must be defined.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host_catalog_plugin#plugin_id HostCatalogPlugin#plugin_id}
        '''
        result = self._values.get("plugin_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def plugin_name(self) -> typing.Optional[builtins.str]:
        '''The name of the plugin that should back the resource. This or plugin_id must be defined.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host_catalog_plugin#plugin_name HostCatalogPlugin#plugin_name}
        '''
        result = self._values.get("plugin_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secrets_hmac(self) -> typing.Optional[builtins.str]:
        '''The HMAC'd secrets value returned from the server.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host_catalog_plugin#secrets_hmac HostCatalogPlugin#secrets_hmac}
        '''
        result = self._values.get("secrets_hmac")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secrets_json(self) -> typing.Optional[builtins.str]:
        '''The secrets for the host catalog.

        Either values encoded with the "jsonencode" function, pre-escaped JSON string, or a file:// or env:// path. Set to a string "null" to clear any existing values. NOTE: Unlike "attributes_json", removing this block will NOT clear secrets from the host catalog; this allows injecting secrets for one call, then removing them for storage.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host_catalog_plugin#secrets_json HostCatalogPlugin#secrets_json}
        '''
        result = self._values.get("secrets_json")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HostCatalogPluginConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HostCatalogStatic(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="hashicorp_boundary.HostCatalogStatic",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/boundary/r/host_catalog_static boundary_host_catalog_static}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        scope_id: builtins.str,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/boundary/r/host_catalog_static boundary_host_catalog_static} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param scope_id: The scope ID in which the resource is created. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host_catalog_static#scope_id HostCatalogStatic#scope_id}
        :param description: The host catalog description. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host_catalog_static#description HostCatalogStatic#description}
        :param name: The host catalog name. Defaults to the resource name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host_catalog_static#name HostCatalogStatic#name}
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        '''
        config = HostCatalogStaticConfig(
            scope_id=scope_id,
            description=description,
            name=name,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="scopeIdInput")
    def scope_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scopeIdInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        jsii.set(self, "description", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="scopeId")
    def scope_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scopeId"))

    @scope_id.setter
    def scope_id(self, value: builtins.str) -> None:
        jsii.set(self, "scopeId", value)


@jsii.data_type(
    jsii_type="hashicorp_boundary.HostCatalogStaticConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "scope_id": "scopeId",
        "description": "description",
        "name": "name",
    },
)
class HostCatalogStaticConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        scope_id: builtins.str,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param scope_id: The scope ID in which the resource is created. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host_catalog_static#scope_id HostCatalogStatic#scope_id}
        :param description: The host catalog description. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host_catalog_static#description HostCatalogStatic#description}
        :param name: The host catalog name. Defaults to the resource name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host_catalog_static#name HostCatalogStatic#name}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        self._values: typing.Dict[str, typing.Any] = {
            "scope_id": scope_id,
        }
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if description is not None:
            self._values["description"] = description
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[cdktf.ITerraformDependable]], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[cdktf.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[cdktf.TerraformProvider], result)

    @builtins.property
    def scope_id(self) -> builtins.str:
        '''The scope ID in which the resource is created.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host_catalog_static#scope_id HostCatalogStatic#scope_id}
        '''
        result = self._values.get("scope_id")
        assert result is not None, "Required property 'scope_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The host catalog description.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host_catalog_static#description HostCatalogStatic#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The host catalog name. Defaults to the resource name.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host_catalog_static#name HostCatalogStatic#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HostCatalogStaticConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="hashicorp_boundary.HostConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "host_catalog_id": "hostCatalogId",
        "type": "type",
        "address": "address",
        "description": "description",
        "name": "name",
    },
)
class HostConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        host_catalog_id: builtins.str,
        type: builtins.str,
        address: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param host_catalog_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host#host_catalog_id Host#host_catalog_id}.
        :param type: The type of host. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host#type Host#type}
        :param address: The static address of the host resource as ``<IP>`` (note: port assignment occurs in the target resource definition, do not add :port here) or a domain name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host#address Host#address}
        :param description: The host description. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host#description Host#description}
        :param name: The host name. Defaults to the resource name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host#name Host#name}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        self._values: typing.Dict[str, typing.Any] = {
            "host_catalog_id": host_catalog_id,
            "type": type,
        }
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if address is not None:
            self._values["address"] = address
        if description is not None:
            self._values["description"] = description
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[cdktf.ITerraformDependable]], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[cdktf.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[cdktf.TerraformProvider], result)

    @builtins.property
    def host_catalog_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host#host_catalog_id Host#host_catalog_id}.'''
        result = self._values.get("host_catalog_id")
        assert result is not None, "Required property 'host_catalog_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''The type of host.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host#type Host#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def address(self) -> typing.Optional[builtins.str]:
        '''The static address of the host resource as ``<IP>`` (note: port assignment occurs in the target resource definition, do not add :port here) or a domain name.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host#address Host#address}
        '''
        result = self._values.get("address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The host description.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host#description Host#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The host name. Defaults to the resource name.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host#name Host#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HostConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HostSet(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="hashicorp_boundary.HostSet",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/boundary/r/host_set boundary_host_set}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        host_catalog_id: builtins.str,
        type: builtins.str,
        description: typing.Optional[builtins.str] = None,
        host_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/boundary/r/host_set boundary_host_set} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param host_catalog_id: The catalog for the host set. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host_set#host_catalog_id HostSet#host_catalog_id}
        :param type: The type of host set. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host_set#type HostSet#type}
        :param description: The host set description. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host_set#description HostSet#description}
        :param host_ids: The list of host IDs contained in this set. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host_set#host_ids HostSet#host_ids}
        :param name: The host set name. Defaults to the resource name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host_set#name HostSet#name}
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        '''
        config = HostSetConfig(
            host_catalog_id=host_catalog_id,
            type=type,
            description=description,
            host_ids=host_ids,
            name=name,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetHostIds")
    def reset_host_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHostIds", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="hostCatalogIdInput")
    def host_catalog_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostCatalogIdInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="hostIdsInput")
    def host_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "hostIdsInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        jsii.set(self, "description", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="hostCatalogId")
    def host_catalog_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostCatalogId"))

    @host_catalog_id.setter
    def host_catalog_id(self, value: builtins.str) -> None:
        jsii.set(self, "hostCatalogId", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="hostIds")
    def host_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "hostIds"))

    @host_ids.setter
    def host_ids(self, value: typing.List[builtins.str]) -> None:
        jsii.set(self, "hostIds", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        jsii.set(self, "type", value)


@jsii.data_type(
    jsii_type="hashicorp_boundary.HostSetConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "host_catalog_id": "hostCatalogId",
        "type": "type",
        "description": "description",
        "host_ids": "hostIds",
        "name": "name",
    },
)
class HostSetConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        host_catalog_id: builtins.str,
        type: builtins.str,
        description: typing.Optional[builtins.str] = None,
        host_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param host_catalog_id: The catalog for the host set. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host_set#host_catalog_id HostSet#host_catalog_id}
        :param type: The type of host set. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host_set#type HostSet#type}
        :param description: The host set description. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host_set#description HostSet#description}
        :param host_ids: The list of host IDs contained in this set. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host_set#host_ids HostSet#host_ids}
        :param name: The host set name. Defaults to the resource name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host_set#name HostSet#name}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        self._values: typing.Dict[str, typing.Any] = {
            "host_catalog_id": host_catalog_id,
            "type": type,
        }
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if description is not None:
            self._values["description"] = description
        if host_ids is not None:
            self._values["host_ids"] = host_ids
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[cdktf.ITerraformDependable]], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[cdktf.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[cdktf.TerraformProvider], result)

    @builtins.property
    def host_catalog_id(self) -> builtins.str:
        '''The catalog for the host set.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host_set#host_catalog_id HostSet#host_catalog_id}
        '''
        result = self._values.get("host_catalog_id")
        assert result is not None, "Required property 'host_catalog_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''The type of host set.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host_set#type HostSet#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The host set description.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host_set#description HostSet#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def host_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of host IDs contained in this set.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host_set#host_ids HostSet#host_ids}
        '''
        result = self._values.get("host_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The host set name. Defaults to the resource name.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host_set#name HostSet#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HostSetConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HostSetPlugin(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="hashicorp_boundary.HostSetPlugin",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/boundary/r/host_set_plugin boundary_host_set_plugin}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        host_catalog_id: builtins.str,
        attributes_json: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        preferred_endpoints: typing.Optional[typing.Sequence[builtins.str]] = None,
        sync_interval_seconds: typing.Optional[jsii.Number] = None,
        type: typing.Optional[builtins.str] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/boundary/r/host_set_plugin boundary_host_set_plugin} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param host_catalog_id: The catalog for the host set. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host_set_plugin#host_catalog_id HostSetPlugin#host_catalog_id}
        :param attributes_json: The attributes for the host set. Either values encoded with the "jsonencode" function, pre-escaped JSON string, or a file:// or env:// path. Set to a string "null" or remove the block to clear all attributes in the host set. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host_set_plugin#attributes_json HostSetPlugin#attributes_json}
        :param description: The host set description. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host_set_plugin#description HostSetPlugin#description}
        :param name: The host set name. Defaults to the resource name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host_set_plugin#name HostSetPlugin#name}
        :param preferred_endpoints: The ordered list of preferred endpoints. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host_set_plugin#preferred_endpoints HostSetPlugin#preferred_endpoints}
        :param sync_interval_seconds: The value to set for the sync interval seconds. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host_set_plugin#sync_interval_seconds HostSetPlugin#sync_interval_seconds}
        :param type: The type of host set. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host_set_plugin#type HostSetPlugin#type}
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        '''
        config = HostSetPluginConfig(
            host_catalog_id=host_catalog_id,
            attributes_json=attributes_json,
            description=description,
            name=name,
            preferred_endpoints=preferred_endpoints,
            sync_interval_seconds=sync_interval_seconds,
            type=type,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="resetAttributesJson")
    def reset_attributes_json(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAttributesJson", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetPreferredEndpoints")
    def reset_preferred_endpoints(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPreferredEndpoints", []))

    @jsii.member(jsii_name="resetSyncIntervalSeconds")
    def reset_sync_interval_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSyncIntervalSeconds", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attributesJsonInput")
    def attributes_json_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "attributesJsonInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="hostCatalogIdInput")
    def host_catalog_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostCatalogIdInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="preferredEndpointsInput")
    def preferred_endpoints_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "preferredEndpointsInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="syncIntervalSecondsInput")
    def sync_interval_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "syncIntervalSecondsInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attributesJson")
    def attributes_json(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "attributesJson"))

    @attributes_json.setter
    def attributes_json(self, value: builtins.str) -> None:
        jsii.set(self, "attributesJson", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        jsii.set(self, "description", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="hostCatalogId")
    def host_catalog_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostCatalogId"))

    @host_catalog_id.setter
    def host_catalog_id(self, value: builtins.str) -> None:
        jsii.set(self, "hostCatalogId", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="preferredEndpoints")
    def preferred_endpoints(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "preferredEndpoints"))

    @preferred_endpoints.setter
    def preferred_endpoints(self, value: typing.List[builtins.str]) -> None:
        jsii.set(self, "preferredEndpoints", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="syncIntervalSeconds")
    def sync_interval_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "syncIntervalSeconds"))

    @sync_interval_seconds.setter
    def sync_interval_seconds(self, value: jsii.Number) -> None:
        jsii.set(self, "syncIntervalSeconds", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        jsii.set(self, "type", value)


@jsii.data_type(
    jsii_type="hashicorp_boundary.HostSetPluginConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "host_catalog_id": "hostCatalogId",
        "attributes_json": "attributesJson",
        "description": "description",
        "name": "name",
        "preferred_endpoints": "preferredEndpoints",
        "sync_interval_seconds": "syncIntervalSeconds",
        "type": "type",
    },
)
class HostSetPluginConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        host_catalog_id: builtins.str,
        attributes_json: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        preferred_endpoints: typing.Optional[typing.Sequence[builtins.str]] = None,
        sync_interval_seconds: typing.Optional[jsii.Number] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param host_catalog_id: The catalog for the host set. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host_set_plugin#host_catalog_id HostSetPlugin#host_catalog_id}
        :param attributes_json: The attributes for the host set. Either values encoded with the "jsonencode" function, pre-escaped JSON string, or a file:// or env:// path. Set to a string "null" or remove the block to clear all attributes in the host set. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host_set_plugin#attributes_json HostSetPlugin#attributes_json}
        :param description: The host set description. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host_set_plugin#description HostSetPlugin#description}
        :param name: The host set name. Defaults to the resource name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host_set_plugin#name HostSetPlugin#name}
        :param preferred_endpoints: The ordered list of preferred endpoints. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host_set_plugin#preferred_endpoints HostSetPlugin#preferred_endpoints}
        :param sync_interval_seconds: The value to set for the sync interval seconds. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host_set_plugin#sync_interval_seconds HostSetPlugin#sync_interval_seconds}
        :param type: The type of host set. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host_set_plugin#type HostSetPlugin#type}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        self._values: typing.Dict[str, typing.Any] = {
            "host_catalog_id": host_catalog_id,
        }
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if attributes_json is not None:
            self._values["attributes_json"] = attributes_json
        if description is not None:
            self._values["description"] = description
        if name is not None:
            self._values["name"] = name
        if preferred_endpoints is not None:
            self._values["preferred_endpoints"] = preferred_endpoints
        if sync_interval_seconds is not None:
            self._values["sync_interval_seconds"] = sync_interval_seconds
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[cdktf.ITerraformDependable]], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[cdktf.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[cdktf.TerraformProvider], result)

    @builtins.property
    def host_catalog_id(self) -> builtins.str:
        '''The catalog for the host set.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host_set_plugin#host_catalog_id HostSetPlugin#host_catalog_id}
        '''
        result = self._values.get("host_catalog_id")
        assert result is not None, "Required property 'host_catalog_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def attributes_json(self) -> typing.Optional[builtins.str]:
        '''The attributes for the host set.

        Either values encoded with the "jsonencode" function, pre-escaped JSON string, or a file:// or env:// path. Set to a string "null" or remove the block to clear all attributes in the host set.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host_set_plugin#attributes_json HostSetPlugin#attributes_json}
        '''
        result = self._values.get("attributes_json")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The host set description.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host_set_plugin#description HostSetPlugin#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The host set name. Defaults to the resource name.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host_set_plugin#name HostSetPlugin#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def preferred_endpoints(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The ordered list of preferred endpoints.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host_set_plugin#preferred_endpoints HostSetPlugin#preferred_endpoints}
        '''
        result = self._values.get("preferred_endpoints")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def sync_interval_seconds(self) -> typing.Optional[jsii.Number]:
        '''The value to set for the sync interval seconds.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host_set_plugin#sync_interval_seconds HostSetPlugin#sync_interval_seconds}
        '''
        result = self._values.get("sync_interval_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''The type of host set.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host_set_plugin#type HostSetPlugin#type}
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HostSetPluginConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HostSetStatic(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="hashicorp_boundary.HostSetStatic",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/boundary/r/host_set_static boundary_host_set_static}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        host_catalog_id: builtins.str,
        description: typing.Optional[builtins.str] = None,
        host_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/boundary/r/host_set_static boundary_host_set_static} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param host_catalog_id: The catalog for the host set. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host_set_static#host_catalog_id HostSetStatic#host_catalog_id}
        :param description: The host set description. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host_set_static#description HostSetStatic#description}
        :param host_ids: The list of host IDs contained in this set. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host_set_static#host_ids HostSetStatic#host_ids}
        :param name: The host set name. Defaults to the resource name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host_set_static#name HostSetStatic#name}
        :param type: The type of host set. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host_set_static#type HostSetStatic#type}
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        '''
        config = HostSetStaticConfig(
            host_catalog_id=host_catalog_id,
            description=description,
            host_ids=host_ids,
            name=name,
            type=type,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetHostIds")
    def reset_host_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHostIds", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="hostCatalogIdInput")
    def host_catalog_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostCatalogIdInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="hostIdsInput")
    def host_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "hostIdsInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        jsii.set(self, "description", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="hostCatalogId")
    def host_catalog_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostCatalogId"))

    @host_catalog_id.setter
    def host_catalog_id(self, value: builtins.str) -> None:
        jsii.set(self, "hostCatalogId", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="hostIds")
    def host_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "hostIds"))

    @host_ids.setter
    def host_ids(self, value: typing.List[builtins.str]) -> None:
        jsii.set(self, "hostIds", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        jsii.set(self, "type", value)


@jsii.data_type(
    jsii_type="hashicorp_boundary.HostSetStaticConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "host_catalog_id": "hostCatalogId",
        "description": "description",
        "host_ids": "hostIds",
        "name": "name",
        "type": "type",
    },
)
class HostSetStaticConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        host_catalog_id: builtins.str,
        description: typing.Optional[builtins.str] = None,
        host_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param host_catalog_id: The catalog for the host set. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host_set_static#host_catalog_id HostSetStatic#host_catalog_id}
        :param description: The host set description. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host_set_static#description HostSetStatic#description}
        :param host_ids: The list of host IDs contained in this set. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host_set_static#host_ids HostSetStatic#host_ids}
        :param name: The host set name. Defaults to the resource name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host_set_static#name HostSetStatic#name}
        :param type: The type of host set. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host_set_static#type HostSetStatic#type}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        self._values: typing.Dict[str, typing.Any] = {
            "host_catalog_id": host_catalog_id,
        }
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if description is not None:
            self._values["description"] = description
        if host_ids is not None:
            self._values["host_ids"] = host_ids
        if name is not None:
            self._values["name"] = name
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[cdktf.ITerraformDependable]], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[cdktf.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[cdktf.TerraformProvider], result)

    @builtins.property
    def host_catalog_id(self) -> builtins.str:
        '''The catalog for the host set.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host_set_static#host_catalog_id HostSetStatic#host_catalog_id}
        '''
        result = self._values.get("host_catalog_id")
        assert result is not None, "Required property 'host_catalog_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The host set description.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host_set_static#description HostSetStatic#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def host_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of host IDs contained in this set.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host_set_static#host_ids HostSetStatic#host_ids}
        '''
        result = self._values.get("host_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The host set name. Defaults to the resource name.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host_set_static#name HostSetStatic#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''The type of host set.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host_set_static#type HostSetStatic#type}
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HostSetStaticConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HostStatic(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="hashicorp_boundary.HostStatic",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/boundary/r/host_static boundary_host_static}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        host_catalog_id: builtins.str,
        address: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/boundary/r/host_static boundary_host_static} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param host_catalog_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host_static#host_catalog_id HostStatic#host_catalog_id}.
        :param address: The static address of the host resource as ``<IP>`` (note: port assignment occurs in the target resource definition, do not add :port here) or a domain name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host_static#address HostStatic#address}
        :param description: The host description. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host_static#description HostStatic#description}
        :param name: The host name. Defaults to the resource name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host_static#name HostStatic#name}
        :param type: The type of host. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host_static#type HostStatic#type}
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        '''
        config = HostStaticConfig(
            host_catalog_id=host_catalog_id,
            address=address,
            description=description,
            name=name,
            type=type,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="resetAddress")
    def reset_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAddress", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="addressInput")
    def address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "addressInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="hostCatalogIdInput")
    def host_catalog_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostCatalogIdInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="address")
    def address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "address"))

    @address.setter
    def address(self, value: builtins.str) -> None:
        jsii.set(self, "address", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        jsii.set(self, "description", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="hostCatalogId")
    def host_catalog_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostCatalogId"))

    @host_catalog_id.setter
    def host_catalog_id(self, value: builtins.str) -> None:
        jsii.set(self, "hostCatalogId", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        jsii.set(self, "type", value)


@jsii.data_type(
    jsii_type="hashicorp_boundary.HostStaticConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "host_catalog_id": "hostCatalogId",
        "address": "address",
        "description": "description",
        "name": "name",
        "type": "type",
    },
)
class HostStaticConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        host_catalog_id: builtins.str,
        address: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param host_catalog_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host_static#host_catalog_id HostStatic#host_catalog_id}.
        :param address: The static address of the host resource as ``<IP>`` (note: port assignment occurs in the target resource definition, do not add :port here) or a domain name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host_static#address HostStatic#address}
        :param description: The host description. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host_static#description HostStatic#description}
        :param name: The host name. Defaults to the resource name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host_static#name HostStatic#name}
        :param type: The type of host. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host_static#type HostStatic#type}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        self._values: typing.Dict[str, typing.Any] = {
            "host_catalog_id": host_catalog_id,
        }
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if address is not None:
            self._values["address"] = address
        if description is not None:
            self._values["description"] = description
        if name is not None:
            self._values["name"] = name
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[cdktf.ITerraformDependable]], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[cdktf.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[cdktf.TerraformProvider], result)

    @builtins.property
    def host_catalog_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host_static#host_catalog_id HostStatic#host_catalog_id}.'''
        result = self._values.get("host_catalog_id")
        assert result is not None, "Required property 'host_catalog_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def address(self) -> typing.Optional[builtins.str]:
        '''The static address of the host resource as ``<IP>`` (note: port assignment occurs in the target resource definition, do not add :port here) or a domain name.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host_static#address HostStatic#address}
        '''
        result = self._values.get("address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The host description.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host_static#description HostStatic#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The host name. Defaults to the resource name.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host_static#name HostStatic#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''The type of host.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/host_static#type HostStatic#type}
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HostStaticConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ManagedGroup(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="hashicorp_boundary.ManagedGroup",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/boundary/r/managed_group boundary_managed_group}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        auth_method_id: builtins.str,
        filter: builtins.str,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/boundary/r/managed_group boundary_managed_group} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param auth_method_id: The resource ID for the auth method. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/managed_group#auth_method_id ManagedGroup#auth_method_id}
        :param filter: Boolean expression to filter the workers for this managed group. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/managed_group#filter ManagedGroup#filter}
        :param description: The managed group description. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/managed_group#description ManagedGroup#description}
        :param name: The managed group name. Defaults to the resource name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/managed_group#name ManagedGroup#name}
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        '''
        config = ManagedGroupConfig(
            auth_method_id=auth_method_id,
            filter=filter,
            description=description,
            name=name,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="authMethodIdInput")
    def auth_method_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authMethodIdInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="filterInput")
    def filter_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "filterInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="authMethodId")
    def auth_method_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authMethodId"))

    @auth_method_id.setter
    def auth_method_id(self, value: builtins.str) -> None:
        jsii.set(self, "authMethodId", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        jsii.set(self, "description", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="filter")
    def filter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "filter"))

    @filter.setter
    def filter(self, value: builtins.str) -> None:
        jsii.set(self, "filter", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        jsii.set(self, "name", value)


@jsii.data_type(
    jsii_type="hashicorp_boundary.ManagedGroupConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "auth_method_id": "authMethodId",
        "filter": "filter",
        "description": "description",
        "name": "name",
    },
)
class ManagedGroupConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        auth_method_id: builtins.str,
        filter: builtins.str,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param auth_method_id: The resource ID for the auth method. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/managed_group#auth_method_id ManagedGroup#auth_method_id}
        :param filter: Boolean expression to filter the workers for this managed group. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/managed_group#filter ManagedGroup#filter}
        :param description: The managed group description. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/managed_group#description ManagedGroup#description}
        :param name: The managed group name. Defaults to the resource name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/managed_group#name ManagedGroup#name}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        self._values: typing.Dict[str, typing.Any] = {
            "auth_method_id": auth_method_id,
            "filter": filter,
        }
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if description is not None:
            self._values["description"] = description
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[cdktf.ITerraformDependable]], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[cdktf.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[cdktf.TerraformProvider], result)

    @builtins.property
    def auth_method_id(self) -> builtins.str:
        '''The resource ID for the auth method.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/managed_group#auth_method_id ManagedGroup#auth_method_id}
        '''
        result = self._values.get("auth_method_id")
        assert result is not None, "Required property 'auth_method_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def filter(self) -> builtins.str:
        '''Boolean expression to filter the workers for this managed group.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/managed_group#filter ManagedGroup#filter}
        '''
        result = self._values.get("filter")
        assert result is not None, "Required property 'filter' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The managed group description.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/managed_group#description ManagedGroup#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The managed group name. Defaults to the resource name.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/managed_group#name ManagedGroup#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ManagedGroupConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Role(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="hashicorp_boundary.Role",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/boundary/r/role boundary_role}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        scope_id: builtins.str,
        default_role: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        grant_scope_id: typing.Optional[builtins.str] = None,
        grant_strings: typing.Optional[typing.Sequence[builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
        principal_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/boundary/r/role boundary_role} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param scope_id: The scope ID in which the resource is created. Defaults to the provider's ``default_scope`` if unset. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/role#scope_id Role#scope_id}
        :param default_role: Indicates that the role containing this value is the default role (that is, has the id 'r_default'), which triggers some specialized behavior to allow it to be imported and managed. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/role#default_role Role#default_role}
        :param description: The role description. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/role#description Role#description}
        :param grant_scope_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/role#grant_scope_id Role#grant_scope_id}.
        :param grant_strings: A list of stringified grants for the role. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/role#grant_strings Role#grant_strings}
        :param name: The role name. Defaults to the resource name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/role#name Role#name}
        :param principal_ids: A list of principal (user or group) IDs to add as principals on the role. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/role#principal_ids Role#principal_ids}
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        '''
        config = RoleConfig(
            scope_id=scope_id,
            default_role=default_role,
            description=description,
            grant_scope_id=grant_scope_id,
            grant_strings=grant_strings,
            name=name,
            principal_ids=principal_ids,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="resetDefaultRole")
    def reset_default_role(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultRole", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetGrantScopeId")
    def reset_grant_scope_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGrantScopeId", []))

    @jsii.member(jsii_name="resetGrantStrings")
    def reset_grant_strings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGrantStrings", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetPrincipalIds")
    def reset_principal_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrincipalIds", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="defaultRoleInput")
    def default_role_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "defaultRoleInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="grantScopeIdInput")
    def grant_scope_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "grantScopeIdInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="grantStringsInput")
    def grant_strings_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "grantStringsInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="principalIdsInput")
    def principal_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "principalIdsInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="scopeIdInput")
    def scope_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scopeIdInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="defaultRole")
    def default_role(self) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "defaultRole"))

    @default_role.setter
    def default_role(
        self,
        value: typing.Union[builtins.bool, cdktf.IResolvable],
    ) -> None:
        jsii.set(self, "defaultRole", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        jsii.set(self, "description", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="grantScopeId")
    def grant_scope_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "grantScopeId"))

    @grant_scope_id.setter
    def grant_scope_id(self, value: builtins.str) -> None:
        jsii.set(self, "grantScopeId", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="grantStrings")
    def grant_strings(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "grantStrings"))

    @grant_strings.setter
    def grant_strings(self, value: typing.List[builtins.str]) -> None:
        jsii.set(self, "grantStrings", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="principalIds")
    def principal_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "principalIds"))

    @principal_ids.setter
    def principal_ids(self, value: typing.List[builtins.str]) -> None:
        jsii.set(self, "principalIds", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="scopeId")
    def scope_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scopeId"))

    @scope_id.setter
    def scope_id(self, value: builtins.str) -> None:
        jsii.set(self, "scopeId", value)


@jsii.data_type(
    jsii_type="hashicorp_boundary.RoleConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "scope_id": "scopeId",
        "default_role": "defaultRole",
        "description": "description",
        "grant_scope_id": "grantScopeId",
        "grant_strings": "grantStrings",
        "name": "name",
        "principal_ids": "principalIds",
    },
)
class RoleConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        scope_id: builtins.str,
        default_role: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        grant_scope_id: typing.Optional[builtins.str] = None,
        grant_strings: typing.Optional[typing.Sequence[builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
        principal_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param scope_id: The scope ID in which the resource is created. Defaults to the provider's ``default_scope`` if unset. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/role#scope_id Role#scope_id}
        :param default_role: Indicates that the role containing this value is the default role (that is, has the id 'r_default'), which triggers some specialized behavior to allow it to be imported and managed. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/role#default_role Role#default_role}
        :param description: The role description. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/role#description Role#description}
        :param grant_scope_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/role#grant_scope_id Role#grant_scope_id}.
        :param grant_strings: A list of stringified grants for the role. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/role#grant_strings Role#grant_strings}
        :param name: The role name. Defaults to the resource name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/role#name Role#name}
        :param principal_ids: A list of principal (user or group) IDs to add as principals on the role. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/role#principal_ids Role#principal_ids}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        self._values: typing.Dict[str, typing.Any] = {
            "scope_id": scope_id,
        }
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if default_role is not None:
            self._values["default_role"] = default_role
        if description is not None:
            self._values["description"] = description
        if grant_scope_id is not None:
            self._values["grant_scope_id"] = grant_scope_id
        if grant_strings is not None:
            self._values["grant_strings"] = grant_strings
        if name is not None:
            self._values["name"] = name
        if principal_ids is not None:
            self._values["principal_ids"] = principal_ids

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[cdktf.ITerraformDependable]], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[cdktf.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[cdktf.TerraformProvider], result)

    @builtins.property
    def scope_id(self) -> builtins.str:
        '''The scope ID in which the resource is created. Defaults to the provider's ``default_scope`` if unset.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/role#scope_id Role#scope_id}
        '''
        result = self._values.get("scope_id")
        assert result is not None, "Required property 'scope_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def default_role(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Indicates that the role containing this value is the default role (that is, has the id 'r_default'), which triggers some specialized behavior to allow it to be imported and managed.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/role#default_role Role#default_role}
        '''
        result = self._values.get("default_role")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The role description.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/role#description Role#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def grant_scope_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/role#grant_scope_id Role#grant_scope_id}.'''
        result = self._values.get("grant_scope_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def grant_strings(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of stringified grants for the role.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/role#grant_strings Role#grant_strings}
        '''
        result = self._values.get("grant_strings")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The role name. Defaults to the resource name.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/role#name Role#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def principal_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of principal (user or group) IDs to add as principals on the role.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/role#principal_ids Role#principal_ids}
        '''
        result = self._values.get("principal_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RoleConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Scope(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="hashicorp_boundary.Scope",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/boundary/r/scope boundary_scope}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        scope_id: builtins.str,
        auto_create_admin_role: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        auto_create_default_role: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        global_scope: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        name: typing.Optional[builtins.str] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/boundary/r/scope boundary_scope} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param scope_id: The scope ID containing the sub scope resource. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/scope#scope_id Scope#scope_id}
        :param auto_create_admin_role: If set, when a new scope is created, the provider will not disable the functionality that automatically creates a role in the new scope and gives permissions to manage the scope to the provider's user. Marking this true makes for simpler HCL but results in role resources that are unmanaged by Terraform. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/scope#auto_create_admin_role Scope#auto_create_admin_role}
        :param auto_create_default_role: Only relevant when creating an org scope. If set, when a new scope is created, the provider will not disable the functionality that automatically creates a role in the new scope and gives listing of scopes and auth methods and the ability to authenticate to the anonymous user. Marking this true makes for simpler HCL but results in role resources that are unmanaged by Terraform. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/scope#auto_create_default_role Scope#auto_create_default_role}
        :param description: The scope description. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/scope#description Scope#description}
        :param global_scope: Indicates that the scope containing this value is the global scope, which triggers some specialized behavior to allow it to be imported and managed. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/scope#global_scope Scope#global_scope}
        :param name: The scope name. Defaults to the resource name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/scope#name Scope#name}
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        '''
        config = ScopeConfig(
            scope_id=scope_id,
            auto_create_admin_role=auto_create_admin_role,
            auto_create_default_role=auto_create_default_role,
            description=description,
            global_scope=global_scope,
            name=name,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="resetAutoCreateAdminRole")
    def reset_auto_create_admin_role(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoCreateAdminRole", []))

    @jsii.member(jsii_name="resetAutoCreateDefaultRole")
    def reset_auto_create_default_role(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoCreateDefaultRole", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetGlobalScope")
    def reset_global_scope(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGlobalScope", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="autoCreateAdminRoleInput")
    def auto_create_admin_role_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "autoCreateAdminRoleInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="autoCreateDefaultRoleInput")
    def auto_create_default_role_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "autoCreateDefaultRoleInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="globalScopeInput")
    def global_scope_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "globalScopeInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="scopeIdInput")
    def scope_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scopeIdInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="autoCreateAdminRole")
    def auto_create_admin_role(self) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "autoCreateAdminRole"))

    @auto_create_admin_role.setter
    def auto_create_admin_role(
        self,
        value: typing.Union[builtins.bool, cdktf.IResolvable],
    ) -> None:
        jsii.set(self, "autoCreateAdminRole", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="autoCreateDefaultRole")
    def auto_create_default_role(
        self,
    ) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "autoCreateDefaultRole"))

    @auto_create_default_role.setter
    def auto_create_default_role(
        self,
        value: typing.Union[builtins.bool, cdktf.IResolvable],
    ) -> None:
        jsii.set(self, "autoCreateDefaultRole", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        jsii.set(self, "description", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="globalScope")
    def global_scope(self) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "globalScope"))

    @global_scope.setter
    def global_scope(
        self,
        value: typing.Union[builtins.bool, cdktf.IResolvable],
    ) -> None:
        jsii.set(self, "globalScope", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="scopeId")
    def scope_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scopeId"))

    @scope_id.setter
    def scope_id(self, value: builtins.str) -> None:
        jsii.set(self, "scopeId", value)


@jsii.data_type(
    jsii_type="hashicorp_boundary.ScopeConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "scope_id": "scopeId",
        "auto_create_admin_role": "autoCreateAdminRole",
        "auto_create_default_role": "autoCreateDefaultRole",
        "description": "description",
        "global_scope": "globalScope",
        "name": "name",
    },
)
class ScopeConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        scope_id: builtins.str,
        auto_create_admin_role: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        auto_create_default_role: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        global_scope: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param scope_id: The scope ID containing the sub scope resource. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/scope#scope_id Scope#scope_id}
        :param auto_create_admin_role: If set, when a new scope is created, the provider will not disable the functionality that automatically creates a role in the new scope and gives permissions to manage the scope to the provider's user. Marking this true makes for simpler HCL but results in role resources that are unmanaged by Terraform. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/scope#auto_create_admin_role Scope#auto_create_admin_role}
        :param auto_create_default_role: Only relevant when creating an org scope. If set, when a new scope is created, the provider will not disable the functionality that automatically creates a role in the new scope and gives listing of scopes and auth methods and the ability to authenticate to the anonymous user. Marking this true makes for simpler HCL but results in role resources that are unmanaged by Terraform. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/scope#auto_create_default_role Scope#auto_create_default_role}
        :param description: The scope description. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/scope#description Scope#description}
        :param global_scope: Indicates that the scope containing this value is the global scope, which triggers some specialized behavior to allow it to be imported and managed. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/scope#global_scope Scope#global_scope}
        :param name: The scope name. Defaults to the resource name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/scope#name Scope#name}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        self._values: typing.Dict[str, typing.Any] = {
            "scope_id": scope_id,
        }
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if auto_create_admin_role is not None:
            self._values["auto_create_admin_role"] = auto_create_admin_role
        if auto_create_default_role is not None:
            self._values["auto_create_default_role"] = auto_create_default_role
        if description is not None:
            self._values["description"] = description
        if global_scope is not None:
            self._values["global_scope"] = global_scope
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[cdktf.ITerraformDependable]], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[cdktf.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[cdktf.TerraformProvider], result)

    @builtins.property
    def scope_id(self) -> builtins.str:
        '''The scope ID containing the sub scope resource.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/scope#scope_id Scope#scope_id}
        '''
        result = self._values.get("scope_id")
        assert result is not None, "Required property 'scope_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def auto_create_admin_role(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''If set, when a new scope is created, the provider will not disable the functionality that automatically creates a role in the new scope and gives permissions to manage the scope to the provider's user.

        Marking this true makes for simpler HCL but results in role resources that are unmanaged by Terraform.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/scope#auto_create_admin_role Scope#auto_create_admin_role}
        '''
        result = self._values.get("auto_create_admin_role")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    @builtins.property
    def auto_create_default_role(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Only relevant when creating an org scope.

        If set, when a new scope is created, the provider will not disable the functionality that automatically creates a role in the new scope and gives listing of scopes and auth methods and the ability to authenticate to the anonymous user. Marking this true makes for simpler HCL but results in role resources that are unmanaged by Terraform.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/scope#auto_create_default_role Scope#auto_create_default_role}
        '''
        result = self._values.get("auto_create_default_role")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The scope description.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/scope#description Scope#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def global_scope(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Indicates that the scope containing this value is the global scope, which triggers some specialized behavior to allow it to be imported and managed.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/scope#global_scope Scope#global_scope}
        '''
        result = self._values.get("global_scope")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The scope name. Defaults to the resource name.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/scope#name Scope#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ScopeConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Target(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="hashicorp_boundary.Target",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/boundary/r/target boundary_target}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        scope_id: builtins.str,
        type: builtins.str,
        application_credential_source_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        default_port: typing.Optional[jsii.Number] = None,
        description: typing.Optional[builtins.str] = None,
        host_source_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
        session_connection_limit: typing.Optional[jsii.Number] = None,
        session_max_seconds: typing.Optional[jsii.Number] = None,
        worker_filter: typing.Optional[builtins.str] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/boundary/r/target boundary_target} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param scope_id: The scope ID in which the resource is created. Defaults to the provider's ``default_scope`` if unset. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/target#scope_id Target#scope_id}
        :param type: The target resource type. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/target#type Target#type}
        :param application_credential_source_ids: A list of application credential source ID's. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/target#application_credential_source_ids Target#application_credential_source_ids}
        :param default_port: The default port for this target. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/target#default_port Target#default_port}
        :param description: The target description. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/target#description Target#description}
        :param host_source_ids: A list of host source ID's. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/target#host_source_ids Target#host_source_ids}
        :param name: The target name. Defaults to the resource name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/target#name Target#name}
        :param session_connection_limit: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/target#session_connection_limit Target#session_connection_limit}.
        :param session_max_seconds: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/target#session_max_seconds Target#session_max_seconds}.
        :param worker_filter: Boolean expression to filter the workers for this target. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/target#worker_filter Target#worker_filter}
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        '''
        config = TargetConfig(
            scope_id=scope_id,
            type=type,
            application_credential_source_ids=application_credential_source_ids,
            default_port=default_port,
            description=description,
            host_source_ids=host_source_ids,
            name=name,
            session_connection_limit=session_connection_limit,
            session_max_seconds=session_max_seconds,
            worker_filter=worker_filter,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="resetApplicationCredentialSourceIds")
    def reset_application_credential_source_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApplicationCredentialSourceIds", []))

    @jsii.member(jsii_name="resetDefaultPort")
    def reset_default_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultPort", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetHostSourceIds")
    def reset_host_source_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHostSourceIds", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetSessionConnectionLimit")
    def reset_session_connection_limit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSessionConnectionLimit", []))

    @jsii.member(jsii_name="resetSessionMaxSeconds")
    def reset_session_max_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSessionMaxSeconds", []))

    @jsii.member(jsii_name="resetWorkerFilter")
    def reset_worker_filter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWorkerFilter", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="applicationCredentialSourceIdsInput")
    def application_credential_source_ids_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "applicationCredentialSourceIdsInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="defaultPortInput")
    def default_port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "defaultPortInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="hostSourceIdsInput")
    def host_source_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "hostSourceIdsInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="scopeIdInput")
    def scope_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scopeIdInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="sessionConnectionLimitInput")
    def session_connection_limit_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "sessionConnectionLimitInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="sessionMaxSecondsInput")
    def session_max_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "sessionMaxSecondsInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="workerFilterInput")
    def worker_filter_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "workerFilterInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="applicationCredentialSourceIds")
    def application_credential_source_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "applicationCredentialSourceIds"))

    @application_credential_source_ids.setter
    def application_credential_source_ids(
        self,
        value: typing.List[builtins.str],
    ) -> None:
        jsii.set(self, "applicationCredentialSourceIds", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="defaultPort")
    def default_port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "defaultPort"))

    @default_port.setter
    def default_port(self, value: jsii.Number) -> None:
        jsii.set(self, "defaultPort", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        jsii.set(self, "description", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="hostSourceIds")
    def host_source_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "hostSourceIds"))

    @host_source_ids.setter
    def host_source_ids(self, value: typing.List[builtins.str]) -> None:
        jsii.set(self, "hostSourceIds", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="scopeId")
    def scope_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scopeId"))

    @scope_id.setter
    def scope_id(self, value: builtins.str) -> None:
        jsii.set(self, "scopeId", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="sessionConnectionLimit")
    def session_connection_limit(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "sessionConnectionLimit"))

    @session_connection_limit.setter
    def session_connection_limit(self, value: jsii.Number) -> None:
        jsii.set(self, "sessionConnectionLimit", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="sessionMaxSeconds")
    def session_max_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "sessionMaxSeconds"))

    @session_max_seconds.setter
    def session_max_seconds(self, value: jsii.Number) -> None:
        jsii.set(self, "sessionMaxSeconds", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        jsii.set(self, "type", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="workerFilter")
    def worker_filter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "workerFilter"))

    @worker_filter.setter
    def worker_filter(self, value: builtins.str) -> None:
        jsii.set(self, "workerFilter", value)


@jsii.data_type(
    jsii_type="hashicorp_boundary.TargetConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "scope_id": "scopeId",
        "type": "type",
        "application_credential_source_ids": "applicationCredentialSourceIds",
        "default_port": "defaultPort",
        "description": "description",
        "host_source_ids": "hostSourceIds",
        "name": "name",
        "session_connection_limit": "sessionConnectionLimit",
        "session_max_seconds": "sessionMaxSeconds",
        "worker_filter": "workerFilter",
    },
)
class TargetConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        scope_id: builtins.str,
        type: builtins.str,
        application_credential_source_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        default_port: typing.Optional[jsii.Number] = None,
        description: typing.Optional[builtins.str] = None,
        host_source_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
        session_connection_limit: typing.Optional[jsii.Number] = None,
        session_max_seconds: typing.Optional[jsii.Number] = None,
        worker_filter: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param scope_id: The scope ID in which the resource is created. Defaults to the provider's ``default_scope`` if unset. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/target#scope_id Target#scope_id}
        :param type: The target resource type. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/target#type Target#type}
        :param application_credential_source_ids: A list of application credential source ID's. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/target#application_credential_source_ids Target#application_credential_source_ids}
        :param default_port: The default port for this target. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/target#default_port Target#default_port}
        :param description: The target description. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/target#description Target#description}
        :param host_source_ids: A list of host source ID's. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/target#host_source_ids Target#host_source_ids}
        :param name: The target name. Defaults to the resource name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/target#name Target#name}
        :param session_connection_limit: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/target#session_connection_limit Target#session_connection_limit}.
        :param session_max_seconds: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/target#session_max_seconds Target#session_max_seconds}.
        :param worker_filter: Boolean expression to filter the workers for this target. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/target#worker_filter Target#worker_filter}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        self._values: typing.Dict[str, typing.Any] = {
            "scope_id": scope_id,
            "type": type,
        }
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if application_credential_source_ids is not None:
            self._values["application_credential_source_ids"] = application_credential_source_ids
        if default_port is not None:
            self._values["default_port"] = default_port
        if description is not None:
            self._values["description"] = description
        if host_source_ids is not None:
            self._values["host_source_ids"] = host_source_ids
        if name is not None:
            self._values["name"] = name
        if session_connection_limit is not None:
            self._values["session_connection_limit"] = session_connection_limit
        if session_max_seconds is not None:
            self._values["session_max_seconds"] = session_max_seconds
        if worker_filter is not None:
            self._values["worker_filter"] = worker_filter

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[cdktf.ITerraformDependable]], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[cdktf.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[cdktf.TerraformProvider], result)

    @builtins.property
    def scope_id(self) -> builtins.str:
        '''The scope ID in which the resource is created. Defaults to the provider's ``default_scope`` if unset.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/target#scope_id Target#scope_id}
        '''
        result = self._values.get("scope_id")
        assert result is not None, "Required property 'scope_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''The target resource type.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/target#type Target#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def application_credential_source_ids(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of application credential source ID's.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/target#application_credential_source_ids Target#application_credential_source_ids}
        '''
        result = self._values.get("application_credential_source_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def default_port(self) -> typing.Optional[jsii.Number]:
        '''The default port for this target.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/target#default_port Target#default_port}
        '''
        result = self._values.get("default_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The target description.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/target#description Target#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def host_source_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of host source ID's.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/target#host_source_ids Target#host_source_ids}
        '''
        result = self._values.get("host_source_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The target name. Defaults to the resource name.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/target#name Target#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def session_connection_limit(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/target#session_connection_limit Target#session_connection_limit}.'''
        result = self._values.get("session_connection_limit")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def session_max_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/target#session_max_seconds Target#session_max_seconds}.'''
        result = self._values.get("session_max_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def worker_filter(self) -> typing.Optional[builtins.str]:
        '''Boolean expression to filter the workers for this target.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/target#worker_filter Target#worker_filter}
        '''
        result = self._values.get("worker_filter")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TargetConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class User(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="hashicorp_boundary.User",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/boundary/r/user boundary_user}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        scope_id: builtins.str,
        account_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/boundary/r/user boundary_user} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param scope_id: The scope ID in which the resource is created. Defaults to the provider's ``default_scope`` if unset. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/user#scope_id User#scope_id}
        :param account_ids: Account ID's to associate with this user resource. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/user#account_ids User#account_ids}
        :param description: The user description. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/user#description User#description}
        :param name: The username. Defaults to the resource name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/user#name User#name}
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        '''
        config = UserConfig(
            scope_id=scope_id,
            account_ids=account_ids,
            description=description,
            name=name,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="resetAccountIds")
    def reset_account_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccountIds", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="accountIdsInput")
    def account_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "accountIdsInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="scopeIdInput")
    def scope_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scopeIdInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="accountIds")
    def account_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "accountIds"))

    @account_ids.setter
    def account_ids(self, value: typing.List[builtins.str]) -> None:
        jsii.set(self, "accountIds", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        jsii.set(self, "description", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="scopeId")
    def scope_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scopeId"))

    @scope_id.setter
    def scope_id(self, value: builtins.str) -> None:
        jsii.set(self, "scopeId", value)


@jsii.data_type(
    jsii_type="hashicorp_boundary.UserConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "scope_id": "scopeId",
        "account_ids": "accountIds",
        "description": "description",
        "name": "name",
    },
)
class UserConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        scope_id: builtins.str,
        account_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param scope_id: The scope ID in which the resource is created. Defaults to the provider's ``default_scope`` if unset. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/user#scope_id User#scope_id}
        :param account_ids: Account ID's to associate with this user resource. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/user#account_ids User#account_ids}
        :param description: The user description. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/user#description User#description}
        :param name: The username. Defaults to the resource name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/user#name User#name}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        self._values: typing.Dict[str, typing.Any] = {
            "scope_id": scope_id,
        }
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if account_ids is not None:
            self._values["account_ids"] = account_ids
        if description is not None:
            self._values["description"] = description
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[cdktf.ITerraformDependable]], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[cdktf.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[cdktf.TerraformProvider], result)

    @builtins.property
    def scope_id(self) -> builtins.str:
        '''The scope ID in which the resource is created. Defaults to the provider's ``default_scope`` if unset.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/user#scope_id User#scope_id}
        '''
        result = self._values.get("scope_id")
        assert result is not None, "Required property 'scope_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def account_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Account ID's to associate with this user resource.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/user#account_ids User#account_ids}
        '''
        result = self._values.get("account_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The user description.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/user#description User#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The username. Defaults to the resource name.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/boundary/r/user#name User#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UserConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "Account",
    "AccountConfig",
    "AccountOidc",
    "AccountOidcConfig",
    "AccountPassword",
    "AccountPasswordConfig",
    "AuthMethod",
    "AuthMethodConfig",
    "AuthMethodOidc",
    "AuthMethodOidcConfig",
    "AuthMethodPassword",
    "AuthMethodPasswordConfig",
    "BoundaryProvider",
    "BoundaryProviderConfig",
    "CredentialLibraryVault",
    "CredentialLibraryVaultConfig",
    "CredentialStoreVault",
    "CredentialStoreVaultConfig",
    "Group",
    "GroupConfig",
    "Host",
    "HostCatalog",
    "HostCatalogConfig",
    "HostCatalogPlugin",
    "HostCatalogPluginConfig",
    "HostCatalogStatic",
    "HostCatalogStaticConfig",
    "HostConfig",
    "HostSet",
    "HostSetConfig",
    "HostSetPlugin",
    "HostSetPluginConfig",
    "HostSetStatic",
    "HostSetStaticConfig",
    "HostStatic",
    "HostStaticConfig",
    "ManagedGroup",
    "ManagedGroupConfig",
    "Role",
    "RoleConfig",
    "Scope",
    "ScopeConfig",
    "Target",
    "TargetConfig",
    "User",
    "UserConfig",
]

publication.publish()

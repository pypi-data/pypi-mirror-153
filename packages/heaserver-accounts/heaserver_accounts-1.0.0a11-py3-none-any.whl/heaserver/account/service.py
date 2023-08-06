"""
The HEA Server AWS Accounts Microservice provides ...
"""
import logging
from asyncio import gather

from aiohttp import hdrs
from heaobject.root import type_for_name
from heaobject.volume import AWSFileSystem
from heaserver.service.heaobjectsupport import type_to_resource_url
from heaserver.service.oidcclaimhdrs import SUB
from heaserver.service.runner import init_cmd_line, routes, start, web
from heaserver.service.db import awsservicelib, mongo
from heaserver.service.wstl import builder_factory, action
from heaserver.service import response, client
from heaobject.bucket import AWSBucket
from heaobject.storage import AWSStorage
from yarl import URL


@routes.get('/ping')
async def ping(request: web.Request) -> web.Response:
    """
    For testing whether the service is up.

    :param request: the HTTP request.
    :return: Always returns status code 200.
    """
    return response.status_ok(None)


@routes.get('/awsaccounts/{id}')
@action('heaserver-accounts-account-get-open-choices', rel='hea-opener-choices', path='/awsaccounts/{id}/opener')
async def get_awsaccount(request: web.Request) -> web.Response:
    """
    Gets the AWS account with the given id. IIf no AWS credentials can be found, it uses any credentials found by the
    AWS boto3 library.

    :param request: the HTTP request.
    :return: a Response object with the requested AWS account or Not Found.
    ---
    summary: The user's AWS account.
    tags:
        - heaserver-accounts-get-awsaccount
    parameters:
        - $ref: '#/components/parameters/id'
    responses:
      '200':
        $ref: '#/components/responses/200'
      '404':
        $ref: '#/components/responses/404'
    """
    return await response.get(request, await awsservicelib.get_account_by_id(request))


@routes.get('/awsaccounts')
@routes.get('/awsaccounts/')
@action('heaserver-accounts-account-get-open-choices', rel='hea-opener-choices', path='/awsaccounts/{id}/opener')
async def get_awsaccounts(request: web.Request) -> web.Response:
    """
    Gets all AWS accounts. If no AWS credentials can be found, it uses any credentials found by the AWS boto3 library.

    :param request: the HTTP request.
    :return: a Response object with the requested AWS accounts or the empty list
    ---
    summary: The user's AWS accounts.
    tags:
        - heaserver-accounts-get-awsaccounts
    responses:
      '200':
        $ref: '#/components/responses/200'
    """
    aws_account_dicts = await awsservicelib.get_all_accounts(request)
    return await response.get_all(request, aws_account_dicts)


@routes.get('/volumes/{volume_id}/awsaccounts/me')
@action('heaserver-accounts-account-get-open-choices', rel='hea-opener-choices',
        path='/volumes/{volume_id}/awsaccounts/me/opener')
async def get_awsaccount_by_volume_id(request: web.Request) -> web.Response:
    """
    Gets the AWS account associated with the given volume id. If the volume's credentials are None, it uses any
    credentials found by the AWS boto3 library.

    :param request: the HTTP request.
    :return: the requested AWS account or Not Found.
    ---
    summary: The user's AWS account.
    tags:
        - heaserver-accounts-get-awsaccount
    parameters:
        - name: volume_id
          in: path
          required: true
          description: The id of the user's AWS volume.
          schema:
            type: string
          examples:
            example:
              summary: A volume id
              value: 666f6f2d6261722d71757578
    responses:
      '200':
        $ref: '#/components/responses/200'
      '404':
        $ref: '#/components/responses/404'
    """
    return await awsservicelib.get_account(request, request.match_info["volume_id"])


@routes.get('/awsaccounts/{id}/opener')
@action('heaserver-accounts-account-open-buckets',
        rel=f'hea-opener hea-context-aws hea-default {AWSBucket.get_mime_type()}', path='/volumes/{volume_id}/awsaccounts/me/buckets/')
@action('heaserver-accounts-account-open-storage',
        rel=f'hea-opener hea-context-aws {AWSStorage.get_mime_type()}', path='/volumes/{volume_id}/storage/')
async def get_awsaccount_opener(request: web.Request) -> web.Response:
    """
    Gets choices for opening an AWS account.

    :param request: the HTTP Request.
    :return: A Response object with a status of Multiple Choices or Not Found.
    ---
    summary: AWS account opener choices
    tags:
        - heaserver-accounts-account-get-open-choices
    parameters:
        - $ref: '#/components/parameters/id'
    responses:
      '300':
        $ref: '#/components/responses/300'
      '404':
        $ref: '#/components/responses/404'
    """
    volume_id = await awsservicelib.get_volume_id_for_account_id(request)
    request.match_info['volume_id'] = volume_id  # Needed to make the action work.
    return await awsservicelib.account_opener(request, volume_id)


@routes.get('/volumes/{volume_id}/awsaccounts/me/buckets')
@routes.get('/volumes/{volume_id}/awsaccounts/me/buckets/')
@action('heaserver-accounts-bucket-get-open-choices', rel='hea-opener-choices',
        path='/volumes/{volume_id}/buckets/{id}/opener')
async def get_buckets(request: web.Request) -> web.Response:
    """
    Gets the S3 buckets in the provided account.

    :param request: the HTTP Request.
    :return: a Response object with status code 200 and a body containing either an empty list or a list of buckets.
    ---
    summary: the buckets in an AWS account.
    tags:
        - heaserver-accounts-account-get-buckets
    parameters:
        - name: volume_id
          in: path
          required: true
          description: The id of the user's AWS volume.
          schema:
            type: string
          examples:
            example:
              summary: A volume id
              value: 666f6f2d6261722d71757578
    responses:
        '200':
            $ref: '#/components/responses/200'
    """
    logging.debug("Getting volume id by account id")

    headers = {SUB: request.headers.get(SUB)} if SUB in request.headers else None
    volume_id = request.match_info['volume_id']
    if volume_id is None:
        logging.debug("Volume id was not found")
        bucket_dicts = []
    else:
        url = URL(await type_to_resource_url(request=request, type_or_type_name=AWSBucket,
                                             file_system_type_or_type_name=AWSFileSystem)) / volume_id / 'buckets'

        async def get_one_bucket_dict(b: AWSBucket):
            logging.info("Bucket names  %s returning", b.display_name)
            return b.to_dict()
        bucket_dicts = await gather(*[get_one_bucket_dict(b) async for b in
                                      client.get_all(app=request.app, url=url, type_=AWSBucket, headers=headers)])

    return await response.get_all(request, bucket_dicts)


@routes.get('/volumes/{volume_id}/awsaccounts/me/opener')
@action('heaserver-accounts-account-open-buckets',
        rel=f'hea-opener hea-context-aws hea-default {AWSBucket.get_mime_type()}', path='/volumes/{volume_id}/buckets/')
@action('heaserver-accounts-account-open-storage',
        rel=f'hea-opener hea-context-aws {AWSStorage.get_mime_type()}', path='/volumes/{volume_id}/storage/')
async def get_awsaccount_opener_by_volume_id(request: web.Request) -> web.Response:
    """
    Gets choices for opening an AWS account.

    :param request: the HTTP Request.
    :return: A Response object with a status of Multiple Choices or Not Found.
    ---
    summary: AWS account opener choices
    tags:
        - heaserver-accounts-account-get-open-choices
    parameters:
        - name: volume_id
          in: path
          required: true
          description: The id of the user's AWS volume.
          schema:
            type: string
          examples:
            example:
              summary: A volume id
              value: 666f6f2d6261722d71757578
    responses:
      '300':
        $ref: '#/components/responses/300'
      '404':
        $ref: '#/components/responses/404'
    """
    return await awsservicelib.account_opener(request, request.match_info['volume_id'])


@routes.post('/volumes/{volume_id}/awsaccounts/me')
async def post_account_awsaccounts(request: web.Request) -> web.Response:
    """
    Posts the awsaccounts information given the correct access key and secret access key.

    :param request: the HTTP request.
    :return: the requested awsaccounts or Not Found.

    FIXME: should only be permitted by an AWS organization administrator, I would think. Need to sort out what the call looks like.
    """
    return await awsservicelib.post_account(request, request.match_info["volume_id"])


@routes.put('/volumes/{volume_id}/awsaccounts/me')
async def put_account_awsaccounts(request: web.Request) -> web.Response:
    """
    Puts the awsaccounts information given the correct access key and secret access key.

    :param request: the HTTP request.
    :return: the requested awsaccounts or Not Found.
    """
    return await awsservicelib.put_account(request, request.match_info["volume_id"])


@routes.delete('/volumes/{volume_id}/awsaccounts/me')
async def delete_account_awsaccounts(request: web.Request) -> web.Response:
    """
    Deletes the awsaccounts information given the correct access key and secret access key.

    :param request: the HTTP request.
    :return: the requested awsaccounts or Not Found.

    FIXME: should only be permitted by an AWS organization administrator, I would think. Need to sort out what the call looks like.
    """
    return await awsservicelib.delete_account(request, request.match_info["volume_id"])


def main() -> None:
    config = init_cmd_line(description='Manages account information details', default_port=8080)
    start(db=mongo.Mongo, wstl_builder_factory=builder_factory(__package__), config=config)

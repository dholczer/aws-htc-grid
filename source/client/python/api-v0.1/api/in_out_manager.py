# Copyright 2021 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
# Licensed under the Apache License, Version 2.0 https://aws.amazon.com/apache-2-0/

import logging

from api.in_out_s3 import InOutS3
from api.in_out_redis import InOutRedis

"""
This function will create appropriate InOut Storage Object depending on the configuration string.
Valid Configurations <service type>

"grid_storage_service" : "S3"
"grid_storage_service" : "REDIS"
"grid_storage_service" : "S3+REDIS"


"""

logging.basicConfig(format="%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s  - %(lineno)d - %(message)s",
                    datefmt='%H:%M:%S', level=logging.INFO)
logging.info("Init AWS Grid Connector")


def in_out_manager(grid_storage_service, s3_bucket, redis_url, s3_custom_resource=None, redis_custom_connection=None):
    """This function returns a connection to the data plane. This connection will be used for uploading and
       downloading the payload associated to the tasks

    Args:
        grid_storage_service(string): the type of storage deployed with the data plane
        s3_bucket(string): the name of the S3 bucket (valid only if an S3 bucket has been deployed with data plane)
        redis_url(string): the URL of the redis cluster (valid only if redis has been deployed with data plane)
        s3_custom_resource(object): override the default connection to AWS S3 service (valid only if an S3 bucket has been deployed with data plane)
        redis_custom_connection(object): override the default connection to the redis cluster (valid only if redis has been deployed with data plane)

    Returns:
        object: a connection to the data plane
    """
    redis_url = "redis://{}:6379".format(redis_url)
    logging.info(" storage_type {} s3 bucket {} redis_url {}".format(grid_storage_service, s3_bucket, redis_url))
    if grid_storage_service == "S3":
        return InOutS3(namespace=s3_bucket)

    elif grid_storage_service == "REDIS":
        return InOutRedis(
            namespace=s3_bucket,
            cache_url=redis_url,
            use_S3=False,
            s3_custom_resource=s3_custom_resource,
            redis_custom_connection=redis_custom_connection)

    elif grid_storage_service == "S3+REDIS":
        return InOutRedis(namespace=s3_bucket, cache_url=redis_url, use_S3=True, s3_custom_resource=s3_custom_resource)

    else:
        raise Exception("InOutManager can not parse connection string: {}".format(
            grid_storage_service))

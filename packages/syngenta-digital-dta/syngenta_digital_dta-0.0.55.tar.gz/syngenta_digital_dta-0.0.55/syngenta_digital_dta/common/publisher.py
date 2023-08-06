import boto3
import simplejson as json

from syngenta_digital_dta.common import logger


def publish(**kwargs):
    if not kwargs.get('arn') or not kwargs.get('data'):
        return
    try:
        publisher = boto3.client('sns', region_name=kwargs.get('region'), endpoint_url=kwargs.get('endpoint'))
        publish_kwargs = {
            'TopicArn': kwargs['arn'],
            'Message': json.dumps(kwargs['data']),
            'MessageAttributes': kwargs.get('attributes', {})
        }
        if kwargs.get('fifo_group_id'):
            publish_kwargs['MessageGroupId'] = kwargs['fifo_group_id']
        if kwargs.get('fifo_duplication_id'):
            publish_kwargs['MessageDeduplicationId'] = kwargs['fifo_duplication_id']
        publisher.publish(**publish_kwargs)
    except Exception as e:
        logger.log(level='WARN', log={'error': f'publish_sns_error: {e}'})

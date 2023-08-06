import itertools
import json
import logging
import os
import time
import traceback
from typing import Optional
import uuid
from contextlib import contextmanager
import decimal


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return str(o)
        return super(DecimalEncoder, self).default(o)


class Base:
    @contextmanager
    def start_span(self, operation: str, **kwargs) -> 'Span':
        s = Span(self, operation)
        self.spans.append(s)
        try:
            s.start_at_timestamp = time.process_time()
            yield s
            s.end_at_timestamp = time.process_time()
        except Exception as e:
            s.error = True
            s.exception = e
            s.exception = {
                'code': str(e),
                'traceback': traceback.format_exc().split("\n")
            }
            s.end_at_timestamp = time.process_time()


class Span(Base):
    def __init__(self, tr: 'Tracer', operation: str):
        self.tr = tr
        self.operation = operation
        self.spans = []
        self.tags = {}
        self.logs = []
        self.exception = None
        self.error = False
        # timing
        self.start_at_timestamp = None
        self.end_at_timestamp = None

    def set_tag(self, key: str, value: str):
        self.tags[key] = value

    def log_kv(self, data: dict):
        self.logs.append(data)

    def get_spans(self):
        spans = [self]
        for x in self.spans:
            [spans.append(y) for y in x.get_spans()]

        return spans

    def to_dict(self):
        if None not in [
            self.start_at_timestamp,
            self.end_at_timestamp,
        ]:
            run_total = "{:.2f} ms".format(
                (self.end_at_timestamp - self.start_at_timestamp) * 1000.0,
            )
        else:
            run_total = None

        d = {
            'operation': self.operation,
            'run_total': run_total,
        }
        if len(self.tags.values()) > 0:
            d = {
                **d,
                'tags': self.tags,
            }
        if self.exception is not None:
            d = {
                **d,
                'exception': self.exception,
            }
        if len(self.logs) > 0:
            d = {
                **d,
                'logs': self.logs,
            }
        if len(self.spans) > 0:
            d = {
                **d,
                'spans': [x.to_dict() for x in self.spans],
            }
        return d


class Tracer(Base):
    def __init__(self, service: str, operation: str):
        self.id = str(uuid.uuid4())
        self.service = service
        self.operation = operation
        self.spans = []

    @property
    def is_success(self):
        spans = list(
            itertools.chain.from_iterable(
                [x.get_spans() for x in self.spans]
            )
        )
        span_errors = [x.error for x in spans]
        return True not in span_errors

    def serilizer_data(self, data: dict, **kwargs) -> Optional[str]:
        env = kwargs.get('env', os.environ.get('ENV'))
        data_serilized = None
        try:
            data_serilized = json.dumps(data, cls=DecimalEncoder)
        except Exception as e:
            if env != 'production':
                raise e
        return data_serilized

    def close(self, **kwargs) -> dict:
        data = {
            'id': self.id,
            'service': self.service,
            'operation': self.operation,
            'is_success': self.is_success,
            'spans': [x.to_dict() for x in self.spans]
        }

        if kwargs.get('log', True):
            data_serilized = self.serilizer_data(data, env=kwargs.get('env'))
            if data_serilized is not None:
                logging.info('instrumenting-trace {}'.format(data_serilized))
            else:
                logging.error('instrumenting-error-trace error by convert')

        return data


class DjangoAPITracer(Tracer):
    def __init__(self, request, **kwargs):
        operation = "HTTP {} {}".format(
            request.method,
            request.path,
        )
        super().__init__("frontend", operation)
        self.request = request

        try:
            request_data = json.dumps(request.data, cls=DecimalEncoder)
            request_data = request.data
        except Exception as e:
            env = kwargs.get('env', os.environ.get('ENV'))
            if env != 'production':
                raise e
            request_data = {}

        self.context = {
            'request': {
                'headers': {
                    'Debug-ID': request.headers.get('Debug-ID'),
                    'User-Agent': request.META.get('HTTP_USER_AGENT'),
                    'X-Appengine-User-Ip': request.headers.get('X-Appengine-User-Ip'),
                    'X-Forwarded-For': request.headers.get('X-Forwarded-For'),
                    'django-user-id': None if request.user.is_anonymous else request.user.id,
                },
                'data': request_data,
            },
        }

    def close(self, **kwargs) -> dict:
        data = {
            **super().close(log=False),
            'context': self.context,
        }

        if kwargs.get('log', True):
            data_serilized = self.serilizer_data(data, env=kwargs.get('env'))
            if data_serilized is not None:
                logging.info('instrumenting-trace {}'.format(data_serilized))
            else:
                logging.error('instrumenting-error-trace error by convert')

        return data

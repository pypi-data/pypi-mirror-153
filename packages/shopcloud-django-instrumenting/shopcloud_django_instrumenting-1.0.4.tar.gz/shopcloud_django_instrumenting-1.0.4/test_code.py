import json
from decimal import Decimal


def test_tracer():
    from shopcloud_django_instrumenting import tracing

    tr = tracing.Tracer('name_of_service', 'name_of_operation')
    with tr.start_span('event.processing') as span:
        pass
    data = tr.close()
    print(data)


def test_tracer_decimal():
    """
    Decimal can not converted
    # https://github.com/Talk-Point/IT/issues/1996
    """
    from shopcloud_django_instrumenting import tracing

    tr = tracing.Tracer('name_of_service', 'name_of_operation')
    with tr.start_span('event.processing') as span:
        span.set_tag('decimal_value', Decimal(10.0))
    data = tr.close()

    assert data.get('spans')[0].get('tags').get('decimal_value') == Decimal(10)
    print(data)


class A:
    pass


def test_tracer_not_json_convertable():
    """
    Type can not converted
    """
    from shopcloud_django_instrumenting import tracing

    tr = tracing.Tracer('name_of_service', 'name_of_operation')
    with tr.start_span('event.processing') as span:
        span.set_tag('decimal_value', A())

    is_fired = False
    try:
        tr.close()
    except Exception as e:
        is_fired = True

    assert is_fired == True


def test_tracer_not_json_convertable_but_production():
    """
    Type can not converted but is production
    """
    from shopcloud_django_instrumenting import tracing

    tr = tracing.Tracer('name_of_service', 'name_of_operation')
    with tr.start_span('event.processing') as span:
        span.set_tag('decimal_value', A())

    is_fired = False
    try:
        tr.close(env='production')
    except Exception as e:
        is_fired = True

    assert is_fired == False


class MockUser():
    def __init__(self) -> None:
        self.id = 1
    
    @property
    def is_anonymous(self) -> bool:
        return False


class MockRequest():
    def __init__(self, **kwargs) -> None:
        self.method = 'GET'
        self.path = '/test'
        self.data = kwargs.get('data', {})
        self.headers = kwargs.get('headers', {})
        self.META = kwargs.get('META', {})
        self.user = MockUser()


def test_django_api_tracer():
    """
    Test Django API Tracer
    https://github.com/Talk-Point/IT/issues/2081
    """
    from shopcloud_django_instrumenting import tracing

    tr = tracing.DjangoAPITracer(MockRequest())
    with tr.start_span('event.processing') as span:
        span.set_tag('decimal_value', Decimal(10.0))
    data = tr.close()

    assert data.get('spans')[0].get('tags').get('decimal_value') == Decimal(10)
    print(data)


def test_django_api_tracer_with_request_data():
    """
    Test Django API Tracer
    https://github.com/Talk-Point/IT/issues/2081
    """
    from shopcloud_django_instrumenting import tracing

    tr = tracing.DjangoAPITracer(MockRequest(data={'value': Decimal(10.0)}))
    with tr.start_span('event.processing') as span:
        span.set_tag('decimal_value', Decimal(10.0))
    data = tr.close()

    is_fired = False
    try:
        tr.close(env='production')
    except Exception as e:
        is_fired = True

    assert is_fired == False


def test_django_api_tracer_with_request_data_not_serilizebar():
    """
    Test Django API Tracer
    https://github.com/Talk-Point/IT/issues/2081
    """
    from shopcloud_django_instrumenting import tracing

    is_fired = False
    try:
        tr = tracing.DjangoAPITracer(
            MockRequest(data={'value': MockUser()}
            ), 
            env='develop'
        )
        with tr.start_span('event.processing') as span:
            span.set_tag('decimal_value', Decimal(10.0))
        data = tr.close()
    except Exception as e:
        is_fired = True
    assert is_fired == True

    is_fired = False
    try:
        tr = tracing.DjangoAPITracer(
            MockRequest(data={'value': MockUser()}
            ), 
            env='production'
        )
        with tr.start_span('event.processing') as span:
            span.set_tag('decimal_value', Decimal(10.0))
        data = tr.close()
    except Exception as e:
        is_fired = True
    assert is_fired == False

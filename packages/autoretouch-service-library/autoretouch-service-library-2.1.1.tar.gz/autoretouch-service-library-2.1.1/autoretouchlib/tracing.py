import functools
import logging
import os
import re
from typing import Callable, Optional, List

from opencensus.trace import execution_context, utils
from opencensus.trace.print_exporter import PrintExporter
from opencensus.trace.tracer import Tracer
from opencensus.trace.span import SpanKind
from opencensus.trace.samplers import AlwaysOnSampler
from opencensus.ext.stackdriver.trace_exporter import StackdriverExporter
from opencensus.trace.propagation.google_cloud_format import GoogleCloudFormatPropagator
from opencensus.trace.attributes_helper import COMMON_ATTRIBUTES

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp


class TracingMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, service_name: str, trace_exporter_supplier: Optional[Callable] = None,
                 exclude_paths: List[str] = ["health", "ready", "metrics"]):
        self.__set_trace_exporter_supplier(trace_exporter_supplier)
        self.service_name = service_name
        self.propagator = GoogleCloudFormatPropagator()
        self.exclude_paths = exclude_paths
        super().__init__(app)

    def __set_trace_exporter_supplier(self, trace_exporter_supplier: Optional[Callable]):
        if trace_exporter_supplier:
            self.trace_exporter_supplier = trace_exporter_supplier
        else:
            if os.environ.get('TRACE_EXPORTER', None) == 'stackdriver':
                self.trace_exporter_supplier = StackdriverExporter
            else:
                self.trace_exporter_supplier = PrintExporter

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        if utils.disable_tracing_url(str(request.url), self.exclude_paths):
            return await call_next(request)
        try:
            span_context = self.propagator.from_headers(dict(request.headers))
            tracer = Tracer(
                exporter=self.trace_exporter_supplier(),
                sampler=AlwaysOnSampler(),
                propagator=self.propagator,
                span_context=span_context)
        except Exception as e:
            logging.error("Failed to trace request: ", e)
            return await call_next(request)
        try:
            span = tracer.start_span()
            span.span_kind = SpanKind.SERVER
            span.name = f"[{request.method}] {self.service_name} /{self.__get_url_path(str(request.url))}"
            self.__add_span_attributes(tracer, request)
        except Exception as e:
            logging.error("Failed to trace request: ", e)

        response = await call_next(request)

        try:
            # the stackdriver exporter implementation seems to work with int but not with str
            tracer.add_attribute_to_current_span(COMMON_ATTRIBUTES['HTTP_STATUS_CODE'], response.status_code)
        except Exception as e:
            logging.error("Failed to trace response: ", e)
        finally:
            tracer.end_span()
            return response

    @staticmethod
    def __get_url_path(url: str):
        # Pattern for matching the 'https://', 'http://', 'ftp://' part.
        scheme_pattern = '^(https?|ftp):\\/\\/'
        url = re.sub(scheme_pattern, '', url)
        return url.split('/', 1)[1]

    def __add_span_attributes(self, tracer: Tracer, request: Request):
        tracer.add_attribute_to_current_span('service', self.service_name)
        tracer.add_attribute_to_current_span(COMMON_ATTRIBUTES['HTTP_HOST'], request.url.hostname)
        tracer.add_attribute_to_current_span(COMMON_ATTRIBUTES['HTTP_METHOD'], request.method)
        tracer.add_attribute_to_current_span(COMMON_ATTRIBUTES['HTTP_PATH'], request.url.path)
        tracer.add_attribute_to_current_span(COMMON_ATTRIBUTES['HTTP_URL'], str(request.url))

        known_header_keys = ['organization-id', 'workflow-execution-id']
        for header_key in known_header_keys:
            if header_key in request.headers.keys():
                tracer.add_attribute_to_current_span(header_key, request.headers.get(header_key))


def with_tracing(func: Callable):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            current_span = execution_context.get_current_span()
            span = current_span.span(name=func.__qualname__)
            span.start()
        except Exception:
            return func(*args, **kwargs)
        result = func(*args, **kwargs)
        span.finish()
        return result

    return wrapper

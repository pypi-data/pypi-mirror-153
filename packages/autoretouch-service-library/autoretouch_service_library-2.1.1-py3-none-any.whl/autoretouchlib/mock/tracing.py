from typing import List, Callable

from opencensus.trace.span_data import SpanData


class MockTraceExporter:
    spans: List[SpanData] = []

    def emit(self, span_datas: List[SpanData]):
        pass

    def export(self, span_datas: List[SpanData]):
        self.spans.extend(span_datas)


with_tracing_mock: Callable[[Callable], Callable] = lambda func: func

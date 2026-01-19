from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Optional


def _utc_now() -> datetime:
    return datetime.now(UTC)


@dataclass
class ModelMetric:
    model_name: str
    timestamp: datetime = field(default_factory=_utc_now)
    request_count: int = 0
    success_count: int = 0
    error_count: int = 0

    def record_request(self, success: bool = True) -> None:
        self.request_count += 1
        if success:
            self.success_count += 1
        else:
            self.error_count += 1


class MetricsCollector:
    def __init__(self) -> None:
        self._metrics: dict[str, ModelMetric] = {}

    def track(self, model_name: str, success: bool = True) -> ModelMetric:
        if model_name not in self._metrics:
            self._metrics[model_name] = ModelMetric(model_name=model_name)

        self._metrics[model_name].record_request(success=success)
        return self._metrics[model_name]

    def get_metric(self, model_name: str) -> Optional[ModelMetric]:
        return self._metrics.get(model_name)

    def get_all_model_names(self) -> list[str]:
        return list(self._metrics.keys())

    def get_all_metrics(self) -> dict[str, ModelMetric]:
        return self._metrics.copy()

    def clear(self) -> None:
        self._metrics.clear()


_collector: Optional[MetricsCollector] = None


def get_collector() -> MetricsCollector:
    global _collector
    if _collector is None:
        _collector = MetricsCollector()
    return _collector


def track_model(model_name: str, success: bool = True) -> ModelMetric:
    return get_collector().track(model_name, success)


def get_tracked_models() -> list[str]:
    return get_collector().get_all_model_names()

import pytest

from metrics import (
    MetricsCollector,
    ModelMetric,
    get_collector,
    get_tracked_models,
    track_model,
)


class TestModelMetric:
    def test_model_metric_stores_model_name(self) -> None:
        metric = ModelMetric(model_name="gpt-4")
        assert metric.model_name == "gpt-4"

    def test_model_metric_initializes_with_zero_counts(self) -> None:
        metric = ModelMetric(model_name="claude-3")
        assert metric.request_count == 0
        assert metric.success_count == 0
        assert metric.error_count == 0

    def test_record_request_increments_request_count(self) -> None:
        metric = ModelMetric(model_name="gpt-4")
        metric.record_request()
        assert metric.request_count == 1

    def test_record_request_success_increments_success_count(self) -> None:
        metric = ModelMetric(model_name="gpt-4")
        metric.record_request(success=True)
        assert metric.success_count == 1
        assert metric.error_count == 0

    def test_record_request_failure_increments_error_count(self) -> None:
        metric = ModelMetric(model_name="gpt-4")
        metric.record_request(success=False)
        assert metric.error_count == 1
        assert metric.success_count == 0


class TestMetricsCollector:
    def test_track_creates_new_metric_for_new_model(self) -> None:
        collector = MetricsCollector()
        metric = collector.track("gpt-4")
        assert metric.model_name == "gpt-4"
        assert metric.request_count == 1

    def test_track_reuses_existing_metric_for_same_model(self) -> None:
        collector = MetricsCollector()
        collector.track("gpt-4")
        collector.track("gpt-4")
        metric = collector.get_metric("gpt-4")
        assert metric is not None
        assert metric.request_count == 2

    def test_get_all_model_names_returns_tracked_models(self) -> None:
        collector = MetricsCollector()
        collector.track("gpt-4")
        collector.track("claude-3")
        collector.track("gemini-pro")

        model_names = collector.get_all_model_names()

        assert "gpt-4" in model_names
        assert "claude-3" in model_names
        assert "gemini-pro" in model_names
        assert len(model_names) == 3

    def test_model_names_appear_in_metrics(self) -> None:
        collector = MetricsCollector()
        collector.track("gpt-4-turbo")
        collector.track("claude-3-opus")

        all_metrics = collector.get_all_metrics()

        assert "gpt-4-turbo" in all_metrics
        assert "claude-3-opus" in all_metrics
        assert all_metrics["gpt-4-turbo"].model_name == "gpt-4-turbo"
        assert all_metrics["claude-3-opus"].model_name == "claude-3-opus"

    def test_clear_removes_all_metrics(self) -> None:
        collector = MetricsCollector()
        collector.track("gpt-4")
        collector.clear()
        assert len(collector.get_all_model_names()) == 0


class TestGlobalCollector:
    @pytest.fixture(autouse=True)
    def reset_collector(self) -> None:
        get_collector().clear()

    def test_track_model_uses_global_collector(self) -> None:
        track_model("gpt-4")
        metric = get_collector().get_metric("gpt-4")
        assert metric is not None
        assert metric.model_name == "gpt-4"

    def test_get_tracked_models_returns_all_model_names(self) -> None:
        track_model("gpt-4")
        track_model("claude-3")

        models = get_tracked_models()

        assert "gpt-4" in models
        assert "claude-3" in models

    def test_model_names_show_in_metrics(self) -> None:
        track_model("llama-2-70b")
        track_model("mistral-7b")
        track_model("phi-3")

        models = get_tracked_models()
        collector = get_collector()

        for model_name in ["llama-2-70b", "mistral-7b", "phi-3"]:
            assert model_name in models
            metric = collector.get_metric(model_name)
            assert metric is not None
            assert metric.model_name == model_name

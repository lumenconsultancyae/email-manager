"""Application service orchestrating smart email analysis, cleanup, and topic grouping."""
from collections import defaultdict

from config.settings import Settings
from domain.models import (
    EmailAnalysisItem,
    EmailAnalyzerPort,
    EmailMessage,
    InboxAnalysisReport,
    TopicCluster,
)


class EmailManagementService:
    """Use-case orchestration for AGY-powered smart inbox analysis."""

    def __init__(self, analyzer: EmailAnalyzerPort, settings: Settings, container_id: str = "agy-email-worker") -> None:
        self._analyzer = analyzer
        self._settings = settings
        self._container_id = container_id

    def analyze_inbox(self, messages: list[EmailMessage]) -> InboxAnalysisReport:
        """Analyze inbox messages, identify useless emails, and group by topic."""
        if not messages:
            return InboxAnalysisReport(
                total_analyzed=0,
                useless_count=0,
                items=(),
                topic_clusters=(),
                agy_container_id=self._container_id,
            )

        items = self._analyzer.analyze_batch(
            messages=messages,
            stale_days_threshold=self._settings.stale_days_threshold,
        )
        grouped: dict[str, list[EmailAnalysisItem]] = defaultdict(list)
        for item in items:
            grouped[item.topic].append(item)

        clusters = tuple(
            TopicCluster(
                topic=topic,
                message_ids=tuple(i.message_id for i in group_items),
                summary=f"{len(group_items)} email(s) categorized under {topic}",
            )
            for topic, group_items in sorted(grouped.items(), key=lambda kv: (-len(kv[1]), kv[0]))
        )
        useless_count = sum(1 for item in items if item.is_useless)
        return InboxAnalysisReport(
            total_analyzed=len(items),
            useless_count=useless_count,
            items=tuple(items),
            topic_clusters=clusters,
            agy_container_id=self._container_id,
        )

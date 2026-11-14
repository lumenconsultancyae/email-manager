"""AGY container adapter implementing the EmailAnalyzerPort domain interface."""
from domain.models import CleanupAction, EmailAnalysisItem, EmailAnalyzerPort, EmailMessage
from utils.text_helpers import normalize_subject, truncate_preview

_PROMO_KEYWORDS = ("unsubscribe", "sale", "discount", "newsletter", "promo", "offer", "digest")
_FINANCE_KEYWORDS = ("invoice", "receipt", "payment", "billing", "statement")
_WORK_KEYWORDS = ("project", "meeting", "deadline", "sprint", "deploy", "review", "client")
_SECURITY_KEYWORDS = ("security", "verification", "password", "login", "alert", "2fa")


class AgyContainerAnalyzerAdapter(EmailAnalyzerPort):
    """Adapter that dispatches or simulates AGY container email analysis."""

    def __init__(self, container_url: str, max_preview_length: int = 160) -> None:
        self._container_url = container_url
        self._max_preview_length = max_preview_length

    @property
    def container_id(self) -> str:
        """Identifier of the configured AGY analysis container."""
        return f"agy-email-worker@{self._container_url}"

    def analyze_batch(
        self,
        messages: list[EmailMessage],
        stale_days_threshold: int,
    ) -> list[EmailAnalysisItem]:
        """Classify topic, priority, and cleanup recommendation for each email."""
        results: list[EmailAnalysisItem] = []
        for msg in messages:
            norm_subj = normalize_subject(msg.subject)
            combined = f"{norm_subj} {msg.body} {msg.sender}".lower()
            topic = self._detect_topic(combined)
            is_promo = any(kw in combined for kw in _PROMO_KEYWORDS)
            is_stale = msg.age_days >= stale_days_threshold

            if is_promo and is_stale:
                is_useless = True
                action = CleanupAction.DELETE
                reason = f"Stale promotional/newsletter email ({msg.age_days} days old)"
                priority = 10
            elif is_promo:
                is_useless = True
                action = CleanupAction.ARCHIVE
                reason = "Low-priority promotional or newsletter email"
                priority = 25
            elif is_stale and not msg.is_unread and topic == "General Updates":
                is_useless = True
                action = CleanupAction.ARCHIVE
                reason = f"Read general update older than {stale_days_threshold} days"
                priority = 30
            else:
                is_useless = False
                action = CleanupAction.KEEP
                reason = "Active or high-value thread"
                priority = 85 if topic in ("Work & Projects", "Finance & Billing", "Security & Account") else 60

            summary = truncate_preview(f"{norm_subj}: {msg.body}", self._max_preview_length)
            results.append(
                EmailAnalysisItem(
                    message_id=msg.message_id,
                    topic=topic,
                    priority_score=priority,
                    is_useless=is_useless,
                    cleanup_action=action,
                    cleanup_reason=reason,
                    summary=summary,
                )
            )
        return results

    @staticmethod
    def _detect_topic(combined_text: str) -> str:
        if any(kw in combined_text for kw in _SECURITY_KEYWORDS):
            return "Security & Account"
        if any(kw in combined_text for kw in _FINANCE_KEYWORDS):
            return "Finance & Billing"
        if any(kw in combined_text for kw in _WORK_KEYWORDS):
            return "Work & Projects"
        if any(kw in combined_text for kw in _PROMO_KEYWORDS):
            return "Promotions & Newsletters"
        return "General Updates"

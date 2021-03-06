from zerver.lib.test_classes import WebhookTestCase


class StatuspageHookTests(WebhookTestCase):
    STREAM_NAME = 'statuspage-test'
    URL_TEMPLATE = "/api/v1/external/statuspage?api_key={api_key}&stream={stream}"

    def test_statuspage_incident(self) -> None:
        expected_topic = "Database query delays: All Systems Operational"
        expected_message = """
**Database query delays**:
* State: **identified**
* Description: We just encountered that database queries are timing out resulting in inconvenience to our end users...we'll do quick fix latest by tomorrow !!!
""".strip()
        self.send_and_test_stream_message('incident_created',
                                          expected_topic,
                                          expected_message,
                                          content_type="application/x-www-form-urlencoded")

    def test_statuspage_incident_update(self) -> None:
        expected_topic = "Database query delays: All Systems Operational"
        expected_message = """
**Database query delays**:
* State: **resolved**
* Description: The database issue is resolved.
""".strip()
        self.send_and_test_stream_message('incident_update',
                                          expected_topic,
                                          expected_message,
                                          content_type="application/x-www-form-urlencoded")

    def test_statuspage_component(self) -> None:
        expected_topic = "Database component: Service Under Maintenance"
        expected_message = "**Database component** has changed status from **operational** to **under_maintenance**."
        self.send_and_test_stream_message('component_status_update',
                                          expected_topic,
                                          expected_message,
                                          content_type="application/x-www-form-urlencoded")

    def get_body(self, fixture_name: str) -> str:
        return self.webhook_fixture_data("statuspage", fixture_name, file_type="json")

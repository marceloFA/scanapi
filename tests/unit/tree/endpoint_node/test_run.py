from pytest import fixture, mark

from scanapi.exit_code import ExitCode
from scanapi.tree.endpoint_node import EndpointNode


@mark.describe("endpoint node")
@mark.describe("run")
class TestRun:
    @fixture
    def mocked_session(self, mocker):
        return mocker.patch("scanapi.tree.endpoint_node.session")

    @fixture
    def mocked_logger(self, mocker):
        return mocker.patch("scanapi.tree.endpoint_node.logger")

    @fixture
    def mocked_failed_run(self, mocker):
        return mocker.patch(
            "scanapi.tree.endpoint_node.RequestNode.run",
            return_value=None,
            side_effect=Exception(),
        )

    @fixture
    def mocked_successful_run(self, mocker):
        return mocker.patch(
            "scanapi.tree.endpoint_node.RequestNode.run",
            return_value="Test passed",
        )

    base_path = "http://foo.com"
    requests = [
        {"name": "First", "path": "http://foo.com/first",},
        {"name": "Second", "path": "http://foo.com/second",},
    ]

    @mark.context("when run fails to execute a request")
    @mark.it("an exception is logged")
    def test_when_run_fails_log_has_error(
        self, mocked_logger, mocked_failed_run
    ):

        parent_node = EndpointNode({"name": "parent-node", "requests": []})

        node = EndpointNode(
            {
                "path": self.base_path,
                "name": "child-node",
                "requests": self.requests,
            },
            parent=parent_node,
        )

        node.run()
        mocked_logger.error.assert_called_once()

    @mark.context("when run fails to execute a request")
    @mark.it("the session exit code is set to error code")
    def test_when_run_fails_with_proper_error_code(
        self, mocked_session, mocked_failed_run
    ):

        parent_node = EndpointNode({"name": "parent-node", "requests": []})
        node = EndpointNode(
            {
                "path": self.base_path,
                "name": "child-node",
                "requests": self.requests,
            },
            parent=parent_node,
        )

        node.run()
        assert mocked_session.exit_code == ExitCode.REQUEST_ERROR

    @mark.context("when run executes a request successfully")
    @mark.it("should yield a response")
    def test_when_run_is_successful(self, mocked_successful_run):

        parent_node = EndpointNode({"name": "parent-node", "requests": []})
        node = EndpointNode(
            {
                "path": self.base_path,
                "name": "child-node",
                "requests": self.requests,
            },
            parent=parent_node,
        )

        responses = node.run()

        assert list(responses) == ["Test passed", "Test passed"]

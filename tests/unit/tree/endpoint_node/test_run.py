from pytest import mark

from scanapi.exit_code import ExitCode
from scanapi.tree import endpoint_node


@mark.describe("endpoint node")
@mark.describe("run")
class TestRun:

    base_path = "http://foo.com"
    parent_node = endpoint_node.EndpointNode(
        {"name": "parent-node", "requests": []}
    )
    requests = [
        {"name": "First", "path": "http://foo.com/first",},
        {"name": "Second", "path": "http://foo.com/second",},
    ]
    node = endpoint_node.EndpointNode(
        {"path": base_path, "name": "child-node", "requests": requests},
        parent=parent_node,
    )

    @mark.context("when run fails to execute a request")
    @mark.it("an exception is logged")
    def test_when_run_fails_log_has_error(self, mocker):
        mocker.patch(
            "scanapi.tree.request_node.RequestNode.run",
            return_value=Exception(),
        )
        mocker.patch("scanapi.tree.endpoint_node.logger.error")
        self.node.run()
        endpoint_node.logger.error.assert_called_with()

    @mark.context("when run fails to execute a request")
    @mark.it("the session exit code is set to error code")
    def test_when_run_fails_with_proper_error_code(self, mocker):

        mocker.patch(
            "scanapi.tree.request_node.RequestNode.run",
            return_value=Exception(),
        )
        self.node.run()
        assert endpoint_node.session.exit_code == ExitCode.REQUEST_ERROR

    @mark.context("when run executes a request successfully")
    @mark.it("should yield a response")
    def test_when_parent_has_url(self):
        pass  # TODO: implement this

"""
Pytest plugin to parametrize and share config with fixtures
"""


import pytest


def pytest_configure(config):
    config.addinivalue_line("markers", "context: useful config values")


@pytest.fixture
def context(request):
    ctx = {}
    # https://github.com/pytest-dev/pytest-repeat/blob/master/pytest_repeat.py#L39
    # marker = request.node.get_closest_marker("context")
    # if marker:
    #     ctx.update(*marker.args, **marker.kwargs)
    # But this looks better:
    # https://docs.pytest.org/en/7.1.x/example/markers.html#passing-a-callable-to-custom-markers
    # Note: https://github.com/pytest-dev/pytest/issues/7597
    # Reversing, so now per-test marker overrides pytestmark-s from higher levels
    for marker in reversed(list(request.node.iter_markers(name="context"))):
        ctx.update(*marker.args, **marker.kwargs)
    # https://docs.pytest.org/en/7.1.x/example/parametrize.html#indirect-parametrization
    if hasattr(request, "param"):
        ctx.update(request.param)
    yield ctx


# # Usage:

# import logging
# LOG = logging.getLogger("context.demo")
# # Note how `a` value` gets overridden by test-level marker
# pytestmark = [pytest.mark.context(a=888, module=999)]


# @pytest.fixture
# def fixt(context):
#     context["fixt"] = 555
#     LOG.info(context)
#     yield context


# @pytest.mark.context(a=111)
# def test_bbb(fixt):
#     assert not fixt  # intentionally failing


# @pytest.mark.parametrize("context", [dict(a=222), dict(a=333)], indirect=True)
# def test_ddd(fixt):
#     assert not fixt  # intentionally failing

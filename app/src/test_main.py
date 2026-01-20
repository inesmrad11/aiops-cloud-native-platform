import asyncio
from src.main import root, health_check


def test_root_endpoint():
    """Call the root handler directly and validate the response."""
    data = asyncio.run(root())
    assert isinstance(data, dict)
    assert data["application"] == "AIOps Metrics Simulator"


def test_health_endpoint():
    """Call the health handler directly and validate the response."""
    data = asyncio.run(health_check())
    assert isinstance(data, dict)
    assert data["status"] == "healthy"

if __name__ == "__main__":
    pytest.main(["-v"])

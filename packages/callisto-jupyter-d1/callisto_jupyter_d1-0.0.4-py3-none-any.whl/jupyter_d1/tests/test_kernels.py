from typing import Dict

from fastapi.testclient import TestClient


class TestKernels:
    def assert_zsh_spec(self, kern):
        assert kern["kernel_name"] == "zsh"
        assert kern["resource_dir"][-11:] == "kernels/zsh"
        spec = kern["spec"]
        assert "python" in spec["argv"][0]
        assert spec["argv"][1:] == [
            "-m",
            "zsh_jupyter_kernel",
            "-f",
            "{connection_file}",
        ]
        assert spec["env"] == {}
        assert spec["metadata"] == {}
        assert spec["display_name"] == "Z shell"
        assert spec["language"] == "zsh"
        assert spec["interrupt_mode"] == "signal"

    def assert_python3_spec(self, kern):
        assert kern["kernel_name"] == "python3"
        assert kern["resource_dir"][-15:] == "kernels/python3"
        spec = kern["spec"]
        assert "python" in spec["argv"][0]
        assert spec["argv"][1:] == [
            "-m",
            "ipykernel_launcher",
            "-f",
            "{connection_file}",
        ]
        assert spec["env"] == {}
        assert spec["metadata"] == {}
        assert spec["display_name"] == "Python 3"
        assert spec["language"] == "python"
        assert spec["interrupt_mode"] == "signal"

    def assert_bash_spec(self, kern):
        assert kern["kernel_name"] == "bash"
        assert kern["resource_dir"][-12:] == "kernels/bash"
        spec = kern["spec"]
        assert "python" in spec["argv"][0]
        assert spec["argv"][1:] == [
            "-m",
            "bash_kernel",
            "-f",
            "{connection_file}",
        ]
        assert spec["env"] == {"PS1": "$"}
        assert spec["metadata"] == {}
        assert spec["display_name"] == "Bash"
        assert spec["language"] == "bash"
        assert spec["interrupt_mode"] == "signal"

    def assert_r_spec(self, kern):
        assert kern["kernel_name"] == "ir"
        assert kern["resource_dir"][-10:] == "kernels/ir"
        spec = kern["spec"]
        assert "/R" in spec["argv"][0]
        assert spec["argv"][1:] == [
            "--slave",
            "-e",
            "IRkernel::main()",
            "--args",
            "{connection_file}",
        ]
        assert spec["env"] == {}
        assert spec["metadata"] == {}
        assert spec["display_name"] == "R"
        assert spec["language"] == "R"
        assert spec["interrupt_mode"] == "signal"

    def test_specs(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        response = client.get(
            "/kernels/specs", headers=superuser_token_headers
        )
        assert response.status_code == 200
        specs = response.json()["kernel_specs"]
        assert len(specs) == 4

        for kern in specs:
            if kern["kernel_name"] == "zsh":
                self.assert_zsh_spec(kern)
            elif kern["kernel_name"] == "python3":
                self.assert_python3_spec(kern)
            elif kern["kernel_name"] == "bash":
                self.assert_bash_spec(kern)
            elif kern["kernel_name"] == "ir":
                self.assert_r_spec(kern)
            else:
                raise AssertionError("unexpected kernel spec")


class TestKernelsPermissions:
    def test_specs(
        self,
        client: TestClient,
        readonly_token_headers: Dict[str, str],
        permissionless_token_headers: Dict[str, str],
    ):
        response = client.get(
            "/kernels/specs", headers=permissionless_token_headers
        )
        assert response.status_code == 403
        response = client.get("/kernels/specs", headers=readonly_token_headers)
        assert response.status_code == 200

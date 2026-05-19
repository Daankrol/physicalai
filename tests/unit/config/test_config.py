# Copyright (C) 2025-2026 Intel Corporation
# SPDX-License-Identifier: Apache-2.0
# ruff: noqa: S101

from __future__ import annotations

from dataclasses import dataclass

import pytest

from physicalai.config import Config, instantiate_obj
from physicalai.config.mixin import FromConfig


class NestedComponent:
    def __init__(self, value: int) -> None:
        self.value = value


class SampleModel(FromConfig):
    def __init__(self, hidden_size: int, component: NestedComponent | None = None) -> None:
        self.hidden_size = hidden_size
        self.component = component


@dataclass
class SampleConfig(Config):
    hidden_size: int = 128


class TestInstantiateObj:
    def test_instantiates_nested_config(self) -> None:
        model = instantiate_obj({
            "class_path": f"{SampleModel.__module__}.SampleModel",
            "init_args": {
                "hidden_size": 256,
                "component": {
                    "class_path": f"{NestedComponent.__module__}.NestedComponent",
                    "init_args": {"value": 7},
                },
            },
        })

        assert isinstance(model, SampleModel)
        assert model.hidden_size == 256
        assert isinstance(model.component, NestedComponent)
        assert model.component.value == 7

    @pytest.mark.parametrize(
        ("contents", "message"),
        [
            ("", "class_path"),
            ("- not\n- a\n- mapping\n", "Expected YAML root to be a mapping"),
        ],
    )
    def test_file_validation(self, tmp_path, contents: str, message: str) -> None:
        path = tmp_path / "config.yaml"
        path.write_text(contents)

        with pytest.raises((TypeError, ValueError), match=message):
            instantiate_obj(path)

    def test_key_requires_mapping_value(self) -> None:
        with pytest.raises(TypeError, match="Configuration at key 'model' must be a mapping"):
            instantiate_obj({"model": 3}, key="model")


class TestFromConfig:
    def test_from_yaml_loads_mapping(self, tmp_path) -> None:
        path = tmp_path / "model.yaml"
        path.write_text("hidden_size: 512\n")

        model = SampleModel.from_yaml(path)

        assert model.hidden_size == 512

    def test_from_yaml_rejects_non_mapping_root(self, tmp_path) -> None:
        path = tmp_path / "model.yaml"
        path.write_text("- hidden_size\n")

        with pytest.raises(TypeError, match="Expected YAML root to be a mapping"):
            SampleModel.from_yaml(path)


class TestConfigLoad:
    def test_load_supports_dict_and_jsonargparse_formats(self, tmp_path) -> None:
        dict_path = tmp_path / "dict.yaml"
        dict_path.write_text("hidden_size: 256\n")

        jsonargparse_path = tmp_path / "jsonargparse.yaml"
        jsonargparse_path.write_text(
            "class_path: builtins.dict\n"
            "init_args:\n"
            "  hidden_size: 512\n",
        )

        assert SampleConfig.load(dict_path).hidden_size == 256
        assert SampleConfig.load(jsonargparse_path).hidden_size == 512

    def test_load_empty_yaml_uses_defaults(self, tmp_path) -> None:
        path = tmp_path / "config.yaml"
        path.write_text("")

        assert SampleConfig.load(path).hidden_size == 128

    @pytest.mark.parametrize(
        ("contents", "message"),
        [
            ("- not\n- a\n- mapping\n", "Expected YAML root to be a mapping"),
            ("class_path: builtins.dict\ninit_args: 3\n", "Expected 'init_args' to be a mapping"),
        ],
    )
    def test_load_validates_yaml_shape(self, tmp_path, contents: str, message: str) -> None:
        path = tmp_path / "config.yaml"
        path.write_text(contents)

        with pytest.raises(TypeError, match=message):
            SampleConfig.load(path)

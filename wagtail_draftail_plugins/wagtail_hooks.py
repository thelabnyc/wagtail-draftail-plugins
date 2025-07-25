from typing import Any, NamedTuple, TypeAlias

from django.utils.translation import gettext as _
from wagtail import hooks
from wagtail.admin.rich_text.converters.html_to_contentstate import (
    BlockElementHandler,
    InlineStyleElementHandler,
)
from wagtail.rich_text.feature_registry import FeatureRegistry
import wagtail.admin.rich_text.editors.draftail.features as draftail_features

ControlDict: TypeAlias = dict[str, Any]


class EditorPlugin(NamedTuple):
    feature_name: str
    type: str
    tag: str
    control: ControlDict


def _register_block_plugin(features: FeatureRegistry, plugin: EditorPlugin) -> None:
    features.register_editor_plugin("draftail", plugin.feature_name, draftail_features.BlockFeature(plugin.control))
    features.register_converter_rule(
        "contentstate",
        plugin.feature_name,
        {
            "from_database_format": {
                plugin.tag: BlockElementHandler(plugin.type),
            },
            "to_database_format": {
                "block_map": {
                    plugin.type: plugin.tag,
                },
            },
        },
    )


def _insert_feature_before(features: FeatureRegistry, insert_feature: str, anchor_feature: str) -> None:
    try:
        index = features.default_features.index(anchor_feature)
    except ValueError:
        index = None
    if index is not None:
        features.default_features.insert(index, insert_feature)
    else:
        features.default_features.append(insert_feature)


def _insert_feature_after(features: FeatureRegistry, insert_feature: str, anchor_feature: str) -> None:
    try:
        index = features.default_features.index(anchor_feature)
    except ValueError:
        index = None
    if index is not None:
        features.default_features.insert(index + 1, insert_feature)
    else:
        features.default_features.append(insert_feature)


@hooks.register("register_rich_text_features")  # type: ignore[misc]
def register_h1_feature(features: FeatureRegistry) -> None:
    type_ = "h1"
    tag = "h1"
    plugin = EditorPlugin(
        feature_name=type_,
        type=type_,
        tag=tag,
        control={
            "type": type_,
            "label": "H1",
            "description": _("Heading 1"),
            "element": tag,
        },
    )
    _register_block_plugin(features, plugin)
    _insert_feature_before(features, type_, "h2")  # Insert h1 before h2


@hooks.register("register_rich_text_features")  # type: ignore[misc]
def register_h5_feature(features: FeatureRegistry) -> None:
    type_ = "h5"
    tag = "h5"
    plugin = EditorPlugin(
        feature_name=type_,
        type=type_,
        tag=tag,
        control={
            "type": type_,
            "label": "H5",
            "description": _("Heading 5"),
            "element": tag,
        },
    )
    _register_block_plugin(features, plugin)
    _insert_feature_after(features, type_, "h4")  # Insert h5 after h4


@hooks.register("register_rich_text_features")  # type: ignore[misc]
def register_paragraph_feature(features: FeatureRegistry) -> None:
    type_ = "paragraph"
    tag = "p"
    plugin = EditorPlugin(
        feature_name=type_,
        type=type_,
        tag=tag,
        control={
            "type": type_,
            "label": "¶",
            "description": _("Paragraph"),
            "element": tag,
        },
    )
    _register_block_plugin(features, plugin)
    _insert_feature_before(features, type_, "h1")  # Insert paragraph before h1


@hooks.register("register_rich_text_features")  # type: ignore[misc]
def register_superscript_feature(features: FeatureRegistry) -> None:
    type_ = "superscript"
    tag = "sup"
    control: ControlDict = {
        "type": type_,
        "label": "x⁹",
        "description": _("Superscript"),
        "style": {
            "fontSize": "0.8em",
            "verticalAlign": "super",
        },
    }
    features.register_editor_plugin("draftail", type_, draftail_features.InlineStyleFeature(control))
    features.register_converter_rule(
        "contentstate",
        type_,
        {
            "from_database_format": {
                tag: InlineStyleElementHandler(type_),
            },
            "to_database_format": {
                "style_map": {
                    type_: tag,
                },
            },
        },
    )
    _insert_feature_after(features, type_, "italic")  # Insert superscript after italic


@hooks.register("register_rich_text_features")  # type: ignore[misc]
def register_subscript_feature(features: FeatureRegistry) -> None:
    type_ = "subscript"
    tag = "sub"
    control: ControlDict = {
        "type": type_,
        "label": "x₉",
        "description": _("Subscript"),
        "style": {
            "fontSize": "0.8em",
            "verticalAlign": "sub",
        },
    }
    features.register_editor_plugin("draftail", type_, draftail_features.InlineStyleFeature(control))
    features.register_converter_rule(
        "contentstate",
        type_,
        {
            "from_database_format": {
                tag: InlineStyleElementHandler(type_),
            },
            "to_database_format": {
                "style_map": {
                    type_: tag,
                },
            },
        },
    )
    _insert_feature_after(features, type_, "superscript")  # Insert superscript after italic

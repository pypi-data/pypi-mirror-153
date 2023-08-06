from collections import namedtuple
import base64
from datetime import date, datetime
import io
import os
from pathlib import Path
from PIL import Image
from typing import List
from jinja2 import Environment, FileSystemLoader
import matplotlib.pyplot as plt

from inspec_ai.__init__ import package_root_dir
from inspec_ai.quality.constants import (
    DETAILED_RESULTS_KEY_IDENTIFIER,
    EVALUATIONS_RESULTS_KEY_IDENTIFIER,
    ERROR_COUNT_KEY_IDENTIFIER,
    FAIL_COUNT_KEY_IDENTIFIER,
    MESSAGE_KEY_IDENTIFIER,
    PASS_COUNT_KEY_IDENTIFIER,
    STATUS_KEY_IDENTIFIER,
)
from inspec_ai.quality.utils import make_plain_english_inner_result, make_plain_english_result

GREEN_HEX = "#00bc80"
RED_HEX = "#f93480"

VISUALISATION_DIR: Path = package_root_dir / "quality/visualisation"
TEMPLATES_DIR = VISUALISATION_DIR / "templates"
ASSETS_DIR = VISUALISATION_DIR / "assets"
ICONS_DIR = ASSETS_DIR / "icons"
FONTS_DIR = ASSETS_DIR / "fonts"

Assets = namedtuple("Assets", "green_check_img red_cross_img exclamation_point_img nunito_fonts styles")


def generate_main_html_report(evaluation_results: dict, output_folder: Path):
    assets = _load_assets()

    completion_circle_img = _make_base64_completion_circle(
        evaluation_results[PASS_COUNT_KEY_IDENTIFIER], evaluation_results[FAIL_COUNT_KEY_IDENTIFIER], evaluation_results[ERROR_COUNT_KEY_IDENTIFIER]
    )

    html_report = _render_html_report(evaluation_results, assets, completion_circle_img)

    _save_html_report(html_report, output_folder)


def _render_html_report(evaluation_results: dict, assets: Assets, completion_circle_img):
    env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
    template = env.get_template("main_report.html")

    return template.render(
        date=date.today().strftime("%d/%m/%Y"),
        pass_count=evaluation_results[PASS_COUNT_KEY_IDENTIFIER],
        n_evaluations=len(evaluation_results[EVALUATIONS_RESULTS_KEY_IDENTIFIER]),
        evaluation_results=_format_results_for_html_report(evaluation_results),
        completion_circle_img=completion_circle_img,
        green_check_img=assets.green_check_img,
        red_cross_img=assets.red_cross_img,
        exclamation_point_img=assets.exclamation_point_img,
        nunito_fonts=assets.nunito_fonts,
        styles=assets.styles,
    )


def _save_html_report(html_report: str, output_folder: Path):
    output_path = output_folder / f"quality_standards_evaluation_{datetime.today().strftime('%Y_%m_%d_%H_%M_%S')}.html"

    with open(output_path, "w") as writer:
        writer.write(html_report)


def _load_assets() -> Assets:
    green_check_img = _load_image_as_base64(ICONS_DIR / "green_check.png")
    red_cross_img = _load_image_as_base64(ICONS_DIR / "red_cross.png")
    exclamation_point_img = _load_image_as_base64(ICONS_DIR / "exclamation_point.png")
    nunito_fonts = _load_font_family(FONTS_DIR / "nunito-v23-latin")

    with open(ASSETS_DIR / "styles.css", "r") as reader:
        styles = reader.read()

    return Assets(green_check_img, red_cross_img, exclamation_point_img, nunito_fonts, styles)


def _format_results_for_html_report(evaluation_results: dict) -> List[dict]:
    results_for_html_report = []

    for result in evaluation_results[EVALUATIONS_RESULTS_KEY_IDENTIFIER]:

        result_for_html_report = {
            "result_name": result.get("name") if result.get("name") else make_plain_english_result(result),
            STATUS_KEY_IDENTIFIER: result[STATUS_KEY_IDENTIFIER].lower(),
        }

        if DETAILED_RESULTS_KEY_IDENTIFIER in result.keys():
            inner_results = []

            for inner_result in result[DETAILED_RESULTS_KEY_IDENTIFIER]:
                inner_results.append(
                    {"result_name": make_plain_english_inner_result(inner_result), STATUS_KEY_IDENTIFIER: inner_result[STATUS_KEY_IDENTIFIER].lower()}
                )

            result_for_html_report[DETAILED_RESULTS_KEY_IDENTIFIER] = inner_results

        if MESSAGE_KEY_IDENTIFIER in result.keys():
            result_for_html_report[MESSAGE_KEY_IDENTIFIER] = result[MESSAGE_KEY_IDENTIFIER]

        results_for_html_report.append(result_for_html_report)

    return results_for_html_report


def _make_base64_completion_circle(pass_count: int, fail_count: int, error_count: int) -> str:
    data = [pass_count, fail_count, error_count]
    colors = [GREEN_HEX, RED_HEX, "#ffffff"]

    pie_sections, _ = plt.pie(data, colors=colors, wedgeprops={"edgecolor": "k", "linewidth": 5})

    pie_sections[2].set_hatch("/")
    plt.rcParams["hatch.linewidth"] = 3

    if error_count > 0:
        ax = plt.gca()
        pos = ax.get_position()
        ax.set_position([pos.x0, pos.y0, pos.width * 0.9, pos.height])
        ax.legend(handles=pie_sections, labels=["pass", "fail", "error"], fontsize=24, frameon=False, bbox_to_anchor=(1, 0.75))

    buffer = io.BytesIO()

    plt.margins(0, 0)
    plt.savefig(buffer, format="png", transparent=True, bbox_inches="tight", pad_inches=0)

    buffer.seek(0)
    encoded_completion_circle = base64.b64encode(buffer.getvalue())
    buffer.close()

    return encoded_completion_circle.decode("utf-8")


def _load_image_as_base64(filepath: Path) -> str:
    image = Image.open(filepath)
    buffer = io.BytesIO()
    image.save(buffer, "PNG")

    buffer.seek(0)
    encoded_image = base64.b64encode(buffer.getvalue())
    buffer.close()

    return encoded_image.decode("utf-8")


def _load_font_family(fonts_dir: Path) -> List[str]:
    individual_fonts = []

    for file in os.listdir(fonts_dir):
        with open(fonts_dir / file, "rb") as reader:
            font = reader.read()

        utf_font = base64.b64encode(font)

        file_ext = file.split(".")[-1]

        individual_fonts.append(f"(data:application/font-{file_ext};charset=utf-8;base64,{utf_font.decode('utf8')}) format('{file_ext}')")

    return individual_fonts

"""Tests for pathcase.core."""

from pathlib import Path

from pathcase.core import camel_case, kebab_case, plan_renames, pascal_case, snake_case, words


class TestWords:
    def test_snake(self):
        assert words("my_file_v2") == ["my", "file", "v2"]

    def test_kebab(self):
        assert words("my-file-v2") == ["my", "file", "v2"]

    def test_spaces(self):
        assert words("My File 2") == ["my", "file", "2"]

    def test_camel(self):
        assert words("myFileV2") == ["my", "file", "v2"]

    def test_pascal(self):
        assert words("MyFileV2") == ["my", "file", "v2"]

    def test_acronym(self):
        assert words("HTTPServer") == ["http", "server"]

    def test_mixed(self):
        assert words("my-file_NAME") == ["my", "file", "name"]

    def test_all_caps(self):
        assert words("REPORT") == ["report"]


class TestStyles:
    def test_snake(self):
        assert snake_case("ScreenShot 2026 09 29") == "screen_shot_2026_09_29"

    def test_kebab(self):
        assert kebab_case("ScreenShot 2026") == "screen-shot-2026"

    def test_camel(self):
        assert camel_case("my report final") == "myReportFinal"

    def test_pascal(self):
        assert pascal_case("my report final") == "MyReportFinal"


class TestPlanRenames:
    def test_extension_preserved(self):
        p = Path("My Photo.jpg")
        plan = plan_renames([p], "snake")
        assert plan == [(p, Path("my_photo.jpg"))]

    def test_no_change_is_skipped(self):
        assert plan_renames([Path("already_snake")], "snake") == []

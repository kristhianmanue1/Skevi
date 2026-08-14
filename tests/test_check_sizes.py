"""Tests para scripts/check_sizes.py. Runner: `python3 -m unittest`."""

from __future__ import annotations

import importlib.util
import io
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
_SPEC = importlib.util.spec_from_file_location(
    "check_sizes", SCRIPTS_DIR / "check_sizes.py"
)
check_sizes = importlib.util.module_from_spec(_SPEC)
sys.modules["check_sizes"] = check_sizes
_SPEC.loader.exec_module(check_sizes)


class LimitForTests(unittest.TestCase):
    def test_default_limit(self):
        self.assertEqual(check_sizes.limit_for("docs/history/foo.md"), 800)

    def test_agents_md_limit(self):
        self.assertEqual(check_sizes.limit_for("AGENTS.md"), 200)

    def test_readme_limit(self):
        self.assertEqual(check_sizes.limit_for("README.md"), 300)

    def test_template_limit(self):
        self.assertEqual(check_sizes.limit_for("templates/skevi/x.md"), 300)


class RegistryBlockTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self._orig_root = check_sizes.ROOT
        check_sizes.ROOT = self.root

    def tearDown(self):
        check_sizes.ROOT = self._orig_root

    def test_no_block_is_not_a_failure(self):
        text = "# AGENTS.md\n\nsin bloque de registro.\n"
        self.assertEqual(
            check_sizes.check_registry_block(Path("AGENTS.md"), text), []
        )

    def test_unbalanced_delimiters(self):
        text = "<!-- skevi:registry:start -->\n[skevi]\nx=y.md\n"
        failures = check_sizes.check_registry_block(Path("AGENTS.md"), text)
        self.assertEqual(len(failures), 1)
        self.assertIn("desbalanceados", failures[0])

    def test_missing_skevi_section(self):
        text = (
            "<!-- skevi:registry:start -->\n"
            "x=y.md\n"
            "<!-- skevi:registry:end -->\n"
        )
        failures = check_sizes.check_registry_block(Path("AGENTS.md"), text)
        self.assertTrue(any("sin sección [skevi]" in f for f in failures))

    def test_valid_block_points_to_existing_file(self):
        (self.root / "contexto.md").write_text("hola\n", encoding="utf-8")
        text = (
            "<!-- skevi:registry:start -->\n"
            "[skevi]\n"
            "contexto=contexto.md\n"
            "<!-- skevi:registry:end -->\n"
        )
        self.assertEqual(
            check_sizes.check_registry_block(Path("AGENTS.md"), text), []
        )

    def test_entry_points_to_missing_file(self):
        text = (
            "<!-- skevi:registry:start -->\n"
            "[skevi]\n"
            "contexto=no-existe.md\n"
            "<!-- skevi:registry:end -->\n"
        )
        failures = check_sizes.check_registry_block(Path("AGENTS.md"), text)
        self.assertTrue(any("ruta inexistente" in f for f in failures))

    def test_entry_escaping_root_is_rejected(self):
        text = (
            "<!-- skevi:registry:start -->\n"
            "[skevi]\n"
            "contexto=../fuera.md\n"
            "<!-- skevi:registry:end -->\n"
        )
        failures = check_sizes.check_registry_block(Path("AGENTS.md"), text)
        self.assertTrue(any("fuera de la raíz" in f for f in failures))


class MainIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self._orig_root = check_sizes.ROOT
        check_sizes.ROOT = self.root
        self._make_minimal_valid_repo()

    def tearDown(self):
        check_sizes.ROOT = self._orig_root

    def _make_minimal_valid_repo(self):
        for relative in sorted(check_sizes.REQUIRED):
            path = self.root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(f"# {relative}\n", encoding="utf-8")

    def _run_main(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            exit_code = check_sizes.main()
        return exit_code, buf.getvalue()

    def test_minimal_valid_repo_passes(self):
        exit_code, output = self._run_main()
        self.assertEqual(exit_code, 0)
        self.assertTrue(output.startswith("OK —"))

    def test_missing_required_file_fails(self):
        (self.root / "README.md").unlink()
        exit_code, output = self._run_main()
        self.assertEqual(exit_code, 1)
        self.assertIn("falta archivo requerido: README.md", output)

    def test_stray_root_markdown_fails(self):
        (self.root / "NOTAS.md").write_text("suelto\n", encoding="utf-8")
        exit_code, output = self._run_main()
        self.assertEqual(exit_code, 1)
        self.assertIn("Markdown operativo suelto en raíz", output)
        self.assertIn("NOTAS.md", output)

    def test_file_over_default_limit_fails(self):
        oversized = self.root / "docs" / "historia" / "largo.md"
        oversized.parent.mkdir(parents=True, exist_ok=True)
        oversized.write_text("\n".join(f"linea {i}" for i in range(801)) + "\n")
        exit_code, output = self._run_main()
        self.assertEqual(exit_code, 1)
        self.assertIn("801 líneas > límite 800", output)

    def test_file_at_default_limit_passes(self):
        exact = self.root / "docs" / "historia" / "justo.md"
        exact.parent.mkdir(parents=True, exist_ok=True)
        exact.write_text("\n".join(f"linea {i}" for i in range(800)) + "\n")
        exit_code, _ = self._run_main()
        self.assertEqual(exit_code, 0)

    def test_skip_dirs_are_not_scanned(self):
        node_modules = self.root / "node_modules" / "pkg"
        node_modules.mkdir(parents=True, exist_ok=True)
        (node_modules / "huge.md").write_text(
            "\n".join(f"linea {i}" for i in range(2000)) + "\n"
        )
        exit_code, _ = self._run_main()
        self.assertEqual(exit_code, 0)


if __name__ == "__main__":
    unittest.main()

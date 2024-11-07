import pytest
import importlib
import sys
from pathlib import Path

# Mapear as camadas e as dependências permitidas
ARCHITECTURE_RULES = {
    "src.api": ["src.application", "src.core"],
    "src.application": ["src.core"],
    "src.core": [],  # Core não deve depender de ninguém
    "src.infrastructure": ["src.application", "src.core"],
}

def get_imports(module_name):
    """Obtem os módulos importados em um módulo específico."""
    module = importlib.import_module(module_name)
    imports = set()

    for name in dir(module):
        attr = getattr(module, name)
        if isinstance(attr, type(module)):
            # Adicionar apenas os módulos dentro do projeto
            if attr.__name__.startswith("src."):
                imports.add(attr.__name__)

    return imports

@pytest.mark.parametrize("module,allowed_imports", ARCHITECTURE_RULES.items())
def test_module_dependencies(module, allowed_imports):
    """Verifica se os módulos estão importando apenas o que é permitido."""
    imports = get_imports(module)
    for imp in imports:
        assert imp in allowed_imports, f"O módulo {module} não deveria importar {imp}"

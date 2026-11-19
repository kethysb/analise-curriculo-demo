"""Cruza requisitos de uma vaga e evidências autodeclaradas."""
import argparse
import json
import unicodedata
from pathlib import Path


def normalize(value):
    return " ".join("".join(
        char for char in unicodedata.normalize("NFKD", value.casefold())
        if not unicodedata.combining(char)
    ).split())


def compare(job, evidence):
    indexed = [(normalize(item["habilidade"]), item["descricao"].strip()) for item in evidence]
    for requirement in job:
        aliases = {normalize(name) for name in [requirement["requisito"], *requirement.get("termos", [])]}
        matches = list(dict.fromkeys(text for name, text in indexed if name and name in aliases and text))
        yield {**requirement, "evidencias": matches,
               "status": "evidência declarada" if matches else "a confirmar"}


def read_array(path, fields):
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(data, list):
        raise ValueError(f"{path.name}: esperado um array.")
    for index, item in enumerate(data, 1):
        if not isinstance(item, dict) or any(
            not isinstance(item.get(field), str) or not item[field].strip() for field in fields
        ):
            raise ValueError(f"{path.name}: campos inválidos na entrada {index}.")
        if "termos" in item and (not isinstance(item["termos"], list) or
                                 any(not isinstance(term, str) for term in item["termos"])):
            raise ValueError(f"{path.name}: termos inválidos na entrada {index}.")
        if "tipo" in fields and normalize(item["tipo"]) not in {"obrigatorio", "diferencial"}:
            raise ValueError(f"{path.name}: tipo inválido na entrada {index}.")
    return data


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("vaga", type=Path)
    parser.add_argument("evidencias", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    try:
        job = read_array(args.vaga, ("requisito", "tipo"))
        evidence = read_array(args.evidencias, ("habilidade", "descricao"))
        rows = list(compare(job, evidence))
    except (OSError, ValueError) as exc:
        parser.exit(1, f"Erro: {exc}\n")

    if args.json:
        print(json.dumps(rows, ensure_ascii=False, indent=2))
        return
    for row in rows:
        print(f'[{row["tipo"]}] {row["requisito"]} — {row["status"]}')
        for text in row["evidencias"]:
            print(f"  - {text}")


if __name__ == "__main__":
    main()

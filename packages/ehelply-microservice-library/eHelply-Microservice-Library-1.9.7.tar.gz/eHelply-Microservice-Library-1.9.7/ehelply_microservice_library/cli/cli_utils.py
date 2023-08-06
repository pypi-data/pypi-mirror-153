import typer
import base64
from typing import List

cli = typer.Typer()


RESERVED_WORDS: List[str] = ["playground", "test", "testing", "privileged"]

@cli.command()
def encode_json_header(
        json: str = typer.Option(..., prompt=True, help="JSON string to encrypt"),
):
    json_bytes = json.encode('utf-8')
    base64_bytes = base64.b64encode(json_bytes)
    base64_str = base64_bytes.decode('utf-8')
    typer.echo(base64_str)


def prune_reserved_words(openapi_data: dict):
    for endpoint_path, endpoints in openapi_data['paths'].items():
        remove: List[str] = []
        for endpoint_verb, endpoint in endpoints.items():
            for reserved_word in RESERVED_WORDS:
                if reserved_word in endpoint['tags']:
                    remove.append(endpoint_verb)
        for remove_verb in remove:
            del endpoints[remove_verb]

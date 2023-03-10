from ansible.errors import AnsibleError
from ansible.parsing.vault import VaultLib, parse_vaulttext_envelope
from ansible.parsing.vault import b_HEADER as b_VAULT_HEADER
from ansible.module_utils.common.text.converters import to_bytes, to_text

b_MV_PREFIX = b'!multi_vault |'
FAIL_DECRYPT = True  # fail-exit when all decryptions failed
FIRST_MATCH = True  # stop trying to decrypt additional blocks when one was successful


def _get_vault_blocks(b_encrypted_blocks: bytes) -> list:
    idx_encrypted_blocks = []
    list_b_encrypted_blocks = []
    find_start_idx = 0

    while True:
        if len(list_b_encrypted_blocks) == 0:
            _block_start = b_encrypted_blocks.find(b_VAULT_HEADER, find_start_idx)

        else:
            _block_start = idx_encrypted_blocks[-1][1] + 1

        find_start_idx = _block_start + len(b_VAULT_HEADER)
        _block_stop = b_encrypted_blocks.find(b_VAULT_HEADER, find_start_idx)

        if _block_stop == -1:
            _block_stop = len(b_encrypted_blocks)

        else:
            _block_stop -= 1

        idx_encrypted_blocks.append((_block_start, _block_stop))
        list_b_encrypted_blocks.append(
            b_encrypted_blocks[_block_start:_block_stop].replace(b' ', b'\n')
        )

        if _block_stop == len(b_encrypted_blocks):
            break

    return list_b_encrypted_blocks


def _decrypt(vault_parser: VaultLib, vault_blocks: list, result: dict, first_match: bool) -> dict:
    for block_idx, b_vault_block in enumerate(vault_blocks):
        _, _, _, vault_id = parse_vaulttext_envelope(
            b_vault_block, filename=None,
        )

        try:
            result['data'] = vault_parser.decrypt(to_text(b_vault_block))
            result['vault_id'] = vault_id
            result['info'].append(
                f"Decrypt successful for block {block_idx} with vault-id: '{vault_id}'"
            )
            if first_match:
                break

        except AnsibleError:
            result['info'].append(
                f"Decrypt failed for block {block_idx} with vault-id: '{vault_id}'"
            )
            continue

    return result


def decrypt_single(vault_data: str, args: dict, vault_parser: VaultLib, fail_validate: bool = True) -> dict:
    result = dict(
        failed=False,
        vault_id=None,
        data=None,
        info=[],
        error='',
    )

    fail_decryption = args['fail'] if 'fail' in args else FAIL_DECRYPT
    first_match = args['first'] if 'first' in args else FIRST_MATCH

    b_encrypted_blocks = to_bytes(
        str(vault_data).strip(),
        errors='strict',
        encoding='utf-8'
    )

    if not b_encrypted_blocks.startswith(b_MV_PREFIX):
        if fail_validate:
            if fail_decryption:
                result['failed'] = True

            result['error'] = f"Value must be string starting with '{to_text(b_MV_PREFIX)}'"

        return result

    result = _decrypt(
        result=result,
        vault_blocks=_get_vault_blocks(b_encrypted_blocks),
        vault_parser=vault_parser,
        first_match=first_match,
    )

    if result['data'] is None:
        if fail_decryption:
            result['failed'] = True

        result['error'] = 'Failed to decrypt vault-data!'

    return result

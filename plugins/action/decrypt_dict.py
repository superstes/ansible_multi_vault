from ansible.plugins.action import ActionBase
from ansible.errors import AnsibleActionFail
from ansible.utils.unsafe_proxy import AnsibleUnsafeText

from ._shared import decrypt_single, FAIL_DECRYPT


class ActionModule(ActionBase):
    def run(self, tmp=None, task_vars=None):
        del tmp, task_vars

        vault_data = self._task.args['vault'] if 'vault' in self._task.args else None
        if vault_data is None:
            raise AnsibleActionFail("You need to provide the 'vault' parameter!")

        fail_decryption = self._task.args['fail'] if 'fail' in self._task.args else FAIL_DECRYPT

        result = dict(
            failed=False,
            vault_id=None,
            data={},
            info={},
            error='',
        )

        def decrypt_string(value: (str, AnsibleUnsafeText)) -> tuple:
            if isinstance(value, AnsibleUnsafeText):
                value = str(value)

            _fail = False
            _result = decrypt_single(
                args=self._task.args,
                vault_parser=self._loader._vault,
                vault_data=value,
                fail_validate=False,  # strings that are no multi-vaults
            )
            _data = value

            if _result['failed']:
                result['error'] = _result['error']
                _fail = True

            if _result['data'] is not None:
                _data = _result['data']

            return _fail, _data, _result['info']

        def recursive_decrypt(rec_data: dict) -> tuple:
            _fail = False
            _data = {}
            _info = {}

            for k, v in rec_data.items():
                _v_info = None
                _v_data = v

                if isinstance(v, (str, AnsibleUnsafeText)):
                    _v_fail, _v_data, _v_info = decrypt_string(v)
                    if not _fail:
                        _fail = _v_fail

                elif isinstance(v, list):
                    _v_info = []
                    _v_data = []

                    for e in v:
                        if isinstance(e, (str, AnsibleUnsafeText)):
                            _e_fail, _e_data, _e_info = decrypt_string(e)
                            if not _fail:
                                _fail = _e_fail

                            _v_info.append(_e_info)
                            _v_data.append(_e_data)

                    if len(_v_data) == 0:
                        _v_data = v

                elif isinstance(v, dict):
                    _v_fail, _v_data, _v_info = recursive_decrypt(v)
                    if not _fail:
                        _fail = _v_fail

                _info[k], _data[k] = _v_info, _v_data

                if fail_decryption and _fail:
                    # stop recursive processing
                    break

            return _fail, _data, _info

        fail, data, info = recursive_decrypt(vault_data)
        result['failed'] = fail
        result['data'] = data

        if result['failed'] and fail_decryption:
            result['data'] = {}

        result['info'] = info

        return result

from ansible.plugins.action import ActionBase
from ansible.errors import AnsibleActionFail

from ._shared import decrypt_single


class ActionModule(ActionBase):
    def run(self, tmp=None, task_vars=None):
        del tmp, task_vars

        vault_data = self._task.args['vault'] if 'vault' in self._task.args else None
        if vault_data is None:
            raise AnsibleActionFail("You need to provide the 'vault' parameter!")

        return decrypt_single(
            args=self._task.args,
            vault_parser=self._loader._vault,
            vault_data=vault_data,
        )

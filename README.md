# Ansible Vault - Multi Value Functionality

[![Ansible Galaxy](https://img.shields.io/ansible/collection/2356)](https://galaxy.ansible.com/superstes/multi_vault)

This Ansible [Action Plugin](https://docs.ansible.com/ansible/latest/plugins/action.html) enables to use you multi-valued Ansible-Vault entries.

## WHY?

Ansible-Vault has [support to work with multiple passwords](https://docs.ansible.com/ansible/latest/vault_guide/vault_using_encrypted_content.html#passing-multiple-vault-passwords)!

This functionality is very useful whenever you are working:
* with multiple Environments (internal, testing, staging, production, ...)
* in bigger teams
* with multiple automation/execution platforms (CICD like GitLab, [Ansible AWX](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwjV2p7d1tH9AhVmiP0HHdT9BWoQFnoECAoQAQ&url=https%3A%2F%2Fgithub.com%2Fansible%2Fawx&usg=AOvVaw1ngFQJip52iIVPdTKQnN5d), [Ansible Molecule](https://molecule.readthedocs.io/en/latest/))
* ...

But that functionality has a problem:

* You need to add 'switches' between multiple encrypted values on 'user-level' (_in Tasks or Playbooks_).

In my opinion this switch should be done automatically in the background as Ansible has all the needed knowledge about provided passwords and tags.
But for now - [this feature](https://github.com/ansible/ansible/issues/80165) will not be implemented.

That's why I implemented it as a plugin.

### Why an 'Action Plugin'?
Action-Plugins seem to be the only kind of plugins that have access to the [DataLoader](https://github.com/ansible/ansible/blob/devel/lib/ansible/parsing/dataloader.py) that loads the [Ansible-Vault secrets](https://github.com/ansible/ansible/blob/devel/lib/ansible/parsing/vault/__init__.py) at runtime.

Correct me if I'm wrong.. (;

## Installation

Either install it using 'ansible-galaxy'

```bash
ansible-galaxy collection install superstes.multi_vault
```

Or download it from GitHub and copy it to your local 'collections' directory:
```bash
cd $PLAYBOOK_DIR
mkdir -p collections/ansible_collections/superstes/multi_vault/
cd collections/ansible_collections/superstes/multi_vault/
wget https://github.com/superstes/ansible_multi_vault/archive/refs/heads/latest.zip -O /tmp/multi_vault.zip
unzip -j /tmp/multi_vault.zip
```

## Usage

See: [Examples](https://github.com/superstes/ansible_multi_vault/blob/latest/Examples.md)

# Testing

You can test the playbook yourself!

Passwords:
* default = t
* tag1 = t1
* tag2 = t2

# superstes.multi_vault.decrypt_single

## Playbook/Config

```yaml
- hosts: localhost
  gather_facts: no
  become: false

  vars:
    data: "!multi_vault |
      $ANSIBLE_VAULT;1.2;AES256;tag1
      35343930656264383039626437366339336132346465353230653731343664613465396530616531
      6134653530636466643136626466326239353437356338360a383133653731353731363466386139
      30353231636435323965333937636665303033336339363436646661633333343436653161623339
      6261306232366464610a363530343564386565353230653938316636363532653365333061323838
      6632
      $ANSIBLE_VAULT;1.2;AES256;tag2
      39656633626264373966343266383938386433613763333764363763326633386635336130313539
      3966333135616237613666396665353063633038393331310a353563303561393733646663373731
      63343336386336613736636666393531626238313762376132343831613438616666373139656666
      3031353339663963360a656436663732333637313062313061663866643764643132363937363338
      6162
      $ANSIBLE_VAULT;1.1;AES256
      38333361366131363835336533336634633131626263623764363232333336636533326331633530
      6530396633653632646265643731363432613130306331380a363164623832643638316665313036
      37373162363863343366643836336266353365323137363937663633653664646232326138313335
      3231313063646661300a313836303464613636386366316666386639643631633265613665336663
      6266"

  tasks:
    - superstes.multi_vault.decrypt_single:
        vault: "{{ data }}"
        # fail: true  # fail call if any decryption fails
        # first: true  # stop trying to decrypt additional blocks when one was successful (per entry..)
      register: test

    - debug:
        var: test.data
    
```

## Execution

### No secrets provided (same with wrong pwd)
```bash
ansible-playbook example.yml

fatal: [localhost]: FAILED! => {
   "changed":false,
   "data":null,
   "error":"Failed to decrypt vault-data!",
   "info":[
      "Decrypt failed for block 0 with vault-id: 'tag1'",
      "Decrypt failed for block 1 with vault-id: 'tag2'",
      "Decrypt failed for block 2 with vault-id: 'default'"
   ],
   "vault_id":null
}
```

### Ask-vault-pass (default tag)

```bash
ansible-playbook example.yml --ask-vault-pass

ok: [localhost]
ok: [localhost] => {
    "test.data": "test3"
}
```

### Ask-vault-pass - pwd from tag1

```bash
ansible-playbook example.yml --ask-vault-pass

ok: [localhost]
ok: [localhost] => {
    "test.data": "test1"
}
```

### Vault-ID - tag2

```bash
ansible-playbook example.yml --vault-id tag2@prompt

ok: [localhost]
ok: [localhost] => {
    "test.data": "test2"
}
```

# superstes.multi_vault.decrypt_dict

## Playbook/Config

```yaml
- hosts: localhost
  gather_facts: no
  become: false

  vars:
    data:
      server1:
        just_some_var: 'yes'
        a_port: 59503
        another: ['nope', 'hää']
        secret1: "!multi_vault |
          $ANSIBLE_VAULT;1.2;AES256;tag1
          35343930656264383039626437366339336132346465353230653731343664613465396530616531
          6134653530636466643136626466326239353437356338360a383133653731353731363466386139
          30353231636435323965333937636665303033336339363436646661633333343436653161623339
          6261306232366464610a363530343564386565353230653938316636363532653365333061323838
          6632
          $ANSIBLE_VAULT;1.2;AES256;tag2
          39656633626264373966343266383938386433613763333764363763326633386635336130313539
          3966333135616237613666396665353063633038393331310a353563303561393733646663373731
          63343336386336613736636666393531626238313762376132343831613438616666373139656666
          3031353339663963360a656436663732333637313062313061663866643764643132363937363338
          6162
          $ANSIBLE_VAULT;1.1;AES256
          38333361366131363835336533336634633131626263623764363232333336636533326331633530
          6530396633653632646265643731363432613130306331380a363164623832643638316665313036
          37373162363863343366643836336266353365323137363937663633653664646232326138313335
          3231313063646661300a313836303464613636386366316666386639643631633265613665336663
          6266"
      server2:
        h:
          u:
            i:
              d:
                - "!multi_vault |
                  $ANSIBLE_VAULT;1.2;AES256;tag1
                  35343930656264383039626437366339336132346465353230653731343664613465396530616531
                  6134653530636466643136626466326239353437356338360a383133653731353731363466386139
                  30353231636435323965333937636665303033336339363436646661633333343436653161623339
                  6261306232366464610a363530343564386565353230653938316636363532653365333061323838
                  6632
                  $ANSIBLE_VAULT;1.2;AES256;tag2
                  39656633626264373966343266383938386433613763333764363763326633386635336130313539
                  3966333135616237613666396665353063633038393331310a353563303561393733646663373731
                  63343336386336613736636666393531626238313762376132343831613438616666373139656666
                  3031353339663963360a656436663732333637313062313061663866643764643132363937363338
                  6162
                  $ANSIBLE_VAULT;1.1;AES256
                  38333361366131363835336533336634633131626263623764363232333336636533326331633530
                  6530396633653632646265643731363432613130306331380a363164623832643638316665313036
                  37373162363863343366643836336266353365323137363937663633653664646232326138313335
                  3231313063646661300a313836303464613636386366316666386639643631633265613665336663
                  6266"
                - "!multi_vault |
                  $ANSIBLE_VAULT;1.2;AES256;tag1
                  35343930656264383039626437366339336132346465353230653731343664613465396530616531
                  6134653530636466643136626466326239353437356338360a383133653731353731363466386139
                  30353231636435323965333937636665303033336339363436646661633333343436653161623339
                  6261306232366464610a363530343564386565353230653938316636363532653365333061323838
                  6632"
      mv: "!multi_vault |
        $ANSIBLE_VAULT;1.2;AES256;tag1
        35343930656264383039626437366339336132346465353230653731343664613465396530616531
        6134653530636466643136626466326239353437356338360a383133653731353731363466386139
        30353231636435323965333937636665303033336339363436646661633333343436653161623339
        6261306232366464610a363530343564386565353230653938316636363532653365333061323838
        6632
        $ANSIBLE_VAULT;1.2;AES256;tag2
        39656633626264373966343266383938386433613763333764363763326633386635336130313539
        3966333135616237613666396665353063633038393331310a353563303561393733646663373731
        63343336386336613736636666393531626238313762376132343831613438616666373139656666
        3031353339663963360a656436663732333637313062313061663866643764643132363937363338
        6162
        $ANSIBLE_VAULT;1.1;AES256
        38333361366131363835336533336634633131626263623764363232333336636533326331633530
        6530396633653632646265643731363432613130306331380a363164623832643638316665313036
        37373162363863343366643836336266353365323137363937663633653664646232326138313335
        3231313063646661300a313836303464613636386366316666386639643631633265613665336663
        6266"


  tasks:
    - superstes.multi_vault.decrypt_dict:
        vault: "{{ data }}"
        # fail: true  # fail call if any decryption fails
        # first: true  # stop trying to decrypt additional blocks when one was successful (per entry..)
      register: test

    - debug:
        var: test.data
```

## Execution

### No secrets provided
```bash
ansible-playbook example.yml
fatal: [localhost]: FAILED! => {
   "changed":false,
   "data":{},
   "error":"Failed to decrypt vault-data!",
   "info":{
      "server1":{
         "a_port":null,
         "another":[
            [],
            []
         ],
         "just_some_var":[],
         "secret1":[
            "Decrypt failed for block 0 with vault-id: 'tag1'",
            "Decrypt failed for block 1 with vault-id: 'tag2'",
            "Decrypt failed for block 2 with vault-id: 'default'"
         ]
      }
   },
   "vault_id":null
}
```

### Ask-vault-pass (default tag)

Fails because entry 'data.server2.h.u.i.d[1]' has an entry that cannot be decrypted.

```bash
ansible-playbook example.yml --ask-vault-pass

fatal: [localhost]: FAILED! => {
   "changed": false,
   "data":{},
   "error":"Failed to decrypt vault-data!",
   "info":{
      "server1":{
         "a_port":null,
         "another":[
            [],
            []
         ],
         "just_some_var":[],
         "secret1":[
            "Decrypt failed for block 0 with vault-id: 'tag1'",
            "Decrypt failed for block 1 with vault-id: 'tag2'",
            "Decrypt successful for block 2 with vault-id: 'default'"
         ]
      },
      "server2":{
         "h":{
            "u":{
               "i":{
                  "d":[
                     [
                        "Decrypt failed for block 0 with vault-id: 'tag1'",
                        "Decrypt failed for block 1 with vault-id: 'tag2'",
                        "Decrypt successful for block 2 with vault-id: 'default'"
                     ],
                     [
                        "Decrypt failed for block 0 with vault-id: 'tag1'"
                     ]
                  ]
               }
            }
         }
      }
   },
   "vault_id":null
}
```

### Ask-vault-pass (default tag) - fail=false

Now - we are setting the 'fail' mode to 'false'

```yaml
  tasks:
    - superstes.multi_vault.decrypt_dict:
        vault: "{{ data }}"
        fail: false  # fail call if any decryption fails
        # first: true  # stop trying to decrypt additional blocks when one was successful (per entry..)
      register: test
```

```bash
ansible-playbook example.yml --ask-vault-pass
ok: [localhost]
ok: [localhost] => {
    "test.data": {
        "mv": "test3",
        "server1": {
            "a_port": 59503,
            "another": [
                "nope",
                "hää"
            ],
            "just_some_var": "yes",
            "secret1": "test3"
        },
        "server2": {
            "h": {
                "u": {
                    "i": {
                        "d": [
                            "test3",
                            "!multi_vault | $ANSIBLE_VAULT;1.2;AES256;tag1 35343930656264383039626437366339336132346465353230653731343664613465396530616531 6134653530636466643136626466326239353437356338360a383133653731353731363466386139 30353231636435323965333937636665303033336339363436646661633333343436653161623339 6261306232366464610a363530343564386565353230653938316636363532653365333061323838 6632"
                        ]
                    }
                }
            }
        }
    }
}

```

### Ask-vault-pass - pwd from tag1

```bash
ansible-playbook example.yml --ask-vault-pass

ok: [localhost]
ok: [localhost] => {
    "test.data": {
        "mv": "test1",
        "server1": {
            "a_port": 59503,
            "another": [
                "nope",
                "hää"
            ],
            "just_some_var": "yes",
            "secret1": "test1"
        },
        "server2": {
            "h": {
                "u": {
                    "i": {
                        "d": [
                            "test1",
                            "test1"
                        ]
                    }
                }
            }
        }
    }
}
```

### Vault-ID - wrong pwd
Entering wrong password.
'fail' is set to 'true' again

```bash
ansible-playbook example.yml --vault-id tag1@prompt

fatal: [localhost]: FAILED! => {
   "changed":false,
   "data":{},
   "error":"Failed to decrypt vault-data!",
   "info":{
      "server1":{
         "a_port":null,
         "another":[
            [],
            []
         ],
         "just_some_var":[],
         "secret1":[
            "Decrypt failed for block 0 with vault-id: 'tag1'",
            "Decrypt failed for block 1 with vault-id: 'tag2'",
            "Decrypt failed for block 2 with vault-id: 'default'"
         ]
      }
   },
   "vault_id":null
}
```

### Vault-ID (tag1)

```bash
ansible-playbook example.yml --vault-id tag1@prompt

ok: [localhost]
ok: [localhost] => {
    "test.data": {
        "mv": "test1",
        "server1": {
            "a_port": 59503,
            "another": [
                "nope",
                "hää"
            ],
            "just_some_var": "yes",
            "secret1": "test1"
        },
        "server2": {
            "h": {
                "u": {
                    "i": {
                        "d": [
                            "test1",
                            "test1"
                        ]
                    }
                }
            }
        }
    }
}
```

### Vault-ID (tag2)

Fails because entry 'data.server2.h.u.i.d[1]' has an entry that cannot be decrypted.

```bash
ansible-playbook example.yml --vault-id tag1@prompt

fatal: [localhost]: FAILED! => {
   "changed":false,
   "data":{},
   "error":"Failed to decrypt vault-data!",
   "info":{
      "server1":{
         "a_port":null,
         "another":[
            [],
            []
         ],
         "just_some_var":[],
         "secret1":[
            "Decrypt failed for block 0 with vault-id: 'tag1'",
            "Decrypt successful for block 1 with vault-id: 'tag2'"
         ]
      },
      "server2":{
         "h":{
            "u":{
               "i":{
                  "d":[
                     [
                        "Decrypt failed for block 0 with vault-id: 'tag1'",
                        "Decrypt successful for block 1 with vault-id: 'tag2'"
                     ],
                     [
                        "Decrypt failed for block 0 with vault-id: 'tag1'"
                     ]
                  ]
               }
            }
         }
      }
   },
   "vault_id":null
}
```

### Vault-ID (tag2) - fail=false

```bash
ansible-playbook example.yml --vault-id tag1@prompt

ok: [localhost]
ok: [localhost] => {
    "test.data": {
        "mv": "test2",
        "server1": {
            "a_port": 59503,
            "another": [
                "nope",
                "hää"
            ],
            "just_some_var": "yes",
            "secret1": "test2"
        },
        "server2": {
            "h": {
                "u": {
                    "i": {
                        "d": [
                            "test2",
                            "!multi_vault | $ANSIBLE_VAULT;1.2;AES256;tag1 35343930656264383039626437366339336132346465353230653731343664613465396530616531 6134653530636466643136626466326239353437356338360a383133653731353731363466386139 30353231636435323965333937636665303033336339363436646661633333343436653161623339 6261306232366464610a363530343564386565353230653938316636363532653365333061323838 6632"
                        ]
                    }
                }
            }
        }
    }
}
```

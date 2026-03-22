# Utilitários Python

Esse repositório tem 3 scripts pequenos e práticos que eu fiz para treinar um pouco de python e entender uma hash.

---

## O que tem aqui

### Hash Calculator
Calcula o hash SHA-256 de todos os arquivos de uma pasta.

lê arquivos em blocos de 8KB, então não trava nem com arquivos de 10GB. Não tem o bug comum de carregar o arquivo inteiro na memória.

Uso:
```bash
# Calcula hash da pasta atual
python HashCalculator.py .

# Calcula hash de qualquer outra pasta
python HashCalculator.py /home/usuario/Downloads
```

Pode usar para verificar se um download não veio corrompido ou adulterado. Olhando se o tamanho compilado é maior ou menor do que o descrito.


---

### System Health Check
Mostra o status real do sistema: CPU, RAM, disco, uptime e tempo de boot.

Ignora automaticamente partições snap e tmpfs que ninguém quer ver.

Uso:
```bash
python System_Check.py
```


---

### Log Parser
Ferramenta para filtrar e procurar em arquivos de log.

---

## Como rodar

```bash

# Depois é só rodar qualquer um dos scripts
python HashCalculator.py .
python System_Check.py
```


---

## Observações

- Todos os scripts foram feitos e testados no Linux. Devem funcionar no Mac também, provavelmente não funcionam no Windows.

---

## Dependencias

Apenas uma, padrão da industria:
```
psutil == 6.1.1
```

Se você não quiser usar o venv incluso, é só instalar ela manualmente com `pip install psutil`.

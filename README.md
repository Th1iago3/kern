<div align="center">
  <img src="https://img.shields.io/badge/CS2-External%20Memory%20Dumper-2ea44f?style=for-the-badge&logo=python&logoColor=white" alt="CS2 Dumper"/>
  <img src="https://img.shields.io/badge/Windows-10%20%7C%2011-critical?style=for-the-badge" alt="Windows Only"/>
  <img src="https://img.shields.io/github/license/Th1iago3/kern?style=for-the-badge" alt="License"/>
  <img src="https://img.shields.io/github/stars/Th1iago3/kern?style=for-the-badge" alt="Stars"/>
  <img src="https://img.shields.io/github/last-commit/Th1iago3/kern?style=for-the-badge" alt="Last Commit"/>
</div>

# kern.py — CS2 External Memory Dumper

Autor original: [@5n6xc1](https://instagram.com/5n6xc1)

Este script faz leitura externa da memória do processo `cs2.exe` (sem injeção).  
Ele baixa automaticamente os offsets e schemas mais recentes, percorre a entity list atual do CS2 (GameEntitySystem) e gera um dump organizado em pasta com todos os arquivos JSON, .cs e .cpp baixados.

Exemplo de saída no console:

```
highest entity index: 2048
local player pawn:    0x140012345678
entity list:          0x1800ABCDEF00
viewmatrix:           [1.234, 0.0, ...]
entity 5:
  index: 5
  controller: 0x1a2b3c...
  pawn: 0x5d6e7f8...
  health: 92
  team: 3
  origin: [1245.67, -890.12, 72.0]
  name: proplayerBR
  active weapon: 0x...
  armor: 100
...
SUCCESS
dump_20260228_0211_xyz789
```

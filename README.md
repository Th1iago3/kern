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
Ele baixa automaticamente os offsets e schemas mais recentes do repositório [a2x/cs2-dumper](https://github.com/a2x/cs2-dumper), percorre a entity list atual do CS2 (GameEntitySystem) e gera um dump organizado em pasta com todos os arquivos JSON, .cs e .cpp baixados.

### O que o script faz em sequência

1. Verifica se está rodando como administrador (pede elevação se necessário)
2. Abre o processo `cs2.exe`
3. Baixa os offsets e schemas (~30 arquivos)
4. Lê os principais ponteiros (entity list, local player, viewmatrix, highest entity index)
5. Itera pela lista de entidades e coleta informações dos jogadores
6. Mostra no console um resumo dos players vivos
7. Cria uma pasta com nome `dump_YYYYMMDD_HHMM_abcdef` e salva tudo lá

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

### Principais offsets e campos usados (valores aproximados — mudam por update)

| Campo                                 | Offset exemplo     | Classe / Estrutura            | Observação                                  |
|---------------------------------------|--------------------|-------------------------------|---------------------------------------------|
| dwEntityList                          | ~0x1E7A000        | client.dll                    | Ponteiro base da entity list                |
| dwLocalPlayerPawn                     | ~0x1AF1234        | client.dll                    | Nosso C_CSPlayerPawn                        |
| dwGameEntitySystem_highestEntityIndex | 0x1580            | client.dll → classes          | Limite seguro para iteração                 |
| m_hPlayerPawn                         | 0x90C / 0x6B4     | CCSPlayerController           | Handle do pawn do jogador                   |
| m_sSanitizedPlayerName                | 0x860 / 0x778     | CCSPlayerController           | Nome limpo (sem clã/tag)                    |
| m_iHealth                             | 0x354             | C_BaseEntity / C_CSPlayerPawn | Vida (1–100)                                |
| m_iTeamNum                            | 0x3F3             | C_BaseEntity                  | 2 = T, 3 = CT                               |
| m_vecAbsOrigin                        | 0xD0 (via m_pGameSceneNode) | CGameSceneNode         | Posição XYZ                                 |
| m_hActiveWeapon                       | 0x60 (via m_pWeaponServices) | C_BasePlayerPawn      | Handle da arma atual                        |
| m_ArmorValue                          | 0x272C            | C_CSPlayerPawn                | Armadura (0–100)                            |

Os offsets são baixados dinamicamente, então o script acompanha os updates do jogo.

### Requisitos

- Windows 10 ou 11 (64-bit)
- Python 3.9 a 3.12
- CS2 aberto (pode estar na tela de loading)
- Executar como administrador (obrigatório)

### Instalação e uso

```bash
git clone https://github.com/Th1iago3/kern
cd kern

pip install pymem requests colorama
```

Depois é só rodar como administrador:

```bash
python3 kern.py
# ou
py -3 kern.py
```

### Contribuição

Se quiser ajudar:

1. Faça fork do repositório
2. Crie uma branch (`git checkout -b feature/alguma-coisa`)
3. Commit suas alterações (`git commit -m 'feat: adiciona X'`)
4. Push (`git push origin feature/alguma-coisa`)
5. Abra um Pull Request
```

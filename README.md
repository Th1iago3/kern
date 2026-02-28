<div align="center">

  <img src="https://img.shields.io/badge/CS2-External%20Memory%20Dumper-2ea44f?style=for-the-badge&logo=python&logoColor=white" alt="CS2 Dumper"/>
  <img src="https://img.shields.io/badge/Windows-10%20%7C%2011-critical?style=for-the-badge" alt="Windows Only"/>
  <img src="https://img.shields.io/github/license/Th1iago3/kern?style=for-the-badge" alt="License"/>
  <img src="https://img.shields.io/github/stars/Th1iago3/kern?style=for-the-badge" alt="Stars"/>
  <img src="https://img.shields.io/github/last-commit/Th1iago3/kern?style=for-the-badge" alt="Last Commit"/>

  <h1>🛡️ kern.py — CS2 Memory Dumper</h1>

  <p>
    <strong>Autor original:</strong> <a href="https://instagram.com/5n6xc1">@5n6xc1</a><br/>
  </p>

</div>

<br/>

## 1. Visão Geral

**kern.py** é uma ferramenta **externa** (external memory reading) que:

- Abre o processo `cs2.exe` com privilégios elevados
- Baixa automaticamente offsets e schemas mais recentes do [a2x/cs2-dumper](https://github.com/a2x/cs2-dumper)
- Itera pela entity list moderna do CS2 (GameEntitySystem)
- Extrai dados reais de jogadores vivos (exclui local player)
- Gera dump organizado em pasta 
- Salva os ~30 arquivos JSON/CS/CPP do dumper

<br/>

## 2. Exemplo de Saída (Console)

```
highest: 2048
lp: 0x140012345678
el: 0x1800ABCDEF00
viewmatrix: [1.234, 0.0, ..., 1.0]
entity 5: {'index': 5, 'controller': '0x1a2b3c...', 'pawn': '0x5d6e7f8...', 'health': 92, 'team': 3, 'origin': [1245.67, -890.12, 72.0], 'name': 'proplayerBR', 'active_weapon': '0x...', 'armor': 100}
...
[ + ]: SUCCESS !!
dump_20260228_0211_xyz789
```

Pasta gerada:
```
dump_20260228_0211_xyz789/
├── local_dump.json          ← resumo + viewmatrix + entidades
├── client_dll.json
├── offsets.json
├── animationsystem_dll.json
└── ... (~30 arquivos)
```

<br/>

## 3. Offsets & Estruturas Principais (2025–2026)

| Campo / Offset                        | Valor Exemplo (pode variar) | Classe Principal              | Descrição Principal                          |
|---------------------------------------|-----------------------------|-------------------------------|----------------------------------------------|
| `dwEntityList`                        | ~0x1E7A000                 | client.dll                    | Ponteiro base da Entity List                 |
| `dwLocalPlayerPawn`                   | ~0x1AF1234                 | client.dll                    | Nosso Pawn (C_CSPlayerPawn)                  |
| `dwGameEntitySystem_highestEntityIndex`| 0x1580                    | client.dll → classes          | Índice máximo para loop seguro               |
| `m_hPlayerPawn`                       | 0x90C / 0x6B4              | CCSPlayerController           | Handle do Pawn associado ao controller       |
| `m_sSanitizedPlayerName`              | 0x860 / 0x778              | CCSPlayerController           | Nome limpo (sem tags/clãs)                   |
| `m_iHealth`                           | 0x354                      | C_BaseEntity / C_CSPlayerPawn | Vida (1–100)                                 |
| `m_iTeamNum`                          | 0x3F3                      | C_BaseEntity                  | Time: 2=Terrorista, 3=Contra-Terrorista     |
| `m_pGameSceneNode → m_vecAbsOrigin`   | 0x338 → 0xD0               | C_BaseEntity → CGameSceneNode | Posição absoluta XYZ (float[3])              |
| `m_pWeaponServices → m_hActiveWeapon` | 0x13D8 → 0x60              | C_BasePlayerPawn              | Handle da arma equipada                      |
| `m_ArmorValue`                        | 0x272C                     | C_CSPlayerPawn                | Valor da armadura (0–100)                    |

> **Importante:** Offsets são baixados dinamicamente → o script se adapta a updates do jogo.

<br/>

## 4. Instalação Rápida

### Requisitos

- **SO:** Windows 10 x64 ou Windows 11 x64
- **Python:** 3.9, 3.10, 3.11 ou 3.12
- **CS2:** aberto e em execução (pode estar na tela de loading)
- **Permissões:** Executar como Administrador (obrigatório)

```bash
# 1. Clone o repositório
git clone https://github.com/Th1iago3/kern
cd kern

# 2. Instale dependências
pip install pymem requests colorama
```

<br/>

### Execução

```bash
# Rode SEMPRE como Administrador
python3 kern.py
# ou
py -3 kern.py
```

O que acontece:
1. Pede elevação UAC (se não estiver admin)
2. Abre cs2.exe
3. Baixa offsets + schemas (~30 arquivos)
4. Processa entity list
5. Mostra jogadores no console
6. Cria pasta `dump_YYYYMMDD_HHMM_random`
7. Salva tudo → sucesso!

<br/>

<br/>

## 5. Contribuição

Contribuições são super bem-vindas!

1. Fork o repositório
2. Crie branch (`git checkout -b feature/nova-coisa`)
3. Commit suas mudanças (`git commit -m 'feat: adiciona X'`)
4. Push (`git push origin feature/nova-coisa`)
5. Abra um **Pull Request**

Por favor, siga o estilo de código existente e adicione comentários em PT-BR.

<br/>

## 6. Segurança & Ética

- **Não** use em contas principais
- **Não** distribua binários compilados
- **Não** publique offsets fixos (sempre dinâmico)
- Teste apenas offline ou em servidores privados

<br/>

## 7. Versões em Outros Idiomas

### Français

**kern.py** — Outil externe de dump mémoire pour CS2 (Windows only).  
Télécharge offsets récents, lit l'entity list, extrait joueurs vivants et sauvegarde dump complet.

### Español

**kern.py** — Herramienta externa de dump de memoria para CS2 (solo Windows).  
Descarga offsets actualizados, lee lista de entidades, extrae jugadores vivos y guarda dump completo.

<br/>

<div align="center">
  <br/>
  <b>Feito com ☕ • 2026</b><br/>
</div>
```

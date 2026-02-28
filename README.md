<div align="center">

  <img src="https://img.shields.io/badge/CS2-Kernel%20Level%20Reader-informational?style=for-the-badge&logo=python&logoColor=white&color=2ea44f" alt="CS2 Reader"/>
  <img src="https://img.shields.io/badge/Status-Proof%20of%20Concept-critical?style=for-the-badge&logo=python" alt="POC"/>
  <img src="https://img.shields.io/github/license/Aleatoriam3695/cript-kern.py?style=for-the-badge" alt="License"/>
  <br/><br/>
  
  <h1>🛠️ cript-kern.py</h1>
  <p>
    <strong>Ferramenta externa de leitura de memória avançada para Counter-Strike 2</strong><br/>
    Dump de entidades, offsets atualizados via cs2-dumper, extração de players vivos, nomes, vida, time, posição, arma ativa e armadura.
  </p>

  <p>
    <strong>Feito por:</strong> <a href="https://x.com/5n6xc1">@5n6xc1</a> • Modificado & Documentado por <a href="https://x.com/Aleatoriam3695">@Aleatoriam3695</a>
  </p>

</div>

<br/>

## 🔥 Visão Geral

Esta ferramenta **lê diretamente a memória do processo cs2.exe** (externamente) utilizando `pymem` + `ctypes` + `kernel32.dll` e faz o seguinte:

- Eleva privilégios automaticamente (UAC prompt)
- Baixa offsets **frescos** do repositório oficial [a2x/cs2-dumper](https://github.com/a2x/cs2-dumper)
- Localiza o `LocalPlayerPawn`, `EntityList`, `ViewMatrix`
- Itera pela **entity list** moderna do CS2 (formato CS2 pós-2023)
- Extrai informações úteis de jogadores vivos
- Salva **dump completo** (JSON + todos arquivos do dumper) em pasta com timestamp + ID aleatório

**Objetivo principal:** servir como base sólida para desenvolvimento de ferramentas externas / analisadores / treinamentos / pesquisa em memory reading no CS2.

> ⚠️ **Aviso Legal Importante**  
> Este código é para **estudo, pesquisa e aprendizado**.  
> O uso em servidores online viola os termos de serviço da Valve e pode resultar em banimento permanente.  
> Use **apenas em ambiente offline/local** ou em servidores privados com permissão explícita.

<br/>

## ✨ Funcionalidades

- [x] Elevação automática de privilégios (Run as Administrator)
- [x] Download automático de offsets mais recentes
- [x] Leitura externa sem injeção (100% external)
- [x] Suporte à entity list particionada do CS2
- [x] Extração de: nome, vida, time, posição 3D, arma ativa, armadura
- [x] Dump completo da pasta output do cs2-dumper (~30 arquivos)
- [x] Cores no terminal via `colorama`
- [x] Tratamento básico de erros e robustez

<br/>

## 📊 Exemplo de Saída no Console

```
highest: 2048
lp: 0x14000000000
el: 0x18000000000
viewmatrix: [1.0, 0.0, ..., 1.0]
entity 3: {'index': 3, 'controller': '0x1a2b3c4...', 'pawn': '0x5d6e7f...', 'health': 87, 'team': 3, 'origin': [1500.2, -340.1, 64.0], 'name': 'PlayerX', 'active_weapon': '0x...', 'armor': 45}
...
[ + ]: SUCCESS !!
dump_20260228_0211_abc123
```

<br/>

## 🛠️ Como Funciona (Fluxo Técnico)

1. Verifica privilégios → pede elevação se necessário  
2. Abre handle do processo `cs2.exe` com `PROCESS_ALL_ACCESS`  
3. Baixa `offsets.json` e `client_dll.json` do GitHub  
4. Localiza bases dos módulos (`client.dll`, etc.)  
5. Calcula endereços absolutos importantes:
   - `dwLocalPlayerPawn`
   - `dwEntityList`
   - `dwViewMatrix`
6. Lê `highestEntityIndex` (limite superior da entity list)
7. Itera índices → resolve **controller → pawn → dados** usando chain de offsets:
   ```
   EntityList → Entry → Identity → Controller → m_hPlayerPawn → Pawn
                                     ↓
                                 m_iHealth / m_iTeamNum / m_vecAbsOrigin / m_sSanitizedPlayerName / ...
   ```
8. Filtra entidades válidas (health 1–100, != localplayer)
9. Salva tudo em pasta timestampada + JSON local + todos arquivos do dumper

<br/>

## ⚙️ Offsets Mais Importantes Usados (2025–2026)

| Offset / Campo                        | Valor típico (exemplo) | Classe / Origem               | Uso principal                     |
|---------------------------------------|------------------------|-------------------------------|-----------------------------------|
| `dwEntityList`                        | ~0x1E00000            | client.dll                    | Lista principal de entidades      |
| `dwLocalPlayerPawn`                   | ~0x1AF0000            | client.dll                    | Nosso jogador (Pawn)              |
| `dwGameEntitySystem_highestEntityIndex` | 0x1580              | client.dll → classes          | Limite superior da iteração       |
| `m_hPlayerPawn`                       | 0x90C / 0x6B4         | CCSPlayerController           | Handle do Pawn do jogador         |
| `m_sSanitizedPlayerName`              | 0x860 / 0x778         | CCSPlayerController           | Nome limpo do jogador             |
| `m_iHealth`                           | 0x354 / 0x34C         | C_BaseEntity / C_CSPlayerPawn | Vida (1–100)                      |
| `m_iTeamNum`                          | 0x3F3 / 0x3EB         | C_BaseEntity                  | Time (2 = T, 3 = CT)              |
| `m_pGameSceneNode → m_vecAbsOrigin`   | 0x338 → 0xD0          | C_BaseEntity → CGameSceneNode | Posição XYZ no mundo              |
| `m_pWeaponServices → m_hActiveWeapon` | 0x13D8 → 0x60         | C_BasePlayerPawn              | Handle da arma atual              |
| `m_ArmorValue`                        | 0x272C                | C_CSPlayerPawn                | Valor da armadura                 |

> **Nota:** valores mudam a cada atualização do jogo → por isso baixamos do cs2-dumper automaticamente!

<br/>

## 🚀 Instalação e Uso

### Requisitos

- Windows 10/11 (64-bit)
- Python 3.9+
- CS2 aberto (jogo em execução)

```bash
# 1. Clone o repositório
git clone https://github.com/SEU_USUARIO/cript-kern.py.git
cd cript-kern.py

# 2. Instale dependências
pip install pymem requests colorama
```

### Execução

```bash
# Rode como administrador (obrigatório)
python cript-kern.py
# ou
py -3 cript-kern.py
```

A ferramenta vai:
- Pedir elevação (UAC)
- Baixar ~30 arquivos do cs2-dumper
- Criar pasta `dump_YYYYMMDD_HHMM_abcdef`
- Mostrar jogadores encontrados no console
- Gerar `local_dump.json` com tudo resumido

<br/>

## 🛡️ Limitações & Cuidados

- **Anti-cheat (VAC)**: leitura externa ainda é detectável em alguns casos (kernel drivers, comportamento suspeito, etc.)
- **Atualizações do CS2**: offsets mudam → o script tenta se atualizar sozinho, mas pode quebrar temporariamente
- **Performance**: itera até ~8000 entidades → pode ser lento em máquinas antigas
- **Estabilidade**: CS2 altera estruturas com frequência → teste sempre após patch

<br/>

## 🌍 Versões em Outros Idiomas

### Français

**cript-kern.py** — Outil externe de lecture mémoire pour Counter-Strike 2  
Récupère automatiquement les offsets les plus récents, lit la liste d'entités, extrait les joueurs vivants (nom, vie, équipe, position, arme, armure) et sauvegarde un dump complet.

### Español

**cript-kern.py** — Herramienta externa de lectura de memoria para Counter-Strike 2  
Descarga offsets actualizados, lee la lista de entidades, extrae jugadores vivos (nombre, vida, equipo, posición, arma activa, armadura) y guarda un dump completo.

<br/>

<div align="center">

  <br/>
  <b>Feito com 🖤 e muito café • 2026</b><br/>
  <sub>Qualquer dúvida → abre issue ou me chama no X → @Aleatoriam3695</sub>

</div>
```

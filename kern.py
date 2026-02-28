import sys,os,ctypes,pymem,requests,json,time,random,string,struct
from ctypes import wintypes
import time
import colorama
from colorama import Fore
def clear():
 os.system('cls' if os.name=='nt' else 'clear')
if not ctypes.windll.shell32.IsUserAnAdmin():
 ctypes.windll.shell32.ShellExecuteW(None,"runas",sys.executable," ".join([f'"{a}"'for a in sys.argv]),None,1)
 sys.exit(0)
kernel32=ctypes.WinDLL('kernel32',use_last_error=True)
OpenProcess=kernel32.OpenProcess
OpenProcess.argtypes=[wintypes.DWORD,wintypes.BOOL,wintypes.DWORD]
OpenProcess.restype=wintypes.HANDLE
ReadProcessMemory=kernel32.ReadProcessMemory
ReadProcessMemory.argtypes=[wintypes.HANDLE,wintypes.LPCVOID,wintypes.LPVOID,ctypes.c_size_t,ctypes.POINTER(ctypes.c_size_t)]
ReadProcessMemory.restype=wintypes.BOOL
PROCESS_ALL_ACCESS=0x1F0FFF
def g(u,i):
 try:r=requests.get(u,timeout=10);r.raise_for_status();return r.json()if i else r.text
 except Exception as e:print(f"Erro ao baixar {u}: {e}");return None
def h(p,a,s=8):
 b=ctypes.create_string_buffer(s)
 if not ReadProcessMemory(p,a,b,s,None):return 0
 if s in(1,2,4,8):return int.from_bytes(b.raw,'little')
 elif s==12:return [int.from_bytes(b.raw[i:i+4],'little')for i in range(0,12,4)]
 else:return b.raw.decode(errors='ignore').rstrip('\x00')
def j(p,el,lp,cl_base,cl,co):
 t=[]
 ges=cl_base+cl["dwGameEntitySystem"]
 hei=cl["dwGameEntitySystem_highestEntityIndex"]
 highest=h(p,ges+hei,4)
 if highest<1 or highest>0x8000:highest=2048
 print(f"highest:{highest}")
 classes=co.get("client.dll",{}).get("classes",{})
 ph_off=classes.get("CCSPlayerController",{}).get("fields",{}).get("m_hPlayerPawn",0x90C)
 name_off=classes.get("CCSPlayerController",{}).get("fields",{}).get("m_sSanitizedPlayerName",0x860)
 health_off=classes.get("C_BaseEntity",{}).get("fields",{}).get("m_iHealth",0x354)
 team_off=classes.get("C_BaseEntity",{}).get("fields",{}).get("m_iTeamNum",0x3F3)
 gs_off=classes.get("C_BaseEntity",{}).get("fields",{}).get("m_pGameSceneNode",0x338)
 origin_off=classes.get("CGameSceneNode",{}).get("fields",{}).get("m_vecAbsOrigin",0xD0)
 weapon_off=classes.get("C_BasePlayerPawn",{}).get("fields",{}).get("m_pWeaponServices",0x13D8)
 active_weapon_off=classes.get("CPlayer_WeaponServices",{}).get("fields",{}).get("m_hActiveWeapon",0x60)
 armor_off=classes.get("C_CSPlayerPawn",{}).get("fields",{}).get("m_ArmorValue",0x272C)
 for idx in range(1,highest+1):
  try:
   le=h(p,el+0x8*((idx&0x7FFF)>>9)+0x10,8)
   if not le:continue
   c=h(p,le+0x78*(idx&0x1FF),8)
   if not c:continue
   ph=h(p,c+ph_off,4)&0x1FFF
   if ph==0:continue
   pe=h(p,el+0x8*((ph&0x7FFF)>>9)+0x10,8)
   if not pe:continue
   pawn=h(p,pe+0x78*(ph&0x1FF),8)
   if not pawn or pawn==lp:continue
   health=h(p,pawn+health_off,4)
   if health<1 or health>100:continue
   team=h(p,pawn+team_off,4)
   gs=h(p,pawn+gs_off,8)
   origin_list=h(p,gs+origin_off,12)if gs else [0,0,0]
   origin=[struct.unpack('f', (o & 0xFFFFFFFF).to_bytes(4,'little'))[0] for o in origin_list]
   name_ptr=h(p,c+name_off,8)
   name=h(p,name_ptr,128)if name_ptr else ""
   weapon_services=h(p,pawn+weapon_off,8)
   weapon=h(p,weapon_services+active_weapon_off,4)if weapon_services else 0
   armor=h(p,pawn+armor_off,4)
   ent={'index':idx,'controller':hex(c),'pawn':hex(pawn),'health':health,'team':team,'origin':origin,'name':name,'active_weapon':hex(weapon),'armor':armor}
   t.append(ent)
   print(f"entity {idx}: {ent}")
  except Exception as e:pass
 return t
def main():
 clear()
 time.sleep(0.5)
 print("#   FEITO POR: @5n6xc1       #")
 try:k()
 except Exception as e:print(f"Erro: {e}")
 finally:input()
def k():
 try:pm=pymem.Pymem("cs2.exe")
 except:print("CS2 nao encontrado");return
 pid=pm.process_id
 h_process=OpenProcess(PROCESS_ALL_ACCESS,False,pid)
 if not h_process:print("Falha ao abrir processo");return
 base_url="https://raw.githubusercontent.com/a2x/cs2-dumper/main/output/"
 files=["animationsystem_dll.cs","animationsystem_dll.hpp","animationsystem_dll.json","animationsystem_dll.rs","buttons.cs","buttons.hpp","buttons.json","buttons.rs","client_dll.cs","client_dll.hpp","client_dll.json","client_dll.rs","engine2_dll.cs","engine2_dll.hpp","engine2_dll.json","engine2_dll.rs","host_dll.cs","host_dll.hpp","host_dll.json","host_dll.rs","info.json","interfaces.cs","interfaces.hpp","interfaces.json","interfaces.rs","materialsystem2_dll.cs","materialsystem2_dll.hpp","materialsystem2_dll.json","materialsystem2_dll.rs","meshsystem_dll.cs","meshsystem_dll.hpp","meshsystem_dll.json","meshsystem_dll.rs","networksystem_dll.cs","networksystem_dll.hpp","networksystem_dll.json","networksystem_dll.rs","offsets.cs","offsets.hpp","offsets.json","offsets.rs","panorama_dll.cs","panorama_dll.hpp","panorama_dll.json","panorama_dll.rs","particles_dll.cs","particles_dll.hpp","particles_dll.json","particles_dll.rs","pulse_system_dll.cs","pulse_system_dll.hpp","pulse_system_dll.json","pulse_system_dll.rs","rendersystemdx11_dll.cs","rendersystemdx11_dll.hpp","rendersystemdx11_dll.json","rendersystemdx11_dll.rs","scenesystem_dll.cs","scenesystem_dll.hpp","scenesystem_dll.json","scenesystem_dll.rs","schemasystem_dll.cs","schemasystem_dll.hpp","schemasystem_dll.json","schemasystem_dll.rs","server_dll.cs","server_dll.hpp","server_dll.json","server_dll.rs","soundsystem_dll.cs","soundsystem_dll.hpp","soundsystem_dll.json","soundsystem_dll.rs","steamaudio_dll.cs","steamaudio_dll.hpp","steamaudio_dll.json","steamaudio_dll.rs","vphysics2_dll.cs","vphysics2_dll.hpp","vphysics2_dll.json","vphysics2_dll.rs","worldrenderer_dll.cs","worldrenderer_dll.hpp","worldrenderer_dll.json","worldrenderer_dll.rs"]
 offs=g(base_url+"offsets.json",True)
 if offs is None:return
 co=g(base_url+"client_dll.json",True)
 if co is None:return
 d={}
 for mod in offs:
  if mod.endswith(".dll"):
   try:
    base=pymem.process.module_from_name(pm.process_handle,mod).lpBaseOfDll
    d[mod+"_base"]=hex(base)
    print(mod+"_base:",hex(base))
    for n,v in offs[mod].items():
     a=base+v
     d[mod+"_"+n]=hex(a)
     print(f"{mod}_{n}: {hex(a)}")
   except:print(f"Modulo {mod} nao encontrado")
 cl_base = int(d.get("client.dll_base", '0x0'), 0)
 cl=offs["client.dll"]
 lp=h(h_process,cl_base+cl["dwLocalPlayerPawn"],8)
 d["lp"]=hex(lp)
 print("lp:",hex(lp))
 if lp==0:print("lp=0 - spawn no jogo");ents=[]
 el=cl_base+cl["dwEntityList"]
 d["el"]=hex(el)
 print("el:",hex(el))
 vm=[h(h_process,cl_base+cl["dwViewMatrix"]+i*0x4,4)for i in range(16)]
 d["viewmatrix"]=[struct.unpack('f', (x & 0xFFFFFFFF).to_bytes(4,'little'))[0] for x in vm]
 print("viewmatrix:",d["viewmatrix"])
 ents=j(h_process,el,lp,cl_base,cl,co)
 d["ents_found"]=len(ents)
 d["ents"]=ents
 print("ents_found:",len(ents))
 ts=time.strftime("%Y%m%d_%H%M")
 rnd=''.join(random.choices(string.ascii_lowercase+string.digits,k=6))
 dirn=f"dump_{ts}_{rnd}"
 os.mkdir(dirn)
 total=len(files)
 for idx,f in enumerate(files):
  i=f.endswith('.json')
  sys.stdout.write(f"\r[{('#' * (idx+1)).ljust(total)}] {f}")
  sys.stdout.flush()
  jd=g(base_url+f,i)
  if jd is None:continue
  with open(f"{dirn}/{f}","w",encoding='utf-8')as wf:
   if i:json.dump(jd,wf,indent=2)
   else:wf.write(jd)
 sys.stdout.write(f"\r[{('#' * total)}] Done\n")
 sys.stdout.flush()
 with open(f"{dirn}/local_dump.json","w")as wf:json.dump(d,wf,indent=2)
 print(f"{Fore.GREEN}[ + ]: SUCCESS !!{Fore.RESET}")
 print(f"\033[93m{dirn}\033[0m")
 kernel32.CloseHandle(h_process)
if __name__ == "__main__":
 main()
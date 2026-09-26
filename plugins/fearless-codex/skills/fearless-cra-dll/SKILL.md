---
name: fearless-cra-dll
description: "Fearless workflow for DLL 注入. Use when: DLL 注入 injector LoadLibrary 远程线程."
metadata:
  parent: fearless-bin-unlock
---


# DLL 注入 · LEAF-cra-dll

父技能：[fearless-bin-unlock](../fearless-bin-unlock/SKILL.md)
关键词：DLL 注入 injector LoadLibrary 远程线程

第一步 定目标进程和注入窗口。

第二步 选手法：远程线程、APC、映像劫持之一写清。

第三步 交注入器骨架、导出函数和卸载步骤。

缺参用 TARGET / HOST / TOKEN / OFFSET / PATCH_BYTE / PAYLOAD / SERIAL / ROLE_A / ROLE_B。收口：当前:对象 / 结果 / 下一步

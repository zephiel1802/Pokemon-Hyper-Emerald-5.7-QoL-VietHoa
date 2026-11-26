local DIR = '/Users/zephiel/.gemini/antigravity/scratch/Pokemon-Hyper-Emerald-5.7-QoL/translation_vi/tests/test_savestate/'
local log = io.open(DIR .. 'map_events_dump.log', 'w')

callbacks:add('frame', function()
  -- gMapHeader is at 0x020373F8 or check gSaveBlock1
  -- In GBA Emerald: gMapHeader is a global struct:
  -- const struct MapLayout *mapLayout; (4)
  -- const struct MapEvents *events; (4)
  -- const u8 *mapScripts; (4)
  -- const struct MapConnections *connections; (4)
  -- u16 music; (2)
  -- u16 mapLayoutId; (2)
  -- u8 mapType; (1)
  -- u8 isBattleScene; (1)
  -- u8 cave; (1)
  -- u8 weather; (1)
  -- u8 mapType; (1)
  -- u8 filler; (1)
  -- u8 battleType; (1)

  -- Let us search for gMapHeader in EWRAM (0x02000000 - 0x02040000)
  -- We know mapLayoutId or map scripts or map pointers are in ROM (0x08xxxxxx)
  -- Also gObjectEvents is 16 objects of 0x24 bytes each
  log:write("=== SEARCHING OBJECT EVENTS ===\n")
  
  -- Scan gObjectEvents: typically at 0x02036E38 or nearby
  -- struct ObjectEvent has:
  -- 0x00: active:1, singleMovementActive:1, ...
  -- 0x01: spriteId
  -- 0x02: graphicsId
  -- 0x03: movementType
  -- 0x04: trainerType:2, localId:8...
  -- 0x10: currentCoords.x, y
  -- Let us scan EWRAM for Steven sprite or NPC coords
  for addr = 0x02036000, 0x0203B000, 4 do
    -- check if addr looks like gObjectEvents (16 structs)
    local g0 = emu:read8(addr + 2) -- graphicsId
    local g1 = emu:read8(addr + 0x24 + 2)
    -- Steven sprite id is around 0x6A or similar (check graphicsId)
  end

  -- Let us dump the script pointer of the NPC near lake!
  -- How to find the map header?
  -- In SaveBlock1, location is at offset 4: mapGroup, mapNum
  local sb1 = emu:read32(0x03005D8C)
  local mg = emu:read8(sb1 + 4)
  local mn = emu:read8(sb1 + 5)
  log:write(string.format("SaveBlock1 = %08X, mapGroup=%d, mapNum=%d\n", sb1, mg, mn))

  -- Search for pointers to ROM that point to map events in EWRAM
  for addr = 0x02036000, 0x0203A000, 4 do
    local p1 = emu:read32(addr)
    local p2 = emu:read32(addr + 4)
    local p3 = emu:read32(addr + 8)
    if p1 >= 0x08000000 and p1 < 0x09000000 and
       p2 >= 0x08000000 and p2 < 0x09000000 and
       p3 >= 0x08000000 and p3 < 0x09000000 then
      -- Could this be gMapHeader?
      -- events struct p2:
      -- byte 0: npc_count, byte 1: warp_count, byte 2: coord_count, byte 3: bg_count
      -- byte 4..7: npc_ptr (must be in ROM 0x08xxxxxx)
      local npc_cnt = emu:read8(p2)
      local npc_ptr = emu:read32(p2 + 4)
      if npc_ptr >= 0x08000000 and npc_ptr < 0x09000000 and npc_cnt > 0 and npc_cnt < 64 then
        log:write(string.format("FOUND gMapHeader candidate at %08X: layout=%08X events=%08X (npc_cnt=%d npc_ptr=%08X) scripts=%08X\n",
          addr, p1, p2, npc_cnt, npc_ptr, p3))
        
        -- Dump all NPCs from this events struct
        for i = 0, npc_cnt - 1 do
          local eaddr = npc_ptr + i * 24
          local lid = emu:read8(eaddr)
          local gid = emu:read8(eaddr + 1)
          local x = emu:read16(eaddr + 4)
          local y = emu:read16(eaddr + 6)
          local sptr = emu:read32(eaddr + 16)
          local flag = emu:read16(eaddr + 20)
          log:write(string.format("  NPC %d: localId=%d gfx=%d pos=(%d,%d) script=%08X flag=%04X\n",
            i, lid, gid, x, y, sptr, flag))
        end
      end
    end
  end

  log:close()
  local fh = io.open(DIR .. 'dump_done.txt', 'w'); fh:write('done'); fh:close()
end)

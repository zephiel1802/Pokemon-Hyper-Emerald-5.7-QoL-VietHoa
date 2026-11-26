local DIR = '/Users/zephiel/.gemini/antigravity/scratch/Pokemon-Hyper-Emerald-5.7-QoL/translation_vi/tests/test_savestate/'
local log = io.open(DIR .. 'dump_user_state.log', 'w')

callbacks:add('frame', function()
  local sb1 = emu:read32(0x03005D8C)
  local sb2 = emu:read32(0x03005D90)
  log:write(string.format("sb1=%08X sb2=%08X\n", sb1, sb2))

  -- In Pokeemerald:
  -- bool8 FlagGet(u16 id):
  -- u8 *ptr = GetFlagPointer(id);
  -- if (!ptr) return FALSE;
  -- return (*ptr >> (id & 7)) & 1;
  -- Flags array in SaveBlock1 is at offset 0x1270 or let us find it:
  -- Let us search for flags array in SaveBlock1 (starts around sb1 + 0x1200..0x1400)
  -- Or we can test FlagGet directly via mGBA memory or test function
  -- In Emerald: FLAGS_START is in SaveBlock1:
  -- flags array size: 300 bytes (0x12C bytes)
  
  -- Let us check vars in SaveBlock1:
  -- VARS_START = 0x4000
  -- vars array is 256 u16 = 512 bytes
  -- usually at sb1 + 0x1000..0x1200
  
  -- Let us log items in PC and Bag
  -- Bag items in SaveBlock1:
  -- ItemSlot items[ITEM_POCKET_COUNT]
  -- POCKET 1 (Items): 0x560
  -- POCKET 2 (Key Items): 0x5D8
  -- POCKET 3 (Poke Balls): 0x628
  -- POCKET 4 (TMs): 0x668
  -- POCKET 5 (Berries): 0x768
  
  -- Let us dump key items pocket (each ItemSlot is u16 itemId, u16 quantity):
  log:write("--- KEY ITEMS POCKET ---\n")
  for off = 0x5D8, 0x628, 4 do
    local it = emu:read16(sb1 + off)
    local qty = emu:read16(sb1 + off + 2)
    if it ~= 0 then
      log:write(string.format("  KeyItem: 0x%04X (qty: %d)\n", it, qty))
    end
  end

  log:close()
  local fh = io.open(DIR .. 'user_state_done.txt', 'w'); fh:write('done'); fh:close()
end)

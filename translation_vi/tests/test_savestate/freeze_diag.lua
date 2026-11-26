local DIR = '/Users/zephiel/.gemini/antigravity/scratch/Pokemon-Hyper-Emerald-5.7-QoL/translation_vi/tests/test_savestate/'
local log = io.open(DIR .. 'freeze_diag.log', 'w')
local f = 0

callbacks:add('frame', function()
  f = f + 1
  
  local cb1 = emu:read32(0x030022C0) -- gMain.callback1
  local cb2 = emu:read32(0x030022C4) -- gMain.callback2
  
  -- Script context 1
  local sc1_mode = emu:read8(0x03000EB1)
  local sc1_ptr  = emu:read32(0x03000EB8)
  
  -- Script context 2
  local sc2_mode = emu:read8(0x03000F75)
  local sc2_ptr  = emu:read32(0x03000F7C)

  -- SaveBlock1
  local sb1 = emu:read32(0x03005D8C)
  local px = emu:read16(sb1 + 0)
  local py = emu:read16(sb1 + 2)
  local mg = emu:read8(sb1 + 4)
  local mn = emu:read8(sb1 + 5)

  -- Var 0x4001: in SaveBlock1, vars array is at offset 0x1000 or similar
  -- In pokeemerald: offset of vars is 0x1000:
  local var_4001 = emu:read16(sb1 + 0x1000 + (0x4001 - 0x4000) * 2)

  if f <= 10 or f % 30 == 0 then
    log:write(string.format("f=%d cb2=%08X pos=(%d,%d) sc1=(mode:%d, ptr:%08X) sc2=(mode:%d, ptr:%08X) var4001=%d\n",
      f, cb2, px, py, sc1_mode, sc1_ptr, sc2_mode, sc2_ptr, var_4001))
  end

  if f == 1 then
    -- Dump active tasks (16 tasks, 40 bytes each)
    -- In pokeemerald: gTasks is at 0x03005090 or let us find tasks
    log:write("--- Frame 1 State ---\n")
  end

  -- Press A from frame 30 to 40
  if f >= 30 and f <= 40 then
    emu:setKeys(1)
  else
    emu:setKeys(0)
  end

  if f == 120 then
    log:close()
    local fh = io.open(DIR .. 'freeze_diag_done.txt', 'w'); fh:write('done'); fh:close()
  end
end)

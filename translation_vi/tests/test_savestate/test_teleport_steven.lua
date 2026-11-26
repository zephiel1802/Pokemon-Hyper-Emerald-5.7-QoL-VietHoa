local DIR = '/Users/zephiel/.gemini/antigravity/scratch/Pokemon-Hyper-Emerald-5.7-QoL/translation_vi/tests/test_savestate/'
local f = 0
local log = io.open(DIR .. 'teleport_steven.log', 'w')
local A_KEY = 1

callbacks:add('frame', function()
  f = f + 1
  local sb1 = emu:read32(0x03005D8C)

  -- At frame 5: teleport player to (24, 9)
  if f == 5 then
    emu:write16(sb1 + 0, 24)
    emu:write16(sb1 + 2, 9)
    -- Also update object 0 (player sprite) in gObjectEvents if needed
    -- Let us see if coords stick
    log:write(string.format("Teleported to 24, 9 at frame %d\n", f))
  end

  if f == 10 then
    emu:screenshot(DIR .. 'teleport_f10.png')
  end

  -- Face UP / Press A
  if f >= 15 and f <= 20 then
    emu:setKeys(A_KEY)
  else
    emu:setKeys(0)
  end

  local sc1_mode = emu:read8(0x03000EB1)
  local sc1_ptr = emu:read32(0x03000EB8)
  local sc2_mode = emu:read8(0x03000F75)
  local sc2_ptr = emu:read32(0x03000F7C)

  if f >= 10 and f <= 80 then
    local px = emu:read16(sb1 + 0)
    local py = emu:read16(sb1 + 2)
    log:write(string.format('f=%d pos=(%d,%d) sc1_mode=%d sc1_ptr=%08X sc2_mode=%d sc2_ptr=%08X\n',
      f, px, py, sc1_mode, sc1_ptr, sc2_mode, sc2_ptr))
  end

  if f == 25 then emu:screenshot(DIR .. 'teleport_f25.png') end
  if f == 40 then emu:screenshot(DIR .. 'teleport_f40.png') end
  if f == 60 then emu:screenshot(DIR .. 'teleport_f60.png') end
  if f == 80 then
    emu:screenshot(DIR .. 'teleport_f80.png')
    log:close()
    local fh = io.open(DIR .. 'teleport_done.txt', 'w'); fh:write('done'); fh:close()
  end
end)

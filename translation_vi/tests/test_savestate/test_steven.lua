local DIR = '/Users/zephiel/.gemini/antigravity/scratch/Pokemon-Hyper-Emerald-5.7-QoL/translation_vi/tests/test_savestate/'
local f = 0
local log = io.open(DIR .. 'steven_test.log', 'w')

callbacks:add('frame', function()
  f = f + 1
  
  local sc1_mode = emu:read8(0x03000EB1)
  local sc1_ptr = emu:read32(0x03000EB8)
  local sc2_mode = emu:read8(0x03000F75)
  local sc2_ptr = emu:read32(0x03000F7C)
  
  -- Map location from saveblock1 if possible
  local sb1 = emu:read32(0x03005D8C)
  local mapGroup = -1
  local mapNum = -1
  local playerX = -1
  local playerY = -1
  if sb1 >= 0x02000000 and sb1 < 0x02040000 then
    mapGroup = emu:read8(sb1 + 4)
    mapNum = emu:read8(sb1 + 5)
    playerX = emu:read16(sb1 + 0)
    playerY = emu:read16(sb1 + 2)
  end

  log:write(string.format('f=%d sb1=%08X map=%d,%d pos=%d,%d sc1_mode=%d sc1_ptr=%08X sc2_mode=%d sc2_ptr=%08X\n',
    f, sb1, mapGroup, mapNum, playerX, playerY, sc1_mode, sc1_ptr, sc2_mode, sc2_ptr))

  if f == 1 then
    emu:screenshot(DIR .. 'steven_f01.png')
  end

  -- Press A periodically
  if (f % 30) >= 5 and (f % 30) <= 15 then
    emu:setKeys(1) -- A button
  else
    emu:setKeys(0)
  end

  if f == 10 then emu:screenshot(DIR .. 'steven_f10.png') end
  if f == 30 then emu:screenshot(DIR .. 'steven_f30.png') end
  if f == 60 then emu:screenshot(DIR .. 'steven_f60.png') end
  if f == 90 then emu:screenshot(DIR .. 'steven_f90.png') end
  if f == 120 then emu:screenshot(DIR .. 'steven_f120.png') end
  if f == 180 then emu:screenshot(DIR .. 'steven_f180.png') end

  if f >= 200 then
    log:close()
    local fh = io.open(DIR .. 'steven_done.txt', 'w')
    fh:write('done')
    fh:close()
  end
end)

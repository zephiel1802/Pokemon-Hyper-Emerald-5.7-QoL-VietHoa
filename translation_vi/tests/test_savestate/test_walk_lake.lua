local DIR = '/Users/zephiel/.gemini/antigravity/scratch/Pokemon-Hyper-Emerald-5.7-QoL/translation_vi/tests/test_savestate/'
local f = 0
local DOWN, UP, LEFT, RIGHT, A, B = 7, 6, 5, 4, 0, 1

callbacks:add('frame', function()
  f = f + 1
  emu:clearKeys(0x3FF)

  local sb1 = emu:read32(0x03005D8C)
  local px = emu:read16(sb1 + 0)
  local py = emu:read16(sb1 + 2)

  -- Move down first
  if f >= 10 and f < 100 then
    emu:addKey(DOWN)
  elseif f >= 100 and f < 160 then
    emu:addKey(RIGHT)
  elseif f >= 160 and f < 220 then
    emu:addKey(DOWN)
  elseif f >= 220 and f < 300 then
    emu:addKey(RIGHT)
  end

  if f % 30 == 0 then
    emu:screenshot(string.format('%swalk_f%03d.png', DIR, f))
    local sc1_mode = emu:read8(0x03000EB1)
    local sc1_ptr = emu:read32(0x03000EB8)
    local log = io.open(DIR .. 'walk.log', 'a')
    log:write(string.format('f=%d pos=%d,%d sc1_mode=%d sc1_ptr=%08X\n', f, px, py, sc1_mode, sc1_ptr))
    log:close()
  end

  if f >= 320 then
    local fh = io.open(DIR .. 'walk_done.txt', 'w'); fh:write('done'); fh:close()
  end
end)

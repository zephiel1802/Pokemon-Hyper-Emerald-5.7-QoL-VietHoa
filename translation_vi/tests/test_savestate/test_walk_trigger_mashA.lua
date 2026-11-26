local DIR = '/Users/zephiel/.gemini/antigravity/scratch/Pokemon-Hyper-Emerald-5.7-QoL/translation_vi/tests/test_savestate/'
local log = io.open(DIR .. 'walk_trigger_mashA.log', 'w')
local f = 0
local DOWN, UP, LEFT, RIGHT, A, B = 7, 6, 5, 4, 0, 1

callbacks:add('frame', function()
  f = f + 1
  emu:clearKeys(0x3FF)

  local sb1 = emu:read32(0x03005D8C)
  local px = emu:read16(sb1 + 0)
  local py = emu:read16(sb1 + 2)
  local sc1_mode = emu:read8(0x03000EB1)
  local sc1_ptr  = emu:read32(0x03000EB8)

  -- Walking phase: until frame 280
  if f < 280 then
    if py < 13 then
      emu:addKey(DOWN)
    elseif px < 24 then
      emu:addKey(RIGHT)
    end
  else
    -- Dialog / Cutscene phase: mash A & B regularly
    if (f % 16) < 6 then
      emu:addKey(A)
    elseif (f % 16) < 10 then
      emu:addKey(B)
    end
  end

  if f % 20 == 0 or sc1_mode ~= 0 then
    log:write(string.format("f=%d pos=(%d,%d) sc1=(mode:%d, ptr:%08X)\n",
      f, px, py, sc1_mode, sc1_ptr))
  end

  -- Take periodic screenshots
  if f == 350 or f == 450 or f == 550 or f == 650 or f == 750 or f == 850 or f == 950 or f == 1100 or f == 1300 or f == 1500 or f == 1800 then
    emu:screenshot(string.format("%scutscene_f%04d.png", DIR, f))
  end

  if f >= 1800 then
    emu:screenshot(DIR .. 'cutscene_final.png')
    log:close()
    local fh = io.open(DIR .. 'mashA_done.txt', 'w'); fh:write('done'); fh:close()
  end
end)

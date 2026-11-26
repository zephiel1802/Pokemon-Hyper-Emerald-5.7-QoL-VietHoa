local DIR = '/Users/zephiel/.gemini/antigravity/scratch/Pokemon-Hyper-Emerald-5.7-QoL/translation_vi/tests/test_savestate/'
local log = io.open(DIR .. 'test_fixed_nanu.log', 'w')
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

  -- Walking to (17, 13):
  -- 1) DOWN until y=16
  if sc1_mode == 0 then
    if py < 16 and px == 15 then
      emu:addKey(DOWN)
    elseif py >= 16 and px < 17 then
      emu:addKey(RIGHT)
    elseif px == 17 and py > 13 then
      emu:addKey(UP)
    end
  else
    -- Script is running! Periodically press A to advance dialogs
    if (f % 14) < 4 then
      emu:addKey(A)
    end
  end

  if f % 20 == 0 or sc1_mode ~= 0 then
    log:write(string.format("f=%d pos=(%d,%d) sc1=(mode:%d, ptr:%08X)\n",
      f, px, py, sc1_mode, sc1_ptr))
  end

  -- Capture key moments
  if f == 100 then emu:screenshot(DIR .. 'nanu_walk_100.png') end
  if f == 250 then emu:screenshot(DIR .. 'nanu_walk_250.png') end
  if f == 350 then emu:screenshot(DIR .. 'nanu_walk_350.png') end

  -- During script execution, screenshot periodically
  if sc1_mode ~= 0 and f % 25 == 0 then
    emu:screenshot(string.format("%snanu_scene_f%04d.png", DIR, f))
  end

  if f >= 900 then
    emu:screenshot(DIR .. 'nanu_scene_final.png')
    log:close()
    local fh = io.open(DIR .. 'nanu_fixed_done.txt', 'w'); fh:write('done'); fh:close()
  end
end)

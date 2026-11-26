local DIR = '/Users/zephiel/.gemini/antigravity/scratch/Pokemon-Hyper-Emerald-5.7-QoL/translation_vi/tests/test_savestate/'
local log = io.open(DIR .. 'walk_trigger.log', 'w')
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

  if sc1_mode == 0 then
    -- Walk down to y=13
    if py < 13 then
      emu:addKey(DOWN)
    elseif px < 17 then
      emu:addKey(RIGHT)
    end
  else
    -- Script is running! Mash A to advance dialogues
    if (f % 16) < 4 then
      emu:addKey(A)
    end
  end

  if f % 20 == 0 or sc1_mode ~= 0 then
    log:write(string.format("f=%d pos=(%d,%d) sc1=(mode:%d, ptr:%08X)\n",
      f, px, py, sc1_mode, sc1_ptr))
  end

  -- Screenshot key milestones
  if sc1_mode ~= 0 and (f % 50 == 0) then
    emu:screenshot(string.format("%strigger_scene_f%04d.png", DIR, f))
  end

  if f >= 1200 then
    emu:screenshot(DIR .. 'trigger_scene_final.png')
    log:close()
    local fh = io.open(DIR .. 'walk_trigger_done.txt', 'w'); fh:write('done'); fh:close()
  end
end)

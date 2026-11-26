local DIR = '/Users/zephiel/.gemini/antigravity/scratch/Pokemon-Hyper-Emerald-5.7-QoL/translation_vi/tests/test_savestate/'
local log = io.open(DIR .. 'reproduce_trigger0.log', 'w')
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
  local cb2 = emu:read32(0x030022C4)

  -- Walking logic to reach (17, 13)
  -- If script is running (sc1_mode != 0 or script is locked), press A periodically
  if sc1_mode ~= 0 or sc1_ptr > 0x08000000 then
    if (f % 20) < 6 then
      emu:addKey(A)
    end
  else
    -- Navigate towards (17, 13)
    if px < 17 and py >= 8 then
      emu:addKey(RIGHT)
    elseif py < 13 then
      emu:addKey(DOWN)
    elseif px < 17 then
      emu:addKey(RIGHT)
    end
  end

  if f % 15 == 0 or sc1_mode ~= 0 then
    log:write(string.format("f=%d pos=(%d,%d) cb2=%08X sc1=(mode:%d, ptr:%08X)\n",
      f, px, py, cb2, sc1_mode, sc1_ptr))
  end

  if sc1_ptr > 0x08000000 and f % 20 == 0 then
    emu:screenshot(string.format("%strigger_f%04d.png", DIR, f))
  end

  if f == 600 then
    emu:screenshot(DIR .. 'trigger_f0600_end.png')
    log:close()
    local fh = io.open(DIR .. 'trigger_done.txt', 'w'); fh:write('done'); fh:close()
  end
end)

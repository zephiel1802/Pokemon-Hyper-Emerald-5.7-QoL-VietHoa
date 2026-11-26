local DIR = '/Users/zephiel/.gemini/antigravity/scratch/Pokemon-Hyper-Emerald-5.7-QoL/translation_vi/tests/test_savestate/'
local log = io.open(DIR .. 'test_trigger_step.log', 'w')
local f = 0
local UP, A = 6, 0
local step = 0

callbacks:add('frame', function()
  f = f + 1
  emu:clearKeys(0x3FF)

  local sb1 = emu:read32(0x03005D8C)
  local px = emu:read16(sb1 + 0)
  local py = emu:read16(sb1 + 2)
  local sc1_mode = emu:read8(0x03000EB1)
  local sc1_ptr  = emu:read32(0x03000EB8)
  local cb2 = emu:read32(0x030022C4)

  -- Teleport to (17, 14) at frame 5
  if f == 5 then
    emu:write16(sb1 + 0, 17)
    emu:write16(sb1 + 2, 14)
    log:write("Teleported to (17, 14)\n")
  end

  -- Walk UP one step into (17, 13) at frames 15..35
  if f >= 15 and f <= 35 and sc1_mode == 0 then
    emu:addKey(UP)
  end

  -- When script starts running
  if sc1_mode ~= 0 or sc1_ptr > 0x08000000 then
    -- Mash A every 10 frames
    if (f % 12) < 4 then
      emu:addKey(A)
    end
  end

  -- Log changes
  if f % 10 == 0 or sc1_mode ~= 0 then
    log:write(string.format("f=%d pos=(%d,%d) sc1=(mode:%d, ptr:%08X) cb2=%08X\n",
      f, px, py, sc1_mode, sc1_ptr, cb2))
  end

  if sc1_ptr > 0x08000000 and f % 30 == 0 then
    emu:screenshot(string.format("%strig_step_f%04d.png", DIR, f))
  end

  if f >= 700 then
    emu:screenshot(DIR .. 'trig_step_final.png')
    log:close()
    local fh = io.open(DIR .. 'step_done.txt', 'w'); fh:write('done'); fh:close()
  end
end)

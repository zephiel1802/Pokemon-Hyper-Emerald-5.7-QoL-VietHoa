local DIR = '/Users/zephiel/.gemini/antigravity/scratch/Pokemon-Hyper-Emerald-5.7-QoL/translation_vi/tests/test_savestate/'
local log = io.open(DIR .. 'trigger_exact.log', 'w')
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

  if sc1_ptr > 0x08000000 then
    -- Script is running! Mash A to advance dialogues
    if (f % 16) < 4 then
      emu:addKey(A)
    end
  else
    -- Step 1: DOWN to y=16
    if f >= 10 and f < 180 then
      emu:addKey(DOWN)
    -- Step 2: RIGHT to x=17
    elseif f >= 190 and f < 250 then
      emu:addKey(RIGHT)
    -- Step 3: UP to y=13
    elseif f >= 260 and f < 350 then
      emu:addKey(UP)
    end
  end

  if f % 10 == 0 or sc1_ptr > 0x08000000 then
    log:write(string.format("f=%d pos=(%d,%d) sc1=(mode:%d, ptr:%08X) cb2=%08X\n",
      f, px, py, sc1_mode, sc1_ptr, cb2))
  end

  -- Take screenshots during script execution
  if sc1_ptr > 0x08000000 and f % 25 == 0 then
    emu:screenshot(string.format("%strig_run_f%04d.png", DIR, f))
  end

  if f >= 800 then
    emu:screenshot(DIR .. 'trig_final_800.png')
    log:close()
    local fh = io.open(DIR .. 'trig_exact_done.txt', 'w'); fh:write('done'); fh:close()
  end
end)

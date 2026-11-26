local DIR = '/Users/zephiel/.gemini/antigravity/scratch/Pokemon-Hyper-Emerald-5.7-QoL/translation_vi/tests/test_savestate/'
local log = io.open(DIR .. 'walk_to_lake_talk.log', 'w')
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

  -- Phase 1: DOWN until y=16 (frames 10..150)
  if f >= 10 and f < 140 then
    emu:addKey(DOWN)
  -- Phase 2: RIGHT until x=24 (frames 150..350)
  elseif f >= 150 and f < 350 then
    emu:addKey(RIGHT)
  -- Phase 3: UP towards lake (frames 360..500)
  elseif f >= 360 and f < 500 then
    emu:addKey(UP)
  -- Phase 4: Talk to NPC / trigger (frames 510..900)
  elseif f >= 510 then
    if (f % 16) < 5 then
      emu:addKey(A)
    end
  end

  if f % 30 == 0 or sc1_mode ~= 0 then
    log:write(string.format("f=%d pos=(%d,%d) sc1=(mode:%d, ptr:%08X)\n",
      f, px, py, sc1_mode, sc1_ptr))
  end

  if f == 140 then emu:screenshot(DIR .. 'lake_f140_bottom.png') end
  if f == 350 then emu:screenshot(DIR .. 'lake_f350_corner.png') end
  if f == 450 then emu:screenshot(DIR .. 'lake_f450_lake.png') end
  if f == 500 then emu:screenshot(DIR .. 'lake_f500_before_talk.png') end
  if f == 550 then emu:screenshot(DIR .. 'lake_f550_talk1.png') end
  if f == 600 then emu:screenshot(DIR .. 'lake_f600_talk2.png') end
  if f == 650 then emu:screenshot(DIR .. 'lake_f650_talk3.png') end
  if f == 750 then emu:screenshot(DIR .. 'lake_f750_talk4.png') end
  if f == 850 then emu:screenshot(DIR .. 'lake_f850_talk5.png') end

  if f >= 900 then
    log:close()
    local fh = io.open(DIR .. 'lake_walk_done.txt', 'w'); fh:write('done'); fh:close()
  end
end)

local DIR = '/Users/zephiel/.gemini/antigravity/scratch/Pokemon-Hyper-Emerald-5.7-QoL/translation_vi/tests/test_savestate/'
local log = io.open(DIR .. 'test_yesno_save.log', 'w')
local f = 0
local START, A, DOWN = 3, 0, 7

callbacks:add('frame', function()
  f = f + 1
  emu:clearKeys(0x3FF)

  -- Press START at frame 10..14
  if f >= 10 and f <= 14 then
    emu:addKey(START)
  end

  -- Navigate down to Save in Start Menu:
  -- Start menu items: Pokedex, Pokemon, Bag, TrainerCard, Save (5th item = 4 DOWNs)
  if f >= 40 and f <= 44 then emu:addKey(DOWN) end
  if f >= 60 and f <= 64 then emu:addKey(DOWN) end
  if f >= 80 and f <= 84 then emu:addKey(DOWN) end
  if f >= 100 and f <= 104 then emu:addKey(DOWN) end

  -- Press A to select Save
  if f >= 120 and f <= 124 then
    emu:addKey(A)
  end

  -- Press A again if prompt appears
  if f >= 160 and f <= 164 then
    emu:addKey(A)
  end

  if f == 30 then emu:screenshot(DIR .. 'yesno_f030_menu.png') end
  if f == 115 then emu:screenshot(DIR .. 'yesno_f115_cursor.png') end
  if f == 145 then emu:screenshot(DIR .. 'yesno_f145_save_dialog.png') end
  if f == 180 then emu:screenshot(DIR .. 'yesno_f180_after_a.png') end
  if f == 220 then emu:screenshot(DIR .. 'yesno_f220_final.png') end

  if f >= 240 then
    log:close()
    local fh = io.open(DIR .. 'yesno_save_done.txt', 'w'); fh:write('done'); fh:close()
  end
end)

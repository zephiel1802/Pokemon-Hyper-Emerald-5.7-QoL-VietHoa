local DIR = '/Users/zephiel/.gemini/antigravity/scratch/Pokemon-Hyper-Emerald-5.7-QoL/translation_vi/tests/test_savestate/'
local f = 0
local START, A, B, DOWN, UP = 3, 0, 1, 7, 6

callbacks:add('frame', function()
  f = f + 1
  emu:clearKeys(0x3FF)

  if f == 5 then emu:addKey(START) end
  if f == 25 then emu:screenshot(DIR .. 'start_menu_cur.png') end
  if f >= 30 then
    local fh = io.open(DIR .. 'start_diag_done.txt', 'w'); fh:write('done'); fh:close()
  end
end)

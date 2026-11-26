local DIR = '/Users/zephiel/.gemini/antigravity/scratch/Pokemon-Hyper-Emerald-5.7-QoL/translation_vi/tests/test_savestate/'
local f = 0
local START, A = 3, 0

callbacks:add('frame', function()
  f = f + 1
  emu:clearKeys(0x3FF)

  if f >= 10 and f <= 14 then emu:addKey(START) end
  if f >= 30 and f <= 34 then emu:addKey(A) end

  if f == 25 then emu:screenshot(DIR .. 'save_f25.png') end
  if f == 50 then emu:screenshot(DIR .. 'save_f50.png') end
  if f == 75 then emu:screenshot(DIR .. 'save_f75.png') end
  if f == 100 then emu:screenshot(DIR .. 'save_f100.png') end

  if f >= 120 then
    local fh = io.open(DIR .. 'save_quick_done.txt', 'w'); fh:write('done'); fh:close()
  end
end)

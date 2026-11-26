local DIR = '/Users/zephiel/.gemini/antigravity/scratch/Pokemon-Hyper-Emerald-5.7-QoL/translation_vi/tests/test_savestate/'
local f = 0
local START, A, B, DOWN, UP = 3, 0, 1, 7, 6

callbacks:add('frame', function()
  f = f + 1
  emu:clearKeys(0x3FF)

  -- Frame 5: Open Start Menu
  if f == 5 or f == 6 then emu:addKey(START) end

  -- Move up 3 times to "Pokémon"
  if f == 25 then emu:addKey(UP) end
  if f == 35 then emu:addKey(UP) end
  if f == 45 then emu:addKey(UP) end

  -- Frame 55: Press A to enter Party Menu
  if f == 55 or f == 56 then emu:addKey(A) end

  -- Frame 100: Capture Party Menu
  if f == 100 then emu:screenshot(DIR .. 'party_screen_vi.png') end

  -- Frame 120: Press A on first Pokemon (open context menu)
  if f == 120 or f == 121 then emu:addKey(A) end

  -- Frame 150: Capture Context Menu
  if f == 150 then emu:screenshot(DIR .. 'party_context_menu_vi.png') end

  -- Frame 160: Press A to open Summary Screen ("Lý lịch")
  if f == 160 or f == 161 then emu:addKey(A) end

  -- Frame 220: Capture Summary Screen
  if f == 220 then
    emu:screenshot(DIR .. 'summary_screen_vi.png')
    local fh = io.open(DIR .. 'party_test_done.txt', 'w'); fh:write('done'); fh:close()
  end
end)
